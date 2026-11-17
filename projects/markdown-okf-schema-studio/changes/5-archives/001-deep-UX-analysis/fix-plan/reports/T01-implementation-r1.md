# T01-impl implementation — round 1

STATUS: DONE

## Summary
Added the formatting-preservation corpus for tables and frontmatter (QA-01), plus the `lineDelta`
helper. No file under `src/` changed. Before adding any `todo` marker, the new tests were run and
every failing test was recorded. Only those failing tests carry a marker. The `unit` gate passes:
321 pass, 0 fail, 34 todo. The 34 todo tests are the T04, T05 and T06 targets. The corpus
confirms the findings: every table edit that touches a non-canonical source and every frontmatter
value and structural edit in the task's list fails today.

## Files changed
- `test/shared/lineDelta.ts` (new) — `lineDelta(before, after)`: splits on `\n`, trims the common
  prefix and then the common suffix without overlap, returns `{ removed, added }`.
- `test/webview/markdownTablePreservation.test.ts` (new) — 3 `lineDelta` tests, then the 9-entry
  table corpus with a round-trip test and a one-cell-edit test per entry. Padding rule kept as a
  comment (T04 contract).
- `test/frontmatter/frontmatterPreservation.test.ts` (new) — fixtures F1–F4, 14 value-edit tests
  compared on the full resulting text, 4 structural tests, 1 comment-preservation test.

## Tests written first (failing before the fix)
Run on the untouched `src/` tree, with no markers. Raw output: `logs/T01-tap.txt`.

Table, round trip (UX-12, T04):
- round trip preserves the source: compact-book — `serialize` gives `| Step | Owner |` / `| --- | --- |`, the delimiter is rewritten
- round trip preserves the source: padded — `| ---------- | ---------- |`, the cell padding is collapsed to `| first | second |`
- round trip preserves the source: no-spaces — `|a|b|` becomes `| a | b |`
- round trip preserves the source: no-outer-pipes — `a | b` becomes `| a | b |`
- round trip preserves the source: escaped-and-code — delimiter `|---|---|---|` rewritten to `| --- | --- | --- |`
- round trip preserves the source: indented — leading indentation dropped
- round trip preserves the source: crlf — delimiter rewritten
- round trip preserves the source: wider-than-padding — padding collapsed

Table, one-cell edit (UX-12, T04):
- one-cell edit changes exactly one line: compact-book — `expected: 1`, `actual: 2` (the delimiter line also changes)
- one-cell edit changes exactly one line: padded — `expected: 1`, `actual: 2`
- one-cell edit changes exactly one line: no-spaces — `expected: 1`, `actual: 3`
- one-cell edit changes exactly one line: no-outer-pipes — `expected: 1`, `actual: 3`
- one-cell edit changes exactly one line: escaped-and-code — `expected: 1`, `actual: 3`
- one-cell edit changes exactly one line: indented — `expected: 1`, `actual: 3`
- one-cell edit changes exactly one line: crlf — `expected: 1`, `actual: 3`
- one-cell edit changes exactly one line: wider-than-padding — `expected: 1`, `actual: 2`

Frontmatter, value edits (UX-16, T05). Each one reserializes the whole block:
- value edit F1 title — `description` folded scalar joined into one line; `- StRS-CORE-001` re-indented to `  - StRS-CORE-001`
- value edit F1 lifecycle — same reflow and re-indent as above
- value edit F1 annotation_exemption — same
- value edit F1 exemption_reason — same
- value edit F1 derives_from — re-indented sequence; `  - StRS-CORE-002` added with the wrong indent
- value edit F1 derived_by — same reflow and re-indent
- value edit F2 title — `title: Alpha  # trailing comment` becomes `title: Alpha # trailing comment` (comment spacing collapsed); `links: [a.md, b.md]` becomes `links: [ a.md, b.md ]`; folded `summary` text joined
- value edit F2 tags — comment spacing and flow-sequence spacing changed; folded `summary` joined
- value edit F2 links — comment spacing and flow-sequence spacing changed; folded `summary` joined
- value edit F2 quoted — same
- value edit F2 summary — `summary: >-` replaced by `summary: New summary` (the folded block style is lost); comment spacing changed
- value edit F2 status — comment spacing and flow-sequence spacing changed; folded `summary` joined
- value edit F3 title — CRLF kept, but the same description reflow and re-indent as F1
- value edit F4 status — same as F2 status (`...` closing is kept)

Frontmatter, structural (UX-16, T06):
- structural F2 rename title to heading keeps the trailing comment — comment spacing collapsed, folded `summary` joined, flow sequence spacing changed
- structural F2 remove links deletes exactly that line — the `summary` reflow also appears in the output (`  spans lines.` is lost into the joined line)
- structural F2 remove tags deletes exactly the sequence lines — comment spacing and flow spacing changed, folded `summary` joined
- structural F1 add owner appends one line before the closing delimiter — description reflow and sequence re-indent

Not marked (passes today): structural F2 edits keep both comments unless their own line is
removed. The comments survive all five operations, so this test is a guard, not a failing target.

## Tests added or changed
- `lineDelta` identical input — no removed or added lines
- `lineDelta` one changed line — one removed, one added
- `lineDelta` one inserted line — one added
- round trip preserves the source (9 entries) — `serialize(parse(source)) === source`
- one-cell edit changes exactly one line (9 entries) — `lineDelta` gives 1 removed, 1 added, and the expected added line
- value edit F1/F2/F3/F4 (14 rows) — `createFrontmatterFieldPatch` result equals the full expected document
- structural F2 rename, F2 remove links, F2 remove tags, F1 add owner — `createFrontmatterFieldRenamePatch` / `createFrontmatterFieldRemovePatch` / `createFrontmatterFieldPatch` on the full document
- structural F2 comments survive — both comment lines present after 5 operations (passes today)

## Todo markers (every test that fails today, and nothing else)
- `UX-12 (T04)`: round trip and one-cell edit for compact-book, padded, no-spaces, no-outer-pipes, escaped-and-code, indented, crlf, wider-than-padding (16 tests).
- `UX-16 (T05)`: all 14 value-edit tests.
- `UX-16 (T06)`: the 4 structural tests (rename, remove links, remove tags, add owner).
- Not marked: `alignment` round trip and one-cell edit (both pass today), the 3 `lineDelta` tests, and the comment-preservation test.

Total todo: 34. Total pass: 321 in the full `unit` run.

Note for T04: the failing one-cell tests fail on the delimiter line before padding comes into play.
The delimiter is rewritten to `| --- |`. Fixing the delimiter alone (keeping the source's own
delimiter cells) may clear several of them, so do not treat the padding rule as the only root cause.

## Existing assertions changed
None.

## Verification
- `scripts/gate.sh T01-impl unit` → PASS (compile PASS, unit PASS; `logs/T01-impl-unit.log`)
- `node --test --test-reporter=tap` on the two new corpus files → 40 tests, 6 pass, 0 fail, 34 todo (`logs/T01-tap.txt` is the pre-marker run)

## Evidence for reviewers
- Failure output before markers: `logs/T01-tap.txt`
- Gate logs: `logs/T01-impl-compile.log`, `logs/T01-impl-unit.log`

## Feedback addressed (rounds 2–3)
Not applicable (round 1).

## Open points / STOP reason
- Nothing blocking. No file outside the Allowed files was touched; `git status` shows only the three new test files plus `test/shared/` (the `M` entries under `book/` and `.agents/thinking/` were already present before this task).
- Nothing committed, staged, or pushed.
