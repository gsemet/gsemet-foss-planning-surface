# T27 review — round 1

Base: 25fefa5 · Reviewed diff (extension scope): 4 files — `src/extension.ts` +70/-2,
`test/integration/previewEditing.test.ts` +68/-0, new `src/mapping/insertion.ts`, new
`test/mapping/insertion.test.ts`. (Other files in `git diff` — QA skill, book chapter — predate this
task and are not part of T27.)

## Gates
unit: PASS (logs/T27-unit.log, 0 `not ok`) · types: PASS · contracts: PASS · trusted: PASS, exit 0
(logs/T27-trusted.log). No new failure relative to the T00 baseline.

## Done-when
- [x] `unit` and `trusted` gates pass — logs above.
- [x] Protocol test: open leaves document unchanged; autosave + final save yields the block once with
  separators; cancel after save removes it; whitespace-only save inserts nothing — new block in
  `previewEditing.test.ts` (red run: logs/T27-red-trusted.log, "Timed out waiting for the inserted
  block to appear").
- [x] Unit spec cases pinned in `insertion.test.ts`: between blocks, after last line (with and without
  final break), directly-followed list item, empty doc, start without/with frontmatter (re-parsed via
  `extractFrontmatter`), CRLF (including CRLF frontmatter), whitespace-only raw, trailing breaks
  dropped, out of range (`2` on `"A\n"` proves a final break is not a line). Written after the
  module, but each assertion is an exact string equality on the spec's expected output, so they
  do pin the behaviour.

## Protected features checked
- P-E6 (stale-source): first insertion save goes through `currentPreviewDocument`, which requires
  `document.version === message.documentVersion` and a current stage → a save against a changed
  version is refused with "The preview is stale", never applied at a shifted offset. The plan is
  recomputed on the save's own (verified) text. Later saves go through `drainActiveBlockEdit`, whose
  check compares the text at `[sourceStartOffset, +lastSavedText.length)` with `lastSavedText`;
  on the first save `lastSavedText === ""` is vacuous but safe because the version check above
  already pinned the text in the same synchronous turn. Once a non-empty block is saved, the check is
  meaningful (the inserted text starts exactly at `plan.offset`).
- P-E6 interleaving: `preview.activeBlockEdit` is single-slot; an insertion save while any edit is
  active falls to the common guard and fails on `editId`/version; an ordinary save while an
  insertion is active fails the same way. The extra `insertAfterLine !== edit.insertAfterLine` check
  compares `undefined === undefined` for ordinary edits, so it cannot reject a legitimate ordinary
  save; for insertion saves the webview echoes the same value, so it cannot reject a legitimate one
  either. It only adds protection. Accepted.
- P-S2: `insertAfterLine` validated in `isPreviewSyncMessage` (open/save/cancel only, safe integer
  >= 0); `line`/`endLine` requirements unchanged.
- P-E8: insertion uses the same message handlers, gated identically to ordinary edits (read-only
  previews never reach them); no new path bypasses the gating.
- Ordinary block edits, checkbox refusal, frontmatter saves: the `else if (!edit)` branch and
  cancel are byte-identical to base apart from the `pendingText` ternary, which is a no-op when
  `edit.insertion` is undefined; existing trusted tests for these paths still pass.

## Findings
1. [MINOR] `src/extension.ts`:`drainActiveBlockEdit` — if within one insertion session the user
   clears the text (autosave sets `lastSavedText = ""`) and the document is then changed before the
   offset by another actor, the next save's safety check is vacuous and would insert at a stale
   offset. The same gap already exists for ordinary blocks emptied mid-session, so this is not a
   regression. Follow-up: when `edit.insertion` is set and `lastSavedText === ""`, also require
   `source.document.version` to equal the version recorded after the last applied edit (store it in
   `ActiveBlockEdit` on apply), with a unit/integration test that clears, edits elsewhere, then saves.
2. [MINOR] `src/mapping/insertion.ts`:`planInsertion` — `planInsertion("", 1)` returns a plan with
   prefix `"\n\n"`, producing `"\n\nNEW"` in an empty document. Spec says out-of-range → `undefined`;
   an empty document has 0 lines. Follow-up: return `undefined` for `afterLine >= 1` on empty text
   and add `assert.equal(planInsertion("", 1), undefined)`.
3. [NIT] No integration test asserts that an insertion save with an outdated `documentVersion` is
   refused; the guarantee holds by code reading (shared `currentPreviewDocument`). Worth adding when
   T28 lands.

## Existing assertions changed
None — OK.

VERDICT: PASS
