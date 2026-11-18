# Intent

The user, 2026-11-17: start a Griller from the web board, to discuss a CR directly. Split from
`session-events-board-griller` (events-Q8), which this CR waits for: the board's events and the
Chief of Staff's watch carry its messages. To be grilled later; the user gave the direction.

## Direction (the user, 2026-11-17, after round 2)

- The Griller is an agent started headless, most likely by a CLI: `claude -p` or `copilot -p`.
  That session may send messages to the Chief of Staff.
- A second mode to support: a Griller session in a worktree, remote; so the hand-over to the
  Chief of Staff must also be able to carry files (the `files for <slug>: <paths>` line is not
  enough when the files are on another machine).
- This direction replaces griller-Q4's answer (a desktop session started by the Chief of Staff);
  the grill settles it.

## Recorded earlier (from the first item's grill)

- griller-Q4 (round 1): a "Grill" button on a card writes an event (`grill CR-<n>`); the Chief of
  Staff, woken by it, starts a desktop Griller session on that CR. Superseded by the direction
  above, to be grilled again.
- griller-Q7 (round 2): a Griller may ask the Chief of Staff a question (whether a CR is in the
  batch, what a PR holds) and, on the user's word, ask to add a CR to the running batch; the
  Chief of Staff decides, acts and answers. `<slug> specified` and `files for <slug>: <paths>`
  stay.
