# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""One-off migration of chantier planning folders (CR-253, Part B). Never kept.

Usage: uv run --script migrate-legacy.py [--dry-run] <planning folder>...

A folder holding `projects/` is a planning surface: the old, empty stage folders of each
project's `changes/` are renamed to chantier's layout. Any other folder is a chantier planning
folder (`.agents/changes/`): archived STATUS.json files carrying an old batch id are rewritten
to `batch-NN`, one line each. No git write; renames are plain file-system renames.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

BATCH_OK = re.compile(r"^batch-\d+$")
OLD_DIRS = ("3-requests", "4-archives", "5-trash", "3-stash", "4-batches", "3-batches", "4-archive")
SURFACE_RENAMES = {
    "agentic-planning-surface": [
        ("3-batches", "4-batch"),
        ("4-archive", "5-archives"),
        ("5-trash", "6-trash"),
    ],
    "chantier": [("3-stash", "3-ready"), ("4-batches", "4-batch")],
    "markdown-okf-schema-studio": [("3-stash", "3-ready"), ("4-batches", "4-batch")],
    "okf-schema": [("3-stash", "3-ready"), ("4-batches", "4-batch")],
}


class Refusal(Exception):
    pass


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def holds_only_keep(folder: Path) -> bool:
    """True when the folder holds only `.gitkeep` files and empty folders."""
    return all(p.is_dir() or p.name == ".gitkeep" for p in folder.rglob("*"))


def is_surface(folder: Path) -> bool:
    return (folder / "projects").is_dir()


# ---------------------------------------------------------------- chantier planning folder


def records_map(folder: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for rec in sorted((folder / "5-archives" / "batches").glob("batch-*.json")):
        data = read_json(rec)
        former = (data.get("backfill") or {}).get("former_id")
        if former:
            mapping[former] = data["batch"]
    return mapping


def refuse_chantier(folder: Path) -> None:
    for name in ("3-requests", "4-archives"):
        if (folder / name).exists():
            raise Refusal(f"{folder / name}: an old folder, refused")
    trash = folder / "5-trash"
    if trash.exists() and not holds_only_keep_files(trash):
        raise Refusal(f"{trash}: holds more than .gitkeep, refused")
    for bj in folder.rglob("batch.json"):
        if "4-batch" in bj.relative_to(folder).parts[:1]:
            continue
        if read_json(bj).get("status") in ("open", "landed"):
            raise Refusal(f"{bj}: status open/landed, refused")


def holds_only_keep_files(folder: Path) -> bool:
    return all(p.name == ".gitkeep" for p in folder.rglob("*") if p.is_file()) and not any(
        p.is_dir() for p in folder.rglob("*")
    )


def status_files(folder: Path):
    for stage in ("5-archives", "6-trash"):
        base = folder / stage
        if base.is_dir():
            for cr in sorted(p for p in base.iterdir() if p.is_dir() and p.name != "batches"):
                f = cr / "STATUS.json"
                if f.is_file():
                    yield f


def migrate_chantier(folder: Path, dry: bool) -> int:
    refuse_chantier(folder)
    mapping = records_map(folder)
    print(f"map read from 5-archives/batches ({len(mapping)} entries):")
    for old, new in mapping.items():
        print(f"  {old} -> {new}")
    changes: list[tuple[Path, str, str, str]] = []
    for f in status_files(folder):
        text = f.read_bytes().decode("utf-8")
        value = json.loads(text).get("batch")
        if not value or BATCH_OK.match(value):
            continue
        if value not in mapping:
            raise Refusal(f"{f}: old batch id {value!r} not named by the records' map")
        changes.append((f, value, mapping[value], text))
    for f, old, new, text in changes:
        pat = re.compile(r'("batch"\s*:\s*)"' + re.escape(old) + '"')
        out, n = pat.subn(lambda m: f'{m.group(1)}"{new}"', text, count=1)
        if n != 1:
            raise Refusal(f"{f}: cannot find the batch value in the text")
        rel = f.relative_to(folder).as_posix()
        print(f"{rel}: {old} -> {new}")
        if not dry:
            f.write_bytes(out.encode("utf-8"))
    if not changes:
        print("nothing to do")
    else:
        print(f"{len(changes)} file(s) {'would change' if dry else 'changed'}")
    return len(changes)


# ---------------------------------------------------------------- planning surface


def git_dirty(surface: Path, rel: str) -> str:
    r = subprocess.run(
        ["git", "-C", str(surface), "status", "--porcelain", "--", rel],
        capture_output=True, text=True, encoding="utf-8",
    )
    if r.returncode != 0:
        raise Refusal(f"git status failed under {rel}: {r.stderr.strip()}")
    return r.stdout.strip()


def migrate_surface(folder: Path, dry: bool) -> int:
    plan: list[tuple[Path, Path, str]] = []
    for project, renames in SURFACE_RENAMES.items():
        changes = folder / "projects" / project / "changes"
        if not changes.is_dir():
            continue
        for old, new in renames:
            src, dst = changes / old, changes / new
            if not src.exists():
                continue
            if not holds_only_keep(src):
                raise Refusal(f"{src}: holds more than .gitkeep and empty folders, refused")
            if dst.exists() and any(p.is_file() for p in dst.rglob("*")):
                raise Refusal(f"{dst}: target exists with files, refused")
            rel = src.relative_to(folder).as_posix()
            dirty = git_dirty(folder, rel)
            if dirty:
                raise Refusal(f"{rel}: uncommitted changes, refused:\n{dirty}")
            plan.append((src, dst, f"projects/{project}/changes/{old} -> {new}"))
    for src, dst, label in plan:
        print(f"rename {label}")
        if not dry:
            if dst.exists():
                shutil.rmtree(dst)
            src.rename(dst)
    if not plan:
        print("nothing to do")
    else:
        print(f"{len(plan)} rename(s) {'would run' if dry else 'done'}")
    return len(plan)


# ---------------------------------------------------------------- scan


def planning_folders(folder: Path) -> list[Path]:
    if is_surface(folder):
        return sorted(p / "changes" for p in (folder / "projects").iterdir() if (p / "changes").is_dir())
    return [folder]


def scan(folder: Path) -> list[str]:
    bad: list[str] = []
    for pf in planning_folders(folder):
        for name in OLD_DIRS:
            if (pf / name).exists():
                bad.append(f"{pf / name}: old folder present")
        for f in status_files(pf):
            v = json.loads(f.read_text(encoding="utf-8")).get("batch")
            if v and not BATCH_OK.match(v):
                bad.append(f"{f}: batch {v!r} outside batch-NN")
        files = list(pf.glob("4-batch/*/batch.json")) + list(pf.glob("4-batch/**/batch.json"))
        files += list((pf / "5-archives" / "batches").glob("batch-*.json"))
        for jf in dict.fromkeys(files):
            for cr in read_json(jf).get("crs", []):
                for key in ("path", "archive"):
                    val = cr.get(key)
                    if isinstance(val, str) and val.startswith(".agents/changes/"):
                        bad.append(f"{jf}: crs[].{key} starts with .agents/changes/: {val}")
    return bad


def main(argv: list[str]) -> int:
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8")
    dry = "--dry-run" in argv
    folders = [Path(a) for a in argv if not a.startswith("--")]
    if not folders:
        print("usage: migrate-legacy.py [--dry-run] <planning folder>...", file=sys.stderr)
        return 2
    try:
        for folder in folders:
            if not folder.is_dir():
                raise Refusal(f"{folder}: not a folder")
        for folder in folders:
            print(f"== {folder} ({'surface' if is_surface(folder) else 'chantier'}"
                  f"{', dry run' if dry else ''})")
            (migrate_surface if is_surface(folder) else migrate_chantier)(folder, dry)
        if not dry:
            print("== scan")
            bad = [b for f in folders for b in scan(f)]
            for b in bad:
                print(f"BAD {b}")
            print("scan: " + ("clean" if not bad else f"{len(bad)} problem(s)"))
            return 1 if bad else 0
    except Refusal as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
