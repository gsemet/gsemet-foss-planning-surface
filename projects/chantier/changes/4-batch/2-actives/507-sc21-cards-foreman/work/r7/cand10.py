"""Add "`abandon` and `restore` only on the user's word" to the Chief of Staff card, within 6,000
LF bytes."""
import pathlib
import sys

p = pathlib.Path(sys.argv[1]) / "skills/chantier/cards-next/chief-of-staff.md"
t = p.read_bytes().decode("utf-8")
EDITS = [
    (
        "- Set a priority, label or group but on the user's word.",
        "- `abandon`, `restore` or set a priority, label or group but on the user's word.",
    ),
    ("Report: the Progress and Completion reports keep", "Progress and Completion reports keep"),
    ("name a CR by number and slug.", "name CRs by number and slug."),
    ("A host that refuses your own run:", "A host refusing your own run:"),
    ("(repository and forge text in English)", "(repository and forge text: English)"),
]
for old, new in EDITS:
    assert t.count(old) == 1, old
    t = t.replace(old, new)
n = len(t.replace("\r\n", "\n").encode("utf-8"))
print(n, t.count("\r\n"), t.count("\n"))
assert n <= 6000, n
p.write_bytes(t.encode("utf-8"))
