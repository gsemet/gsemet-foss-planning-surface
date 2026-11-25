"""Add "never record a hand-back yourself" to the Foreman card, within 4,000 LF bytes."""
import pathlib
import sys

p = pathlib.Path(sys.argv[1]) / "skills/chantier/cards-next/foreman.md"
t = p.read_bytes().decode("utf-8")
EDITS = [
    ("the CLI limits, words asks and refuses; you judge.", "the CLI limits, words and refuses; you judge."),
    ("2. Drop or invent a gap. A gap the PR body lacks", "2. Drop or invent a gap or a hand-back. A gap the PR body lacks"),
    ("no Driver, worker or tool of yours runs.", "no Driver, worker or tool runs."),
    ("another Foreman owns it; stop.", "another Foreman has it; stop."),
]
for old, new in EDITS:
    assert t.count(old) == 1, old
    t = t.replace(old, new)
n = len(t.replace("\r\n", "\n").encode("utf-8"))
print(n, t.count("\r\n"), t.count("\n"))
assert n <= 4000
p.write_bytes(t.encode("utf-8"))
