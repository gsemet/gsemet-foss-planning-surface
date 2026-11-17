# Report: CR 237

Status: **done** (2026-11-03, branch `change-requests/237-frontmatter-collapse`, PR [#282](https://github.com/gsemet/markdown-okf-schema-studio/pull/282), merged by auto-merge as f4960e63 and 75186b3d).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 round 1 | A toggle next to "Frontmatter properties" collapses and expands the table (`aria-expanded`, state kept in page memory across edits and patches; a reload or a newly opened document shows the table again). | f4960e63 |
| T1 round 2 | Owner decision: the toggle shows a down arrow when expanded and a right arrow when collapsed; the Description column keeps its own icon. | 75186b3d |

New requirement SwRS-MDOKFSTUDIO-FMSCHEMA-090 (`proposed`), with a verification note and a dated entry in `requirements/tiers/log.md`.

## Proof of completion

- New assertion in `test/core/frontmatter/propertiesTable.test.ts` checks the exact glyph pair and fails on the round 1 markup.
- `just check`: unit 3518, contracts 73 pass; simulated visual group `frontmatter-schema`: 31 scenarios pass.
- CI run 41628013942 green on the rebased head 3d0dcaea (static, visual, report, checks). Real-window jobs not run (manual).
- Screenshots (expanded dark, collapsed light and dark) on branch `change-requests/237-frontmatter-collapse-assets`.
- Reviews: APPROVE in rounds 1 and 2 (2 of 3 rounds used).

## Open items

- No dedicated test for the issue-badge expand path and the Enter/Space guard (accepted by the owner as non-blocking).
