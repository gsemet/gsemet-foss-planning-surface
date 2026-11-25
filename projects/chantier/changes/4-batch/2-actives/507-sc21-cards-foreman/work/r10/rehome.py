"""Round 10: set the `new home` (and `check`) cell of rows whose home did not hold their rule.

Run: python -I rehome.py <evidence folder> [--apply]
Without --apply it prints each change and writes nothing.
"""

import pathlib
import re
import sys

# id -> (new home cell, new check cell or None to keep it)
MOVES = {
    "C-1376": ("topic release-chief-after", "help release-chief-after"),
    "C-495": ("card chief-of-staff.md:39", None),
    "H-089": ("topic batch-plan-show, board; card chief-of-staff.md:26 (the writer stages the surface)", None),
    "H-186": ("topic batch-pause, retro, retro-lines", "help retro"),
    "H-187": ("topic retro", "help retro"),
    "C-024": ("topic pr-template-own", "help pr-template-own"),
    "H-282": ("topic long-gate", "help long-gate"),
    "H-711": ("topic status-notes-more", "help status-notes-more"),
    "C-1031": ("topic grill-series", "help grill-series"),
    "C-1032": ("topic grill-series", "help grill-series"),
    "C-1033": ("topic grill-series", "help grill-series"),
    "C-793": ("topic stack-changes-chief", "help stack-changes-chief"),
    "C-797": ("topic stack-changes-chief", "help stack-changes-chief"),
    "C-1152": ("topic grill-backlog", "help grill-backlog"),
    "H-1449": ("topic host-allow-add", "help host-allow-add"),
}


def cells(line):
    return re.split(r"(?<!\\)\|", line)


def main():
    folder = pathlib.Path(sys.argv[1])
    apply = "--apply" in sys.argv
    seen = {key: [0, 0] for key in MOVES}
    for path in sorted(folder.glob("cards-inventory-*.md")):
        lines = path.read_bytes().decode("utf-8").split("\n")
        changed = False
        for index, line in enumerate(lines):
            parts = cells(line.rstrip("\r"))
            if len(parts) < 4 or parts[1].strip() not in MOVES:
                continue
            key = parts[1].strip()
            home, check = MOVES[key]
            if len(parts) == 10:
                home_at, check_at = 7, 8
                seen[key][0] += 1
            elif len(parts) == 5:
                home_at, check_at = 3, None
                seen[key][1] += 1
            else:
                print("unexpected shape", path.name, index + 1, len(parts))
                continue
            old_home = parts[home_at].strip()
            parts[home_at] = f" {home} "
            if check_at is not None and check is not None:
                old = parts[check_at].strip()
                tick = "`" if old.startswith("`") else ""
                parts[check_at] = f" {tick}{check}{tick} "
            print(f"{path.name}:{index + 1} {key}: {old_home} -> {home}")
            ending = "\r" if line.endswith("\r") else ""
            lines[index] = "|".join(parts) + ending
            changed = True
        if changed and apply:
            path.write_bytes("\n".join(lines).encode("utf-8"))
    for key, (main_rows, end_rows) in seen.items():
        if main_rows != 1:
            print("main row count", key, main_rows, "end rows", end_rows)


if __name__ == "__main__":
    main()
