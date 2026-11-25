"""Round 9: for every inventory row homed in a given topic, measure which words of the row's
sentence the topic's readings do not carry. A reading aid: each flagged row is then read by hand.

usage: homes.py <threshold> [topic ...]   (no topic: the topics added or edited in rounds 7 to 9)
"""

import json
import pathlib
import re
import sys

WT = pathlib.Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507")
CARDS = WT / "skills/chantier/cards-next"
EV = pathlib.Path(__file__).resolve().parents[2] / "evidence"

TARGETS = """batch-close batch-plan-mode config delivery-time demo forge-permissions
grill-critic-steps grill-series grill-specify lease lost-driver lost-outside lost-silent
main-checkout merge-recorded merge-series-stack merge-stack-ready merge-words orders
project-rules refused-push-chief release-chief-after stack-changes-chief stack-checks stack
status-notes-more steering-reports sync-offer wakes watcher-board watcher-lines
direct-mode direct-mode-switch order-drop order-verbs ready-asks mode-switch drop""".split()

STOP = set(
    """the and for its not are with that this when from you your one has have was were will
    may can all any but out only each then than them they their there here also into onto over
    under per via his her him she who whom which what how does did done been being is it in on
    of to a an or by as at be if no so do we our us""".split()
)


def words(text):
    text = re.sub(r"\]\([^)]*\)", "]", text)
    found = re.findall(r"[a-z0-9][a-z0-9_.-]*[a-z0-9]|[a-z0-9]", text.lower())
    return [w for w in found if len(w) > 2 and w not in STOP]


def stem(word):
    return word[:5]


def main():
    threshold = float(sys.argv[1])
    targets = sys.argv[2:] or TARGETS
    topics = json.loads((CARDS / "topics.json").read_text(encoding="utf-8"))["topics"]
    texts = {}
    for name in targets:
        if name not in topics:
            print(f"?? no topic row {name}")
            continue
        parts = []
        for reading in topics[name]["readings"]:
            files = reading.values() if isinstance(reading, dict) else [reading]
            for f in files:
                parts.append((CARDS / f.split("#")[0]).read_text(encoding="utf-8"))
        texts[name] = {stem(w) for w in words("\n".join(parts))}
    total = flagged = 0
    for inv in sorted(EV.glob("cards-inventory-*.md")):
        for line in inv.read_text(encoding="utf-8").splitlines():
            if not re.match(r"\| *[A-Z]+-[A-Z]?\d+ *\|", line):
                continue
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
            if len(cells) != 8:
                continue
            rid, _, _, behaviour, source, kind, home, _ = cells
            named = [n for n in re.findall(r"topic ([a-z0-9-]+)", home) if n in texts]
            if not named:
                continue
            total += 1
            have = set().union(*(texts[n] for n in named))
            row = words(behaviour)
            if not row:
                continue
            missing = [w for w in row if stem(w) not in have]
            share = 1 - len(missing) / len(row)
            if share < threshold:
                flagged += 1
                print(f"{rid} [{kind}] {','.join(named)} {share:.2f} {source}")
                print(f"   {behaviour[:420]}")
                print(f"   missing: {' '.join(dict.fromkeys(missing))}")
    print(f"rows read {total}, flagged {flagged}")


main()
