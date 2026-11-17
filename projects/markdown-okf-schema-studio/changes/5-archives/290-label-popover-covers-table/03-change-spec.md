---
title: Change spec - the label rename popover leaves the table below it visible and clickable
cr: 290
date: 2026-11-11
issue: none
priority: P3
source: QA campaign 271, QA271-09 (Low)
blast_radius: 1 (placement of one popover; no write path changes)
inspector: Sonnet
stack: 290 (bottom), 289, 293, 292, 291, 288 (top)
---

# Change spec: the label rename popover leaves the table below it visible and clickable

> [!NOTE]
> Source: QA campaign 271, finding QA271-09. Sheet:
> `.agents/changes/4-archives/271-qa-campaign-tables-2026-11-10/01-stray-anchors/c1-1-label-rename-popover-covers-table-cells.md`,
> evidence `../evidence/c1-1-currently.jpg`. Owner's answers: `02-answers.md` (run now, bottom of
> the stack of six, no GitHub issue). Owner's decision: the label rename popover must not cover
> the first table cells nor swallow their clicks. Read code and guidelines on `origin/main`
> (`33fb65ef` at the time of writing). Rules: `.agents/constitution.md`, `AGENTS.md`,
> `requirements/guidelines/project.guidelines.md` ("During a change").

## Problem

In edit mode a click on the anchor icon of `(table-label)=` opens the Rename label popover 6 px
under the icon (`place()` sets `top = icon bottom + 6`). The label of a table has no paragraph or
heading to hold its icon, so the icon sits in a zero-height `.okf-anchor-row` right above the
table, and the popover (`position: fixed`, `width: min(22em, 100vw - 16px)`, 322 px in a 290 px
pane) lands on the header and the first body row. A click on a covered cell hits the popover, so
the outside-press handler does not close it and the cell editor does not open. After a successful
rename the popover stays 5 s, and the cells stay covered for those 5 s.

## Target behaviour

- When the anchor icon sits in an `.okf-anchor-row` (the labelled block starts right below the
  icon: a table, and also a code block, a figure, a directive), the popover opens **above** the
  icon: its bottom edge is 6 px above the icon's top edge, its left edge as today
  (`max(8, icon left)`). It is anchored by its bottom (`bottom` style, not `top`), so the status
  line ("Renaming...", "Renamed. ...", a refusal) makes it grow upwards, away from the block.
- Room: the popover goes above only when it fits between the icon and the top obstruction of the
  pane (the preview toolbar band when it is shown, otherwise 8 px from the viewport top). When it
  does not fit and the page can scroll up by the missing height, the page scrolls up by that
  height first, then the popover opens above. When the page cannot (the label is at the very top
  of the document), the popover opens below as today. That last case is the only one where a
  table cell can still be covered (see Open questions).
- A label held by a paragraph or a heading (icon inline in the text) keeps today's placement,
  under the icon.
- With the popover open, a press on any table cell outside the popover closes it (today's
  outside-press rule, unchanged) and the click goes on to the cell: the cell editor opens in the
  same click. Nothing else changes: Enter, Escape, the 6 s answer timeout, the 5 s close after
  success, the edit-mode gate and the blocked reason of an open editor (BLOCK-041).

## Code anchors (origin/main)

- `src/page/modules/labelRename.ts` (179 lines): `place(anchor)` (lines 52-57) is the only
  placement; `open()` (line 85) calls it after appending the box; the outside `pointerdown`
  handler (lines 150-155) closes on a press outside the popover and the icon.
- `src/core/preview/styles/contentBlockStyles.ts` lines 75-111: `[data-okf-label-rename]`
  (`position: fixed; z-index: 1060; width: min(22em, calc(100vw - 16px))`); lines 113-121:
  `.okf-anchor-row` (zero height, before the labelled block).
- `src/core/render/mystInlineTransforms.ts` lines 60-70: where the renderer puts the icon in an
  `.okf-anchor-row` (no paragraph or heading to hold it).
- `src/page/runtime.ts` line 199: `installLabelRename(document, window, {...})`, the options to
  extend if the module needs the toolbar's bottom edge. Look for the helper the find bar or the
  block editor already uses for the top obstruction before writing a new one.

## Recommended approach

1. In `place(anchor)`: `const row = anchor.closest(".okf-anchor-row")`. Without a row, today's
   code. With a row: measure the popover (`popover.getBoundingClientRect().height` after it is in
   the DOM), compute `room = iconTop - 6 - topInset`; if `room < height` and
   `window.scrollY >= height - room`, `window.scrollBy(0, -(height - room))` and measure the icon
   again; if it now fits, set `bottom = innerHeight - (iconTop - 6)` and clear `top`; otherwise
   keep today's `top`.
2. Add a `topInset(): number` option to `LabelRenameOptions` only if the module cannot read the
   toolbar band itself; wire it in `runtime.ts`.
3. Mark `place` with `@implements_req SwRS-MDOKFSTUDIO-MYST-038`.

`labelRename.ts` stays far under 800 lines. No CSS change is needed (the box is already fixed);
if the coder adds a data attribute for the side (`data-okf-label-rename-side="above"`), it is for
tests only.

## Requirements

No `approved` requirement is touched (no SwRS of the bundle carries `approved_by`), so no owner
agreement is needed.

- **SwRS-MDOKFSTUDIO-MYST-038** (`req_lifecycle: proposed`, `status: stable`; amend). The nominal
  scenario "The click opens the rename field" says "opens under it": keep it for a label before a
  paragraph. Add a scenario (boundary) "A label above a table opens the field above its icon": a
  labelled table, the field opens above the icon, covers no cell of the table, and grows upwards
  with its status line; when the room above is short the page scrolls up first; at the very top of
  the document it opens under the icon (state it as it behaves). Extend "Escape or an outside press
  closes the field" with the row "Pointer press on a table cell while the field is open | the
  field closes, nothing is sent and the cell editor opens in the same click". Replace the
  verification line "the pointer press outside the popover has no named test (untested)" with the
  new tests. Normative text: add "placed so that it does not cover the block its label introduces".
- No new SwRS. `just requirements-update`, generated files committed, a dated entry in
  `requirements/tiers/log.md`.
- Writing skill: no change (no rendered syntax changes).

## Tests first (each fails on origin/main)

1. **Unit**, `test/page/modules/labelRename.test.ts` (170 lines), `@tests_req
   SwRS-MDOKFSTUDIO-MYST-038`:
   - an icon inside an `.okf-anchor-row` with room above: the popover gets a `bottom` equal to
     `innerHeight - (iconTop - 6)` and no `top`;
   - the same icon with too little room and enough `scrollY`: one `scrollBy` up by the missing
     height, then placed above;
   - the same icon at `scrollY = 0` and no room: placed below (today's `top`);
   - an icon held by a paragraph: placed below, as today;
   - a `pointerdown` on an element outside the popover (a fake `td`) closes it (names the untested
     line of MYST-038).
2. **Real input**, promoting the replay: a new `test/integration/realInput/labelRenameAboveTable.ts`
   (scenario `label-rename-above-table`, registered in `test/integration/realInput/run.ts`: import,
   the named map, the sequential list), on the content of `synth/anchors-tables.md`, in a pane
   narrowed as far as the harness allows: edit mode, click the icon of `table-label`; the
   rectangles of `[data-okf-label-rename]` and every `table td` do not intersect; click the cell
   `alpha`: `[data-sphinx-preview-table-cell-editor] textarea` exists; Escape; the buffer is
   unchanged. `@tests_req SwRS-MDOKFSTUDIO-MYST-038`. Runs in the heavy CI run.
3. **Visual**: a new scenario `myst/v46-label-rename-above-table-light-290` (next free `myst`
   number at the time of writing; re-check at rebase) in a new file
   `test/visual/labelRenameScenarios.ts`, on a new fixture `test/visual/fixtures/84-label-above-table.md`
   (next free fixture number; a heading, a paragraph, `(table-label)=`, a three-row table),
   viewport `{ width: 290, height: 800 }`, edit mode on. Its check goes in a new module
   `test/visual/capture_label_rename.py`, imported by `test/visual/capture.py` (592 lines; never by
   `capture_edit_checks.py`, which is at its 1 500 line limit). It clicks the icon and asserts that
   the popover box and every `td` box do not intersect (1 px tolerance) and that the popover is
   fully inside the viewport. `@tests_req SwRS-MDOKFSTUDIO-MYST-038`. Save an `open` step shot.
   Map the id and its description in `test/visual/scenarioIds.ts` and register the scenario list in
   `test/visual/scenarios.ts`.

### Replay promoted

From local commit `87307e8f` (branch `qa/271-table-campaign-replays`, not pushed; read with
`git show 87307e8f:<path>`, never merge or push that branch), add to this PR:

- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c1-1-label-rename-popover-covers-table-cells.json`

Its fixture `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/anchors-tables.md`
(and `anchors-tables.comments.json`) is already on `origin/main`, identical: do not copy it.

## Acceptance checks (the Verifier runs each at the pushed head)

| # | Claim | Command (from the worktree root) |
| --- | --- | --- |
| A1 | The new unit tests pass at the head | `fnm exec -- npm run compile && fnm exec -- node scripts/node-test.mjs unit "out/test/page/modules/labelRename.test.js"` |
| A2 | The placement tests fail on the base | the same command in a detached worktree of the base (`git worktree add --detach <tmp> <base>`), with the new test file copied in: the "above" cases fail |
| A3 | Popover clear of the cells, inside the pane, at 290 px | `fnm exec -- npm run visual:render && uv run --no-sync --group docs python test/visual/capture.py --scenario myst/v46-label-rename-above-table-light-290` passes |
| A4 | A click on a cell under the old popover position opens the cell editor | the heavy CI run at the head (`gh run list --workflow ci.yml --branch <branch> --json databaseId,headSha,conclusion`) is green and its integration log names `label-rename-above-table` |
| A5 | Traceability | `uv run --no-sync --group requirements okfreq validate --check-links --project-root .` passes; `git grep -n "SwRS-MDOKFSTUDIO-MYST-038" -- test/page/modules/labelRename.test.ts test/visual/capture_label_rename.py test/integration/realInput/labelRenameAboveTable.ts` shows a `@tests_req` in each |
| A6 | The replay is in the PR | `git diff --stat <base>...HEAD -- .agents/skills/markdown-studio-exploratory-qa-claude/scenarios/` lists the c1-1 replay |
| A7 | Gates | `just check` and `just preflight` pass |

## Screenshots expected in the PR

- Before (base) and after (head), light theme, 290 px pane, edit mode, the popover open on
  `table-label`: before it covers the header and `alpha`; after it sits above the icon and the
  whole table is visible. Use the `open` step shot of `myst/v46-...` and the same capture on a
  detached worktree of the base. Dark is not needed (the popover already follows the theme
  tokens).

## CHANGELOG line (`## Unreleased`)

- The Rename label field of a table's label now opens above its anchor icon, so it no longer
  hides the first rows of the table, and a click on a cell opens the cell editor right away.

## Files expected to change

- `src/page/modules/labelRename.ts` (and `src/page/runtime.ts` only for a `topInset` option)
- `test/page/modules/labelRename.test.ts`
- `test/integration/realInput/labelRenameAboveTable.ts` (new), `test/integration/realInput/run.ts`
- `test/visual/fixtures/84-label-above-table.md` (new), `test/visual/labelRenameScenarios.ts` (new),
  `test/visual/capture_label_rename.py` (new), `test/visual/capture.py`, `test/visual/scenarios.ts`,
  `test/visual/scenarioIds.ts`, `test/visual/scenarioAssertions.ts` (only for a scenario flag)
- `requirements/tiers/swrs/myst/SwRS-MDOKFSTUDIO-MYST-038.md`, `requirements/tiers/log.md` and the
  generated requirement files
- `CHANGELOG.md`
- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c1-1-label-rename-popover-covers-table-cells.json` (new)

## Shared with the other CRs of the stack

`test/integration/realInput/run.ts` (every CR of the stack adds a scenario), `test/visual/capture.py`,
`test/visual/scenarios.ts`, `test/visual/scenarioIds.ts`, `test/visual/scenarioAssertions.ts`, the
visual fixture numbers (84 here, then 85 in 289, 86 in 291) and the `myst/vNN` number,
`requirements/tiers/log.md` and the generated requirement files, `CHANGELOG.md`. The product code
(`labelRename.ts`) is touched by no other CR of the stack. As the bottom PR, it rebases first;
the CRs above take the next free numbers.

## Blast radius

1. One popover's position. The rename message, the host side and the outside-press rule are
unchanged. Risks: a scroll on open (only when the room is short) moves the page under the reader;
the popover above may cover the end of the previous block, which is the accepted trade.

## Open questions

- At the very top of a document (a `(label)=` on the first line, followed by a table), no scroll
  can make room above the icon, so the popover still opens below and covers the first row until
  Escape or a press elsewhere. **Recommended answer: accept this edge case**, stated as it behaves
  in MYST-038; the alternative (placing the popover beside or below the whole table) moves it far
  from the icon in a narrow pane.
