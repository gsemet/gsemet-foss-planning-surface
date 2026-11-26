"""Read-only: the topics that rows of one source file are homed on, against the split list."""

import re
import sys
from pathlib import Path

EV = Path(__file__).resolve().parents[2] / "evidence"
SOURCE = "chief-of-staff-merge.md"

got: dict[str, list[str]] = {}
for path in EV.glob("cards-inventory-*.md"):
    for line in path.read_text(encoding="utf-8").split("\n"):
        c = [x.strip() for x in re.split(r"(?<!\\)\|", line)]
        if len(c) >= 10 and c[5].startswith(SOURCE):
            for topic in re.findall(r"(?:^|; )topic ([a-z0-9-]+)", c[7]):
                got.setdefault(topic, []).append(c[1])
for topic in sorted(got):
    print(topic, len(got[topic]), got[topic][:5])
text = (EV / "cards-inventory-host-and-shared.md").read_text(encoding="utf-8")
row = next(t for t in text.split("\n") if t.startswith(f"| references/{SOURCE} "))
listed = row.split("split into topics ", 1)[1].rstrip(" |").split(", ")
print("listed, no row homed there:", sorted(set(listed) - set(got)))
print("homed, not listed:", sorted(set(got) - set(listed)))
sys.exit(0)
