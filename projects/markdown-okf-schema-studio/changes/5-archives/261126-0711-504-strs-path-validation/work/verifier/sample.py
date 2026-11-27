"""Random sample of SwRS fragment markers at a revision: marker, scenario title, the code under it.

usage: uv run --no-project --with pyyaml python -I sample.py <worktree> <rev> <seed> <count>
"""
import random
import re
import subprocess
import sys

import yaml

REPO, REV, SEED, COUNT = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
MARK = re.compile(r"@tests_req\s+(SwRS-[A-Za-z0-9]+-[A-Z]+-\d+)#(S\d+)")


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True).stdout.decode("utf-8", "replace").replace("\r\n", "\n")


hits = []
for line in git("grep", "-n", "-I", "-E", "@tests_req SwRS-[A-Za-z0-9]+-[A-Z]+-[0-9]+#S[0-9]+", REV, "--", "test").split("\n"):
    parts = line.split(":", 3)
    if len(parts) == 4 and MARK.search(parts[3]):
        m = MARK.search(parts[3])
        hits.append((parts[1], int(parts[2]), m.group(1), m.group(2)))
files = {l.rsplit("/", 1)[1][:-3]: l for l in git("ls-tree", "-r", "--name-only", REV, "requirements/tiers/swrs").split("\n") if l.endswith(".md")}
random.seed(SEED)
print("SwRS fragment marker lines", len(hits))
for path, number, rid, frag in random.sample(hits, COUNT):
    front = yaml.safe_load(git("show", f"{REV}:{files[rid]}").split("\n---", 1)[0][4:])
    scen = {s["id"]: s["title"] for s in front.get("scenarios", [])}
    src = git("show", f"{REV}:{path}").split("\n")
    i = number
    while i < len(src) and (not src[i].strip() or src[i].strip().startswith(("//", "#", "/*", "*"))):
        i += 1
    print("=" * 100)
    print(f"{path}:{number} {rid}#{frag}: {scen.get(frag)}")
    print("   all scenarios:", "; ".join(f"{k} {v}" for k, v in scen.items()))
    for l in src[i:i + 22]:
        print("   |", l[:170])
