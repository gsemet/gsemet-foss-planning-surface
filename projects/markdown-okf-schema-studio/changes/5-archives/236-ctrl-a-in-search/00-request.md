# 236 — Text shortcuts work in the find and replace fields

Type: fix · Priority: P1 · Approved by the owner on 2026-11-03 · Worktree
`../markdown-okf-schema-studio-wt-236`, branch `change-requests/236-ctrl-a-in-search`.

## Intent

From [01-intent.md](01-intent.md): in the search box, Ctrl+A does not work; check the other
classic shortcuts.

## Owner decisions (2026-11-03)

> [!NOTE]
> Scope: every native editing shortcut of a text field, not only Ctrl+A.

- In the find and replace fields, the native text-field shortcuts act on the field, never on the
  page: Cmd/Ctrl+A (select all), C, X, V, Z, Shift+Z / Y (redo), word left/right, delete a word,
  Home/End, Shift+arrows.
- The bar's own keys keep working (Escape, Enter, Shift+Enter, Cmd/Ctrl+Alt+Enter, Cmd/Ctrl+F,
  Alt+C/W/R, F3).
