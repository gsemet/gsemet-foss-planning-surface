import sys
from pathlib import Path
subs = {
    "skills/chantier/references/hosts/copilot.md": [
        ("(no `--stream` here: it ends after each block, started again from its last line)",
         "(no `--stream` here: it ends after each block)"),
        ("its output is read from the background task", "its output read from the task"),
    ],
    "skills/chantier/references/concepts.md": [
        ("(after each block in its plain form, after 2 h with no event and no batch in flight, or when the seat is another session's)",
         "(after each block in its plain form, after 2 h with no event nor batch in flight, or when the seat moves)"),
    ],
}
for name, pairs in subs.items():
    p = Path(name)
    t = p.read_bytes().decode("utf-8")
    for a, b in pairs:
        assert t.count(a) == 1, a
        t = t.replace(a, b)
    p.write_bytes(t.encode("utf-8"))
