# 156 — An empty document can be started from the keyboard

Type: fix · Priority: P2 · From backlog: `02-backlog/P2/right-on-table-selection-to-enter-edit-cell`
(first half; the second half is CR 157). Intent copied verbatim: [01-intent.md](../01-intent.md),
section "Start edition only from keyboard", images [image.png](../evidence/image.png), [image-1.png](../evidence/image-1.png).

## Intent

New `.md` file, edit mode on: the page shows only the "Start writing" button. Up, Down and Enter do
nothing; the user must click. Expected: the keyboard starts writing, and the button carries a hint
line under it ("Enter to create a new block"), in the same style as the block editor's hint line
("New block · Enter: new line · Tab: indent · Esc: cancel · ⌘↩: done", image-1).

## Autonomous decisions (orchestrator, 2026-10-28; list them in the PR body)

- Split from structural navigation (CR 157) because it is small and independent.
- In edit mode on an empty document, the "Start writing" button is the keyboard selection: Enter
  (and Down) opens the new-block editor; the hint text reads "Enter to create a new block". "typo"
  in the intent is read as "typography" (same style as the editor hint line).
