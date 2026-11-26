import difflib
import getpass
import io
import json
import os
import re

cr = r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/507-sc21-cards-foreman"
raw = open(cr + "/work/verifier/r17-pr.log", "rb").read()
d = json.loads(raw.decode("utf-8-sig"))
body = d.pop("body")
print(d)
posted = body.replace("\r\n", "\n")
out = cr + "/work/verifier/posted-r17.md"
io.open(out, "w", encoding="utf-8", newline="\n").write(posted)
local_raw = open(cr + "/pr-body.md", "rb").read()
local = local_raw.decode("utf-8")
print("local bytes", len(local_raw), "bom", local_raw.startswith(b"\xef\xbb\xbf"), "crlf", b"\r\n" in local_raw)
print("posted chars", len(posted), "crlf in posted", "\r\n" in body, "bom", body.startswith("\ufeff"))
print("posted == local", posted == local.replace("\r\n", "\n"), "stripped equal", posted.strip() == local.strip())
before = io.open(cr + "/work/verifier/posted-r16.md", encoding="utf-8").read()
a = before.split("\n")
b = posted.split("\n")
print("lines before", len(a), "now", len(b))
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag != "equal":
        print("==", tag, "before", i1 + 1, "-", i2, "now", j1 + 1, "-", j2)
        for l in a[i1:i2]:
            print("-", l)
        for l in b[j1:j2]:
            print("+", l)
print("--- structure")
names = {getpass.getuser(), os.path.basename(os.path.expanduser("~"))}
pat = re.compile(r"<details|</details>|<summary|^## |^### |!\[|<img|CR-[0-9]|batch-[0-9]|child [0-9]|round [0-9]|STALE|UNVERIFIED|- \[.\]|Review: |" + "|".join(re.escape(n) for n in names) + r"|C:[\\/]Users|/home/|/Users/", re.I)
for n, l in enumerate(b, 1):
    if pat.search(l):
        hit = [m for m in pat.findall(l)]
        shown = l
        for name in names:
            shown = re.sub(re.escape(name), "<NAME>", shown, flags=re.I)
        print(n, shown)
print("name hits", sum(len(re.findall(re.escape(n), posted, re.I)) for n in names))
