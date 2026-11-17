# Review round 3: frame focus loss redo (CR 205)

Inspector, 2026-10-31. Scope: `git diff HEAD` in `markdown-okf-schema-studio-wt-205`. The focus is
on `test/shared/editorBlurInterruption.ts`, `test/build/editorBlurInterruption.test.ts` and
`test/integration/realInput/editorWidgets.ts`. The stress-input files (`ci.yml`, `justfile`,
`test_workflows.py`, `ci.guidelines.md`) were approved in round 2 and have not changed since.
Evidence: `/private/tmp/claude-502/cr205-driver/repro-facts.md` and `stress1.log` (CI run
41145454738, stress round 40/100, alert-dropdown).

## Gate

`just check` was run once in the foreground: **exit 0**.

- Node unit tests: 3259 passed, 0 failed, 0 skipped. Second suite: 71 passed. pytest: 139 passed
  (12 warnings).
- check-boundaries (310 modules), check-limits (882 files) and check-settings (19) all passed.
- The new tests ran: `the CI trace: a frame focus loss inside a focused window ...` and
  `no window loss: a frame focus loss, named so ...`.

## (1) Does the rule match the trace, and does the new test fail on the old code?

**Yes, on both.** The page trace in the fixture matches `stress1.log` event for event. The commit
is `related=none commit active=body pageFocus=true` at 722 and the page blur is at 723. The only
press since the step start was the alert press at 502, which is before the step start at 579, and
no `option=WARNING` mousedown appears anywhere. The rule really does turn this trace from "no
redo" into "redo".

I ran the new test file against the old `editorBlurInterruption.ts` (HEAD, transpiled into a
scratch copy of `out/`). 4 of the 10 tests fail. The CI trace test fails on its first assertion
(`false !== true`). The other three that fail are the changed existing assertions. So the new test
does reproduce the CI failure on the old code.

Two places where the fixture does not match the trace (minor, but the comment claims it does):

- **The window-state event is in the wrong place.** In the log, `windowStates` is
  `[{at: 927, focused: true}]` on the scenario clock. The page blur at 723 (page clock) is 864 on
  the scenario clock. So the host saw a window-state change **63 ms after the page blur**, not
  "at the very end". The fixture puts it 704 ms after (10 927 vs 9 500 + 723). It also sets
  `stepStartedAt` to 10 000 while page clock 579 gives wall 10 079.
- **What the event is.** `onDidChangeWindowState` fires on a change of `focused` or `active`.
  The recorder keeps only `focused`, so a `focused: true` event with no earlier `false` was most
  likely an `active` change. Either way, something changed at window level 63 ms after the frame
  lost the focus. The rule ignores it and the reason does not mention it.

## (2) Does the change weaken a legitimate negative?

**Yes, in a way that matters. This is the blocking finding.**

The old redo needed an **external, positive** cause: the host proved that the VS Code window lost
the OS focus at the moment of the page blur. The new frame branch (lines 122–131) redoes when:

- no press reached the page,
- a commit to nowhere is followed by a page blur within 50 ms, **and**
- the host recorded **no** window focus loss.

The last condition is absence of evidence. It does not tell an environmental frame loss apart from
**a frame loss the product caused.** The product moves the workbench focus on its own in several
places:

- `src/host-vscode/groupFocus.ts`: `workbench.action.focus*EditorGroup`, run by background focus
  work (LIFE-151).
- `src/host-vscode/groupLock.ts`: `lock`/`unlockEditorGroup`.
- `src/host-vscode/activation.ts:210` and `previewPanel.ts:68`: `panel.reveal()` without
  `preserveFocus`.

The same CI dump shows two such product moves (`focusFirstEditorGroup`) at −3 836 and −1 006 ms,
about a second before the scenario. Suppose one of these lands during the Warning pick as an
intermittent race, for example a late group-unlock job. That produces exactly this signature:
textarea blur `related=none pageFocus=true`, a page blur 1 ms later, no press, and the window
still focused. The new rule redoes it and the run is green. The race only shows if it hits both
attempts. CI rule 12 says a flake is "a race in the product or the test", to be traced "through
each code path that can produce the observed state". This change accepts an unexplained focus loss
as environmental without excluding the product's own focus paths.

The evidence that would make the frame branch a real proof is **already collected by the harness,
but the rule does not use it**:

- `previewGroupFocusMovesForTests(since)`, the product's own focus commands. The CI case has none
  during the step.
- The workbench focus trace from `workbenchFocusDump.ts`: focusin/focusout/window-blur in the main
  document. The facts say there was none after the step start, and the active element was still
  `iframe.webview.ready` with `hasFocus=true`.

With both as required conditions, the CI trace would still be redone, and a product focus steal
would be refused. Without them, the single redo is not "proven": it is a retry on an unexplained
blur. That is what the owner ruled out.

### The three changed existing assertions

1. **`inFocusedPage` with a window loss → redo (was: fail).** This is **not justified by the
   trace.** The CI case went down the no-window-loss branch, so the window branch did not need to
   be loosened. With a real window loss, `document.hasFocus()` is already false at the element
   blur, which the old comment and the new comment both say. `pageFocus=true` together with a host
   window loss within 1 s means a frame loss first (possibly product-caused, see above) and then a
   window loss that happened to fall near it. Keep `pageFocus=false` required on the window
   branch. Accept `pageFocus=true` only on the frame branch, and only with its proof.
2. **`beforeStep` (window lost at 9 990, before the step, never regained) → now named a frame
   focus loss.** The window was **unfocused for the whole step**, yet the reason says "the VS
   Code window kept the focus". The reason is false. The case should fail, or at least not be
   named a frame loss.
3. **`earlier` (lost at 9 900, regained at 10 100) → redo (was: fail).** This is the worst of the
   three. The window was unfocused at the step start and **regained the focus at 10 100, 1 ms
   before the page blur at 10 101**. That is a window-level event exactly on the blur, not "a
   window that kept the focus". The old code was right to fail this case. The new test now locks
   in the wrong answer.

Both 2 and 3 come from the frame branch filtering only `!focused && at >= stepStartedAt`. It never
checks that the window was focused **at** the step start, and it ignores focus *gains* during the
step.

The untouched negatives still hold: a press that reached the page, a commit with
`related=<element>`, a page blur more than 50 ms later or after a page focus, and a different page
document.

## (3) The redo path when the window never lost focus

This part is acceptable. `ensureTestWindowFocused()` returns at once on Linux, or when the window is
already focused. Then:

1. The redo waits for the committed editor to close.
2. It waits for the host block edit to settle and for the committed NOTE in the buffer.
3. It resets the document and waits for the render.
4. It runs `openTypeList()`, which clicks into the frame and then waits for "steady editor"
   (`activeElement` is a textarea, `document.hasFocus()` is true, the list is open).

So if the frame never gets the focus back, the redo fails with the full dump and
`(redone after: …)`. It is not masked. The comment in `editorWidgets.ts` ("needs no window
activation then") is accurate. The log line `step("focus loss: …")` is fine.

## (4) Honesty of the reason text

- The frame reason says **"the VS Code window kept the focus"**. That is false in cases 2 and 3
  above. Even in the CI case it is only true of the recorded `focused` flag: it hides the
  window-state event 63 ms after the blur. The reason should report what was seen, for example "no
  host window focus loss during the step; window states during it: focused:true at +63 ms from the
  page blur". The recorder should also keep `active`, so the next dump can tell an activity change
  from a missed focus loss.
- The module header (lines 1–5) and the `editorBlurBeforePress` JSDoc (line 60, "lost to a window
  blur") still describe a window-blur-only proof. The `witnessPress` JSDoc in `editorWidgets.ts`
  says the same ("lost to a window blur").
- The list item at lines 69–70 still says the page blur is "the window blur that made the editor
  commit". On the frame branch it is the frame's blur.
- The rejection prefix "no block editor commit on a page focus loss" and the shorter "not a blur
  to nowhere" are accurate.

## Verdict

CHANGES REQUIRED

1. **Make the frame branch a positive proof.** Pass the product's focus moves during the step
   (`previewGroupFocusMovesForTests(stepStartedAt)`) in the host witness and require that there
   are none. Also require that the workbench focus trace shows no focusin/focusout/window-blur in
   the main document from the step start to the verdict, with the webview iframe still the active
   element (the evidence the CI dump already had). Add a unit test for each: the CI trace plus a
   product `focusFirstEditorGroup` during the step gives no redo, and the CI trace plus a
   workbench focusin on another part gives no redo.
2. **Require the window to be focused at the step start and through the page blur** on the frame
   branch. Record `vscode.window.state.focused` (and `active`) at `witnessPress` time, and do not
   treat a focus *gain* near the page blur as "kept the focus". Restore the old outcome for
   `earlier` (no redo). Make `beforeStep` fail, or name it truthfully.
3. **Keep `pageFocus=false` required on the window-loss branch.** Revert the `inFocusedPage`
   assertion to "fail with a window loss". `pageFocus=true` is accepted only on the
   frame-loss branch.
4. **Reason text:** list the window states seen during the step instead of saying "kept the
   focus". Record `active` in `windowStates`. Update the module header, the JSDoc of
   `editorBlurBeforePress` (lines 60 and 69–70) and the JSDoc of `witnessPress` to cover both
   kinds of interruption.
5. **Fixture accuracy:** put the CI `focused:true` window state 63 ms after the page blur, and
   make `stepStartedAt` agree with page clock 579. Fix the comment that says "at the very end".

The stress-input files from round 2 stay approved.
