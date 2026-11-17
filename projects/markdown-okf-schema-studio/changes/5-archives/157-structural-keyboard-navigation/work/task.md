# Task T1 — Structural keyboard navigation

Worktree `../markdown-okf-schema-studio-wt-157`, branch `change-requests/157-structural-keyboard-navigation`.
Extend the keyboard block-selection model with a level: Right = into children (table cells,
admonition/card/tab inner blocks, nested lists if mapped), Left/Escape = to parent; table cell
grid navigation with arrows; Enter on a cell opens the cell editor. Tests first (unit on the
selection model, webview tests, the real-window keyboard scenario if one exists). SwRS new
`--lifecycle proposed`; ask main before changing an approved keyboard requirement. Docs: keyboard
page. Screenshots before/after light+dark (selected cell highlight).
Gates: `just check`; normal CI; heavy CI dispatched.
