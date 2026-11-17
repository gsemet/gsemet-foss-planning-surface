#!/usr/bin/env python3
"""Reviewer checklist for a scope: old scenarios and Known issues per tile member. See plan.md 4.3.

Usage: scenario-checklist.py --worktree WT --base BASE --mapping mapping.csv --tiles tiles.local.csv
       --scope SCOPE --out FILE
"""
import argparse
import csv
import pathlib
import re
import subprocess


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worktree", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--mapping", required=True)
    ap.add_argument("--tiles", required=True)
    ap.add_argument("--scope", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    wt = pathlib.Path(a.worktree)
    tiles = {r["tile_key"]: r for r in csv.DictReader(open(a.tiles))}
    mapping = list(csv.DictReader(open(a.mapping)))
    names = subprocess.run(["git", "ls-tree", "-r", "--name-only", a.base, "requirements/tiers"], cwd=wt, capture_output=True, text=True).stdout.split("\n")
    where = {pathlib.Path(n).stem: n for n in names if n.endswith(".md") and not n.endswith("index.md")}
    members = {}
    for r in mapping:
        members.setdefault(r["new_tile_key"], []).append(r)
    out = [f"# Review checklist: {a.scope}", "",
           "Fill every empty cell. 'covered by' = new scenario title or table row, or 'duplicate of <new scenario>'.",
           "'kept as' = the new Known issue note.", ""]
    tot = [0, 0, 0, 0]
    for key, t in tiles.items():
        if t["scope"] != a.scope or t["level"] != "SwRS" or (a.only and key not in a.only.split(",")):
            continue
        sid = t["survivor_id"]
        out += [f"## {key} ({sid})", ""]
        nscen = nki = 0
        for r in members.get(key, []):
            old = r["old_id"]
            if old not in where:
                continue
            body = subprocess.run(["git", "show", f"{a.base}:{where[old]}"], cwd=wt, capture_output=True, text=True).stdout
            scen = re.findall(r"^### (Scenario.*)$", body, re.M)
            kis = [l.strip() for l in body.split("\n") if "Known issue" in l]
            out.append(f"### Member {old} ({r['action']})")
            out.append("")
            if scen or kis:
                out += ["| old item | covered by / kept as |", "| --- | --- |"]
                out += [f"| {s} |  |" for s in scen]
                out += [f"| {k[:300]} |  |" for k in kis]
                out.append("")
            nscen += len(scen)
            nki += len(kis)
        p = next(iter((wt / "requirements/tiers/swrs").glob(f"*/{sid}.md")), None)
        new_s = new_r = new_k = 0
        if p:
            text = p.read_text(encoding="utf-8")
            new_s = len(re.findall(r"^### Scenario", text, re.M))
            new_r = sum(1 for l in text.split("\n") if l.startswith("|") and not re.match(r"^\|[ \-:|]+\|$", l)) 
            new_k = sum(1 for l in text.split("\n") if "Known issue" in l)
        out += [f"Totals: old scenarios {nscen}, old Known issues {nki}; new scenarios {new_s}, table rows (with headers) {new_r}, new Known issues {new_k}", ""]
        tot[0] += nscen; tot[1] += nki; tot[2] += new_s; tot[3] += new_k
    out += [f"## Scope totals", "", f"old scenarios {tot[0]}, old Known issues {tot[1]}, new scenarios {tot[2]}, new Known issues {tot[3]}"]
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {a.out}: {tot}")


if __name__ == "__main__":
    main()
