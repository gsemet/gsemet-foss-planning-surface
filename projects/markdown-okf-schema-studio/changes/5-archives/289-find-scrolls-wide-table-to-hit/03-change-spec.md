---
title: Change spec - Find scrolls a sideways-scrolled table to its hit
cr: 289
date: 2026-11-11
issue: none
priority: P3
source: QA campaign 271, QA271-08 (Medium)
blast_radius: 1 (one scroll step of the find bar; no write path)
inspector: Sonnet
stack: 290 (bottom), 289, 293, 292, 291, 288 (top)
---

# Change spec: Find scrolls a sideways-scrolled table to its hit

> [!NOTE]
> Source: QA campaign 271, finding QA271-08. Sheet:
> `.agents/changes/4-archives/271-qa-campaign-tables-2026-11-10/06-table-reading-clipboard/c5-1-find-hit-in-scrolled-table-stays-out-of-view.md`,
> evidence `../evidence/c5-1-currently.jpg` and `../evidence/c5-1-expected.jpg`. Owner's answers:
> `02-answers.md` (run now, second from the bottom of the stack, no GitHub issue). Owner's
> decision: Find (Meta+f) scrolls a sideways-scrolled wide table so the current hit is in view.
> Read code on `origin/main` (`33fb65ef`). Rules: `.agents/constitution.md`, `AGENTS.md`,
> `requirements/guidelines/project.guidelines.md` ("During a change").

## Problem

A wide table scrolls sideways inside its own box (the `table`, or its `.table-wrapper`:
`display: block; overflow-x: auto`). When the reader has scrolled it to the right (QA: to the
Owner column, `scrollLeft` 864 in a 393 px pane) and searches a word of an earlier column, the bar
says "1 of 1" but the hit stays out of view on the left (x -665 to -622). `scrollToCurrent()`
only checks the range's `top` and `bottom` against the window; when the hit is vertically in
view, nothing scrolls at all. When it is not, `target.scrollIntoView({ block: "center" })` on the
hit's parent element (often the whole cell) does not guarantee the hit is in view either: a cell
wider than the box is aligned on its start.

## Target behaviour

- After the current match changes (typing, Enter, Shift+Enter, F3, the search run again after a
  content update when it moves the current match), the find bar brings the **hit text** (the
  match range) into view horizontally as well as vertically.
- Horizontal: for each ancestor of the hit between the hit and the content root that scrolls
  sideways (computed `overflow-x` `auto` or `scroll`, and `scrollWidth > clientWidth`), from the
  innermost out, when the range's rectangle is not fully inside the box's visible width less a
  margin of 16 px on each side, `scrollLeft` is set so that the range sits inside it; a range
  wider than the box is aligned on its start (the side where the text begins). In practice that is
  the table or its wrapper; a code block that scrolls sideways follows the same rule.
- Vertical: unchanged (the hit is centred when it is above 70 px or below `innerHeight - 20`).
  The horizontal step runs after the vertical one and measures the range again.
- A hit already in view horizontally moves nothing: no `scrollLeft` write.
- Only the scroll boxes move: the page itself never scrolls sideways for this.

## Code anchors (origin/main)

- `src/page/modules/findBar.ts` (689 lines), `scrollToCurrent()` lines 247-260: the vertical test
  and `target.scrollIntoView?.({ block: "center" })`; `showCurrent()` lines 262-270 calls it after
  `paint()`; the markers `@implements_req SwRS-MDOKFSTUDIO-TOOLBAR-010` sit at line 113.
- `src/core/preview/styles/tableStyles.ts` lines 10-18: the table (or `.table-wrapper`) is the
  sideways scroll box.
- `src/page/features/tableCellEditor.ts` lines 21-53: `revealCellInTable` and `CELL_REVEAL_MARGIN`,
  the same idea for the cell editor (TABLE-035). `page/modules` cannot import `page/features`:
  do not import it; a small helper in `findBar.ts` (or a new `src/page/modules/revealInline.ts`)
  is enough.

## Recommended approach

1. In `findBar.ts`, after the vertical branch of `scrollToCurrent()`, call a small function
   `revealRangeInline(range, target, root)`: walk `target` up to the content root; for each
   element whose computed `overflow-x` is `auto|scroll` and that overflows, compare the range's
   `getBoundingClientRect()` with the element's (client box, `clientLeft` included) and adjust
   `scrollLeft` by the difference plus the 16 px margin. Read the range rectangle again after
   each adjustment.
2. Mark it `@implements_req SwRS-MDOKFSTUDIO-TOOLBAR-010`.
3. `findBar.ts` grows by about 25 lines (limit 800). If the helper goes in a new module, keep it
   free of `features` imports.

## Requirements

No `approved` requirement is touched (none in the bundle carries `approved_by`): no owner
agreement needed.

- **SwRS-MDOKFSTUDIO-TOOLBAR-010** (`req_lifecycle: draft`; amend). Normative text: "... move the
  current match with Enter, Shift+Enter and F3, unfold the folded sections that hold it **and
  bring it into view, vertically and inside any box that scrolls sideways**". Amend the second
  nominal scenario's THEN ("scrolls the match to the middle when it is outside the pane") to keep
  it, and add a scenario (nominal) "A hit inside a table scrolled sideways": GIVEN a wide table
  scrolled to its last column and a word that exists only in its second column, WHEN the reader
  types it and presses Enter, THEN the table's box scrolls so that the hit text lies inside it with
  a 16 px margin, and the page does not scroll sideways. Add a boundary row "A hit already in view
  horizontally | no sideways scroll". Add the new tests to the verification notes.
- No new SwRS. `just requirements-update`, generated files committed, a dated entry in
  `requirements/tiers/log.md`.
- Writing skill: no change.

## Tests first (each fails on origin/main)

1. **Unit**, `test/page/modules/findBar.test.ts` (585 lines), next to "a match is scrolled to the
   middle only when it is outside the pane" (line 355), `@tests_req SwRS-MDOKFSTUDIO-TOOLBAR-010`:
   - a match whose range rectangle is left of its scroll box (fake box with `overflow-x: auto`,
     `scrollWidth > clientWidth`, `scrollLeft` 864): after Enter, `scrollLeft` is such that the
     range is inside the box with the margin;
   - a range right of the box: `scrollLeft` grows;
   - a range inside the box: `scrollLeft` is not written;
   - a range vertically in view: no `scrollIntoView` (unchanged rule) but the horizontal step runs.
   The fake `getComputedStyle` and rectangles go in the test's own harness; if the file would pass
   about 700 lines, put the cases in a new `test/page/modules/findBarInline.test.ts`.
2. **Real input**, promoting the replay: a new `test/integration/realInput/findWideTable.ts`
   (scenario `find-wide-table`, registered in `test/integration/realInput/run.ts`), on the content
   of `synth/c5-reading.md`: side preview, edit mode, click `carol`, Escape, the table's
   `scrollLeft > 100`; Meta+f, type `needle`, Enter; the range of `needle` lies inside the table's
   box and inside `[0, innerWidth]`. `@tests_req SwRS-MDOKFSTUDIO-TOOLBAR-010`. Runs in the heavy
   CI run. (`test/integration/realInput/findAfterClick.ts` shows how Meta+f is driven there.)
3. **Visual**: a new scenario `toolbar-navigation/v41-find-hit-in-wide-table-light-393` (next free
   number at the time of writing; re-check at rebase) in a new file
   `test/visual/findWideTableScenarios.ts`, on a new fixture
   `test/visual/fixtures/85-find-wide-table.md` (the first table of `c5-reading.md` is enough),
   viewport `{ width: 393, height: 800 }`, edit mode on. Its check, in a new module
   `test/visual/capture_find_wide_table.py` imported by `test/visual/capture.py`, scrolls the table
   to its end, opens the bar, types `needle`, presses Enter, and asserts that the range is inside the
   table box and the viewport and that `window.scrollX` is 0. `@tests_req
   SwRS-MDOKFSTUDIO-TOOLBAR-010`. Save a `found` step shot. Map the id in `scenarioIds.ts`, register
   the list in `scenarios.ts`.

### Replay promoted

From local commit `87307e8f` (branch `qa/271-table-campaign-replays`, not pushed; read with
`git show 87307e8f:<path>`, never merge or push that branch), add to this PR:

- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c5-1-find-hit-in-scrolled-table-stays-out-of-view.json`
- its fixture `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/c5-reading.md`
  (absent from `origin/main`). CRs 293 and 292 above in the stack use the same fixture and do not
  add it again.

## Acceptance checks (the Verifier runs each at the pushed head)

| # | Claim | Command (from the worktree root) |
| --- | --- | --- |
| A1 | The new unit tests pass | `fnm exec -- npm run compile && fnm exec -- node scripts/node-test.mjs unit "out/test/page/modules/findBar*.test.js"` |
| A2 | They fail on the base | the same command in a detached worktree of the base with the new cases copied in: the horizontal cases fail |
| A3 | The hit is in view in a scrolled wide table (headless) | `fnm exec -- npm run visual:render && uv run --no-sync --group docs python test/visual/capture.py --scenario toolbar-navigation/v41-find-hit-in-wide-table-light-393` passes |
| A4 | The vertical find checks are unchanged | `uv run --no-sync --group docs python test/visual/capture.py --group toolbar-navigation` passes |
| A5 | The same in a real VS Code window | the heavy CI run at the head is green and its integration log names `find-wide-table`; `test/integration/findInPreview.test.ts` still passes there |
| A6 | Traceability | `uv run --no-sync --group requirements okfreq validate --check-links --project-root .` passes; `git grep -n "@tests_req SwRS-MDOKFSTUDIO-TOOLBAR-010"` lists the new tests |
| A7 | Replay and fixture in the PR | `git diff --stat <base>...HEAD -- .agents/skills/markdown-studio-exploratory-qa-claude/` lists the c5-1 replay and `c5-reading.md` |
| A8 | Gates | `just check` and `just preflight` pass |

## Screenshots expected in the PR

- Before (base) and after (head), light theme, 393 px pane, edit mode, the find bar showing
  "1 of 1" for `needle`: before, the table still shows the Owner column and no highlight is
  visible; after, the table has scrolled to the Description cell and the highlighted `needle` is
  in view. Use the `found` step shot of `toolbar-navigation/v41-...` and the same capture on a
  detached worktree of the base. Dark not needed (the highlight colours are unchanged).

## CHANGELOG line (`## Unreleased`)

- Find now scrolls a wide table sideways to show the match, instead of counting a match you could
  not see when the table was scrolled to another column.

## Files expected to change

- `src/page/modules/findBar.ts` (or a new small `src/page/modules/revealInline.ts`)
- `test/page/modules/findBar.test.ts` (or a new `test/page/modules/findBarInline.test.ts`)
- `test/integration/realInput/findWideTable.ts` (new), `test/integration/realInput/run.ts`
- `test/visual/fixtures/85-find-wide-table.md` (new), `test/visual/findWideTableScenarios.ts` (new),
  `test/visual/capture_find_wide_table.py` (new), `test/visual/capture.py`, `test/visual/scenarios.ts`,
  `test/visual/scenarioIds.ts`, `test/visual/scenarioAssertions.ts` (only for a scenario flag)
- `requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-010.md`,
  `requirements/tiers/log.md` and the generated requirement files
- `CHANGELOG.md`
- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c5-1-find-hit-in-scrolled-table-stays-out-of-view.json` (new)
- `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/c5-reading.md` (new)

## Shared with the other CRs of the stack

`test/integration/realInput/run.ts`, `test/visual/capture.py`, `test/visual/scenarios.ts`,
`test/visual/scenarioIds.ts`, `test/visual/scenarioAssertions.ts`, the fixture numbers (84 in
290 below, 85 here, 86 in 291), `requirements/tiers/log.md` and the generated requirement files,
`CHANGELOG.md`, and the fixture `synth/c5-reading.md` (added here, used by 293 and 292). No other
CR of the stack touches `findBar.ts`.

## Blast radius

1. One extra scroll step after a find move, on scroll boxes only. Risk: a hit inside a nested
sideways box (a code block inside a wide table cell) moves both boxes; that is the intended
nearest-first behaviour.

## Open questions

None. Extending the rule to every sideways-scrolling box (a code block too) is the same code; it
is listed as a choice in the PR's "Autonomous decisions".
