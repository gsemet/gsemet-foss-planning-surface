"""Round 9: move inventory rows to the topic that holds their rule.

Run: python -I rehome.py <evidence folder> [--apply]
Without --apply it prints each change and writes nothing.
"""

import pathlib
import re
import sys

# id -> (new home topic, text after the topic name, or None to keep the old tail)
MOVES = {
    "C-028": ("recovery", "; the rule it applies: floor 7"),
    "C-029": ("demo", ""),
    "C-410": ("batch-plan-mode", None),
    "C-412": ("batch-plan-mode", ""),
    "C-417": ("batch-plan-mode", ""),
    "C-426": ("batch-plan-mode", ""),
    "C-432": ("batch-plan-cut", ""),
    "C-433": ("batch-plan-cut", ""),
    "C-439": ("batch-plan-cut", ""),
    "C-442": ("batch-plan-cut", ""),
    "C-444": ("batch-plan-cut", ""),
    "C-449": ("batch-plan-cut", ""),
    "C-451": ("foreman-start", ""),
    "C-453": ("foreman-start", ""),
    "C-455": ("batch-plan-mode", ""),
    "C-511": ("order-verbs", None),
    "C-519": ("order-drop", ""),
    "C-547": ("driver-question", ""),
    "C-1098": ("grill-series", "; no rule: a worked example"),
    "C-1127": ("grill-specify", ""),
    "C-1277": ("ticket-summary", ""),
    "FM-103": ("ready-asks", ""),
    "FM-459": ("lost-silent", None),
    "H-127": ("merge", ""),
    "H-130": ("merge", ""),
}


def cells(line):
    return re.split(r"(?<!\\)\|", line)


def main():
    folder = pathlib.Path(sys.argv[1])
    apply = "--apply" in sys.argv
    seen = {key: [0, 0] for key in MOVES}
    for path in sorted(folder.glob("cards-inventory-*.md")):
        raw = path.read_bytes().decode("utf-8")
        lines = raw.split("\n")
        changed = False
        for index, line in enumerate(lines):
            parts = cells(line.rstrip("\r"))
            if len(parts) < 4 or parts[1].strip() not in MOVES:
                continue
            key = parts[1].strip()
            topic, tail = MOVES[key]
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
            match = re.match(r"topic ([a-z0-9-]+)(.*)$", old_home)
            kept = match.group(2) if match and tail is None else (tail or "")
            new_home = f"topic {topic}{kept}"
            parts[home_at] = f" {new_home} "
            if check_at is not None:
                old_check = parts[check_at].strip()
                tick = "`" if old_check.startswith("`") or key.startswith(("H-",)) else ""
                parts[check_at] = f" {tick}help {topic}{tick} "
                print(f"{path.name}:{index + 1} {key}: {old_home} [{old_check}] -> {new_home} [{parts[check_at].strip()}]")
            else:
                print(f"{path.name}:{index + 1} {key} (end list): {old_home} -> {new_home}")
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
