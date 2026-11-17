#!/usr/bin/env python3
"""Apply the requirement reduction (mapping.csv / tiles.csv) to a worktree. See plan.md 4.1."""
import argparse
import csv
import importlib.util
import os
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ID_RE = re.compile(r"S[tw]RS-MDOKFSTUDIO-[A-Z]+-\d{3}")
MARK_RE = re.compile(
    r"^(?P<pre>\s*(?:(?://|#|\*|/\*|<!--)\s*)?)@(?P<tag>implements|tests)_req\s+"
    r"(?P<id>S[tw]RS-MDOKFSTUDIO-[A-Z]+-\d{3})\s*(?:\*/|-->)?\s*$"
)
TOKEN_SCOPE = {"CORE": "rendering-core", "CODE": "code-blocks", "GFM": "gfm", "MYST": "myst", "DIAG": "diagrams",
               "FMSCHEMA": "frontmatter-schema", "FMEDIT": "frontmatter-editing", "LAYOUT": "layout-width",
               "THEME": "theme-zoom", "TOOLBAR": "toolbar-navigation", "BLOCK": "block-editing",
               "PALETTE": "palette-slash", "TABLE": "table-editing", "REVIEW": "review-annotations",
               "LIFE": "lifecycle-sync", "TRUST": "trust-security"}
MAIN_TOKENS = {"CORE", "CODE", "GFM", "MYST", "DIAG", "FMSCHEMA", "FMEDIT", "LAYOUT"}
SRC_DIRS = ["src", "sphinx", "scripts", "test"]


def load_exempt():
    spec = importlib.util.spec_from_file_location("setex", HERE / "set-exemption.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def lifecycle(path):
    m = re.search(r"^lifecycle: (\S+)$", path.read_text(encoding="utf-8").split("\n---\n")[0], re.M)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worktree", required=True)
    ap.add_argument("--mapping", required=True)
    ap.add_argument("--tiles", required=True)
    ap.add_argument("--scopes", required=True)
    ap.add_argument("--levels", default="both")
    ap.add_argument("--only", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--okfreq", default="/private/tmp/claude-502/okf.sh")
    a = ap.parse_args()
    wt = pathlib.Path(a.worktree)
    scopes = set(a.scopes.split(","))
    only = set(filter(None, a.only.split(",")))
    tiles = {r["tile_key"]: r for r in csv.DictReader(open(a.tiles))}
    mapping = list(csv.DictReader(open(a.mapping)))
    tier = wt / "requirements" / "tiers"

    def path_of(rid):
        lvl = "swrs" if rid.startswith("SwRS") else "strs"
        hits = list((tier / lvl).glob(f"*/{rid}.md"))
        return hits[0] if hits else None

    def survivor(key):
        return tiles[key]["survivor_id"] if key in tiles else None

    selected = []
    for r in mapping:
        t = tiles.get(r["new_tile_key"]) or {"scope": TOKEN_SCOPE[r["old_id"].split("-")[2]], "level": "SwRS"}
        if t["scope"] not in scopes:
            continue
        if a.levels != "both" and t["level"] != a.levels:
            continue
        if only and r["new_tile_key"] not in only:
            continue
        selected.append(r)

    errors = []
    for r in selected:
        s = survivor(r["new_tile_key"])
        if s is None:
            continue
        sp = path_of(s) if s != "NEW" else None
        if sp is None or lifecycle(sp) != "draft":
            errors.append(f"survivor {s} of {r['new_tile_key']} missing or not active")
    if errors:
        print("\n".join(sorted(set(errors))))
        sys.exit(2)

    rename = {}
    for r in selected:
        if r["action"] == "keep":
            continue
        rename[r["old_id"]] = None if r["action"] == "drop-implementation-detail" else survivor(r["new_tile_key"])

    # markers
    files = subprocess.run(["git", "ls-files", *SRC_DIRS], cwd=wt, capture_output=True, text=True).stdout.split("\n")
    renamed = deleted = 0
    for f in filter(None, files):
        p = wt / f
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        if "_req" not in text:
            continue
        lines = text.split("\n")
        marked = set()
        for ln in lines:
            m = MARK_RE.match(ln)
            if m:
                marked.add((m["tag"], m["id"]))
        out, changed = [], False
        for ln in lines:
            m = MARK_RE.match(ln)
            if m and m["id"] in rename:
                tag, new = m["tag"], rename[m["id"]]
                marked.discard((tag, m["id"]))
                changed = True
                if new is None or (tag, new) in marked:
                    deleted += 1
                    continue
                marked.add((tag, new))
                renamed += 1
                ln = ln.replace(m["id"], new)
            out.append(ln)
        if changed and not a.dry_run:
            p.write_text("\n".join(out), encoding="utf-8")

    # files
    n_del = n_sup = n_arc = 0
    for r in selected:
        if r["action"] == "keep":
            continue
        old = r["old_id"]
        op = path_of(old)
        if op is None or lifecycle(op) != "draft":
            continue
        token = old.split("-")[2]
        main = token in MAIN_TOKENS
        if main and r["action"] == "drop-implementation-detail":
            n_arc += 1
            if not a.dry_run:
                subprocess.run([a.okfreq, "archive", old, "--path", ".", "--yes"], check=True, capture_output=True, text=True, cwd=wt)
        elif main:
            n_sup += 1
            if not a.dry_run:
                subprocess.run([a.okfreq, "supersede", old, survivor(r["new_tile_key"]), "--path", ".", "--yes"], check=True, capture_output=True, text=True, cwd=wt)
        else:
            n_del += 1
            if not a.dry_run:
                subprocess.run(["git", "rm", "-q", "-f", str(op.relative_to(wt))], check=True, cwd=wt)

    # references (whole mapping)
    full = {}
    for r in mapping:
        op = path_of(r["old_id"])
        if r["action"] == "keep":
            continue
        if op is None or lifecycle(op) != "draft":
            tgt = survivor(r["new_tile_key"])
            if tgt not in (None, "NEW") and r["action"] != "drop-implementation-detail":
                full[r["old_id"]] = tgt
    refs = 0
    targets = []
    for lvl in ("swrs", "strs"):
        for p in (tier / lvl).glob("*/*.md"):
            if p.name == "index.md" or lifecycle(p) != "draft":
                continue
            targets.append(p)
    for f in filter(None, files):
        if f.startswith("test/visual/capture_") or f.endswith((".ts", ".py", ".mjs", ".md")):
            targets.append(wt / f)
    for p in targets:
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        if not any(i in full for i in ID_RE.findall(text)):
            continue
        new = ID_RE.sub(lambda m: full.get(m.group(0), m.group(0)), text)
        if p.suffix == ".md" and "tiers" in p.parts:
            head, sep, body = new.partition("\n---\n")
            head = dedupe_lists(head)
            new = head + sep + body
        if new != text:
            refs += 1
            if not a.dry_run:
                p.write_text(new, encoding="utf-8")
    # retired files: only the frontmatter lists, so that links still resolve
    ret = 0
    for lvl in ("swrs", "strs"):
        for p in (tier / lvl).glob("*/*.md"):
            if p.name == "index.md" or lifecycle(p) == "draft":
                continue
            text = p.read_text(encoding="utf-8")
            head, sep, body = text.partition("\n---\n")
            new = re.sub(r"^(- )(S[tw]RS-MDOKFSTUDIO-[A-Z]+-\d{3})$", lambda m: m.group(1) + full.get(m.group(2), m.group(2)), head, flags=re.M)
            new = dedupe_lists(new)
            if new != head:
                ret += 1
                if not a.dry_run:
                    p.write_text(new + sep + body, encoding="utf-8")
    ex = 0
    if not a.dry_run:
        ex = load_exempt().run(wt)
    print(f"rows applied: {len(selected)}; deleted: {n_del}; superseded: {n_sup}; archived: {n_arc}; "
          f"marker lines renamed: {renamed}, deleted: {deleted}; files with references rewritten: {refs}; exempted: {ex}; retired files relinked: {ret}")


def dedupe_lists(head):
    out, i, lines = [], 0, head.split("\n")
    while i < len(lines):
        ln = lines[i]
        out.append(ln)
        if re.match(r"^(derives_from|depends_on):\s*$", ln):
            seen = []
            j = i + 1
            while j < len(lines) and re.match(r"^- ", lines[j]):
                if lines[j] not in seen:
                    seen.append(lines[j])
                j += 1
            out.extend(seen)
            i = j
            continue
        i += 1
    return "\n".join(out)


if __name__ == "__main__":
    main()
