"""Posted PR body now against the one judged last pass and the local pr-body.md."""

import difflib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
cr = Path(sys.argv[1])
notes = cr / "work" / "verifier"
data = json.loads((notes / "pr487-r16.json.log").read_text(encoding="utf-8-sig"))
posted = data["body"]
old = (notes / "posted-r15.md").read_text(encoding="utf-8")
local_bytes = (cr / "pr-body.md").read_bytes()
local = local_bytes.decode("utf-8")


def norm(text):
    return text.replace("\r\n", "\n").rstrip("\n")


print("headRefOid", data["headRefOid"], "updatedAt", data["updatedAt"])
print("local bytes", len(local_bytes), "bom", local_bytes.startswith(b"\xef\xbb\xbf"), "crlf", b"\r\n" in local_bytes)
print("posted chars", len(posted), "crlf in posted", "\r\n" in posted, "bom", posted.startswith("﻿"))
print("posted == local", norm(posted) == norm(local))
a = norm(old).split("\n")
b = norm(posted).split("\n")
print("lines before", len(a), "now", len(b))
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
    if tag == "equal":
        continue
    print(f"== {tag} before {i1 + 1}-{i2} now {j1 + 1}-{j2}")
    for line in a[i1:i2]:
        print("-", line)
    for line in b[j1:j2]:
        print("+", line)
(notes / "posted-r16.md").write_text(posted.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
