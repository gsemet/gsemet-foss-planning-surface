"""Scratch: resolve conflict hunks by an explicit plan.

Usage: resolve.py <plan.py>   (from the ref root)
The plan defines PLAN = {path: [replacement for hunk 1, replacement for hunk 2, ...]}; a replacement
that is the string "UNION" keeps both sides, "UNION2" keeps both with two blank lines between.
"""
import re
import runpy
import sys
from pathlib import Path

plan = runpy.run_path(sys.argv[1])["PLAN"]
HUNK = re.compile(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)

for path, repls in plan.items():
    text = Path(path).read_text(encoding="utf-8")
    it = iter(repls)

    def pick(m):
        r = next(it)
        if r == "UNION":
            return m.group(1) + m.group(2)
        if r == "UNION1":
            return m.group(1) + "\n" + m.group(2)
        if r == "UNION2":
            return m.group(1) + "\n\n" + m.group(2)
        return r

    new = HUNK.sub(pick, text)
    assert next(it, None) is None, f"{path}: unused replacements"
    assert "<<<<<<<" not in new, f"{path}: hunks left"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new)
    print("resolved", path)
