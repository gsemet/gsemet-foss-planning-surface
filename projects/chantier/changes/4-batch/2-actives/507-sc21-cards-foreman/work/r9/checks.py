"""Read-only: topic files and the topic index of cards-next.

Run: python -I checks.py <worktree>
(a) each `-p<n>.md` header says "part n of m", m the number of parts; (b) every row that reads
one part of a split file reads all its parts, in order; (c) topic and card sizes in LF bytes
over their budgets; (d) `part <n>` mentions inside a part stay within the number of parts.
"""

import json
import pathlib
import re
import sys

CARD_BUDGETS = {
    "foreman.md": 4000,
    "chief-of-staff.md": 6000,
    "griller-skill.md": 4000,
    "coder.md": 1500,
}


def size(path):
    return len(path.read_bytes().replace(b"\r\n", b"\n"))


def main():
    root = pathlib.Path(sys.argv[1], "skills/chantier/cards-next")
    topics = root / "topics"
    parts = {}
    for path in sorted(topics.glob("*.md")):
        found = re.fullmatch(r"(.+)-p(\d+)\.md", path.name)
        if found:
            parts.setdefault(found.group(1), []).append(int(found.group(2)))
    for base, numbers in sorted(parts.items()):
        numbers.sort()
        if numbers != list(range(1, len(numbers) + 1)):
            print("gap in parts", base, numbers)
        for n in numbers:
            text = (topics / f"{base}-p{n}.md").read_text(encoding="utf-8")
            head = text.split("\n", 1)[0]
            said = re.search(r"\(part (\d+) of (\d+)\)", head)
            if said and (int(said[1]), int(said[2])) != (n, len(numbers)):
                print("header", base, n, head)
            for mention in re.findall(r"[Pp]arts? (\d+)", text.split("\n", 1)[-1]):
                if int(mention) > len(numbers):
                    print("mention", base, n, mention)
    index = json.loads((root / "topics.json").read_text(encoding="utf-8"))["topics"]
    for name, row in index.items():
        files = []
        for reading in row["readings"]:
            files += reading.values() if isinstance(reading, dict) else [reading]
        for base, numbers in parts.items():
            wanted = [f"topics/{base}-p{n}.md" for n in numbers]
            have = [f for f in files if f in wanted]
            if have and have != wanted:
                print("row", name, base, [f[-6:] for f in have], len(wanted))
    over = [
        (size(p), p.name)
        for p in sorted(topics.glob("*.md"))
        if size(p) > 1500
    ]
    print("topics over 1500:", len(over))
    for bytes_, name in over:
        print(f"  {bytes_} {name}")
    for name, budget in CARD_BUDGETS.items():
        print(f"{name}: {size(root / name)} of {budget}")


if __name__ == "__main__":
    main()
