# T05 implementation — round 2

STATUS: DONE

## Summary
- Fixed review findings 1–4 in `minimalPairPatch` (`src/frontmatter/okfFrontmatter.ts`), using the
  reviewer's exact steps. Block scalars keep their header comment (`commentNode` is cleared only when the
  original value is not a block scalar). Block and flow collections get the suffix only through the
  reviewer's formula, which excludes block scalars. The plain-to-literal type copy now skips `PLAIN`.
- Duplicated comments are gone: a block sequence's trailing commented-out lines, a nested map's trailing
  comment, and a scalar's inline comment replaced by a list are each emitted once.
- Applied NIT 6 (unused `currentPreviewFrame` import removed from `realInput.test.ts`) and NIT 7 (one blank
  line before `applyFieldPatch`). MINOR 5 is not changed.
- Unit: 388 pass, 0 fail, 4 todo (T06 markers only). Types and trusted gates pass, including RI-T05
  (`08-frontmatter-value-minimal-patch`).

## Files changed
- `src/frontmatter/okfFrontmatter.ts` — `originalIsBlockScalar`; suffix
  condition; `commentNode` (saved, cleared, restored in `finally`) replaces the scalar-only comment handling;
  type copy skips `PLAIN` originals. The type restore stays separate.
- `test/frontmatter/okfFrontmatter.test.ts` — six new tests appended (below);
  blank-line NIT.
- `test/integration/realInput.test.ts` — removed unused `currentPreviewFrame`
  import (NIT 6). No other change in this round.

## Tests written first (failing before the fix)
Log: `logs/T05-impl-r2-prefix-unit.log` (`gate.sh T05-impl-r2-prefix unit`, run after the tests were added and
before the fix code changed): 392 tests, 383 pass, 5 fail, 4 todo.
- `appending to a sequence keeps a trailing commented-out item once` — failure excerpt:
  `+ '  # - StRS-CORE-002\n' +` (the comment line appears twice).
- `editing a nested map keeps its trailing comment once` — fails on the same duplicated-comment defect.
- `editing a block scalar keeps its header comment` — actual `'summary: >-\n  New'`, expected
  `'summary: >- # header\n  New'` (header comment lost).
- `replacing a commented scalar by a list keeps the comment once` — `2 !== 1` (`# c` written twice).
- `a multi-line value on a plain field is written as a literal block` — actual `'description: a\n\n  b'`,
  expected `'description: |-\n  a\n  b'`.
- Guard, not a bug reproduction: `a commented last item of a block sequence keeps its comment once` already
  PASSED before the fix (no duplication in that case). It is kept as a regression guard for the new suffix formula.

## Tests added or changed
- `appending to a sequence keeps a trailing commented-out item once` — whole-output check for appending
  (`# - StRS-CORE-002` kept once), plus `["StRS-CORE-001"]` gives output identical to the source.
- `a commented last item of a block sequence keeps its comment once` — `# keep` appears once after appending;
  data checked.
- `editing a nested map keeps its trailing comment once` — exact output.
- `editing a block scalar keeps its header comment` — exact output with `>- # header` kept.
- `replacing a commented scalar by a list keeps the comment once` — `# c` appears once; data deep-equal.
- `a multi-line value on a plain field is written as a literal block` — exact output `|-`.

## Existing assertions changed
- None. `frontmatterPreservation.test.ts` is not touched in this round.

## Verification
- `scripts/gate.sh T05-impl-r2-prefix unit` → FAIL as expected (5 new tests) — `logs/T05-impl-r2-prefix-unit.log`
- `scripts/gate.sh T05-impl-r2 unit types` → PASS: unit 388 pass / 0 fail / 4 todo (`logs/T05-impl-r2-unit.log`),
  types PASS (`logs/T05-impl-r2-types.log`). The "✖ failing tests:" header in the unit log lists only the
  T06 `todo` test, with `fail 0`.
- `scripts/gate.sh T05-impl-r2 trusted` → PASS, exit 0, 34 s (`logs/T05-impl-r2-trusted.log`). Includes
  `08-frontmatter-value-minimal-patch`. No `Frame was detached` failure.
- Extra probes (scratch script, not committed): block list replaced by `[]`, a sequence of maps with a trailing
  comment, a scalar with a trailing `# after` line, a `null` value on a block scalar with a header comment, and a
  nested map that gains a key. Each keeps its comments once and writes the expected data.

## Evidence for reviewers
- Trusted run screenshot (from the harness): `08-frontmatter-value-minimal-patch`, written during the trusted run.
  I did not open it in this round.

## Feedback addressed (rounds 2–3)
- Finding 1 (BLOCKER, duplicated trailing comments): `originalIsBlockScalar`; the suffix is restricted to non-block
  scalars; `commentNode` holds the node comment for scalar, seq and map values and is not emitted when the
  original was not a block scalar. Tests: sequence append, nested map.
- Finding 2 (BLOCKER, lost block-scalar header comment): `commentNode` is not cleared for block-scalar originals,
  so the renderer emits the header comment. Test: block scalar header.
- Finding 3 (MAJOR, comment doubled when scalar becomes a list): the same `commentNode` change; the suffix is
  emitted once and the renderer does not add the node comment. Test: scalar to list.
- Finding 4 (MAJOR, PLAIN type copied): the type copy skips `PLAIN` originals. Test: multi-line plain field.
- Finding 6 (NIT): unused import removed. Finding 7 (NIT): extra blank line removed.
- Finding 5 (MINOR): not changed, as instructed.

## Open points / STOP reason
- None for this round. The round-1 open points (ArrowDown → type-ahead for RI-T05, and the missing pre-fix RI-T05
  run) are unchanged. The task file already records the ArrowDown amendment. The pre-fix RI-T05 run is not
  recorded, as in round 1; the review accepted the reproduction.
- The suffix formula is applied exactly as the review states it. It has no separate branch for block sequences whose
  last item has an inline comment. Probes and the guard test show no duplication for that case.
