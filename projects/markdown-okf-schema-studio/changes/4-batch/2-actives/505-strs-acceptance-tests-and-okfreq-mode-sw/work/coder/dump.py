"""For one SwRS, print every `@tests_req` marker block of it with the code that follows (read only).

usage: python -I dump.py <worktree> NNN [NNN ...]
"""
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
root = Path(sys.argv[1])
COMMENT = re.compile(r"^\s*(//|#|\*|/\*|<!--|$)")


def block(lines, start):
    """The lines from a marker to the end of the declaration that follows it."""
    index = start
    while index < len(lines) and COMMENT.match(lines[index]):
        index += 1
    if index >= len(lines):
        return start, index
    first = lines[index]
    indent = len(first) - len(first.lstrip())
    end = index
    if first.rstrip().endswith((";", "};")) and first.count("(") == first.count(")") and first.count("{") == first.count("}"):
        return start, min(len(lines), index + 25)
    for end in range(index + 1, min(len(lines), index + 140)):
        row = lines[end]
        if row.strip() and len(row) - len(row.lstrip()) <= indent and row.lstrip().startswith(("}", "]", ")")):
            if not row.rstrip().endswith("{"):
                break
    return start, end + 1


for num in sys.argv[2:]:
    ident = f"SwRS-MDOKFSTUDIO-TRUST-{num}"
    found = subprocess.run(
        ["git", "-C", str(root), "grep", "-n", "--untracked", "-E", rf"@tests_req {ident}\b",
         "--", "test", "tests", "sphinx/tests"], capture_output=True).stdout.decode("utf-8")
    seen = {}
    for entry in found.splitlines():
        name, line, text = entry.split(":", 2)
        lines = (root / name).read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
        start, end = block(lines, int(line) - 1)
        key = (name, end)
        seen.setdefault(key, []).append((start, int(line), text.strip()))
    print("#" * 30, ident, len(found.splitlines()), "marker lines")
    for (name, end), marks in seen.items():
        start = min(m[0] for m in marks)
        lines = (root / name).read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
        print("-" * 10, name, "markers:", ", ".join(f"L{m[1]} {m[2].split(ident)[1]}" for m in marks))
        for number in range(max(0, start - 3), end):
            print(f"{number + 1}\t{lines[number]}")
