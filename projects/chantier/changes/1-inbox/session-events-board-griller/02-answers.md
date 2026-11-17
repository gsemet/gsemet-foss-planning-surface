# Answers

## Round 1 (2026-11-17)

### events-Q1: how the CLI wakes the Chief of Staff on Claude Code

The user chose the recommended answer: a monitor. The Chief of Staff runs `chantier watch` with
the `Monitor` tool; each event is one line, and each line wakes the session, which says it or
acts on it. The board writes its events to a file the watch reads (`board-events.jsonl`); the
watch also reads the forge (about every 60 s) and prints a merge it sees.

### events-Q2: which events wake the Chief of Staff

The user chose the recommended answer: decisions and merges, grouped over about 30 s into one
wake-up: a priority or stage changed (Triage, Kanban), an item added to the inbox, a comment or a
note on a CR, a PR merge seen on the forge, a Configuration change (agent or model). No wake-up
for opening a page or for text being edited.

### events-Q3: Copilot, and hosts where nothing can wake the session

The user: Copilot should now have the same behaviour (to check which tool it offers for it), but
a fallback is needed. So: on a host with no way to wake the session, the events wait in the file,
and the Chief of Staff reads and summarises them at the user's next message or at the next
`status`, and says at the session's start that this host does not wake it. This fallback is
today's pull path (`status`), not a look-alike tool.

### griller-Q4: where the board's Griller talks

The user chose the recommended answer: a desktop session. A "Grill" button on a card writes an
event (`grill CR-<n>`); the Chief of Staff, woken by it, starts a Griller session on that CR. The
Griller reads the same files and talks with the Chief of Staff by `SendMessage`, as today; the
user grills in the app, or under Remote Control.

## Round 2 (2026-11-17)

### events-Q5: what the Chief of Staff does alone when woken

The user chose the recommended answer: merges only. A merge the watch saw on the forge is
checked there, recorded (`order merged`) and sent to the Foreman, without waiting for the user's
"merged". Every other event: one line to the user, no action.

### events-Q6: when the watch runs

The user chose the recommended answer: the whole session. The Chief of Staff starts it at the
session's start, with or without a batch, and starts it again at its next turn if it stopped or
expired; it ends with the session. The forge is read only while a PR of the batch is open.

This widens AGENTS.md's forge rule: today only the board's PRs page reads the forge; the watch
reads it too (read-only, the user's own `gh` or `glab`, about every 60 s, only while a PR of the
batch is open).

### griller-Q7: what a Griller may say to the Chief of Staff

The user chose the recommended answer, for `board-griller`: questions and requests. A Griller may
ask the Chief of Staff a question (whether a CR is in the batch, what a PR holds) and, on the
user's word, ask to add a CR to the running batch; the Chief of Staff decides, acts and answers.
`<slug> specified` and `files for <slug>: <paths>` stay.

### events-Q8: one CR or two

The user chose the recommended answer: two. This CR is the events (the watch, the events file,
the wake-up, the forge, the fallback). The Griller started from the board is its own CR,
`board-griller`, which waits for this one; griller-Q4 and griller-Q7 are recorded there.

## Grilled enough (2026-11-17)

After the restatement, the user: grilled enough. The specification is written after batch-23.
Left for the spec-writer to check: whether a `Monitor` expires and must be started again, and
which tool wakes a Copilot session.
