# T06 implementation — round 2

STATUS: DONE

## Summary
- BLOCKER 1 fixed: `afterField` now inserts after the anchor field's trailing comment lines. A new helper
  `fieldEndWithTrailingComments` extends the insertion point over the indented `#` lines that yaml
  attaches to the value (those before `range[2]`). `minimalAddPatch` uses it; the rename and remove paths do not.
- BLOCKER 2 fixed: `verified` rejects any candidate whose root is not a mapping (`!isMap(check.contents)`), and the
  `?? {}` fallback is removed. Removing the only field now fails minimal verification and falls back to the
  whole-document patch, which writes `{}` as base did.
- MINOR 5 fixed: the two CRLF tests (`structural CRLF add at the end ...`, `structural CRLF remove of the last field ...`)
  each have an extra compact-sequence case (`- a` stays unindented), which only the minimal path keeps.
- NIT 6 fixed: the RI-T06 comment now states the cause (Cmd/Ctrl+A is echoed by the workbench asynchronously).
- NIT 7: round-1 report counts were wrong. Round 1 added 12 new tests (2 in `okfFrontmatter.test.ts`, 10 in
  `frontmatterPreservation.test.ts`), not 13 and 11. The 13 was the pre-fix failure count. Round 2 adds 7 tests (see below).
- MINORs 3 and 4 are unchanged, as instructed (follow-ups).

## Files changed
- `src/frontmatter/okfFrontmatter.ts` — `fieldEndWithTrailingComments` (new);
  `minimalAddPatch` uses it for the anchor offset; `verified` requires a mapping root and drops `?? {}`.
- `test/frontmatter/frontmatterPreservation.test.ts` — `extractFrontmatter` imported;
  7 tests added; 2 compact-sequence assertions added to the round-1 CRLF tests.
- `test/integration/realInput.test.ts` — comment text of the RI-T06 pause only.

## Tests written first (failing before the fix)
Pre-fix run: round-1 code plus the new tests, `scripts/gate.sh T06-impl-r2-prefix unit`, log
`logs/T06-impl-r2-prefix-unit.log`: 413 tests, 407 pass, 6 fail.
- `add after a list keeps its commented-out item above the new field` — actual
  `'---\ntags:\n  - a\nowner: Ana\n  # - b\nstatus: x\n---\n'`.
- `add after a list keeps its commented-out item above the new field on CRLF` — same defect with `\r\n`.
- `add after a nested map keeps its trailing comment above the new field` — actual
  `'---\nmeta:\n  k: v\nowner: Ana\n  # trailing in meta\nstatus: x\n---\n'`.
- `add of a multi-line value after a commented list is still positioned` — `false !== true` (`positioned`).
- `removing the only field leaves a valid empty mapping` — actual `'---\n\n---\nBody\n'`, expected `'---\n{}\n---\nBody\n'`.
- `removing the only field of a CRLF document leaves a valid empty mapping` — actual `'---\r\n\r\n---\r\nBody\r\n'`.
- Not failing before the fix, by design: `add after a list keeps a column-0 comment with the next field` (guard against
  over-extending) and the compact-sequence CRLF assertions (guards for the minimal path; the round-1 code already
  passes them).

## Tests added or changed
- `add after a list keeps its commented-out item above the new field` (LF and CRLF) — the trailing-comment fix.
- `add after a nested map keeps its trailing comment above the new field` — same, for a map value.
- `add of a multi-line value after a commented list is still positioned` — the fix keeps `positioned === true` and
  the block-scalar output.
- `add after a list keeps a column-0 comment with the next field` — the fix must not move a column-0 comment.
- `removing the only field leaves a valid empty mapping` (LF and CRLF) — `extractFrontmatter` reports no error and
  `frontmatter` deep-equals `{}`.
- CRLF round-1 tests: compact-sequence assertion added to `structural CRLF add at the end ...` and
  `structural CRLF remove of the last field ...`. These are the MINOR 5 fix.

## Existing assertions changed
- None. All changed assertions are in tests written in round 1 (T06), not existing tests.

## Verification
- `scripts/gate.sh T06-impl-r2-prefix unit` → FAIL as intended, 6 expected failures (`logs/T06-impl-r2-prefix-unit.log`).
- `scripts/gate.sh T06-impl-r2 unit types trusted` → PASS
  - compile: `logs/T06-impl-r2-compile.log`
  - unit: PASS, 413 tests, 413 pass, 0 fail, 0 todo (`logs/T06-impl-r2-unit.log`)
  - types: PASS (`logs/T06-impl-r2-types.log`)
  - trusted: PASS, exit 0, 37 s (`logs/T06-impl-r2-trusted.log`). RI-T06 screenshots `09-frontmatter-rename-minimal-patch`
    and `10-frontmatter-remove-minimal-patch` pass; no `Frame was detached` failure.
- `grep "UX-16 (T06)"` in `frontmatterPreservation.test.ts` → no matches.
- Only the four Allowed files are modified by this task (`git status`); the book and `.agents` changes already in the
  tree were not touched.

## Evidence for reviewers
- Logs: `logs/T06-impl-r2-prefix-unit.log`, `logs/T06-impl-r2-unit.log`, `logs/T06-impl-r2-trusted.log`.
- Screenshots: from the trusted run, under `.artifacts/` (newest real-input folder).

## Feedback addressed (rounds 2–3)
- Finding 1 (BLOCKER, add with `afterField` moves the anchor's comments): new `fieldEndWithTrailingComments` used for the
  insertion offset in `minimalAddPatch`. Four tests added (list LF/CRLF, nested map, multi-line value, column-0 guard).
- Finding 2 (BLOCKER, removing the only field gives `null`): `verified` requires a mapping root; `?? {}` removed. Two
  tests added (LF and CRLF), expecting `{}` and no parse error.
- Finding 5 (MINOR, CRLF tests cannot tell minimal from fallback): compact-sequence cases added to both tests.
- Finding 6 (NIT, RI-T06 pause comment): comment rewritten to name the cause.
- Finding 7 (NIT, report counts): corrected above.
- Findings 3 and 4 (MINOR, follow-ups): not changed, as instructed.

## Open points / STOP reason
- No STOP condition was hit.
- The `afterField` insertion after a trailing-comment block: the comment lines are inserted before the new field, so the
  anchor's comments stay with the anchor. A column-0 `#` line after the anchor stays above the next field (guarded by the
  column-0 test). A field that is followed by an indented comment and then a blank line is not separately tested.
- Follow-ups (not changed): Finding 3 (blank line before the fence on a plain add) and Finding 4 (indented comments
  of a removed field stay with the previous field).
