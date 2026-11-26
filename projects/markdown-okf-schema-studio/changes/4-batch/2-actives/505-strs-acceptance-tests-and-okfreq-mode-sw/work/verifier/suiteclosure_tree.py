"""Verifier of CR-505: which integration suites reach the files that hold `@accepts_req`, in one tree.

usage: python -I suiteclosure_tree.py <tree>
Reads the files of the tree (no git call per file) and follows relative imports from each suite.
"""
import os
import posixpath
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1])
IMPORT = re.compile(r"""(?:from\s+|import\s*\(\s*|require\s*\(\s*|^\s*import\s+)["'](\.{1,2}/[^"']+)["']""", re.M)
files = {}
for top in ("test", "src", "scripts"):
    for root, _, names in os.walk(tree / top):
        for name in names:
            full = Path(root) / name
            files[full.relative_to(tree).as_posix()] = full


def closure(entry):
    seen, todo = set(), [entry]
    while todo:
        path = todo.pop()
        if path in seen or path not in files:
            continue
        seen.add(path)
        for spec in IMPORT.findall(files[path].read_text(encoding="utf-8", errors="replace")):
            target = posixpath.normpath(posixpath.join(posixpath.dirname(path), spec))
            for candidate in (target + ".ts", target + "/index.ts", target):
                if candidate in files:
                    todo.append(candidate)
                    break
    return seen


suites = ["scroll-sync-suite", "untrusted-suite", "trusted-suite", "standalone-suite",
          "reverse-migration-suite", "reload-suite"]
reach = {s: closure(f"test/integration/{s}.ts") for s in suites}
for suite in suites:
    print(f"{suite}: {len(reach[suite])} files reached")
MARK = re.compile(r"^\s*(?://|/\*+|\*|#)\s*@accepts_req\s+(\S+)", re.M)
total = 0
for path in sorted(files):
    if not path.startswith("test/") or not path.endswith((".ts", ".py", ".mjs", ".js")):
        continue
    found = MARK.findall(files[path].read_text(encoding="utf-8", errors="replace"))
    if not found:
        continue
    by = [s for s in suites if path in reach[s]]
    total += len(found)
    print(f"{path}: {len(found)} marker line(s), reached by {by or 'NO integration suite'}")
print(f"marker lines: {total}")
