"""Verifier: home rules over every inventory row (spec acceptance: no empty home, every kind-a row
held by a card, the floor or a refusal, no inferable row of kind a), and every `card <file>:<line>`
home citation resolves to a non-blank, non-heading line of cards-next/."""

import collections
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
CR = Path("<CR folder>")
sys.path.insert(0, str(CR / "work/r10"))
import inv  # noqa: E402

N = Path("<worktree>/skills/chantier/cards-next")
TOPICS = json.loads((N / "topics.json").read_text(encoding="utf-8"))["topics"]
total = collections.Counter()
kinds = collections.Counter()
empty, bad_a, inf_a, bad_cite, bad_topic = [], [], [], [], []
ids = collections.Counter()
cites = 0
for name, n, r in inv.rows():
    total[name] += 1
    ids[r["id"]] += 1
    home, kind = r["new home"], r["kind"][:1]
    kinds[kind] += 1
    if not home or home == "-":
        empty.append(r["id"])
    if kind == "a" and not re.match(r"(card|floor|refusal)\b", home):
        bad_a.append((r["id"], home[:80]))
    if kind == "a" and "inferable" in (home + r.get("check", "")).lower():
        inf_a.append((r["id"], home[:80], r.get("check", "")[:60]))
    for m in re.finditer(r"\bcard `?([A-Za-z0-9_./-]+\.md):(\d+)", home):
        cites += 1
        p = N / m[1]
        if not p.is_file():
            bad_cite.append((r["id"], m[0], "no file"))
            continue
        ls = p.read_text(encoding="utf-8").split("\n")[:-1]
        k = int(m[2])
        if k < 1 or k > len(ls) or not ls[k - 1].strip() or ls[k - 1].startswith("#"):
            bad_cite.append((r["id"], m[0], "blank, heading or beyond end"))
    for m in re.finditer(r"\btopic `?([a-z0-9]+(?:-[a-z0-9]+)*)`?", home):
        t = m[1]
        if t not in TOPICS and not (N / "topics" / f"{t}.md").is_file():
            bad_topic.append((r["id"], t))
print("rows per file", dict(total), "all", sum(total.values()))
print("kinds", dict(sorted(kinds.items())))
print("duplicate ids", [i for i, v in ids.items() if v > 1][:5])
print("empty home", len(empty), empty[:5])
print("kind-a home not card/floor/refusal", len(bad_a), bad_a[:8])
print("kind-a marked inferable", len(inf_a), inf_a[:8])
print("card:line citations", cites, "bad", len(bad_cite), bad_cite[:10])
print("unknown topic names", len(bad_topic), bad_topic[:10])
