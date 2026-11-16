"""Scratch: resolve every conflict hunk of the given files by keeping both sides (ours, then theirs).

Usage: union.py file[=N] ...   N blank lines are put between the two sides (default 0).
"""
import sys
from pathlib import Path

for arg in sys.argv[1:]:
    name, _, gap = arg.partition("=")
    gap = int(gap or 0)
    out, state = [], "text"
    for line in Path(name).read_text(encoding="utf-8").splitlines(keepends=True):
        if line.startswith("<<<<<<< "):
            state = "ours"
        elif line.startswith("=======") and state == "ours":
            state = "theirs"
            out.append("\n" * gap)
        elif line.startswith(">>>>>>> ") and state == "theirs":
            state = "text"
        else:
            out.append(line)
    with open(name, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(out))
    print("union", name, "gap", gap)
