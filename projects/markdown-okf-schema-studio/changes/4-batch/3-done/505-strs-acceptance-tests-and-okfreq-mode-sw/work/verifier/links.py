"""Verifier of CR-505: compare the broken-link warnings of the two coverage modes, rewrite local paths.

usage: python -I links.py <requirements-lint raw log> <new-mode log>
Paths of the worktree in the first log are replaced by <worktree> in place. `just requirements-lint`
runs okfreq `validate` and then `lint`, and each prints the broken links, so the current-mode log
holds each of them twice.
"""
import re
import sys
from collections import Counter
from pathlib import Path

lint, new = Path(sys.argv[1]), Path(sys.argv[2])
text = lint.read_text(encoding="utf-8", errors="replace")
bs = chr(92)
root = re.compile("[A-Za-z]:[" + bs + bs + "/]Users[^\\r\\n']*?batch-09-CR-505")
text, replaced = root.subn("<worktree>", text)
lint.write_text(text, encoding="utf-8", newline="\n")
LINK = re.compile(r"^W2\w* .*?((?:SwRS|StRS)-MDOKFSTUDIO-[A-Z]+-\d+|[\w.-]+)\.md: Broken cross-link '([^']*)'", re.M)


def warnings(source):
    return Counter(LINK.findall(source))


old = warnings(text)
fresh = warnings(new.read_text(encoding="utf-8"))
print("paths replaced:", replaced, "| user folder left:", "Users" + bs in text or "Users/" in text)
print("broken-link lines, current mode:", sum(old.values()), "| distinct:", len(old))
print("broken-link lines, new mode:", sum(fresh.values()), "| distinct:", len(fresh))
print("same distinct links:", set(old) == set(fresh))
print("each printed exactly twice in the current-mode log:", old == fresh + fresh)
print("W004 in new mode:", len(re.findall(r"^W004 ", new.read_text(encoding="utf-8"), re.M)))
