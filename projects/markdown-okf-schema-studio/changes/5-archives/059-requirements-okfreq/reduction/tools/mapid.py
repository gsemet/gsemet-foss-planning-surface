#!/usr/bin/env python3
"""Translate old requirement ids to their tile survivor. Usage: mapid.py ID [ID...] (or text on stdin with --stdin)."""
import csv, pathlib, re, sys
R = pathlib.Path(__file__).resolve().parent.parent
tiles = {r["tile_key"]: r for r in csv.DictReader(open(R / "tiles.local.csv"))}
mp = {r["old_id"]: r for r in csv.DictReader(open(R / "mapping.csv"))}
ID = re.compile(r"S[tw]RS-MDOKFSTUDIO-[A-Z]+-\d{3}")
ids = ID.findall(sys.stdin.read()) if "--stdin" in sys.argv else sys.argv[1:]
for i in ids:
    r = mp.get(i)
    if not r:
        print(f"{i}: not in the mapping (deprecated before the reduction, or unknown)")
        continue
    t = tiles.get(r["new_tile_key"])
    s = t["survivor_id"] if t else "(dropped)"
    print(f"{i} -> {s}  [{r['new_tile_key']}, {r['action']}]  {t['proposed_title'] if t else ''}")
