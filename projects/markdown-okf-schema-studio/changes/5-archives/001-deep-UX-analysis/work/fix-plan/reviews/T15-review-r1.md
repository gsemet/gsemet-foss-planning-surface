# T15 review — round 1

Base: b9317ba · Reviewed diff: 8 files (README, previewStyles.ts, scrollSync.ts, realInput.test.ts,
capture.py, scenarios.ts, previewStyles.test.ts, scrollSync.test.ts)

## Gates
compile: PASS · unit: PASS · types: PASS · trusted: PASS (logs/T15-trusted.log, RI-T15 included) ·
visual: PASS vs T00 baseline, 0 new failure lines (logs/T15-visual.log).

## Done-when
- [x] unit, trusted, visual gates pass; RI-T15 passes — orchestrator gate summary + `scenarioEditAffordances`.
- [x] Hover outline visible — `visual-T15/edit-affordances-hover-and-open-hover.png`: dashed outline on the
  nested `ul` only, no layout shift.
- [x] Frame, hint, buttons visible, nothing clipped — `edit-affordances-hover-and-open.png`,
  `edit-paragraph-dark.png`: 1px focusBorder frame, opaque editor background, monospace textarea,
  readable "Lines 47–49 · … · Esc or ⌘↩: done", Done (primary) and Revert inside the frame.
  Only the dark theme is captured (the task's scenario defines one theme), acceptable.
- [x] Status `Lines 50–52`, Done/Revert exist, Revert disabled — unit "an opened block editor shows its
  line range, Done and a disabled Revert".
- [x] Revert after autosave posts `previewEditCancel`; without autosave posts nothing, clears timer, blur
  posts nothing — unit "Revert enables on change and cancels only what reached the document".
- [x] Done posts a final save — unit "Done posts a final save and both buttons keep the textarea focused".
- [x] previewStyles assertions for outline, frame, editor font (block + YAML, text field excluded).

## Revert logic (explicitly judged)
- `edit.hasAutosavedChange` is set in `postBlockEditSave` when a save carrying text different from the
  original is *posted* (not when acknowledged), so any autosave that may have reached the document leads
  to `closeBlockEdit(true)` → `previewEditCancel` → host `handlePreviewEditCancel`, which sets
  `pendingText = edit.originalText` (text when the editor opened) and drains after the queued save.
  Messages are ordered, so a save still in flight is overwritten by the restore. RI-T15 proves this on a
  real buffer (type ` R`, wait 600 ms, Revert → buffer equals original).
- Without an autosave, `closeBlockEdit(false)` clears the pending debounce timer before it fires and
  removes the editor; the textarea blur that follows finds `activeBlockEdit` undefined, so nothing is
  posted. No text reaches the document, nothing to restore. Correct.
- Revert never discards text from before the editor opened: the cancel restores only `originalText` of
  this edit session. Revert stays enabled after autosave even if the user typed back to the original,
  which correctly allows undoing the autosaved state.
- Revert is the only cancel caller; Escape/blur/Cmd+Enter/edit-mode-off still commit (T08 semantics
  unchanged; existing tests untouched and passing).

## mousedown preventDefault
Both buttons call `preventDefault` on `mousedown`, so the textarea keeps focus and its blur commit does
not run before `click`. Verified by unit test and by real clicks in RI-T15 (Revert would otherwise have
committed ` R`). Correct.

## Sticky band style tag in the new scenario
`check_edit_affordances` injects `display:none` on the sticky heading band. Each scenario runs on a fresh
`context.new_page()` (capture.py:2618), so it does not leak to other scenarios, and only this new scenario
is affected. T15 does not touch the sticky band; the band/toolbar overlap is a baseline failure. It does
mean `overlay-clipped` in this scenario cannot detect the band covering the editor frame or buttons; the
existing `edit-*` scenarios still run with the band visible and pass. Acceptable (MINOR note below).

## capture.py frame check
`check_preview_edit_mode`: `borderWidth != "0px"` → "still has a frame" became `borderTopWidth != "1px"`
→ "no visible frame". This inverts an assertion that encoded the old, now intentionally changed design
(step 2), and the task's "Expected changes to existing tests" names it. Not weakened: it now asserts the
new frame exactly. OK.

## Protected features checked
- P-E (inline editing, Escape/blur/Cmd+Enter commit, Tab indent, list continuation, undo): handlers not
  changed beyond adding buttons and a hint; existing scrollSync tests and the RI scenarios
  (TabIndents, CaretAtClick, PreviewKeepsMarkdown…) pass in trusted.
- P-E8 read-only: hover uses `editMode`, false when edit mode is unavailable; buttons exist only inside an
  opened editor.
- P-S2/P-S4: no new message types; Revert reuses `previewEditCancel` with version/editId checks; button
  text and hint set via `textContent`.
- P-N1 R7: editor got 6px 8px padding + border; edit-paragraph/admonition/list scenarios and anchoring
  tests pass in visual and trusted.
- P-R6/UX-34 sticky text, UX-22, UX-24: untouched.
- Table cell editor visuals: the frame rule is on `.sphinx-preview-block-editor`; table-cell editor class
  unchanged (edit-table scenarios pass).
- Conventions §2: new runtime code has no backtick or `${`, `\u` escapes are inside the TS template as
  string escapes that the existing tests exercise, `navigator` guarded with try/typeof, timers via
  `window.setTimeout` only.

## Findings
1. [MINOR] README.md "Edit mode" paragraph — rewrapped one sentence per line instead of at 100 columns
   with several short clauses per line, which the orchestrator note and AGENTS.md ("Do not force one
   clause per line") ask for. Fix: rejoin into lines filling up to 100 columns, breaking at clause
   boundaries; no wording change.
2. [MINOR] scrollSync.ts `receiveBlockEditSource` — Done/Revert are not reachable from the textarea by
   keyboard because Tab indents (T14). Escape still commits, so no keyboard path is lost, but Revert has
   no keyboard equivalent. Follow-up: consider a shortcut or document it.
3. [MINOR] capture.py `check_edit_affordances` — hiding the sticky band means this scenario cannot catch
   the band covering the editor. Follow-up once the baseline sticky/toolbar failure is fixed: remove the
   injected style tag.
4. [NIT] Status line sits ~1em above the buttons (paragraph margin wins), visible in screenshots;
   cosmetic, as the report notes.

## Existing assertions changed
- scrollSync.test.ts "edit mode loads raw Markdown…": Done/Revert existence added, no-Save/Cancel kept — OK.
- previewStyles.test.ts `::before` marker assertions → frame assertions (step 2) — OK.
- previewStyles.test.ts frontmatter test, editor rule `padding:0;border:0;background:transparent` → frame — OK.
- previewStyles.test.ts block textarea `font: inherit` → editor font-family — OK.
- capture.py `check_preview_edit_mode` frame check inverted to require the 1px frame — OK (listed in task).

VERDICT: PASS
