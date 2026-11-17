# Task T1 — Keyboard start on an empty document

Worktree `../markdown-okf-schema-studio-wt-156`, branch `change-requests/156-empty-document-keyboard-start`.
Find the "Start writing" button and the keyboard block-selection code; make Enter/Down on an empty
document in edit mode open the new-block editor (also after the preview first gets focus), and add
the hint line styled like the block editor hint. Tests first (webview unit + visual, real-window if
an existing scenario fits). SwRS new `--lifecycle proposed` (ask main before changing an approved
one). Docs: keyboard page of docs/user. Screenshots before/after light+dark.
Gates: `just check`; normal CI; heavy CI dispatched.
