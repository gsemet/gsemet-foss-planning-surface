# Before and after, CR-344

Before: base 1690ec4f (detached worktree, removed). After: cd015442b8cb083809b24a8d3726aa4a1d8763e8.
Reproduce: a scratch copy of docs/demo (make_surface of scripts/docs_screenshots.py, same data for both),
`chantier board` of each tree, Chromium 1440x900 (phone 375x812), clock 2026-06-18T10:30Z, the board's
paths rewritten to /home/demo/... by the script's route. No image shows a username or home path (looked at).

| Pair | Shows |
| --- | --- |
| before/after-triage.png | one post-it picked (check mark after the chip); Backlog one column with P1-P4 lanes headed by chips; sub-lines |
| before/after-kanban.png | priority filters: Inbox, P1, P3 on; P2, P4 off. After: the Inbox column's cards are squeezed, their meta band clipped (see verify.md) |
| before/after-batch.png | Batch graph nodes and PR column cards |
| before/after-config-timing.png | Timing tab host cards |
| before/after-costs.png | mobile-app, batch-02 (closed): receipt, no stamp; the receipt's header meta box (grey) is gone after |
| before/after-home.png | Home |
| before/after-overview-phone.png | Overview phone cards |

Not captured: the Costs receipt with its stamp on a running batch (shop-api batch-03): the captures showed
the machine's home folder in the receipt's error text, so they were deleted. "Copy as image" not captured.
The stack rail hairline is not visible in the demo's Batch view at 1440x900 (no stacked PR under a rail in view).

## Second verification, after at 6f63babc5d5b5f7782b0f22d7174ee3cdc4379c9

Recaptured (same method and data, 1440x900): after-kanban.png (cards keep full height, meta band visible, body scrolls), after-costs.png (receipt header meta band restored, matches before-costs.png). New: after-costs-running.png (shop-api batch-03 running: NOT FINISHED stamp and Copy as image button visible; home paths rewritten in the DOM). Other after-*.png are from cd01544 (untouched by the move). Not proved: Copy as image output, Batch stack rail hairline.
