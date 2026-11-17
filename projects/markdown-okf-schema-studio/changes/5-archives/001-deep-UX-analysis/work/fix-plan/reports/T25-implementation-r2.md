# T25 implementation — round 2

STATUS: DONE

## Summary
Finding 1 fixed with consume-once semantics for the pending frontmatter edit, in `src/webview/scrollSync.ts` only.
Any frontmatter message posted (value save, key rename, remove, add) from the editor opened for the pending edit now drops the pending edit first. A new `add` then stores its own entry.
The render whose load opened the editor is recorded (`pendingFrontmatterEditOpenedIn`, persisted by `stateSnapshot`). A load of a different render drops the pending edit; a repeated load of the same render may still reopen it. Round-1 deviations 1 and 2 are kept.

## Files changed
- src/webview/scrollSync.ts — `consumePendingFrontmatterEdit()` called before the three `previewFrontmatterSave` posts; `pendingEditOpenedIn` state and its cleanup/persistence; check in `resumePendingFrontmatterEdit`.
- test/webview/scrollSync.test.ts — two new tests; harness config type gets `requestId` (harness extension only).
- test/integration/realInput.test.ts — RI-T25 closed-editor assertion before clicking `scope`.

## Tests written first (failing before the fix)
- T25: saving a value from the pending edit's editor consumes the pending edit — failure excerpt: `pendingFrontmatterEdit` still `{ fieldName: 'lifecycle', ... }` (logs/T25-impl2-pre-unit.log)
- T25: a later render does not reopen an editor that was already opened for the pending edit — `true !== false` (logs/T25-impl2-pre-unit.log)
- RI-T25 closed-editor assertion: NOT run against the round-1 code. I did not swap sources to do it. The round-1 failure is shown by the reviewer's screenshot of the reopened editor, and the unit tests above reproduce the cause.

## Tests added or changed
- The two unit tests above (Finding 1).
- RI-T25: after saving `Ana` and the render, waits for the `reviewer` row to exist with zero `[data-okf-frontmatter-editor]`, then captures `33-custom-key-added`, then clicks `scope`.

## Existing assertions changed
- None. The round-1 test asserting `{"fieldName":"lifecycle"}` is unchanged: the opened-in marker lives in a separate state key.

## Verification
- `PLAN/scripts/gate.sh T25-impl2 unit types contracts trusted visual` → PASS on all levels (logs/T25-impl2-*.log); visual: PASS vs baseline, 0 new failure lines.

## Evidence for reviewers
- Screenshot `33-custom-key-added`, retaken by the passing trusted run (real-input evidence folder in `.artifacts/`), after the closed-editor assertion.

## Feedback addressed (rounds 2–3)
- Finding 1: pending edit is consume-once, as described in the summary. Findings 2 and 3 untouched, per instructions.

## Open points / STOP reason
- A first attempt without `pendingFrontmatterEditOpenedIn` in `stateSnapshot` failed the unit test, because the snapshot overwrote the state; fixed.
- The pre-fix RI-T25 failure was not recorded (see above).
