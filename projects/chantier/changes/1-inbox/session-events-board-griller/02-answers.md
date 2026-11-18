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

## Several projects on one surface (2026-11-17)

The user: take into account that one planning-surface checkout can hold n projects
(`projects/<name>/`), each with its own Chief of Staff session, and one board serving them all
(its picker). Each event names its project; a Chief of Staff's watch wakes it only for its own
project's events and reads the forge only for its own project's repository; two Chiefs of Staff
on the same surface never record each other's merges. The user asked for the specification to be
written now and checked by the spec critic.

## Spec questions (2026-11-17, after the spec critic)

- events-Q9 (a board of another chantier version): the user chose the recommended answer. The
  watch and `status` read the board's version in `board.json` (CR-323's record) and say once:
  "the board is chantier <v>: its writes do not reach me; restart it". The forge stays read by
  the watch, so merges are still seen.
- events-Q10 (the `Monitor` permission): the user chose the recommended answer. A `Monitor` rule
  for `chantier watch` joins P10's "Every batch" row (added on the user's yes, as P10's rules
  are), marked unproved until a trial. If the host still refuses it (auto mode's classifier),
  the session runs the pull path and says so once.
- events-Q11 (a watch that stopped): the user chose the recommended answer. `status` prints
  `no watch runs for project <name>` whenever no watch of that project is alive (its PID in
  `watch.json`), and the Chief of Staff starts it again. This also covers a `Monitor` that
  expires (the spec-writer's open question 1).
- events-Q12 (Copilot): the user chose the recommended answer. The CR names a trial to find the
  Copilot tool that wakes a session; until it is proved, Copilot runs the pull path
  (`watch --once` at each user message), said once at the session's start.
- Label, group, ungroup and next-batch (the spec-writer's open question 3): settled by events-Q2,
  which lists what wakes; these ride along with the next wake-up.

## Re-scoped by surface-forge-hub (2026-11-18)

- hub-Q8 (the user, answer A, in the grill of surface-forge-hub): surface-forge-hub takes over this
  item's forge and merge part (its `chantier watch`, its forge reads, its replacement of
  `board-seen.jsonl`). This item keeps only the board events (moves, notes, Configuration) and its
  specification is to be written again on top of the hub, with the same journal and the same
  `watch`, once surface-forge-hub is merged. Its current 03-change-spec.md is superseded.
