"""Verifier probe: scope coverage, superseded markers, diagrams (CR-343)."""
import json, re, sys, pathlib

wt = pathlib.Path(sys.argv[1])
trace = json.load(open(sys.argv[2], encoding="utf-8"))
req = wt / "requirements" / "tiers"

def fm(p):
    t = p.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---\n", t, re.S)
    return (m.group(1) if m else ""), t

life = {}
files = {}
for p in req.rglob("*.md"):
    m = re.match(r"(S[wt]RS-MDOKFSTUDIO-[A-Z]+-\d+)\.md$", p.name)
    if not m:
        continue
    f, t = fm(p)
    lm = re.search(r"^req_lifecycle:\s*(\S+)", f, re.M)
    life[m.group(1)] = lm.group(1) if lm else "?"
    files[m.group(1)] = (p, f, t)

scope = lambda i: re.match(r"S[wt]RS-MDOKFSTUDIO-(BLOCK|TABLE)-\d+$", i)
inforce = lambda i: life.get(i) in ("proposed", "approved", "draft")

bad = []
for kind in ("implemented", "tested", "validation_tests"):
    for i in trace[kind]:
        if i not in life:
            bad.append((kind, i, "unknown"))
        elif not inforce(i):
            bad.append((kind, i, life[i]))
print("markers on non-in-force or unknown IDs:", bad)

sw = [i for i in life if i.startswith("SwRS") and scope(i) and inforce(i)]
exempt = [i for i in sw if re.search(r"^annotation_exemption:\s*true", files[i][1], re.M)]
noimpl = [i for i in sw if i not in trace["implemented"] and i not in exempt]
notest = [i for i in sw if i not in trace["tested"] and i not in exempt]
print("in-force SwRS BLOCK/TABLE:", len(sw), "exempt:", exempt)
print("no implementation marker:", sorted(noimpl))
print("no test marker:", sorted(notest))

st = sorted(i for i in life if i.startswith("StRS") and scope(i) and inforce(i))
print("in-force StRS BLOCK/TABLE:", len(st))
for i in st:
    t = files[i][2]
    sec = re.search(r"^### Use case diagram[ \t]*\n(.*?)(?=^#{1,3} |\Z)", t, re.M | re.S)
    n = sec.group(1).count("```mermaid") if sec else 0
    print(f"  {i} {life[i]} diagram_section={bool(sec)} mermaid_in_section={n} validation_test={i in trace['validation_tests']}")
