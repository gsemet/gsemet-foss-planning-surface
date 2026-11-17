# T05 implementation — round 1

STATUS: STOP

## Summary
- `createFrontmatterFieldPatch` now builds a minimal patch for an existing top-level field. The patch
  covers only that field's lines (`minimalPairPatch` in `src/frontmatter/okfFrontmatter.ts`). Comments,
  folded scalars, sequence indentation, quoting, and CRLF outside the field stay byte-identical.
- The minimal patch is verified before use: the candidate YAML must parse without errors and `toJS`
  must deep-equal the expected data (`isDeepStrictEqual`). On any failure, or when the field has an
  anchor or alias, or when the key is not at column 0, the existing whole-document patch is used
  unchanged. The add path is unchanged.
- All 14 T01 value-edit tests pass without `todo` markers. Unit: 382 pass, 0 fail, 4 todo (the T06 markers).
  Types and trusted gates pass.
- STOP reason: RI-T05 presses ArrowDown to choose `active`, as the task specifies, but that does not
  change the select value in this harness. The scenario therefore uses type-ahead (`a`). See Open points.

## Files changed
- `src/frontmatter/okfFrontmatter.ts` — new `minimalPairPatch` and helpers
  (`nodeRange`, `hasAnchorOrAlias`, `isFlowCollection`, `blockSequenceIndented`); `createFrontmatterFieldPatch`
  computes `expected` before the edit, tries the minimal patch for an existing pair, and falls back to
  `createFrontmatterDocumentPatch`. Imports: `node:util` (`isDeepStrictEqual`), `isAlias`, `YAMLMap`,
  `Document` (as `YamlDocumentBuilder`), `type Pair`.
- `test/frontmatter/frontmatterPreservation.test.ts` — removed the 14
  `todo: "UX-16 (T05)"` markers (entries and the `todo` option of the value-edit test); appended the four
  F2 outputs (tags, links, quoted, summary) to the comment-preservation test.
- `test/frontmatter/okfFrontmatter.test.ts` — six new tests appended (see below).
- `test/integration/realInput.test.ts` — `withDocument` takes an optional schema
  (`writeSchema`); new `REQ_SCHEMA`, `REQ_DOCUMENT`, scenario `scenarioFrontmatterValueMinimalPatch` (RI-T05),
  called last in `run()`.

## Tests written first (failing before the fix)
Log: `logs/T05-impl-prefix-unit.log` (`gate.sh T05-impl-prefix unit`, run after the tests were written and
before the fix; 16 failing: 14 T01 value edits, 2 new tests).
- `value edit F1 title changes only the named field` — failure excerpt:
  `+ 'description: When export is requested, the service SHALL write the report as CSV output.\n'` vs
  `- 'description: ... as CSV\n  output.\n'` (whole-document re-serialization folds the plain scalar).
- The other 13 `value edit …` cases fail the same way (whole-document re-serialization).
- `value patch rewrites only the edited field line and keeps its inline comment` — fails, since the patch covers the whole frontmatter.
- `value patch with an unchanged value leaves the document text identical` — fails, since re-serialization changes the text.
- RI-T05 (`08-frontmatter-value-minimal-patch`): NOT recorded before the fix. I tried a temporary revert of
  `okfFrontmatter.ts` to HEAD for the trusted run, and the auto-mode classifier denied that write. The fixed
  file was restored byte-identical (checked with `cmp`). The pre-fix behaviour is expected to fail, because the
  whole-document patch would reformat `tags` (indented sequence) and the two-line `summary`, so `lineDelta`
  would show more than one line. This still needs a recorded run.

## Tests added or changed
- `frontmatterPreservation.test.ts` — the 14 value-edit cases now run (no marker); F2 comment test covers 4 more outputs.
- `okfFrontmatter.test.ts` (new, all pass):
  - `value patch rewrites only the edited field line and keeps its inline comment` — the patch range is exactly `title: Alpha  # trailing comment`.
  - `value patch for an anchored value still writes correct data` — anchor → fallback path, data correct.
  - `value patch for a nested map written as an object yields the same data` — checked with `toJS`.
  - `appending a sequence item keeps a comment line between existing items` — `  # note` kept.
  - `value patch with an unchanged value leaves the document text identical` — no-op, for scalar and list.
  - `value patch fills an empty value on CRLF documents without touching the next line` — `exemption_reason: n/a\r\n`.
- `realInput.test.ts` RI-T05 — passes in the trusted gate; `lineDelta` asserted as removed `status: draft`, added `status: active`.

## Existing assertions changed
- None. No existing expectation needed to change: `okfFrontmatter.test.ts` and `previewEditing.test.ts`
  had no whole-document expectations after a value edit. The only removals are the T05 `todo` markers,
  which the task requires.

## Verification
- `scripts/gate.sh T05-impl unit types trusted` → compile PASS, unit PASS (382 pass, 0 fail, 4 todo, T06 only),
  types PASS, trusted-build PASS, trusted PASS (34 s) — `logs/T05-impl-unit.log`, `logs/T05-impl-types.log`,
  `logs/T05-impl-trusted.log`. The trusted log includes `PASS real-input screenshot: 08-frontmatter-value-minimal-patch`.
- Pre-fix unit run: FAIL (16) — `logs/T05-impl-prefix-unit.log`.
- Probe runs (temporary, informational; the test file was restored afterwards):
  - `logs/T05-impl-probe-trusted.log` — ArrowDown twice and Enter: value stays `draft`, editor closes, buffer unchanged.
  - `logs/T05-impl-probe2-trusted.log` — typing `a`: value becomes `active`.
- Not run: `contracts`, `full`, `visual`, `scroll`, `reload` (not in the task's gate).

## Evidence for reviewers
- Screenshot: written by the real-input harness during the trusted run (`08-frontmatter-value-minimal-patch`); the
  evidence folder is produced by `createEvidence("real-input")`, which I did not inspect.

## Feedback addressed (rounds 2–3)
- n/a (round 1).

## Open points / STOP reason
1. **RI-T05 keyboard step deviates from the task.** The task says: "press `ArrowDown` until `active`, then `Enter`".
   In the trusted run on macOS, ArrowDown twice left the select on `draft`, and Enter then closed the editor
   without a change (`logs/T05-impl-probe-trusted.log`). I changed the step to a type-ahead key (`a`, which
   selects `active`), then Enter. This is a test-only keyboard change, but the task says to STOP on a mismatch,
   so the reviewer or user must approve it or give a different key sequence.
2. **Pre-fix RI-T05 failure not recorded** (see Tests section). The auto-mode classifier blocked the temporary
   revert needed for the probe. The fix file was restored and verified. The reviewer or user should record
   the pre-fix run (e.g. with `git stash`-free means such as a temporary copy of HEAD's file) before accepting.
3. The minimal patch also covers the case with no value node (`pair.value` null), using `key.range[1] + 1`, per the design.
   It is only reached when the parser gives no value node, which the task's table does not cover.
4. Stale-logs note: `logs/T05-impl-trusted.log` now holds the final passing run; the earlier failing RI-T05 run
   (ArrowDown) was overwritten.
