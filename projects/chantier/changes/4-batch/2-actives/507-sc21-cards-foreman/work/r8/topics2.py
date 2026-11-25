"""Round 8: put back the small rules the row-by-row check found missing from topics (run once)."""

from pathlib import Path

TOPICS = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next/topics")

EDITS: dict[str, list[tuple[str, str]]] = {
    "lost-outside.md": [
        ("to a message. Read it at once, no ping, and never try", "to a message to a recorded agent. Read it at once, no ping, never try"),
        ("A mode switch's restart path clears it itself.", "A mode switch's restart path clears it."),
        ("who stopped the agent, and a compaction", "who stopped the agent; a compaction"),
    ],
    "delivery-time-p2.md": [
        (
            "- A CI run's time comes from the forge, read-only (`gh run list --json`, `glab ci list`); no CI on PRs counts 0, said so. Unreadable: `CI time unknown, not counted`.",
            "- A CI run's time: the latest passed runs on its PRs or default branch, read on the forge, read-only (`gh run list --json`, each run's start and update times; `glab ci list`); no CI on PRs counts 0, said so. Unreadable (no `gh` or `glab`, no rights, no passed run yet): `CI time unknown, not counted`.",
        ),
    ],
    "forge-permissions.md": [("Everything only warns.", "Everything only warns; a CLI not logged in still fails P9.")],
    "project-rules.md": [
        (
            "tell the user only what P5, P9 and P10 say.",
            "tell the user only what P5, P9 and P10 say. A missing tool is said with what to install.",
        ),
    ],
    "steering-reports-p1.md": [
        (
            'direct mode applies the Foreman\'s "Deliver by a time" yourself.',
            'direct mode applies the Foreman\'s "Deliver by a time" yourself. Tell the user no more than the report says.',
        ),
    ],
    "grill-critic-steps.md": [
        (
            "before the user sees anything; a fix it refuses",
            "before the user sees anything, then review again against `02-answers.md`; a fix it refuses",
        ),
    ],
    "release-chief-after-p2.md": [
        (
            '"auto" never covers these comments.',
            '"auto" never covers these comments.\n- Once published, the user is asked nothing more for this release but what this list asks.',
        ),
    ],
    "watcher-board.md": [
        (
            "- An `order add` refused: say its text.",
            '- "Rescan", "I updated the priorities": read the backlog again (`status`, the dashboard, `next-batch.json`) and say what moved and whether the next batch is declared ready; with a watcher or the pull path running, only when the user asks.\n- An `order add` refused: say its text.',
        ),
    ],
    "config-p1.md": [
        (
            "`batch.slots` (4 by default, 0 or more).",
            "`batch.slots` (4 by default, 0 or more), `ci.beside_gate` (more CI minutes), `hosts.<host>.timing` (wakes, cache TTL, CI re-runs).",
        ),
    ],
    "lease.md": [("Times in its texts are UTC.", "Times in its texts are UTC. It is local to the batch's machine.")],
    "merge-recorded.md": [
        (
            "- GitLab: a fold",
            "- Parallel batch: the first CR ready to merge wins; the user merges in the order they become ready unless told otherwise.\n- GitLab: a fold",
        ),
    ],
    "status-notes-more.md": [
        (
            'after a no, the holders only, "a later yes still counts").',
            'after a no, the holders only, "a later yes still counts"); other holders: what the user may stop.',
        ),
    ],
}

for name, pairs in EDITS.items():
    path = TOPICS / name
    text = path.read_bytes().decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    for old, new in pairs:
        new = new.replace("\n", newline)
        if text.count(old) != 1:
            print("MISS", name, old[:60])
            continue
        text = text.replace(old, new)
    path.write_bytes(text.encode("utf-8"))
    print(name, len(text.encode("utf-8").replace(b"\r", b"")))
