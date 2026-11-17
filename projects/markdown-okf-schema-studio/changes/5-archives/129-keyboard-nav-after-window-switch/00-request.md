# 129 — Keyboard block navigation survives leaving and coming back to the window

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-keyboard-nav-lost-after-window-switch`

## Intent (user)

See [01-intent.md](01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "lance 4 CR max en parallèle pour fixer tout ça et finaliser une nouvelle stack PR" (same autonomous mode as the previous run). List these in the PR body under "Autonomous decisions".
- Reproduce first (see the item). On focus return in edit mode, the block selection is restored (last selected block, else the block nearest the top); the page itself never takes the block focus ring.
