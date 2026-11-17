Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.3 critic review: review-annotations StRS and SwRS

Scope `review-annotations`: 18 StRS (REVIEW-001..018), 216 SwRS (REVIEW-001..216), reviewed against
`inventory/review-annotations.md`, `reviews/review-annotations-inventory.md`, the sources and tests of
`markdown-okf-schema-studio-wt-059-b3` (`src/core/comments/*`, `src/session/features/{comments,incomingChanges,sourceEdits}.ts`,
`src/session/{hostEvents,pageMessages}.ts`, `src/page/modules/{commentThreads,commentCompose,chipToggle,commentsToggle,inlineThread,incomingChanges}.ts`,
`src/core/render/commentMarkers.ts`, `src/core/preview/styles/commentStyles.ts`, `src/core/mapping/lineDiff.ts`,
`src/host-vscode/headBaseline.ts`, `src/core/protocol/pageToHost.ts`, `src/core/palette/paletteActions.ts`) and the other
batch-4 scopes in the worktree (lifecycle-sync, trust-security, palette-slash). Read-only; no lint, no build, no test run.

Verdict: REVISE

## What passed

- Structure (scripted over all 216 files): heading equals title, description equals the Normative behavior
  paragraph, exactly one SHALL, exactly two scenarios, no leftover placeholder, no backlog id, inventory id,
  `D25`-style id or relative reference in any requirement text. Every one of the 18 StRS is derived by at least
  two SwRS.
- Verification notes: every backticked test title (about 330) was found by grep in `test/`, every quoted test file
  exists, the integration assertion strings ("an invalid file posts nothing", "no sidecar write while typing", "two quick
  creates must both be saved", "invalid messages write nothing", "one undo should remove the reply", and so on) exist.
  Visual and real-window ids (`r02..r06`, `v01..v20`) exist in `test/visual/scenarioIds.ts` or the capture registry.
- The "untested" claims I probed are honest (010, 016, 022, 062, 064, 066, 122, 123, 124, 127, 128, 129, 148, 155, 181 to 184, 213):
  none has a test. The "tested" claims I sampled hold.
- Numbers, texts and defaults verified in the code: 2 MiB / 1000 threads / 200 comments / 10 000 characters, 150 ms sidecar
  debounce, 300 ms incoming-change debounce, 15 s answer timeout, 500 / 32 / 32 anchor limits, 100-character author cut,
  `MIN_MOVED_QUOTE` 12, `WINDOW_LINES` 50, `FUZZY_RATIO` 0.2, 60 percent resemblance, 20 rare occurrences, 20 million cells,
  2 million characters, negation list, 8 MiB bound, 1 MiB baseline, 64-entry cache, 20 000 lines / 2000 edits, 3 px bar,
  360 px popover, 120-character orphan excerpt, all quoted UI strings (Delete thread?, Resolved, Orphaned comments,
  New comment, Write a comment, Reply to this thread, Hide/Show comments, Hide/Show changes since last commit,
  Toggle TODO comment, "The comment was not saved: ...", the 15 s texts, the thread refusal texts, the rename warning).
- Known issues: all three are true and precise. They sit on REVIEW-132, REVIEW-158 and REVIEW-180.
  - 132 and 180: `previewManager` makes a session read-only when there is no workspace folder or the workspace
    is untrusted (`readOnly = workspaceFolder === undefined || !host.workspace.trusted`), while `writeComment` and
    `handleThreadChange` answer "needs a trusted workspace" for both causes; `commentsEnabled: !preview.readOnly`
    removes the controls in both cases.
  - 158: `commentsToggle` sets `data-sphinx-preview-comments`, the stylesheet hides only `kind="comment"` for it, while
    `data-okf-show-comments="false"` also hides `kind="thread"` (commentStyles.ts lines 516 to 533).
- Special check, ids of the Known issues: REVIEW-123, 147 and 169 carry no Known issue and are about other content
  (123: clean document changed, 147: open boxes kept in webview state, 169: thread message header). The described
  contents are on 132, 158 and 180 (creation order versus final order). No file of the CR folder cites 123, 147 or 169
  as Known issue, so nothing else needs correcting; the analyst's hand-over note is just wrong.
- Special check, inventory contradictions (all three confirmed, and the SwRS state the code behaviour, not the
  inventory claim):
  - A rename whose comments file names another document is skipped silently: `moveSidecars` does `continue` when
    `parsed.errors.length === 0 && parsed.document !== oldName`, no warning (SwRS-127 correct). The JSDoc of
    `moveSidecars` still says "a warning says so": stale code comment, not a product defect, no Known issue needed.
  - Only the render refresh waits 300 ms: `manager.incoming.schedule(preview)` after a render
    (rendering.ts:491) uses the default; HEAD watch, trust grant, preview settings change, page load and the Diff
    preference all call `schedule(.., 0)` (SwRS-197 and 198 correct; inventory F-REVIEW-065 says "debounced by 300 ms" for all).
  - Diff off clears the marks: `post` computes `ranges = []` when the Diff choice is off and, if `marksShown`, posts the
    empty list. The behaviour is real but only half written (see defect 6).
- Lifecycle-sync's three "no SwRS yet" items do exist here: `preview.showComments` is REVIEW-152 to 156,
  `preview.showIncomingChanges` is REVIEW-216 (with 195, 196, 199), and the incoming-change scheduling on trust grant
  is REVIEW-198 (scenario "Trust granted"). LIFE-155 ("each preview keeps its read-only/writable state on trust grant")
  does not contradict REVIEW-198: marks are posted for a read-only preview too (`post` tests `workspace.trusted` and the
  scheme, not `readOnly`). LIFE-048 lists showComments only as the counter-example (live setting). No duplicate.
- Cross-cites checked: DIAG-019 (comment quotes never wrapped in diagrams) and DIAG-020 (no comment offered inside
  diagrams) say exactly what REVIEW-018 and REVIEW-039 claim; TOOLBAR-021 and TOOLBAR-139 (band and sticky entries without
  chips), TOOLBAR-017 (incomingChanges preference schedules the refresh), TOOLBAR-013 and 015 (preference validation and
  normalization), TOOLBAR-001 (row 3 holds Diff and Comments), TABLE-090 (block-only shortcut does nothing in a cell),
  BLOCK-121/181/224 (read-only refusals) all exist, are `draft`, and match. No cite to a deprecated id.
- StRS: all are user use cases, no path, message name, ms or px. Observation only: StRS-013 says the toolbar button or the
  setting "hide the gray comment chips"; true for both, and the thread-chip difference is the documented Known issue.

## Defects (14)

1. SwRS-MDOKFSTUDIO-REVIEW-190 specifies an unreachable behaviour and contradicts 178 and 179.
   - Evidence: `pageToHost.ts` `previewThreadReply` validator drops a blank text and a text over 10 000 characters
     before any handler runs (REVIEW-178: "drop it"), so the host never answers them. For lines that are not a thread,
     `planThreadReply` calls `readThreadLines` first and returns `THREAD_GONE` ("The thread is no longer in the source.
     Refresh the preview.", REVIEW-179), never `THREAD_REPLY_REFUSED`. After `isThreadSource` passes, `threadReplyEdit`
     can only fail on the three checks the validator already made or on a missing `-->`, which `isThreadSource`
     excludes. `THREAD_REPLY_REFUSED` ("The reply could not be added to this thread.") cannot be sent in the product; the
     scenario "Non-thread lines" even says "the edit is refused" without text, and "Blank reply" says "a reply of blanks
     that reached the host", which cannot happen.
   - Fix: delete REVIEW-190 (and its derive link; StRS-015 stays covered by 178, 179, 186 to 189), or turn it into a defensive-code
     note outside the SwRS. If kept, rewrite it with a scenario that can occur and cite the case.

2. SwRS-MDOKFSTUDIO-REVIEW-111 overclaims: "two places that are far apart" always orphan.
   - Evidence: `anchoring.ts` `decide`: with two or more candidates, those inside the 50-line window of the old lines are kept;
     one near candidate wins even if another lies far away (`near.length === 1` returns it); with several near ones the
     nearest wins when strictly nearer. Context (prefix and suffix) can also pick one. The scenario is only true because
     both sentences are 200 lines from the old lines. "Far apart from each other" is not the criterion; distance to the old
     lines is.
   - Fix: reword the SHALL to "When a fuzzy search finds several places and the same decision as for exact copies (surroundings,
     50 line window, strictly nearest) picks none, the extension SHALL orphan the thread", and make scenario 1 "two places, both more
     than 50 lines from the old lines, none fitting the surroundings"; add to scenario 2 "one place near, one far moves to the near one" or
     drop the sentence about distance between the places.

3. SwRS-MDOKFSTUDIO-REVIEW-026 claims more than the code does ("inside the pane", "at least 8 px from the edges").
   - Evidence: `commentThreads.ts` `position`: only `left` is clamped (to 8 px and `innerWidth - width - 8`); `top` is
     `min(rect.bottom + 6, max(8, innerHeight - 120))` and can be negative for a highlight scrolled above the viewport, and a
     popover taller than 120 px under the lowest allowed top overflows the bottom. With a pane under 216 px the right gap
     is under 8 px (width floor 200). The size is taken from the window, not the pane.
   - Fix: say "SHALL keep its left edge at least 8 px from the left edge and, as long as the pane is at least 216 px wide, its
     right edge at least 8 px from the right edge, and give it a width of at most 360 px", rename the title "The thread popover stays
     inside the pane horizontally", and drop the vertical claim (or file the vertical overflow as a Known issue).

4. SwRS-MDOKFSTUDIO-REVIEW-057 says every refusal shows a warning; the code does not.
   - Evidence: the warning comes from `refuse()` inside `writeComment` only. The refusals made earlier in `handleCreate` and
     `handleReply` ("the comment is empty or too long.", "the reply is empty or too long." = REVIEW-072), `handleResolve` and
     `handleDelete` ("the thread is unknown.") and the `catch` of `answer` (unexpected error, REVIEW-056) answer the page without
     `showWarning`. The SHALL "When the host refuses to write a comment, a reply, a resolve or a delete" includes them.
   - Fix: restrict the SHALL to "When the host refuses a comment action because the preview is read-only, the document is not a
     saved file, the comments file has unsaved changes, or the change itself is refused (full file, unknown thread, too
     large, invalid file)", and add to REVIEW-072 that no warning is shown for an empty body; or add the missing warnings in the code.

5. SwRS-MDOKFSTUDIO-REVIEW-184 bundles two outcomes under one SHALL.
   - Evidence: `handleThreadChange.finish`: not applied gives "VS Code could not apply the change."; a rejected apply gives the
     error message (`error.message` or `String(error)`). The SHALL names only the first reason, scenario 2 ("Edit throws" -> "the
     message of the error") is a different outcome not in the SHALL.
   - Fix: make the SHALL "... SHALL answer ok false, with the reason "VS Code could not apply the change." when VS Code refuses the
     edit and with the message of the error when the application fails", or split into two SwRS.

6. SwRS-MDOKFSTUDIO-REVIEW-196 contradicts its own scenario and leaves the Diff-off take-back unwritten.
   - Evidence: the SHALL and the title say "post no ranges"/"No incoming-change ranges are posted", scenario 1 says "no incoming-change
     message is posted", scenario 2 says the page receives `enabled false` and no ranges. In `incomingChanges.ts` `post`: the gates give
     `ranges = []`; the message is skipped only when there are no marks showing and `enabled` equals `enabledPosted`, otherwise an
     empty list (with the enabled value) is posted. So turning the Diff choice off (or losing trust, or a file leaving Git) with marks
     showing posts an empty list that clears them (the inventory's "diff off clears marks"); no SwRS says it. REVIEW-199 scenario 2
     only covers "document now equals HEAD". REVIEW-216 scenario "Off" repeats the "enabled false, no ranges" half of 196.
   - Fix: reword the SHALL "... the extension SHALL post an empty list of ranges, or nothing when no mark is showing and the enabled value
     is unchanged", add the case "marks showing and the Diff choice turned off" to REVIEW-199 scenario 2, and remove the duplicated
     setting-off scenario from one of 196 and 216 (keep it in 216).

7. SwRS-MDOKFSTUDIO-REVIEW-062, 063, 075 and 079 quote the refusal reasons without the final period the user sees.
   - Evidence: `writeComment` does `refuse(\`${result.reason}.\`)`, so the page and the warning get "the comments file would become too
     large.", "the comments file is full.", "the thread no longer exists or has too many comments.", "the thread no longer exists."
     REVIEW-064, 072, 061, 132 and 180 quote the full text with its period. An implementer following 062 would emit a different string.
   - Fix: put the period inside the quotes in the four SHALLs, scenarios and Criteria.

8. Missing requirement: which parts make a review comments file not valid (REVIEW-002, 004, 007).
   - Evidence: `parseSidecar`/`parseThread`/`parseComment` reject a repeated thread id, a thread with no comment, `endLine < line` or line
     below 1, a date that is not an ISO 8601 instant with a zone, a missing or non-boolean `resolved`, an empty id; F-REVIEW-003 lists them.
     REVIEW-004 says "any part not valid" without defining valid, REVIEW-002 says "valid threads", and the only trace is the "or with
     no comment" half of REVIEW-007 scenario 2, which is outside that SHALL (it says "more than 200").
   - Fix: add one SwRS, for example "A thread needs a unique id, one to 200 comments, valid lines and ISO dates": SHALL treat the file
     as not valid when a thread id repeats, a thread holds no comment, `endLine` is before `line` or a date is not an ISO 8601 date-time
     with a zone; and remove "or with no comment" from REVIEW-007 (or rename it "no comment or more than 200").

9. SwRS-MDOKFSTUDIO-REVIEW-073 duplicates SwRS-MDOKFSTUDIO-TRUST-066 (cross-scope, trust-security).
   - Evidence: TRUST-066 specifies "previewCommentCreate, Reply, Resolve or Delete ... dropped unless its document and request identifiers
     equal those of the render the host holds, whatever its revision"; REVIEW-073 says the same ("names the shown document and render ...
     whatever revision"), same code (`PAGE_MESSAGE_GATES` gate `comment`, `PageMessageDispatcher.handle`).
   - Fix: keep TRUST-066 (the gate table belongs to trust-security next to TRUST-065); delete REVIEW-073 and move its verification
     (`commentWrite.test.ts` "a create with an old documentVersion must still be written") to TRUST-066.

10. SwRS-MDOKFSTUDIO-REVIEW-181 duplicates SwRS-MDOKFSTUDIO-BLOCK-227 (cross-scope, block-editing).
    - Evidence: BLOCK-227 "When the host holds an open block edit and receives a reply to, or the deletion of, an inline thread, it SHALL
      answer "Save or cancel the open Markdown edit before changing a thread." and change nothing" is the same behaviour and text as
      REVIEW-181 (`handleThreadChange`: `preview.edits.active`).
    - Fix: keep REVIEW-181 (inline threads are this scope's feature, and StRS-016 is derived here) and remove BLOCK-227 from block-editing
      (ask that scope's owner; its StRS keeps another SwRS), or the reverse, but only one of the two.

11. SwRS-MDOKFSTUDIO-REVIEW-165 duplicates SwRS-MDOKFSTUDIO-PALETTE-086 (cross-scope, palette-slash); REVIEW-166 overlaps PALETTE-003.
    - Evidence: PALETTE-086 "Cmd+/ or Ctrl+/, with or without Shift, in a block text box ... match the shortcut of the TODO action" and
      REVIEW-165 are the same `shortcutFor` rule (`paletteActions.ts` todo: `shortcut`, `anyShift`, `modifier: "any"`). PALETTE-003 already
      lists the TODO and Thread buttons of the palette; the REVIEW-166 palette scenario is that fact again. The slash aliases `todo`, `fixme`,
      `task` and the title "Toggle TODO comment" are in no palette-slash SwRS (PALETTE-263/266 list other aliases).
    - Fix: delete REVIEW-165 and cite PALETTE-086 in the REVIEW-160 notes; reduce REVIEW-166 to the slash entry ("types todo, fixme or task ->
      TODO action, titled Toggle TODO comment") or move it to palette-slash with the other alias rows.

12. SwRS-MDOKFSTUDIO-REVIEW-169 states the indentation rule more strictly than the parser.
    - Evidence: `inlineThread.ts` `parseThreadBody`: every line after a header belongs to that message and `INDENT = /^(?: {1,2}|\t)/u` strips
      one or two spaces or a tab; an unindented line is kept as text (only a line that matches the header pattern starts a new message).
      "lines after it, indented by two spaces or a tab" would make a conforming implementation reject text at one space or none.
    - Fix: "... and the lines after it up to the next header, removing one indentation of up to two spaces or a tab from each, and keep blank
      lines inside a message", and add the unindented line to scenario 2 or note it.

13. SwRS-MDOKFSTUDIO-REVIEW-091 scenario 2 does not belong to its SHALL.
    - Evidence: the SHALL is "stop each key event so that no other handler sees it"; scenario "Escape ... the popover closes" is REVIEW-027
      (the document-level Escape handler closes the popover, then stops the event). Escape in the reply box also drops the draft, which neither
      requirement says.
    - Fix: replace scenario 2 by "Cmd+Enter in the box sends the reply and stops the event" (tested: `T43: Cmd/Ctrl+Enter sends a reply and keys typed
      in the reply box stay there`).

14. SwRS-MDOKFSTUDIO-REVIEW-132 is unconditional where the code answers differently for malformed messages.
    - Evidence: `handleCreate`/`handleReply` check `normalizeBody` and `isValidAnchor` before `writeComment`, so a read-only preview that sends a
      blank create or reply gets "the comment is empty or too long." / "the reply is empty or too long.", not "comments need a trusted workspace.".
      Resolve and delete (valid shapes only) always get the trust text.
    - Fix: "When the host receives a valid create, reply, resolve or delete message from a read-only preview" (and the same word in the
      scenario "All kinds").

## Re-check (to run after the fixes)

- Defects 1, 7 and 14: grep the four period-less strings and "could not be added" in the SwRS and confirm the final text equals the
  source constants (`sourceEdits.ts` `THREAD_REPLY_REFUSED`, `comments.ts` `refuse`).
- Defects 9, 10, 11: confirm that exactly one SwRS of TRUST-066 / REVIEW-073, BLOCK-227 / REVIEW-181 and PALETTE-086 / REVIEW-165 remains and that the
  removed ids are gone from `derives_from`/`derived_by` of their StRS.

## Re-check

Verdict: FIX-REQUIRED

Scope re-read in full: 215 active SwRS (REVIEW-073 and 190 are `lifecycle: deprecated`; REVIEW-217 is new) and 18 StRS, against
`src/` and `test/` of `markdown-okf-schema-studio-wt-059-b3`. Read-only; no build, no test run.

### The 14 earlier defects

All 14 are fixed in the text and hold against the code:

1. 190 archived. `THREAD_REPLY_REFUSED` is cited by no active requirement; blank and over-long replies stay in 178, non-thread lines in 179.
2. 111 now says "the decision used for exact copies picks none"; scenario 1 is the real test (`T45: two fuzzy matches far apart ...`, both copies more than 50 lines from line 100).
3. 026 is horizontal only; matches `commentThreads.ts` lines 510 to 512 (width `min(360, max(200, W-16))`, left clamped to 8 and `W-width-8`).
4. 057 lists the four refusal causes of `writeComment`; the Criteria names the three answers without a warning (empty body, unknown thread id, unexpected error).
5. 184 states both outcomes in the SHALL (`sourceEdits.ts` line 201 plus the error message).
6. 196, 199, 216 read consistently with `incomingChanges.ts` `post` (lines 56 to 60): empty list when marks are showing or the enabled value changed, nothing otherwise. The Diff-off take-back is in the 196 SHALL and in 199 scenario 2; 216 keeps the setting-off scenario. Not a defect.
7. Periods are inside the quotes in 062, 063, 075, 079 and equal `comments.ts` lines 472 to 503 plus `refuse(\`${reason}.\`)`.
8. REVIEW-217 added; its SHALL, both scenarios and the test `T42: one invalid thread rejects the whole file` hold (lines 0, 5>4, "yesterday", "2026-13-45T99:00:00Z", repeated id, empty comments are all in that test). REVIEW-007 now says only "more than 200".
9. 073 archived; TRUST-066 holds the same behaviour (see new defect 1 for its verification note).
10. BLOCK-227 archived, REVIEW-181 is the only one left.
11. PALETTE-086 archived, REVIEW-165 is the only one left (PALETTE-083 cites it). 166 is narrowed to the aliases `todo`, `fixme`, `task` and the title "Toggle TODO comment" (`paletteActions.ts` lines 325 to 334); the aliases exist in no palette-slash SwRS (PALETTE-266 lists `todo` and `task` only for Checkbox in GFM or MyST, which does not conflict) and PALETTE-003 is cited, not repeated. Modes are additive, so the TODO action is listed in every mode.
12. 169 matches `parseThreadBody` (indent of up to two spaces or a tab, unindented line kept, blank lines kept); its three test titles exist.
13. 091 scenario 2 is now Cmd+Enter, and the cited test exists.
14. 132 now says "valid" create, reply, resolve or delete, and the scenario "All kinds" uses valid messages.

### Special checks

- Known issues: only REVIEW-132, 158 and 180 carry one; all three are true (read-only is also set for a file outside every workspace folder; the Comments button sets `data-sphinx-preview-comments`, which hides only the `comment` kind, while the setting hides `thread` too). None is a test gap.
- No active SwRS cites an archived id (scripted over all four batch-4 scopes and the older ones: no hit in any active SwRS; the only hits are `derived_by` lists of StRS, see the notes below).
- Structure (scripted over 215 SwRS): heading = title, description = Normative paragraph (after YAML unescaping), one SHALL, two scenarios, no relative or internal id; StRS of the scope hold no path, message name, ms or px. All 18 StRS are derived by at least two active SwRS; every `derives_from` resolves; `derived_by` of the StRS equals the `derives_from` of the SwRS except the two archived ids below.
- Test titles: every backticked test title of the active SwRS was found in `test/` (scripted).
- Behaviours now specified nowhere because of the orchestrator's removal of "see also" lines: none concerns this scope. The patched-record nonce, stale or malformed patch fields and the scroll report belong to lifecycle-sync and trust-security and are outside the review-annotations text.

### Defects (2)

1. SwRS-MDOKFSTUDIO-TRUST-066 (trust-security) lost the verification that REVIEW-073 held and says "Untested" for a behaviour that is tested.
   - Evidence: TRUST-066 Verification notes: "Method: Untested. Read from the comment gate in PageMessageDispatcher.handle ...". The integration test `test/integration/commentWrite.test.ts` (lines 108 to 111) sends `previewCommentCreate` with `documentVersion - 1`, asserts the result `[true, "create"]` and the assertion text "a create with an old documentVersion must still be written", and the next lines assert that a wrong document id is still dropped (file unchanged). That was exactly REVIEW-073's Method. The behaviour itself is equal (gate `comment` in `pageMessages.ts` lines 115 to 118).
   - Fix: in TRUST-066 replace the Method with "The integration test test/integration/commentWrite.test.ts (assert "a create with an old documentVersion must still be written"; a create naming another document id is dropped and the comments file is unchanged). The dropped request id is not asserted by a test." and set the Criteria to "The comments file gains the thread for the old revision and is unchanged for the other document." Keep the gate comment as a second sentence if wanted.

2. SwRS-MDOKFSTUDIO-REVIEW-217 Criteria claims more than its SHALL and uses a wrong field name.
   - Evidence: the SHALL lists five defects (repeated id, no comment, end line before line, line below 1, date without zone). The Criteria add "an empty id, a non-boolean resolved flag and a non-string text are refused the same way": they are not in the SHALL (they are REVIEW-004 content), and the field is `body` (the test uses `comment({ body: 7 })`), not "text".
   - Fix: delete that clause from the Criteria (REVIEW-004 already covers the empty id and the resolved flag), or reword it "... (the empty id, the non-boolean resolved flag and the non-string body are covered by SwRS-MDOKFSTUDIO-REVIEW-004)".

### Notes (not counted as defects)

- StRS-REVIEW-005 still lists SwRS-REVIEW-073 and StRS-REVIEW-015 lists SwRS-REVIEW-190 in `derived_by`, as the lifecycle-sync StRS do for their archived ids (e.g. LIFE-008 keeps LIFE-081). This is consistent across the four scopes; if the orchestrator decides that archived ids leave `derived_by`, change both together with the index.
- Cross-scope traces: StRS-PALETTE-027 still lists the archived PALETTE-086 and StRS-BLOCK-021 the archived BLOCK-227 in `derived_by`; the Ctrl+/ shortcut now lives in REVIEW-165, which derives only from StRS-REVIEW-014. Palette-slash and block-editing own those lines.
- The JSDoc of `moveSidecars` still says "a warning says so" (stale code comment, REVIEW-127 is right).
