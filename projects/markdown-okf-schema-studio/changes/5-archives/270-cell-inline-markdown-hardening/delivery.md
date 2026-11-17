# Report — 270-cell-inline-markdown-hardening

Status: **done** (2026-11-10, branch `change-requests/270-cell-inline-markdown-hardening`, PR #339, merge commit `da6d7b14`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | The table-cell inline Markdown builder drops `//host` links and uses CommonMark-style flanking rules, so `snake_case_name` and `2 * 3 * 4` stay plain text after Tab; the arrow-key test covers all four arrows; TABLE-035 notes, requirements log and CHANGELOG line | `da6d7b14` |

## Proof of completion

- New `test/page/cellInlineMarkdown.test.ts` (5 tests, `@tests_req SwRS-MDOKFSTUDIO-TABLE-035`); the link and emphasis cases failed on the old code.
- `just check` passed locally (3655 unit, 74 security). One coder round, Inspector APPROVE with no blocking finding.
- CI on the merged head `0fb0a303` (after the CHANGELOG rewrap): run 42830176975 passed. Earlier head `89382b08`: run 42829175975 passed.

## Open items

- `[t](javascript:f(1))` still leaves a stray `)` in a cell; out of scope here, a possible follow-up for the owner to decide.
- No screenshot was taken (rendering change limited to emphasis edge cases).
