"""CR-505 Investigator, read only: uncovered StRS paths and SwRS scenarios per scope at a worktree.

usage: python -I count.py <worktree> [SCOPE-TOKEN ...]
Declarations come from the requirement frontmatter (`scenarios:`), markers from `git grep` on the
worktree files. Prints the per-scope counts; with scope tokens, also lists their uncovered items.
"""
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

root = Path(sys.argv[1])
shown = sys.argv[2:]
RETIRED = {"superseded", "deprecated", "archived"}
D7 = {"StRS-MDOKFSTUDIO-CORE-007", "StRS-MDOKFSTUDIO-CORE-008", "StRS-MDOKFSTUDIO-TRUST-014"}
D7_DIRS = ("test/build/", "test/security/", "test/site/", "test/core/")

declared = {}
lifecycle = Counter()
exempt_strs = []
for path in sorted((root / "requirements" / "tiers").rglob("*.md")):
    if not re.match(r"(SwRS|StRS)-MDOKFSTUDIO-[A-Z]+-\d+\.md$", path.name):
        continue
    front = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n---\n", 1)[0].split("\n")
    fields = {}
    for line in front:
        match = re.match(r"([a-z_]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    if fields.get("req_lifecycle", "") in RETIRED:
        continue
    tier = path.stem.split("-")[0]
    lifecycle[(tier, fields.get("req_lifecycle"))] += 1
    if fields.get("annotation_exemption") == "true":
        if tier == "StRS":
            exempt_strs.append(path.stem)
        continue
    inside = False
    for line in front:
        if line.startswith("scenarios:"):
            inside = True
            continue
        if inside:
            match = re.match(r"- id:\s*(S\d+)", line)
            if match:
                declared[(path.stem, match.group(1))] = fields.get("req_lifecycle")
            elif not line.startswith(" "):
                inside = False

grep = subprocess.run(
    ["git", "-C", str(root), "grep", "-n", "--untracked", "-E",
     r"@(tests_req|accepts_req) (SwRS|StRS)-MDOKFSTUDIO-", "--", "src", "sphinx", "scripts", "test", "tests"],
    capture_output=True, check=True).stdout.decode("utf-8")
MARKER = re.compile(
    r"^\s*(?:(?:#|//|/\*+|\*|<!--)\s*)?@(tests_req|accepts_req) ((?:SwRS|StRS)-MDOKFSTUDIO-[A-Z]+-\d+)#(S\d+)\b")
tests, accepts, counting = set(), set(), set()
for entry in grep.splitlines():
    name, _, line = entry.split(":", 2)
    match = MARKER.match(line)
    if not match:
        continue
    key = (match.group(2), match.group(3))
    if match.group(1) == "tests_req":
        tests.add(key)
    else:
        accepts.add(key)
        if name.startswith("test/integration/") or (key[0] in D7 and name.startswith(D7_DIRS)):
            counting.add(key)


def token(ident):
    return ident.split("-")[2]


rows = defaultdict(Counter)
bare = defaultdict(list)
for key in declared:
    area = rows[token(key[0])]
    if key[0].startswith("StRS-"):
        area["paths"] += 1
        if key not in counting:
            area["no_accept"] += 1
            if key not in tests:
                area["no_marker"] += 1
            bare[token(key[0])].append((key, "tests_req only" if key in tests else "no marker"))
    else:
        area["scen"] += 1
        if key not in tests and key not in accepts:
            area["scen_bare"] += 1
            bare[token(key[0])].append((key, declared[key]))

print("live lifecycle:", sorted((f"{t}:{s}", n) for (t, s), n in lifecycle.items()))
print("exempt live StRS:", exempt_strs)
print("scope paths no_accept no_marker | swrs_scenarios bare")
total = Counter()
for area in sorted(rows):
    r = rows[area]
    total.update(r)
    print(area, r["paths"], r["no_accept"], r["no_marker"], "|", r["scen"], r["scen_bare"])
print("TOTAL", total["paths"], total["no_accept"], total["no_marker"], "|", total["scen"], total["scen_bare"])
print("accepted paths:", sorted(f"{i[17:]} {s}" for i, s in counting))
for area in shown:
    items = sorted(bare[area], key=lambda x: (x[0][0], int(x[0][1][1:])))
    for tier in ("StRS", "SwRS"):
        grouped = defaultdict(list)
        for (ident, fragment), note in items:
            if ident.startswith(tier):
                grouped[ident.split("-")[3]].append(fragment)
        print(area, tier, "; ".join(f"{n} {','.join(v)}" for n, v in grouped.items()))
