# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Validate every project bundle of the planning surface against the shared schemas.

A project is a bundle once it has an `index.md` at its root (projects/<name>/index.md); the others
are listed as not yet bundles and fail nothing.

For each bundle:

1. okf-schema validates it against `_schemas/`. Every error fails, and every warning except W1
   (recommended `title`): a change request's frontmatter is minimal on purpose, its title is the
   body's heading.
2. Each change request (a folder with `01-intent.md`) is placed from its path: its stage and its
   priority are derived from the folder, never written in the frontmatter. Its frontmatter `id` must
   be the folder's name. The table of change requests is printed.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

OKF_SCHEMA = ["uvx", "--python", "3.12", "--from", "okf-schema==0.17.0", "okf-schema"]
ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "_schemas"
TOLERATED_WARNINGS = {"W1"}

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
WARNING = re.compile(r"WARNING \[(W\d+)\]")
ID_LINE = re.compile(r"^id:\s*['\"]?([^'\"\s]+)", re.MULTILINE)


def run_okf_schema(project: Path) -> bool:
    result = subprocess.run(
        [*OKF_SCHEMA, "validate", "--path", str(project), "--schema-db", str(SCHEMAS),
         "--check-links"],
        check=False, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    output = result.stdout + result.stderr
    blocking = [code for code in WARNING.findall(output) if code not in TOLERATED_WARNINGS]
    shown: list[str] = []
    header: str | None = None  # a file's path line, printed only if one of its findings is shown
    for line in output.splitlines():
        if not line.strip():
            continue
        if not line.startswith(" "):
            if line.startswith(("Bundle", "Validation")):
                shown.append(line)
            else:
                header = line
            continue
        if any(f"[{code}]" in line for code in TOLERATED_WARNINGS):
            continue
        if header is not None:
            shown.append(header)
            header = None
        shown.append(line)
    print("\n".join(shown))
    return result.returncode == 0 and not blocking


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


def check_change_requests(project: Path) -> bool:
    changes = project / "changes"
    if not changes.is_dir():
        return True
    ok = True
    rows = []
    for intent in sorted(changes.rglob("01-intent.md")):
        folder = intent.parent.name
        stage, priority, problem = place(intent, changes)
        match = ID_LINE.search(intent.read_text(encoding="utf-8").split("\n---", 1)[0])
        if match is None or match.group(1) != folder:
            found = match.group(1) if match else "none"
            problem = problem or f"frontmatter id {found} is not the folder name {folder}"
        if problem:
            ok = False
            print(f"  ERROR   {intent.relative_to(ROOT)}: {problem}")
        rows.append((folder, stage, priority or "-"))
    if rows:
        width = max(len(r[0]) for r in rows)
        print(f"  {'change request':<{width}}  {'stage':<13}  priority")
        for folder, stage, priority in rows:
            print(f"  {folder:<{width}}  {stage:<13}  {priority}")
    return ok


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
        if not (project / "index.md").is_file():
            print(f"-- {project.name}: not a bundle yet (no index.md), skipped")
            continue
        print(f"== {project.name}", flush=True)
        valid = run_okf_schema(project)
        placed = check_change_requests(project)
        if not (valid and placed):
            failed.append(project.name)
    if failed:
        print(f"FAILED: {', '.join(failed)}", file=sys.stderr)
        return 1
    print("all bundles conformant")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
