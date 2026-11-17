# CR 196, round 2: Inspector review

Verdict: **APPROVE**. Finding 1 is a merge gate for the driver; findings 2 to 5 are low or nit and
do not block.

Scope reviewed: `git diff` and the untracked files in `markdown-okf-schema-studio-wt-196`
(findBar.ts, runtime.ts, previewManager.ts comment, runtimeHarness.ts, the new
runtimeFindFromBlockEditor.test.ts, findBar.test.ts, findInPreview.test.ts, TOOLBAR-009, BLOCK-047,
toolbar-navigation index, log.md).

## Evidence

- `npm run compile`: clean.
- Page, session and security unit tests: 1887 of 1887 pass. The three files I targeted pass 78 of 78.
- Fail-before, checked in a scratch copy (`/private/tmp/claude-502/cr196-inspect/repo`) with the
  worktree's src reverted there:
  - Both src files at HEAD: all 11 new tests fail.
  - Fixed findBar with only the `open()` early return removed: 3 fail (the idempotence tests in both
    files, plus the "unsaved block edits" test).
  - Fixed findBar with runtime.ts at HEAD (no `canRestoreFocus`): 1 fails, the Escape-after-commit
    assertion.
  - So each part of the fix has a test that needs it. No existing assertion was weakened. The only
    removed assertion is the old "a text area keeps the key" one, which encoded the behaviour this
    CR replaces.
- `check:limits`, `check:markers`, `check:exports` and `requirements-lint` (index and coverage
  `--check`) pass. findBar.ts is 618 lines, under the 800-line limit. `check:boundaries` could not
  run: dependency-cruiser refuses this machine's Node 25. That is environmental, not caused by the
  change.

## Assessment against the checklist

1. **Fix and idempotence: correct.**
   - Ctrl+F in a field now prevents the default, stops propagation and calls `open()`. `open()`
     focuses and selects the find field at once.
   - A later `open()` without `replace` while the focus is anywhere in the bar (find field, replace
     field or a toggle) returns early: no rebuild, no refocus, no reselect, no new search.
   - `open({replace:true})` still goes through, as before.
   - Ctrl+F inside the bar is handled by `barKeydown`. From the replace field it moves to the find
     field and selects it, like VS Code.
   - Neither F3 in a field nor Ctrl+Alt+F / Ctrl+Shift+F is taken; the `!altKey && !shiftKey` guard
     is still there and a test covers it.
   - On macOS, Ctrl+F (Emacs forward-char) in a textarea is still not taken, because the command
     key there is `metaKey`.
2. **Capture-phase stopPropagation: harmless either way.**
   - The repro report shows that before the fix the key reached VS Code's webview keydown forwarder
     (`did-keydown`) while the page did not stop it, so that forwarder runs at the target or bubble
     phase of the same window.
   - A `stopPropagation()` in the window's capture phase ends the dispatch before those phases. VS
     Code then most likely never sees the key, and no `previewFindCommand` follows.
   - If some VS Code build forwards in capture too, or registers its listener earlier, the late
     command reaches an `open()` that does nothing while the focus is in the bar.
   - Either way there is one bar, the query is kept and the focus stays put. Content targets already
     took this path before the change.
3. **Tests: genuine; they fail without the fix (see Evidence).** They test synchronously in the
   harness, with no race hidden by timers. `flushTimers()` is used only to drain the autosave and
   cell-commit timers.
4. **Harness: faithful enough for these handlers.** `blurOnFocusChange` dispatches `blur` with
   `relatedTarget`, and `blur()` sets the focus to nothing and dispatches `blur(relatedTarget=null)`.
   Both are opt-in, so existing tests are unchanged. Finding 2 lists the small differences from a
   browser.
5. **Real-window step: robust by construction.**
   - It waits with `settle` for the textarea focus, the exact query "studio", the editor closing and
     the bar closing, with no `force`.
   - The assumption "an unchanged editor closes on blur" holds: in `postBlockEditSave(true)`, when
     `editedText === originalText` and `!hasAutosavedChange`, it calls `closeBlockEdit()`. The find
     field is outside the editor frame, so the blur commits.
   - The 300 ms sleep is only a negative probe for a late host command; finding 4 covers it.
   - The step has not been run (finding 1).
6. **Requirements: consistent with the code.**
   - TOOLBAR-009 is `draft` and BLOCK-047 is `proposed`; no StRS was touched.
   - The new rows match the code: field selection seeds the query, Escape skips a finishing editor,
     the host command is a no-op in the bar, Ctrl+F in the bar reselects, and F3 stays with fields.
   - `implemented_in_files` and `tested_in_files` were updated, the index line was regenerated
     (`requirements-update --check` shows 0 changes), and the log entry is present.
   - Broader scope (comment box, palette and panel controls): acceptable. Before the change, the
     host path moved the focus to the find field from those controls too, one round trip later, so
     the blur effects (link and figure panel `onLeave`) are the same, only earlier.
7. **Regressions: none found.**
   - No other `src/` code reacts to Ctrl+F or KeyF; `previewFindCommand` only calls `open()`.
   - The editor textarea's own keydown listeners no longer see Ctrl+F, and none of them used it.
   - `canRestoreFocus` edge cases:
     - The editor was removed: `isConnected` is false, so the field blurs.
     - `tableInput`: covered.
     - The save was refused: `finishing` is reset, so the focus is restored, which is correct.
     - Frontmatter fields are not in the hook but are self-protecting: `saveValue` disables the
       control while the save is in flight, so `focus()` fails, or closes the editor when nothing
       changed.
   - The new `findInput.blur?.()` in `close()`: in a browser a hidden focused control loses the
     focus anyway, and the full suite passes.
8. **Quality: good.** Comments are short and explain why, and the markers are present.

## Findings

1. **Medium, merge gate (driver): the real-window step has never run.** The step in
   `test/integration/findInPreview.test.ts` cannot run locally. The bug was reproduced only in the
   page harness (as `reports/repro-attempt.md` notes), so the real-window behaviour has been checked
   neither before nor after the fix. Before merge, run the heavy CI integration job on the branch
   (`gh workflow run ci.yml --ref <branch> -f heavy=true`) and link the run.
2. **Low: the harness differs from a browser in three small ways.**
   - Order: `RuntimeElement.focus()` sets `windowState.focused` to the new element before it
     dispatches `blur` on the old one. In a browser, `document.activeElement` is the body during
     `blur`.
   - There is no `focus`, `focusin` or `focusout` event.
   - The blur handlers this CR reaches use `relatedTarget` (block textarea, frontmatter, panels) or
     a `setTimeout(0)` (table cell), so no result depends on these differences today. A future test
     that reads `activeElement` inside a blur handler would see the wrong value. Swap the order
     (dispatch the blur while the focus is unset, then set it), or note the difference in the
     doc comment.
3. **Low, already there before: `restoreFocus` is not refreshed when the bar is already open.** If
   the reader goes back into a block editor while the bar is open and presses Ctrl+F there,
   `restoreFocus` still points to the target from the first open. Escape then goes to that stale
   target, or to the body if that target is disconnected or refused, not to the editor just left.
   The old host path behaved the same, and nothing is lost, so this can be a backlog item.
4. **Low/nit: the fixed 300 ms sleep in `findFromBlockEditor`.** It probes for the absence of a late
   host command. It cannot cause a false failure, but it may miss a command that arrives later. It
   is acceptable as a probe; a comment saying the page normally stops the key (so the command
   usually never comes) would make its purpose clear.
5. **Nit:** `test/page/modules/findBar.test.ts` has a stray space in `{ code: "Enter" , key: "Enter" }`.
