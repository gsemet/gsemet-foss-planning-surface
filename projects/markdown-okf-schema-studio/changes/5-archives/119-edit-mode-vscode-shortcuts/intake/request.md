# 119 — Edit mode follows VS Code undo, redo, select-all and delete-line shortcuts

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/ctrl-z-now-working`

## Intent (user)

when i do a mistake in edition mode, Ctrl+z (mac: Cmd+z) does not work. expected: should cancel the last action. several action needs to be cancellable. redo needs also to be supported.

You need to respect the vscode shortcuts.

Same for Ctrl+a (cmd+a) for selecting a like, ctrl+k/cmd+k to delete the current line

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- In the block editor, undo, redo, select all and delete line are contributed as VS Code keybindings with a `when` clause on the preview edit context, so the user's own rebinding applies; defaults are VS Code's (Cmd/Ctrl+Z, Cmd+Shift+Z / Ctrl+Y, Cmd/Ctrl+A, Cmd/Ctrl+Shift+K for delete line).
- The intent says Cmd/Ctrl+K deletes the line; VS Code's default delete-line is Cmd/Ctrl+Shift+K and Cmd/Ctrl+K is a chord prefix, so we follow VS Code (the stated principle: respect VS Code keybindings).
- Select all selects the content of the block editor only, not the page.
