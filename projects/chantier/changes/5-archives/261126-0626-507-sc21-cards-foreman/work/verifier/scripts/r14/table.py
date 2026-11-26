"""Verifier: the PR body's edited-lines table against the head. Each listed `file line` must differ
from the earlier families' tree (`fe7fbf0f`), and every line a file of that tree changed must be
listed."""

import difflib
import re
import subprocess
from pathlib import Path

CR = Path("<CR folder>")
W = "<worktree>"
CN = "skills/chantier/cards-next"
EARLY = "fe7fbf0f"


def git(*a):
    return subprocess.run(["git", "-C", W, *a], capture_output=True, check=True).stdout.decode("utf-8")


def tree(rev):
    return {p[len(CN) + 1:] for p in git("ls-tree", "-r", "--name-only", rev, "--", CN).split("\n") if p}


old_tree, head_tree = tree(EARLY), tree("HEAD")


def lines(rev, f):
    return git("show", f"{rev}:{CN}/{f}").split("\n")[:-1]


def changed(f):
    b = lines("HEAD", f)
    if f not in old_tree:
        return set(range(1, len(b) + 1)), 0
    a = lines(EARLY, f)
    out, gone = set(), 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag in ("replace", "insert"):
            out |= set(range(j1 + 1, j2 + 1))
        if tag == "delete":
            gone += i2 - i1
    return out, gone


body = (CR / "pr-body.md").read_text(encoding="utf-8").split("\n")
start = next(i for i, x in enumerate(body) if x.startswith("| File and line"))
rows = []
for x in body[start + 2:]:
    if not x.startswith("|"):
        break
    c = [y.strip() for y in x.strip().strip("|").split("|")]
    rows.append((c[0], c[1]))


def resolve(name, topics):
    name = name.removesuffix(".md")
    order = (f"{name}.md", f"topics/{name}.md")
    for cand in (*(order[::-1] if topics else order), f"skills/{name}.md"):
        if cand in head_tree:
            return cand
    return None


def numbers(text):
    out = set()
    for tok in re.findall(r"\d+(?:-\d+)?", text):
        a, _, b = tok.partition("-")
        out |= set(range(int(a), int(b or a) + 1))
    return out


listed = {}
for cell, _ in rows:
    if cell == "topics.json":
        continue
    topics = cell.startswith(("topics:", "topics, rules put back:"))
    text = cell.split(":", 1)[1] if topics else cell
    cur = None
    # tokens: a name (with .md or a topic name) followed by its line numbers
    for m in re.finditer(r"(?P<name>[A-Za-z][A-Za-z0-9-]*(?:\.md)?)(?P<nums>(?:\s+\d+(?:-\d+)?(?:(?:,\s*|\s+and\s+)\d+(?:-\d+)?(?![\w.-]))*))", text):
        name, nums = m["name"], numbers(m["nums"])
        if name == "and":
            name = cur
        f = resolve(name, topics)
        if f is None:
            print("UNRESOLVED", name, m["nums"])
            continue
        cur = name
        listed.setdefault(f, set()).update(nums)

print("rows", len(rows), "files listed", len(listed))
bad = []
for f, ns in sorted(listed.items()):
    ch, _ = changed(f)
    n = len(lines("HEAD", f))
    for k in sorted(ns):
        if k > n:
            bad.append((f, k, f"beyond end ({n})"))
        elif k not in ch:
            bad.append((f, k, "unchanged since " + EARLY))
print("listed lines that do not differ:", len(bad))
for b in bad:
    print("  ", b, "|", lines("HEAD", b[0])[b[1] - 1][:120] if "unchanged" in b[2] else "")

status = [x.split("\t") for x in git("diff", "--name-status", "-M", EARLY, "HEAD", "--", CN).split("\n") if x]
mod = [(s[0], s[-1][len(CN) + 1:], s[1][len(CN) + 1:]) for s in status]
print("changes since", EARLY, {k: sum(1 for m in mod if m[0][0] == k) for k in "AMDR"})
print("\n-- files of the earlier tree, modified or renamed, with unlisted changed lines")
for s, f, was in mod:
    if s[0] == "D":
        print("  deleted", f)
        continue
    if s[0] == "A" or f == "topics.json":
        continue
    if s[0] == "R":
        a, b = lines(EARLY, was), lines("HEAD", f)
        ch = set()
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
            if tag in ("replace", "insert"):
                ch |= set(range(j1 + 1, j2 + 1))
        gone = 0
    else:
        ch, gone = changed(f)
    miss = sorted(k for k in ch - listed.get(f, set()) if lines("HEAD", f)[k - 1].strip())
    if miss or f not in listed:
        print(f"  {s} {f} (was {was}) unlisted {miss} changed {sorted(ch)} listed {sorted(listed.get(f, set()))} deleted-lines {gone}")
