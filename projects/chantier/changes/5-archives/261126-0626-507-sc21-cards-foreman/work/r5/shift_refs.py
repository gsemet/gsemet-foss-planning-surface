"""Shift this CR's three earlier inventories' card line refs after round 5 inserted lines, then check.

Round 5 inserted one line at chief-of-staff.md:27, foreman.md:27 and griller-skill.md:24. Only
cards-next refs move ("card <file>:N", with its ", N" continuations, and the closing lists'
"`<file>:N` \"quote"); the source column (base refs) does not. Safe to run twice: a file whose
quotes already sit on their lines is only checked.
"""

import re
import sys
from pathlib import Path

CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
EV = Path("C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/"
          "2-actives/507-sc21-cards-foreman/evidence")
FROM = {"chief-of-staff.md": 27, "foreman.md": 27, "griller-skill.md": 24}
CARD = re.compile(r"(card (chief-of-staff|foreman|griller-skill)\.md:)"
                  r"(\d+(?:-\d+)?(?:(?:, ?| and )(?:card )?:?\d+(?:-\d+)?)*)")
QUOTE = re.compile(r"`((?:chief-of-staff|foreman|griller-skill|griller)\.md):(\d+)(?:-\d+)?` "
                   r"\"(.*?)\"(?= \||;| `|$)", re.M)


def lines(name):
    return (CN / name).read_text(encoding="utf-8").splitlines()


def holds(name, n, quote):
    body = lines(name)
    if not 0 < n <= len(body):
        return False
    line = " ".join(body[n - 1].replace("`", "").split())
    at = 0
    for part in quote.replace("\\|", "|").split("…"):
        part = " ".join(part.replace("`", "").split())
        at = line.find(part, at)
        if at < 0:
            return False
        at += len(part)
    return True


bad_total = 0
for inv in ("chief-of-staff", "foreman", "griller"):
    path = EV / f"cards-inventory-{inv}.md"
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    stale = [(f, n) for f, n, q in QUOTE.findall(text) if not holds(f, int(n), q)]
    moved = 0
    if stale:
        def shift(name, spec):
            global moved

            def one(m):
                global moved
                v = int(m.group(0))
                if v >= FROM[name]:
                    moved += 1
                    return str(v + 1)
                return m.group(0)

            return re.sub(r"\d+", one, spec)

        text = CARD.sub(lambda m: m.group(1) + shift(m.group(2) + ".md", m.group(3)), text)
        text = re.sub(r"`((?:chief-of-staff|foreman|griller-skill)\.md):(\d+(?:-\d+)?)(?=` \")",
                      lambda m: f"`{m.group(1)}:{shift(m.group(1), m.group(2))}", text)
        path.write_bytes(text.encode("utf-8"))
    quotes = QUOTE.findall(text)
    bad = [(f, n, q[:60]) for f, n, q in quotes if not holds(f, int(n), q)]
    refs = []
    for m in CARD.finditer(text):
        for v in re.findall(r"\d+", m.group(3)):
            n, name = int(v), m.group(2) + ".md"
            body = lines(name)
            if n > len(body) or not body[n - 1].strip() or body[n - 1].startswith("#"):
                refs.append((name, n))
    # grep checks: the phrase must still be in the file named
    greps = [g for g in re.findall(r"grep(?: -\w+)* '([^']+)' ([\w./-]+)", text) if g[0] != "<phrase>"]
    miss = []
    for phrase, name in greps:
        target = CN / name
        if not target.is_file():
            miss.append((name, "no such file"))
        elif phrase.replace("\\|", "|") not in target.read_text(encoding="utf-8"):
            miss.append((name, phrase))
    print(f"{path.name}: stale quotes before {len(stale)}; numbers moved {moved}; "
          f"quotes checked {len(quotes)}, wrong {len(bad)}; card refs to a blank, heading or "
          f"missing line {len(refs)}; grep checks {len(greps)}, not matching {len(miss)}")
    for item in bad[:20] + sorted(set(refs))[:20] + sorted(set(miss))[:30]:
        print("   ", item)
    bad_total += len(bad) + len(refs) + len(miss)
sys.exit(1 if bad_total else 0)
