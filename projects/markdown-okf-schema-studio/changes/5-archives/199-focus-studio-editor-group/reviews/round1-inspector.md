# Round 1 — Inspector review (CR 199)

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-199 (uncommitted, on 198 head 31a540b3).

## Verdict: APPROVE (non-blocking notes below)

## 1. Rebuttal of the request's diagnosis — verified against run 40806677284

`gh run view 40806677284 --log-failed` (stress, round 2/20, slash-menu) holds two different dumps:

- The dump printed first ("Real-input failure: …") shows the active element
  `div.editor-group-container.active.empty` ("Editor Group 1 (empty)"), editor tab **none**, and
  "Webview host frames … none attached". Its last focus move is `-1003 ms focusin … Editor Group 1 (empty)`,
  which the at-timeout dump does not have. Its trace is the same as the at-timeout trace, shifted by
  1607 ms (-18541 vs -16934 for the first entry). So it was read **after** `withDocument`'s cleanup
  (`closeAllEditors`). The Coder is right.
- The dump embedded in the error (read when `waitMenu` timed out) shows part `webview`, active element
  `iframe.webview.ready`, editor tab "smoke.md, preview", the host frame `index.html id=5c1c…` with
  `hasFocus=true`, active element `iframe#active-frame`; the page has `pageFocus:true`, active = textarea, no
  blur in the page trace. No focus was stolen at the failing step.
- The host focus moves (`focusFirstEditorGroup` at -3003/-1179 ms) are the product's `groupFocus`
  records, not harness calls.

The empty group 1 is the normal layout left by `closeAllEditors`, not a leftover. The request's premise does
not hold; the Driver must word the PR accordingly (test race + misleading post-cleanup dump).

**Undo race hypothesis: plausible and sound.** I checked the product path: `textControls.ts` `hostEditKey`
cancels Cmd/Ctrl+Z and `runEditCommand` applies `document.execCommand("undo")` only when VS Code sends
`previewEditCommand` back, so each undo is an extension-host round trip while typed keys land at once. The
old code pressed 6 undos blindly and only waited for `original`, which needs fewer steps; late undos then pop
the next native undo group. The observed value `Second paragraph.tab` (the `\n/` group gone, `tab` kept, so
the menu never opens) fits exactly. The fix presses one undo at a time and waits for its visible effect, so
it presses only what is needed and nothing is in flight. Native `execCommand` undo steps always change the
value, so `undoOneStep` cannot wait on a no-op in this scenario. No sleep added (a 120 ms sleep is removed),
no retry, no raised timeout, assertions unchanged ("one undo brings the /h2 back", "undo reached the bare
heading prefix", back to `original` is now enforced by `undoUntil`, which fails with the values seen).

## 2. `focusFirstEditorGroup` → `waitForActiveSourceEditor`

Correct in every changed test: each use follows `showTextDocument(doc, ViewColumn.One)` (focusing, no
`preserveFocus`) and precedes a step that needs the **source** editor (Studio command or `undo`), never the
Studio. `waitForActiveSourceEditor` checks the state first, then waits on `onDidChangeActiveTextEditor`
(disposes its listener on both paths; 10 s bound with the host report). findInPreview:263 swap of order
(focus command removed from before `showTextDocument`) is right. It checks `activeTextEditor`, not DOM
focus; that is the same guarantee `showTextDocument` already gave, and no new window was opened compared
with the old position-based command. Remaining group-index commands: `checkboxToggle.test.ts:142` (kept,
harmless: no preview open yet) and `realInput/previewWindow.ts` (the group-lock scenario, which needs
positions by design), plus the product `groupFocus.ts` (LIFE-151). All acceptable.

## 3. ALERT-PICK-PROBE

Moved out of `STRESS_SCENARIOS` (run.ts) and `STRESS_SCENARIOS_BY_HOST.trusted` (stressPlan.ts) together,
so the `assert.deepEqual(Object.keys(STRESS_SCENARIOS), …trusted)` check stays consistent. Runs once in
the integration list after `scenarioAlertDropdown`; still available as single scenario
`alert-type-pick-probe`. `probeAlertPick` assertions untouched (only doc comments changed).

## 4. Dump change

Correct and useful: `withFocusDumpOnFailure` reads the dump before `withDocument`'s `finally` cleanup and
rethrows the same error; nested `withDocument` keeps the first dump (`??=`); run.ts prints the at-failure
dump then the post-cleanup one, each labelled. An empty host-frame section now says why
(`explainMissingHostFrames`). Unit-tested, including the CI ordering. Note: request item 3 ("fix none
attached") is resolved by explanation, not by finding a missing frame, because the frame really was gone.

## 5. Compatibility (3-way merges with real merge bases, `git merge-file`)

- **#205** (`run.ts`, `stressPlan.ts`): 198 + #205 **already** conflict at the end of the stress map. With
  this change on top of 198 both files merge **cleanly** (toc kept, probe gone). The Coder's report says the
  opposite; correct it in the hand-back.
- **#206** (`editorWidgets.ts`, shared step helpers): no overlap, clean.
- **#193** (`checkboxToggle.test.ts`): one **trivial conflict on the import line** (`windowFocus` import
  vs #193's added `markProgress`/`bounded` imports). The Coder's "no shared lines" is not exact.
  Resolution: keep both imports. The line-174 hunk merges cleanly.

## 6. Gates (run by me)

`just check`: exit 0. Node unit tests 3188/3188, second suite 69/69, pytest 80 passed,
`okfreq validate`: 1067 requirements, 0 errors, 0 warnings; lint 0 indexes would change; coverage 0
files would change.

## Scope "replace with focusing the Studio group" not done — acceptable

Every harness use targeted the source editor in column One, never the Studio; replacing them with
"focus the Studio group" would have broken those steps (the Studio command and `undo` need the text
editor). The real failure was not a focus loss. Waiting on reported state (active text editor) is the
right replacement. The empty-group question is answered (post-cleanup layout). The Driver must state
this deviation in the PR body.

## Non-blocking notes

1. Hand-back/PR: fix the compatibility statements (#205 merges cleanly with this change; #193 has a
   one-line import conflict).
2. `undoSteps.test.ts` first test models the hypothesis but ends at `"Second paragraph."`, not the CI
   value `"Second paragraph.tab"`. Optionally land one queued undo between typing `\n/` and `tab` to
   reproduce the exact CI value. Either way the PR must say the race is inferred and the proof is the
   two heavy runs.
3. Follow-up after #193 lands: replace `checkboxToggle.test.ts:142` with
   `waitForActiveSourceEditor(document)` inside `bounded(...)`.
4. `failureDump` is module state cleared only by `takeFailureFocusDump()`; a scenario error swallowed by
   a caller would leave a stale dump for a later failure. I found no such caller today (the
   `frontmatterFields.ts:305` `try` is a `finally`); keep in mind.
