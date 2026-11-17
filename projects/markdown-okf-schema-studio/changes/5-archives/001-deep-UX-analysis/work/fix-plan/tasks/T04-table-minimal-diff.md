# T04 — Editing one table cell changes one source line

| Field | Value |
| --- | --- |
| Fixes | [UX-12](../../02-table-editing/UX-12-cell-edit-rewrites-whole-table.md) (+ part-2 evidence: aligned and compact tables) |
| Depends on | T01, T02 |
| Gate | `unit trusted` |
| Risk | Medium (table editing is protected feature P-E5) |
| Commit message | `fix(vscode): keep table formatting when editing one cell` |

## Goal

`serialize(model)` must reproduce every untouched row **byte for byte**. In an edited row, only the
edited cell's segment between its pipes changes. All T01 `todo: "UX-12 (T04)"` tests pass, and their
markers are removed.

## Context to read first

- `src/webview/markdownTable.ts`: `createMarkdownTableTools`, `splitRow`, `escapeCellPipes`, `parse`,
  `serialize`, `insertRowAfter`, `deleteRow`, `insertColumnAfter`, `deleteColumn`. The factory is
  stringified into the webview runtime (`conventions.md` §3): keep it self-contained.
- How the runtime uses it, in `src/webview/scrollSync.ts`: `renderTableCellEditor`, `switchTableCell`,
  `postBlockEditSave` (`tableTools.serialize(edit.tableModel)`), `receiveBlockEditSource`
  (`tableTools.parse(message.originalText)`).
- `test/webview/markdownTablePreservation.test.ts` (T01) and `test/webview/markdownTable.test.ts`.

## Allowed files

- `src/webview/markdownTable.ts`
- `test/webview/markdownTablePreservation.test.ts` (remove the `todo` markers; add tests)
- `test/webview/markdownTable.test.ts` (add tests only)
- `test/integration/realInput.test.ts` (add RI-T04)
- `test/webview/scrollSync.test.ts` and `test/integration/previewEditing.test.ts`: only under the
  conditions listed in "Expected changes to existing tests"

## Design (follow it exactly)

1. Extend `MarkdownTableModel` with **optional** fields. They are optional so that code building a
   model by hand keeps working.

   ```ts
   sourceLines?: string[];               // original lines, without line endings, indentation included
   sourceRows?: string[][];              // cells as parsed from sourceLines (deep copy)
   rowOrigins?: (number | undefined)[];  // for each current row, the index of its source row; undefined for new rows
   columnsChanged?: boolean;             // set by insertColumnAfter / deleteColumn
   ```

2. `parse`: fill `sourceLines` (the `lines` array after removing the trailing empty element),
   `sourceRows` (`rows.map(row => [...row])`) and `rowOrigins` (`rows.map((_, i) => i)`).
3. Add an internal `cellSegments(line)` that scans the **untrimmed** line with exactly the same rules
   as `splitRow` (backslash escapes, code-span backtick runs, optional outer pipes). It returns, for
   each cell, `{ start, end }`: the offsets in `line` of the text between the two delimiting pipes,
   including surrounding whitespace. For a line without a leading pipe, the first segment starts
   after the indentation. Unit-test it directly, by exporting it on the returned tools object as
   `cellSegments`.
4. Add `spliceRow(line, oldCells, newCells)`. For each cell index where
   `newCells[i] !== oldCells[i]`, replace the segment with `leading + escapeCellPipes(newCells[i]) + trailing`:
   - `leading` is the segment's original leading whitespace.
   - If the original segment had trailing whitespace: `trailing` = spaces up to the original
     segment length, minimum 1 space.
   - Otherwise `trailing` = `""`.

   Unchanged segments stay verbatim. Apply the replacements from the last cell to the first so that
   offsets stay valid.
5. `serialize(model)`:
   - **No `sourceLines`, or `columnsChanged === true`:** use the current canonical serialization
     (unchanged code path). Column operations rewrite every line anyway.
   - **Otherwise,** for each current row `r` with origin `o = rowOrigins[r]`:
     - `o !== undefined` and the cells equal `sourceRows[o]` → `sourceLines[o]` verbatim;
     - `o !== undefined` and some cells changed → `spliceRow(sourceLines[o], sourceRows[o], row)`;
     - `o === undefined` (new row) → `spliceRow(template, templateCells, row)`. The template is the
       source line of the nearest preceding row that has an origin (never the delimiter row, index 1);
       when the new row comes right after the delimiter, use the first body row, or the header if
       there is none. With an all-empty new row, this yields a correctly padded empty row in the
       table's own style.
   - Join with `model.lineEnding` and append it when `model.trailingLineEnding`, as today.
6. `insertRowAfter` / `deleteRow`: keep `rowOrigins` in sync by splicing `undefined` in, or the
   entry out, at the same index as the row (only when `rowOrigins` exists).
   `insertColumnAfter` / `deleteColumn`: set `columnsChanged = true`.
7. Keep every exported name and every existing signature unchanged.

## Tests

Write first, and show the failures:

1. Remove every `todo: "UX-12 (T04)"` marker in `markdownTablePreservation.test.ts`. All tests pass
   after the fix.
2. Add, in `markdownTable.test.ts`:
   - `cellSegments` offsets for `| a | b |`, `|a|b|`, `a | b`, `  | a \| b | \`x|y\` |`;
   - unchanged model → `serialize(parse(s)) === s` for the padded and compact corpus tables
     (already covered; do not duplicate it if it exists);
   - insert a row after body row 1 of the padded table → `lineDelta` adds exactly one line, equal to
     `|          |          |`;
   - **added after the T01 review (NIT):** a shrinking value in the padded table: `rows[2][1]` =
     `s` → the changed line is `| first    | s        |` (the original cell width is kept);
   - delete body row 1 of the compact table → exactly one line removed;
   - insert a column → the output parses back with one more column (canonical style accepted);
   - CRLF table: the inserted row keeps `\r\n`.
3. Real-input E2E, scenario **RI-T04** in `realInput.test.ts`:
   - Fixture with a padded table and a compact table (copy the corpus `padded` and `compact-book`
     sources, separated by a paragraph).
   - In edit mode, click the cell `second`, press `End`, type ` X`, press `Enter`.
   - Assert `lineDelta(original, buffer)` has exactly one removed and one added line, and the added
     line is `| first    | second X |`.
   - Repeat on the compact table: click `Ana`, type ` Lee`, `Enter` → `| Plan | Ana Lee |`.

   This test must fail before the fix (whole-table rewrite). Record the failure.

## Expected changes to existing tests

- `scrollSync.test.ts` table tests and the table expectations in `previewEditing.test.ts` change
  **only if** their fixture table is not in canonical `| a | b |` + `| --- |` style. Each changed
  expectation must now equal the source line style. List each change in the report, with the old
  and new expected text.
- No other existing assertion may change.

## Must not change

- Cell parsing rules (`splitRow`), escaping of pipes typed by the user (`escapeCellPipes`), the
  header and last-body-row deletion guards, and the toolbar behaviour (P-E5).
- `parse` must still reject non-tables exactly as before. Run the existing tests unchanged.

## Done when

- The `unit` and `trusted` gates pass; T01 table todos are gone.
- RI-T04 passes, and its two captures show the edited tables.
- `git diff` of the RI-T04 fixture after the edit shows exactly one changed line per edit, as
  evidenced by the test assertions.
