"""Read-only: (a) each row homed on a card line whose grep phrase sits on that card but not on a
cited line; (b) host-and-shared kind a quotes that no longer start the cited line; (c) every topic
home names a topic of topics.json; (d) listed protecting-looking homes equal the row's home."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "r7"))
from inv import EV, NAMES, cells, rows  # noqa: E402

CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
INDEX = json.loads((CN / "topics.json").read_text(encoding="utf-8"))["topics"]
GREP = re.compile(r"grep(?: -\w+)* '([^']+)' ([\w./-]+\.md)")


def lines_of(name):
    return (CN / name).read_text(encoding="utf-8").split("\n")


for name in NAMES:
    off, quotes, bad_topic, listed = [], [], [], []
    homes = {}
    for i, d in rows(name):
        home = d.get("new home", "")
        homes[d["id"]] = home
        base = home.split("; the rule")[0].split("; no rule")[0].split("; gap")[0]
        for topic in re.findall(r"(?:^|; )topic ([a-z0-9-]+)", base):
            if topic not in INDEX:
                bad_topic.append((d["id"], topic))
        cited = re.findall(r"card ([\w./-]+\.md):([\d, -]+)", base)
        m = GREP.search(d.get("check", ""))
        if not cited or not m:
            continue
        phrase, card = m.groups()
        card = card.removeprefix("cards-next/")
        nums = []
        for ref, spec in cited:
            if ref == card:
                for part in spec.split(","):
                    if "-" in part:
                        lo, hi = part.split("-")
                        nums += range(int(lo), int(hi) + 1)
                    elif part.strip():
                        nums.append(int(part))
        if nums:
            text = lines_of(card)
            if not any(phrase in text[n - 1] for n in nums if n <= len(text)):
                at = [n for n, x in enumerate(text, 1) if phrase in x]
                if at:
                    off.append((d["id"], card, nums, at, phrase))
    section = ""
    for line in (EV / f"cards-inventory-{name}.md").read_text(encoding="utf-8").split("\n"):
        if line.startswith("## "):
            section = line
            continue
        if not line.startswith("|"):
            continue
        c = cells(line)
        if c[0] not in homes:
            continue
        if section.startswith("## Protecting-looking rows a topic") and c[2] != homes[c[0]]:
            listed.append((c[0], c[2], homes[c[0]]))
        if name == "host-and-shared" and section.startswith("## Protecting rows and") and len(c) == 4:
            m = re.match(r"card ([\w./-]+\.md):(\d+)", c[2])
            if m:
                now = lines_of(m.group(1))[int(m.group(2)) - 1].strip().replace("|", chr(92) + "|")
                start = c[3].removesuffix("...").removesuffix("…").strip()
                if not now.startswith(start):
                    quotes.append((c[0], c[2][:40], start[:60], now[:60]))
            if c[2] != homes[c[0]]:
                listed.append((c[0], c[2], homes[c[0]]))
    print(f"{name}: off-line {len(off)}, quotes {len(quotes)}, topics {bad_topic}, listed {len(listed)}")
    for item in off + quotes + listed:
        print("  ", item)
