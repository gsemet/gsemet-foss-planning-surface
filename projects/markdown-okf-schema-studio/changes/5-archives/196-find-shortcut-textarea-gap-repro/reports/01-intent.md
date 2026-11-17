# Backlog (P3, unverified): Cmd/Ctrl+F from a block editor textarea opens Find after a host round trip

Found by CR 188 (2026-10-29, PR #201) while reading the code; not reproduced.

- When the focus is already in a block editor textarea, Cmd/Ctrl+F goes through VS Code and the
  extension host before the find bar opens (`package.json` keybinding ~193-196,
  `previewManager.ts:250`, `findBar.ts:559-562`).
- Keys typed in that gap could land in the textarea; when the find field then takes the focus, the
  editor commits on blur (BLOCK-047), so stray characters could reach the Markdown.
- Also check consistency with the SwRS TOOLBAR-009 table row that says the bar does not open from a
  block editor field.
- Next step: a real-window or held-reply reproduction (CR 188's `holdEditSourcesForTests()` hook
  pattern); fix only once reproduced.
