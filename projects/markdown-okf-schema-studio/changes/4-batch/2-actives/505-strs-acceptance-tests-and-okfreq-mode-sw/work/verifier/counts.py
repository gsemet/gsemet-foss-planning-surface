"""Verifier of CR-505: scenario and path counts from the requirement files and okfreq trace JSON.

usage: python -I counts.py <base tree> <base trace.json> <head tree> <head trace.json>
Declarations: `scenarios:` of every requirement file that is not retired (superseded,
deprecated, archived) and not annotation exempt. Markers: `scenario_markers` of
`okfreq trace --json`.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

RETIRED = {"superseded", "deprecated", "archived"}


def declared(tree):
    out, all_ids = {}, {}
    for path in sorted((Path(tree) / "requirements" / "tiers").rglob("*.md")):
        if not re.match(r"(SwRS|StRS)-MDOKFSTUDIO-[A-Z]+-\d+\.md$", path.name):
            continue
        front = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n---\n", 1)[0].split("\n")
        fields, scen, inside = {}, [], False
        for line in front:
            m = re.match(r"([a-z_]+):\s*(.*)$", line)
            if m:
                fields[m.group(1)] = m.group(2).strip()
            if line.startswith("scenarios:"):
                inside = True
                continue
            if inside:
                m2 = re.match(r"- id:\s*(\S+)", line)
                if m2:
                    scen.append(m2.group(1))
                elif not line.startswith(" "):
                    inside = False
        all_ids[path.stem] = scen
        if fields.get("req_lifecycle", "") in RETIRED or fields.get("annotation_exemption") == "true":
            continue
        out[path.stem] = scen
    return out, all_ids


def load(tree, trace):
    live, every = declared(tree)
    data = json.load(open(trace, encoding="utf-8"))
    marks = defaultdict(list)
    for m in data["scenario_markers"]:
        marks[(m["id"], m["fragment"])].append((m["marker"], m["file"]))
    return live, every, marks


def report(name, tree, trace):
    live, every, marks = load(tree, trace)
    paths = [(i, s) for i, sc in live.items() if i.startswith("StRS") for s in sc]
    scen = [(i, s) for i, sc in live.items() if i.startswith("SwRS") for s in sc]
    accepted = [k for k in paths if any(v == "accepts" for v, _ in marks.get(k, []))]
    unmarked = [k for k in scen if not marks.get(k)]
    unmarked_tests = [k for k in scen if not any(v == "tests" for v, _ in marks.get(k, []))]
    trust_scen = [k for k in scen if "-TRUST-" in k[0]]
    trust_paths = [k for k in paths if "-TRUST-" in k[0]]
    print(f"== {name}")
    print(f"use case paths: {len(paths)}, accepted: {len(accepted)}, not accepted: {len(paths) - len(accepted)}")
    print(f"SwRS scenarios: {len(scen)}, without any marker: {len(unmarked)}, without @tests_req: {len(unmarked_tests)}")
    print(f"TRUST SwRS scenarios: {len(trust_scen)}, with @tests_req: "
          f"{sum(any(v == 'tests' for v, _ in marks.get(k, [])) for k in trust_scen)}")
    print(f"TRUST paths: {len(trust_paths)}, accepted: "
          + ", ".join(f"{i[-9:]} {s}" for i, s in trust_paths if (i, s) in accepted))
    print("TRUST paths not accepted: " + ", ".join(f"{i[-9:]} {s}" for i, s in trust_paths if (i, s) not in accepted))
    undeclared = sorted(k for k in marks if k[1] not in every.get(k[0], []))
    print(f"markers on a fragment its requirement does not declare: {len(undeclared)} {undeclared[:6]}")
    return live, every, marks, accepted, unmarked


base = report("base", sys.argv[1], sys.argv[2])
head = report("head", sys.argv[3], sys.argv[4])
print("== base to head")
removed = [(i, s) for i, sc in base[1].items() for s in sc if s not in head[1].get(i, [])]
added = [(i, s) for i, sc in head[1].items() for s in sc if s not in base[1].get(i, [])]
print(f"scenarios removed (all requirement files): {len(removed)} {removed[:10]}")
print(f"scenarios added: {len(added)} {added}")
newly = sorted(set(head[3]) - set(base[3]))
print(f"paths accepted at head and not at base: {len(newly)}")
for i, s in newly:
    print("  ", i, s, [f for v, f in head[2][(i, s)] if v == "accepts"])
print(f"paths accepted at base and not at head: {sorted(set(base[3]) - set(head[3]))}")
print("files of accepts markers at base:", sorted({f.rsplit('/', 1)[0] for k in base[3] for v, f in base[2][k] if v == 'accepts'}))
lost = sorted(k for k in set(head[4]) - set(base[4]))
print(f"SwRS scenarios unmarked at head but marked at base: {len(lost)}")
for i, s in lost:
    print("  ", i, s)
gained = sorted(k for k in set(base[4]) - set(head[4]))
by = defaultdict(int)
for i, s in gained:
    by[i.split("-")[2]] += 1
print(f"SwRS scenarios unmarked at base and marked at head: {len(gained)} {dict(by)}")
print("TRUST ones: " + ", ".join(f"{i[-3:]} {s}" for i, s in gained if "-TRUST-" in i))
