"""Non-marker code differences between two revisions (read-only)."""
import collections
import re
import subprocess
import sys

REPO, BASE, HEAD = sys.argv[1:4]


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, check=True).stdout.decode("utf-8", "replace")


MARK = re.compile(r"@(tests_req|accepts_req|implements_req)\b")
files = [f for f in git("diff", "--name-only", "--no-renames", BASE, HEAD).split("\n") if f]
main_files = set(f for f in git("diff", "--name-only", "--no-renames", "4a47151e", BASE).split("\n") if f)


def content(rev, f):
    p = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{f}"], capture_output=True)
    return p.stdout.decode("utf-8", "replace").split("\n") if p.returncode == 0 else []


changed = []
removed = collections.Counter()
added = collections.Counter()
for f in files:
    if f.startswith(("requirements/", ".agents/")):
        continue
    a = collections.Counter(x.rstrip() for x in content(BASE, f) if not MARK.search(x) and x.strip())
    b = collections.Counter(x.rstrip() for x in content(HEAD, f) if not MARK.search(x) and x.strip())
    if a != b:
        changed.append((f, sum((a - b).values()), sum((b - a).values()), f in main_files))
        if f.startswith("test/") and not f.startswith(("test/build/", "test/site/requirementsViewer/")):
            for k, n in (a - b).items():
                removed[k] += n
            for k, n in (b - a).items():
                added[k] += n
total_code = [f for f in files if not f.startswith(("requirements/", ".agents/"))]
print("files outside requirements/.agents:", len(total_code), "with non-marker differences:", len(changed))
for c in changed:
    print("  ", c[0], "-%d +%d" % (c[1], c[2]), "(also changed by main since 4a47151e)" if c[3] else "")
lost = removed - added
print("split test files: non-marker lines removed and not re-added anywhere:", sum(lost.values()))
for k, n in lost.most_common(80):
    print("   ", n, k[:150])
