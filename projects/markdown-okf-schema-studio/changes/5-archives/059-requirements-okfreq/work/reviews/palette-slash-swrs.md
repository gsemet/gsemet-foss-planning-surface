Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.3 critic review: palette-slash StRS and SwRS

Scope `palette-slash`: 27 StRS, 270 SwRS (PALETTE), reviewed against `inventory/palette-slash.md`, the sources and
tests of `markdown-okf-schema-studio-wt-059-b3`, and the defect classes of the batch-3 reviews. Read-only review: no
lint, no build, no test run.

Verdict: REVISE

## What passed

- Structure (scripted over all 297 files): heading equals title in all 270 SwRS; description equals the Normative
  behavior paragraph in all of them (the 12 differences of a naive diff are YAML quoting only); exactly one SHALL
  each; `derives_from` and `derived_by` are consistent in both directions; every StRS has children; no leftover
  placeholder, no backlog or UX id and no F-id in a normative sentence or scenario.
- Coverage: F-PALETTE-001..105 are mapped except F-PALETTE-101 (registry integrity: icons, one handler per
  descriptor), which is a test-only invariant and is rightly not specified, and F-PALETTE-105 (table toolbar), which
  belongs to table-editing.
- Read: 100 percent of the 270 SwRS were read in full; about 65 were checked line by line against source
  (`paletteActions.ts`, `slashMenu.ts`, `editPalette*.ts`, `hostRequests.ts` x2, `bibScan.ts`, `mystTargets.ts`,
  `figureDirective.ts`, `figurePanel.ts`, `editorChrome.ts`, `pageMessages.ts`, `hostToPage.ts`, `pageToHost.ts`,
  `propertiesStyles.ts`, `editPaletteStyles.ts`). Numbers confirmed: 15 / 8 / 15 buttons per mode (38 in all), 9 x 9
  grid, 16 swatches, 8 emoji per row, 4 px sticky offset, 40 percent and 520 px, +12 px scroll padding, 8 px caret gap,
  +2 px alert list, 320 px slash menu and 1400 z-index, 3 px starting offset, 6 s / 10 s / 30 s / 10 min timeouts,
  edit id 1..100, 500 labels, 1000 keys, 80 characters, 20 files, 2 MiB, 5 s, 14,000,000 base64 characters,
  10 MiB, `-1000` suffix, 1,000,000 HTML characters, scores 1000 / 600 / 400, aliases of every command, all warning
  and refusal texts of 144, 146, 157-159, 166, 175, 187, 191, 193, 194, 197, 205-207. The Reference list
  (previewListTargets) really has no read-only check (182) and the citation list does (187).
- Result message gate: correct. `hostToPage.ts` registers the six `<type>Result` messages with `own-id`
  addressing and `runtime.ts` / `hostRequests.ts` (page) match by edit id and type only, as SwRS-172 and 173 say; the
  request gate is `render` for all six types (`PAGE_MESSAGE_GATES`), as SwRS-174 says.
- Test citations: all 370 `Unit test <title> in <file>` citations name an existing test title in an existing file;
  the integration suites (`paletteMode`, `mystPickers`, `imagePicker`, `imagePaste`, `pasteImageWrite`), the 21
  `palette-slash/...` scenario ids and the `scenario*` functions of `realInput.test.ts` exist.
- Cited external ids all exist, are `draft` (none deprecated) and specify what is claimed: TABLE-063, 073-076, 079,
  085, 089, 090, 093, 106, 111, 115, 117, 124; BLOCK-051, 086, 230, 231; LAYOUT-001, 009, 042; FMEDIT-066;
  CORE-046, 050, 051, 068; GFM-030, 034; MYST-033; DIAG-018.
- StRS: user cases, no paths, message names or pixel values; rationales are behaviour.
- Ownership: Thread button (114) has no twin in review-annotations (REVIEW-167..194 are inline-thread display and
  changes), so it stays here. REVIEW-155 is NOT a TODO duplicate: it is the show-comments setting post; the real
  overlaps are in defects 8 and 9.

## The shared Known issue (SwRS-181, 188, 191, 195)

The brief names SwRS 181, 186, 199; the files carrying it are 181, 188, 191 and 195 (186 and 199 have none).

Verified in code: it is a real bug, not a test gap.

- `hostRequests.ts:handleListTargets/handleListCitations/handlePickDocument/handlePickImage` call
  `sessionDocuments.ts:currentPreviewDocument`, which requires `document.revision === message.revision` and
  `stage.activeDocumentRevision === document.revision`.
- The page stamps every request with `context.revision`, the render revision (`blockEditor.ts`, never updated while the
  editor is open), so the gate `matchesCurrent` passes.
- An autosave (`blockEdits.ts:drainActiveBlockEdit` -> `host.documents.applyEdits`) moves `document.revision`;
  `completeActiveBlockEdit` re-renders only when the editor closes (`releaseHostEditKeepingEditor`: "page updates keep
  waiting for the editor to close"). So after the first autosave of the open editor, and the autosave follows every
  palette button edit and every pause in typing, the five calls (Reference, Citation, Document link, Image, Figure
  Browse) answer "The preview is out of date..." until the editor is closed. The text "Try again once it has refreshed"
  cannot come true.
- The maintainers knew: `HostRequestController.handlePasteImage` documents "the editor's autosaves move the document
  version, so neither is checked", `page/modules/hostRequests.ts` matches the answers by edit id "because the edit
  itself can move the document version", and `hostToPage.ts` registers the results as `own-id`. The picker and list
  handlers were not given the same treatment. The paste handlers (200, 202) are unaffected: that contrast is the
  evidence the refusal is unintended.
- Not covered by any test: `imagePicker.test.ts` and `mystPickers.test.ts` never edit before asking.

The four texts are word for word identical, so they are consistent, but see defects 1 to 6.

## Defects (21)

1. SwRS-181, 188, 191, 195: the same Known issue paragraph is copied four times. Keep the full text once, in
   SwRS-181 (first by number, owns the label list), and in 188, 191, 195 write
   "Known issue: same cause as SwRS-MDOKFSTUDIO-PALETTE-181 (the autosave of the open editor makes this refusal
   permanent until the editor closes)" (the block-editing precedent: BLOCK-101, 123, 183). In 191 the issue concerns
   only the stale clause, say so.

2. SwRS-181 (the owner), Known issues: understated and not reachable from the user-facing requirements. Rewrite as
   "after the editor has saved any change, whether by the autosave after typing or by a palette button, Reference,
   Citation, Document link, Image and the Browse of the figure form answer the out-of-date reason until the editor is
   closed; the paste of an image or of rich text is not affected (SwRS-200, 202)". Replace "(deduced from the code, not
   run)" by the code reference `sessionDocuments.ts:currentPreviewDocument` (the code settles it). Add one line
   "Known issue: see SwRS-MDOKFSTUDIO-PALETTE-181" to the SwRS the writer actually meets: 109 (Image), 140 and 144
   (Reference and Citation lists, whose error text is this reason), 148 (Document link), 150 and 168 (Figure, Browse).
   None of them mentions it today.

3. SwRS-181, 188, 195, Scenarios "Stale revision" / "Stale preview": "GIVEN a document edited since the render" is
   exactly the bug trigger, presented as intended behaviour. Reword the scenarios to the intended trigger (the
   document changed outside the editor after the render, so the request names an older text) and leave the editor's own
   autosave to the Known issue.

4. SwRS-195, Verification notes, Method: false evidence. `test/integration/imagePicker.test.ts` sends
   `revision: document.version + 5`, which `PAGE_MESSAGE_GATES: render` drops without any answer; it only asserts
   `ok !== true` ("answered with a refusal or dropped") and no dialog call. It covers SwRS-174, not the refusal answered
   by `handlePickImage`. Fix: "Method: untested for the answered refusal; the integration test `imagePicker.test.ts`
   (stale preview) only shows that a request naming another revision opens no dialog (dropped by the gate, SwRS-174)".
   SwRS-181, 188 and 191 are correctly marked untested.

5. SwRS-191, Normative behavior and title: two behaviours in one SHALL, with a garbled second half ("...or a preview
   that is out of date, The preview is out of date, or the document is not a file."). The Known issue applies to the
   second only. Fix: split into (a) read-only preview answers "Linking a document needs a trusted workspace." and
   (b) a stale preview or a document that is not a saved Markdown file answers "The preview is out of date, or the
   document is not a file."; keep the Known issue on (b). Same split pattern for 194/195 (already separate: good).

6. SwRS-195, Normative behavior: says "a refusal" while 191 gives the exact text and the second scenario of 195
   asserts "The preview is out of date, or the document is not a file." Put the exact answer text in the SHALL sentence
   (code: `handlePickImage`), as 181, 188 and 191 do.

7. SwRS-174: duplicate of a generic requirement and of a sibling pattern. TRUST-065 ("A render-gated page message
   must name the render the host holds", batch 4, trust-security) already lists these six types among its 17;
   BLOCK-248 does the same per family. Keep TRUST-065 as the generic owner; reduce 174 to one sentence that cites
   TRUST-065 and names the six types, and add the BLOCK-248 consequence as a Known issue if kept: a request naming an
   older render is dropped without an answer, so the page waits for its own timeout (6 s, or 10 minutes with the
   blur suspended for a file dialog, SwRS-175/176).

8. SwRS-086 duplicates REVIEW-165 ("Ctrl+/ or Cmd+/ runs the TODO action in a block editor", review-annotations,
   same behaviour, same unit test `shortcutFor accepts Ctrl+/ and Cmd+/ on every platform`). Keep REVIEW-165 (the TODO
   feature owner); delete SwRS-086 (and from StRS-027 derived_by) or reduce it to a citation. 083-085, 087, 088 are
   the shortcut mechanics and stay.

9. SwRS-104, 171, 176 overlap BLOCK-051 ("Moving the focus inside the editor or into a host dialog does not commit":
   no final save when the focus goes to the palette, the link panel, the figure form or while a native dialog is
   open). Keep BLOCK-051 as owner of that rule; in 104 and 171 keep only the control-specific part (what leaving the
   frame from a panel field does, the blur-with-no-target case) and in 176 keep the pending-request/timeout mechanics
   and cite BLOCK-051 for the commit.

10. SwRS-034, 107, 169: 034 already says typing or a mouse press in the text box closes "the open popover, the link
    panel and the figure form"; 107 (panel) and 169 (form) say it again. Make 034 popover-only and keep 107 and 169.

11. SwRS-038, Verification notes: "untested for the palette selectors" is wrong. `previewStyles.test.ts` (CR 046 tests:
    "...turns off every animation and transition", "...the motion layer is short...") asserts that the palette,
    popover and slash selectors sit under the motion mark, have `@starting-style` rules and are listed in the
    reduced-motion rule; only the 3 px offset is unasserted. Also StRS-024 says "unless the writer prefers reduced
    motion" but its only child (038) states no such clause (CORE-050 is only mentioned in a note): add "and show it
    without the fade when the writer prefers reduced motion" to 038, or add a SwRS for it.

12. SwRS-175, Verification notes: the test `a request without an answer times out with an error result` passes
    `timeoutMs: 6000` itself, so the default 6 s and the 10 min of a dialog (the Criteria) are untested. Fix: "the
    explicit-timeout path is tested; the defaults 6 s and 10 min are untested". SwRS-177 ("untested") is partly
    tested: `a dialog request keeps the editor's blur suspended...` calls `cancelAll()` and asserts
    `isDialogOpen() === false`; the "without calling back" and the cleared timers are not asserted.

13. SwRS-159, Criteria: the list of messages is incomplete. `figureDirective.ts:validate` also answers "Choose or type
    the image path." (empty Source) and "A legend needs a caption." (SwRS-159 requires "a Legend only together with a
    Caption" but gives no text for it). Add both.

14. SwRS-183 / 185 (and 184): the truncated flag at the 20-file cap is specified nowhere. `bibScan.ts:search` sets
    `truncated = true` when `files.length >= MAX_BIB_FILES`, so a workspace with exactly 20 `.bib` files shows "More
    entries exist" although nothing was cut. Add to 183 "and mark the list truncated when the cap is reached", and a
    Known issue: the flag is also set when exactly 20 files exist (code, not run).

15. SwRS-044, Criteria: "a # without a following space is not a heading" is wrong for a line that is only `#`:
    `blockEditActions.ts:setHeading` uses `/^(#{1,6})(?:[ \t]+|$)/`, so a lone `#` counts as heading level 1 (no table
    row tests it). Fix: "a # followed by text without a space is not a heading; a line holding only number signs
    (one to six) is one".

16. SwRS-200: bundles three refusal conditions (read-only, not a saved Markdown file, outside the workspace with
    symlinks resolved) in one SHALL, and its Criteria omits the fourth text of `handlePasteImage`, "Save the document
    before pasting an image." (no path, or document id differs from the previewed one). Split into read-only /
    document / folder, or list the four reasons, and state that this handler, unlike the pickers, does not check the
    render revision (see the shared Known issue).

17. SwRS-241, Criteria: "5 above a score of 1000" is imprecise: `slashMenu.ts:rank` adds 5 when `best >= 1000` (an exact
    label scores 1010 because the label gets +10), else 8 for scores of 400 or more. Fix: "5 for a score of 1000 or
    more, 8 for 400 to 999".

18. SwRS-268, Criteria: "Nothing in the Studio says which of the two to use" is opinion, not verifiable behaviour.
    Delete the sentence (the SwRS-005 pointer can stay).

19. SwRS-262..267 (alias lists): five SwRS enumerate about 120 alias strings, 4 of which are asserted by tests
    (their own Methods say so). They are registry data, not behaviours; any alias change breaks the requirement.
    Merge 263-267 into one SwRS "Every command is found by its label and its aliases" with the test-asserted
    examples (bold, link, image, code, quote, hr, table, todo, task, math, figure, ref, admonition, cite) and move
    the full alias table to the Criteria, or keep them and mark the unasserted aliases as untested in each Method
    (done in 263, 266, 267 only).

20. SwRS-029 / 026: `syncPaletteSticky` sets `data-sphinx-palette-static` and the scroll padding on every scroll and
    resize event; the SwRS say "when ... taller than 40 percent" without saying the check reruns on scroll and resize.
    Add "re-evaluated on every scroll and resize" to 026 (code: `bindPaletteSticky`).

21. SwRS-025, Method: "v04 keeps an older id that says not sticky; it checks the sticky palette in a 360 px pane" is
    a note on a test's naming, not verification. Delete it (or move to the test).

## Re-check (planning notes of the first review)

- Defects 1 to 6 (shared Known issue): after the edit the owner text exists once, the other three cite it, and
  109/140/144/148/150/168 point to it; SwRS-195 Method no longer claims the integration test.
- Defect 7 and 8: confirm the final choice against TRUST-065 and REVIEW-165 in `lifecycle` of those scopes (they
  were written in parallel); the same pair of ids must be edited once.
- After defect 5 and 8 re-run `okfreq lint` and `update-coverage` (derived_by of StRS-013, StRS-021, StRS-027 change).
- Backlog: the shared Known issue deserves a backlog fix item (answer from the render the page holds, or match by
  edit id like the Result messages); not a requirement text.

## Re-check

Verdict: FIX-REQUIRED

Scope re-read: 270 earlier SwRS minus 2 archived, plus the new 271-273 (271 SwRS in all, 27 StRS). Scripted over all files:
one SHALL each, `derives_from`/`derived_by` consistent both ways, every cited SwRS/StRS id exists, no active
requirement cites an archived one (086 and 174 appear only in their own files, the two StRS `derived_by` lists
(027, 021) and the scope index, as for the other scopes), and the archived pair has no replacement gap: SwRS-086 is
held by REVIEW-165 (active, same behaviour), SwRS-174 by TRUST-065 (active, lists the six types).

Earlier defects 1 to 21 are fixed against src/ and test/ (checked again in code): the stale-preview Known issue lives in
full in 181 (cause `sessionDocuments.ts:currentPreviewDocument`, reach list, paste exemption), 188, 195, 271 cite it,
109/140/144/148/150/168 point to it, 191 and 195 carry exact texts, 195's Method no longer claims the integration test,
175 and 183 Known issues match `bibScan.ts` (line 59) and the TRUST-065 drop, 159 lists both missing messages (code
lines 236 and 250), 044/241/268/262-267/025/026/029/038/177 are corrected. Handoffs: no behaviour is specified nowhere;
nothing of the palette-slash scope depended on the removed LIFE see-also lines (those lines concerned nonce, patch and
scroll report, which are not palette-slash behaviours).

New defects:

1. Frontmatter not updated after the body edits (heading = title and description = normative sentence broken). Scripted
   over the 271 active files, 11 differ:
   - title differs from the `##` heading: 191 (title still "...and for an unsaved or stale document"), 200 (title
     "...for an unsaved document and outside the workspace"), 176 (title "suspends the blur commit", heading "reports a
     dialog as open"), 104 (title "Focus moves between the editor and the link panel do not save, leaving the frame
     does", heading "Leaving the editor frame from the link panel or the text box saves once"), 034 (title "...popover
     and panels", heading "...popover").
   - description differs from the Normative behavior sentence: 191 (garbled second half), 195 ("a refusal", the SHALL gives
     the exact text), 200, 176, 104, 026 (lacks "checking this again on every scroll and resize"), 029 (lacks
     "re-evaluating on every scroll and resize"), 038 (lacks the reduced-motion clause), 171 (still the old
     two-branch sentence, the SHALL is now only the figure-form case), 183 (lacks "mark the list truncated when that
     cap is reached"), 034.
   Fix: for each of the 11 ids set `title` to the heading text and `description` to the Normative behavior sentence
   verbatim, then regenerate the indexes (176: choose one wording and use it in title, heading and index; 171: its
   title "Focus moves inside the editor frame keep the editor open and leaving it saves" no longer fits a SHALL that
   covers only the figure form leaving the frame: use "Leaving the editor frame from the figure form saves once").

2. SwRS-272 bundles two refusals in one SHALL ("... answer Save the document before pasting an image. or Pasting an
   image needs a Markdown file."), and its scenarios omit the third condition of the SHALL (the document is not the
   previewed one, `document.id !== preview.documentUri`). Fix: SHALL only the first reason (no file path or not the
   previewed document: "Save the document before pasting an image.") with scenarios Unsaved and Other document; move
   "a saved file that is not .md answers Pasting an image needs a Markdown file." to one more SwRS (derives_from
   StRS-018 and 021, derived_by updated), as 273 was split from 200.

3. SwRS-194 and SwRS-200, Verification notes, "untested": `test/integration/untrusted-suite.ts` (lines 114-140) sends
   previewPickImage and previewPasteImage to a read-only preview and asserts that no dialog opens and that the folder
   content is unchanged. Fix: 194 Method "the integration suite untrusted-suite.ts shows that a read-only preview
   opens no image dialog; the answered text is untested"; 200 Method "the same suite shows that a read-only preview
   writes no file; the answered text is untested" (replace "the read-only refusal has no test of its own"). Also
   TRUST-006 already cites that suite: keep it as the only test owner and have 200 cite it.

4. Scenarios "Stale revision" / "Stale preview" of 181, 188, 195, 271 (GIVEN "a document that changed outside the
   editor after the render, so the request names an older text"): the request names the render revision, which the
   gate (`previewManager.ts:matchesCurrent`) requires to equal the stage; the out-of-date answer only happens while the
   document has moved and no new render exists yet. Once the render has been replaced, the request is dropped without
   an answer (TRUST-065, Known issue of 175). Fix: GIVEN "a document whose text changed outside the editor and is not
   rendered yet", and add to 181's Criteria "after the render has been replaced the request is dropped by the gate
   instead (SwRS-MDOKFSTUDIO-TRUST-065)".

Not defects (checked): 038 reduced-motion clause matches StRS-024 and the reduced-motion test; the REL-style words
(above, below, same) are screen positions or in-scenario references, not cross-requirement relative references; no
implementation names in the StRS; 271-273 duplicate nothing in other scopes (TRUST-006 and TRUST-065 only mention the
message types); StRS `derived_by` lists keep the archived ids as in the other batch-4 scopes.
