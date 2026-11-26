"""Per test block, print the trust SwRS markers that HEAD and the worktree do not share."""

import collections
import re
import subprocess
import sys

root = sys.argv[1]
MARK = re.compile(r"@tests_req SwRS-MDOKFSTUDIO-TRUST-(\d{3})(?:#(S\d+))?")
TITLE = re.compile(r"""(?:\b(?:test|it)(?:\.skip)?\(\s*|^\s*def )(["'`]?)(.+?)\1\s*(?:,|\(|$)""")


def git(*args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, check=True).stdout.decode("utf-8")


def blocks(text):
    found = collections.OrderedDict()
    pending = []
    lines = text.replace("\r\n", "\n").split("\n")
    for index, line in enumerate(lines):
        stripped = line.strip()
        hit = MARK.search(line)
        if hit and stripped.startswith(("//", "#", "*", "/*")):
            pending.append(f"{hit.group(1)}#{hit.group(2)}")
            continue
        if not pending or not stripped or stripped.startswith(("//", "#", "*", "/*", "@")):
            continue
        title = TITLE.search(line)
        if not title and re.search(r"\b(?:test|it)\($", stripped):
            title = TITLE.search(stripped + lines[index + 1].strip())
        key = title.group(2) if title else stripped
        found.setdefault(key[:150], collections.Counter()).update(pending)
        pending = []
    return found


def show(counter):
    grouped = collections.OrderedDict()
    for item in sorted(counter.elements()):
        ident, scenario = item.split("#")
        grouped.setdefault(ident, []).append(scenario)
    return "; ".join(f"{ident} {','.join(values)}" for ident, values in grouped.items()) or "none"


for path in git("diff", "--name-only", "HEAD", "--", "test").split():
    before = blocks(git("show", f"HEAD:{path}"))
    with open(f"{root}/{path}", encoding="utf-8") as handle:
        after = blocks(handle.read())
    for key in list(before) + [k for k in after if k not in before]:
        old = before.get(key, collections.Counter())
        new = after.get(key, collections.Counter())
        gone, came = old - new, new - old
        if gone or came:
            name = key.replace("|", "/")
            print(f"| {path.removeprefix('test/')} | {name} | {show(gone)} | {show(came)} |")
