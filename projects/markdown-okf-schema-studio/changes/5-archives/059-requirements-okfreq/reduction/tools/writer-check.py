#!/usr/bin/env python3
"""Writer self-check of rewritten tile files. Usage: writer-check.py FILE... (files named <ID>.md)"""
import csv, pathlib, re, sys
import yaml

R = pathlib.Path(__file__).resolve().parent.parent
tiles = {r["survivor_id"]: r for r in csv.DictReader(open(R / "tiles.local.csv"))}
survivors = set(tiles)
mp = {r["old_id"]: r for r in csv.DictReader(open(R / "mapping.csv"))}
ID = re.compile(r"S[tw]RS-MDOKFSTUDIO-[A-Z]+-\d{3}")
bad = 0
for arg in sys.argv[1:]:
    p = pathlib.Path(arg)
    f = []
    text = p.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        print(f"{p.name}: no frontmatter"); bad += 1; continue
    head, _, body = text[4:].partition("\n---\n")
    try:
        fm = yaml.safe_load(head)
    except Exception as e:
        print(f"{p.name}: frontmatter does not parse: {e}"); bad += 1; continue
    sid = p.stem
    t = tiles.get(sid)
    if fm.get("id") != sid:
        f.append("frontmatter id differs from the file name")
    if not t:
        f.append("not a survivor id of tiles.local.csv")
    h = re.search(r"^## (.+)$", body, re.M)
    if not h or h.group(1).strip() != str(fm.get("title")).strip():
        f.append("title differs from the first ## heading")
    m = re.search(r"^### Normative behavior\s*$(.*?)(?=^### |\Z)", body, re.M | re.S)
    norm = m.group(1).strip() if m else ""
    if " ".join(norm.split()) != " ".join(str(fm.get("description")).split()):
        f.append("description differs from the Normative behavior text")
    if len(re.findall(r"\bSHALL\b", norm)) != 1:
        f.append("the normative behaviour needs exactly one SHALL")
    if fm.get("type") == "SwRS":
        scen = re.findall(r"^### Scenario \((nominal|refusal|boundary)\): .+", body, re.M)
        cc = t and t["crosscutting"] == "yes"
        if len(scen) > 9 or (len(scen) < 2 and not cc):
            f.append(f"{len(scen)} scenarios (need 2 to 9)")
        if "nominal" not in scen:
            f.append("no nominal scenario")
        if not cc and not ({"refusal", "boundary"} & set(scen)):
            f.append("no refusal or boundary scenario")
        if re.search(r"^### Scenario:", body, re.M):
            f.append("unnamed '### Scenario:' heading")
        if "### Verification notes" not in body:
            f.append("no Verification notes section")
    for rid in set(ID.findall(text)) - {sid}:
        if rid not in survivors:
            r = mp.get(rid)
            f.append(f"cites {rid}, which is not a surviving id; run tools/mapid.py {rid}" if r else f"cites {rid}, which is not in the mapping")
    for k in ("derives_from", "depends_on"):
        for d in fm.get(k) or []:
            if d not in survivors:
                f.append(f"{k} {d} is not a surviving id")
    for kw in re.findall(r"(?i)backlog item|P[123]/[a-z-]+", body):
        f.append(f"names a backlog item: {kw}")
    if f:
        bad += 1
        for x in f:
            print(f"{p.name}: {x}")
print(f"{bad} file(s) with findings")
sys.exit(1 if bad else 0)
