---
title: "CR 279: block ids and tokens at the end of a table row"
description: QA271-02 (Medium) and QA271-10 (Low). A column move carries a `^id` from the end of a row into the middle of the row; a token after a row's closing pipe makes the handles inert and sends cell clicks to the raw editor.
status: open
date: 2026-11-10
---

# CR 279: block ids and tokens at the end of a table row

> [!NOTE]
> Source: QA campaign 271, findings QA271-02 (Medium) and QA271-10 (Low), both reproduced and
> replayed. Sheets (read them: steps, variants, code pointers):
> `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/4-archives/271-qa-campaign-tables-2026-11-10/01-stray-anchors/c1b-1-column-move-carries-last-cell-block-id-into-row.md`
> and `.../01-stray-anchors/c1b-2-token-after-last-pipe-table-handles-inert.md`. Owner's answers:
> `02-answers.md` (authoritative). Absorbs the former P1 item `stray-anchors-block-editing`
> (`00-origin.md`): QA never saw a blocked page, so this CR does not chase it. No GitHub issue.
> Priority P2, part of the stack 277 to 282.

## What ships

Owner (2026-11-10): `^id` tokens in table rows come from other tools or agents. A column move must not
carry them into the middle of the row; a trailing token must not make the handles inert.

1. **A token after the closing pipe of a body row is kept as the row tail** (QA271-10). A pipe-table
   body row with more cells than the header, such as `| alpha | 1 | first | ^row-a`,
   `| alpha | 1 | first | {#row-c}` or `| alpha | 1 | first | <!-- keep -->`, is read as a row of
   the header's column count plus a tail: the text after the closing pipe of the last column, kept
   verbatim. The preview already ignores those extra cells, as GFM and markdown-it do. The table is
   then editable: the column and row handles move it, and a click on a cell opens the cell editor,
   not the raw Markdown editor. Every edit keeps the tail at the end of its line:
   - a row move takes the tail along with its row,
   - a column move, column insert or delete, or cell edit leaves it at the end of the line,
   - a new row never copies a tail from its template row,
   - a row delete removes the tail with the row.

   A header or delimiter row with extra cells is still not an editable table. GFM does not render it
   as a table either.
2. **A block id at the end of the last cell stays at the end of the row** (QA271-02). If a column
   operation means the source's last column is no longer last, and the last cell of a body row ends
   with an Obsidian block id (whitespace, then `^` and `[A-Za-z0-9-]+`, at the end of the cell),
   that token leaves the cell and becomes the row tail. This covers a move, and also an insert after
   the last column (same helper). It only happens when the row has no tail yet. The sheet's expected
   diff, which the owner kept:

   ```diff
   -| alpha | 1 | first ^row-b |
   +| alpha | first | 1 | ^row-b
   ```

   This form is also the one `#^row-b` links resolve. `markdownFragmentRange` in
   `src/core/navigation/previewNavigation.ts` matches `\^id` only at the end of a line, so
   `first ^row-b |` was never a link target and `| ^row-b` is. Moving the column back leaves the
   token in the tail (point 1).
   Only `^id` is lifted. `<a id="x"></a>` and other text in the last cell still travel with their
   cell, because they name the cell rather than the row (the sheet's T4).
3. **A conversion that would drop a tail is refused** (SwRS-MDOKFSTUDIO-TABLE-076 rule): pipe to
   list-table, pipe to HTML (convert action, TABLE-073/074), and the toolbar "HTML table" on a pipe
   table (TABLE-117). Each changes nothing. Where a reason channel exists, the reason is:
   "A row has text after its closing pipe that would be lost. Nothing was changed."

## Root cause hypothesis (code anchors on `origin/main`)

- `src/page/modules/markdownTable.ts` `parse` (around line 209) requires
  `rows.every(row.length === columnCount)`. `splitRow` turns `| first | ^row-a` into a fourth cell,
  so `parse` returns `undefined`. Two callers then fall back:
  - `src/page/features/tableRowMove.ts` `movedText` (around line 226) returns `undefined`, and
    `receiveSource` posts `previewEditClosed` without a notice. The move "does nothing".
  - `src/page/features/blockSourceEditor.ts` (around line 80, `tableTools.parse(originalText) ??
    tableTools.parseListTable(...)`) falls back to the raw Markdown editor.

  Handles are decided from the DOM alone (`mappedTable`, `movableRows` and `movableColumns` in
  `tableRowMove.ts`), and the rendered table has three columns, so they show. Fixing the parse fixes
  both symptoms. Hiding the handles would need the source at `refresh` time, so it is not the
  direction.
- `moveColumn` (around line 331) moves whole cells, and `columnsRow` (around line 148) writes each
  kept segment verbatim. The `^row-b` that is part of the last cell's text therefore travels with
  it.

## Design (suggested, the driver may refine)

- `MarkdownTableModel` gains `sourceTails?: string[]`, indexed like `sourceRows` (`""` = no tail).
  `parse` splits each body row with `cellSegments`. When a row has more segments than `columnCount`:
  - its body is `line.slice(0, segments[columnCount - 1].end + 1)`, up to and including the closing
    pipe;
  - its tail is the rest;
  - the body goes in `sourceLines` and its cells in `sourceRows`.

  Every existing path (`spliceRow`, `columnsRow`, the canonical fallback that ends with `|`) works
  on the body unchanged. `serializePipe` appends `sourceTails[origin]` for rows with an origin, and
  nothing for new rows.
- The block-id lift happens in `serializePipe` on the `!sameColumns` path:
  - `S` is the last source column. When `origins.at(-1) !== S` and `origins` contains `S`, for each
    row with origin `o >= 2` and an empty tail whose cell for column `S` matches
    `/^(.*?)\s*(\^[A-Za-z0-9-]+)$/u`, strip the token from that cell (pass the stripped cell as the
    new value, so `columnsRow` rewrites the segment) and use `" " + token` as the tail.
  - Doing it at serialization covers the move by handle, the move with a cell editor open
    (`moveInCellEditor`) and the insert after the last column, with no change to `moveColumn`.
- `tableConversion.ts` `pipeGrid` and `tableEditActions.ts` `htmlTable` refuse a model with any
  non-empty tail. `alignColumn` gives no edit when the caret is in a tail segment, because
  `cellSegments` of the raw line has one segment more.
- Keep `markdownTable.ts` under the 800-line ratchet (426 now). A small helper module is fine if it
  grows.

## Requirements

Every SwRS below is `status: stable`, `req_lifecycle: proposed`, so none is approved and no recorded
agreement is needed. If the driver finds that an **approved** requirement must change, it stops with
`status: blocked` and the exact sentence.

- **SwRS-MDOKFSTUDIO-TABLE-007** (amend): new scenario "A block id at the end of a row stays at the
  end of the row":
  - `| alpha | 1 | first ^row-b |`, last column moved left, gives `| alpha | first | 1 | ^row-b`;
  - a row with a tail `| ^row-a` keeps it at the end of the line after the move;
  - `<a id>` in the last cell moves with its cell.

  Add a scenario row: a table with a token after one row's closing pipe moves like any table.
- **SwRS-MDOKFSTUDIO-TABLE-002** (amend): a row with a tail moves with its tail, and the handles of
  such a table work.
- **SwRS-MDOKFSTUDIO-TABLE-001** (amend): a body row with text after the closing pipe of its last
  column is still an editable pipe table. The cell editor opens, and the tail is kept verbatim on
  save. This makes the "not an editable pipe table" fallback precise. Check
  **SwRS-MDOKFSTUDIO-TABLE-094** (one cell edit changes exactly one line) still holds with a tail.
  Add a criterion if needed rather than change its intent.
- **SwRS-MDOKFSTUDIO-TABLE-076** (amend): the refusal row for a pipe table whose rows have text after
  the closing pipe. Check **TABLE-117** (toolbar HTML table) and say there that such a table is not
  converted.
- **SwRS-MDOKFSTUDIO-TABLE-102** (edge pipes optional): read it. If it states the cell count rule,
  add the tail case there instead of in TABLE-001, so the rule lives in one place.
- No new SwRS is expected. If the driver prefers one leaf for "the row tail", it is created with
  `okfreq new` (never hand-allocated).
- Markers: `@implements_req` on `parse`, `serializePipe` (TABLE-001/007/002), `pipeGrid` and
  `htmlTable` (TABLE-076/117). `@tests_req` on each new test. Run `just requirements-update`, add a
  dated entry in `requirements/tiers/log.md`, and a `CHANGELOG.md` `## Unreleased` line.
- No change to the writing skill: no rendered syntax changes.

## Tests first (each must fail on the unchanged code)

Unit:

- `test/page/modules/tableColumnMove.test.ts`:
  - T2 row `| alpha | 1 | first ^row-b |`: `moveColumn(2 -> 1)` then `serialize` gives
    `| alpha | first | 1 | ^row-b`, header `| Name | Note | Value |`, and the other rows only
    reordered;
  - moving the column back keeps `| ^row-b` at the line end;
  - `<a id="x"></a>` moves with its cell;
  - inserting a column after the last also lifts the token;
  - a cell that is only `^row-b` leaves an empty cell.
- `test/page/modules/markdownTable.test.ts`:
  - `parse` accepts T1, T3, T5 (tails `^row-a`, `{#row-c}`, `<!-- keep -->`) with 3 columns;
  - `serialize` without an edit is byte-identical, CRLF included;
  - a cell edit on the tailed row changes only that row's cell and keeps the tail;
  - `moveRow` takes the tail along;
  - a new row inserted after the tailed row has no tail;
  - a header row with an extra cell is still refused;
  - `| a | b | c | d |` in a 3-column table keeps ` d |` verbatim as the tail.
- Conversion: `convertTable(T1, "list-table")` returns `ok: false` with the reason. The toolbar
  HTML table on T1 gives no edit. Use the existing conversion and edit-action tests:
  `test/page/modules/listTable.test.ts` or `markdownTable.test.ts`, and
  `test/page/modules/editActions.test.ts`. The last is at 1498 lines, near the 1500 test ratchet,
  so put that test in a new file.
- `test/page/runtimeTableRowMove.test.ts` (706 lines): a host source with T1, Alt+Left on the Note
  column handle, gives one `previewEditSave` whose text is the expected table with `| ^row-a`
  kept.
- Cell editor: a click on a cell of a T1-like table answered with that source opens
  "Markdown table cell editor", not "Raw Markdown editor".
  `test/page/runtimeTableCellEditor.test.ts` is at 1499 lines, so use a new file or a smaller
  neighbour.

Real input (real VS Code window, run by CI, heavy run). This CR promotes these replays from the local
branch `qa/271-table-campaign-replays` (commit 87307e8f, not pushed). Read them with `git show`; do
not merge that branch:

- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c1b-1-column-move-carries-last-cell-block-id-into-row.json`
  (QA271-02, the owner asked for it). Promote it.
- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c1b-2-token-after-last-pipe-table-handles-inert.json`
  (QA271-10). Promote it as well: same fixture, a few more lines.

  Its diff check describes the old behaviour (`equal: false` with `notContains: "| Name | Note |
  Value |"`), so it fails once the move works. The real-input test asserts the fixed behaviour: the
  header becomes `| Name | Note | Value |`, the row becomes `| alpha | first | 1 | ^row-a`, and a
  click on "beta" opens the cell editor (`[data-sphinx-table-menu]` present).
- Fixture: `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/anchors-trailing-tokens.md`,
  from the same commit. Take it with the scenarios, or inline the needed tables in the test through
  `withDocument`, as `tableEscape.ts` does.

New file `test/integration/realInput/tableRowTokens.ts`, registered in
`test/integration/realInput/run.ts`. Its header names both replays, as `qa210Replays.ts` does.

## Files expected to change (for ordering the stack)

- `src/page/modules/markdownTable.ts` (`parse`, `serializePipe`, model type): the main change.
- `src/page/modules/tableConversion.ts` (`pipeGrid` refusal).
- `src/page/modules/tableEditActions.ts` (`htmlTable` refusal, `alignColumn` guard).
- Probably none in `src/page/features/tableRowMove.ts` or `blockSourceEditor.ts`: they recover through
  `parse`. Only comments or markers change there.
- Tests:
  - `test/page/modules/tableColumnMove.test.ts`, `test/page/modules/markdownTable.test.ts`,
    `test/page/runtimeTableRowMove.test.ts`;
  - a new unit test file for the cell editor open and the HTML refusal;
  - `test/integration/realInput/tableRowTokens.ts` (new), `test/integration/realInput/run.ts`.
- Requirements: `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-{001,002,007,076}.md`
  (maybe 102 and 117), `requirements/tiers/log.md`, plus generated index and coverage files.
- `CHANGELOG.md`.

Stack overlap:

- **CR 278** (short delimiter) changes the delimiter regex in the same `parse` function. Both
  touch `markdownTable.ts` `parse` and probably TABLE-001.
- `run.ts`, `requirements/tiers/log.md`, `CHANGELOG.md` and the generated requirement indexes
  conflict with every CR of the stack that adds a real-input scenario or a requirement.
- CRs 277, 280 and 282 likely touch the cell editor and preview patching, not `markdownTable.ts`.

## Blast radius

2. `parse` is the shared pipe-table reader of the cell editor, the row and column moves, the table
bar actions, the conversions and the raw-editor table actions. Accepting rows with a tail widens what
all of them see. Every other table must still serialize byte-identically, so the existing
`markdownTablePreservation.test.ts` must pass unchanged. One visible change: a lifted `^id` is no
longer shown in the preview cell, because GFM drops extra cells. This follows the owner's chosen
direction and makes `#^id` links resolve.

## Gates

- `just check` (format, types, import boundaries, size ratchet, unit, contract, requirements lint).
- Headless visual of the group:
  `uv run --no-sync --group docs python test/visual/capture.py --group table-editing` after
  `npm run visual:render` (no visual change is expected; the handles must still be placed).
- `just requirements-update`; okfreq validate and coverage as CI runs them.
- No local real VS Code window (a QA session uses one). Run the heavy CI run on the branch with
  `gh workflow run ci.yml --ref <branch> -f heavy=true` for the real-input scenarios. The PR is
  opened as a draft and marked ready only when the PR CI and the heavy run are green and the
  Inspector approved.

## Done when

- The two promoted scenarios pass in the heavy run. T1, T3 and T5 move and open the cell editor. In
  T2, `^row-b` ends its row after a column move. T4 and T6 behave as today.
- Every unit test above fails on `origin/main` and passes on the branch.
- `just check`, the visual group, the requirements update, the log entry and the CHANGELOG line are
  done.

## Open questions

None. The owner kept the sheet's expected diff (token after the closing pipe), and the
other choices follow from it.
