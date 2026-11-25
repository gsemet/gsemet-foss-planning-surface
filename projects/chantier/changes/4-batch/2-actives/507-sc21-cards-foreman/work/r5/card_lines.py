"""Add the kind-a CR-folder rule (F5, from concepts.md) and the shell topic pointers to the cards.

Each replacement must match exactly once. Prints the sizes before and after.
"""

D = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next/"

BULLET = (
    "- keep CR work in the host's scratchpad or a temp folder (whatever the host says), "
    "or put a secret or personal data in a CR folder;\n"
)


def before(anchor):
    return (anchor, BULLET + anchor)


EDITS = {
    "coder.md": [before("- point a test or probe of the board's write paths")],
    "conflict-resolver.md": [before("- write by another way a path the guard refused")],
    "debugger.md": [before("- point a test or probe of the board's write paths")],
    "investigator.md": [before("- claim a check you did not run.")],
    "demo-explorer.md": [before("- claim a check you did not run.")],
    "verifier.md": [before("- keep an image that shows the username")],
    "cr-driver.md": [
        before("- upload or keep an image that shows the username"),
        (
            "`cr-workers` (starting a worker, its prompt, its reply)",
            "`cr-workers` (starting a worker, its prompt, its reply); `cr-review-step` (a review "
            "step's prompt); `session-shell` (a shell call that waits, backgrounds or changes "
            "folder; forge text)",
        ),
    ],
    "release-driver.md": [
        before("- keep or upload an image that shows the username"),
        (
            "`release-notes` (the notes",
            "`session-shell` (a shell call that waits, backgrounds or changes folder; forge text); "
            "`release-notes` (the notes",
        ),
    ],
    "stack-driver.md": [
        before("- upload or keep an image that shows the username"),
        (
            "`stack-restack` (the restack pass",
            "`session-shell` (a shell call that waits, backgrounds or changes folder; forge text); "
            "`stack-restack` (the restack pass",
        ),
    ],
    "qa-driver.md": [
        before("- keep a screenshot that shows the username"),
        (
            "`qa-results` (the result file",
            "`session-shell` (a shell call that waits, backgrounds or changes folder); "
            "`qa-results` (the result file",
        ),
    ],
    "spec-writer.md": [
        (
            "Never: commit, push or open a PR; decide what the answers leave open.",
            "Never: commit, push or open a PR; decide what the answers leave open; keep a draft "
            "in a scratchpad or temp folder, or put a secret or personal data in the CR's folder.",
        ),
        (
            "Rare cases: `$CHANTIER help spec-writer-extras`",
            "Rare cases: `$CHANTIER help session-shell` (a shell call that changes folder or "
            "waits); `$CHANTIER help spec-writer-extras`",
        ),
    ],
    "spec-critic.md": [
        (
            "No summary, no praise.",
            "No summary, no praise.\n\nRare cases: `$CHANTIER help session-shell` (a shell call "
            "that changes folder or waits).",
        )
    ],
    "retro-critic.md": [
        (
            "nothing worth changing`. Nothing else.",
            "nothing worth changing`. Nothing else.\n\nRare cases: `$CHANTIER help session-shell` "
            "(a shell call that changes folder or waits).",
        )
    ],
    "foreman.md": [
        (
            "7. Go on after exit 3: another Foreman owns the batch. Stop at once.\n",
            "7. Go on after exit 3: another Foreman owns the batch. Stop at once.\n"
            "8. Keep CR work in a scratchpad or temp folder, or put a secret or personal data in "
            "a CR folder.\n",
        ),
        ("`wakes`, `refused-push`,", "`wakes`, `session-shell`, `refused-push`,"),
    ],
    "chief-of-staff.md": [
        (
            "- Set a priority, label or group but on the user's word.\n",
            "- Set a priority, label or group but on the user's word.\n"
            "- Keep CR work in the host's scratchpad or a temp folder (whatever the host says), "
            "or put a secret or personal data in a CR folder.\n",
        ),
        ("`help session-start`, `first-turn`,", "`help session-start`, `session-shell`, `first-turn`,"),
    ],
    "griller-skill.md": [
        (
            "- Start the board or the watcher; only the Chief of Staff does.\n",
            "- Start the board or the watcher; only the Chief of Staff does.\n"
            "- Keep CR work in the host's scratchpad or a temp folder (whatever the host says), "
            "or put a secret or personal data in a CR folder.\n",
        ),
        (
            "A refusal you do not understand: `$CHANTIER access` before you ask.",
            "A refusal you do not understand: `$CHANTIER access` before you ask. A shell call "
            "that waits or changes folder: `$CHANTIER help session-shell`.",
        ),
    ],
    "griller.md": [
        (
            "You write only in that CR's folder.",
            "You write only in that CR's folder, never a secret or personal data.",
        )
    ],
}

for name, edits in EDITS.items():
    path = D + name
    raw = open(path, encoding="utf-8", newline="").read()
    crlf = "\r\n" in raw
    text = raw.replace("\r\n", "\n")
    old_size = len(text.encode("utf-8"))
    for old, new in edits:
        assert text.count(old) == 1, (name, old, text.count(old))
        text = text.replace(old, new)
    out = text.replace("\n", "\r\n") if crlf else text
    open(path, "w", encoding="utf-8", newline="").write(out)
    print(f"{name}: {old_size} -> {len(text.encode('utf-8'))} LF bytes")
