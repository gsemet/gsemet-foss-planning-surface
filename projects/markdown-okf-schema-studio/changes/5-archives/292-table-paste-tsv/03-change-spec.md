---
title: Change spec - a spreadsheet (TSV) paste into a table cell fills the cells like a spreadsheet
cr: 292
date: 2026-11-11
issue: none
priority: P3
source: QA campaign 271, QA271-12 (Low)
blast_radius: 2 (a paste now changes several cells, rows and columns in one write)
inspector: Opus
stack: 290 (bottom), 289, 293, 292, 291, 288 (top)
---

# Change spec: a spreadsheet (TSV) paste into a table cell fills the cells like a spreadsheet

> [!NOTE]
> Source: QA campaign 271, finding QA271-12. Sheet:
> `.agents/changes/4-archives/271-qa-campaign-tables-2026-11-10/06-table-reading-clipboard/c5-2-pasted-tsv-keeps-raw-tab-in-cell.md`
> (no image: the defect is in the source line). Owner's answers: `02-answers.md` (run now, fourth
> from the bottom of the stack, no GitHub issue). The owner's decision **replaces** the sheet's
> suggestion (tabs turned into spaces in one cell): a spreadsheet (TSV) paste of several cells
> into a table cell fills the cells from the current one, rightwards and downwards, like a
> spreadsheet, and adds the missing rows and columns; one undo step undoes the whole paste; a
> single value without tab or newline pastes as today. Read code on `origin/main` (`33fb65ef`).
> Rules: `.agents/constitution.md`, `AGENTS.md`, `requirements/guidelines/project.guidelines.md`.

## Problem

The cell text box has no paste listener (native paste). Its `input` listener turns line breaks
into spaces (SwRS-MDOKFSTUDIO-TABLE-091) but keeps tab characters. Pasting two spreadsheet rows
(`a\tb\tc\n1\t2\t3\n`) into the cell `row five` writes
`| Five | a<TAB>b<TAB>c 1<TAB>2<TAB>3  | erin |`: invisible tabs and a trailing space in one cell.
Copying cells from the preview gives TSV too, so pasting it back does the same.

## Target behaviour

### When a paste is a grid paste

- A paste into the cell text box is a **grid paste** when its plain text (`text/plain`), after
  removing one final line break (`\r\n`, `\n` or `\r`), holds at least one tab character.
- Otherwise the paste is native, exactly as today: a single value, and also a multi-line text
  without any tab (its line breaks become spaces, TABLE-091). See Open questions.
- Cmd/Ctrl+Shift+V (paste as plain text) is a grid paste too when the text has a tab: the grid
  is plain text already.

### What a grid paste does

- The text is split into lines (`\r\n`, `\n`, `\r`) and each line into values at each tab. No
  quote handling: a value is the text between two tabs, as it is (a spreadsheet's quoted cell with
  a line break inside is out of scope). Each value is trimmed of surrounding spaces; its pipes are
  written `\|` by the usual cell writing (TABLE-091). Empty values are empty cells.
- The grid is written from the **open cell**, which takes the first value (its whole text is
  replaced, whatever the selection inside the field), then rightwards along the row and downwards
  row by row, like a spreadsheet. Starting in the header row, the next lines go to the first body
  rows (the delimiter row is never written).
- Missing columns are added at the right end of the table (empty header cell, `---` delimiter
  cell, empty cells in the other rows), missing rows are added at the end of the table (empty
  cells outside the grid). Cells outside the grid keep their text.
- The table is saved **once** (one final `previewEditSave`, so one undo step in the source undoes
  the whole paste), the table is rendered again and the cell editor reopens in the start cell
  showing its new text, as after a structural button (the `structural` helper).
- Works the same in a `{list-table}` opened in the cell editor (the model's `insertRowAfter` and
  `insertColumnAfter` already handle it).
- Nothing else of the cell editor changes: typing, Tab, Escape, the inline palette.

## Code anchors (origin/main)

- `src/page/features/tableCellEditor.ts` (609 lines), `renderTableCellEditor` (line 248 on): the
  text box `input` listener that flattens line breaks (lines 279-292, `@implements_req
  TABLE-091`); the `structural` helper (around line 361) that saves the model and reopens the
  editor through `rememberPendingBlockNavigation(... { tableRowIndex, tableColumnIndex })`;
  `modelRowOf()` (line 18: the rendered row to the model row, skipping the delimiter row).
- `src/page/features/blockSourceEditor.ts` lines 164-200: the paste listener of the raw block
  editor (comment: "the table cell editor has no paste listener (native paste)"), useful as the
  pattern for reading `clipboardData`.
- `src/page/modules/markdownTable.ts`: `insertRowAfter`, `insertColumnAfter`, `serialize` (the
  cell escaping happens on write).
- `src/page/modules/tableStructure.ts`: `insertRowBefore`, `insertColumnBefore`.

## Recommended approach

1. A new pure module `src/page/modules/tableGridPaste.ts`:
   - `spreadsheetGrid(text: string): string[][] | undefined` (undefined when the paste is not a
     grid paste);
   - `fillGrid(model, tools, startRenderedRow, startColumn, grid)`: adds the missing columns and
     rows through the model tools, writes the values, returns nothing. `@implements_req
     SwRS-MDOKFSTUDIO-TABLE-120` (provisional ID).
2. In `renderTableCellEditor`, a `paste` listener on the text box: if `spreadsheetGrid` returns a
   grid, `preventDefault()`, `fillGrid(...)`, then the `structural` path (save once, reopen in the
   start cell). Otherwise do nothing (native paste and today's `input` flattening).
3. Text typed in the cell before the paste and not yet autosaved goes into that one save; the
   start cell's text is replaced by the paste anyway, so nothing typed elsewhere is lost.

## Requirements

No `approved` requirement is touched (none in the bundle carries `approved_by`): no owner
agreement needed.

- **New SwRS, provisional ID SwRS-MDOKFSTUDIO-TABLE-120** (scope `table-editing`, created with
  `okfreq new ... --lifecycle proposed`, derives from `StRS-MDOKFSTUDIO-TABLE-012`, the parent of
  TABLE-091): "A spreadsheet paste into a table cell fills the cells from that cell". Normative:
  When the writer pastes into a cell text box a text that holds a tab, the extension SHALL write its
  values into the cells from the open cell rightwards and downwards, add the missing columns at the
  right and the missing rows at the end, save the table in one edit and reopen the editor in that
  cell. Scenarios: (nominal) the QA case (2×3 grid at `row five`: `| Five | a | b | c |` and a new
  row `|  | 1 | 2 | 3 |`, one new column with an empty header); (nominal) a grid that fits (no row or
  column added, cells outside the grid unchanged); (boundary) start in the header row (the delimiter
  is skipped); (boundary) trailing line break, CRLF, empty values, a value with a pipe (`\|`);
  (boundary) one undo step; (refusal) a single value or a text without a tab: native paste
  (TABLE-091); (boundary) a list-table. Provisional: the stack assigns the next free `TABLE` IDs
  bottom to top (this CR takes the first, 291 the second); `okfreq new` allocates the real one at
  rebase, and the code markers follow it.
- **SwRS-MDOKFSTUDIO-TABLE-091** (`proposed`, `stable`; amend). Scenario "Line break pasted into
  the cell text box": add "a text without a tab"; add a related-requirements line to TABLE-120 ("a
  pasted text with a tab is a grid paste").
- `just requirements-update`, generated files committed, a dated entry in `requirements/tiers/log.md`.
- Writing skill: no change (no rendered syntax changes).

## Tests first (each fails on origin/main)

1. **Unit, pure**: a new `test/page/modules/tableGridPaste.test.ts`, `@tests_req
   SwRS-MDOKFSTUDIO-TABLE-120`: `spreadsheetGrid` on `a\tb\tc\n1\t2\t3\n`, `a\tb\r\n`, `a\n`
   (undefined), `abc` (undefined), `a\t\tc`; `fillGrid` on a 2-column, 2-body-row model: grid that
   fits, grid adding one column and one row, start in the header row, a value with a pipe, a
   list-table model. Serialised text compared line by line.
2. **Unit, runtime**: a new `test/page/runtimeTableCellPaste.test.ts` (harness of
   `runtimeTableCellEditor.test.ts`, which is at 1 499 lines and must not grow), `@tests_req
   SwRS-MDOKFSTUDIO-TABLE-120`: a `paste` event with `clipboardData` `text/plain` = the QA grid on
   the `row five` cell: default prevented, exactly one final save whose text is the expected table,
   and a pending navigation to the start cell; a paste of `x` or `a\nb`: default not prevented, no
   save (TABLE-091 path unchanged).
3. **Unit, existing**: `test/page/fmtableReqTable.requirements.test.ts`, test "a line break pasted
   into the cell text box becomes a space in the source row" (line 353) stays as it is and must
   pass.
4. **Real input**, promoting the replay: a new `test/integration/realInput/tableGridPaste.ts`
   (scenario `table-grid-paste`, registered in `test/integration/realInput/run.ts`), on
   `synth/c5-reading.md`: `await vscode.env.clipboard.writeText("a\tb\tc\n1\t2\t3\n")`, click
   `row five`, Meta+a, Meta+v: the buffer holds `| Five | a | b | c |` and a new last row with
   `1`, `2`, `3`, no tab character, the editor open in the start cell; Escape; then one
   `undo` in the source gives the buffer as before the paste. `@tests_req
   SwRS-MDOKFSTUDIO-TABLE-120`. Runs in the heavy CI run.
5. **Visual**: `table-editing/v32-grid-paste-light-900` (next free number after 293's v30-v31;
   re-check at rebase), in a new file `test/visual/tableGridPasteScenarios.ts`, fixture
   `08-okf-schema`, edit mode; a new capture module `test/visual/capture_table_grid_paste.py`
   (imported by `test/visual/capture.py`) opens the editor in the last body row, dispatches a
   `paste` event with a `DataTransfer` holding a 2×2 grid that adds one row and one column, waits for
   the reopened editor and asserts the new cells' text. Save a `pasted` step shot.

### Replay promoted

From local commit `87307e8f` (branch `qa/271-table-campaign-replays`, not pushed; read with
`git show 87307e8f:<path>`, never merge or push that branch), add to this PR:

- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c5-2-pasted-tsv-keeps-raw-tab-in-cell.json`

Its fixture `synth/c5-reading.md` is added by CR 289 below in the stack; do not add it again.
Change the replay's last check, because the owner's decision changes the expected result (the
sheet expected `| Five | a b c 1 2 3 | erin |`): drop `"maxLines": 1`, keep `"notContains": "\t"`,
and check that the file holds `| Five | a | b | c |` and a row with `1`, `2` and `3`. Say why in
the commit body.

## Acceptance checks (the Verifier runs each at the pushed head)

| # | Claim | Command (from the worktree root) |
| --- | --- | --- |
| A1 | The new unit tests pass | `fnm exec -- npm run compile && fnm exec -- node scripts/node-test.mjs unit "out/test/page/modules/tableGridPaste.test.js" "out/test/page/runtimeTableCellPaste.test.js"` |
| A2 | They fail on the base | the runtime test copied into a detached worktree of the base fails (no paste listener) |
| A3 | A single value and a multi-line text paste as today | `fnm exec -- node scripts/node-test.mjs unit "out/test/page/fmtableReqTable.requirements.test.js"` passes, and the runtime test's native cases pass |
| A4 | The grid fills cells and adds a row and a column (headless) | `fnm exec -- npm run visual:render && uv run --no-sync --group docs python test/visual/capture.py --scenario table-editing/v32-grid-paste-light-900` passes |
| A5 | Real window: cells filled, no tab, one undo step | the heavy CI run at the head is green and its integration log names `table-grid-paste` |
| A6 | Traceability | `uv run --no-sync --group requirements okfreq validate --check-links --project-root .` passes; the new SwRS lists `src/page/modules/tableGridPaste.ts` and the three test files |
| A7 | Replay in the PR with the new expected result | `git show HEAD:.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c5-2-pasted-tsv-keeps-raw-tab-in-cell.json` has no `maxLines` and checks `\| Five \| a \| b \| c \|` |
| A8 | Gates | `just check` and `just preflight` pass |

## Screenshots expected in the PR

- Before (base) and after (head), light theme, 900 px, the `08-okf-schema` table after the 2×2
  grid paste: before, one cell holds the raw values with spaces; after, the values fill four
  cells and the table has its new row and column, the editor open in the start cell. Use the
  `pasted` step shot of v32 and the same capture on a detached worktree of the base.

## CHANGELOG line (`## Unreleased`)

- Pasting cells copied from a spreadsheet into a table cell now fills the cells from that one,
  rightwards and downwards, and adds the rows and columns the table lacks. One undo takes the whole
  paste back. Pasting a single value works as before.

## Files expected to change

- `src/page/modules/tableGridPaste.ts` (new)
- `src/page/features/tableCellEditor.ts` (the paste listener)
- `test/page/modules/tableGridPaste.test.ts` (new), `test/page/runtimeTableCellPaste.test.ts` (new)
- `test/integration/realInput/tableGridPaste.ts` (new), `test/integration/realInput/run.ts`
- `test/visual/tableGridPasteScenarios.ts` (new), `test/visual/capture_table_grid_paste.py` (new),
  `test/visual/capture.py`, `test/visual/scenarios.ts`, `test/visual/scenarioIds.ts`,
  `test/visual/scenarioAssertions.ts` (only for a flag)
- `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-120.md` (new, provisional ID),
  `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-091.md`, `requirements/tiers/log.md`
  and the generated requirement files (indexes, coverage, StRS link lists)
- `CHANGELOG.md`
- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c5-2-pasted-tsv-keeps-raw-tab-in-cell.json` (new, last check adapted)

## Shared with the other CRs of the stack

- `src/page/features/tableCellEditor.ts`: 293 below (hint, Escape) and 291 above (contained
  tables). This CR only adds a `paste` listener in `renderTableCellEditor`.
- The new SwRS ID: 292 takes the first free `TABLE` ID (120 at the time of writing), 291 the next.
- `test/integration/realInput/run.ts`, `test/visual/capture.py`, `scenarios.ts`, `scenarioIds.ts`,
  `scenarioAssertions.ts`, the `table-editing/vNN` numbers (v32 here), `requirements/tiers/log.md`
  and the generated requirement files, `CHANGELOG.md`, the fixture `synth/c5-reading.md` (from 289).
- 291 above makes contained tables editable: a grid paste there goes through the same model and
  save, so it keeps the container prefix; 291 checks it.

## Blast radius

2. One paste can now change many lines (every row gets a cell when a column is added). Risks: a
paste that is not meant as a grid (a code snippet with a tab) spreads over cells (one undo takes
it back); a large paste writes a large table; a stale model if the paste lands while a save is in
flight (the `structural` path already guards on `edit.finishing`).

## Open questions

- A one-column copy from a spreadsheet (`a\nb\nc`, no tab) cannot be told apart from a multi-line
  text. **Recommended answer: keep it as today** (one cell, line breaks become spaces, TABLE-091):
  only a text with a tab is a grid paste. The other reading of "a single value without tab or
  newline" (every multi-line paste fills a column) would change TABLE-091 and split pasted prose
  or a pasted Markdown table into rows.
