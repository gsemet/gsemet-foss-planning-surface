The board's batch view shows, on each working CR, the step it is at and who runs it: "investigator", "coder r3", "inspector", "verifier", "gate scenario", "CI", "rebase", "waits for the user", as the "Phase" and "owner" columns of a status map seen on Twitter (zedBSD's work map, 2026-11-13). Today a node shows only "r3/6".

The user (2026-11-13): "étape oui ça a du sens".

Open points for the grill:
- Where the step comes from: the record has to carry it (a field the Driver sets at each step, in `STATUS.json`), so a small CLI change, not only the board.
- Runs after CR-225 (board-read-views), which draws the batch view.
- Also shows "next to start": the queued CR that starts when a slot frees and its dependencies are met.
