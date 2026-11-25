"""Check that the texts the specification dictates are in the files at head (run from the worktree)."""

import re
import sys
from pathlib import Path

root = Path("C:/Users/gaeta/Projets/okf-schema.worktrees/batch-01-CR-104")
spec = Path(sys.argv[1]).read_text(encoding="utf-8")


def read(rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8")


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def spec_row(prefix: str) -> str:
    """Return the backtick-quoted table row of the specification starting with prefix."""
    for line in spec.splitlines():
        line = line.strip()
        line = line.rstrip(".")
        if line.startswith("`" + prefix) and line.endswith("`"):
            return line[1:-1]
        if line.startswith("- `" + prefix) and line.endswith("`"):
            return line[3:-1]
    raise SystemExit("row not found in the specification: " + prefix)


checks = [
    ("feature map row", "docs/source/explanation/project-feature-coverage.md",
     spec_row("| OKF 0.2 trust tier and actor forms")),
    ("how-to W10 row", "docs/source/how-to/validate-standalone-files.md", spec_row("| **W10** |")),
    ("okf-schema skill W10 row", "skills/okf-schema/SKILL.md", spec_row("| W10 | Actor syntax")),
    ("record-findings example", "skills/okfkb-record-findings/SKILL.md",
     "by: <actor, e.g. human:alice or reference_agent/gemini-2.5-pro>"),
    ("shipped schema description", "src/okf_schema/data/kb/_schema/Base.schema.yaml",
     "description: Actor string (OKF 0.2 section 7), e.g. 'human:alice', 'process:nightly-check' or "
     "'reference_agent/gemini-2.5-pro'."),
    ("example schema description", "examples/okfkb-hw-knowledge-base/_schema/Base.schema.yaml",
     "description: Actor string (OKF 0.2 section 7), e.g. 'human:alice', 'process:nightly-check' or "
     "'reference_agent/gemini-2.5-pro'."),
    ("module docstring W10", "src/okf_schema/validator.py",
     "W10 – `verified[].by` actor in no OKF 0.2 form (`<producer>/<version>`, `<prefix>:<identifier>`)"),
    ("W10 title", "docs/source/reference/validation-codes.md",
     "### W10: Unrecognized Actor String in `verified[].by`"),
    ("W10 example comment", "docs/source/reference/validation-codes.md",
     "# no recognized form: counts as machine-confirmed"),
    ("W10 fix human", "docs/source/reference/validation-codes.md", 'by: "human:alice"'),
    ("W10 fix agent", "docs/source/reference/validation-codes.md", 'by: "reference_agent/gemini-2.5-pro"'),
    ("W10 stable code", "docs/source/reference/validation-codes.md", "Stable code: `W10`"),
    ("log subheading", "requirements/tiers/log.md", "## 2026-11-25 ### Trust tier actor forms"),
]
for name, rel, wanted in checks:
    print(f"{'ok     ' if norm(wanted) in norm(read(rel)) else 'MISSING'} {name}: {rel}")
log = read("requirements/tiers/log.md")
print("day headings 2026-11-25:", len(re.findall(r"(?m)^## 2026-11-25$", log)),
      "| first heading:", re.findall(r"(?m)^## .+$", log)[0])
section = read("docs/source/reference/validation-codes.md").split("### W10:")[1].split("\n---")[0]
print("--- W10 section as at head")
print("### W10:" + section.rstrip())
