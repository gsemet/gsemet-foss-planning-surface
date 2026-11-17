# Round 1 Inspector review — CR 218

Change under review: worktree `markdown-okf-schema-studio-wt-218`, HEAD `dc3bff92` on `0b4ede78`
(`git diff HEAD~1`). 10 files, +329 / -9. Source: `frontmatterEditor.ts` (+45), `frontmatterValueEditor.ts`
(+4), `pageInput.ts` (+6), `pageRuntime.ts` (+14).

## 1. Behaviour against the approved note

| Approved point | Implementation | Verdict |
| --- | --- | --- |
| Refocus after refusal, only when focus is lost (body/null, the control, inside the cell) | `receiveFrontmatterResult` records `focusLost` before `afterResult`, refocuses only if the edit is still active and not saving; list editor via `edit.focusControl` | OK |
| Escape closes the refused editor | Refocus puts the focus back in the control; the control's Escape handler and the properties-section handler both close it | OK |
| Blur does not post the unchanged refused text again | `holdsRefusedText()` guard in the value blur, the list `focusout` and the key blur | OK |
| Click/Enter/Space on another value or key cell closes it without a save and opens the clicked field | `closeRefusedEditorFor(cell)` in the capture link click, the field click and the Enter/Space path; `cancel()` and then close, so the field shows its saved value | OK |
| Changed text: saved once; changed + click other = today's behaviour | `controlText` differs, so the blur saves (`saving` is true), `closeRefusedEditorFor` returns false and the open is a no-op as today | OK |

Regression walk-through:

- **BLOCK-041 click on a block after a refusal:** the blur now posts nothing, so `plainSavePending` stays
  false. `openBlockEditor` closes the idle field editor and opens the block in the same click. This is the
  same outcome as before, with one round trip fewer. When the refusal arrives while a block click waits,
  `afterResult` closes the field editor and opens the block. `state.activeFrontmatterEdit !== edit`, so the
  page does not refocus. OK.
- **FMEDIT-067 navigation flush:** `flushFrontmatterEditor` calls `save()` directly. It does not go through
  the blur guard, so the refused text is still flushed. A refusal that triggers the flush through
  `afterResult` leaves `saving` true, so the page does not refocus. OK.
- **Checkbox:** `controlText` = `String(checked)`. `focusTextControlAtLastContent` skips the selection
  range on non-text inputs, so a number, date or checkbox control does not throw. OK.
- **Enum select and YAML textarea:** both read `.value`. OK.
- **List editor:** `controlText` = the JSON of the item input values. The `focusout` guard is in place and
  focus goes to the first item. OK (see optional items).
- **Key editor:** the refused `activeFrontmatterEdit` is the object rebuilt in `saveKey`, and its
  `cancel()` sets the shared `cancelled` flag. OK.
- **Pending new field:** the refusal already clears the pending edit, and closing it is harmless. OK.
- **Click on the same field's cell:** `edit.valueCell === cell` → no close, and the open is a no-op. The
  editor stays and Escape still closes it. OK.
- **Click on the editor's own controls or menu:** the menu sits inside `[data-okf-frontmatter-editor]`,
  and the field click handler returns early. OK.
- **Race (the result arrives after the writer moved):** focus on another cell (tabindex) or another
  control → `focusLost` is false, so the page does not refocus. A click during the save keeps today's
  no-op. OK.

## 2. Tests

- I verified that the new tests fail without the fix. I built a scratch copy of HEAD with `src/` taken
  from HEAD~1, compiled it with tsc and ran `out/test/page/runtimeFrontmatterEditor.test.js`: 39 tests,
  34 pass, 5 fail. The 5 failures are refocus, Escape, click-other, changed-value-blur and key refocus +
  blur. The corrected-value + Enter test passes before the fix; it is a regression guard, as in round 0.
  The worktree itself was never modified.
- No existing assertion was changed. No force, retry or timeouts.
- **Real-input RI-T44 (`scenarioRefusedValueKeepsEditorUsable`):**
  - It uses a real mouse and keyboard and `waitFor` polling.
  - Its schema refuses the value for real: `priority` is an integer with maximum 5. The host
    `checkFrontmatterCandidate` refuses it with "Schema validation failed", because a plain save is
    schema-checked.
  - It checks the buffer.
  - It is registered in `run.ts` after RI-T26, and its marker is in `markers.ts`.
  - It compiles (part of `just check`).
  - Part 2 fails without the fix: no refocus, then the title click opens nothing, so `waitForEditor`
    times out.
  - Not run locally, per the rules.

## 3. Requirements

- Only `SwRS-MDOKFSTUDIO-FMEDIT-019` and `SwRS-MDOKFSTUDIO-BLOCK-041` changed. Both are
  `req_lifecycle: proposed`.
- No approved requirement changed, including generated lines.
- The new rows match the note. Both known issues are removed.
- Generated `implemented_in_files` / `tested_in_files` entries were added (pageInput.ts, markers.ts,
  runtimeFrontmatterEditor.test.ts).
- The markers are correct: `@implements_req` on the new functions and on the click handler,
  `@tests_req` on each new test.
- `okfreq validate --check-links`: 1072 requirements, 0 errors, 21 warnings. All warnings are
  pre-existing W2 palette cross-links.

## 4. Minimal diff on frontmatterValueEditor.ts

4 added lines: `focusControl` and 2 blur/focusout guards plus 1 comment. The refused-state logic lives in
frontmatterEditor.ts. This fits the stacked CR 219.

## 5. Gates

`just check` (rerun by the Inspector): exit 0, unit 3326/3326, contracts 71/71, security 0, markers,
limits, exports, coverage `--check`: 0 files would change. No flake on this run. The "HANG DUMP written"
lines are the fixtures of the CR 173 watchdog tests.

Shots after-refused-{dark,cream} and after-click-other-{dark,cream} show what the note describes. The
title editor is open, priority is back at 2, and the refused value shows with its message. There is no
focus ring after the programmatic focus; the coder already reported this.

## Optional items (not blocking)

1. The refocus condition includes "inside the value cell", and the field menu/picker sits inside the
   editor. A writer who opens the Add field picker while the save runs gets the focus pulled back to the
   control when the refusal arrives. A fix: exclude `[data-okf-frontmatter-menu]` from `focusLost`.
2. The list editor refocuses its first item, not the one being edited, and no unit test covers it.
3. The Escape unit test has a conditional branch (`if activeElement === control`). An unconditional
   control Escape would read more clearly.
4. RI-T44's message "the refused value is not posted again" cannot detect a re-post, because the host
   would refuse it as well. The real proof is the same-click open. Rewording the message would help.
5. Enter on the unchanged refused text still posts it again. The note allows this; it is mentioned only
   for the record.

VERDICT: APPROVE
