# T06 implementation — round 1

STATUS: DONE

## Summary
- Rename, remove and add of a frontmatter field now patch only the lines of that field, not the whole block. Each
  minimal patch is verified by re-parsing the candidate text (data, key order, parse errors). When verification
  fails, the whole-document patch is used as before.
- `minimalPairPatch` (T05) was refactored into shared helpers: `fieldRegion`, `yamlStyle`, `renderPair` (T05's
  comment save/clear/restore and CRLF body normalization, unchanged) and `verified`. T05 behaviour is unchanged;
  all T05 value-edit tests pass.
- Add takes an optional `{ afterField }`. The new pair goes after that field's line, or at the end of the YAML text.
  `positioned` reports whether `afterField` was honoured. Adding to an empty frontmatter block (`---\n---`) now works.
- Removing the last field deletes the preceding line break instead, so no double line break is left.
- All 4 `todo: "UX-16 (T06)"` markers were removed; their tests pass. 13 new tests and 1 real-input scenario were added.

## Files changed
- `src/frontmatter/okfFrontmatter.ts` — shared helpers; `minimalRenamePatch`,
  `minimalRemovePatch`, `minimalAddPatch`; `createFrontmatterFieldPatch(source, name, value, options?)`;
  `FrontmatterFieldPatch.positioned?`; `stringify` import from `yaml`.
- `test/frontmatter/frontmatterPreservation.test.ts` — 4 T06 markers removed; 11 tests
  added (add after field, add after last field, add to empty block, compact list add, remove last field with full
  expected text, quoted rename, four CRLF add/remove tests).
- `test/frontmatter/okfFrontmatter.test.ts` — 2 tests added (remove keeps comment
  lines above the key; `afterField` reports `positioned`, including the missing-field case).
- `test/integration/realInput.test.ts` — RI-T06 (`scenarioFrontmatterStructuralMinimalPatch`):
  rename `summary` → `abstract` in the name cell, then remove `tags` with the Remove button. Asserts `lineDelta`
  and the full buffer. Screenshots `09-frontmatter-rename-minimal-patch` and `10-frontmatter-remove-minimal-patch`.

## Tests written first (failing before the fix)
Pre-fix state: the committed code (HEAD `b3ee36d`), with only the new signature (`options`) and `positioned?` added so
that the tests compile. The behaviour is unchanged. The fixed file was restored afterwards and verified with `cmp`.

- Unit, `scripts/gate.sh T06-impl-prefix unit` → 13 failing, log `logs/T06-impl-prefix-unit.log`:
  - `structural F2 rename title to heading keeps the trailing comment` — `'heading: Alpha # trailing comment\n'` vs
    expected `'heading: Alpha  # trailing comment\n'`, plus the folded summary re-flowed to one line.
  - `structural F2 remove links deletes exactly that line` — `'title: Alpha # trailing comment'` (spacing normalized) and
    the rest of the block rewritten.
  - `structural F2 remove tags deletes exactly the sequence lines` — `'links: [ a.md, b.md ]'` (flow padding added).
  - `structural F1 add owner appends one line before the closing delimiter` — `'description: ... as CSV output.'` (plain
    scalar re-flowed); `'  - StRS-CORE-001'` (sequence re-indented).
  - Also failing: `structural F2 add owner after title…`, `structural F2 add after the last field…`,
    `structural add to an empty frontmatter block…` (no patch), `structural F1 add of a list…`,
    `structural F2 remove of the last field…`, `structural F2 rename to a key that needs quoting…`,
    `structural CRLF add after a field keeps CRLF line endings`, `frontmatter field removal keeps the comment lines
    above the removed key`, `frontmatter add with afterField reports whether the field was placed` (`positioned`
    missing).
  - The CRLF remove and CRLF add-at-end tests pass before the fix as well. The whole-document path already gave the
    right bytes there, so they are regression guards.
- Real input, `scripts/gate.sh T06-impl-prefix trusted` → FAIL, log `logs/T06-impl-prefix-trusted.log`. The run
  failed earlier than the structural check: the first typed character after select-all was lost (`bstract`). See
  Open points.
- Real input, `scripts/gate.sh T06-impl-prefix2 trusted` (same pre-fix code, with the pause added) → FAIL at
  `Timed out waiting for the key rename to reach the source buffer`, log `logs/T06-impl-prefix2-trusted.log`. The
  buffer never reached the expected one-line change. I did not capture the exact pre-fix buffer text.

## Tests added or changed
- `frontmatterPreservation.test.ts`: 4 T01 markers removed (the existing rename/remove/add assertions kept verbatim).
- `frontmatterPreservation.test.ts`: the new tests listed under Files changed. Each asserts the full resulting text.
- `okfFrontmatter.test.ts`: `frontmatter field removal keeps the comment lines above the removed key`; `frontmatter add
  with afterField reports whether the field was placed`.
- `realInput.test.ts`: RI-T06 (see Files changed).

## Existing assertions changed
- None. The existing `okfFrontmatter.test.ts` rename/remove tests use regex matches and pass unchanged.
  `previewEditing.test.ts` was not changed and passes in the trusted run, so no expectation there needed an update.

## Verification
- `scripts/gate.sh T06-impl compile unit types` → PASS: compile `logs/T06-impl-compile.log`; unit 406 pass, 0 fail,
  0 todo (`logs/T06-impl-unit.log`); types `logs/T06-impl-types.log`.
- `scripts/gate.sh T06-impl trusted` → PASS, exit 0 (`logs/T06-impl-trusted.log`, `logs/T06-impl-trusted-build.log`).
  Includes RI-T06 and screenshots 09 and 10.
- Ad-hoc probe (not in the repo; scratch script on the compiled `out/`): 72 cases in LF and CRLF on three comment-heavy
  documents (remove, rename, rename-quoted and add for every field, plus add with `afterField`). No lone `\r`/`\n` in
  CRLF patches, no comment change for rename and add, and no new comment for remove. 0 problems.
- Done-when: no `UX-16 (T06)` marker left in `frontmatterPreservation.test.ts` (`grep` shows none). RI-T06 shows
  one-line diffs (`lineDelta` asserts `summary:`→`abstract:` only, and removal of exactly `tags:`, `- alpha`, `- beta`).

## Evidence for reviewers
- Logs: `logs/T06-impl-prefix-unit.log`, `logs/T06-impl-prefix-trusted.log`, `logs/T06-impl-prefix2-trusted.log`,
  `logs/T06-impl-unit.log`, `logs/T06-impl-trusted.log`.
- Screenshots of the post-fix run (real-input folder, newest): `.artifacts/real-input-33aIqt/09-frontmatter-rename-minimal-patch.png`
  and `.../10-frontmatter-remove-minimal-patch.png`. The `.md` next to each PNG holds its note.

## Feedback addressed (rounds 2–3)
- Not applicable (round 1).

## Open points / STOP reason
- No STOP condition was hit. The working tree has pre-existing changes outside this task (`book/chapters/*`,
  `.agents/thinking/...`). I did not touch them.
- Harness detail, not part of the design: in RI-T06, the first character typed after `${MOD}+A` in the key input was
  lost (`bstract`). I added a 300 ms pause after select-all with a code comment. The task text does not mention it.
  The reviewer should judge whether this deviates from the task's steps. The pause is the only change to the
  specified steps.
- Blank line before the closing fence: when the YAML text ends with a blank line, an add without `afterField` inserts
  the new line after that blank line (`a: 1`, blank, `owner: Ana`, `---`). This follows the task's "end of text, with
  lineEnding + rendered" rule literally. It is valid, but it leaves a blank line between the fields.
- `afterField` naming a field whose line cannot be located (for example flow mappings) falls back to the
  whole-document path with `positioned: false`.
- Remove deletes comment lines that sit inside the removed field's own lines (between its items). Comment lines after
  the field's last line stay in place. The task says "never delete user comments" and I read the inner comments as
  part of the removed field. Please check this reading.
- Empty frontmatter (`---\n---`): `createFrontmatterFieldPatch` accepts it for add. `extractFrontmatter` still reports
  it as an error, so the properties table does not offer an add there. T24 must handle that UI case.
- Pre-existing test-host noise: the trusted run logs `Command failed: git fetch` and `CodeWindow: failed to load`. Both
  are unrelated to this change, and the run passed.
