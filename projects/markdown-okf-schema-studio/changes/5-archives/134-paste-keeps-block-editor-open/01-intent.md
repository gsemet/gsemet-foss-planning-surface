# A paste in a block editor re-renders the preview and closes the editor

Type: fix · Priority: P2 · Found 2026-10-27 by CR 123 round 6 (tall block scroll)

After a paste into an open block editor, the preview re-renders, which closes the editor and
restores the last saved scroll position (now the caret, before the top of the page). Expected: the
editor stays open with the caret where the paste ended, and the page does not move.

Also from that review (small, same area): SwRS PALETTE-021 line 78 wording ("the band bottom"),
stale doc comment at `src/page/modules/caretRect.ts:69`, and `test/integration/tallBlockScroll.test.ts:221`
stops checking "never moves up" once the editor closes.
