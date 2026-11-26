"""Print cards-next topics (or card files) by name, with LF byte sizes."""

import sys
from pathlib import Path

ROOT = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    for name in sys.argv[1:]:
        path = ROOT / name if name.endswith(".md") else ROOT / "topics" / f"{name}.md"
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        print(f"----- {path.name} ({len(text.encode('utf-8'))} B)")
        print(text)


main()
