"""Verifier r15: independent comparison of the four inventories with the copies before round 15."""
import difflib, json, re, sys, collections, getpass, os
from pathlib import Path

cr, wt = Path(sys.argv[1]), Path(sys.argv[2])
SPLIT = re.compile(r"(?<!\\)\|")
ID = re.compile(r"^(?:FM-B?\d{3}|[A-Z]{1,3}-\d{3,4})$")
NAMES = ["chief-of-staff", "foreman", "griller", "host-and-shared"]
cases = {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in sorted((wt / "evals/quiz").glob("*/*.json"))}

def cells(line):
    c = [x.strip() for x in SPLIT.split(line.strip().strip("|"))]
    return c if line.startswith("|") and len(c) == 8 and ID.match(c[0]) else None

user = {getpass.getuser(), Path.home().name}
tot = collections.Counter()
by_case = collections.defaultdict(list)
child = []
rule_ids = collections.Counter()
for n in NAMES:
    new_p = cr / "evidence" / f"cards-inventory-{n}.md"
    old_p = cr / "work/scratch/r15/before" / f"cards-inventory-{n}.md"
    raw = new_p.read_bytes()
    ol = old_p.read_text(encoding="utf-8").split("\n")
    nl = new_p.read_text(encoding="utf-8").split("\n")
    o = [(l, cells(l)) for l in ol if cells(l)]
    m = [(l, cells(l)) for l in nl if cells(l)]
    changed = other_col = bad_append = 0
    for (_, a), (_, b) in zip(o, m):
        if a[:7] != b[:7]: other_col += 1
        if a[7] != b[7]:
            changed += 1
            if not b[7].startswith(a[7] + "; "): bad_append += 1
    for _, b in m:
        rule_ids[b[0]] += 1
        q = re.findall(r"\bquiz ([A-Za-z0-9-]+)", b[7])
        for x in q: by_case[x].append((n, b[0]))
        if q: tot["rows naming quiz"] += 1
        if "child 25" in b[7]: child.append((n, b[0], b[7], b[3]))
    nonrow = [l for l in difflib.ndiff(ol, nl) if l[:2] in ("- ", "+ ") and not cells(l[2:])]
    print(f"{n}: rows {len(o)} -> {len(m)}; check cells changed {changed}; other columns changed {other_col}; "
          f"check not appended {bad_append}; non-row lines -{sum(l[0]=='-' for l in nonrow)} +{sum(l[0]=='+' for l in nonrow)}; "
          f"table lines changed outside rule rows {sum(l[2:].startswith('|') for l in nonrow)}")
    text = raw.decode("utf-8")
    print(f"   bytes {len(raw)} BOM {raw[:3]==b'\xef\xbb\xbf'} CRLF {b'\r' in raw} username hits {sum(len(re.findall(re.escape(u), text, re.I)) for u in user)}"
          f" protecting list {len(re.findall(r'^## Protecting-looking', text, re.M))}")
    tot["rows"] += len(m); tot["changed"] += changed
    tot["text home"] += sum(1 for _, b in m if "cards-next" in b[6])
print(dict(tot))
print("distinct ids", len(rule_ids))
print("quiz cases", len(cases), "named", len(set(by_case) & set(cases)), "unknown", sorted(set(by_case) - set(cases)))
unnamed = sorted(set(cases) - set(by_case))
print("named in no row's check:", len(unnamed))
for u in unnamed: print("   ", u, cases[u]["role"], cases[u]["rules"])
print("distinct rows naming a quiz case:", len({r for v in by_case.values() for r in v}))
print("rows saying child 25:", len(child))
planned = collections.defaultdict(list)
for n, i, chk, beh in child:
    for t in re.findall(r"child 25: ([^;]+)", chk):
        planned[t.strip()].append(i)
for k in sorted(planned): print("   ", k, planned[k])
print("planned case files present:", [p for p in ("a8-ask-settings-json","tracker-approval","direct-brief-foreman","griller-tracker-never") if p in cases])

# review sheet
rowmap = {}
for n in NAMES:
    for l in (cr / "evidence" / f"cards-inventory-{n}.md").read_text(encoding="utf-8").split("\n"):
        c = cells(l)
        if c: rowmap[(n, c[0])] = c
out = []
for k in sorted(cases):
    d = cases[k]
    out.append(f"=== {k} [{d['role']}] {d['rules']}\n S: {d['situation']}\n E: {d['expected'] if isinstance(d['expected'], str) else json.dumps(d['expected'])}")
    for r in by_case.get(k, []):
        c = rowmap[r]
        out.append(f"   -> {r[1]} ({r[0][:4]}) {c[3][:330]}")
out.append("=== CHILD 25 rows")
for n, i, chk, beh in child:
    out.append(f"   {i} ({n[:4]}) [{chk[-90:]}] {beh[:330]}")
Path(sys.argv[3]).write_text("\n".join(out), encoding="utf-8", newline="\n")
print("review sheet chars", len("\n".join(out)), "lines", len("\n".join(out).split("\n")))
