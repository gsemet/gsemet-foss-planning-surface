"""Posted pull request body against the local copy, plus the description rules and the Changes list.

usage: uv run --no-project python -I prcheck.py <pr json> <local body> <worktree> <base> <head>
"""
import difflib
import json
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

data = json.loads(open(sys.argv[1], encoding="utf-8-sig").read())
local = open(sys.argv[2], encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")
body = data["body"].replace("\r\n", "\n").rstrip("\n")
print("title", data["title"])
print("draft", data["isDraft"], "head", data["headRefOid"])
print("author", "set" if data.get("author") else None, "reviewRequests", len(data["reviewRequests"]), "reviews", len(data["reviews"]))
print("--- differences local -> posted")
for line in difflib.unified_diff(local.split("\n"), body.split("\n"), lineterm="", n=0):
    print(line[:220])
print("--- headings")
for line in body.split("\n"):
    if line.startswith("## ") or line.startswith("<details") or line.startswith("</details") or line.startswith("<summary"):
        print(line)
print("--- after </details>:", repr(body.split("</details>")[-1][:80]))
outside = body.split("## Internal references")[0]
for pat in [r"\bCR-?\d+", r"\bbatch\b", r"\bround\b", r"\.agents/changes", r"\b(Driver|Verifier|Inspector|Coder|Foreman|Griller|Investigator)\b", r"#S\d", r"STALE", r"UNVERIFIED",
            r"(?i)c:[\\/]users", r"(?i)gaeta", r"!\[", r"<img", r"(?i)planning"]:
    found = [m.group(0) for m in re.finditer(pat, outside)]
    allfound = len(re.findall(pat, body))
    print(f"{pat}: before Internal references {len(found)}, whole body {allfound}")
for i, line in enumerate(outside.split("\n"), 1):
    if re.search(r"\bCR-?\d+|\bbatch\b|\bround\b|\b(Driver|Verifier|Inspector|Coder|Foreman)\b", line):
        print("   line", i, line[:200])
print("--- Test plan and Impacts")
part = body[body.index("## Impacts"):]
print(part)
print("--- diff file groups")
names = subprocess.run(["git", "-C", sys.argv[3], "diff", "--name-status", f"{sys.argv[4]}...{sys.argv[5]}"], capture_output=True, text=True).stdout.split("\n")
groups = {}
for n in names:
    if not n:
        continue
    path = n.split("\t")[-1]
    key = "/".join(path.split("/")[:2]) if "/" in path else path
    groups[key] = groups.get(key, 0) + 1
for k, v in sorted(groups.items()):
    print(f"{v:5} {k}")
