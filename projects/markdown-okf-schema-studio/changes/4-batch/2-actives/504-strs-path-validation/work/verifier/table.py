"""Check each row of the PR body's StRS marker table against the revisions."""
import collections
import re
import subprocess
import sys

REPO, BODY, BEFORE, HEAD = sys.argv[1:5]
cache = {}


def lines(rev, path):
    if (rev, path) not in cache:
        p = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"], capture_output=True)
        cache[(rev, path)] = p.stdout.decode("utf-8", "replace").split("\n") if p.returncode == 0 else None
    return cache[(rev, path)]


rows = []
for line in open(BODY, encoding="utf-8"):
    m = re.match(r"^\| (test/\S+) \| (\d+) \| (StRS-\S+) \| ([^|]+?) \| ([^|]+?) \| (\d+|-) \|", line)
    if m:
        rows.append(m.groups())
print("rows", len(rows), "classes", dict(collections.Counter(r[3] for r in rows)))
bad = []
for f, old, rid, cls, out, now in rows:
    t = lines(BEFORE, f)
    if t is None or rid not in t[int(old) - 1]:
        bad.append(("before", f, old, rid))
    if now != "-":
        h = lines(HEAD, f)
        verb, frag = out.split()
        if h is None or f"{verb} {rid}{frag}" not in h[int(now) - 1]:
            bad.append(("now", f, now, rid, out, (h or [""] * 10000)[int(now) - 1].strip() if h else None))
print("bad rows", len(bad))
for b in bad:
    print("  ", b)

# set comparison with the files themselves
def scan(rev):
    p = subprocess.run(["git", "-C", REPO, "grep", "-n", "-E", r"@(tests_req|accepts_req) StRS-MDOKFSTUDIO-", rev, "--",
                        "test", "src", "scripts", "sphinx"], capture_output=True)
    out = []
    for l in p.stdout.decode("utf-8", "replace").split("\n"):
        m = re.match(r"^[^:]+:([^:]+):(\d+):.*?@(tests_req|accepts_req) (StRS-MDOKFSTUDIO-[A-Z]+-\d+)(#S\d+)?", l)
        if m:
            out.append((m.group(1), int(m.group(2)), m.group(3), m.group(4), m.group(5) or ""))
    return out


for rev in ("4a47151e", BEFORE, HEAD):
    s = scan(rev)
    print(rev, "StRS marker lines", len(s), "files", len({x[0] for x in s}))
now_set = {(f, int(n)) for f, _, _, _, _, n in rows if n != "-"}
print("head markers without a table row:", [x for x in scan(HEAD) if (x[0], x[1]) not in now_set])
before_set = {(f, int(n)) for f, n, *_ in rows}
print("e5ee markers without a row:", [x for x in scan(BEFORE) if (x[0], x[1]) not in before_set])
head_pairs = {(x[0], x[3]) for x in scan(HEAD)}
rm = [(f, rid) for f, n, rid, cls, out, now in rows if now == "-"]
print("removed rows whose file still names the StRS:", sorted({r for r in rm if r in head_pairs}))
