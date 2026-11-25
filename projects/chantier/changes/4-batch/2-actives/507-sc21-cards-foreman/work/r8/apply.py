"""Round 8: exact one-time replacements in cards-next/ (each old text must occur once)."""
from pathlib import Path

W = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")

EDITS = [
    ("topics/main-checkout.md", "add `; uv.lock changed: sync pending`: you never sync.",
     "add `; uv.lock changed: sync pending`: only the Chief of Staff syncs."),
    ("topics/main-checkout.md", "Stop at the first no, with its `<why>`:", "First no stops, with its `<why>`:"),
    ("topics/main-checkout.md", "Run it right after you handle", "Run it after you handle"),
    ("sync-checkout.md", "Stop or kill nothing and ask no one to: go on unsynced and try again at each next\n   turn but a reload.",
     "Stop or kill nothing and ask no one to: go on unsynced and try again at each next\n   turn but a reload. Judge a sync by this line, never by `$CHANTIER status` (this surface's\n   batch only)."),
    ("topics/demo-p1.md", "no commit, push, PR, or write in a CR's worktree.",
     "no commit, push, PR, or write in a CR's worktree. Implementation goes through a CR and the Foreman."),
    ("topics/batch-plan-mode-p2.md", "A batch keeps its steering until the user's word.",
     "A batch keeps its steering until the user's word. No separate yes for the mode: the go is the yes, and the user may change it before the go by saying so. Under Remote Control a forced `foreman` starts a new Foreman in this session's folder or reuses the last one (host rows), and this session must be fit for one (a main checkout)."),
    ("topics/merge-stack-ready-p2.md", "(red changes nothing by itself).",
     "(red changes nothing by itself). The local-gate record: the last `gate` events of that CR at that full head in `events.jsonl` (`status` keeps `exempt: <rule>` for `--no-gate`)."),
    ("topics/merge-series-stack-p2.md", "for `--outside-stack \"O-<k>: ...\"`.",
     "for `--outside-stack \"O-<k>: ...\"`. In direct mode check your own asks the same way."),
    ("topics/merge-words.md", "no reproach.", "no reproach, no question."),
    ("topics/stack-changes-chief-p1.md", "A held CR: nothing to rebuild.",
     "A held CR: nothing to rebuild. Ask the user nothing more."),
    ("topics/batch-close-p2.md", "A held agent that still runs: wait for its hand-back, never a timer.",
     "A held agent that still runs: wait for its hand-back, never a timer. `status`'s second line names the last closed batch."),
    ("topics/batch-close-p2.md", "- It refuses, naming each cause,",
     "- At a batch's end say it stays open while a CR is held; name each parked or blocked CR with what it waits for and its way back as the CLI's line gives it, offer to wait or to send it out (`order drop <cr> --note trash|ready|P1..P4`), and act on the answer only.\n- It refuses, naming each cause,"),
    ("topics/grill-series.md", "Never `CR250-Q3`.", "Never `CR250-Q3`. An answer's list number there need not match."),
    ("topics/watcher-lines.md", "Another session's watcher does not wake you.",
     "Another session's watcher does not wake you. In Foreman mode the resuming `take` is the Foreman's: the line reaches you at your next `status`."),
    ("topics/refused-push-chief-p2.md",
     "- A failed lease: answer `push failed <branch> <git's text>` and tell the user at once with what it means (the remote moved); never retried.",
     "- A failed lease or a protected-branch rejection: answer `push failed <branch> <git's text>` and tell the user at once, as information, with what it means (the remote moved; the branch is protected); never retried."),
    ("topics/wakes.md", "A batch left blocked is such a stop.", "A batch left blocked is such a stop: send nothing more."),
    ("topics/wakes.md", "never wait inside a call,", "never wait inside a call or run a long command,"),
    ("topics/stack-checks.md", "then `stack-ready-to-merge`. You edit no PR yourself.",
     "then `stack-ready-to-merge`. The new CR shows in the partial-stack line once its PR is mergeable. You edit no PR yourself."),
    ("topics/lost-silent.md", "Never record a hand-back yourself.",
     "Never record a hand-back yourself.\n- When a Driver ends, read its row in `status` before `agents set <cr> -`: `ended, no hand-back recorded` is handled first, with the id still recorded (the flag reads it)."),
    ("topics/lost-driver.md", "- The proof of a death, and a Driver that ended with no hand-back:",
     "- A refused message to an agent you no longer record is not a Driver stopped from outside.\n- The proof of a death, and a Driver that ended with no hand-back:"),
]

NEW = {
    "topics/ready-asks.md": """# A newer readiness ask

A readiness ask (`ready-to-merge`, `pr-in-draft`, `ready-locally` for a CR, `stack-ready-to-merge` for the stack) marks the earlier unread one of the same CR (or of the stack) read, printed `superseded by A-<k>`. Send the line `judge` or `asks` prints first, never an earlier ask again. `question` and `blocked` asks are never superseded.
""",
    "topics/order-verbs.md": """# The orders

Orders are the user's word. Each is one `$CHANTIER order`, applied to the state at once and printed as the line to send the Foreman (by your host's means; a QA order with its `qa-driver prompt` block, as printed), who does what needs its hands and marks it done. `status` lists the open ones, those the CLI applied apart from those nothing has touched.
- `order add --note <prepared-folder or a release's fix file> [--fix-for <release-cr> | --release]`
- `order after <cr> --note "<cr>,<cr>"` (what a queued CR waits for, `-` none; `--add <cr>`, `--remove`; not a release's)
- `order drop <cr> --note trash|ready|P1..P4` (a release or fix CR: trash only; `help order-drop`)
- `order note <cr> --note "<one line: a change, an answer, a priority>"`
- `order merged <cr>`; `order slots --note <n>` (0 holds); `order rounds <cr> --note <n>` (the user's word or the rounds exception); `order budget --note <usd>`; `order mode --note parallel|series|stack`
- `order qa --note "<what to test>"` (a QA driver on the project's head, takes a slot)
- `order waive stack|<cr> --note "<the user's words>"` (`--follow-up <backlog folder>` for a CR; `--note -` withdraws)
- `order approve <release-cr> --note "<the action>"`; `order grant <release-cr> --note "releases=<n> fixes=on|off budget=<usd>"`; `order confirm <release-cr> --note "<the user's word>"` once the other CRs are merged
""",
    "topics/order-drop.md": """# Where a dropped CR goes

- The user's word that takes a CR out of a batch ("drop", "take it out", "postpone", "remove from the batch") names where it goes. When it does not, ask once, in the user's language, before the order: the trash (cancelled), the next batch (`ready`, `3-ready`) or the backlog P1..P4 (postponed or handed off; the usual case for delegated work). A word that already says it needs no question ("cancel it" is the trash; "postpone it, P2" is `P2`).
- Never choose for the user: `order drop` is refused with no `--note`. The inbox is not one of them, for any CR (`--note inbox` is refused); a later move of its folder, the inbox included, is `triage` or the board on the user's word.
- A word that only keeps a CR out of the order for now (a ready CR of a stack, or a live CR in any mode) is `order hold`, not a drop.
- Whatever the destination, the CR keeps its work (worktree, branch, PR); only the trash closes its PR, else it stays a draft; a CR moved to the backlog or `3-ready` keeps its number.
""",
}


def main():
    texts = {}
    for name, old, new in EDITS:
        raw = texts.get(name) or (W / name).read_bytes().decode("utf-8")
        crlf = "\r\n" in raw
        o, n = (old.replace("\n", "\r\n"), new.replace("\n", "\r\n")) if crlf else (old, new)
        assert raw.count(o) == 1, (name, old, raw.count(o))
        texts[name] = raw.replace(o, n)
    for name, text in texts.items():
        (W / name).write_bytes(text.encode("utf-8"))
    for name, text in NEW.items():
        assert not (W / name).exists(), name
        (W / name).write_bytes(text.encode("utf-8"))
    for name in [*texts, *NEW]:
        data = (W / name).read_bytes().replace(b"\r", b"")
        print(len(data), name, "OVER" if len(data) > 1500 else "")


main()
