"""Import closure of each integration suite at the head, against the files the change touches.

Usage: python -I suiteclosure.py <worktree> <base> <head>
Also lists, for the base and the head, the files that hold `@accepts_req` and the suites that reach them.
"""
import posixpath
import re
import subprocess
import sys

worktree, base, head = sys.argv[1:4]


def git(*args):
    return subprocess.run(["git", "-C", worktree, *args], check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout


IMPORT = re.compile(r"""(?:from\s+|import\s*\(\s*|require\s*\(\s*|^\s*import\s+)["'](\.{1,2}/[^"']+)["']""", re.M)


def closure(sha, entry):
    files = set(git("ls-tree", "-r", "--name-only", sha).splitlines())
    seen, todo = set(), [entry]
    while todo:
        path = todo.pop()
        if path in seen or path not in files:
            continue
        seen.add(path)
        for spec in IMPORT.findall(git("show", f"{sha}:{path}")):
            target = posixpath.normpath(posixpath.join(posixpath.dirname(path), spec))
            for candidate in (target + ".ts", target + "/index.ts", target):
                if candidate in files:
                    todo.append(candidate)
                    break
    return seen


def code_changes(path):
    lines = git("diff", "-U0", base, head, "--", path).splitlines()
    body = [l for l in lines if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    code = [l for l in body if l[1:].strip() and not l[1:].strip().startswith(("//", "*", "/*"))]
    return len(body), code


changed = set(git("diff", "--name-only", base, head).splitlines())
suites = ["scroll-sync-suite", "untrusted-suite", "trusted-suite", "standalone-suite",
          "reverse-migration-suite", "reload-suite"]
for suite in suites:
    entry = f"test/integration/{suite}.ts"
    reached = closure(head, entry)
    touched = sorted(reached & changed)
    print(f"== {suite}: {len(reached)} files reached, {len(touched)} touched by the change")
    for path in touched:
        total, code = code_changes(path)
        print(f"   {path}: changed lines {total}, non-comment changed lines {len(code)}")
        for line in code[:6]:
            print(f"      {line[:140]}")

for sha in (base, head):
    hits = [l.split(":", 1)[1] for l in git("grep", "-c", "@accepts_req", sha, "--", "test").splitlines()]
    reach = {s: closure(sha, f"test/integration/{s}.ts") for s in suites}
    print(f"== @accepts_req at {sha[:7]}")
    total = 0
    for hit in hits:
        path, count = hit.rsplit(":", 1)
        by = [s for s in suites if path in reach[s]]
        total += int(count)
        print(f"   {path}: {count} line(s), reached by {by or 'NO integration suite'}")
    print(f"   marker lines: {total}")
