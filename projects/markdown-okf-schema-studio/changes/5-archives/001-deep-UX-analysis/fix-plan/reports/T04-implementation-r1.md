# T04 implementation — round 1

STATUS: DONE

## Summary
- `serialize` now reuses the source line of every untouched row byte for byte. An edited row keeps
  everything outside the changed cells; only the edited cell's segment between its pipes is
  rewritten. The cell keeps its leading whitespace and fills the original width with trailing
  spaces (at least one).
- New rows take the style of the nearest preceding body row, then the first body row, then the
  header, and are padded to the table's own style.
- Column operations set `columnsChanged` and keep the canonical serialization. Row insert and delete
  keep `rowOrigins` in sync.
- `cellSegments` is exported on the tools object for direct unit tests. `spliceRow` stays internal.
- Model fields are optional, so hand-built models keep working. `parse` rejects non-tables exactly
  as before. Cell parsing, pipe escaping, delete guards and the toolbar are unchanged.

## Files changed
- `src/webview/markdownTable.ts` — optional source fields on the model;
  `cellSegments`, `spliceRow`; origin-aware `serialize`; origin sync in `insertRowAfter`/`deleteRow`;
  `columnsChanged` in column operations.
- `test/webview/markdownTablePreservation.test.ts` — removed the 8
  `todo: "UX-12 (T04)"` corpus entries and the `{ todo }` option (16 test usages); dropped the unused `todo?` field;
  removed "not yet implemented" from the padding-rule comment.
- `test/webview/markdownTable.test.ts` — six new tests and a
  `lineDelta` import.
- `test/integration/realInput.test.ts` — RI-T04 scenario, a shared
  `withDocument` helper (`withSmokeDocument` now delegates to it with the same content), a
  `TABLE_DOCUMENT` fixture and the scenario call in `run()`.

## Tests written first (failing before the fix)
- Unit (`logs/T04-impl-prefix-run.log`, 21 failing before the fix; the preservation tests and the new
  table tests): e.g. `round trip preserves the source: padded` — `actual '| Column A | Column B |\n| ---------- | ---------- |\n| first | second |'`;
  `one-cell edit changes exactly one line: wider-than-padding` — `2 !== 1`;
  `cellSegments …` — `TypeError: tools.cellSegments is not a function`;
  `a row inserted into a CRLF table keeps CRLF line endings` — actual `'| A | B |\r\n| --- | --- |\r\n| 1 | 2 |\r\n|  |  |\r\n'`.
- Trusted (`logs/T04-impl-prefail-trusted.log`): RI-T04 fails before the fix with
  `Timed out waiting for the padded table cell edit to reach the source buffer.` (the whole-table rewrite
  never produced `| first    | second X |`). The old `markdownTable.ts` was restored from HEAD only for this run.
  The run was done by hand because the gate stops at compile when the new tests reference `cellSegments`.
  `logs/T04-impl-prefail-build.log` has the build. The file was restored and compared with the saved copy.

## Tests added or changed
- `markdownTable.test.ts` — `cellSegments returns the text between the delimiting pipes…`: offsets for
  `| a | b |`, `|a|b|`, `a | b`, and `  | a \| b | \`x|y\` |`.
- `markdownTable.test.ts` — `inserting a row after the first body row of a padded table adds one padded line`: adds only `|          |          |`.
- `markdownTable.test.ts` — `a shrinking value in a padded table keeps the original cell width`: `| first    | s        |`.
- `markdownTable.test.ts` — `deleting the first body row of a compact table removes exactly one line`.
- `markdownTable.test.ts` — `inserting a column re-serializes the table with one more column`: reparses with 3 cells.
- `markdownTable.test.ts` — `a row inserted into a CRLF table keeps CRLF line endings`.
- `markdownTablePreservation.test.ts` — the existing 18 corpus tests (round trip and one-cell edit, 9 entries each), now
  active (todo removed). All pass.
- `realInput.test.ts` — RI-T04 `scenarioTableMinimalDiff`: click `second`, End, ` X`, Enter; `lineDelta`
  must be exactly one removed and one added line (`| first    | second   |` → `| first    | second X |`).
  Then click `Ana`, End, ` Lee`, Enter; `lineDelta` against the state before it must be
  `| Plan | Ana |` → `| Plan | Ana Lee |`. Each step waits for the source buffer and the final render
  (`waitForRender`) and for the cell editor to close.

## Existing assertions changed
- None. `scrollSync.test.ts` and `previewEditing.test.ts` needed no change, and their table
  expectations already match the source style.

## Verification
- `scripts/gate.sh T04-impl unit` → PASS (349 pass, 0 fail; `logs/T04-impl-unit.log`)
- `scripts/gate.sh T04-impl unit trusted` → PASS (`logs/T04-impl-trusted.log`; RI-T04 passed,
  `PASS real-input` ordering 01–04, 06, 07, 05; no `Frame was detached` failure in this run)

## Evidence for reviewers
- Screenshots / notes: `.artifacts/real-input-JZRxpE/`
  - `06-table-padded-edit.png` / `.md` — padded table after the edit; buffer excerpt shows `| first    | second X |`.
  - `07-table-compact-edit.png` / `.md` — compact table after the edit; buffer excerpt shows `| Plan | Ana Lee |`, delimiter `|---|---|` unchanged.
- The gate logs are in `PLAN/logs/T04-impl-*.log`.

## Feedback addressed (rounds 2–3)
- None (round 1).

## Open points / STOP reason
- Deviation, defensive: `serialize` takes the canonical path when `sourceLines`, `sourceRows` or
  `rowOrigins` is missing, not only when `sourceLines` is missing or `columnsChanged` is true. Models from
  `parse` always carry all three, so behaviour is unchanged. Say if the reviewer wants the strict guard.
- Deviation in the template lookup, to match "never the delimiter row; first body row, else header": the
  search for a template row covers body rows only (index ≥ 2). The header is used only when no body row exists.
- The two RI-T04 captures are taken mid-scenario, while the harness doc asks for captures after the last
  action. The padded capture is taken before the second edit. Scroll and hover state held up in the run,
  but the reviewer should check the padded capture.
- `realInput.test.ts` `withSmokeDocument` now delegates to a new `withDocument` helper. Its behaviour is
  unchanged (same content, same cleanup).
- No `Frame was detached` flake occurred in these runs.
