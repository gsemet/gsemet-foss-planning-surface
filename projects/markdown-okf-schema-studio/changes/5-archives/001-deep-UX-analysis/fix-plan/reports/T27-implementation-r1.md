# T27 implementation — round 1

STATUS: DONE

## Summary
The host now accepts block insertion through the existing `previewEditOpen`/`previewEditSave`/
`previewEditCancel` messages with a new optional `insertAfterLine`. A new pure module plans the
offset and blank-line separators; the host reuses `drainActiveBlockEdit` (minimal edits, undo
grouping, stale-source check), so cancel removes the inserted text and empty text inserts nothing.

## Files changed
- src/mapping/insertion.ts — new: `planInsertion`, `insertionText`, `InsertionPlan`
- src/extension.ts — `insertAfterLine` field and validation (open/save/cancel only, safe integer >= 0); `ActiveBlockEdit.insertion`/`insertAfterLine`; open replies with `originalText: ""` and echoes `insertAfterLine`; save creates the insertion edit; later saves use `insertionText`; save rejects a mismatched `insertAfterLine` as stale
- test/mapping/insertion.test.ts — new unit tests
- test/integration/previewEditing.test.ts — protocol test added before the "references" section

## Tests written first (failing before the fix)
- previewEditing integration, insertion protocol — failure excerpt: `Preview editing integration failed: Error: Timed out waiting for the inserted block to appear.` (log: logs/T27-red-trusted.log). The unit tests for `insertion.ts` were written after the pure module (its spec is fully determined); they have no red run.

## Tests added or changed
- insertion.test.ts — between blocks, last line, directly-followed list item, empty doc, body without/with frontmatter (re-parses, same frontmatter), CRLF, whitespace-only raw, trailing breaks, out of range.
- previewEditing.test.ts — open leaves the document unchanged; autosave then final save yields one block with separators; cancel after a save removes it; whitespace-only save inserts nothing.

## Existing assertions changed
- none

## Verification
- `PLAN/scripts/gate.sh T27-impl unit types contracts trusted` → PASS (logs/T27-impl-*.log; unit 568 pass, 0 fail)

## Evidence for reviewers
- None (no UI).

## Open points / STOP reason
- Beyond the spec: `ActiveBlockEdit.insertAfterLine` is stored and a save whose `insertAfterLine` differs from the active edit's is rejected as stale (keeps ordinary and insertion sessions from mixing). Cancel is unchanged.
- Following-line detection uses the actual break at the offset, equivalent to the spec for uniform documents.
