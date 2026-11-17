# T04 review — round 1

Base: ce5784ed5251957a865b8f31771f888d89591ccc · Reviewed diff: 4 files, +273/-18

## Gates

- compile: PASS (`logs/T04-compile.log`, reviewer rerun `logs/T04-review-compile.log`)
- unit: PASS. 367 tests, 349 pass, 0 fail, 18 todo (`logs/T04-unit.log`, reviewer rerun
  `logs/T04-review-unit.log`). The 18 remaining `todo` markers are the T05 and T06 frontmatter
  markers. No `UX-12 (T04)` marker is left.
- trusted: PASS, exit 0 (`logs/T04-trusted.log`). Real-input order 01–04, 06, 07, 05. No
  `Frame was detached`.
- T00 baseline comparison: no new failure. The unit and trusted baselines were clean.

## Done-when

- [x] `unit` and `trusted` gates pass, and the T01 table todos are gone. Evidence: the logs above.
  `rg "UX-12" test` finds nothing.
- [x] RI-T04 passes, and its two captures show the edited tables. Evidence:
  `.artifacts/real-input-JZRxpE/06-table-padded-edit.png` and `07-table-compact-edit.png`. I opened
  both. Each shows the source line and the rendered cell (`second X`, `Ana Lee`), with no open cell
  editor and no overlay.
- [x] One changed line per edit in the RI-T04 fixture. Evidence: the `assert.deepEqual(lineDelta(…))`
  checks in `scenarioTableMinimalDiff`, plus the whole-buffer equality waits.
- [ ] Goal: "`serialize(model)` must reproduce every untouched row byte for byte; in an edited row only
  the edited cell's segment changes". This holds for tables with both outer pipes. It does **not**
  hold safely for rows without a leading or trailing pipe (finding 1), and the padding rule fails
  for whitespace-only cells (finding 2).
- [x] Tests written first. The unit pre-fail log (`logs/T04-impl-prefix-run.log`) and the RI-T04
  pre-fail run are genuine. `logs/T04-impl-prefail-trusted.log` was run with the base
  `markdownTable.ts` bundled. It fails in `scenarioTableMinimalDiff` with
  `Timed out waiting for the padded table cell edit to reach the source buffer`. Scenarios 01–04
  passed in that run, so the failure comes from the whole-table rewrite.

## Protected features checked

- **P-E5 (table cell editor): REGRESSION for tables without outer pipes (finding 1).**
  - What still works:
    - Row and column insert and delete still go through the same functions.
    - The `deleteRow` refactor is equivalent to the base: same index clamp, same return value.
    - The header and last-body-row guards are unchanged. I verified that `deleteRow(m, 0)` and the
      last body row both return `undefined`.
    - Column operations set `columnsChanged` and use the old canonical path. The existing
      `scrollSync.test.ts` test "table cell editing exposes row and column operations…" still
      passes, with byte-identical expected output.
    - `switchTableCell` keeps changes: the model and `rowOrigins` persist for the whole session, and
      `originalText` does not change within a session, so `sourceLines` always matches it.
  - What I probed with the compiled module and a 359-case property check: every non-delimiter cell
    set to `""`, `x`, `a|b`, `` `c|d` `` and a long value, plus Row+ at every position, Row+ with a
    filled cell, and Row− at every position, across 11 table styles. The styles were compact,
    padded, no-spaces, alignment, no outer pipes, leading pipe only, trailing pipe only,
    escaped/code, indented, CRLF, and old-canonical empty cells.
    - Escaped pipes, code spans with pipes, alignment rows, CRLF (Row+ keeps `\r\n`), indented tables
      and trailing whitespace after the last pipe are correct.
    - **22 cases produce a row that `parse` rejects. All are in tables without a leading and/or
      trailing pipe.**
    - The base serializer produced 0 rejected rows on the same check, so this is a T04 regression.
- **P-R1 (rendering):** affected through finding 1. markdown-it renders `  | d` (first cell cleared,
  no outer pipes) as the row `d |  `, so the value moves into the first column. I checked this with
  `markdown_it` in the repository venv.
- **P-E3:** the raw-Markdown editor path is unchanged. Note: finding 1 sends the user to this
  fallback whenever `parse` rejects the table.
- **P-E6:** host checks are unchanged. `originalText` is still the session's original block text, and
  `editedText` keeps its trailing line ending. An unchanged model now serializes to exactly
  `originalText`, so Enter without a change closes the editor without a save. Before, a save
  rewrote the table. This is an improvement.
- **P-E8:** no new interactive surface. Table editing is still reached only in edit mode.
- **P-S2:** no new message types or fields.
- **P-S4:** no `innerHTML` change.
- **Conventions §3 (injected factory):** `cellSegments`, `spliceRow` and the `templateRowOrigin`
  arrow are declared inside `createMarkdownTableTools`.
  - They reference only sibling helpers and globals (`Math`, `Array`).
  - TypeScript-only syntax is limited to erased annotations and `as number`.
  - The factory reaches the runtime through the `${createMarkdownTableTools.toString()}`
    substitution. Backticks inside it are therefore inserted verbatim and are safe; the only one is
    the pre-existing canonical template. The §2 template rules apply to `scrollSync.ts`, which is
    unchanged.
  - tsconfig targets ES2022, and esbuild targets node20 without `keepNames`, so no outer helper is
    referenced.
  - Proof:
    - the vm-evaluated `scrollSync.test.ts` suite passes;
    - RI-T04 reproduces the byte-exact expected lines from the minified bundle.

## Deviations in the report's open points

1. Canonical path when `sourceLines`, `sourceRows` **or** `rowOrigins` is missing: **accepted**.
   Models from `parse` always carry all three, and the stricter guard prevents a crash on partial
   hand-built models.
2. Template lookup uses body rows only, and the header only when no body row exists:
   **accepted**.
   - It implements the explicit design clause: "never the delimiter row; right after the
     delimiter → first body row, else header".
   - When several new rows are stacked, it takes the style of the next original body row instead
     of the header. That is the more consistent choice.
3. Mid-scenario capture `06`: **accepted**. It is taken after the commit, the re-render and the
   closing of the editor, so it shows the intended state. The document fits on one screen. The
   second step re-targets `Ana` with a fresh click, so the capture's scroll-to-top and pointer move
   cannot affect it.
4. The `withDocument` helper is accepted. `withSmokeDocument` delegates with the same content, file
   name and cleanup.

## Findings

1. **[BLOCKER]** `src/webview/markdownTable.ts`, `spliceRow` (used by `serialize`): on a row
   without a leading pipe, without a trailing pipe, or without both, an empty first or last cell
   loses its delimiter. The row then no longer splits back into the model's cells.
   - Reproduction (compiled module):

     | Input | Action | Output | Result |
     | --- | --- | --- | --- |
     | `a \| b` / `--- \| ---` / `c \| d` | `insertRowAfter(m, 1)` | new line `  \| ` | `parse` rejects |
     | same | `rows[2][0] = ""` | `  \| d` | `parse` rejects; markdown-it renders `d` in column 1 |
     | same | `rows[2][1] = ""` | `c \| ` | `parse` rejects |
     | same | Row+ then `rows[3][0] = "n"` | `n \| ` | `parse` rejects |
     | `\| a \| b` / `\| --- \| ---` / `\| c \| d` | clear the last cell, or Row+ | — | `parse` rejects |
     | `a \| b \|` / … | clear the first cell, or Row+ | — | `parse` rejects |

   - Effects, which the base serializer never produced because it always emitted outer pipes:
     - From the next click on, the table opens in the raw editor instead of the cell editor
       (P-E5 lost for that table).
     - Clearing the first cell moves the second value into the first column of the rendered table
       (content change).
   - **Fix:** at the end of `spliceRow`, after the loop, check the result and fall back to one
     canonical row. Keep the source line's indentation:

     ```ts
     const expected = newCells.map((cell) => escapeCellPipes(cell).trim());
     const actual = splitRow(result);
     if (actual.length === expected.length && actual.every((cell, index) => cell === expected[index])) {
       return result;
     }
     const indentation = line.slice(0, line.length - line.trimStart().length);
     return indentation + "| " + newCells.map(escapeCellPipes).join(" | ") + " |";
     ```

     This changes only that one line, so the one-line diff still holds. Record it in the report as
     a deliberate deviation: rows that cannot keep their style are rewritten canonically. I
     prototyped this change together with finding 2 on a copy of the compiled module:
     - all 31 current table tests pass;
     - the 359-case property check has 0 failures.
   - **Tests to add** in `test/webview/markdownTable.test.ts`:
     - `rows without outer pipes stay parseable when an edge cell is emptied`:
       - Source `"a | b\n--- | ---\nc | d"`.
       - `rows[2][0] = ""`: `tools.parse(output).rows[2]` deep-equals `["", "d"]`.
       - `rows[2][1] = ""`: it deep-equals `["c", ""]`.
       - Each case: `lineDelta` has exactly 1 removed and 1 added line.
     - `inserting a row into a table without outer pipes adds one parseable row`:
       - Same source, `insertRowAfter(table, 1)`.
       - `lineDelta(source, output)` deep-equals `{ removed: [], added: ["|  |  |"] }`.
       - `tools.parse(output).rows[3]` deep-equals `["", ""]`.
       - Repeat with `table.rows[3][0] = "n"` after the insert: the reparsed `rows[3]` is
         `["n", ""]`.
     - `rows with only one outer pipe stay parseable`:
       - Source `"| a | b\n| --- | ---\n| c | d"`, clear column 1: reparsed `rows[2]` is
         `["c", ""]`.
       - Source `"a | b |\n--- | --- |\nc | d |"`, clear column 0: reparsed `rows[2]` is
         `["", "d"]`.
       - Row+ on each source: `tools.parse(output)` is not `undefined`.
     - In `test/webview/markdownTablePreservation.test.ts`, add a generic safety test:
       - Loop over every corpus entry, every row except index 1, every column, and the values
         `""`, `"x"` and `"a|b"`.
       - Set the cell, then serialize.
       - `tools.parse(output)` must return rows equal to the edited model rows, with a typed `|`
         expected as `\|`.
       - `lineDelta` (after replacing `\r\n` with `\n` on both sides) must have 1 removed and
         1 added line, or 0 and 0 when the value equals the original cell.

2. **[MAJOR]** `src/webview/markdownTable.ts`, `spliceRow`: a whitespace-only segment is treated as
   all "leading whitespace". Filling an empty cell therefore right-aligns the value and grows the
   cell by 2 characters, which breaks the T04 padding rule "the segment keeps its original width".
   - Reproduction:
     - `| first    |          |`, set column 1 to `x` → `| first    |          x |`.
     - `| c |  |` (empty cells written by the old serializer; `book/chapters/05-skills.md:792` and
       `07-harness-engineering.md:193` contain such cells) → `| c |  x |`.
   - This is the normal path after Row+: the next edit session re-parses
     `|          |          |`, and typing `x` gives `|          x |          |`.
   - **Fix:** in `spliceRow`, compute `leading` as follows. Keep the trailing rule unchanged.

     ```ts
     const leading = text.trim() === ""
       ? (text.length > 0 ? " " : "")
       : (/^\s*/u.exec(text)?.[0] ?? "");
     ```

   - **Tests to add** in `test/webview/markdownTable.test.ts`, test name
     `filling an empty cell keeps the table's padding`:
     - `"| A        | B        |\n|----------|----------|\n| first    |          |"`, `rows[2][1] = "x"`.
       Expected delta: added `["| first    | x        |"]`.
     - Padded corpus table: `insertRowAfter(table, 1)`, serialize to `s1`, `tools.parse(s1)`, then
       `rows[3][0] = "x"`. Expected `lineDelta(s1, output)`:
       `{ removed: ["|          |          |"], added: ["| x        |          |"] }`.
     - `"| a | b |\n| --- | --- |\n| c |  |"`, `rows[2][1] = "x"`. Expected added line `| c | x |`.
     - `"|a|b|\n|---|---|\n|c||"`, `rows[2][1] = "x"`. Expected added line `|c|x|` (no-space
       style kept).

3. **[NIT]** `test/integration/realInput.test.ts`, `scenarioTableMinimalDiff`: when the buffer never
   matches, the failure is a bare timeout. A message that included `bufferText(document)` would
   make a future regression easier to read. Optional.

## Existing assertions changed

- `markdownTablePreservation.test.ts`: OK.
  - The `{ todo: entry.todo }` option was removed from the 2 corpus loops (16 test instances), and
    the unused `todo?` field was dropped.
  - "not yet implemented" was removed from the padding-rule comment.
  - All assertions are unchanged. The task allowed and required this.
- `markdownTable.test.ts`: additions only (the `lineDelta` import and 6 tests). OK.
- `realInput.test.ts`: additions only. The `withSmokeDocument` body moved into `withDocument` with
  identical behaviour. No assertion changed. OK.
- `scrollSync.test.ts`, `previewEditing.test.ts`: untouched. OK.

VERDICT: CHANGES REQUESTED
