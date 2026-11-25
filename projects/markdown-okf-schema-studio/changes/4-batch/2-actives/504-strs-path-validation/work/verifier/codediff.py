"""Changed files whose content differs beyond marker lines, comment-only lines and blank lines."""
import re
import subprocess
import sys

REPO, BASE, HEAD = sys.argv[1:4]


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, check=True).stdout.decode("utf-8", "replace")


MARK = re.compile(r"@(tests_req|accepts_req|implements_req)\b")


def strip(rev, path):
    p = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"], capture_output=True)
    if p.returncode:
        return None
    out = []
    for line in p.stdout.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
        s = line.strip()
        if MARK.search(s) or s in ("", "/**", "*/", "*", '"""') or s.startswith("//"):
            continue
        # a doc comment that absorbed or lost a marker line: /** text */ and * text compare equal
        s = re.sub(r"^(/\*\*|\*)\s*", "", s)
        s = re.sub(r"\s*\*/$", "", s)
        out.append(s)
    return out


changed = [f for f in git("diff", "--name-only", "-z", BASE, HEAD).split("\0") if f and not f.startswith("requirements/")]
code = [f for f in changed if strip(BASE, f) != strip(HEAD, f)]
print("changed files outside requirements/:", len(changed))
print("with changes beyond marker and comment lines:", len(code))
for f in code:
    print("  ", f)
