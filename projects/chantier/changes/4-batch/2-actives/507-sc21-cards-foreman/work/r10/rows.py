"""Print inventory rows by id: id, home, check, quoted behaviour.

Run: python -I rows.py <evidence folder> <id> [<id> ...] [--full]
"""

import pathlib
import re
import sys


def split(line):
    return [part.strip() for part in re.split("(?<!" + chr(92) * 2 + ")" + chr(92) + "|", line)]


def main():
    evidence = pathlib.Path(sys.argv[1])
    full = "--full" in sys.argv
    wanted = [a for a in sys.argv[2:] if a != "--full"]
    found = {}
    for path in sorted(evidence.glob("cards-inventory-*.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            parts = split(line)
            if len(parts) >= 10 and parts[1] in wanted:
                found[parts[1]] = (parts[7], parts[5], parts[4])
    for row in wanted:
        if row not in found:
            print(row, "NOT FOUND")
            continue
        home, source, text = found[row]
        print(f"{row} -> {home} [{source}]")
        if full:
            print("   ", text)


if __name__ == "__main__":
    main()
