"""CR-505 Investigator, read only: the marker blocks CR-504 round 3 dropped (finding D).

usage: python -I dropped.py <CR-504 work/scratch folder> <worktree>
Joins review.json (the 486 weak entries) with dec3.txt (the decisions) and prints a TSV on stdout:
scope, SwRS, fragments before the drop, whether the file still names that SwRS, file, line of the test
title at the head (0 when the title is not found), title. The per-scope counts go to stderr.
"""
import json
import sys
from collections import Counter
from pathlib import Path

scratch, root = Path(sys.argv[1]), Path(sys.argv[2])
entries = {e["n"]: e for e in json.loads((scratch / "review.json").read_text(encoding="utf-8"))}
decisions = {}
for line in (scratch / "dec3.txt").read_text(encoding="utf-8").split("\n"):
    line = line.strip()
    if line and not line.startswith("//"):
        number, value = line.split(None, 1)
        decisions[int(number)] = value.strip()

drops = [entries[n] for n, v in sorted(decisions.items()) if v.upper() == "DROP"]
scopes = Counter()
moved_scopes = Counter()
print("scope\tswrs\tdropped fragments\tfile still names it\tfile\tline\ttitle")
for entry in drops:
    scope = entry["rid"].split("-")[2]
    scopes[scope] += 1
    path = root / entry["file"]
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    title = entry.get("title", "")
    line = next((i for i, row in enumerate(text.split("\n"), 1) if title and title[:50] in row), 0)
    print("\t".join([scope, entry["rid"], ",".join(entry.get("frags", [])), str(entry["rid"] + "#" in text),
                     entry["file"], str(line), title]))

print("decisions", len(decisions), "entries", len(entries), "dropped", len(drops), file=sys.stderr)
print("files", len({e["file"] for e in drops}), "swrs", len({e["rid"] for e in drops}), file=sys.stderr)
print("per scope", dict(sorted(scopes.items())), file=sys.stderr)
benches = Counter("/".join(e["file"].split("/")[:2]) for e in drops)
print("per bench", dict(sorted(benches.items())), file=sys.stderr)
