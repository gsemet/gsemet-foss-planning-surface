# Report — hotkey-editing-mode

Status: **done** for the bug scope (P2 bug run, 2026-10-15, branch `dev/gsemet`).
Block moving and bold/italic styling inside the editor are feature work and were left out.

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T3 | Esc = Cancel, Cmd/Ctrl+Enter validates | `03fda60` |
| T5 | Arrow keys move cell to cell in tables | `273fcc8` |
| T6 | Up/Down follow wrapped visual lines, undo keys, `*`/`_` wrap the selection | `3bbb56b` |
| T7 | Block insertion after a standalone image / figure at document end | `0c4cea4` |
| T8 | Enter on an empty document starts writing | `4abf94a` |

## Proof of completion

- T6: review FIX-REQUIRED (U+200B marker split words), fixed; a real-Chromium check fails with
  the old marker; re-review APPROVE.
- T7: root cause was bare image / `{image}` not mapped to source; review fix applied.
- Final run: 775 unit + 2 contract + 20 security tests pass; visual 119 scenarios green.

## Open item

Keyboard-injection integration suites were not run (screen locked). Re-run `npm run test:e2e`.
