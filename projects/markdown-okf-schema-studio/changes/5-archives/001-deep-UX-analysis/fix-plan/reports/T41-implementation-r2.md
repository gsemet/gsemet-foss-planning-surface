# T41 implementation — round 2

STATUS: DONE

## Summary
Round 1 review findings 1 and 2 are applied. `isPlainSafeScalar` now also requires the YAML 1.1 stringify round-trip and rejects tabs and a bare `=` or `<<`. The `leading` insertion now goes after leading comment lines, at the start of the first key's line, with CRLF handled. No dependency was installed or fetched.

## Feedback addressed
- Finding 1 (MAJOR): `isPlainSafeScalar` adds `stringify(text, { version: "1.1", lineWidth: 0 }) === text + "\n"`, and returns false for `/\t/` and `/^(?:=|<<)$/`. The unit list holds all the cases the review named. `?x` stays plain. The `2026-10-13` patch case writes `approver: "2026-10-13"`.
- Finding 2 (MINOR): in `minimalAddPatch`, `leading` now uses `offset = text.lastIndexOf("\n", firstKeyStart - 1) + 1`. Unit test `# header` covers LF and CRLF: `# header`, then `a: ""`, then `title: x`, as a one-line diff.
- Finding 3: no action.

## Files changed
- `src/frontmatter/okfFrontmatter.ts` — the two fixes above.
- `test/frontmatter/okfFrontmatter.test.ts` — extended safety test, date patch test, header test.

## Tests written first (failing before the fix)
- `T41: plain scalar safety` — `AssertionError: "2026-10-13": true !== false` (`logs/T41-pre2-unit.log`).
- `T41: plainScalar quotes a date-like value` and `T41: beforeField on the first key inserts after leading comment lines` — both failed against round 1 (same log).

## Tests added or changed
- The three tests above. The safety test is the round 1 test extended with the review's full list, so no assertion was removed.

## Existing assertions changed
- None in round 2 (round 1 changes to RI-T24 and RI-T25 stand).

## Verification
- `gate.sh T41-impl2 unit types trusted full` → unit, types and trusted PASS. `full` FAILED once on the checkbox-toggle "one undo" timeout (`logs/T41-impl2-full.log`). The screen was unlocked. This test is unrelated to T41 and is a focus-sensitive one.
- Rerun `gate.sh T41-impl2b full` → PASS (`logs/T41-impl2b-full.log`), including RI-T41.

## Evidence for reviewers
- Same real-input captures as round 1 (`t41-*`).

## Open points / STOP reason
- The `full` failure above is a one-off. It passed on the immediate rerun with no code change.
