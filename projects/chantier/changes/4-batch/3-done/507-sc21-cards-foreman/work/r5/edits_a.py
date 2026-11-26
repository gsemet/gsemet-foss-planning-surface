"""Kind-a rules the inventory walk found without a card home: one replace per file, line count kept."""

from pathlib import Path

CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
SYNC = ("(go on unsynced: [sync-checkout]", "(stop or kill no holder; go on unsynced: [sync-checkout]")
EDITS = {f"skills/{n}-SKILL.md": [SYNC] for n in ("chantier", "chief-of-staff", "griller", "status")}
EDITS["cr-driver.md"] = [(
    "before `$CHANTIER handback` is accepted.",
    "before `$CHANTIER handback` is accepted, or start an agent in place of one that may still run.")]
EDITS["stack-driver.md"] = [(
    "yourself, or leave the stack unstacked or a rebuild half done;",
    "yourself, leave the stack unstacked or a rebuild half done, or start an agent in place of one that may still run;")]
EDITS["release-driver.md"] = [(
    "- keep or upload an image that shows the username or the home folder.",
    "- keep or upload an image that shows the username or the home folder, or publish a personal path, email, private repository or session id taken from a source.")]
EDITS["foreman.md"] = [
    ("with the fewest questions to the user that still leave every decision that is theirs to them.",
     "with the fewest questions that still leave the user every decision that is theirs."),
    ("never from what you remember of an earlier one.", "never from memory of an earlier one."),
    ("turning it to draft, as its drop order says.", "turning it to draft, as its drop order says. Stop no sync holder."),
]

for rel, pairs in EDITS.items():
    path = CN / rel
    data = path.read_bytes()
    for old, new in pairs:
        if data.count(new.encode()) == 1:
            continue
        assert data.count(old.encode()) == 1, (rel, old)
        data = data.replace(old.encode(), new.encode())
    path.write_bytes(data)
    size = len(data.replace(b"\r\n", b"\n"))
    print(rel, size)
