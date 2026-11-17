# T04 implementation — round 2

STATUS: DONE

## Summary
- Fixed review finding 1 (BLOCKER): `spliceRow` now verifies its result. When the spliced row no
  longer splits into the new cells (rows without outer pipes, or with only one, after an edge cell
  is emptied), the row is rewritten canonically (`| a | b |`), keeping the source line's indentation.
  This is a deliberate deviation: such rows lose their original style rather than becoming
  unparseable.
- Fixed review finding 2 (MAJOR): a whitespace-only segment keeps one leading space, so filling an
  empty cell is no longer right-aligned and the padded width is kept.
- Added every test the review asked for, written first and shown failing. The generic corpus safety
  test was also added. Existing assertions are unchanged.

## Files changed
- `src/webview/markdownTable.ts` — `spliceRow`: leading-whitespace
  rule for whitespace-only segments; post-splice verification with canonical fallback.
- `test/webview/markdownTable.test.ts` — four new tests (appended).
- `test/webview/markdownTablePreservation.test.ts` — one generic
  test per corpus entry (appended); one type annotation (`const unchanged: boolean`) so that
  `tsc` compiles.

## Tests written first (failing before the fix)
Gate `T04-impl-r2-prefix` (log `logs/T04-impl-r2-prefix-unit.log`): 5 failing, 357 pass, 18 todo.
- `rows without outer pipes stay parseable when an edge cell is emptied` — `assert.ok(reparsedFirst)`
  falsy (the row no longer parses).
- `inserting a row into a table without outer pipes adds one parseable row` — actual added
  `'  | '`, expected `'|  |  |'`.
- `rows with only one outer pipe stay parseable` — `assert.ok(leadingReparsed)` falsy.
- `filling an empty cell keeps the table's padding` — actual added `'| first    |          x |'`,
  expected `'| first    | x        |'`.
- `every single-cell edit reparses and changes at most one line: no-outer-pipes` —
  `0,0,"" is not a table`.

## Tests added or changed
- `markdownTable.test.ts` — `rows without outer pipes stay parseable when an edge cell is emptied`:
  `a | b / --- | --- / c | d`, first and last cells cleared; reparse gives `["", "d"]` and `["c", ""]`,
  one removed and one added line each.
- `markdownTable.test.ts` — `inserting a row into a table without outer pipes adds one parseable row`:
  adds exactly `|  |  |`; reparsed `["", ""]`; after `rows[3][0] = "n"`, reparsed `["n", ""]`.
- `markdownTable.test.ts` — `rows with only one outer pipe stay parseable`: leading-pipe-only and
  trailing-pipe-only sources, cleared edge cell reparses; Row+ reparses.
- `markdownTable.test.ts` — `filling an empty cell keeps the table's padding`: padded `|          |`
  filled with `x` gives `| first    | x        |`; inserted padded row filled with `x` gives
  `| x        |          |`; `| c |  |` gives `| c | x |`; `|c||` gives `|c|x|`.
- `markdownTablePreservation.test.ts` — `every single-cell edit reparses and changes at most one
  line: <entry>` (one per corpus entry, 9 total): every row except index 1, every column, values
  `""`, `"x"`, `"a|b"`; the reparsed rows equal the edited model (with `|` written as `\|`); the
  line delta (CRLF normalized) is one removed and one added line, or none when the value is unchanged.

## Existing assertions changed
- None in this round. Round 1 changes (todo markers removed) are unchanged.

## Verification
- `scripts/gate.sh T04-impl-r2 unit` → PASS (380 tests, 362 pass, 0 fail, 18 todo; `logs/T04-impl-r2-unit.log`)
- `scripts/gate.sh T04-impl-r2 trusted` → PASS, exit 0 (`logs/T04-impl-r2-trusted.log`). Real-input
  order 01–04, 06, 07, 05 all PASS. No `Frame was detached` failure. The `CodeWindow: failed to load`
  lines also appear in the round 1 trusted log, so they are not new.

## Evidence for reviewers
- RI-T04 captures (from this run, `.artifacts/real-input-w75hsX/`):
  `06-table-padded-edit.png` / `.md` (buffer: `| first    | second X |`, padding kept) and
  `07-table-compact-edit.png` / `.md` (buffer: `| Plan | Ana Lee |`, delimiter `|---|---|` unchanged).

## Feedback addressed (rounds 2–3)
- Finding 1 (BLOCKER): `spliceRow` checks that `splitRow(result)` equals the new cells (trimmed,
  pipes escaped). If not, it returns `indentation + "| " + cells joined by " | " + " |"`. The five
  finding-1 tests were added and shown failing before the fix; all pass now. The generic corpus
  safety test covers every cell of every corpus table.
- Finding 2 (MAJOR): a whitespace-only segment uses `" "` as its leading whitespace (empty segment:
  `""`). The trailing-width rule is unchanged. The four finding-2 cases are in
  `filling an empty cell keeps the table's padding`; all pass now.
- Finding 3 (NIT, optional): not done. `scenarioTableMinimalDiff` still reports a bare timeout.

## Open points / STOP reason
- Finding 1 fallback changes the style of a row that cannot keep its own style (rewritten as
  `| … |`). Only that row changes, and the one-line diff still holds. This is the fix the review
  specified.
- The fallback template literal in `spliceRow` is a runtime value inside the factory's
  `.toString()` text, so it does not touch the §2 template rules. The existing `serialize` already
  uses the same form.
- The NIT (realInput failure message) was left out.
