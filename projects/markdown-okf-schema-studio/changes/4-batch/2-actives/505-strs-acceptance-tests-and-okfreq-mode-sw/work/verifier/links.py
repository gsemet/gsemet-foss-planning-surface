"""Verifier of CR-505: compare the broken-link warnings of the two coverage modes, rewrite local paths.

usage: python -I links.py <requirements-lint raw log> <new-mode log>
Paths of the worktree in the first log are replaced by <worktree> in place.
"""
import re
import sys
from pathlib import Path

lint, new = Path(sys.argv[1]), Path(sys.argv[2])
text = lint.read_text(encoding="utf-8", errors="replace")
bs = chr(92)
root = re.compile("[A-Za-z]:[" + bs + bs + "/]Users[^\\r\\n']*?batch-09-CR-505")
text, replaced = root.subn("<worktree>", text)
lint.write_text(text, encoding="utf-8", newline="\n")
LINK = re.compile(r"^W2\w* .*?((?:SwRS|StRS)-MDOKFSTUDIO-[A-Z]+-\d+|[\w.-]+)\.md: Broken cross-link '([^']*)'", re.M)


def warnings(source):
    return sorted(LINK.findall(source))


def block(source):
    """The validate run only: it ends at its own summary of the next command."""
    start = source.index("requirements, 0 errors")
    return source[start:]


old = warnings(block(text))
fresh = warnings(new.read_text(encoding="utf-8"))
print("paths replaced:", replaced, "| user folder left:", "Users" + bs in text or "Users/" in text)
print("broken links, current mode:", len(old))
print("broken links, new mode:", len(fresh))
print("same list:", old == fresh)
print("W004 in new mode:", len(re.findall(r"^W004 ", new.read_text(encoding="utf-8"), re.M)))
