# Report — 280-table-comment-mark-after-undo

Status: **done** (2026-11-11, branch `change-requests/280-table-comment-mark-after-undo`, PR #350, merged 99c2a2b4 with 8cd67080; QA 271 P2 stack, no GitHub issue).

## Delivered

A comment mark is put back after an undone row delete (8cd67080); the comment mark scenarios undo by command (99c2a2b4).

## Proof of completion

- Five rounds (round 4 and 5 granted by the owner). Heavy CI fully green at afafb1ec (run 42981123336), stress included, before the PR turned ready.
- Round 5 diagnosis: the two red real-window scenarios were test defects (key-driven Ctrl+Z racing the focus change; the preview panel is created without `preserveFocus`), not a product defect.
- The Chantier repository was not touched.

## Open items

- `createWebviewPanel` in `src/host-vscode/activation.ts` takes focus (no `preserveFocus`); worth a backlog item.
