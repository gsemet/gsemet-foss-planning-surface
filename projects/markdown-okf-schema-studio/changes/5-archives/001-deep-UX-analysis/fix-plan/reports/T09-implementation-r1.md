# T09 implementation — round 1

STATUS: DONE

## Summary
Inline typing is now written to the source 400 ms after the last keystroke instead of per keystroke.
Blur, Escape, Cmd/Ctrl+Enter, edit-mode off and block navigation still flush at once through
`postBlockEditSave(true)`; a table cell switch now flushes at once through `postBlockEditSave(false)`.
The host replaces only the changed characters (`minimalReplacement`), keeping the stale-source guard
and the `applying`/`pendingText` coalescing. A typing burst is one document change and one undo step.

## Files changed
- src/mapping/textDiff.ts — new pure `minimalReplacement` (CRLF and surrogate safe)
- src/extension.ts — `drainActiveBlockEdit` applies the minimal range; import added
- src/webview/scrollSync.ts — `AUTOSAVE_DELAY_MS`, debounced `autosaveBlockEdit`, timer cleared in `postBlockEditSave` and `closeBlockEdit`, `switchTableCell` flushes immediately
- test/mapping/textDiff.test.ts — new
- test/webview/scrollSync.test.ts — fake timers (`flushTimers`, `pendingTimerCount`), new tests, flushes in 3 existing tests
- test/integration/realInput.test.ts — RI-T09 (`scenarioTypingUndoGrouping`)

## Tests written first (failing before the fix)
- typing is saved once after the autosave delay, carrying the last text — `true !== false` (save posted before flush)
- blur after typing posts one final save and clears the autosave timer — `2 !== 1` (two saves)
- switching table cells posts the pending change immediately — `0 !== 1` (log: logs/T09-impl-pre-unit.log)
- RI-T09 (logs/T09-impl-pre-trusted.log) — 20 content changes while typing, each replacing the block (`{"rangeLength":18,"textLength":19}` ... `{"rangeLength":37,"textLength":38}`)

## Tests added or changed
- textDiff.test.ts — identical, insert/delete/replace, start/end, overlap, CRLF, emoji, 200 seeded random pairs
- the 3 scrollSync tests above, plus harness fake timers
- RI-T09 after the fix: 1 content change while typing (`{"rangeLength":0,"textLength":20}`), one undo restores `Second paragraph.`
  (the test also waits for the block editor to close and focuses the first editor group before `undo`)

## Existing assertions changed
- scrollSync.test.ts: three tests that assert a `previewEditSave` right after an `input` event
  ("Escape ... previewEditSave" test with `(1 reworks)`, "edit mode loads raw Markdown..." unchanged,
  "raw Markdown block edits autosave on input...") — old: assertion directly after `dispatch("input")` →
  new: `harness.flushTimers()` inserted before it (1 call in the Escape test, 2 in the autosave test); expected message content unchanged;
  required by: the 400 ms debounce.

## Verification
- `gate.sh T09-impl unit trusted scroll` → PASS / PASS / PASS (logs/T09-impl-unit.log, T09-impl-trusted.log, T09-impl-scroll.log)
- The first scroll run failed with "Timed out waiting for the custom editor render" before any scroll test body (flake); the rerun passed.

## Evidence for reviewers
- Screenshot `15-typing-undo-grouping` in the real-input evidence folder.

## Open points / STOP reason
- None. Screen was unlocked.
