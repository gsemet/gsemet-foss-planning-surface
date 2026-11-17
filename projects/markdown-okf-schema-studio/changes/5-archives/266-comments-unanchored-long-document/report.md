# Report — comments-unanchored-long-document

Status: **done** (2026-11-06, branch `change-requests/266-comments-unanchored-long-document`, PR #328, merge commit `99222b55`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A comment quote that crosses a soft line break gets its inline highlight; length was not the cause (SwRS REVIEW-216) | `99222b55` |

## Proof of completion

- `test/page/modules/commentThreadsLongDocument.test.ts` added, failed on the old code.
- `just check` exit 0 (unit 3618 of 3618); PR CI green; heavy run 42184807228 green on the stack top. Approved in round 1.

## Open items

- Not seen by hand in a real window; no before and after screenshots.
- Quotes that span several inline elements still get a badge, by design of REVIEW-017.
- No changelog line in `## Unreleased`: to add before the next release.
