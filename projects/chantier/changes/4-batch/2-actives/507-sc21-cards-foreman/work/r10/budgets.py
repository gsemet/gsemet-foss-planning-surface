"""List cards-next files over their LF byte budget.

Run: python -I budgets.py <cards-next folder> <pr-body.md>
Topics over 1,500 B that the pr-body Known gaps text already lists are marked "listed".
"""

import json
import pathlib
import re
import sys

CARDS = {"foreman.md": 4000, "chief-of-staff.md": 6000, "skills/griller-SKILL.md": 4000, "griller-skill.md": 4000, "cr-driver.md": 4096, "stack-driver.md": 4096}


def size(path):
    return len(path.read_bytes().replace(b"\r\n", b"\n"))


def main():
    root = pathlib.Path(sys.argv[1])
    body = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
    listed = dict((m.group(1), int(m.group(2).replace(",", ""))) for m in re.finditer(r"\b([a-z0-9-]+) ([0-9],[0-9]{3})\b", body))
    for name, limit in CARDS.items():
        path = root / name
        if path.exists() and size(path) > limit:
            print("CARD OVER", name, size(path), limit)
    for path in sorted((root / "topics").glob("*.md")):
        n = size(path)
        if n > 1500:
            was = listed.get(path.stem)
            state = "new" if was is None else ("same" if was == n else f"listed {was}")
            print(f"{path.stem} {n} {state}")
    for name, was in listed.items():
        path = root / "topics" / f"{name}.md"
        if was > 1500 and (not path.exists() or size(path) <= 1500):
            print("listed but no longer over", name, was)
    data = json.loads((root / "topics.json").read_text(encoding="utf-8"))
    readings = []
    for entry in data["topics"].values():
        for reading in entry["readings"]:
            readings.extend(reading.values() if isinstance(reading, dict) else [reading])
    missing = [r for r in readings if isinstance(r, str) and not (root / r).exists()]
    print("topics", len(data["topics"]), "readings", len(readings), "missing", missing)
    used = {r for r in readings if isinstance(r, str)}
    for path in sorted((root / "topics").glob("*.md")):
        if f"topics/{path.name}" not in used:
            print("unreferenced", path.name)


if __name__ == "__main__":
    main()
