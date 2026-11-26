"""Verifier: in each inventory, every kind b-f row whose home is a topic and whose behaviour says
never or "only on/after" is named in that inventory's protecting-looking section."""

import re
from pathlib import Path

CR = Path("<CR folder>")
SPLIT = re.compile(r"(?<!\\)\|")
WORDS = re.compile(r"(?i)\bnever\b|\bonly on\b|\bonly after\b|\bmust not\b|the user's word|without the user")
ID = re.compile(r"\b(?:FM-B?\d{3}|[A-Z]{1,3}-\d{3,4})\b")

for f in sorted((CR / "evidence").glob("cards-inventory-*.md")):
    lines = f.read_text(encoding="utf-8").split("\n")
    start = next(i for i, x in enumerate(lines) if x.startswith("## Protecting-looking"))
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    section = "\n".join(lines[start:end])
    named = set(ID.findall(section))
    # ranges such as C-001 to C-005 or C-001-C-005
    for a, b in re.findall(r"\b([A-Z]+-\d{3,4})\s*(?:-|to)\s*([A-Z]+-\d{3,4})\b", section):
        p = a.rsplit("-", 1)[0]
        for n in range(int(a.rsplit("-", 1)[1]), int(b.rsplit("-", 1)[1]) + 1):
            named.add(f"{p}-{n:03d}")
    want, miss = [], []
    for line in lines[:start]:
        c = [x.strip() for x in SPLIT.split(line.strip().strip("|"))]
        if len(c) == 8 and ID.fullmatch(c[0]) and c[5][:1] in "bcdef" and c[6].startswith("topic") and WORDS.search(c[3]):
            want.append(c[0])
            if c[0] not in named:
                miss.append((c[0], c[5], c[6][:60], c[3][:90]))
    print(f.name, "section lines", start + 1, end, "| ids named", len(named), "| topic-home protecting-looking", len(want),
          "| not named", len(miss))
    for m in miss[:12]:
        print("    ", *m)
