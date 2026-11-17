# 297 — Release 1.7.0

## Owner request

2026-11-11: the owner asked whether a release was worth it, then said "oui lance le process de
release". Version agreed: **1.7.0** (minor: five `feat` changes since 1.6.1).

## Scope

Everything on `main` since `v1.6.1` (the stack is already merged; no PR to land first):

| CR | PR | Change |
| --- | --- | --- |
| 290 | #358 | fix(render): label rename popover opens above a table's anchor icon |
| 289 | #359 | feat(render): Find scrolls a sideways-scrolled table to the match |
| 293 | #362 | feat(editor): "Tab: new row" hint, Escape drops an empty Tab row |
| 292 | #363 | feat(editor): fill table cells from a spreadsheet paste |
| 291 | #364 | feat(editor): edit a table inside a quote or an admonition cell by cell |
| 288 | #365 | feat(render): export a page as one self-contained HTML file |
| 286, 287, 294, 295, 296 | #355, #356, #357, #361, #366 | process, docs and CI only (contributors section) |

## Decisions

- Headline candidates: HTML export, and tables (spreadsheet paste, tables in quotes and
  admonitions). The notes follow `release-process.guidelines.md` on `origin/main`.
- The version PR body shows the rendered notes and thread (rule from 286).
- Every other merge is held until 1.7.0 is published.
