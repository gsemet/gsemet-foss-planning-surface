# Undo of a row delete restores the row but its comment mark stays missing until the preview is reopened

Severity Medium · Reproduced · Verdict Gap · Requirements: none found (REVIEW-001..003 specify the marks, not their refresh after an undo of a structural edit) · Area Tables · Comments · Side preview ·
c1b-3 · Replay `scenarios/271-c1b-3-undo-row-delete-keeps-comment-mark.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![currently](../../evidence/c1b-3-currently.jpg) | none: working case is the same table before the delete (the "beta" cell highlighted, mark `t1`). |
| After Row - on the beta row and Meta+z, the buffer equals the baseline and the row is back, but "beta" has no comment highlight (marks: `t2` only). | The row and its comment mark both come back; the sidecar still holds `t1` (source: the buffer and the sidecar are back to what they were). |

## Why this is wrong

The author deletes a row by mistake and undoes. The text is back but the review comment on it seems lost: nothing in the page shows that a thread exists on that row, and it is not recovered by a webview reload, only by closing and reopening the preview. A reviewer's comment disappearing is the kind of thing that makes people distrust the tool. The sidecar file is unchanged on disk (checked), so the data is intact; the refresh is wrong.

## Steps to reproduce

1. Fixture `synth/anchors-tables.md` (with its `.comments.json`), preview to the side, edit mode on.
2. Click the cell "2" of the beta row, toolbar "Row -", Escape. Marks: `t2` only.
3. Meta+1, Meta+z. Buffer equals the baseline; marks: `t2` only (expected `t1,t2`).
4. Close the preview and reopen it: `t1,t2`.

## Impact

Comment visually lost after undo; can be mistaken for deleted.

## Where it comes from

Not investigated (the thread anchor is probably dropped in memory when its line disappears and not re-matched when the line returns).

## Suggested direction

- (x) Re-anchor threads whose quote reappears after a text change
- ( ) Keep orphaned threads visible in the comments list

Uncheck to disagree: [x]

## Test to add

Real-input E2E: the replay scenario above.

Uncheck to disagree: [x]

## Done when

- [ ] The replay scenario passes.
