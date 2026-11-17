#!/usr/bin/env python3
"""Write one brief per scope: tiles with survivor, proposed title and member bodies (BASE snapshot paths).

Usage: gen-briefs.py --base-dir SNAPSHOT --mapping M --tiles T --out DIR [--level SwRS|StRS]
"""
import argparse, csv, pathlib, re

ap = argparse.ArgumentParser()
ap.add_argument("--base-dir", required=True)
ap.add_argument("--mapping", required=True)
ap.add_argument("--tiles", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
base = pathlib.Path(a.base_dir)
paths = {}
for p in base.glob("requirements/tiers/s*rs/*/*.md"):
    if p.name != "index.md":
        paths[p.stem] = p
tiles = list(csv.DictReader(open(a.tiles)))
members = {}
for r in csv.DictReader(open(a.mapping)):
    members.setdefault(r["new_tile_key"], []).append(r)
out = pathlib.Path(a.out)
out.mkdir(parents=True, exist_ok=True)
for scope in sorted({t["scope"] for t in tiles}):
    for level in ("SwRS", "StRS"):
        ts = [t for t in tiles if t["scope"] == scope and t["level"] == level]
        if not ts:
            continue
        lines = [f"# {level} tiles of scope {scope}", ""]
        for t in ts:
            lines += [f"## {t['tile_key']}", "",
                      f"- survivor id: {t['survivor_id']}", f"- level: {level}",
                      f"- cross-cutting: {t['crosscutting'] or 'no'}",
                      f"- proposed title: {t['proposed_title']}", "- members (old id, action, BASE file):"]
            for r in members.get(t["tile_key"], []):
                p = paths.get(r["old_id"])
                lines.append(f"  - {r['old_id']} ({r['action']}) {p if p else '(no file)'}")
            lines.append("")
        (out / f"{level.lower()}-{scope}.md").write_text("\n".join(lines), encoding="utf-8")
print("ok")
