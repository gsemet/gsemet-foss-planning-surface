"""Throwaway (acceptance evidence 7): cards-next/topics.json loads and is complete."""

import json
import re
import subprocess
from pathlib import Path

from chantier import roles_data
from chantier.commands.help import load_topics, section

WT = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507")
SKILL = WT / "skills" / "chantier"
CN = SKILL / "cards-next"
SRC = "skills/chantier/scripts/cli/src"

topics = load_topics(CN / "topics.json")
print(f"load_topics: {len(topics)} topics loaded")
forms = []
for name, topic in topics.items():
    for reading in topic.readings:
        for form in reading.values() if isinstance(reading, dict) else [reading]:
            file, _, heading = form.partition("#")
            assert (CN / file).is_file(), (name, form)
            if heading:
                assert section(CN / file, heading), (name, form)
            forms.append(form)
print(f"readings resolved: {len(forms)} ({sum('#' in f for f in forms)} with a #heading, "
      f"{sum(isinstance(r, dict) for t in topics.values() for r in t.readings)} host maps)")

grep = subprocess.run(
    ["git", "-C", str(WT), "grep", "-h", "-o", "help [a-z-]*", "HEAD", "--", SRC],
    capture_output=True, text=True, check=True,
).stdout.split("\n")
names = sorted({line.removeprefix("help ") for line in grep if line.removeprefix("help ")})
# words after "help" that are prose or code, not a topic name (checked by eye in the source)
prose = [n for n in names if n not in topics]
print("CLI `help <word>` matches:", ", ".join(names))
print("  not topic names (prose or code):", ", ".join(prose))
base = json.loads((SKILL / "references" / "topics.json").read_text(encoding="utf-8"))["topics"]
print(f"base names: {len(base)}; missing from cards-next: {sorted(set(base) - set(topics)) or 'none'}")
known = roles_data.names()
bad = {n: [r for r in t.roles if r not in known] for n, t in topics.items()}
bad = {n: r for n, r in bad.items() if r}
print(f"roles.yaml roles: {len(known)}; topic roles outside it: {bad or 'none'}")
rare = [n for n, t in topics.items() if t.review_by]
print(f"review_by: {len(rare)} topics, values {sorted({topics[n].review_by for n in rare})}")

# every `help <name>` a card of cards-next/ names resolves
cited: dict[str, list[str]] = {}
for md in sorted(CN.rglob("*.md")):
    text = md.read_text(encoding="utf-8")
    found = re.findall(r"help ([a-z][a-z0-9-]*)", text)
    for listed in re.findall(r"help <topic>`:(.*)", text):
        found += re.findall(r"`([a-z][a-z0-9-]*)` \(", listed)
    for tail in re.findall(r"help --for [a-z-]+` lists all, among them (.*)", text):
        found += re.findall(r"`([a-z][a-z0-9-]*)`", tail)
    for tail in re.findall(r"(`\$CHANTIER help [a-z-]+`(?:, `[a-z][a-z0-9-]*`)+)", text):
        found += re.findall(r", `([a-z][a-z0-9-]*)`", tail)
    for name in found:
        cited.setdefault(name, []).append(md.relative_to(CN).as_posix())
cited.pop("refine", None)  # topics/seat-p1.md: the sentence "I can help refine the backlog's ideas"
unknown = {n: sorted(set(v)) for n, v in cited.items() if n not in topics}
print(f"topic names cited in cards-next: {len(cited)}; not in topics.json: {unknown or 'none'}")
unread = sorted(
    p.relative_to(CN).as_posix() for p in (CN / "topics").glob("*.md")
    if p.relative_to(CN).as_posix() not in forms
)
print("topic files no topic reads:", unread or "none")
