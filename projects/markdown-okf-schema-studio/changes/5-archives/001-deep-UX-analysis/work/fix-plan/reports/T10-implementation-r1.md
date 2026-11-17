# T10 implementation — round 1

STATUS: DONE

## Summary
Approach A shipped: a `keepUndoInControl(event)` helper in the webview runtime calls
`stopPropagation` (never `preventDefault`) for Cmd/Ctrl+Z, Cmd/Ctrl+Shift+Z and Ctrl+Y (keyCode
90/89, no Alt). It is the first statement of the keydown listeners of the block textarea, the table
cell input, and the frontmatter key and value controls. VS Code's bubble-phase handler therefore
never sees the key, and the browser performs the native textarea undo in both hosts. Approach B
was not needed.

## Files changed
- src/webview/scrollSync.ts — `keepUndoInControl` helper + 4 call sites
- test/webview/scrollSync.test.ts — new unit test
- test/integration/realInput.test.ts — RI-T10 (side + open-with)

## Tests written first (failing before the fix)
- RI-T10 open-with: `Timed out waiting for the undo to remove the last typing chunk. Editor state: {"tag":"BODY"}; buffer: "Second paragraph. abc"`
  (the editor closed and the document undo ran). The side-preview run passed before the fix, as the task predicted.
  Log: logs/T10-impl-red-trusted.log

## Tests added or changed
- scrollSync.test.ts "undo and redo shortcuts stop at the block textarea and keep the native undo" — Meta/Ctrl+Z,
  Shift+Z, Ctrl+Y call stopPropagation and never preventDefault; plain z/y, Cmd+S, Alt+Cmd+Z do not; no messages sent.
- realInput.test.ts RI-T10 (`scenarioUndoStaysInEditor`, run for side and open-with) — types ` abc`, waits, ` def`,
  Mod+Z leaves the textarea focused with a proper prefix value (Chromium undoes by word, leaving `... abc `, so the
  assertion accepts any strict prefix starting with `Second paragraph.`), the buffer follows, and Mod+Shift+Z restores
  ` abc def`. Screenshots 16-undo-stays-side / 16-undo-stays-open-with.

## Existing assertions changed
None.

## Verification
- `gate.sh T10-impl unit trusted` → PASS (logs/T10-impl-unit.log, logs/T10-impl-trusted.log; trusted includes RI-T10 in both modes)

## Evidence for reviewers
- Screen was not locked. Screenshots 16-undo-stays-side and 16-undo-stays-open-with are listed in the trusted log.

## Open points / STOP reason
- The frontmatter key/value controls got the helper without a dedicated unit/E2E test (same code path as the block
  textarea); the task only requires the block textarea unit test.
