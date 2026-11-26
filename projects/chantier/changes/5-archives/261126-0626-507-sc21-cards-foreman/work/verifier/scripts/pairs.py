"""Before (base) and after (head) readings: bytes of the card files, the file counts and the diff."""

import subprocess

B = "<CR folder>/work/scratch/ver/base"
W = "<worktree>"
CN = "skills/chantier/cards-next"


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8").stdout


for label, cwd in (("before (base)", B), ("after (head)", W)):
    print(f"== {label} {git(cwd, 'rev-parse', 'HEAD').strip()}")
    sizes = {}
    for line in git(cwd, "ls-tree", "-r", "-l", "HEAD", CN, "evals/quiz/chief-of-staff").splitlines():
        meta, path = line.split("\t")
        sizes[path] = int(meta.split()[3])
    cards = [p for p in sizes if p.startswith(CN)]
    print("files under cards-next:", len(cards), "| quiz cases under evals/quiz/chief-of-staff:", len(sizes) - len(cards))
    for name in ("foreman", "chief-of-staff", "griller-skill", "griller", "concepts", "pr-template", "review-step",
                 "cr-driver", "stack-driver", "release-driver", "qa-driver", "floor"):
        print(f"  {name}.md: {sizes.get(f'{CN}/{name}.md', 'absent')}")
print("== diff base..head")
stat = git(W, "diff", "--stat", "24111e6d..HEAD").splitlines()
print(stat[-1])
status = git(W, "diff", "--name-status", "24111e6d..HEAD").splitlines()
print("by status:", {k: sum(1 for s in status if s[0] == k) for k in {s[0] for s in status}})
print("outside cards-next:", [s for s in status if f"\t{CN}/" not in s])
print("== git diff 24111e6d..HEAD -- skills/chantier/cards-next/griller.md")
print(git(W, "diff", "24111e6d..HEAD", "--", f"{CN}/griller.md"))
