# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Validate every project bundle of the planning surface against the shared schemas.

A project is a bundle once it has an `index.md` at its root (projects/<name>/index.md); the others
are listed as not yet bundles and fail nothing. Each bundle is validated with okf-schema, strict,
against `_schemas/`.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

OKF_SCHEMA = ["uvx", "--python", "3.12", "--from", "okf-schema==0.17.0", "okf-schema"]
ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "_schemas"


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
        result = subprocess.run(
            [*OKF_SCHEMA, "validate", "--path", str(project), "--schema-db", str(SCHEMAS),
             "--strict", "--check-links"],
            check=False,
        )
        if result.returncode != 0:
            failed.append(project.name)
    if failed:
        print(f"FAILED: {', '.join(failed)}", file=sys.stderr)
        return 1
    print("all bundles conformant")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
