import subprocess, sys, yaml

WT = sys.argv[1]
def git(*a):
    return subprocess.run(["git", "-C", WT, *a], capture_output=True, text=True, encoding="utf-8").stdout

base = git("merge-base", "origin/main", "HEAD").strip()
files = [l.split("\t") for l in git("diff", "--name-status", base, "HEAD", "--", "requirements/tiers/").splitlines()]

def split(text):
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm) or {}, body

for st, path in files:
    if not path.endswith(".md") or path.endswith("index.md") or path.endswith("log.md"):
        continue
    old = git("show", f"{base}:{path}") if st != "A" else ""
    new = git("show", f"HEAD:{path}")
    ofm, ob = split(old) if old else ({}, "")
    nfm, nb = split(new)
    print(f"== {st} {path.rsplit('/',1)[-1]}")
    for k in sorted(set(ofm) | set(nfm)):
        if ofm.get(k) != nfm.get(k):
            print(f"   {k}: {ofm.get(k)!r} -> {nfm.get(k)!r}")
    print(f"   body changed: {ob.strip() != nb.strip()}")
