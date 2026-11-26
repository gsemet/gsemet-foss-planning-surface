"""Every `[foreman→chief-of-staff] ...` code span of the base's Foreman cards, whitespace joined, looked for in the new card and topics."""

import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
W = "<worktree>"
SPAN = re.compile(r"`(\[foreman→chief-of-staff\][^`]*)`")


def git(*args):
    return subprocess.run(["git", *args], cwd=W, capture_output=True, check=True, text=True, encoding="utf-8").stdout


def spans(rev, keep):
    found = {}
    for path in git("ls-tree", "-r", "--name-only", rev, "skills/chantier").splitlines():
        if keep(path):
            text = git("show", f"{rev}:{path}")
            for m in SPAN.finditer(text):
                found.setdefault(" ".join(m[1].split()), path.rsplit("/", 1)[1])
    return found


print("head", git("rev-parse", "HEAD").strip())
base = spans("24111e6d", lambda p: re.search(r"references/foreman[^/]*\.md$", p))
head = spans("HEAD", lambda p: p.startswith("skills/chantier/cards-next/") and p.endswith(".md"))
head_text = " ".join(
    " ".join(git("show", f"HEAD:{p}").split())
    for p in git("ls-tree", "-r", "--name-only", "HEAD", "skills/chantier/cards-next").splitlines()
    if p.endswith(".md")
)
print("base reply spans:", len(base), "| missing byte for byte at head:",
      [s for s in base if s not in head and s not in head_text])
for s in sorted(base):
    print("  ", s)
short = "pong <first line of status>"
print("pong form in new foreman card:", short in git("show", "HEAD:skills/chantier/cards-next/foreman.md"))
print("base pong text:", [l.strip() for l in git("show", "24111e6d:skills/chantier/references/foreman.md").splitlines() if "pong" in l])
