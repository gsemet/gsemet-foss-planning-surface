Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.3 critic review: block-editing StRS and SwRS

Scope `block-editing`: 26 StRS (BLOCK-001..026), 250 SwRS (BLOCK-001..250), worktree
`markdown-okf-schema-studio-wt-059-b3`, checked against `inventory/block-editing.md`, `src/`, `test/` and the
SwRS already written for other scopes (toolbar-navigation, layout-width, frontmatter-editing, table-editing, gfm, myst,
diagrams, rendering-core). No lint, build or test was run (read-only review). Note: the numbering in the task text
("SwRS-212", "BLOCK-224 thread guard") is one to three off the real ids; the Diagram source click is BLOCK-215, the
thread guard is BLOCK-227.

Verdict: REVISE

## What passed

- Structure (scripted over all 276 files): every frontmatter `title` equals the first `##` heading; every
  `description` equals the Normative behavior sentence; no leftover placeholder; no SwRS or StRS text names a backlog
  item, CR or archive id (CR/STAB ids appear only inside quoted test titles); `derives_from` / `derived_by` are
  consistent both ways (counts per StRS match); every StRS has at least 1 SwRS; each SwRS has 2 scenarios.
- Verification notes name only existing files; every quoted test title exists in its file (scripted; the 5 hits that
  looked missing are `test(\`...\${name}\`)` templates and exist); every `scenarioXxx` and `blockEditing/vNN` named exists.
  Exception: BLOCK-029 (see defect 4).
- Inventory: all F-BLOCK rows 001..075 and 077 are mapped to at least one SwRS; F-BLOCK-076 is doc-only (stale
  `docs/known-limitations.md`, a P10.5 fix, not a requirement), acceptable.
- Read about 62 percent of the SwRS against code (001-003, 005, 008-011, 013-018, 022, 024-026, 029-030, 033-037,
  039-054, 057, 060-068, 072-073, 079-084, 087-089, 090-117, 119, 123-124, 127, 130-135, 138-140, 145-147, 152-156,
  160-163, 166-170, 172-179, 182-187, 189-190, 191-205, 209, 214-221, 223-229, 244-250). Strings, numbers and defaults
  verified: 400 ms, 32 characters, tab size 4, 2 px / 1 px outlines, `font-size - 1px`, 6 s move status, 4 s notices,
  5 s flights and pin lifetime, 5 s reload window, 1.5 s flush waits, 100 000 px pins, 100-char ids, 40-entry trace,
  all quoted refusal texts and aria labels, the placeholder text, AltGr handling in wrap vs chord.
- Known issues confirmed true against the code: 039 (`status` is appended to the frame only for a cell,
  `blockEditor.ts openBlockEditor`), 041 (`openBlockEditor` returns while `activeBlockEdit` exists; blur on a changed
  editor leaves it finishing), 047 (Done, Ctrl+Enter and blur call `postBlockEditSave(true)`, which only refuses
  non-final saves while finishing), 094 (`planInsertion` finds line ends with `indexOf("\n")` only), 123/183/218/248
  (page-state and render gates drop an older render silently; `reportStaleEdit` answers only save, cancel and
  frontmatter save; mouse arrows keep `data-sphinx-move-pending` with no timer, keyboard flights time out at 5 s;
  `blocksFlight` 5 s), 138 (`moveChordDirection` never reads AltGraph), 179 (`checkBlocksPaste` tests the one line only),
  216 (error branch of `receiveBlockEditSource`; frame has no buttons, refresh stays disabled, edit mode off closes it).
- SwRS-215 (the "Diagram source" click, F-DIAG-014): true by the code. `normalizeDiagram` puts the source position on
  the `figure` only, the `summary` has none, so the document click handler of `pageInput.ts` resolves the figure as the
  mapped target, calls `preventDefault` (which stops the `details` toggle) and `openMappedEditor`. Wrongly absent:
  nothing; the "Untested" note is honest. Small gaps in defect 17.

## Defects (18)

1. SwRS-MDOKFSTUDIO-BLOCK-134 and BLOCK-160 (and the StRS-014 rationale line): a refused keyboard or selection-key
   move does NOT show its reason. Evidence: `blockMoves.ts receiveBlockMoveResult` finds the bar with
   `data-sphinx-move-pending`; only the arrow `click` handlers in `addMoveButtons` set it. `requestBlockMove` and
   `requestSelectionMove` via Alt+Arrow never do, so `if (!point) return;` ends silently. The test
   `T37: a refused keyboard move can be retried` asserts only the second message. BLOCK-134 scenario 1 ("the reason is
   shown next to the bar") and BLOCK-160 scenario 1 ("the reason is shown next to the bar") are false for the keys.
   Fix: in BLOCK-134 and BLOCK-160 remove "the reason is shown next to the bar" from the key scenarios (keep it for the
   arrow, BLOCK-116) and add to both: "Known issue: a move refused after a key press shows no reason, because the
   status is attached to the bar marked pending by an arrow click and a key press marks none." StRS-014 rationale: say
   "a move refused after an arrow click shows a reason next to the bar".

2. BLOCK-057, scenario 2 is false in the common case. `completeActiveBlockEdit` refreshes when `hasAppliedEdit` and
   `document.revision !== stage.activeDocumentRevision`. A final save whose text equals the text last written (the usual
   Done after an autosave) still renders. Only a held edit that never applied anything renders nothing.
   Fix: scenario 2 becomes "GIVEN a held edit for which no autosave changed the document; WHEN its final save carries the
   original text; THEN no render is started"; add a third sentence in Method that the autosaved-then-Done case renders once.

3. BLOCK-024 scenario 2, BLOCK-015 scenario 2, BLOCK-018 (and F-BLOCK-010): "the link behaves as in reading mode and no
   editor opens" / "no editor opens on a link" is not supported by the code. Only block elements carry
   `data-sphinx-source-line` (`mystRenderer.ts` / `sourceMapping.ts`), so for an inline link in a paragraph
   `event.target.closest(MAPPINGS_SELECTOR)` is the paragraph and `target.closest("a")` is null. The document click
   handler then calls `openMappedEditor` after `linkNavigation.activate` (bound first) has posted `previewLink`; the
   `keydown` handler excludes only `a[data-sphinx-preview-navigation^="okf-link:"]`, not other links. The hover rule
   (`editHoverTarget`) likewise outlines the paragraph under a hovered link. No test clicks an inline link in edit mode.
   Fix: either add a unit test that clicks a link in a mapped paragraph and make the scenarios match what it shows, or
   (if the editor opens) change the scenarios, add a Known issue ("a click on a link inside a paragraph in edit mode
   follows the link and also opens the paragraph editor") and narrow BLOCK-018 to "an element that is itself inside a
   link". Mark the link half "Untested" until then.

4. BLOCK-029, Verification notes: "Unit test `edit mode loads raw Markdown and saves changes when the block loses
   focus` ... reads the names" is false. That test (runtimeBlockEditor.test.ts:255) asserts button labels, never
   "Raw Markdown editor" or "Raw Markdown block". The names are read by `runtimeContentPatch.test.ts` (region name in a
   recorded op) and the visual checks (`capture_layout_checks.py` locators). Fix: Method must name those, say the unit
   suite does not assert the text box name, and keep "Untested" for the region name in the unit layer.
   Also BLOCK-030: `spellcheck` false is asserted nowhere (only autocorrect, autocapitalize, autocomplete in
   `active Markdown editors leave ...`); say so.

5. BLOCK-060 (CRLF Known issue, deduced not run) is stated as fact beyond the code evidence. The body says the block "is
   saved with LF inside, because the text box reports LF; the host then compares ... and can refuse a second save".
   Repo code shows only: the `textarea` value uses LF (browser behaviour), `edit.trailingLineEnding` restores the trailing
   break only, `minimalReplacement` produces LF text, `lastSavedText` is that LF text, and the next
   `drainActiveBlockEdit` compares `document.getText().slice(start, start + lastSavedText.length)` with it. That the
   file then holds CRLF (VS Code converting inserted text to the document EOL, no code in `host-vscode/documents.ts`
   does it) and that the slice therefore differs is an inference about VS Code, not evidenced here. StRS-024 repeats
   it. Fix: rewrite the Known issue as "Known issue (deduced from the code, not run): no code converts the text box's LF
   back to the document's line ending inside a multi-line block. If VS Code writes the LF text into a CRLF document as
   CRLF, the next save finds a different text under `lastSavedText` and is refused with "The source block changed while
   it was being edited."". Keep the same hedge in StRS-024 ("may"), and keep "No test opens ..." in Method. Alternatively
   run it once in the real window and state the observed result.

6. BLOCK-052, BLOCK-053, BLOCK-055 say the editor closes "without posting any message" / "no message is posted", but
   BLOCK-196 (and `closeBlockEdit`, `edit.reportClose`) posts `previewEditClosed` for an unchanged or cancelled editor
   that the host watches. Fix: add "except the close report of SwRS-MDOKFSTUDIO-BLOCK-196 when the host asked for it"
   in the three THEN clauses, or word them "posts no save and no cancel".

7. Duplicates inside the scope:
   - BLOCK-191 scenario 2 and BLOCK-219 scenario 1 are the same assertion (first save whose original text differs,
     answer "The source block changed while it was being edited."). Fix: in BLOCK-191 drop scenario 2 and use as boundary
     "a second save of the held edit does not take the original text from the document again"; keep the refusal in 219.
   - BLOCK-101 scenario 2 (save of an insertion after a missing line, "The preview is stale. Reopen the block before
     saving.") is covered by BLOCK-220 ("a first previewEditSave names lines ... that do not fit"). Fix: BLOCK-101 keeps
     the open (insertion) refusal only; make 220 cite insertions explicitly in its scenario 1, or give 101 only the open
     message and a boundary scenario of an existing line.
   - The same Known issue ("an older render is dropped without an answer") is written in 4 places (123, 183, 218, 248,
     with different tails). Fix: keep the full text in 248 (the gate), and in 123, 183, 218 write one line "Known issue: see
     SwRS-MDOKFSTUDIO-BLOCK-248" to avoid drift when it is fixed.
   - BLOCK-139 is contained in BLOCK-136/138 and in the macOS test they share; BLOCK-076 and BLOCK-077 are the same rule
     seen from both sides (the second has no behaviour of its own: "does not stop propagation"). Fix: merge 077 into 076
     as its boundary scenario and archive 077; merge 139 into 138.
   - BLOCK-014, BLOCK-021, BLOCK-023 and BLOCK-215 (open part) are one behaviour (click a mapped block opens the editor of
     the mapped ancestor); 021 and 023 add no code path (the image and admonition "cases" are `closest(MAPPINGS)`).
     Fix: merge 021 and 023 into 014 as scenarios (keep only the linked-image capture handler, BLOCK-022, separate).

8. Duplicates of other scopes (cite by id, do not restate):
   - BLOCK-012 "A read-only preview has no Edit button" = SwRS-MDOKFSTUDIO-TOOLBAR-002 (same title). Fix: archive
     BLOCK-012 and let StRS-002 derive from TOOLBAR-002 (cross-scope `derives_from` is allowed); BLOCK-013 (page side
     "starts in reading mode") stays.
   - BLOCK-224 "host refuses block editing in a read-only preview" = F-TRUST-007 (trust-security inventory). BLOCK-121 and
     BLOCK-181 (move and clipboard read-only refusals) are rows of the F-TRUST-008 matrix. Fix: orchestrator decides the
     owner before P10.3 of trust-security; the cheapest is to keep 121/181/224 here and have trust-security cite them.
   - BLOCK-227 "thread reply or delete refused while a block edit is open" = F-REVIEW-055 (review-annotations). Fix:
     move to review-annotations (host guard `handleThreadChange`), and note there that the page also blocks with the
     different text "Save or cancel the open edit before changing a thread." (`runtime.ts blockedReason`), which BLOCK-227
     does not mention.
   - BLOCK-200 "block or field editor" overlaps SwRS-MDOKFSTUDIO-FMEDIT-058 (Refresh blocked while a field editor is
     open). Fix: restrict BLOCK-200 to the block editor and cite FMEDIT-058 for the field editor.
   - BLOCK-029 scenario 2 (table cell frame name) duplicates TABLE-012's fallback; BLOCK-078/076 say "serves the table cell
     and the field editors" (TABLE-047 exists). Fix: scenario 2 of 029 -> cite TABLE-012; add cross-references.

9. Wrong cross-scope pointers: BLOCK-105 (Method) and BLOCK-108 (Method) say the Start writing spacing is
   SwRS-MDOKFSTUDIO-LAYOUT-013, which is "Collapsing the toolbar measures the clearance again". Start writing is
   LAYOUT-010 (40 px) and LAYOUT-015 (pushed only under the toolbar). Fix: replace 013 by 010 and 015.

10. Relative references in requirement text: BLOCK-104 scenario 2 ("next requirement"), BLOCK-109 scenario 2 ("see the
    selection move requirements"), BLOCK-120 scenario 2 ("see the glue requirement"), BLOCK-083 / BLOCK-101 / BLOCK-182
    Method ("the next requirement", "the first insertion requirement", "the clipboard key ownership requirement"),
    BLOCK-227 Method ("above"), StRS-024 ("see the software requirement"), BLOCK-014 scenario 2 ("specified with the
    scroll and reveal behaviour": no such SwRS exists yet). These break on reorder. Fix: replace each with the id
    (105, 156/164, 119, 084, 094, 189, 114/174, 060); for BLOCK-014 scenario 2 either cite the lifecycle-sync id once it
    exists or delete the scenario and keep a boundary of "edit mode off: no previewEditOpen posted".

11. BLOCK-232, BLOCK-233, BLOCK-234, BLOCK-235 specify internal helpers, not extension behaviour: `applyTextEdits`,
    `RangeError`, "the core counts lines", `isRefusal`. No writer can observe them; scenario 2 of 235 only checks a type
    guard. Same style in BLOCK-128/225 scenarios ("GIVEN applyEdits resolves false"), BLOCK-127 ("after the planner's own
    checks"), BLOCK-249/250 (`window.__studioDiagnostics`, `callers`). Fix: archive 235; merge 232 and 233 into one
    "overlapping or out-of-range planned edits are refused and nothing is written" worded on the observable effect
    (a move/cut/paste request whose edits overlap leaves the document unchanged); keep 234 as the line-ending rule behind
    StRS-024; rewrite the GIVENs of 128/225 as "VS Code refuses the edit"; drop the planner wording from 127.

12. BLOCK-250 omits a bound: `callers()` returns at most 3 names (`names.slice(skip, skip + 3)`), also skips frames whose
    name starts with `<`, and strips a leading `Object.`. The scenario has exactly 3 names so the cap is invisible.
    Fix: Normative "... the nearest named functions of that stack, at most three, innermost first ..." and a boundary
    scenario with 5 frames returning 3 names.

13. BLOCK-008 misses the read-only condition in the code (`initialEditMode: !preview.readOnly && choices.editMode === true`,
    `rendering.ts:387`). Normative says "only when the edit mode stored for the workspace is true"; scenario 2 lists false,
    absent and non-boolean, not "read-only". Because StRS-002 says "except in a preview that cannot edit the file", add
    to the Normative "and the preview is writable" and add the read-only case to scenario 2.

14. StRS wording (use cases must not leak implementation, messages, numbers):
    - StRS-025 ("When the page asks for a change of the document ... checks the lines and the version of every request
      ... A malformed request is ignored") is protocol language. Fix: "When a writer's edit, move, cut or paste reaches
      the file, the Studio SHALL change exactly the lines the writer meant or leave the file as it was"; move the
      request/version rationale to the SwRS.
    - StRS-017 ("also across a full page reload within five seconds"), StRS-016 ("a content patch"), StRS-006 ("as small
      changes to the file and not as a rewrite of the whole block"), StRS-019 ("hold back every update that would replace
      the page"), StRS-022 ("scrolls the page by the palette height", "asks the next render") name numbers and
      mechanisms. Fix: state the user-visible effect ("the selection stays after the move", "the text I type is not
      replaced while I type", "the text stays where I looked").
    - StRS-026 (maintainer reads an editor trace) is not observable in VS Code; its SwRS 249/250 are test support. Fix:
      keep as StRS only if the project accepts a maintainer use case; otherwise set `annotation_exemption` false but
      derive 249/250 from a quality StRS "editor failures are diagnosable" without naming the trace.
    - StRS-007 holds two outcomes (keep and restore) in one SHALL; split "Finish an edit" and "Abandon an edit", or
      state it as one use case "I choose to keep or to drop what I typed" with one outcome each in the SwRS (as is).
    - StRS-002 lists "a file outside the workspace" and "a standalone file" as two cases; they are one (F-TRUST-001).
      Same in SwRS-012. Fix: "a file outside every workspace folder".

15. BLOCK-016 / StRS-003 mismatch for nested lists: `editingElementFor` uses `target.closest("ul, ol")`, the nearest list, so
    a click on an item of a nested list opens the nested list only, not "the whole list" (StRS-003 rationale, BLOCK-016
    scenario 1 title). Method admits nested lists are untested. Fix: add a scenario "a nested item opens its own list
    (the innermost list)" and mark it untested, or add a Known issue; correct the StRS rationale to "the list that holds
    the clicked item".

16. BLOCK-047 Known issue says "Only Cancel and the palette focus-leave check the finishing state." Also
    `navigateBlockEdit`, `moveBlockFromEditor`, `cancelBlockEdit`, `flushOpenEditors` and the paste `isCurrent` check
    `edit.finishing`. Fix: "Done, Ctrl+Enter and the text box blur have no guard (they call `postBlockEditSave(true)`)".

17. Small scenario/Method gaps:
    - BLOCK-215 scenario 2: in reading mode the same click also posts `previewReveal` (generic branch of the click
      handler); say "the disclosure toggles and the click reveals the source line".
    - BLOCK-021 Method: visual v05 clicks the admonition title only; scenario 2 (body click) has no test; say so.
    - BLOCK-090 Method: v08 asserts the list hover and editor (its lock text equals v06/v07), not the plus button
      visibility; say "not asserted".
    - BLOCK-193 lists five kinds of held-back work (render, theme, PlantUML, link refresh, include change); code supports
      all (`hostEvents.ts`, `viewState.ts`, `frontmatter.ts`, `plantUml.ts`) but only the render is tested; say so.
    - BLOCK-037 bundles five layout facts (75 percent font, one row, buttons right, centred, wrapping) in one SHALL; split
      "status line and buttons share one row" from "buttons wrap below at narrow width", or move the font ratio to
      layout-width.

18. BLOCK-065 title/normative bundle two constructs (quote prefix, indentation) and BLOCK-064 bundles list marker,
    number increment, checkbox reset and item split in one SHALL with 4 scenarios in the Method; the user-visible rule is
    one ("Enter continues the construct of the line"), so keep them but state in Normative the closed list of constructs
    (list marker, quote prefix, indentation) to make the "one SHALL" bounded. (Low.)

## Counts

Defects 18 (blocking: 1, 2, 3, 4, 5, 7, 8, 9; non-blocking: 6, 10-18). After fixes 1-5 and the duplicates (7, 8) the
SwRS count drops by about 8 to 12 (archive 012, 077, 139, 021/023 merged, 235, 232/233 merged), which the orchestrator
must re-derive in the StRS `derived_by` lists via `okfreq`.

## Re-check

Scope after revision: 25 active StRS, 241 active SwRS (11 SwRS and StRS-026 archived: 012, 021, 023, 077, 139, 227,
232, 233, 235, 249, 250), worktree `markdown-okf-schema-studio-wt-059-b3`. Read-only: no build, lint or test was run.

Scripted over all 1312 requirement files of the worktree: all frontmatter parses, no duplicate uuid, `title` equals
the first `##` heading and `description` equals the Normative sentence in every active block-editing file, exactly one
`SHALL` per SwRS, every SwRS has at least 2 scenarios with balanced GIVEN/WHEN/THEN, `derives_from` / `derived_by` are
consistent both ways, no active requirement of any scope derives from or cites an archived BLOCK id in its body (no
reference to BLOCK-012/021/023/077/139/227/232/233/235/249/250 anywhere outside the archived files themselves; the
archived ids stay in the `derived_by` of their StRS, which is the okfreq convention seen in the other scopes), every
quoted test title and every `test/` or `src/` path named in the Verification notes exists.

The 18 earlier defects:

- 1 (key-press refusal reason): fixed. BLOCK-134 and BLOCK-160 now carry the Known issue; true by
  `blockMoves.ts` (`data-sphinx-move-pending` is set only at lines 232 and 237, in the arrow click handlers; the key
  handler `bindKeys` never sets it). StRS-014 rationale reworded.
- 2 (057): fixed (autosaved-then-Done renders once; no-render case is the held edit without autosave).
- 3 (link click): fixed in 018 and 024 (narrowed to "an element that is itself inside a link" plus a Known issue,
  verified by `pageInput.ts` and `editHoverTarget`: `mapped.closest("a")` is null for a paragraph that holds a link).
  The same flaw survives in the Enter/Space path, see defect 3 below.
- 4 (029/030 verification notes): fixed.
- 5 (060 hedge): fixed ("deduced from the code, not run"; StRS-024 says "may"). Consistent with the code: no EOL
  conversion in `src/page` or `src/core/edits` for a block text; only `document.eol` for thread replies.
- 6 (052/053/055 vs 196): fixed.
- 7 duplicates: fixed (191/219, 101/220, 123/183/218 now point to 248, 076/077 and 138/139 merged, 021/023 merged into
  014).
- 8 other scopes: fixed (012 archived, 200 narrowed with FMEDIT-058, 029 cites TABLE-012). 227 is archived but
  `requirements/tiers/swrs/review-annotations/` holds only an `index.md`; the orchestrator must keep the hand-off
  ("thread reply or delete refused while a block edit is open", host `handleThreadChange`, and the different page
  text "Save or cancel the open edit before changing a thread.") for the review-annotations analyst. Not a defect of
  this scope.
- 9 (LAYOUT-013): fixed (LAYOUT-010 and 015; LAYOUT-008 and 014 exist and are active).
- 10 relative references: fixed (no "next requirement", "above requirement", "see the ... requirement" left).
- 11 internal helpers: mostly fixed (235, 232, 233, 249, 250 archived; 128/225/127 reworded) but the replacement
  SwRS-252 is itself wrong, see defect 1 below.
- 12 (250), 14 (StRS wording, 026), 15 (016 nested list), 16 (047), 17 (215, 021, 090, 193), 18 (064/065): fixed.
  Exception: 037 still bundles two facts, see defect 5 below.
- 13 (008 read-only): fixed (`initialEditMode: !preview.readOnly && ...`).

The new Known issues were checked against `src/`: 134/160 true (above); 018/024 true by `pageInput.ts` (click handler
resolves the paragraph through `MAPPINGS_SELECTOR` and `target.closest("a")` is null; `linkNavigation.activate`
posts `previewLink` and does not stop the later document listener); 060 is correctly hedged; 216 and 248 true
(`previewEditOpen` is gated `page-state`, the four move/clipboard types are gated `render`; 218 pointing to 248 is a
loose but acceptable pointer).

Verdict: FIX-REQUIRED

Defects (5; 1 to 3 are false or overclaimed statements, 4 and 5 are low):

1. SwRS-MDOKFSTUDIO-BLOCK-252 ("Overlapping or out-of-range planned edits leave the document unchanged") describes
   production behaviour that does not exist. Evidence: `applyTextEdits` (`src/core/edits/textEdit.ts:31`, the only
   thrower of the RangeError) is called in one place, `src/host-memory/memoryDocumentStore.ts:112`, the in-memory
   document store of the test host. The real host (`src/host-vscode/documents.ts`) hands the edits to VS Code
   unchanged; whether VS Code refuses overlapping edits is VS Code's rule, and the extension then reports it through
   BLOCK-128 / BLOCK-225. The Normative says "the extension SHALL refuse", scenario 2 says "refused with a range
   error", and the Method admits "no integration test reaches it". It is the old 232/233 helper requirement under a
   new id, deriving StRS-025. Exact fix: archive SwRS-252 (StRS-025 keeps 234, 236..248 and the others as
   derived_by; re-run okfreq to drop 252 from `derived_by`). Do not restate it for the in-memory store.

2. SwRS-MDOKFSTUDIO-BLOCK-078, Verification notes, Method: "The same rule serves the table cell editor
   (SwRS-MDOKFSTUDIO-TABLE-047) and the field editors." TABLE-047 is `lifecycle: deprecated`
   (`requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-047.md`, "The policy is page-wide; this requirement
   states the cell case"), so the cite dangles. Exact fix: replace the sentence with "The same rule serves the table
   cell editor and the field editors." (no id; BLOCK-078 is the owner).

3. SwRS-MDOKFSTUDIO-BLOCK-015, scenario "Keys that stay with their control": GIVEN "... a navigation link ..."
   THEN "no block editor opens" is false for links in the body. Evidence: the `keydown` listener of
   `src/page/features/pageInput.ts` (line 221) returns only for `a[data-sphinx-preview-navigation^="okf-link:"]`,
   and `okf-link:` requests are generated only in the properties table (`src/core/frontmatter/propertiesTable.ts:46`).
   For Enter or Space on a focused link inside a paragraph, `closest(MAPPINGS_SELECTOR)` is the paragraph,
   `target.closest("a")` is null, so `openMappedEditor` runs (and `linkNavigation` also posts `previewLink`): the same
   defect the analyst already recorded for the click in 024. Exact fix: in 015 replace "a navigation link" by "a link
   value of the properties table" and add "Known issue: Enter on a focused link inside a paragraph follows the link and
   also opens the paragraph editor (deduced from the keydown listener; no test)", or reference the Known issue of
   SwRS-MDOKFSTUDIO-BLOCK-024.

4. SwRS-MDOKFSTUDIO-BLOCK-052, Method cites only `Escape in an unchanged Markdown block editor closes it without a
   message` and `T28: Done on an untouched empty insertion closes without saving` for a scenario that promises the
   same for Done, leaving the text box and Ctrl+Enter on an unchanged (non-empty) block; no test in `test/` presses
   Done, blurs or sends Ctrl+Enter on an unchanged existing block (only `runtimeTableCellEditor.test.ts:879`, edit mode
   off). Exact fix: add to Method "Done, blur and Ctrl+Enter on an unchanged existing block are untested; Escape and
   Done on an empty insertion are asserted".

5. SwRS-MDOKFSTUDIO-BLOCK-037 still holds two unrelated facts in one SHALL (the 75 percent font size of the status
   line, and the one-row layout with right-aligned, vertically centred buttons); the wrapping half was split into 251
   but the font ratio was not moved. Exact fix: drop "set at 75 percent of the parent font size" from the Normative
   and the "Font size" scenario of 037, and either state it in a one-sentence SwRS of its own or move it to
   layout-width; keep the Normative to the single row.

Not defects of this scope (for the orchestrator): `toolbar-navigation` SwRS-TOOLBAR-013, 015, 073, 114 cite archived
THEME-052, THEME-053 and TABLE-030 in their bodies; the 227 hand-off to review-annotations above.
