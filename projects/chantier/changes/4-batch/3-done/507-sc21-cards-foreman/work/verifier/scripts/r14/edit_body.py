"""Verifier's description pass: exact-string narrowings in pr-body.md, each found exactly once."""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CR = Path("<CR folder>")
BODY = CR / "pr-body.md"
S = Path(__file__).resolve().parent

EDITS = [
    (
        "one sentence of `griller.md`",
        "one sentence and one clause of `griller.md`",
    ),
    (
        "Host claude, no unit but where a row says otherwise. Every row was measured in one run on the cards of\n"
        "this PR's last commit. A unit's brief also holds the unit's facts from the record, so the six workers'\n"
        "bytes, measured on this change's unit, move between measurements on both sides (today's coder brief:\n"
        "9,575 here, 9,790 and 9,116 in earlier measurements). Start readings before this change, as the specification gives\n"
        "them (declared / measured):",
        "Host claude, no unit but where a row says otherwise. Every row was measured in one run before this PR's\n"
        "last commit; a run at `88d9ab4` gives the same bytes for every row but the six workers', each 396 bytes\n"
        "less on both sides. A unit's brief also holds the unit's facts from the record, so the six workers'\n"
        "bytes, measured on this change's unit, move between measurements on both sides (today's coder brief:\n"
        "9,575 here, 9,790 and 9,116 in earlier measurements). Start readings before this change, as the specification gives\n"
        "them (declared / measured):",
    ),
    (
        "- Inventory homes: of the 4,224 rows of the four inventories, 3,916 name a text home under `cards-next/`.\n",
        "- Inventory homes: of the 4,127 rows of the four inventories, 3,885 name a text home under `cards-next/`.\n",
    ),
    (
        "At least 1,835 of\n",
        "At least 1,824 of\n",
    ),
    (
        "The other rows (at most 2,081) were not read by hand in that pass",
        "The other rows (at most 2,061) were not read by hand in that pass",
    ),
    (
        "Each of the four inventories lists the\n  protecting-looking rows a topic carries, for the later review.",
        "Each of the four inventories has a list of\n  protecting-looking rows for the later review; at least one such row a topic carries is not listed\n  (FM-103).",
    ),
    (
        "card:24, with \"stop\" and \"hold\" only (the third case, the user's words in the Foreman's chat, is dropped by default)",
        "card:24, with \"stop\" and \"hold\" only (the third case, the user's line allowing a refused action, is dropped as the specification sets it: a refused command goes to the Chief of Staff)",
    ),
    (
        "No visual change; nothing loads the new files.",
        "No visual change; no session loads the new files (`just quiz` and `just eval-dry-run` read the quiz cases).",
    ),
    (
        "removes, and converts the tests that read the old Foreman cards: `test_came_back.py`,",
        "removes, and converts the tests the specification names as reading the old Foreman cards: `test_came_back.py`,",
    ),
    (
        "`test_release_tag.py` and `moved_rules.tsv`.\n",
        "`test_release_tag.py` and `moved_rules.tsv`; `test_plugin_files.py`, not named there, reads\n  `foreman-stack.md` too.\n",
    ),
]

raw = BODY.read_bytes()
assert not raw.startswith(b"\xef\xbb\xbf") and b"\r\n" not in raw
text = raw.decode("utf-8")
(S / "pr-body.before.md").write_bytes(raw)
for old, new in EDITS:
    n = text.count(old)
    assert n == 1, (n, old[:60])
    text = text.replace(old, new)
BODY.write_bytes(text.encode("utf-8"))
print("applied", len(EDITS), "edits;", len(raw), "->", len(text.encode("utf-8")), "bytes")
