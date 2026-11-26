"""Write work/r9-body.json: the old and new pr-body.md texts round 9 makes necessary. It reads
pr-body.md and the host-and-shared inventory, and writes nothing else.

Run: python -I make_body.py
"""

import json
import re
from pathlib import Path

R9 = Path(__file__).parent
CR = R9.parents[1]
body = (CR / "pr-body.md").read_text(encoding="utf-8")
inventory = (CR / "evidence/cards-inventory-host-and-shared.md").read_text(encoding="utf-8")


def line_of(start: str) -> str:
    found = [line for line in body.split("\n") if line.startswith(start)]
    assert len(found) == 1, (start, len(found))
    return found[0]


def join(numbers: list[str]) -> str:
    if len(numbers) == 1:
        return numbers[0]
    return ", ".join(numbers[:-1]) + " and " + numbers[-1]


section = inventory.split("## Sibling-card edits", 1)[1].split("## Behaviour changes on purpose", 1)[0]
put_back = []
for row in section.split("\n"):
    found = re.match(r"\| topics/([\w.-]+)\.md:([\d, ]+) \|.*\| (review|review; trim) \|$", row)
    if found:
        put_back.append(f"{found[1]} {join(found[2].split(', '))}")

old_row = line_of("| topics, rules put back:")
new_row = ("| topics, rules put back: " + ", ".join(put_back)
           + " | a lost or misstated rule or its wording, line by line in the host and shared inventory |")

old_index = line_of("| topics.json |")
assert old_index.endswith("names `order mode` |"), old_index
new_index = (old_index[: -len(" |")]
             + "; the split topics list their parts; `ready-asks` serves the Foreman and the Chief of Staff |")

pairs = [
    {"old": old_row, "new": new_row},
    {"old": old_index, "new": new_index},
    {"old": "topic index: 238 topics load, 432 readings resolve",
     "new": "topic index: 238 topics load, 447 readings resolve"},
]
for pair in pairs:
    assert body.count(pair["old"]) == 1, pair["old"]
(CR / "work/r9-body.json").write_text(json.dumps(pairs, indent=1, ensure_ascii=False) + "\n",
                                      encoding="utf-8", newline="\n")
print(len(put_back), "topic rows put back")
for pair in pairs:
    print("OLD", pair["old"])
    print("NEW", pair["new"])
