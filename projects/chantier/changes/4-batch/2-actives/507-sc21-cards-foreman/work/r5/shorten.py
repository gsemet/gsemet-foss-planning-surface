"""Shorten the lines card_lines.py added, to keep the overshoots small. Same rule, fewer bytes."""

D = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next/"
OLD = (
    "- keep CR work in the host's scratchpad or a temp folder (whatever the host says), "
    "or put a secret or personal data in a CR folder;"
)
NEW = (
    "- keep CR work in a scratchpad or temp folder (whatever the host says), "
    "or secrets or personal data in a CR folder;"
)
OLD_PTR = (
    "Rare cases: `$CHANTIER help session-shell` (a shell call that changes folder or waits)."
)
NEW_PTR = "Shell calls that wait or change folder: `$CHANTIER help session-shell`."

BULLETS = (
    "coder conflict-resolver debugger investigator demo-explorer verifier cr-driver "
    "release-driver stack-driver qa-driver"
).split()
EDITS = [(f"{n}.md", OLD, NEW) for n in BULLETS]
EDITS += [(f"{n}.md", OLD_PTR, NEW_PTR) for n in ("spec-critic", "retro-critic")]

for name, old, new in EDITS:
    raw = open(D + name, encoding="utf-8", newline="").read()
    assert raw.count(old) == 1, (name, raw.count(old))
    out = raw.replace(old, new)
    open(D + name, "w", encoding="utf-8", newline="").write(out)
    lines = out.replace("\r\n", "\n").split("\n")
    at = next(i for i, ln in enumerate(lines, 1) if new in ln)
    print(f"{name}:{at} -> {len(out.replace(chr(13) + chr(10), chr(10)).encode('utf-8'))} LF bytes")
