# Report — 277-table-preview-stale-after-undo-or-revert

Status: **done** (2026-11-11, branch `change-requests/277-table-preview-stale-after-undo-or-revert`, PR #348, merged ad7b5636 + 74f0bc5f; QA 271 P2 stack, no GitHub issue).

## Delivered

Table preview shows the buffer after an undo or revert under an open cell editor (ad7b5636); the real-input scenario undoes by command (74f0bc5f).

## Proof of completion

- Heavy CI fully green at the pushed head 5dede86a before the PR turned ready; `just check` green locally.
- The Chantier repository was not touched.

## Open items

- None recorded here; see the PR body for autonomous decisions.
