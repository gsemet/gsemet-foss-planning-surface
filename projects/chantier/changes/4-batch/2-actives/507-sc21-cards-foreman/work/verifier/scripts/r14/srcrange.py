"""Verifier: every inventory row's source range at the base shares a word with its behaviour."""

import re
import subprocess
from pathlib import Path

CR = Path("<CR folder>")
W = "<worktree>"
BASE = "24111e6d"
SPLIT = re.compile(r"(?<!\\)\|")
ID = re.compile(r"^(?:FM-B?\d{3}|[A-Z]{1,3}-\d{3,4})$")


def git(*a):
    return subprocess.run(["git", "-C", W, *a], capture_output=True, check=True).stdout.decode("utf-8", "replace")


tree = git("ls-tree", "-r", "--name-only", BASE).split("\n")
cache = {}


def lines(p):
    if p not in cache:
        cache[p] = git("show", f"{BASE}:{p}").split("\n")
    return cache[p]


def words(s):
    return {w.lower() for w in re.findall(r"[A-Za-z_]{3,}", s)}


for f in sorted((CR / "evidence").glob("cards-inventory-*.md")):
    n, fail = 0, []
    for line in f.read_text(encoding="utf-8").split("\n"):
        c = [x.strip() for x in SPLIT.split(line.strip().strip("|"))]
        if len(c) != 8 or not ID.match(c[0]):
            continue
        m = re.match(r"`?([^:`]+):(\d+)(?:-(\d+))?", c[4])
        if not m:
            fail.append((c[0], "unparsed", c[4][:60]))
            continue
        a, z = int(m[2]), int(m[3] or m[2])
        p = next((x for x in (m[1], f"skills/chantier/references/{m[1]}", f"skills/chantier/{m[1]}", f"skills/{m[1]}") if x in tree), None)
        if p is None:
            fail.append((c[0], "no file", m[1]))
            continue
        n += 1
        text = " ".join(lines(p)[a - 1 : z])
        if words(c[3]) and not words(c[3]) & words(text):
            fail.append((c[0], c[4], c[3][:80]))
    print(f"{f.name}: rows checked at {BASE}: {n}; failures: {len(fail)} {fail[:10]}")
