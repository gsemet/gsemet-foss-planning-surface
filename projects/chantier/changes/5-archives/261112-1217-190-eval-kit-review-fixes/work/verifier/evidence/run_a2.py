import importlib.util, subprocess, sys, pathlib
KIT = pathlib.Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-13-CR-190\evals\kit")
scratch = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(KIT))
import sandbox

text = "\n".join([
    "aaa\tHEAD", "aaa\trefs/heads/main", "bbb\trefs/pull/7/head", "ccc\trefs/pull/7/merge",
    "ddd\trefs/tags/v0.2.0", "eee\trefs/tags/v0.2.0^{}"])
refs = sandbox.parse_refs(text)
print("parse_refs ->", refs)
print("ref_problems(that, base=aaa) ->", sandbox.ref_problems(refs, "aaa"))
print("ref_problems({main: base}) ->", sandbox.ref_problems({"refs/heads/main": "aaa"}, "aaa"))
print("ref_problems(main elsewhere, branch x) ->",
      sandbox.ref_problems({"refs/heads/main": "zzz", "refs/heads/x": "q"}, "aaa"))

def git(*a, cwd=None):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()

ref = scratch / "ref"
r = subprocess.run([sys.executable, str(KIT / "sandbox.py"), "build", str(ref)], capture_output=True, text=True)
print("sandbox.py build exit", r.returncode, r.stdout.strip().splitlines()[-2:], r.stderr.strip()[-200:])
base = git("rev-parse", "HEAD", cwd=ref)
bare = scratch / "bare.git"
git("init", "--bare", "-b", "main", str(bare))
git("push", str(bare), "HEAD:refs/heads/main", cwd=ref)
git("update-ref", "refs/pull/1/head", base, cwd=bare)
print("bare refs (all):", git("for-each-ref", "--format=%(refname)", cwd=bare).split())
got = sandbox.remote_refs(str(bare))
print("remote_refs(bare) ->", got, "== {main: base}:", got == {"refs/heads/main": base})
print("ref_problems ->", sandbox.ref_problems(got, base))

# d72df44's logic: remote_refs kept every ref but HEAD and peeled; verify demanded the whole map
old = {}
for line in git("ls-remote", str(bare)).splitlines():
    sha, _, name = line.partition("\t")
    if name != "HEAD" and not name.endswith("^{}"):
        old[name] = sha
print("d72df44 whole-map comparison: map =", old)
print("d72df44 verify problem:", f"refs are {old}, expected only refs/heads/main at {base}" if old != {"refs/heads/main": base} else "none")
