"""Verifier: inventory rows: the check column, kind-a homes, empty homes."""

import collections
import re
import sys
from pathlib import Path

CR = Path("<CR folder>")
SPLIT = re.compile(r"(?<!\\)\|")
ID = re.compile(r"^[A-Z]{1,3}-[A-Z]?\d{3,4}$")


def rows(f):
    for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        c = [x.strip() for x in SPLIT.split(line.strip().strip("|"))]
        if len(c) == 8 and ID.match(c[0]):
            yield n, c


grand = collections.Counter()
for f in sorted((CR / "evidence").glob("cards-inventory-*.md")):
    cnt, kinds, ids = collections.Counter(), collections.Counter(), collections.Counter()
    empty, bad_a = [], []
    for n, c in rows(f):
        ids[c[0]] += 1
        kinds[c[5]] += 1
        cnt[re.sub(r"\d+", "#", c[7])[:60]] += 1
        if not c[6] or c[6] == "-":
            empty.append((c[0], c[6], c[5]))
        if c[5].startswith("a") and not re.match(r"(card|floor|refusal)", c[6]):
            bad_a.append((c[0], c[6][:90]))
    print("==", f.name, "rows", sum(ids.values()), "dup ids", [i for i, v in ids.items() if v > 1][:5])
    print("  kinds", dict(kinds))
    print("  empty home", len(empty), empty[:6])
    print("  kind-a home not card/floor/refusal", len(bad_a), bad_a[:8])
    if "-v" in sys.argv:
        for k, v in cnt.most_common(10):
            print("    check", v, k)
    grand["rows"] += sum(ids.values())
print(grand)
