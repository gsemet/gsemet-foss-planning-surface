# T10 review — round 1

Base: 3a1c944 · Reviewed diff: 3 files, about +105/-0 (scrollSync.ts +13, scrollSync.test.ts +29,
realInput.test.ts +66)

## Gates
compile: PASS · unit: PASS · types: PASS · trusted: PASS (logs/T10-trusted.log, exit 0; 47 s).
No new failure compared with the T00 baseline. The implementer's red run
(logs/T10-impl-red-trusted.log) shows RI-T10 open-with failing before the fix.

## Done-when
- [x] `unit` and `trusted` gates pass: orchestrator gate summary and logs/T10-trusted.log.
- [x] RI-T10 passes in the side preview and the Open With editor: `scenarioUndoStaysInEditor`
  runs for both modes in `run()`. The screenshots `16-undo-stays-side` and
  `16-undo-stays-open-with` were captured; the open-with PNG shows the block editor still open on
  "Second paragraph. abc def" after redo.
- [x] Report states the approach: approach A shipped, so B was not needed. The red excerpt proves
  that the bug reproduced before the fix (`{"tag":"BODY"}`, document undo ran).
- [x] Unit test for approach A: "undo and redo shortcuts stop at the block textarea and keep the
  native undo". It covers Meta/Ctrl+Z, Shift+Z and Ctrl+Y (stopPropagation, no preventDefault). It
  also checks that plain z/y, Cmd+S and Alt+Cmd+Z are not intercepted and that no message is sent.

## Protected features checked
- P-E3/P-E4 (raw editor, arrow navigation): `keepUndoInControl` returns early only for
  modifier+Z/Y, so `navigateBlockEdit`, Escape and Enter paths are unchanged. They stay covered by
  the existing scrollSync unit tests and the RI scenarios 01–15, which all passed in trusted.
- P-E8 (read-only): the helper lives only inside listeners of controls that exist in edit mode, so
  no new interactive surface appears in read-only mode.
- P-S2/P-S4: no new message types or fields, and nothing new reaches `innerHTML`.
- Must-not-change: Cmd/Ctrl+S is not intercepted (unit case). Document undo outside inline
  editors is untouched because only control-level listeners changed. Copy, paste and find keys
  are not matched (keyCodes 90/89 only).
- Conventions §2: the runtime code has no backtick, no `${`, and no backslash. It uses `?.()`,
  which matches existing runtime usage.

## Findings
1. [MINOR] scrollSync.ts frontmatter key/value keydown listeners: the helper is wired in, but no
   test covers it. Follow-up: add a unit test that dispatches a Meta+Z keydown on a frontmatter
   text control and asserts that stopPropagation is called once and preventDefault is not.
2. [NIT] RI-T10 accepts any strict prefix after undo, which is looser than the task's "ends with
   ` abc`". The report justifies it: Chromium undoes by word. The redo assertion is exact, so the
   test still fails without the fix.

## Existing assertions changed
None.

VERDICT: PASS
