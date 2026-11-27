"""Verifier of CR-505: check the marker tables of pr-body.md against the markers of both trees.

usage: python -I tables.py <base tree> <base trace.json> <head tree> <head trace.json> <pr-body.md>
A marker belongs to the first code line after its comment block (a test title, a function name or
the line itself). "Removed" is (anchor, scenario) at base and not at head, "added" the reverse,
counted per test file, for the trust-security software requirements.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

base_tree, base_trace, head_tree, head_trace, body = sys.argv[1:6]
TITLE = re.compile(r"""^\s*(?:await\s+)?(?:test|it|t\.test|describe|suite)(?:\.\w+)?\(\s*(["'`])(.*?)(?<!\\)\1""")
NAME = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?(?:def|function|class)\s+(\w+)")
COMMENT = re.compile(r"^\s*(//|/\*|\*|#|<!--|--|@)")


MARK = re.compile(r"^\s*(?:(?:#|//|/\*+|\*|<!--|--)\s*)?@tests_req\s+(SwRS-MDOKFSTUDIO-TRUST-\d+)#(S\d+)")


def anchors(tree, trace):
    """Every marker line of the files that carry one (okfreq's JSON lists one line per file and
    scenario, so the files are read here)."""
    out = defaultdict(Counter)
    found = set()
    for top in ("test", "sphinx", "tests"):
        for path in (Path(tree) / top).rglob("*"):
            if path.suffix not in {".ts", ".py", ".js", ".mjs", ".tsx"} or not path.is_file():
                continue
            f = path.relative_to(tree).as_posix()
            lines = path.read_text(encoding="utf-8").splitlines()
            for index, text_ in enumerate(lines):
                m = MARK.match(text_)
                if not m:
                    continue
                found.add((m.group(1), m.group(2)))
                i = index + 1
                while i < len(lines) and (not lines[i].strip() or COMMENT.match(lines[i])):
                    i += 1
                line = lines[i] if i < len(lines) else "<eof>"
                t = TITLE.match(line)
                n = NAME.match(line)
                anchor = t.group(2) if t else (n.group(1) if n else line.strip())
                out[f][(anchor, m.group(1)[-3:], m.group(2))] += 1
    data = json.load(open(trace, encoding="utf-8"))
    okfreq = {(m["id"], m["fragment"]) for m in data["scenario_markers"]
              if m["marker"] == "tests" and m["id"].startswith("SwRS-MDOKFSTUDIO-TRUST-") and m["fragment"]}
    print(f"cross-check {tree.rsplit('/', 1)[-1]}: scenarios read {len(found)}, okfreq {len(okfreq)}, "
          f"difference {sorted(found ^ okfreq)}")
    return out


b, h = anchors(base_tree, base_trace), anchors(head_tree, head_trace)


def parse_cell(cell):
    counts = Counter()
    if cell.strip() == "none":
        return counts
    for group in cell.split(";"):
        words = group.strip().split(" ", 1)
        number, rest = words[0], words[1]
        for item in rest.split(","):
            mm = re.match(r"\s*(S\d+)(?:\s+x(\d+))?\s*$", item)
            if not mm:
                raise ValueError(f"cannot read {item!r} in {cell!r}")
            counts[(number, mm.group(1))] += int(mm.group(2) or 1)
    return counts


text = Path(body).read_text(encoding="utf-8").splitlines()
table = {}
inside = False
for line in text:
    if line.startswith("| Test file | Removed | Added |"):
        inside = True
        continue
    if inside:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0].startswith("---"):
            continue
        table["test/" + cells[0].strip("`")] = (parse_cell(cells[1]), parse_cell(cells[2]))

computed = {}
for f in sorted(set(b) | set(h)):
    removed = b[f] - h[f]
    added = h[f] - b[f]
    if not removed and not added:
        continue
    r = Counter((n, s) for (a, n, s), c in removed.items() for _ in range(c))
    a_ = Counter((n, s) for (a, n, s), c in added.items() for _ in range(c))
    computed[f] = (r, a_, removed, added)

fmt = lambda c: ", ".join(f"{n} {s}" + (f" x{v}" if v > 1 else "") for (n, s), v in sorted(c.items(), key=lambda x: (x[0][0], int(x[0][1][1:])))) or "none"
print(f"table rows: {len(table)}; files with a changed trust marker: {len(computed)}")
print("files changed but not in the table:", sorted(set(computed) - set(table)))
print("table rows with no changed marker:", sorted(set(table) - set(computed)))
same = 0
for f in sorted(set(table) & set(computed)):
    tr, ta = table[f]
    r, a_ = computed[f][0], computed[f][1]
    if tr == r and ta == a_:
        same += 1
        continue
    print(f"\n-- DIFFERS {f}\n   table    removed: {fmt(tr)} | added: {fmt(ta)}\n   computed removed: {fmt(r)} | added: {fmt(a_)}")
    for label, group in (("-", computed[f][2]), ("+", computed[f][3])):
        for (anchor, n, s), c in sorted(group.items(), key=lambda x: (x[0][1], x[0][2], x[0][0])):
            print(f"   {label} {n} {s} @ {anchor[:130]}")
print(f"\nrows equal: {same}")

print("\n== table of newly covered scenarios")
live_gained = []
inside = False
rows = []
for line in text:
    if line.startswith("| SwRS | Scenario | Now covered by |"):
        inside = True
        continue
    if inside:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells[0].startswith("---"):
            rows.append(cells)
base_titles = {}
for number, scen, covered in rows:
    files = sorted({f for f in h for (a, n, s) in h[f] if n == number and s == scen})
    short = sorted(re.sub(r"(\.requirements)?(\.test)?\.(ts|py)$", "", f[5:]) for f in files)
    before = sorted({f for f in b for (a, n, s) in b[f] if n == number and s == scen})
    print(f"{number} {scen}: table: {covered}\n   head files: {short}; base files: {before}")
    for f in files:
        base_text = (Path(base_tree) / f).read_text(encoding="utf-8") if (Path(base_tree) / f).exists() else ""
        for (a, n, s) in h[f]:
            if n == number and s == scen:
                print(f"     {'NEW ' if a not in base_text else 'old '}{f[5:]} :: {a[:140]}")
print(f"rows: {len(rows)}")
