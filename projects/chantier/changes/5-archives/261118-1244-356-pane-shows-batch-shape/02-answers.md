# Grill answers: pane-shows-batch-shape (short name `shape`)

Grilled with the user on 2026-11-18.

- **shape-Q1, what the pane shows:** A. On the batch's line of the CR board pane, next to "Slots",
  the batch's shape as a word: series, parallel or stack.
- **shape-Q2, the odd "Slots 4/1":** the user's explanation: it was a transition. The user had cut
  the slots from 4 to 1 while 4 Drivers were still running, and the pane showed 4 held of 1 until
  they stopped. Not a bug: the count does not change.

## Settled by the Chief of Staff

- The shape comes from the batch's record, as `status` prints it (`shape parallel`), through the
  `STATUS.json` field the pane already reads or one added beside it; no new source.
- AGENTS.md applies: the PR carries one screenshot of the pane from a real Claude Code session at
  its head, or names its absence in Known gaps, and the Chief of Staff asks the user for it.
