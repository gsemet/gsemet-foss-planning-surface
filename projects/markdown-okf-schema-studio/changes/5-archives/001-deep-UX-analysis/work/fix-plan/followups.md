# Follow-ups

Non-blocking findings deferred by reviews (MINOR/NIT), plus known out-of-scope items. One entry per
item: source (task and review round), description, suggested action.

## Known at planning time

- **D-09 (optional).** Publish frontmatter schema and link issues as VS Code diagnostics
  (Problems panel).
- **Part-2 findings UX-35 … UX-48.** Not approved; out of scope. UX-35 (CRLF inline edits) is the
  most severe; T09's minimal edits must not make it worse.
- **`AGENTS.md`.** Its extension section still describes a `sphinx-build` rendering pipeline,
  while the preview renders MyST in process. This is a documentation correction to propose to the
  user, outside this plan, except for the Identity bullet updated by T37.

## From reviews

- **T00 r2 [MINOR] scroll flake.** Scroll campaign timed out once in 3 runs waiting for
  `[data-sphinx-preview-block-editor] textarea` after `solo-block-anchored`
  (`logs/T00-impl-r2-full.log:311`). Rerun once before treating it as a regression; if it recurs
  more often, investigate the wait in the scroll campaign.
- **T00 r2 [MINOR] stale visual check.** `test/visual/capture.py` narrow-schema check expects
  headers `Name/Value` but the Value heading now contains the restore toggle (`Value◀▶`). Part of
  the visual baseline; fix it in a task that may touch `capture.py` (T03) or at T40.
- **T00 r2 [NIT] baseline durations.** `trusted`, `scroll` and `reload` are not timed separately;
  they run inside `full`.
- **T01 r1 [MINOR] comment check coverage.** Four F2 value edits missing from the comment test.
  Folded into T05 step 2b.
- **T01 r1 [NIT] shrinking padded cell.** Folded into T04's Tests list.
- **T01 r1 [NIT]** wording in the implementation report only; no action.
- **T02 r2 F1 [MINOR, pre-existing, needs user approval].** `previewEditing.test.ts` theme loops
  (around lines 447-450, 471-474, 502-505, 528-531) resolve the preview frame once and click with
  no retry when the frame detaches. A late file-system event for the freshly written `finding.md`
  can re-render the preview in between (1 run in 11, `logs/T02-r2b-trusted.log`). Product cause:
  an FS change event on the active file re-renders even when the disk text equals the buffer, and
  every render reloads the webview (UX-28). Check again after T34. Hardening the protected test
  needs the user's approval.
- **T02 r2 F2 [NIT].** `test/integration/fixtures/realinput-*` is not gitignored (same as
  `checkbox-e2e-*`).
- **T02 r3 F3 [NIT].** Edit mode will persist per workspace after T38: folded into T38's Allowed files note.
- **T03 r2 [MINOR] comment wording.** `test/shared/geometry-checks.js` header comment (lines 4–5):
  the last clause about `overlays`/`ignoreWithin` options is partly wrong
  (see `reviews/T03-review-r2.md` finding 1). Fix when the file is next touched.
- **T03 r2 [NIT]** `capture.py` `machine_check_lines` names the wrong item in its `None` line;
  report arithmetic only. No action needed.
- **T04 r2 [MINOR] backslash value test.** In `markdownTablePreservation.test.ts`, loop "every
  single-cell edit reparses and changes at most one line": add `"C:\\"` to the values array
  `["", "x", "a|b"]` (no-spaces style is protected only by the fallback today).
- **T04 r2 [MINOR] process.** Implementers must keep pre-fail gate logs under the name their report
  cites (added to the implementer prompt reminders by the orchestrator).
- **T04 r2 [NIT]** tab-led whitespace-only cell gets a space; no visible effect.
- **T05 [MINOR] remaining frontmatter style cases (data always correct).** Inside the edited field
  only: a `|+` block scalar as the last field leaves a blank line before `---`; header comments on
  block collections (`tags:  # c`) and `key: # c` move to their own line; inline comment spacing in
  collections is normalized; `x:  # why` (empty value with comment) falls back to the whole-document
  patch. See `reviews/T05-review-r1.md` finding 5 and `reviews/T05-review-r2.md` follow-ups.
- **T06 r2 [MINOR] structural edge cases (data correct; two identical to base).** `afterField`
  after a block scalar followed by a less-indented comment line; removing the only field and
  removing the last field after a `|+` block scalar go through the whole-document fallback. Also
  from r1: add without `afterField` after trailing blank lines leaves a blank line between fields;
  remove keeps the removed field's own indented trailing comments. See `reviews/T06-review-r1.md`
  and `-r2.md`.
- **T07 r1 [MINOR] README wrap.** The "Edit mode" paragraph line edited by T07 exceeds the
  100-column wrap rule. Rewrap at clause boundaries (any later task touching README.md, or T40).
- **T07 r1 [NIT]** the `multiline` check looks for `"\n"` only; a lone `"\r"` is theoretical in a
  textarea.
- **T08 r1 [MINOR]** README "Edit mode" paragraph: the edited lines exceed 100 columns (same as
  T07). T15 edits this paragraph again: rewrap it there.
- **T08 r1 [MINOR]** `test/visual/capture.py` `check_preview_edit_mode`: `original_cell_html` is now
  unused. Remove it, or reuse it for the T15 Revert check.
- **T08 r1 [NIT]** no unit test for `applyEditMode(false)` with an open table-cell editor, or with a
  block whose source has not loaded (`closeBlockEdit(false)` branch).
- **T09 [NIT]** `drainActiveBlockEdit`: the empty-replacement branch is unreachable (the earlier
  `editedText === edit.lastSavedText` check returns first). Harmless.
- **T10 r1 [MINOR]** the undo-key helper is wired into the frontmatter key/value keydown listeners
  without a test. Add a unit test: Meta+Z keydown on a frontmatter text control calls
  `stopPropagation` once and never `preventDefault`.
- **T10 r1 [NIT]** RI-T10 accepts any strict prefix after undo (Chromium undoes by word); the redo
  assertion is exact.
- **T11 r1 [MINOR] process.** RI-T11 was not run red before the fix (judged meaningful by
  inspection). Remind implementers to run new E2E scenarios once against the base code.
- **T11 r1 [NIT]** a thematic break written `* * *` or `- - -` parses as a list item, so Enter after
  it inserts `\n* `.
- **T09 → T11 [process]** T09's gate had no `visual`; its debounce broke one capture.py check,
  fixed in T11. The orchestrator now adds `visual` to every webview-runtime task.
- **T12 r1 [MINOR] process** pure `indentSelection` tests written after the function (runtime and
  RI-T12 were shown red). **[NIT]** quote-prefix regex recomputed in the collapsed-caret branch.
- **T13 r1 [NIT]** `lifecycle.test.ts`: one long `assert.ok(... status ...)` line. **[MINOR] process:** the lifecycle block was not run red first (RI-T13 was).
- **T15 r1 [MINOR]** Revert has no keyboard path: Tab indents inside the textarea, so Done and
  Revert are reachable by mouse only. Escape still commits. Consider a shortcut, or document it.
- **T15 r1 [MINOR]** `capture.py` `check_edit_affordances` hides the sticky band with an injected
  style tag. Remove it once the baseline sticky/toolbar failure is fixed.
- **T15 r1 [NIT]** the status line sits about 1em above the buttons (a paragraph margin wins).
- **T15 r1 [MINOR, fixed]** README reflow done by the orchestrator: only line breaks changed.
- **T16 r1 [MINOR]** `capture.py` `check_preview_edit_mode`: the warning-paragraph check only checks the computed style. Also assert that the warning body has exactly 1 rect top ("warning paragraph reflowed in edit mode").
- **T17 r1 [MINOR]** `commitCellEditorOnFocusLoss`: if you click in a cell and then switch to another VS Code editor within 500 ms, the blur is ignored and the cell editor stays open. No data is lost (autosave keeps running). Option: re-check on window focus or blur, or after the guard expires.
- **T18 r2 [MINOR]** `applyAnchor` re-reveal: when a cell switch changes the wrap of the status
  text, the bar height changes and the page can scroll up a few pixels. This only happens while the
  bar sits under the band. Optional: a unit test showing that a cell switch with an unchanged bar
  height keeps `scrollY`. **[NIT]** `capture.py` still returns `controlsBottom` but never uses it.
- **D-18a (user review)** orchestrator refinement: the toolbar is revealed when it appears hidden.
  See `decisions.md`.
- **T19 [MINOR]** `markWideTables` reads `textContent`, which may include the text of an open editor overlay. Harmless, because marks are only ever added. **[NIT]** In the dark theme, the overflow cue is a lighter band, not a dark shadow.
- **T21 r1 [MINOR]** in edit mode, Enter on a focused okf link in a properties value still navigates, while a click edits (D-07 only specifies click). Option: Enter opens the editor and Cmd/Ctrl+Enter navigates.
- **T22 r1 [MINOR, worth fixing]** `refreshLinkWarning`: an unknown-stem warning overwrites a shown
  validation error (`data-state="error"`). Keep the error text and still set `aria-invalid`.
  Also, removing the only unknown item with the remove button leaves the warning in place: call
  `refreshLinkWarning()` after a row is removed. See `reviews/T22-review-r1.md` for the exact tests.
  **[NIT]** existing unknown items are only flagged on input.
- **T23 [MINOR]** the list editor `focusout` now saves when focus leaves the picker `<select>` for something outside the row. Before, the picker sat outside the editor. This is consistent with blur-save. **[NIT]** at 540 px, Add field and Remove field stack vertically.
- **T24 r1 [MINOR]** Add picker `select`: on platforms where arrow keys fire `change` (Windows/Linux Chromium with a closed select), a keyboard user may add the first field they move over. Low impact on macOS. Consider ignoring arrow-key changes.
- **T25 r1 [MINOR]** saving a value into a field added with `""` keeps the double quotes
  (`reviewer: "Ana"`, not `reviewer: Ana`). Valid YAML, same value; it comes from the existing
  quote preservation of the value patch (`preserveYamlNodeMetadata`). Option: drop the quotes when
  the replaced value was the empty string written by an add.
- **T25 r1 [NIT]** the properties table lists unknown keys (such as a custom key) last, while the
  buffer has them where they were inserted (after the current row, T24). Existing ordering.
- **T25 r2 [process]** the new RI-T25 assertion (no editor open after saving the new field's value)
  was not shown red against the round-1 code; the two unit tests were, and the round-1 review
  screenshot showed the reopened editor. A custom key with no schema gets the generic YAML editor,
  which saves with Cmd/Ctrl+Enter, not plain Enter.
- **T26 r1 [MINOR]** `scrollSync.test.ts` "the badge click scrolls to and focuses…" asserts
  `focusOptions !== undefined || scrollY !== 900` (a disjunction that does not prove focus). Assert
  `frontmatterValueCell.focusOptions` deep-equals `{ preventScroll: true }` and, if the harness can
  record it, `scrollIntoView({ block: "center" })`. RI-T26 proves the real behaviour.
- **T26 r1 [MINOR]** the issue badge does nothing when no row carries an issue class (for example
  when the only issue is the missing-required summary). Fall back to the missing-required summary
  or the properties title; add a unit test.
- **T26 r1 [MINOR]** no light-theme capture shows an invalid link (no visual fixture has one). All
  new colours come from theme variables. Add an invalid-link frontmatter fixture to one visual
  scenario.
- **T26 r1 [NIT]** `linkStatusLabel` has a `"was not found"` branch that matches no message in
  `fileLinks.ts`. In reading mode the invalid span is focusable and Enter falls through to the
  mapped-block reveal (consistent, not a regression).
- **T27 r1 [MINOR]** `drainActiveBlockEdit`: when an insertion session is cleared mid-session
  (`lastSavedText = ""`) and another actor then edits before the offset, the next save's safety
  check is vacuous and could insert at a stale offset. Ordinary blocks emptied mid-session have the
  same gap (not a regression). Option: record the document version after each applied edit and
  require it when `lastSavedText === ""`; test: clear, edit elsewhere, save.
- **T27 r1 [MINOR]** `planInsertion("", 1)` returns a plan (prefix `"\n\n"`) instead of
  `undefined` for an empty document. Return `undefined` for `afterLine >= 1` on empty text; add the
  assertion. (T28's empty-body "Start writing" should send `insertAfterLine: 0`.)
- **T27 r1 [NIT]** no integration test asserts that an insertion save with an outdated
  `documentVersion` is refused (holds by code reading).
- **T28 r1 [MINOR]** the invisible `+` insertion buttons are in the Tab order in edit mode (one per
  block); they become visible on `:focus-visible`, so keyboard use works but Tab stops multiply.
- **T28 r1 [MINOR]** clicking `+` while another block editor is open only commits that editor; a
  second click opens the insertion editor. Option: open the insertion editor after the commit
  (pending-navigation mechanism).
- **T28 r1 [NIT]** RI-T28 names its empty document `smoke.md` (in a `realinput-t28-*` folder), not
  `scratch.md`; behaviour is identical.
- **T29 r1 [design, for the user]** the pending status banner is in flow (about 23 px at the top of
  the content; only `success` is visually hidden). It was already shown on the reloaded pending
  page before T29. Now that it appears in place (and with T34 in-place content), content at the top
  of the page shifts by 23 px while a render is pending. Scroll anchoring hides it when the reader is
  scrolled down. Option: an overlay or a reserved-height status strip.
- **T29 r1 [perf]** the host queues a second render about 150 ms after the first ready render of
  every opened document (seen in instrumented RI-T16 runs). It may be wasted work; investigate the
  trigger.
- **T29 r1 [MINOR]** late `previewReady`: a ready report from a replaced document with the *same*
  requestId (an enrichment re-assign with changed html) could set `readyRequestId` while the new
  document is still loading; the in-place status would reach the old document. The host string
  stays correct and the next load shows the right state.
- **T31 [note]** UX-29 case 1 (the preview jumps when you type after a preview scroll) did not
  reproduce on HEAD before the change. H1 was kept as the documented intent: catch up only on
  hidden → visible. The `restorePreviewStateCalls` test hook now guards both directions. The bug
  sheet's case 2 (a 178 px jump on the first table-cell click) did not reproduce: the cell's
  viewport top moved 0.39 px.
- **T32 r2 [MINOR]** `takePendingPin`'s `minVersion` branch has no test: `extension.ts` has no
  unit seam. If an extension-host unit seam is added later, cover three cases: an older version
  keeps the pin, the current version consumes it, an expired pin is dropped. The preview's own
  autosaves cannot start a render while the block editor is open (`refreshPreview` skips change
  events while `applying`), so the guard only matters for renders started from outside.
- **T32 r2 [MINOR]** RI-T32 table sits at the scroll clamp (short document, about 260 px of room)
  because of the table-typing jump below. Once that is fixed, move the table to mid-document with
  filler below it and assert `|T1 - T0| <= 3` instead of measuring against `Tcommit`.
- **T32 [UX, for the user] Home/End in preview text editors scroll the whole page on macOS.**
  Investigated on 2026-10-11 with a probe at d596de8 (scratch worktree; logs
  `scratchpad/probe*-d596de8.log`, not committed). The "typing jump" is not caused by typing:
  - plain typing and Cmd+→ in a table cell move nothing (0 px);
  - **End** in a cell or block editor runs Chromium's native macOS binding
    (`scrollToEndOfDocument`): the page scrolls smoothly to the bottom (scrollY 1294 → 3012) and
    the caret does not move. **Home** scrolls to the top;
  - the next typed character scrolls the caret back into view at the viewport edge. The block ends
    about 340 px (cell) or 233 px (paragraph) from where it was;
  - no runtime call (`scrollTo`, `scrollIntoView`, `focus`) runs during the jump, and the
    `scrollPreviewWithEditor` / `scrollEditorWithPreview` settings change nothing. It is not a
    plan regression.
  - Option (needs a decision): on macOS, make plain Home/End (and Shift+Home/End) in the preview's
    text controls go to the line start/end, as VS Code's own editor does. Otherwise leave the
    native behaviour.
  - Test mechanics: `realInput.test.ts` presses bare `End` in about 14 places. On macOS it does not
    move the caret; those tests pass because the caret is already at the end. `caretToEnd`
    (Meta+ArrowDown on darwin) is the reliable helper. RI-T32 table needed a short document only
    because of this; review r2 finding 3 above can use `caretToEnd` or Meta+ArrowRight.
- **T35 r1 [MINOR]** `src/build/sphinxBuild.ts` is dead (nothing imports it; `buildSphinxSnapshot`
  is referenced only inside it) and still holds "Sphinx" error strings. Delete it, or add it to
  `scannedFiles()` in `userFacingText.test.ts` and reword its strings.
- **T35 r1 [MINOR]** RI-T35 needed a 2 s settle and `workspace.fs.delete`: an `fs.rmSync` right
  after the fixture was created was missed by the watcher. Add a lifecycle probe (create, open the
  preview, wait for the render, `fs.rmSync`, expect `missing-source` within 10 s); if it fails,
  investigate the watcher setup in `extension.ts`.
- **T35 r1 [MINOR]** `userFacingText.test.ts`: assert `literals(source).length > 0` per file, and
  that `extension.ts` yields a literal containing "could not follow the link", so a tokenizer
  desync (regex literals are not handled) fails loudly.
- **T36 r1 [MINOR]** `openPreview(uri)` from the Explorer while the Studio webview has focus:
  `showTextDocument(opened, { preview: false })` uses the active group, which can be the
  preview's. T39's group lock should send it to another group; check this case at T39. Otherwise
  pass `viewColumn: ViewColumn.One` (or the last text editor's column) and add a lifecycle case.
- **T36 r1 [MINOR]** the Explorer entry shows the full title "Markdown OKF-Schema Studio: Open
  Preview to Side". Acceptable; a shorter menu label needs a separate command.
- **T37 r1 [MINOR]** the Open With editor title (basename) has no integration assertion. If a
  test hook can reach the custom-editor panel, open it with `vscode.openWith(uri,
  "markdown-okf-schema-studio.editor")` and assert `title === "<basename>"`.
- **T37 r1 [NIT]** a restored side preview whose source is missing is titled `Studio` with no file
  name. It could use the basename of `restoredState.sourceFile`.
- **T38 r2 [MINOR]** RI-T38's "previewState carries editMode: true" check (`scrollTop > 0`) can
  also pass through `previewScroll`. Isolate it: with edit mode on, collapse the Description
  column and `waitFor` `descriptionsCollapsed === true` (only `previewState` carries it). The
  previewEditing Description scenario already covers the regression.
- **T38 r2 [MINOR]** the reload suite has no edit-mode assertion, although P-L3 lists edit mode
  (a gap that predates T38). Turn edit mode on, reload, assert `on`; turn it off, reload, assert
  `off`. The second reload proves that the saved state beats a workspace value of `true`.
- **T38 r2 [NIT]** the unit test "T38: an unpaired preview…" should assert `aria-pressed="true"`
  after re-pairing, and add a `savedAnchorMode=false` variant.
- **T38 [process]** a gate-caught bug: task step 2 said to validate `editMode` "on this type
  only". `previewState` always carries `editMode`, so every saved state was dropped. Fixed in
  round 2.

- **T36 r1 → resolved in T39** the Explorer entry with the preview focused now opens the file
  outside the preview's group (`columnOutsideSidePreview`), asserted in RI-T39 (c).
- **T39 r3 [MINOR]** with `workbench.editor.closeEmptyGroups: false`, closing a side preview runs
  the stale-column fallback on every empty group without a preview: focus flickers, and an empty
  group the user locked on purpose is unlocked. When `groupAt(column)` is not empty, read the
  setting and skip the fallback if it is `false`.
- **T39 r3 [MINOR]** RI-T39 keeps fixed settle waits (400 ms after closing a preview, 1 s at the
  start), because the unlock has no observable state. Replace them if a test hook appears.
- **T39 [UX]** the lock adds a small focus change when the preview closes in the last group
  (that group gets focus). Focus in the terminal or the sidebar cannot be restored through the API.

- **T40 replay [UX, extends the Home/End entry]** in a table cell editor, End also scrolls the
  whole preview to the bottom (macOS default; the cell `keydown` in `renderTableCellEditor`
  handles neither End nor Home). The next keystroke brings the caret back under the sticky band,
  about 440 px above where the user clicked. This predates the plan
  (`replay/table-commit-scroll.md`). Commit by Enter, Tab or blur keeps the table within 1 px.
- **T40 replay [test]** `realInput.test.ts` RI-T32 table case (around line 884) and the skill's
  `table-cell-edit.json` press End after the click. The test comment attributes the ~1700 px
  paging to typing, but it comes from End. Use `Meta+ArrowDown`, or no caret move: the editor
  already opens with the caret at the end.
- **T40 replay [seen once, unconfirmed]** while the save render swaps the preview's inner frame,
  scroll position samples sometimes read a wrong value for 26–100 ms. This is UX-28 territory
  (blocked T29/T33/T34).
- **T40 visual review [harness]** the visual campaign's "sticky heading overlaps the reserved
  toolbar row" check fails on many images where no text is covered. Tighten it to actual
  text/toolbar intersection. Several real-input notes (26, 27, 32, 33) describe a state their
  screenshot does not show; capture after the measured state settles.
- **T40 visual review [minor]** `12-frontmatter-title-multiline`: a two-line title is shown on one
  line in the properties table. `24-start-writing-open`: the floating toolbar overlaps the top
  right of the empty editor (UX-44 family).
- **T40 replay [side finding]** creating a Studio webview sometimes logs bursts of `401`
  resource-load errors from short-lived `fake.html` frames (`replay/UX-03.md`).

- **T41 r2 [test flakiness]** `checkboxToggle.test.ts` "one undo to restore the original source"
  timed out in 2 of 5 runs on the same tree (`logs/T41-impl2-full.log`, `logs/T41r2-full.log`).
  The other runs passed: `T41-impl2b`, `T41r2-trusted1` and `T41r2-trusted2`. The test runs
  `showTextDocument` then `executeCommand("undo")`, which acts on the focused editor. When the test
  window lacks OS focus, the undo goes elsewhere. Make it focus-independent: target the document
  with `workbench.action.focusActiveEditorGroup`, then `undo`, and wait for
  `activeTextEditor.document === document` before running it.

## Blocked tasks

**Resolved on 2026-10-14.** T29 was superseded by T43 (D-22, `e26e836`). T30 (`a9d4545`), T33
(`0f4605a`) and T34 (`8d1ee21`) then ran on top of T43 and are done. The entries below are kept
as history.

- **T29 — Pending status without a webview reload (UX-28 step 1). BLOCKED after 3 rounds.**
  The work is saved as `logs/T29-blocked.patch` (+449/−26 in 6 files). It re-applies cleanly on
  `fed90bd`; apply it with `git apply`. Reports are r1–r3; reviews are r1–r2.
  - **Done and reviewed:**
    - the `assignWebviewHtml` funnel with the `htmlAssignments` counter;
    - `readyRequestId` readiness;
    - the in-place `previewStatus` message, and the runtime `applyPreviewStatus`;
    - a re-anchor after the in-place status change when the reader is scrolled (RI-T29b proves it:
      the content stayed still where it used to move 23 px);
    - RI-T29;
    - the RI-T16 setup wait.
  - **Open problem:**
    - The pending banner is in flow (about 23 px above the content) and `overflow-anchor` is off.
      - At scrollY 0 with an open inline editor, the round-2 code lets the editor jump 23 px under
        the caret during a pending render (review r2, MAJOR).
      - Round 3 also re-anchors when an editor anchor is active. The page then scrolls 22 px to
        hold the editor, and after the ready reload it stays 22 px down instead of returning to 0:
        `scroll-sync-suite.ts`, keyboard navigation, `window.scrollY` 22 !== 0. This persists after
        status `success`.
    - **Likely root fix (needs a decision):** make the pending banner take no layout space (an
      overlay or a reserved strip). Then no re-anchoring is needed at all, and T35's status layout
      can follow. A design decision for the user, about the visual style of the pending banner.
      - Alternative: on the ready reload, restore by the editor's viewport anchor instead of the
        saved `scrollTop`.
  - **Downstream:** T30 builds on T29 (counter, readiness, the in-place status helper) and is
    skipped. T34 reuses the T29 status helper.
- **T30 — skipped, blocked by T29.** It patches the properties section and links in place using
  T29's `htmlAssignments` counter, readiness and in-place status. Run it after T29 is unblocked.
- **T33 — deferred, blocked with T34.** A no-behaviour refactor of the runtime start-up that
  only prepares T34. It has no user benefit on its own, so it stays out until T29 and T34 can run.
- **T34 — blocked by T29.** The in-place content patch needs T29's `assignWebviewHtml`,
  `htmlAssignments`, `readyRequestId` and in-place status helper (task file lines 59–96 and RI-T34).

## T30 review r1 (2026-10-14)

- **Group move after an in-place table patch** (MINOR). If VS Code reloads the iframe when the
  preview moves between groups, it loads `panel.webview.html`, the page from the last full
  assignment, so the properties table can be one patch behind until the next render. Possible
  fix: in the `previewReady` handler, when `panel.webview.html !== preview.webview.html` for the
  current stage, re-post the properties markup from the host record.
- **"Saved. Refreshing preview…" stays about 1 s** (MINOR). The 300 ms table patch is deferred
  while a frontmatter editor is open, so the editor closes at the next full render instead.

## T34 review r1 (2026-10-14)

- **PlantUML patch without a fallback** (MINOR 3). `scheduleDeferredPreviewWork` posts the
  PlantUML content patch without arming a fallback timer. If that message is lost, the diagrams
  only appear at the next render.
- **Stale link-target hints after a patch** (from the T34 report). `linkNavigation.rescan()` keeps
  `discovered`, so hints for links that were already known can stay stale until the next full
  load. A one-line `discovered.clear()` in `rescan()` would match the reload behaviour.

## Final replay (2026-10-14)

- **The UX-30 scenario's title-button check is stale.** It filters the tooltip on `/Studio/`.
  Since T42 (D-20) the tooltip reads "Open Preview to Side (⌘K ⇧V)". The button exists and works.
  Update `replay/scenarios/UX-30-entry-points.json`.
- **The VS Code built-in action "Open Preview to the Side (⌘K V)"** sits next to ours, "Open
  Preview to Side (⌘K ⇧V)". The two labels differ by one word.
- **`[pageerror] Found unexpected null`**, seen once while the preview switched documents. It is
  thrown by VS Code's webview host (`assertIsDefined` in `pre/index.html`) when a pending frame is
  replaced quickly. It did not reproduce.
