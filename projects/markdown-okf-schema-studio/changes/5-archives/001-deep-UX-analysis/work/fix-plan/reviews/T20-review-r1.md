# T20 review — round 1

Base: 21106e0 · Reviewed diff: 4 task files (scrollSync.ts +8/-1, scrollSync.test.ts +60/-2,
realInput.test.ts +58, capture.py +6/-1). Ignored: `test/visual/screenshots/` (killed-run leftovers)
and `book/chapters/05-skills.md` (pre-existing worktree change, not from this task, must not be in
the T20 commit).

## Gates
compile: PASS (logs/T20-compile.log) · unit: PASS (logs/T20-unit.log) · types: PASS ·
trusted: PASS incl. RI-T20 "26-boolean-one-click" (logs/T20-trusted.log). The "CodeWindow: failed to
load" lines are the usual electron noise. visual: not run yet (orchestrator, after restore).

## Done-when
- [x] One click on a boolean value cell toggles and saves — unit "one click on a boolean value cell
  toggles and saves it" (fieldValue true, label "true", "Saving frontmatter…"), "…true…saves false".
- [x] Name cell still opens key editor; reading mode inert — unit guard test.
- [x] RI-T20 real mouse click → buffer `annotation_exemption: true`, one-line delta, no editor left;
  failed before the fix (logs/T20-pre-trusted.log, timeout).
- [x] unit and trusted gates pass.

## Protected features checked
- Keyboard flow: keydown listener untouched; existing checkbox test now drives it via Enter and keeps
  all assertions.
- Validation errors / null button: toggle goes through the normal `saveValue()` (guarded by
  `edit.saving`, so the later blur cannot double-post); error path unchanged. Null button untouched;
  a null boolean toggles to `true` (`value !== true`), reasonable.
- P-E8 read-only: click listener still returns when `!editMode`; tested.
- P-S2/P-S4: no new message type or innerHTML.
- Webview template rules: no backticks, `${`, or new timers in the added runtime lines.
- Non-schema boolean rows (`schemaFound` false) fall back to just opening the editor — safe.

## Findings
1. [NIT] scrollSync.test.ts — the amended existing test also dropped `stopPropagation` from the
   event object; harmless for keydown.
2. [MINOR] Do not include `book/chapters/05-skills.md` or the screenshots folder in the T20 commit.

## Existing assertions changed
- scrollSync.test.ts "boolean frontmatter values use a checkbox and save on change": click → keydown
  Enter; all assertions kept — OK (amended task).
- capture.py `frontmatter-boolean`: click → focus + Enter for this target only; checks kept — OK.

VERDICT: PASS
