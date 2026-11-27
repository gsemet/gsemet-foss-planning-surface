"""Read-only checks of the posted PR #529 description: rendering, names, SHAs, boxes.

Usage (from the worktree): python -I verify_desc_render.py <base sha>
"""
import getpass
import json
import os
import re
import subprocess
import sys

base = sys.argv[1]
raw = subprocess.run(
    ["gh", "api", "repos/gsemet/markdown-okf-schema-studio/pulls/529", "-H",
     "Accept: application/vnd.github.full+json"], check=True, capture_output=True).stdout
pr = json.loads(raw.decode("utf-8"))
html, body = pr["body_html"], pr["body"].replace("\r\n", "\n")
print("title:", pr["title"], "| head", pr["head"]["sha"][:7], "| base", pr["base"]["ref"], pr["base"]["sha"][:7],
      "| state", pr["state"], "| draft", pr["draft"])
for tag in ("h2", "h3", "table", "tr", "pre", "details", "img"):
    print("%s %d" % (tag, len(re.findall(r"<%s[\s>]" % tag, html))))
print("checkboxes", len(re.findall(r'type="checkbox"', html)))
print("literal ** in html", html.count("**"), "| markdown images", len(re.findall(r"!\[[^\]]*\]\(", body)))
names = {getpass.getuser(), os.path.basename(os.path.expanduser("~"))}
hits = sum(len(re.findall(re.escape(n), body, re.I)) for n in names)
print("user name hits", hits, "| home path hits", len(re.findall(r"[A-Za-z]:[\\/]Users|/Users/|/home/", body)))
print("STALE|UNVERIFIED", len(re.findall(r"STALE|UNVERIFIED", body)))
for number, line in enumerate(body.split("\n"), 1):
    if re.search(r"\bCR[- ]?\d+|\b(Driver|Verifier|Inspector|Coder|Foreman|Investigator|Chief of Staff)\b|O-\d{3}|heavy-ci-Q", line, re.I):
        print("role/internal L%d: %s" % (number, line))
print("headings:", [l for l in body.split("\n") if l.startswith("#")])
print("boxes:")
for line in body.split("\n"):
    if re.match(r"- \[[ x]\]", line):
        print("  " + line)
shas = sorted(set(s for s in re.findall(r"`([0-9a-f]{7,40})`", body)))
for sha in shas:
    code = subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], capture_output=True).returncode
    on_base = subprocess.run(["git", "merge-base", "--is-ancestor", sha, base], capture_output=True).returncode
    print("sha", sha, "ancestor of HEAD", code == 0, "| ancestor of base", on_base == 0)
print("run ids:", sorted(set(re.findall(r"\b45\d{9}\b", body))))
