"""PR body lists (uncovered scenarios, uncovered paths, 66 candidate paths) against the head scan and the older tables."""
import collections
import json
import re
import subprocess
import sys

REPO, CR = sys.argv[1:3]
scan = json.load(open(CR + "/work/scratch/vf-scan-head.json", encoding="utf-8"))
body = open(CR + "/work/pr-body.md", encoding="utf-8").read()

marked = collections.defaultdict(set)
for p, n, verb, rid, frag, line in scan["markers"]:
    if verb != "implements_req" and frag:
        marked[rid].add(frag)
# exempt SwRS declare no scenario, so the declared set is "in force and not exempt"
want_sw = {(k.split("-", 2)[2], i) for k in scan["live_swrs"] for i in scan["decl"].get(k, {}) if i not in marked[k]}
want_st = {(k.split("-", 2)[2], i) for k in scan["live_strs"] for i in scan["decl"].get(k, {}) if i not in marked[k]}


def section(start, end):
    return body[body.index(start) : body.index(end)]


def parse(text):
    got, counts = set(), {}
    for line in text.split("\n"):
        m = re.match(r"^- ([A-Z]+) \((\d+)\): (.*)$", line.strip())
        if not m:
            continue
        group, count, rest = m.groups()
        n = 0
        for entry in rest.split(";"):
            em = re.match(r"^\s*(\d{3})\s+(S\d+(?:,S\d+)*)\s*$", entry)
            assert em, (group, entry)
            for i in em.group(2).split(","):
                got.add((f"{group}-{em.group(1)}", i))
                n += 1
        counts[group] = (int(count), n)
    return got, counts


sw, swc = parse(section("**SwRS scenarios:", "**StRS paths:"))
st, stc = parse(section("**StRS paths:", "## Changes"))
for label, got, want, counts in (("SwRS", sw, want_sw, swc), ("StRS", st, want_st, stc)):
    print(label, "listed", len(got), "computed", len(want), "listed-not-computed", sorted(got - want)[:10], "computed-not-listed", sorted(want - got)[:10])
    print("  group headers wrong:", {g: v for g, v in counts.items() if v[0] != v[1]})
for line in re.findall(r"^\*\*(?:SwRS scenarios|StRS paths): .*$", body, re.M):
    print(line)

# the 66 candidate paths
m = re.search(r"these 66 had a candidate marker.*?named in the table\. (.*?)\. None of", body, re.S)
c66 = set()
for part in m.group(1).split(";"):
    gm = re.match(r"^\s*([A-Z]+) (.*)$", part)
    group = gm.group(1)
    num = None
    for tok in gm.group(2).split(","):
        t = tok.strip().split()
        if len(t) == 2:
            num, i = t
        else:
            i = t[0]
        c66.add((f"{group}-{num}", i))
print("66 list size", len(c66), "all unmarked at head:", c66 <= want_st, sorted(c66 - want_st))

# candidate markers at the previous re-read = rows of the round 6 table
r6 = open(CR + "/work/scratch/r7-sort-r6.md", encoding="utf-8").read()
cand = set()
for line in r6.split("\n"):
    mm = re.match(r"^\| (test/\S+) \| \d+ \| StRS-MDOKFSTUDIO-(\S+) \| [^|]+ \| ([^|]+?) \| [^|]+ \|", line)
    if mm:
        am = re.search(r"@(?:tests_req|accepts_req) (#S\d+)", mm.group(3))
        if am:
            cand.add((mm.group(2), am.group(1)[1:]))
print("round 6 marked paths", len(cand), "of which unmarked at head", len(cand & want_st), "equal to the 66 list:", (cand & want_st) == c66,
      "diff", sorted((cand & want_st) ^ c66))

head_marked = sorted({(r.split("-", 2)[2], i) for r in scan["live_strs"] for i in marked[r]})
print("marked paths at head", len(head_marked))
for rid in ("CORE-007", "CORE-008", "TRUST-012", "TRUST-014", "LIFE-023"):
    print(rid, "markers", [x[:5] for x in scan["markers"] if x[3] == "StRS-MDOKFSTUDIO-" + rid])
print("examples unmarked:", all(x in want_st for x in [("MYST-007", "S1"), ("TABLE-015", "S1"), ("TABLE-001", "S1"), ("LIFE-014", "S1"), ("TRUST-004", "S1"), ("BLOCK-011", "S2"), ("CODE-004", "S1"), ("MYST-009", "S1"), ("DIAG-001", "S2")]))
for p, n, verb, rid, frag, line in scan["markers"]:
    if rid.startswith("StRS") and verb != "implements_req":
        print("KEPT", p, n, verb, rid.split("-", 2)[2], frag)
for k in scan["live_swrs"]:
    pass
