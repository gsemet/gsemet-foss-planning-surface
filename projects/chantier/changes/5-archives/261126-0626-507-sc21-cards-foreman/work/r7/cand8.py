"""Add the drop order's "no comment, branch kept" to the Foreman card, within 4,000 LF bytes."""
import pathlib
import sys

p = pathlib.Path(sys.argv[1]) / "skills/chantier/cards-next/foreman.md"
t = p.read_bytes().decode("utf-8")
EDITS = [
    ("the Chief of Staff uses this card (`help direct`)", "the Chief of Staff uses it (`help direct`)"),
    ("After a compaction reread your brief", "After compaction reread your brief"),
    ("a refusal or empty variable is a stop.", "a refusal or empty variable: stop."),
    ("a dropped CR's PR per its drop order.", "a dropped CR's PR per its drop order (no comment, branch kept)."),
    ("7. Go on after exit 3: another Foreman owns the batch; stop.", "7. Go on after exit 3: another Foreman owns it; stop."),
    ("(`inbox --epoch <n>`) next wake.", "(`inbox --epoch <n>`) next."),
    ("Name a CR by number and slug.", "Name CRs by number and slug."),
]
for old, new in EDITS:
    assert t.count(old) == 1, old
    t = t.replace(old, new)
n = len(t.replace("\r\n", "\n").encode("utf-8"))
print(n, t.count("\r\n"), t.count("\n"))
assert n <= 4000
p.write_bytes(t.encode("utf-8"))
