"""Verifier: the posted description against pr-body.md, and a few structure checks."""

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CR = Path("<CR folder>")
S = Path(__file__).resolve().parent
pr = json.loads((S / "pr.json").read_text(encoding="utf-8-sig"))
local = (CR / "pr-body.md").read_bytes()
posted = pr["body"].replace("\r\n", "\n").rstrip("\n")
mine = local.decode("utf-8").replace("\r\n", "\n").rstrip("\n")
print("state", pr["state"], "draft", pr["isDraft"], "mergeable", pr["mergeable"], "head", pr["headRefOid"])
print("posted equals pr-body.md:", posted == mine, len(posted), len(mine))
print("bom", local.startswith(b"\xef\xbb\xbf"), "crlf", local.count(b"\r\n"), "lines", mine.count("\n") + 1)
print("details open/close", mine.count("<details>"), mine.count("</details>"), "code fences", mine.count("```"))
bad = []
for n, line in enumerate(mine.split("\n"), 1):
    if line.startswith("|") and line.count("`") % 2:
        bad.append(n)
print("table rows with an odd backtick count", bad)
head, _, tail = mine.partition("## Internal references")
print("CR or batch ids before Internal references:",
      [(m[0]) for m in re.finditer(r"\bCR-\d+\b|\bbatch-\d+\b", head)])
print("role words before Internal references:",
      sorted({m[0] for m in re.finditer(r"\b(?:the )?(?:Driver|Verifier|Inspector)\b", head)}))
for m in re.finditer(r"^.*\b(?:Driver|Verifier|Inspector)\b.*$", head, re.M):
    print("   ", m[0][:170])
