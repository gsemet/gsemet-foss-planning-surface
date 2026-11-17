# T06 review — round 2

Base: b3ee36dc8e4e0c608feabd9060a7cfd86a372ba1 · Reviewed diff: 4 files, +587/-64

The same four files as round 1 changed, and all of them are in **Allowed files**:
- `src/frontmatter/okfFrontmatter.ts`;
- `test/frontmatter/frontmatterPreservation.test.ts`;
- `test/frontmatter/okfFrontmatter.test.ts`;
- `test/integration/realInput.test.ts`.

There is no unrelated churn, and the frozen areas (UX-22, UX-24, UX-34) are untouched.

**Round-2 source delta.** I diffed the round-1 source snapshot from my round-1 scratch against the current file. The
only changes are these three, exactly as round 1 specified:
- the new helper `fieldEndWithTrailingComments`, verbatim;
- in `minimalAddPatch`, `offset = fieldEndWithTrailingComments(text, anchor, region.end)`;
- in `verified`, `|| !isMap(check.contents)`, with `?? {}` dropped.

`realInput.test.ts` changes only the comment above the existing 300 ms pause.

## Gates
- compile: PASS (`logs/T06-r2-compile.log`; my rerun `logs/T06-review-r2-compile.log`).
- unit: PASS, 413 tests, 413 pass, 0 fail, 0 todo (`logs/T06-r2-unit.log`; my rerun
  `logs/T06-review-r2-unit.log`). That is 406 from round 1 plus 7 new tests. Every round-1 test name is still
  present, so nothing was removed.
- types: PASS (`logs/T06-r2-types.log`, `logs/T06-review-r2-types.log`).
- trusted: PASS, exit 0 (`logs/T06-r2-trusted.log`). It includes `PASS real-input screenshot:
  09-frontmatter-rename-minimal-patch` and `10-frontmatter-remove-minimal-patch`. The `CodeWindow: failed to load`
  lines are known test-host noise.
- Compared with the T00 baseline, there is no new failure.

## Done-when
- [x] The `unit` and `trusted` gates pass. Evidence: the logs above.
- [x] No T01 todo marker remains. `grep "UX-16 (T06)"` finds nothing. The only deleted test lines from the base
  are the 4 `{ todo: "UX-16 (T06)" }` headers.
- [x] RI-T06 shows one-line or field-only diffs. I opened `.artifacts/real-input-NxjzAD/09-…png` and
  `10-…png` from the orchestrator's r2 run:
  - in 09, the buffer has `abstract:` with `  as CSV.` untouched;
  - in 10, exactly `tags:`, `- alpha` and `- beta` are gone, and the compact `- StRS-CORE-001` is unchanged;
  - in both, the table matches the buffer.
- [x] Goal: "rename, remove and add touch only the lines of the field concerned" with P-E7. Both round-1
  regressions are fixed (see below).

## Round-1 findings: verification

1. **BLOCKER 1 (add with `afterField` moved the anchor's comments): FIXED.**
   - **Tests.** The four requested tests are present, assert the full output, and check `positioned === true`:
     - list, LF and CRLF;
     - nested map;
     - multi-line value;
     - column-0 guard.
   - **The tests fail without the fix.** `logs/T06-impl-r2-prefix-unit.log` shows 4 failures with the round-1
     symptoms (`owner: Ana` above `# - b`, and `positioned` false). I reproduced this independently. In a
     scratch copy of `out/`, I reverted only the offset line to `region.end`. Exactly those 4 tests fail, and
     the column-0 guard passes, as designed.
   - **Sibling probe.** I ran 49 hand-written anchor shapes × LF/CRLF × 6 values (`"Ana"`, `"multi\nline"`,
     a list, a map, `null`, `""`), 588 adds against the compiled `out/`. For each one I checked:
     - the data;
     - the key order;
     - `positioned`;
     - CRLF purity;
     - yaml comment attachment of every existing field.

     Every shape below inserts after the anchor's own comments, with no comment byte moved:
     - plain, quoted and multi-line scalars, including indented comments after them and blank lines between
       comments;
     - block scalars (`|`, `>-`, `|+` with a blank line, a header comment, a `#` content line);
     - indented and compact sequences (inner, trailing, deep and tab comments);
     - sequences of maps, nested sequences, nested maps with deep trailing comments, flow collections;
     - empty values followed by an indented or column-0 comment;
     - the first field after a leading comment;
     - the last field before `---` and before `...`;
     - quoted keys and `key :` keys.

     Column-0 comments stay with the next field.
   - **Fuzz.** I re-ran the round-1 fuzz (4 seeds × 1,500 documents × LF/CRLF). Before the fix it reported
     about 4,700 comment-moving `afterField` adds per seed. Now it reports 96 per seed, and all of them are
     the benign case already accepted in round 1: yaml re-attributes the column-0 comments that follow an empty
     last value, while the bytes stay in place. The no-`afterField` adds show the same 48 per seed, identical
     to round 1.
2. **BLOCKER 2 (removing the only field gave `null`): FIXED.**
   - **Tests.** `removing the only field leaves a valid empty mapping` and its CRLF variant assert:
     - `"---\n{}\n---\nBody\n"` and `"---\r\n{}\r\n---\r\nBody\r\n"`;
     - `extractFrontmatter(updated).error === undefined`;
     - `frontmatter` deep-equals `{}`.
   - **The tests fail without the fix.** The prefix log shows `'---\n\n---\nBody\n'`. I reproduced this
     independently by restoring `?? {}` and dropping `isMap` in a scratch copy: exactly these 2 tests fail.
   - **Sibling probe.** I ran 34 removal cases × LF/CRLF against `out/` and base (b3ee36d, bundled with
     esbuild):
     - **Only field.** Plain, with `...`, comment above, comment below, trailing comment, indented trailing
       comment, sequence, block scalar, blank lines, empty value, flow map: all give a valid `{}`,
       byte-identical to base.
     - **First field.** With a leading comment and with a blank line before: the comment and the blank line
       are kept.
     - **Last field.** Before `---` and before `...`, after a blank line, with a column-0 or indented comment
       after it, and after a compact sequence: the data is correct, and the compact sequence keeps its style.
     - **CRLF.** All outputs have clean CRLF breaks.
   - **Value edits.** The `isMap` check changes no value edit: the fuzz reports 0 value patches that differ
     from base, about 68,000 per seed. Rename: 0 problems. A follow-up add on the resulting `{}` behaves as
     on base.
3. **MINOR 5 (CRLF tests could not tell the minimal path from the fallback): FIXED.**
   - Both tests now include the compact-sequence assertions as specified.
   - Mutation check: the `start -= 1` mutant now fails `structural CRLF remove of the last field drops the
     preceding break`.
   - A `"\n" + body` insertion mutant fails 3 CRLF add tests.
4. **NIT 6: FIXED.** The RI-T06 comment names the cause: the workbench echoes `selectAll` asynchronously.
5. **NIT 7: FIXED.** The report gives 12/10 for round 1 and 7 new tests for round 2.

MINORs 3 and 4 are unchanged, as agreed (follow-ups).

## Protected features checked
- **P-E7** (frontmatter editing, YAML comments preserved): covered by the T01 corpus (todo markers removed), the
  round-1 structural tests, and the 7 new tests. My probes and fuzz show no comment byte moved or lost by a
  minimal patch. Only fallback paths drop comments, and those are byte-identical to base.
- **P-E6** (stale versions; required-field removal guard): `handleFrontmatterSave` is unchanged.
  `integration-required-status-remove` passes in the trusted run.
- **P-R7 / UX-24** (properties-table display): `propertiesTable.ts` is untouched. Screenshots 09 and 10 show a
  correct table.
- **P-S2, P-S4, P-E8**: no change to the message protocol, the webview, or edit entry points.
- **Conventions §5** (CRLF must not get worse): every CRLF output in the probes and the fuzz has only `\r\n`
  breaks.

## Findings
None blocking. Follow-ups for the orchestrator's `followups.md` (all MINOR, none caused by round-2 code):

1. **[MINOR] (follow-up) `minimalAddPatch` with `afterField` after a block scalar followed by a less-indented
   comment.**
   - Example: `d: |\n    l1\n  # less\nstatus: x`. yaml attaches `# less` to `status`, so the new field goes
     before it, and the comment then attaches to the new field.
   - No byte moves, and the comment stays directly above `status`.
   - With a multi-line value in this case, verification rejects the candidate, and the add falls back to
     base's append with `positioned: false`. The same happens after a tab-indented comment.
   - This is unchanged since round 1 and very rare.
2. **[MINOR] (follow-up, identical to base) Removing the only field.** It goes through the whole-document
   fallback, so a comment line above that key is dropped: `"---\n# about\ntitle: x\n---\n"` gives
   `"---\n{}\n---\n"`. A later improvement could write `{}` in place of the field lines and keep the
   surrounding comments.
3. **[MINOR] (follow-up, identical to base) Removing the last field after a `|+` block scalar.** The fallback
   drops the scalar's trailing blank line: `status` changes from `"…\n\n"` to `"…\n"`. Example:
   `d: |+\n  l1\n\nstatus: y`. The fuzz finds 6–8 such cases per seed, all byte-identical to base.

## Existing assertions changed
- `frontmatterPreservation.test.ts`: OK.
  - Against the base, only the 4 `{ todo: "UX-16 (T06)" }` options are removed, as the task requires.
  - In round 2, two round-1 T06 tests gained extra assertions. No assertion was weakened.
- `okfFrontmatter.test.ts`: OK. Tests were added only; it is unchanged since round 1.
- `realInput.test.ts`: OK. Round 2 changes only the comment text.
- `previewEditing.test.ts`: unchanged, and it passes in the trusted run.

VERDICT: PASS
