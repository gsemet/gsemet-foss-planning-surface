# 034 — floating-edit-bar

From backlog `P3/bug-move-md-edit-floating-bar` (files copied here as `backlog-*` / images).

## Problem

In edit mode the floating format bar (MyST/GFM dropdown, H, B, I, S, link, code, quote, hr, table, emoji, flag) overlaps the first line of the edited block.

## Decisions (user grill, 2026-10-22 night plan)

1. Decision: the bar sits just ABOVE the edited block, never covering its text. When the block's top scrolls out of view, the bar sticks to the top of the viewport (below the preview toolbar) as long as the block is visible; it never leaves the viewport.
2. Keep keyboard focus and caret in the block when the bar moves; no layout shift of the block text (text never moves).
3. Works for block, table-cell and frontmatter editors that show the bar; narrow pane (360/460 px) keeps the bar inside the pane (wraps or scrolls horizontally inside itself).

Night rules: blocked on a real product decision → apply the driver's recommendation and list it in the PR under "Décisions prises en autonomie" (Autonomous decisions).
