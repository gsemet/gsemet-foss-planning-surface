"""(file, SwRS) test-marker pairs of a base that are gone at the head; per-file line counts for main's requirements."""
import collections
import re
import subprocess
import sys

REPO, BASE, HEAD = sys.argv[1:4]
PAT = r"@(tests_req|accepts_req) SwRS-MDOKFSTUDIO-"


def grep(rev):
    p = subprocess.run(["git", "-C", REPO, "grep", "-n", "-E", PAT, rev, "--", "test", "src", "scripts", "sphinx", "tests"], capture_output=True)
    out = []
    for l in p.stdout.decode("utf-8", "replace").split("\n"):
        m = re.match(r"^[^:]+:([^:]+):(\d+):.*?@(?:tests_req|accepts_req) SwRS-MDOKFSTUDIO-([A-Z]+-\d+)(#S\d+)?", l)
        if m:
            out.append((m.group(1), int(m.group(2)), m.group(3), m.group(4) or ""))
    return out


b, h = grep(BASE), grep(HEAD)
bp = {(f, r) for f, n, r, s in b}
hp = {(f, r) for f, n, r, s in h}
gone = sorted(bp - hp)
print("base pairs", len(bp), "gone at head", len(gone), "new at head", len(hp - bp))
integ = collections.defaultdict(set)
for f, r in bp:
    if f.startswith("test/integration/"):
        integ[r].add(f)
integ_h = {r for f, r in hp if f.startswith("test/integration/")}
lost = sorted(set(integ) - integ_h)
print("SwRS with a test/integration marker at base and none at head:", len(lost), lost)
named = ["TRUST-005", "TRUST-090", "REVIEW-219", "LIFE-169", "LIFE-170"]
for r in named:
    print(r, "gone from integration files:", sorted(f for f, x in gone if x == r and f.startswith("test/integration/")))
allh = {r for f, r in hp}
print("SwRS with a test marker at base and none at head:", sorted({r for f, r in bp} - allh))
if len(sys.argv) > 4:
    for f, r in gone:
        print("  gone", f, r)
