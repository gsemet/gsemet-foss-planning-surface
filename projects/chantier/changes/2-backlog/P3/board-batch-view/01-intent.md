# Web board Batch view: readable dependency arrows and a mode tooltip

The user (2026-11-15, `intake/request.md`, translated) wants the Batch page's graph of connected
cards to do its job, which is to show which CR waits for which, and wants the page to say how a
batch's mode is changed.

Four of the seven points filed are delivered elsewhere and are not part of this change: the batch
history navigation (board-batch-navigator), and the removed "Merged PR" column, the CRs kept in
one place with a state badge, and the level heads without ": after level 0"
(board-visual-refresh).

Intent, for what is left:

- The arrows of the graph read right when a CR waits for several others (the user's example:
  batch-18's CR-275, which waits for CR-268 to CR-274), and a CR's dependencies can be followed
  on the graph.
- A tooltip on "Stack", "Series" and "Parallel" says how to switch: ask the Chief of Staff to
  "change the batch to stack", with the mode named.

Both board languages (English, French). The board stays read-only on a batch. Destination:
batch-30.
