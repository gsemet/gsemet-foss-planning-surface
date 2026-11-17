#!/usr/bin/env python3
"""Gate G5: audit the tiles of the given scopes. See plan.md 4.3.

Usage: tile-audit.py --worktree WT --mapping mapping.csv --tiles tiles.local.csv --scopes a,b
       [--levels SwRS|StRS|both] [--base-trace trace-before.json] [--structure-only]
"""
import argparse
import csv
import json
import pathlib
import re
import subprocess
import sys

import yaml

ID_RE = re.compile(r"S[tw]RS-MDOKFSTUDIO-[A-Z]+-\d{3}")
SCEN_RE = re.compile(r"^### Scenario \((nominal|refusal|boundary)\): .+", re.M)
TOKEN_SCOPE = {"CORE": "rendering-core", "CODE": "code-blocks", "GFM": "gfm", "MYST": "myst", "DIAG": "diagrams",
               "FMSCHEMA": "frontmatter-schema", "FMEDIT": "frontmatter-editing", "LAYOUT": "layout-width",
               "THEME": "theme-zoom", "TOOLBAR": "toolbar-navigation", "BLOCK": "block-editing",
               "PALETTE": "palette-slash", "TABLE": "table-editing", "REVIEW": "review-annotations",
               "LIFE": "lifecycle-sync", "TRUST": "trust-security"}


def split(path):
    text = path.read_text(encoding="utf-8")
    head, _, body = text[4:].partition("\n---\n")
    return yaml.safe_load(head), body


def section(body, name):
    m = re.search(rf"^### {re.escape(name)}\s*$(.*?)(?=^### |\Z)", body, re.M | re.S)
    return m.group(1).strip() if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worktree", required=True)
    ap.add_argument("--mapping", required=True)
    ap.add_argument("--tiles", required=True)
    ap.add_argument("--scopes", required=True)
    ap.add_argument("--levels", default="both")
    ap.add_argument("--base-trace")
    ap.add_argument("--only", default="")
    ap.add_argument("--structure-only", action="store_true")
    ap.add_argument("--okfreq", default="/private/tmp/claude-502/okf.sh")
    a = ap.parse_args()
    wt = pathlib.Path(a.worktree)
    scopes = set(a.scopes.split(","))
    only = set(filter(None, a.only.split(",")))
    tiles = {r["tile_key"]: r for r in csv.DictReader(open(a.tiles))}
    mapping = list(csv.DictReader(open(a.mapping)))
    tier = wt / "requirements" / "tiers"
    files = {}
    for p in list(tier.glob("swrs/*/*.md")) + list(tier.glob("strs/*/*.md")):
        if p.name != "index.md":
            files[p.stem] = p
    meta = {}
    for i, p in files.items():
        meta[i] = split(p)
    life = {i: m[0].get("lifecycle") for i, m in meta.items()}
    f = []

    def sel(level):
        return a.levels in ("both", level)

    for key, t in tiles.items():
        if t["scope"] not in scopes or not sel(t["level"]) or (only and key not in only):
            continue
        sid = t["survivor_id"]
        if sid not in files or life.get(sid) != "draft":
            f.append(f"{key}: survivor {sid} missing or not active")
            continue
        fm, body = meta[sid]
        m = re.search(r"^## (.+)$", body, re.M)
        if not m or m.group(1).strip() != str(fm.get("title")).strip():
            f.append(f"{sid}: title differs from the first ## heading")
        norm = section(body, "Normative behavior")
        if norm is None:
            f.append(f"{sid}: no Normative behavior section")
        else:
            if " ".join(norm.split()) != " ".join(str(fm.get("description")).split()):
                f.append(f"{sid}: description differs from the normative behaviour")
            if len(re.findall(r"\bSHALL\b", norm)) != 1:
                f.append(f"{sid}: normative behaviour has {len(re.findall(r'SHALL', norm))} SHALL")
        for d in fm.get("depends_on") or []:
            if d not in files or life.get(d) != "draft":
                f.append(f"{sid}: depends_on {d} missing or not active")
        for d in fm.get("derives_from") or []:
            if d not in files or life.get(d) != "draft":
                f.append(f"{sid}: derives_from {d} missing or not active")
        if t["level"] == "StRS":
            continue
        scen = SCEN_RE.findall(body)
        cc = t["crosscutting"] == "yes"
        if not (2 <= len(scen) <= 9) and not (cc and 1 <= len(scen) <= 14):
            f.append(f"{sid}: {len(scen)} scenarios (need 2 to 9)")
        if "nominal" not in scen:
            f.append(f"{sid}: no nominal scenario")
        if not cc and not ({"refusal", "boundary"} & set(scen)):
            f.append(f"{sid}: no refusal or boundary scenario")
        if re.search(r"^### Scenario:", body, re.M):
            f.append(f"{sid}: an unnamed '### Scenario:' heading remains")
        if not a.structure_only:
            ver = section(body, "Verification notes")
            if ver is None:
                f.append(f"{sid}: no Verification notes section")
            else:
                for tf in [x for x in (fm.get("tested_in_files") or []) if not x.endswith(".markers.ts")]:
                    if tf not in ver and pathlib.Path(tf).name not in ver:
                        f.append(f"{sid}: verification notes do not name {tf}")
        if key.split(".", 1)[1].startswith("msg-"):
            typ = key.split("msg-", 1)[1]
            if typ not in body and not re.search(re.escape(typ[:14]), body):
                f.append(f"{sid}: message type {typ} not named in the scenarios")

    # references to retired ids from active files
    retired = {i for i, l in life.items() if l != "draft"}
    deleted = set()
    for r in mapping:
        if r["old_id"] not in files:
            deleted.add(r["old_id"])
    bad = retired | deleted
    scan = []
    for i, p in files.items():
        if life[i] == "draft":
            text = "\n".join((meta[i][0].get("derives_from") or []) + (meta[i][0].get("depends_on") or [])) + "\n" + meta[i][1]
            scan.append((p, text))
    srcs = subprocess.run(["git", "ls-files", "src", "sphinx", "scripts", "test"], cwd=wt, capture_output=True, text=True).stdout.split()
    for s_ in srcs:
        try:
            scan.append((wt / s_, (wt / s_).read_text(encoding="utf-8")))
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
    for p, text in scan:
        if "MDOKFSTUDIO" not in text:
            continue
        for rid in set(ID_RE.findall(text)):
            if rid in bad and not (p.stem == rid):
                # only count ids belonging to the audited scopes
                tok = rid.split("-")[2]
                if TOKEN_SCOPE[tok] in scopes or True:
                    f.append(f"{p.relative_to(wt)} cites retired/deleted {rid}")
    for i in sorted(retired):
        fm = meta[i][0]
        if fm.get("annotation_exemption") is not True:
            f.append(f"{i}: {life[i]} but annotation_exemption is not true")

    # mapping rows applied
    for r in mapping:
        t = tiles.get(r["new_tile_key"])
        scope = t["scope"] if t else TOKEN_SCOPE[r["old_id"].split("-")[2]]
        level = t["level"] if t else "SwRS"
        if scope not in scopes or not sel(level) or (only and r["new_tile_key"] not in only):
            continue
        old = r["old_id"]
        if r["action"] == "keep":
            if life.get(old) != "draft":
                f.append(f"{old}: keep row but not active")
        elif old in files and life.get(old) == "draft":
            f.append(f"{old}: row {r['action']} not applied")

    # marker continuity
    if a.base_trace:
        base = json.load(open(a.base_trace))
        out = subprocess.run([a.okfreq, "trace", "requirements", "--json"], cwd=wt, capture_output=True, text=True).stdout
        cur = json.loads(out)
        if cur["missing_ids"] or cur["duplicates"]:
            f.append(f"trace: missing {cur['missing_ids']} duplicates {cur['duplicates']}")
        for r in mapping:
            t = tiles.get(r["new_tile_key"])
            if not t or t["scope"] not in scopes or not sel(t["level"]) or (only and r["new_tile_key"] not in only) or r["action"] == "drop-implementation-detail":
                continue
            sid = t["survivor_id"]
            for kind in ("tested", "validation_tests"):
                if kind == "validation_tests" and t["level"] == "SwRS":
                    continue
                MOVED = {"src/page/modules/editPalette.markers.ts": "src/page/modules/editPalette.ts", "test/page/modules/editActions.markers.ts": "test/page/modules/editActions.test.ts", "test/core/frontmatter/okfFrontmatter.markers.ts": "test/core/frontmatter/okfFrontmatter.test.ts"}
                before = {MOVED.get(x, x) for x in base[kind].get(r["old_id"], [])}
                now = set(cur[kind].get(sid, []))
                miss = before - now
                if miss:
                    f.append(f"marker continuity: {r['old_id']} -> {sid}: lost {kind} files {sorted(miss)}")
        # active SwRS needs implementation and test files (non exempt)
        for key, t in tiles.items():
            if t["scope"] in scopes and sel(t["level"]) and t["level"] == "SwRS" and (not only or key in only):
                sid = t["survivor_id"]
                if sid in meta and life.get(sid) == "draft" and not meta[sid][0].get("annotation_exemption"):
                    if not cur["implemented"].get(sid):
                        f.append(f"{sid}: no @implements_req file")
                    if not cur["tested"].get(sid):
                        f.append(f"{sid}: no @tests_req file")

    for line in f:
        print(line)
    print(f"{len(f)} findings")
    sys.exit(1 if f else 0)


if __name__ == "__main__":
    main()
