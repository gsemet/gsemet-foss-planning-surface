# Round 1 — Coder report (CR 199)

Worktree `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-199`, branch
`change-requests/199-focus-studio-editor-group` (on 198 head 31a540b3). Uncommitted; only `test/` touched,
no product code.

## Main finding: the evidence in 00-request.md was misread

I re-read the failed stress log of run 40806677284 (slash-menu, round 2/20). It holds several dumps:

1. The dump inside the error (`windowFocusReport`, read when the wait timed out) shows the Studio
   **keeping the focus**. The workbench active element is `iframe.webview.ready` and the focused part is
   `webview`. The outer `index.html` frame is attached, with `hasFocus=true` and active element
   `iframe#active-frame`. The page has `pageFocus:true`, and its active element is the block editor's
   textarea. The page trace has no blur after "block editor focused".
2. The dump with "Editor Group 1 (empty)" and "none attached" is the one printed by
   `realInput/run.ts`'s `catch`. That runs after `withDocument`'s `finally` (`leaveEditModeOff` +
   `closeAllEditors`) has closed the preview. Three things show this:
   - its focus trace is the same as dump 1, shifted by about 1.6 s;
   - its active tab is "none";
   - its last move (`-1003 ms focusin Editor Group 1 (empty)`) is the cleanup itself.

   After `closeAllEditors`, one empty group is left. That is normal VS Code layout, not a leftover from
   an earlier scenario.
3. The "host focus moves" `focusFirstEditorGroup` at -3003 and -1179 ms come from the **product's**
   group unlock (`groupLock.ts`), not from the harness. They are on the page clock, so both happened
   before the slash-menu page started, inside the previous scenario's `closeAllEditors` +
   `previewGroupUnlocksSettledForTests`.

So no focus was stolen during the failing step. What the box shows is `Second paragraph.tab`: the
**Enter and the `/`** typed after a run of undos were lost, and `tab` arrived. The cause is a test race:

- In a VS Code webview, Cmd/Ctrl+Z is cancelled by the webview host (`index.html`, `isUndoRedo` →
  `preventDefault`) and forwarded as `did-keydown`.
- VS Code runs the key binding, and the extension sends `previewEditCommand` back to the page
  (`textControls.ts runEditCommand`, BLOCK-003). Each press is a round trip through the extension host.
- The scenario pressed undo **6 times blindly**, then waited for `original`. That wait can succeed while
  some of the 6 undos are still on their way. They then land on the keys typed next (End, Enter, `/tab`).
- The earlier undo loop had the same weakness and covered it with a 120 ms sleep.

## Changes

| File | Change |
| --- | --- |
| `test/shared/undoSteps.ts` (new) | `undoOneStep` presses once and waits until the text box value changes. `undoUntil` presses one observed step at a time until the target value, with a budget. Both are pure, and their failures carry the values seen. |
| `test/build/undoSteps.test.ts` (new) | A fake webview text box where undos land late, in order. The first test **reproduces the stress failure**: blind presses, then typing, loses the typed `\n/tab`. Further tests: `undoUntil` leaves nothing in flight, and the failure messages explain themselves. |
| `test/integration/realInput/textEditing.ts` | Slash menu: the undo walk uses `undoOneStep`, so the `setTimeout(120)` sleep is gone. The 6 blind undos plus `expectValue` become `undoUntil(original, 6)`. The assertions are unchanged ("one undo brings the /h2 back", "undo reached the bare heading prefix", back to `original`). Also: `focusFirstEditorGroup` before `undo` (RI-T09) → `waitForActiveSourceEditor`. |
| `test/integration/windowFocus.ts` | New `waitForActiveSourceEditor(document)`. It waits, on an event with a 10 s bound, until VS Code reports the document as `activeTextEditor`. On failure it gives the host focus report. |
| `blockActionsFollowSelection`, `editToolbarCover`, `tallBlockScroll`, `tableEmptyColumn`, `findInPreview` (both uses), `checkboxToggle` (line 174) `.test.ts` | Each `focusFirstEditorGroup` → `waitForActiveSourceEditor(<doc>)`, placed after `showTextDocument(doc, One)`. In findInPreview the focus command came *before* `showTextDocument` and has been dropped. |
| `test/shared/workbenchFocusDump.ts` | 1. `explainMissingHostFrames(urls)`. An empty host-frame section now says why: "no webview is open (N frame(s) in the page: …)", or "webview frames without a recognised index.html host frame (…)". 2. `withFocusDumpOnFailure(page, action, record)` reads the dump when a step fails, before the caller's cleanup, then rethrows the same error. |
| `test/build/workbenchFocusDump.test.ts` | Two new tests. One covers the explanation text. The other reproduces the CI order: the dump read at failure keeps the host frame; the dump read after "cleanup" says "none attached: no webview is open". |
| `test/integration/realInput/common.ts` | `withDocument` wraps the scenario in `withFocusDumpOnFailure`. It keeps the first dump, labelled with the fixture prefix. New `takeFailureFocusDump()`. |
| `test/integration/realInput/run.ts` | The catch prints "Real-input failure, at the failing step: …" when a dump was recorded, then "…, after the scenario's cleanup: …". The ALERT-PICK-PROBE entry moves out of the stress map into the integration list, once, right after `scenarioAlertDropdown`. Its assertions are unchanged, and it is kept as a single scenario (`STUDIO_REAL_INPUT_SCENARIO=alert-type-pick-probe`). |
| `test/shared/stressPlan.ts` | `alert-type-pick-probe` removed from the trusted list. |
| `test/integration/realInput/alertPickProbe.ts`, `test/shared/alertPickProbe.ts` | Doc comments now say "integration, once" instead of "stress". |

## What replaced `focusFirstEditorGroup`, and why

Every harness use of it targeted the **text editor in column One**, never the Studio:

- before `COMMAND_ID`, so the preview opens for that editor;
- or before `undo` in the source.

Each one followed `showTextDocument(doc, One)`, which already moves the focus there. The position-based
command only added a focus move of its own. The next step needs the document to be the active text
editor, so the replacement waits for exactly that state (`waitForActiveSourceEditor`). I added no
"focus the Studio group" helper: no harness step needed one.

The one left is **`checkboxToggle.test.ts:142`**, kept for compatibility. PR #193 rewrites lines 141–142
(it wraps them in `bounded(...)`), so editing them would conflict. It is harmless: group 1 holds the
document that was just shown, and no preview is open yet. After #193 lands, it can become
`bounded("…", waitForActiveSourceEditor(document))`.

**Product `focusGroupCommand` / `groupLock.ts` and `test/host-vscode/groupFocus.test.ts`: unchanged, on
purpose.**

- That code releases the editor-group lock the extension put on a side preview's group (LIFE-151).
  VS Code has no API for group locks, so it needs focus commands by position.
- It records its moves, and tests wait for `previewGroupUnlocksSettledForTests` (`closeAllEditors`).
- In the failing run, both of its moves happened before the slash-menu page started, so they did not
  steal the focus.

## Gates

- `just check`: exit 0.
  - node unit tests: 3188/3188 (was 3183; 5 new);
  - second suite: 69/69;
  - pytest: 80 passed;
  - requirements: `1067 requirements, 0 errors, 0 warnings`.

  Before that, I had to run `uv sync --group docs --group requirements`. Without it,
  `test_plugin_manifests.py` failed to import `jsonschema`, which comes from the requirements group.
  That is an environment issue, not part of this change.
- `uv run --group requirements okfreq validate --check-links --project-root .`:
  `1067 requirements, 0 errors, 0 warnings`.
- No requirement or doc change was needed (test harness only). No CHANGELOG entry: #218 has none for
  harness changes.
- No real-window run was done locally; heavy CI is the proof.

## Compatibility

- **#206** (`editorWidgets.ts`, `stepInterruption`, `editorBlurInterruption`) and **#205's
  `harness.ts`**: no shared lines.
- **#193**: `checkboxToggle.test.ts` line 142 is left alone. My hunk at line 174 is outside its hunks.
- **#205 / #218 list ends**: removing the `alert-type-pick-probe` lines conflicts as add/delete with
  #205's `toc` entry, which sits next to them in the stress map of `run.ts` and in `stressPlan.ts`. I
  checked this with `git merge-file` on 198 + 205. The conflict cannot be avoided, because the deleted
  lines are next to the added ones. Resolution: keep `toc` (with its import) and drop
  `alert-type-pick-probe` in both files.

The integration-list insertion (after `scenarioAlertDropdown`) touches no other PR's hunk.

## Open doubts

- The undo race is **inferred**. It fits the lost Enter + `/` with `tab` kept, the forwarded-key
  design, and the at-failure dump showing no focus loss. No CI log shows an undo landing late. The proof
  is the two heavy runs with slash-menu green. If it fails again, the `undoUntil` / `undoOneStep`
  messages now list the values seen.
- The request's premise (a workbench focus thief in an empty group 1) does not survive the log. The
  Driver should update the PR wording: the slash-menu failure was a test race, plus a misleading
  post-cleanup dump.
- Adding ALERT-PICK-PROBE to integration adds about 6 s to the integration job. It logs two
  `ALERT-PICK-PROBE` lines and fails the job if a pick does not reach the file.
- The stress job is now shorter by about 2 min (the probe is no longer run 20 times).
