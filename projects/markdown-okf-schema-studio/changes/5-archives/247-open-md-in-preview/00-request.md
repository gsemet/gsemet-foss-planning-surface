# 247 — A document always opens in preview mode, and E switches to edit mode

Type: fix · Priority: P1 · Approved by the owner on 2026-11-03 · Worktree
`../markdown-okf-schema-studio-wt-247`, branch `change-requests/247-open-md-in-preview`.
Part of the stacked run of 2026-11-03 (afternoon), before release 1.3.0.

## Intent

See [01-intent.md](01-intent.md)

## Owner decisions (2026-11-03)

- Bug: Studio sometimes opens a new document in edit mode. Opening a document (a new one, or another one in the same panel) always starts in preview mode.
- In the preview, the E key alone (no modifier, focus outside any text field) switches to edit mode.
- 2026-11-03 (later): a reload of the same document keeps the current mode (edit stays edit). Only opening another or a new document starts in preview.
