# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Validate the planning folders of the surface's projects (all, or the ones named).

The format of a change request belongs to chantier: the surface checks only what chantier does
not check yet, and runs chantier for the rest.

For each project with a `changes/` folder:

1. Each change request (a folder with `01-intent.md`) is placed from its path: its stage and its
   priority come from the folder. A change request outside a stage folder, a priority folder
   outside `2-backlog`, or a backlog item without a P1..P4 folder fails. The table of change
   requests is printed.
2. `chantier summary lint` lists the change requests whose `summary.json` (read by chantier's
   board) is missing or late. It is reported and fails nothing (chantier: a late summary blocks
   nothing); only a chantier that cannot run fails.

chantier runs from its GitHub tag through `uvx`, with the surface's `uv.toml` passed explicitly:
`uvx` reads only the user's uv configuration, not the one of the current folder.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHANTIER_REF = "v0.11.0"
CHANTIER = [
    "uvx", "--quiet", "--config-file", str(ROOT / "uv.toml"),
    "--from", f"git+https://github.com/gsemet/chantier@{CHANTIER_REF}", "chantier",
]
LINT_GAPS = 2  # chantier summary lint's exit code when it lists gaps

# Folder under changes/ -> stage. A stage folder may hold P1..P4 priority folders (the backlog).
STAGES = {
    "1-inbox": "inbox",
    "2-backlog": "backlog",
    "3-ready": "ready",
    "4-batch/1-pending": "batch-pending",
    "4-batch/2-actives": "batch-active",
    "4-batch/3-done": "batch-done",
    "5-archives": "archived",
    "6-trash": "trash",
}
PRIORITY = re.compile(r"^P[1-4]$")


def place(intent: Path, changes: Path) -> tuple[str, str | None, str | None]:
    """Return (stage, priority, problem) of the change request whose 01-intent.md is *intent*."""
    parts = intent.parent.relative_to(changes).parts[:-1]  # folders between changes/ and the CR
    priority = None
    if parts and PRIORITY.match(parts[-1]):
        priority, parts = parts[-1], parts[:-1]
    stage = STAGES.get("/".join(parts))
    if stage is None:
        return "?", priority, f"not in a stage folder: changes/{'/'.join(parts) or '.'}"
    if priority and stage != "backlog":
        return stage, priority, f"a priority folder outside 2-backlog: {priority}"
    if stage == "backlog" and not priority:
        return stage, None, "in 2-backlog without a P1..P4 folder"
    return stage, priority, None


def check_change_requests(changes: Path) -> bool:
    ok = True
    rows = []
    for intent in sorted(changes.rglob("01-intent.md")):
        stage, priority, problem = place(intent, changes)
        if problem:
            ok = False
            print(f"  ERROR   {intent.relative_to(ROOT)}: {problem}")
        rows.append((intent.parent.name, stage, priority or "-"))
    if rows:
        width = max(len(r[0]) for r in rows)
        print(f"  {'change request':<{width}}  {'stage':<13}  priority")
        for folder, stage, priority in rows:
            print(f"  {folder:<{width}}  {stage:<13}  {priority}")
    return ok


def summary_lint(project: Path) -> bool:
    """Print chantier's summary lint; False only when chantier itself could not run."""
    result = subprocess.run(
        [*CHANTIER, "--project", str(project), "summary", "lint"],
        check=False, capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=ROOT,
    )
    lines = [line for line in (result.stdout + result.stderr).splitlines() if line.strip()]
    if result.returncode not in (0, LINT_GAPS) or (lines and lines[0].startswith("error")):
        print(f"  ERROR   chantier summary lint could not run (exit {result.returncode}):")
        for line in lines:
            print(f"    {line}")
        return False
    if result.returncode == LINT_GAPS:
        print("  NOTE    chantier summary lint (fails nothing):")
        for line in lines:
            print(f"    {line.split(' → ', 1)[0]}")
    else:
        print(f"  chantier summary lint: {lines[0] if lines else 'no gap'}")
    return True


def main(argv: list[str]) -> int:
    projects = sorted(p for p in (ROOT / "projects").iterdir() if p.is_dir())
    if argv:
        wanted = set(argv)
        projects = [p for p in projects if p.name in wanted]
        missing = wanted - {p.name for p in projects}
        if missing:
            print(f"unknown project(s): {', '.join(sorted(missing))}", file=sys.stderr)
            return 2
    failed: list[str] = []
    for project in projects:
        changes = project / "changes"
        if not changes.is_dir():
            print(f"-- {project.name}: no changes/ folder, skipped")
            continue
        print(f"== {project.name}", flush=True)
        placed = check_change_requests(changes)
        linted = summary_lint(project)
        if not (placed and linted):
            failed.append(project.name)
    if failed:
        print(f"FAILED: {', '.join(failed)}", file=sys.stderr)
        return 1
    print("all planning folders conformant")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
