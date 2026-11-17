# 134 — A paste in a block editor keeps the editor open and the page still

Type: fix · Priority: P2 · From backlog: `02-backlog/P2/paste-rerender-closes-editor`

## Intent (user)

See [01-intent.md](../01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "pars sur les nouveaux P1/P2" (same autonomous mode as the previous runs). List these in the PR body under "Autonomous decisions".
- Follow the item. Also fix the three small points it lists (SwRS PALETTE-021 wording, stale comment in `caretRect.ts`, `tallBlockScroll.test.ts` check after the editor closes).
- Reproduce first in a real window with a tall block, as in CR 123 round 6.
