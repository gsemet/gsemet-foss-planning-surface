# T04 review — round 2

Base: ce5784ed5251957a865b8f31771f888d89591ccc · Reviewed diff: 4 files, +428/-18

Round 2 changes `spliceRow` in `src/webview/markdownTable.ts` and adds tests to
`test/webview/markdownTable.test.ts` and `test/webview/markdownTablePreservation.test.ts`.
`test/integration/realInput.test.ts` is unchanged since round 1. All four files are in
**Allowed files**. `scrollSync.ts`, `scrollSync.test.ts` and `previewEditing.test.ts` are untouched.

## Gates

- compile: PASS (`logs/T04-r2-compile.log`).
- unit: PASS. 380 tests: 362 pass, 0 fail, 18 todo (`logs/T04-r2-unit.log`).
  - The 18 `todo` markers are the T05 and T06 frontmatter markers.
  - `rg "UX-12" src test` finds nothing.
  - I reran `npm test` and got the same numbers. The contracts pass (2/2).
- trusted: PASS, exit 0 (`logs/T04-r2-trusted.log`).
  - Real-input order: 01–04, 06, 07, 05, all PASS.
  - No `Frame was detached` error.
  - The bundle (`out/bundle/extension.js`, 20:10:38) is newer than `markdownTable.ts` (20:09:10). It
    contains the minified fallback.
- T00 baseline: the unit and trusted baselines were clean, and there is no new failure.

## Round-1 findings: verification

### Finding 1 (BLOCKER): fixed

`spliceRow` now checks the spliced row. It compares `splitRow(result)` with
`newCells.map(c => escapeCellPipes(c).trim())`. On a mismatch it returns
`indentation + "| " + cells.join(" | ") + " |"`, which is the review's specified fix.

Tests fail without the fix. I copied the compiled module and tests to the scratchpad, outside the
repository, and removed only the fallback:

- 4 tests fail:
  - `rows without outer pipes stay parseable when an edge cell is emptied`
  - `inserting a row into a table without outer pipes adds one parseable row`
  - `rows with only one outer pipe stay parseable`
  - `every single-cell edit reparses and changes at most one line: no-outer-pipes`
- With both fixes removed (the round-1 code), the same 4 tests and the finding-2 test fail. That
  makes 5 failures, which matches the report's list exactly.

### Finding 2 (MAJOR): fixed

A whitespace-only segment now uses `" "` as its leading whitespace, or `""` when the segment is
empty. The trailing rule is unchanged.

The test fails without the fix: with only the old `leading` rule restored, exactly
`filling an empty cell keeps the table's padding` fails.

All four cases from the review are present, with the exact expected lines:

- `| first    | x        |`
- `| x        |          |` (Row+, then re-parse)
- `| c | x |`
- `|c|x|`

### Sibling cases of the same bug class

I checked `spliceRow` and `serialize` with a property check on the compiled module.

- **Scope:** 6,642 cases over 18 table styles.
  - Styles: compact, padded, no-spaces with an empty cell, alignment, no outer pipes, leading pipe
    only, trailing pipe only, escaped pipe and code span, indented, indented without outer pipes,
    CRLF, empty cells in the old style, trailing whitespace after the last pipe, tabs, a backslash
    inside a cell, header only, double-backtick code, Unicode.
  - Values: `""`, `x`, `a|b`, whitespace, `C:\`, `\`, unbalanced and balanced backticks, `` `a|b` ``,
    `a\|b`, a bare `|`, `x |`, `| x`, emoji, tab, `---`, `:---:`, and others.
  - Operations: every cell; Row+ at every position, with each cell then filled; two stacked Row+; a
    second session after Row+ (re-parse, then edit); Row− at every position; Col+ and Col− at every
    column; the unchanged round trip.
- **Oracle:** the base serializer, which is the same function with `sourceLines` removed.
- **Results:**
  - **0** cases where `parse(output)` fails but the base output parses.
  - **0** cases where the reparsed cells differ from the base.
  - Every edit changes at most one line, and Row+ adds exactly one line.
  - The only line-count differences are 56 cases where `" "` is written into an already-empty cell.
    The output is unchanged there, which is correct: the trimmed value is the same.
  - Column operations are byte-identical to the base.
- **Without the fallback,** the check finds a sibling case the round-1 review did not list. In the
  no-spaces style, a value ending in a backslash breaks the row:
  - `|C:\|b|` merges two cells (485 regressions).
  - In the last cell, `|f||C:\|` changes the cell content (18 cases).
  - The fallback rewrites these rows to `| C:\ | b |`, which parses correctly. They are covered now,
    but no test pins them. See finding 2 below.
- **Where the fallback fires:** I compared against a no-fallback copy. With normal values (`x`,
  `""`, `a|b`, Markdown inline syntax, emoji) in tables with outer pipes, the fallback never fires.
  The minimal splice is kept. It fires only for empty edge cells and for Row+ in tables without
  outer pipes.
- **Rendering:** I checked the fallback rows with `markdown_it` (commonmark + table) in the
  repository venv. Mixed rows render the right cells:
  - `|  | d` → `['', 'd']`
  - `| c |  |` → `['c', '']`
  - `|  |  |` → `['', '']`
  - an indented row
  - a header row with an empty first cell

  The content no longer shifts between columns.
- **Same as base:** two inputs still break the table, but identically to the base serializer:
  - a value with an unbalanced backtick, such as `` `x ``;
  - a value with an embedded newline, which a paste into the cell `<textarea>` can produce.

  They are not T04 regressions. See the follow-ups.

## Done-when

- [x] The `unit` and `trusted` gates pass, and the T01 table todos are gone. Evidence: the logs
  above and `rg "UX-12"`.
- [x] RI-T04 passes, and its two captures show the edited tables.
  - Evidence: `.artifacts/real-input-J2ytM9/06-table-padded-edit.png` and
    `07-table-compact-edit.png`, from the orchestrator's r2 trusted run. I opened both.
  - 06: the buffer line 5 is `| first    | second X |`, with the padding kept, and the rendered
    cell is `second X`.
  - 07: the buffer line 11 is `| Plan | Ana Lee |`, and `|---|---|` is untouched. The rendered cell
    is `Ana Lee`.
  - Neither capture shows an open cell editor or an overlay.
- [x] One changed line per edit in the RI-T04 fixture. Evidence: the `assert.deepEqual(lineDelta(…))`
  checks in `scenarioTableMinimalDiff`.
- [x] Goal: "untouched rows byte for byte; in an edited row only the edited cell's segment changes".
  - This holds for every table with outer pipes, as the generic corpus test and my property check
    show.
  - The deliberate deviation for rows that cannot keep their style was specified by the round-1
    review and is recorded in the report. It is a canonical rewrite of that one row only.

## Protected features checked

- **P-E5 (table cell editor):** covered.
  - One cell edit changes one line. Row and column insert and delete work.
  - The header and last-body-row guards are unchanged: `deleteRow` is as reviewed in round 1.
  - Switching cells keeps changes: `serialize` does not mutate the model, and `rowOrigins` persists
    for the session.
  - Coverage:
    - `markdownTable.test.ts` (16 tests)
    - `markdownTablePreservation.test.ts` (corpus round trip, one-cell edit, and the new
      every-cell safety net over 9 corpus entries)
    - the `scrollSync.test.ts` table tests, unchanged and passing
    - RI-T04 and RI scenario 04 in the trusted gate
  - The round-1 regression, where a table falls back to the raw editor after an edit, is gone: every
    output parses whenever the base output parses.
- **P-R1 (rendering):** the fallback rows render the right cells (markdown-it check above). The
  contracts pass.
- **P-E3:** the raw editor path is unchanged (`postBlockEditSave` non-table branch).
- **P-E6:** host checks are unchanged. An unchanged model still serializes to exactly
  `originalText`, so Enter without a change closes the editor without a save.
- **P-E8, P-S2, P-S4:** there is no new interactive surface, message type, field, or `innerHTML`.
- **Conventions §3 (injected factory):** the new code in `spliceRow` uses only factory-local helpers
  (`splitRow`, `escapeCellPipes`, `cellSegments`).
  - The template literal in the fallback reaches the runtime through the
    `${createMarkdownTableTools.toString()}` substitution, as the existing canonical serializer
    already does, so §2 does not apply.
  - The minified bundle contains it as expected.
  - The vm-evaluated `scrollSync.test.ts` suite passes, and the trusted run passes against the
    bundle.
- **Frozen behaviour (UX-22, UX-24, UX-34):** not touched.

## Findings

1. **[MINOR]** `.agents/…/fix-plan/reports/T04-implementation-r2.md`: the pre-fail evidence log the
   report cites, `logs/T04-impl-r2-prefix-unit.log`, does not exist. Only the excerpts in the
   report remain.
   - I reproduced the failures independently (see "Round-1 findings: verification"), so this does
     not block.
   - Fix for future tasks: keep the pre-fail gate log under the name the report cites.
2. **[MINOR]** `test/webview/markdownTablePreservation.test.ts`, the
   `every single-cell edit reparses and changes at most one line` loop: the sibling case "value
   ending in a backslash in the no-spaces style" is protected only by the generic fallback. No test
   pins it.
   - Fix: add `"C:\\"` to the values array `["", "x", "a|b"]`. The `expected` mapping needs no change
     because the value contains no `|`.
   - Without the fallback, the `no-spaces` entry would then fail for this value.
3. **[NIT]** `src/webview/markdownTable.ts`, `spliceRow`: a whitespace-only segment that starts with
   a tab gets a space as its leading whitespace. This has no visible effect on the rendering.
4. **[NIT]** (carried over from round 1, optional) `test/integration/realInput.test.ts`,
   `scenarioTableMinimalDiff`: a buffer mismatch still reports a bare timeout.

## Follow-ups (pre-existing, not caused by T04, same output as the base serializer)

- A cell value with an unbalanced backtick, such as `` `x ``, makes `splitRow` treat the next pipe
  as part of a code span. `escapeCellPipes` does not escape that pipe either. The table then stops
  parsing and opens in the raw editor. GFM treats an unbalanced backtick as a literal.
- A multi-line paste into the cell `<textarea>` puts a newline into the cell and splits the row.
  The cell editor could replace newlines (with a space or `<br>`) before storing the value.

## Existing assertions changed

- `markdownTablePreservation.test.ts`: OK.
  - Round 1 removed the `todo` markers and the unused `todo?` field, as the task required.
  - Round 2 only appends the generic test and adds the type annotation `const unchanged: boolean`.
  - No other line was removed.
- `markdownTable.test.ts`: additions only. `git diff` shows no removed lines. OK.
- `realInput.test.ts`: unchanged since round 1, which was additions only plus the
  behaviour-identical `withDocument` extraction. OK.
- `scrollSync.test.ts`, `previewEditing.test.ts`: untouched. OK.

VERDICT: PASS
