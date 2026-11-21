# Diagnosis: J5 "Timed out waiting for the marker on line 25" (CI run 44933517789)

Reproduction: only in a real VS Code window (Linux CI): `gh workflow run ci.yml --ref chantier/batch-07/cr-456-... -f heavy=true`
(`just ci-integration`). Not reproducible on this Windows machine. Nothing here was run; it is read from the code and the log.

## Proven (code + log)
- The log shows two `command` / `diff-side` selection records, both with a jump on doc.md: line 25, then line 1.
  `jumpVerdict` (core/navigation/jumpSignal.ts) makes every `command` change with one selection on an eligible diff side a jump,
  and `editorJumps.ts` maps either side of the diff to the real file (virtual side -> `realSideOfDiff` -> doc.md). So the
  line-1 record is a jump by the product's own rules, whichever side it came from.
- Each jump goes `onJump` -> `onEditorJumped` -> `requestJumpMarker` -> `requestRevealLine`, which OVERWRITES
  `scroll.pendingRevealLine`; `postPendingRevealLine` then sets `scroll.markedLine = {line}` (scrollSync.ts:317-318). The last jump wins.
  After the two records, `markedLine.line` is 1 (or undefined if the switch/refresh cleared it, `forgetLinesOutside`), never 25.
  The test's `waitFor(markedLine()?.line === 25)` therefore times out. This matches "J1-J4 pass, J5 fails": J1-J4 produce one jump each.
- The marker is not removed by an edit (no edit in J5) and nothing else in the code sets it back to 25.

## Guessed (not provable from the log)
- Which editor produced the line-1 record. Most likely the diff editor re-applying/resetting a cursor at line 1 on a side
  (the original virtual side or the modified side) when `vscode.diff` is re-executed on the diff that is ALREADY open with the same
  URIs: VS Code reuses the tab and sets the selection, then the side editor's model/cursor is re-set (kind `command`, line 0).
  The test printed only kind/target/jump, not the event uri or `firstLine` per side, so this stays a guess.
- Whether a real user could hit it: a genuine Go to Line/search click gives ONE selection change (J1 proves the click gives one record),
  so the user case is fine. The double record is an artifact of the test re-executing `vscode.diff` on an open diff (CR-455's lesson:
  a new `vscode.diff` replaces/reuses the preview tab, so wait for the active tab, do not assume a fresh editor).
- Product behaviour "last jump wins" is correct and must not be changed to ignore a line-1 jump (a real Go to Line 1 is a jump).

## Place to fix: the test (smallest fix), test/integration/sidePreviewJump.test.ts, J5
1. Do not re-execute `vscode.diff` on the open diff. Instead open the diff ONCE, with the selection, from a clean state:
   `closeAllEditors()`, show doc.md + `COMMAND_ID` + wait `previewOf`, then a single
   `vscode.commands.executeCommand("vscode.diff", virtualOf(doc), doc, "Diff under test", { selection })`, then wait for the diff to be
   the active tab (reuse `openDiff`'s wait; give `openDiff` an optional options argument). Let the initial selection events settle.
2. Make the assertion robust to the ordering instead of the exact record: after the open settles, move with a SECOND, separate jump
   that is a single move, on the already-open diff: `vscode.window.activeTextEditor.revealRange` is not a selection change, so use
   `activeTextEditor.selection = ...` (kind none, no jump) -> not usable; the reliable move is `vscode.open`/`vscode.diff` with a selection
   AFTER waiting 500 ms of quiet, then wait for `markedLine().line === 25` and, only as a fallback diagnostic, print `markedLine()` and the
   records WITH `uri` and `firstLine` (add them to the `console.log` at line ~139) so the next failure is decisive.
3. If step 1 still gives a trailing line-1 jump, assert the last-jump semantic explicitly: wait for the recorder to be quiet
   (no new record for 500 ms), then expect `markedLine().line` equals the line of the LAST jump record (`diffRecords.at(-1).jump.line`),
   and require that at least one jump record exists with the real file's uri. That checks the CR (a diff-side jump marks the real
   file) without depending on VS Code's internal ordering of the reset.
Option 3 is the smallest and does not depend on guesses; add the uri/firstLine to the log in the same edit.

Not recommended: a product change (debounce or ignore line-1 jumps right after a diff opens). It would drop real jumps; no evidence of a user bug.
