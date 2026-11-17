# T28 implementation — round 1

STATUS: DONE

## Summary
In edit mode the webview runtime now adds a zero-height insertion point (`.sphinx-preview-insert-point`,
`data-sphinx-insert-after-line="N"`, one `+` button) after each top-level mapped block (after the
enclosing `pre` for code), and after the properties section with N=0. An empty or frontmatter-only body
(only on a successfully rendered preview) gets a single `Start writing` point with N=0. A click opens
`openBlockEditor(point, undefined, {line: max(1,N), endLine: max(1,N), insertAfterLine: N}, "end")`;
`insertAfterLine` is carried in `previewEditOpen`, `previewEditSave` (autosave and final) and
`previewEditCancel`. The empty textarea gets the placeholder `Type Markdown, for example "## Heading" or "- item"`.
Points are removed in reading mode and rebuilt on each toggle and at init. CSS keeps layout unchanged.
Host code (T27) is untouched.

## Files changed
- src/webview/scrollSync.ts — insertion points, `insertAfterLine` in openBlockEditor/active edit/messages, placeholder, hint prefix "New block" for insertions, early returns for `.sphinx-preview-insert-point` in the document click and keydown handlers
- src/preview/previewStyles.ts — insertion point CSS (zero height, gutter button, hover/focus reveal, `Start writing` variant)
- test/webview/scrollSync.test.ts — harness options (`emptyBody`, `propertiesMapped`, `previewStatus`, `removed` flag, `.sphinx-preview-insert-point` in fake `closest`), 12 new T28 tests
- test/webview/previewStyles.test.ts — T28 CSS test
- test/visual/scenarios.ts — scenario `edit-insert-point-hover` (fixture 04-code-and-tables; reuses the existing `editAffordances` flow, whose hover PNG shows the revealed + button; capture.py unchanged)
- test/integration/realInput.test.ts — RI-T28
- README.md — Edit mode sentence

## Tests written first (failing before the fix)
12 of 14 new T28 unit tests failed before the implementation (2 negative tests, "failed render offers no Start writing" and "ordinary block edits never carry insertAfterLine", pass by design). Log: scratchpad `red.log`. Failing: CSS test, edit-mode points, init points, properties point, empty body point, frontmatter-only point, click posts previewEditOpen, Start writing click, document-level guard test, empty reply/Done saves, Done on untouched empty closes, autosave/Revert carry insertAfterLine. Typical excerpt: `an insertion point after line 52` assertion (`undefined` is not ok) and the CSS regex `PREVIEW_THEME_CSS` not matching `.sphinx-preview-insert-point`.
RI-T28 was written together with the fix (real-VS Code run needs the implementation), so it has no separate red run.

## Tests added or changed
- 12 T28 unit tests in scrollSync.test.ts: points after each block with right N and none in reading mode (and recreated, not duplicated), init in edit mode, properties N=0, Start writing (empty, frontmatter-only, not on failed render), click messages, guard against document-level handlers, empty textarea + placeholder + Done saves with `insertAfterLine` and `originalText: ""`, untouched Done closes without saving, autosave/Revert carry `insertAfterLine`, ordinary edits do not.
- previewStyles T28 test: zero-height point, gutter button geometry, hover/focus reveal, Start writing variant.
- RI-T28 (real input): empty `scratch` document, Start writing, typed heading + two Enters + paragraph, Done, buffer exactly `# Incident review checklist\n\nFirst paragraph.\n`; hover heading, click its +, type `- check logs`, Done, buffer exactly `# Incident review checklist\n\n- check logs\n\nFirst paragraph.\n`; edit mode off/on changes scrollHeight and last paragraph top by at most 2 px.

## Existing assertions changed
- test/webview/scrollSync.test.ts:"activating a centered block editor preserves scroll before and after layout stabilization" — old: `harness.mappings[1].insertedElements[0].getBoundingClientRect().top` → new: `blockEditorOf(harness.mappings[1]).getBoundingClientRect().top` — required by: insertion points are also recorded in the fake's `insertedElements`, so index 0 is no longer the editor (same assertion, editor located by attribute).
- test/webview/scrollSync.test.ts:"fenced Markdown editors sit outside the rendered pre..." — old: `pre.insertedElements[0]` → new: `blockEditorOf(pre)` — same reason. (`code.insertedElements.length === 0` still holds because the point is placed after the `pre`.)

## Verification
- `PLAN/scripts/gate.sh T28-impl unit types trusted scroll visual`:
  - unit PASS (logs/T28-impl-unit.log; 582 pass, 0 fail in the earlier direct run)
  - types PASS (logs/T28-impl-types.log)
  - trusted PASS incl. RI-T28 (logs/T28-impl-trusted.log; screenshots 24-start-writing-open, 25-block-inserted)
  - scroll PASS (logs/T28-impl-scroll.log)
  - visual PASS vs baseline, 0 new failure lines (logs/T28-impl-visual.log); the gate reported "4 baseline line(s) now passing", not caused by this task as far as I can tell. screenshots folder was clean afterwards.

## Evidence for reviewers
- logs/visual-T28-impl/edit-insert-point-hover-hover.png: round + in the left gutter below the hovered list, no layout shift.
- RI-T28 evidence screenshots 24 and 25 in the real-input evidence folder.

## Open points / STOP reason
- Hint text for an insertion editor reads `New block · Enter: new line · ...` (instead of `Line 1`, which would be wrong for N=0); the rest of the T15 hint is identical.
- "Start writing" requires `[data-sphinx-preview-status]` to be `success`/`recovery` (hasRenderedPreview), so a failed render never offers it.
- Clicking + while another block editor is open first commits that editor through blur; a second click is then needed (existing "one editor at a time" rule).
- The visual scenario cannot hover the + itself without changing capture.py (not allowed); it relies on the existing list-hover step of `editAffordances`, which reveals the + below the list.
