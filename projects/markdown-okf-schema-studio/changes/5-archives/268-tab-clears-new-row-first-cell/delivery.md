# Report — 268-tab-clears-new-row-first-cell

Status: **done** (2026-11-10, branch `change-requests/268-tab-clears-new-row-first-cell`, PR #337, merge commit `ede6863e`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A table cell left with Tab, Shift+Tab or an arrow key shows the text just typed as inline Markdown (new `src/page/modules/cellInlineMarkdown.ts`); SwRS TABLE-035 scenario, requirements log, CHANGELOG line | `ede6863e` |

## Proof of completion

- Three new unit tests failed on the old code and pass now; one real-input assertion added to the table Tab scenario; one existing assertion that encoded the bug was changed, intent kept.
- `just check` passed locally (3643 unit, 74 security). PR run 42813817998 green; heavy run 42813816920: checks, static, visual and real-window integration passed.
- Screenshots (light and dark, before and after) are on branch `change-requests/268-tab-clears-new-row-first-cell-assets`.

## Open items

- Inspector notes, not blocking: no direct unit test for href safety and escapes in `cellInlineMarkdown.ts`; the link allow-list admits protocol-relative `//host` links; `_` and `*` open emphasis inside words until the next render; only ArrowRight is unit-tested.
