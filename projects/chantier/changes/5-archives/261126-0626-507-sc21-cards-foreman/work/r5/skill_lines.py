"""Align the SKILL texts' launcher-failure line with sync-checkout.md step 4."""

D = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next/skills/"
OLD = "or any other failure of the launcher is a stop: report its text, never another command."
NEW = (
    OLD
    + " One exception: a `--sync` that fails at a batch's start or after a merge is one line with"
    " uv's text, and you go on ([sync-checkout](../chantier/references/sync-checkout.md))."
)

for name in ("chantier", "chief-of-staff", "griller", "status"):
    path = D + name + "-SKILL.md"
    raw = open(path, encoding="utf-8", newline="").read()
    assert raw.count(OLD) == 1, name
    old_size = len(raw.replace("\r\n", "\n").encode("utf-8"))
    out = raw.replace(OLD, NEW)
    open(path, "w", encoding="utf-8", newline="").write(out)
    print(f"{name}-SKILL.md: {old_size} -> {len(out.replace(chr(13) + chr(10), chr(10)).encode('utf-8'))} LF bytes")
