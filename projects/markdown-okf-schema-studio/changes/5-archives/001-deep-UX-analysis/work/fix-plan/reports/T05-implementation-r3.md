# T05 implementation — round 3

STATUS: DONE

## Summary
- Fixed the round-2 BLOCKER (review finding 1): on CRLF documents, `minimalPairPatch` produced a lone `\r`
  inside multi-line comments (for example `# note line 1\r` followed by `\n`), which the editor turns into
  a blank line. The body is now normalized the same way as `createFrontmatterDocumentPatch`: every `\r\n`,
  `\r` or `\n` becomes the document line ending, and one trailing line break is stripped.
- No other code changed. Review MAJOR findings: none in round 2. The review's MINOR follow-ups are not
  changed (see Open points).
- Unit: 390 pass, 0 fail, 4 todo (T06 markers only). Types: PASS.
- Trusted, full, scroll, reload and visual were not run, because the macOS screen is locked. The orchestrator
  must run `trusted` after unlock.

## Files changed
- `src/frontmatter/okfFrontmatter.ts` — `body` in `minimalPairPatch` uses
  `rendered.replace(/\r\n|\r|\n/gu, lineEnding).replace(/(?:\r\n|\r|\n)$/u, "")`.
- `test/frontmatter/okfFrontmatter.test.ts` — two tests appended (below).

## Tests written first (failing before the fix)
Log: `logs/T05-impl-r3-prefix-unit.log` (`gate.sh T05-impl-r3-prefix unit`, run after the tests were added and
before the fix).
- `a multi-line comment between CRLF sequence items keeps CRLF line endings` — failure:
  `AssertionError: The input was expected to not match the regular expression /\r(?!\n)/u`.
- `a multi-line comment inside a CRLF nested map keeps CRLF line endings` — failure: the same regex assertion
  (lone `\r` in the patch text).
- Other entries in that log (T06 `todo` tests at `frontmatterPreservation.test.js` lines 177–192) are reported
  by the runner but are not counted as failures. They are the expected T06 markers.

## Tests added or changed
- `a multi-line comment between CRLF sequence items keeps CRLF line endings` — no lone `\r` in the patch, and
  the applied result equals the expected CRLF text with `- three` added and both comment lines kept.
- `a multi-line comment inside a CRLF nested map keeps CRLF line endings` — no lone `\r` in the patch, and the
  applied result equals the expected CRLF text with `k: w` (both comment lines kept).

## Existing assertions changed
- None.

## Verification
- `scripts/gate.sh T05-impl-r3-prefix unit` → FAIL as expected (the two new CRLF tests; T06 todos reported
  but not counted) — `logs/T05-impl-r3-prefix-unit.log`
- `scripts/gate.sh T05-impl-r3 unit types` → PASS: compile PASS (`logs/T05-impl-r3-compile.log`), unit PASS with
  390 pass / 0 fail / 4 todo (`logs/T05-impl-r3-unit.log`), types PASS (`logs/T05-impl-r3-types.log`)
- `trusted` → NOT RUN. The macOS screen is locked, and the trusted gate needs window focus. The orchestrator
  runs `gate.sh T05-impl-r3 trusted` after unlock.

## Evidence for reviewers
- Logs listed above. No screenshots were taken in this round.

## Feedback addressed (rounds 2–3)
- Round-2 finding 1 (BLOCKER, lone `\r` in CRLF multi-line comments): `body` normalization replaced with the
  reviewer's exact expression, which matches `createFrontmatterDocumentPatch`. Tests: both CRLF tests above.
  Both failed before the fix and pass after it.
- Round-2 findings 2–4 and NITs: already applied in round 2 and not changed in this round. Finding 5 (MINOR):
  not changed, as allowed.
- Round-2 MINOR follow-ups (not blocking, not changed): the `|+` trailing blank line as the last field; comments
  moved to their own line in the edited field (`tags:  # c`, `key: # c`); nested-map trailing comment
  re-indent; inline comment spacing in collections (`- a  # ca` → `- a # ca`). The reviewer notes these match
  base or are cosmetic, and the data is correct.

## Open points / STOP reason
- The working tree has changes in files outside this task (`book/chapters/*`, `.agents/thinking/...`). They
  were already present at the start of this round. I did not touch them.
- Trusted gate not run (locked screen). The round-2 review requires it after this fix. The round-2
  `trusted` pass (`logs/T05-impl-r2-trusted.log`) predates this fix.
- The earlier "Open points" from round 1 (RI-T05 ArrowDown amendment; no recorded pre-fix RI-T05 run) are
  unchanged.
