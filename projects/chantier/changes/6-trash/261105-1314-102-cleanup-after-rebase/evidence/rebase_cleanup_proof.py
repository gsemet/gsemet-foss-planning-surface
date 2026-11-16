"""Proof for CR-102: after a rebase merge, `git branch -d` refuses; the Foreman card's steps work.

Run: python rebase_cleanup_proof.py
Throwaway repository and bare remote in a temporary folder. No forge is used: the forge check
("the CR's PR is merged") is STOOD IN FOR by the rebase merge done locally and pushed to the
bare remote, which is what a forge's "rebase and merge" button does.
"""
import subprocess
import sys
import tempfile
from pathlib import Path


def git(cwd, *args, check=True):
    r = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=cwd,
                       capture_output=True, text=True)
    print(f"$ git {' '.join(args)}   [{Path(cwd).name}]")
    for line in (r.stdout + r.stderr).strip().splitlines():
        print("  " + line)
    if check and r.returncode:
        sys.exit(f"unexpected failure ({r.returncode})")
    return r


with tempfile.TemporaryDirectory() as tmp:
    t = Path(tmp)
    bare, repo, wt = t / "remote.git", t / "repo", t / "repo.worktrees" / "b-CR-1"
    git(t, "init", "--bare", "-b", "main", str(bare))
    git(t, "clone", str(bare), str(repo))
    (repo / "a.txt").write_text("a\n")
    git(repo, "add", "."); git(repo, "commit", "-m", "base"); git(repo, "push", "origin", "HEAD:main")
    git(repo, "worktree", "add", "-b", "chantier/b/cr-1-x", str(wt), "origin/main")
    (wt / "f.txt").write_text("f\n")
    git(wt, "add", "."); git(wt, "commit", "-m", "cr work"); git(wt, "push", "origin", "HEAD")
    # another change lands on main meanwhile, so the rebase merge rewrites the CR's commit
    (repo / "b.txt").write_text("b\n")
    git(repo, "add", "."); git(repo, "commit", "-m", "other"); git(repo, "push", "origin", "HEAD:main")
    print("--- rebase merge (what the forge does), pushed to the remote's main")
    git(repo, "checkout", "-b", "tmp-rebase", "origin/main")
    git(repo, "cherry-pick", "chantier/b/cr-1-x")
    git(repo, "push", "origin", "HEAD:main"); git(repo, "checkout", "main"); git(repo, "pull")
    git(repo, "fetch", "origin")
    print("--- old way: refuses, the rebased commit has another hash")
    git(repo, "worktree", "remove", str(wt))
    r = git(repo, "branch", "-d", "chantier/b/cr-1-x", check=False)
    assert r.returncode != 0 and "not fully merged" in r.stderr, "expected -d to refuse"
    print("--- card's steps: PR merged (stand-in, see header), then -D from the main checkout")
    git(repo, "branch", "-D", "chantier/b/cr-1-x")
    out = git(repo, "branch", "--list", "chantier/*")
    assert not out.stdout.strip(), "branch still there"
    print("RESULT: -d refused after the rebase merge; worktree remove + branch -D removed it")
