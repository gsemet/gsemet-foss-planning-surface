# Audit: block-editing and table-editing (okfreq gardening, phases 4, 6, 6b, read-only)

Repository: markdown-okf-schema-studio, `main` at dedbdb2a. Method: `okfreq trace requirements --json`,
frontmatter inventory of every requirement, then each `@implements_req` and `@tests_req` site read with
its surrounding code or test. Paths are relative to the repository root. Nothing was changed.

Scope: 14 in-force StRS (StRS-BLOCK-026 is deprecated, ignored), 86 in-force SwRS of the two scopes, plus
9 SwRS of other scopes that these StRS derive (LIFE-169/170/173, TRUST-001/005/059/064/065, PALETTE-031):
those are cited where they matter here and left to their own scope's audit. `okfreq trace`: no
missing IDs, no non-leaf markers. Orphan SwRS: none. Phase 6: the four approved StRS (BLOCK-003,
BLOCK-025, TABLE-001, TABLE-012) carry `approved_by` and `approved_at`; every in-force SwRS is `proposed`.

IDs below drop the `MDOKFSTUDIO-` part (BLOCK-042 = SwRS-MDOKFSTUDIO-BLOCK-042). Severity: **H**
(wrong or misleading traceability, missing behaviour), **M** (split, merge or marker placement to fix),
**L** (wording).

## Summary

| StRS | Title (short) | #SwRS | Relevance | Split OK? | Markers OK? | Tests OK? | Validation test? | Diagram |
|---|---|---|---|---|---|---|---|---|
| BLOCK-001 | Switch edit mode, found as left | 7 | Real; good | No: 257, 258 misparented; 236 internal | Mostly | Mostly | Partial (Restricted Mode scenario only) | State |
| BLOCK-003 | Edit a block's raw Markdown in a frame | 11 | Real; core | No: 029 and 033 overlap; 002 a scenario | No: CSS header, stacked markers | Mostly | Yes (`previewEditing.test.ts`, oversized) | Sequence |
| BLOCK-006 | Typed text saved, never lost | 19 | Real; verbose | No: 033, 148, 169 misparented; overlaps BLOCK-025 | Mostly | Gaps | Registry only (H) | Sequence |
| BLOCK-008 | Text-editor keys, move between blocks | 5 | Real | Yes; 004 and 254 belong here | OK | OK | Partial (`editKeys` covers undo only) | State |
| BLOCK-011 | Add blocks, start an empty document | 4 | Real; good | Yes | OK | Gap (102 refusal) | Visual + registry | Sequence |
| BLOCK-014 | Reorder blocks | 13 | Real | Yes; 240 internal | Mostly | Gap (109 refusal) | Yes (`blockMove.test.ts`) | Sequence |
| BLOCK-016 | Select, copy, cut, paste blocks | 17 | Real | No: 001, 004, 254 misparented; 241-243 internal | OK | Gap (148) | Yes (`blockClipboard.test.ts`) | State |
| BLOCK-025 | Edits land exactly or are refused | 36 | Quality goal, not a use case; too broad | No: 10 protocol validators, many UI SwRS | Mostly | Oracle-only for 236-239 | Yes (integration) | Sequence |
| TABLE-001 | Edit a cell in place, never lose text | 10 | Real; too verbose | Mostly; 013 internal wording | Mostly | 013 mis-marked | Registry only (H) | Sequence |
| TABLE-002 | Move row or column by handle | 2 | Real; good | Yes | OK | Good | Visual only | Sequence |
| TABLE-006 | Keys in a cell | 1 | Real; thin | No: BLOCK-003, BLOCK-069 missing as children | OK | OK | Registry only (H) | State |
| TABLE-008 | Table bar: position, rows, columns | 8 | Real; stale text (H) | No: 003, 004, 005 are scenarios of 055; 118 misparented | No: buttons unmarked | OK | Visual + registry | Sequence |
| TABLE-011 | Convert forms; one-line diff | 8 | Two needs in one | No: 070/073/074/076/080 one behaviour; 102 a scenario | OK | Header markers | Registry only, unsupported (H) | Sequence |
| TABLE-012 | Format, insert, align, caption | 9 | Two needs in one | No: 120 misparented | OK | Header markers | Registry only, unsupported (H) | Sequence |

## Cross-cutting findings

- **X1 (H) `test/integration/realInput/markers.ts` is a marker registry, not a test.** Lines 4-65 list
  13 StRS and 26 SwRS of these scopes in one comment block ("Each marker names a requirement the
  real-window scenarios check"), detached from any scenario. For BLOCK-006, TABLE-001, TABLE-006,
  TABLE-011 and TABLE-012 it is the **only** StRS validation link. For TABLE-011 and TABLE-012 no
  real-input scenario exists: grep over `test/integration/realInput/` finds no table conversion, no
  Table or Column alignment action and no cell formatting (only the bar labels at
  `editorWidgets.ts:941`). Move each marker next to the scenario function that checks it and drop
  the ones that no scenario backs.
- **X2 (M) Markers in style-file headers.** `src/core/preview/styles/editModeStyles.ts:1-12` holds 12
  markers (BLOCK-014, 017, 029, 087, 109, 140, 254, 258, TABLE-006, 048, 064, DIAG-001) above one
  1,000-line CSS template; `contentBlockStyles.ts:6-19` the same (BLOCK-002 and 13 others, the `hr` rule
  is at line 490). Split the CSS into named constants per behaviour (for example `HR_HIT_AREA_CSS`)
  and mark each one, or record an explicit exemption in `project.guidelines.md`.
- **X3 (M) Stacked markers on hub functions.** `blockEditor.ts:224-228` `openBlockEditor` (BLOCK-014,
  029, 041, 102, TABLE-001); `blockEditor.ts:39-43` `closeBlockEdit` (BLOCK-148, 228, PALETTE-089,
  TABLE-064, 085); `editMode.ts:128-131` `openMappedEditor` (BLOCK-014, 041, TABLE-001, 018);
  `blockSourceEditor.ts:45-52` `receiveBlockEditSource` (BLOCK-029, 087, 216, TABLE-001, 034);
  `tableCellEditor.ts:263-265` `renderTableCellEditor`, about 340 lines (TABLE-001, 055, 091). Put each
  marker on the branch that does the behaviour (examples are given per StRS).
- **X4 (M) Large tests that carry many IDs.** `test/integration/previewEditing.test.ts:240-256`: one
  `run()` carries 17 markers (StRS-BLOCK-003, BLOCK-014, 053, 058, 094, 191, 216, FMSCHEMA, TOOLBAR,
  LIFE). `test/page/modules/editActions.test.ts:38-51` and `tableInsertAfterTable.test.ts:7-9` put the
  TABLE-073/074/076/106/111/115/117 markers in the file header, while the matching tests exist
  further down (`editActions.test.ts:757-825` htmlTable, `883-904` columnAlign, `1077` tableCaption,
  `1404-1438` list/pipe table). Move each marker onto its `test(...)`.
- **X5 (M) Protocol validators as SwRS (internals).** BLOCK-236 to 245 (10 SwRS) each specify the
  payload shape of one page message (`previewEditOpen needs an edit id and a line range`). No writer
  observes them. They all `depends_on` TRUST-052. Proposal: supersede the 10 with **one** SwRS ("The host
  ignores a malformed block-editing message and changes nothing"), with one table of messages and
  fields, derived from BLOCK-025, or fold them into TRUST-052 as scenarios. Tests: BLOCK-236 to 239
  share a single oracle test (`test/core/protocol/pageStateMessages.test.ts:220-229`, "accept exactly
  what the frozen validator accepted") that never states their refusal scenarios; BLOCK-240 to 245
  have one direct test each (`pageToHost.test.ts:173, 190-193, 281, 294`): adequate.
- **X6 (M) Shared rules spread through `derives_from` instead of `depends_on`.** BLOCK-041 (one edit at
  a time) is derived by 10 StRS, BLOCK-058 by 7, TRUST-065 by 12. The guideline says a shared rule is
  cited by `depends_on`. Keep one parent (BLOCK-025 for 058, BLOCK-003 for 041) and cite them by
  `depends_on` elsewhere. Otherwise each StRS lists 13-36 SwRS and stops reading on its own.

## StRS-BLOCK-001: A writer switches edit mode and finds it as left (proposed)

SwRS: BLOCK-001, 236, 257, 258, LIFE-169, LIFE-170, TRUST-001.

1. Relevance: a clear use case with good Main paths. (L) The normative text says "start that preview
   in edit mode" while Path 2 speaks of "view choices"; name edit mode in path 2.
2. Split: **(H)** BLOCK-257 (grid card widens with an editor) and BLOCK-258 (card title or option
   opens on its own line) derive **only** from BLOCK-001. They are about the block editor in a card:
   reparent to StRS-BLOCK-003. (M) BLOCK-236 is a protocol validator (X5). (M) BLOCK-258 joins two
   behaviours, the line mapping of card parts and the Enter/Tab keys of a one-line editor: split into
   "a card part opens on its own line" (BLOCK-003) and "a one-line editor commits on Enter"
   (BLOCK-008).
3. Markers: BLOCK-001 `src/page/features/editMode.ts:49` on `applyEditMode`: correct. BLOCK-258 has 10
   sites, including `src/core/security/html-sanitizer.ts:95` (allow-list of the single-line data
   attribute; acceptable) and `editModeStyles.ts:2` (X2).
4. Tests: BLOCK-001 nominal and tidy-up scenarios covered (`runtimePageControls.test.ts:197`,
   `blockReq.requirements.test.ts:95`, `runtimeBlockSelection.test.ts:160`). (M) "Edit mode on keeps
   the reading layout" and "Hover and click do not reflow": no test asserts that the layout does not
   move. `runtimeBlockEditor.test.ts:365` (hover marks the list) is a BLOCK-017 test that also
   carries the BLOCK-001 marker.
5. Validation: `test/integration/realWindowGaps.ts:668` (Restricted Mode, editable) checks the trust
   rule only. Missing: an integration step that turns edit mode on, closes and reopens the preview
   and finds edit mode on (LIFE-169/170).
6. Diagram: **state**. States: Reading, Editing (nothing open), Editing (editor open), Reopened.
   Transitions: Edit click (BLOCK-001), Edit click with an editor open (save, clear the selection),
   remember per workspace (LIFE-169), reopen restores (LIFE-170).

## StRS-BLOCK-003: A writer edits the raw Markdown of a block in a framed editor (approved)

SwRS: BLOCK-001, 002, 014, 017, 026, 029, 033, 041, 102, 127, 255.

1. Relevance: the core use case; clear. (L) The rationale has 7 bullets, 2 of them pointers to other
   scopes; trim them.
2. Split: (M) **BLOCK-029 and BLOCK-033 overlap**: both specify the status line with Done and Cancel
   (029: "lay out the status line with the Done and Cancel buttons beneath"; 033: "status line ...
   primary Done button beside a Cancel button"). Merge into one "framed editor" SwRS. (M) BLOCK-002
   (the hit area of a horizontal rule) is a boundary scenario of BLOCK-014 (what a click opens): merge.
   Missing from the path: BLOCK-255 (late open) is an option of state 2. (M) The approved StRS still
   needs the reparented BLOCK-257/258 (see BLOCK-001).
3. Markers: (M) BLOCK-033 is marked only on `blockEditHint` (`blockEditor.ts:511`); the frame inserted
   at once and the Done/Cancel buttons (`createEditorButtons`, `blockEditor.ts:523`, marked TABLE-006
   only) carry no BLOCK-033 marker. BLOCK-002 is at `contentBlockStyles.ts:6`, far from the `hr` rule
   at line 490 (X2). BLOCK-014, 029 and 102 stacked on `openBlockEditor` (X3). BLOCK-026
   (`editMode.ts:85`, `textEditing.ts:197`) and BLOCK-255 (`blockEditor.ts:316`,
   `textControls.ts:298`): correct.
4. Tests: BLOCK-014 well covered (link, alert, reading-mode cases in `linkEditModeClick.test.ts`,
   `alertBlockEditOpen.test.ts`). (M) BLOCK-014 "An error or a malformed previewEditSource": not found
   among its tests (it is under BLOCK-216, `blockReq.requirements.test.ts:453`). BLOCK-026 "Link
   label": only the parametrised `textEditing.test.ts:135`; acceptable. BLOCK-029 "Cell that cannot
   be parsed" and "grows with its text": not asserted in its 2 unit tests (visual only,
   `scenarioDefinitions1.ts:842`).
5. Validation: `test/integration/previewEditing.test.ts:244` and `test/visual/scenarioDefinitions1.ts:1216`.
   Valid, but inside the 17-marker `run()` (X4).
6. Diagram: **sequence**. Participants: Writer, Page, Host, Document. Messages: click on a block
   (BLOCK-014), the frame appears at once and the outline goes (BLOCK-033), previewEditOpen, the host
   checks the range and the include (BLOCK-127, BLOCK-256), previewEditSource, text box with the caret
   at the clicked word (BLOCK-026), Done or Cancel.

## StRS-BLOCK-006: Typed text is saved, survives updates and is never lost on leaving (proposed)

SwRS: BLOCK-033, 041, 042, 047, 053, 058, 148, 169, 191, 193, 205, 216, 228, 244, 245, 256, TRUST-005,
TRUST-064, TRUST-065.

1. Relevance: real and important. (L) Too verbose: `user_need` is about 110 words and covers five
   needs (autosave, stability while typing, keep or drop, leave safely, keep the place). (M) It
   overlaps StRS-BLOCK-025: both derive 042, 053, 058, 191, 205, 216, 244, 245. Proposal: BLOCK-006
   keeps "never lose typed text" (042, 047, 053, 193, 205, 216); BLOCK-025 keeps "the file is changed
   exactly or not at all".
2. Split: (H) BLOCK-148 (a block selection survives saves), BLOCK-169 (cut) and BLOCK-033 (status
   line) do not serve this need: drop BLOCK-006 from their `derives_from`. BLOCK-244 and 245 are
   validators (X5). BLOCK-191 (the host edit lock) describes internals; rewrite it as observable ("a
   change inside the open block ends the edit with an error and keeps the text").
3. Markers: BLOCK-042 (`src/core/mapping/textDiff.ts:15`, `blockEditor.ts:387` `autosaveBlockEdit`),
   BLOCK-047 (`blockEditor.ts:336/436`, `blockSourceEditor.ts:163` blur), BLOCK-053 (`blockEditor.ts:502`,
   `blockEdits.ts:479`) and BLOCK-205 (`flushWait.ts:7`, `hostHandlers.ts:69`, `history.ts:79`,
   `links.ts:216`): correct. (L) BLOCK-205 at `src/session/features/blockEdits.ts:120`
   (`postEditSourceError`, a generic error reply) is loosely tied; the "save refused during a flush
   warns" branch is the place.
4. Tests: (M) **BLOCK-148 has one test** (`runtimeBlockSelection.test.ts:161`). The tests that check
   its "named by position" and "dropped without its patch" scenarios exist without the marker:
   `runtimeBlockSelection.test.ts:194`, `:209`, `:220`. Add BLOCK-148 to them. BLOCK-042 "One save
   applied at a time": `session/blockReq.requirements.test.ts:281`, good. BLOCK-053 "Escape during an
   IME composition": no test found. BLOCK-047, 193 and 205: thorough.
5. Validation: **registry only** (X1, H). The real scenarios exist:
   `test/integration/realInput/flushBeforeNavigate.ts:235` (`scenarioFlushBeforeLink`), `:254` (Back),
   `:275` (tab switch). Put the StRS marker there.
6. Diagram: **sequence**. Participants: Writer, Page, Host, Document. Messages: typing, then
   previewEditSave final=false 400 ms later (BLOCK-042), a render waits (BLOCK-193), Done gives the final
   save (BLOCK-047) or Escape gives previewEditCancel (BLOCK-053), link or Back gives
   previewFlushEdit and then save before navigate (BLOCK-205), one render (BLOCK-058).

## StRS-BLOCK-008: A writer types and moves between blocks with text editor keys (proposed)

SwRS: BLOCK-003, 061, 069, 079, LIFE-173.

1. Relevance: real; clear.
2. Split: good. (M) Behaviours of this use case live under other StRS: BLOCK-004 (Up and Down select,
   Enter opens, Escape returns to the selection) and BLOCK-254 (Right and Left walk the structure)
   derive only from BLOCK-016 (copy and paste). Reparent them here, or create a "keyboard walk through
   the document" StRS. (L) BLOCK-069 is wide (10 scenarios: wrapping, Home/End, select-all, undo,
   alt-text Enter, key isolation); acceptable, but its title is truncated ("... stay in the").
3. Markers: BLOCK-061 (`textEditing.ts:13/84`), BLOCK-069 (`textControls.ts:202`, `editorKeys.ts:9`,
   `selectAllKey.ts:11`) and BLOCK-079 (`textControls.ts:33`): correct. BLOCK-003 is spread over 10
   sites from host to page; each one is a real link in the command path: OK.
4. Tests: good overall. BLOCK-079 "remembered in the webview state" and "Page replaced before the save
   is rendered": no test found among its 4 tests.
5. Validation: `test/integration/editKeys.test.ts:38` covers undo/redo/select-all/delete-line only.
   Missing: list continuation and arrow-at-edge in a real window (`realInput/blockKeys.ts` probably
   does it: put the StRS marker on that scenario).
6. Diagram: **state**. States: Editor open mid-text, Caret at the first or last line, Next block
   editor open, Selection made. Transitions: Enter continues the list (061), marker key wraps (069),
   ArrowDown at the edge saves and opens the next block (079), a modifier keeps the key native (refusal).

## StRS-BLOCK-011: A writer adds blocks and starts an empty document from the preview (proposed)

SwRS: BLOCK-087, 094, 102, 253.

1. Relevance: real; well sized; good Main paths.
2. Split: OK. (L) BLOCK-102 (click or Enter on Start writing) and BLOCK-253 (Start writing is the
   keyboard selection; Enter or ArrowDown) overlap on Enter. Keep 102 for the button and 253 for the
   keyboard selection, and remove the Enter scenario from one of them.
3. Markers: BLOCK-087 (`insertPoints.ts:96`), BLOCK-094 (`src/core/mapping/insertion.ts:12`
   `planInsertion`) and BLOCK-253 (`insertPoints.ts:199`): correct. (L) BLOCK-094 is also on
   `blockEdits.ts:160` `handleEditOpen`, which only routes an insertion open; the write happens on
   save. BLOCK-102 is stacked on `openBlockEditor` (X3).
4. Tests: (M) BLOCK-102 "No Start writing button on a failed or pending render" is checked by
   `runtimeBlockMoves.test.ts:374` ("a failed render offers no Start writing point"), which has no
   marker. BLOCK-094: line endings and refusal of a whitespace-only text are covered
   (`insertion.test.ts`).
5. Validation: `test/visual/scenarioDefinitions1.ts:1257` plus the registry. `realInput/renderPatching.ts`
   exercises Start writing and could carry the StRS marker.
6. Diagram: **sequence**. Participants: Writer, Page, Host, Document. Messages: hover shows the plus
   (087), click opens an empty insertion editor, typing then Done, previewEditSave with
   insertAfterLine, the host writes the block with one blank line on each side (094), render. Variant:
   empty body, Start writing (102/253).

## StRS-BLOCK-014: A writer reorders blocks with arrows, keys and selections (proposed)

SwRS: BLOCK-041, 058, 109, 117, 124, 127, 129, 130, 156, 240, TRUST-005, TRUST-065.

1. Relevance: real. (L) The rationale states the chord "Cmd+Alt on macOS and Ctrl+Alt elsewhere"
   (formerly the deprecated BLOCK-139); BLOCK-130 now carries it: fine.
2. Split: good. BLOCK-129 (the page applies a move result only for its own render) is internal; fold
   it into BLOCK-109 as a boundary scenario. BLOCK-240 is a validator (X5).
3. Markers: BLOCK-117 (`sourceEdits.ts:193` `planBlockMoveEdit`, `blockMove.ts:47`), BLOCK-130
   (`blockMoves.ts:387`, `blockEditor.ts:173`) and BLOCK-156 (`blockMoves.ts:218`): correct. (L)
   BLOCK-109 at `blockSelectionView.ts:71` and `editMode.ts:252` (pointer tracking for "actions show on
   one block"): acceptable.
4. Tests: (M) BLOCK-109 "A refused move says why next to the bar for six seconds" is checked by
   `runtimeBlockMoves.test.ts:131`, which carries BLOCK-129 and TRUST-059 but not BLOCK-109.
   BLOCK-117 and 156: good (`blockMove.test.ts` core and integration).
5. Validation: `test/integration/blockMove.test.ts:37` (one swap, one undo, refusals): good.
6. Diagram: **sequence**. Participants: Writer, Page, Host, Document. Messages: arrow click or
   Alt+ArrowDown (109/130), previewBlockMove (both ranges), the host checks the ranges and the include
   (124/127), swaps one span keeping the separator (117), one undo stop and one render (058),
   previewBlockMoveResult, the page refocuses the moved block (130/156).

## StRS-BLOCK-016: A writer selects blocks and copies, cuts and pastes them as Markdown (proposed)

SwRS: BLOCK-001, 004, 041, 058, 124, 127, 140, 148, 166, 169, 174, 241, 242, 243, 254, TRUST-005,
TRUST-065.

1. Relevance: real; good.
2. Split: (H) BLOCK-001 (the Edit button), BLOCK-004 and BLOCK-254 (keyboard navigation) are not
   copy/cut/paste: reparent them (see BLOCK-008). BLOCK-241 to 243 are validators (X5). Missing: no SwRS
   names "the clipboard keys stay native in a text box, a field, the properties table and in reading
   mode"; it is a scenario of BLOCK-166 ("The keys stay with the browser"): OK.
3. Markers: BLOCK-166, 169 and 174 are each marked on the model (`blockRange.ts:77/91/149`), the page
   (`blockSelectionView.ts:392/305/393`) and the host (`sourceEdits.ts:407/465`): good. BLOCK-127 is
   at 5 correct sites. BLOCK-140 is at `blockSelectionView.ts:127`: good.
4. Tests: (M) BLOCK-174 "Empty clipboard": only inside `previewEditing.test.ts:1410` (the large
   `run()`), with no BLOCK-174 marker near it. BLOCK-166 "A held key sends one request until the host
   answers": not found. BLOCK-140 "Shift+mousedown does not extend the text selection": not found
   among its 3 tests.
5. Validation: `test/integration/blockClipboard.test.ts:83` (host messages) and
   `test/visual/scenarioDefinitions2.ts:1107`. The real keys (Shift+click, Ctrl+C) are not exercised
   in a real window for this StRS; `realInput/blockKeys.ts` could carry it.
6. Diagram: **state**. States: No selection, Run selected, Markdown on the clipboard, Blocks pasted.
   Transitions: Shift+click or Shift+Arrow (140), the selection stops at an include (127), Ctrl+C (166),
   Ctrl+X removes with one separator (169), Ctrl+V (174), patch, Escape or plain click clears (148/140).

## StRS-BLOCK-025: Preview edits land exactly, in one undo step, keep line endings, or are refused (approved)

SwRS (36): BLOCK-003, 041, 042, 053, 058, 069, 094, 109, 117, 124, 127, 129, 130, 156, 166, 169, 174,
191, 205, 216, 234, 236-245, TRUST-005/059/064/065.

1. Relevance: a cross-cutting quality goal, not a use case a writer runs; useful as the "safety
   contract". (H) **Stale known issue**: "a multi-line block of a CRLF document may have its second save
   refused (see BLOCK-234)". BLOCK-234 and its test `test/session/blockReq.requirements.test.ts:492`
   ("... the next save is not refused", LF, CRLF and CR) show it fixed. Remove it (approved: owner
   agreement needed).
2. Split: (M) Too broad: 36 children, including UI behaviours (003 VS Code keys, 069 marker keys, 109
   arrows, 130 Alt+Arrow) that have nothing to do with landing exactly. Keep the host-side children:
   058, 094, 117, 124, 127, 169, 174, 216, 234, 256, plus one merged validator SwRS (X5). Drop the
   rest from `derives_from`.
3. Markers: BLOCK-234 (`withLineEndingOf` at `sourceEdits.ts:281`, `sourceLines` at `textEdit.ts:61`,
   `markdownTable.ts:268` `serialize`) and BLOCK-058 (`sourceEdits.ts:65` `apply`, `blockEdits.ts:318`):
   correct. BLOCK-058 is also at `src/session/features/frontmatter.ts:335` (shared rule: fine).
4. Tests: BLOCK-058 "Cancelled session" and "No visible text editor": not found among the unit tests;
   integration tests check undo. BLOCK-124: every refusal case checked (`blockMove.test.ts:85`,
   `blockRange.test.ts:26`). BLOCK-234: good.
5. Validation: `test/integration/blockClipboard.test.ts:82` and `blockMove.test.ts:36`: real and
   appropriate.
6. Diagram: **sequence** (refusal-focused). Participants: Page, Host, Document. Messages: edit, move
   or clipboard request with revision and ranges, range or revision check (124/256) with a refusal
   reason, include check (127), plan one edit with the line endings kept (234), apply as one undo stop
   (058), render once, or "VS Code could not apply" answered (058).

## StRS-TABLE-001: A writer edits a table cell in place and never loses the text (approved)

SwRS: BLOCK-205, BLOCK-228, TABLE-001, 006, 013, 018, 025, 034, 119, 121.

1. Relevance: real and central. (M) **Too verbose**: 18 rationale bullets, about 8 of them only
   restating that something "belongs to the block-editing scope" (SwRS-BLOCK-053, 205, GFM-001,
   LAYOUT-032). Cut them to the constraints a writer sees. Overlaps BLOCK-006 by design (the cell
   version of the same need): fine, with the dependencies stated.
2. Split: good. (L) TABLE-013 is worded as internals ("remember each change in the table model"):
   reword it as observable ("moving to another cell keeps every change; the whole session is one undo
   step"). (L) TABLE-006 combines cell font/wrap and the minimum widths in edit mode (9 scenarios):
   acceptable.
3. Markers: TABLE-025 (`tableCellEditor.ts:102` `cancelTableCellEdit`, `:569` keydown), TABLE-119
   (`editLock.ts:62/73`, `hostEvents.ts:287`, `blockEdits.ts:523`) and TABLE-121
   (`tableInContainer.ts:86`): correct. TABLE-001 at `markdownTable.ts:227` (`parse`) and `:275`
   (`serializePipe`): serialisation is TABLE-094's, not TABLE-001's. (M) TABLE-034 is marked only on
   the dispatcher `blockSourceEditor.ts:52`; the code that keeps the text and drops the navigation is
   unmarked.
4. Tests: (H) **TABLE-013 is mis-marked**: its only test, `runtimeTableCellEditor.test.ts:19`, is the
   row/column toolbar test. The test that checks it, `:636` ("switches cells without losing changes
   and finalizes before leaving the table"), carries only TABLE-034. Add TABLE-013 to `:636`; keep
   TABLE-034 there only for its refused-save part (`:712`). TABLE-018 "A pointer press in the last 500
   ms": not found. TABLE-025: exhaustive (`runtimeTableCellEscape.test.ts`,
   `runtimeTableCellTabRow.test.ts`).
5. Validation: **registry only** (X1, H). Real scenarios exist: `realInput/editorWidgets.ts:549-576`
   (type in a cell, Enter commits), `flushBeforeNavigate.ts:298` (`scenarioFlushCellAndFrontmatter`),
   `realInput/tableEscape.ts`. Put the StRS marker on them.
6. Diagram: **sequence**. Participants: Writer, Cell editor, Page, Host, Document. Messages: click on a
   cell (TABLE-001), previewEditOpen, table source, raw cell text, typing with the whole table
   autosaved (013), Tab to the next cell in the same session (013/035), Enter or click away gives the
   final save (018) or Escape drops the cell (025), a host refusal shows in the bar (034).

## StRS-TABLE-002: A table row or column moves by its handle in edit mode (proposed)

SwRS: TABLE-002, TABLE-007.

1. Relevance: real; clear; good Main paths. (L) It overlaps BLOCK-014 only by the Alt+Arrow chord:
   fine.
2. Split: good (row versus column).
3. Markers: each one is on `movableRows`/`movableColumns`, `moveInCellEditor`, `receiveSource`,
   `zoneTarget` and `reposition` in `tableRowMove.ts`, and on the models (`markdownTable.ts:372/392`,
   `listTableMove.ts:104/156`): correct. (L) Both are also on `serializePipe` (`markdownTable.ts:276-277`).
4. Tests: thorough (`runtimeTableRowMove.test.ts`, `listTableRowMove.test.ts`, `tableColumnMove.test.ts`,
   integration `tableMoves.ts`), including the refusal and the one-undo scenarios.
5. Validation: visual only (`scenarioDefinitions2.ts:1388-1475`). `test/integration/tableMoves.ts:255`
   and `:299` (real drag, one edit) could carry StRS-TABLE-002.
6. Diagram: **sequence**. Participants: Writer, Handle, Page, Host, Document. Messages: drag the handle
   or Alt+Arrow, drop zone marker, request the table source, move the row or column in the model,
   final save (one edit), render, handles repositioned.

## StRS-TABLE-006: Tab, arrows and editing keys work in a table cell (proposed)

SwRS: TABLE-035 (deprecated children: TABLE-044 to 047).

1. Relevance: real but **thin**: one SwRS. (M) Its own rationale delegates undo, select-all, wrapping
   and key isolation to BLOCK-069; BLOCK-003 covers undo/redo in "a block or table-cell text box".
   Neither derives from TABLE-006. Add TABLE-006 to their `derives_from`, or merge this StRS into
   BLOCK-008 ("text editor keys in block and cell editors").
2. Split: (M) **TABLE-035 is too wide**: 13 scenarios and 4 behaviours. Proposal: split into (a) Tab
   and the arrows move between cells, (b) Tab in the last cell adds a row and shows the hint
   (`tableTabRow.ts`), (c) the cell left shows its typed text rendered (`tableCellEditor.ts:75`,
   `cellInlineMarkdown`), (d) the cell is revealed in the table's scroll box (`revealCellInTable`).
3. Markers: 9 sites, each on its branch: correct.
4. Tests: good (`runtimeTableCellEditor.test.ts:725-863, 1446-1486`, `runtimeTableCellTabRow.test.ts`).
   "Final save cannot be posted" (refusal): not found.
5. Validation: **registry only** (X1, H). `realInput/editorWidgets.ts:790` ("RI-T17: Tab moves between
   table cells, adds a row on the last cell") is the right place for the StRS marker.
6. Diagram: **state**. States: Cell (r,c) open, Last cell open with the hint, New row open, Neighbour
   block editor open. Transitions: Tab or Shift+Tab, an arrow at the text edge, Tab in the last cell
   adds a row, an arrow with no cell in that direction goes to the neighbour block, a modifier keeps
   the key native.

## StRS-TABLE-008: A table bar locates the writer and edits rows and columns (proposed)

SwRS: TABLE-001, 003, 004, 005, 048, 055, 064, 118.

1. Relevance: real. (H) **Stale and contradictory text.** It says "five labelled buttons (Row +, Row −,
   Col +, Col −, List table)"; TABLE-048 specifies seven and `realInput/editorWidgets.ts:941` asserts
   "Row above", "Row below", "Row −", "Col left", "Col right", "Col −", "List table". It says twice ("a
   column operation rewrites the whole table in one fixed style, so the table's own padding and
   indentation are lost"; one of the two is a Known issue) the opposite of TABLE-055, StRS-TABLE-011
   and the test `markdownTable.test.ts:372` ("a column operation keeps the padding, indentation and
   outer pipes of every line").
2. Split: (M) **TABLE-003 (Row above), TABLE-004 (Col left) and TABLE-005 (buttons on a list-table) are
   scenarios of TABLE-055**, which already cites 003 and 004 in its own text. Merge: 003, 004, 005 and 055
   become one SwRS "row and column buttons", with 005 as a boundary scenario. (L) TABLE-118 (late open
   keeps the find focus) is not about the bar: reparent it to TABLE-001 and merge it with BLOCK-255
   (the same rule for block editors).
3. Markers: (M) TABLE-055 is marked on `renderTableCellEditor` (`tableCellEditor.ts:264`) and
   `markdownTable.ts:356`. The buttons themselves (`tableCellEditor.ts:405-422`, the `addAction` calls
   for Row above to Col −) carry no marker; TABLE-003/004 are marked only on the model
   (`tableStructure.ts:18/33`). Put TABLE-055 (and 003/004 until merged) on lines 405-422. TABLE-048
   (`tableCellEditor.ts:323`) and TABLE-064 (`tableCellEditor.ts:214/239`, `editorChrome.ts:71`): correct.
4. Tests: TABLE-055 good (`runtimeTableCellEditor.test.ts:164-243`). TABLE-004 "Style kept": checked
   only under TABLE-055 (`:243`). TABLE-118: 2 tests, fine. TABLE-064: good.
5. Validation: `test/visual/scenarioDefinitions1.ts:948` (visual) and the registry.
   `realInput/editorWidgets.ts:941` (the bar labels in a real window) could carry it; no real-window
   step presses a row or column button.
6. Diagram: **sequence**. Participants: Writer, Table bar, Cell editor, Page, Host. Messages: a cell
   opens and the bar is created above the table with its position (048), scrolling keeps the bar under
   the sticky band (064), Row below with the typed text stored (055), final save, render, the editor
   reopens on the new row.

## StRS-TABLE-011: A table converts between forms and a cell edit is a one-line change (proposed)

SwRS: BLOCK-234, TABLE-070, 073, 074, 076, 080, 094, 102.

1. Relevance: real, but **two use cases under one title** (convert a table without loss; a cell edit
   is a minimal diff). (M) Split into "a writer converts a table between forms" and "a table edit
   changes only the lines it touches". The second could join StRS-BLOCK-025 (edits land exactly).
2. Split: (M) **TABLE-070, 073, 074, 076 and 080 are one behaviour**, the conversion of a table between
   forms. The bar button (070) and the palette and slash actions (073 for the list-table direction,
   074 for the pipe direction) are entry points: per the guideline, buttons are scenarios. The refusal
   (076) and the fidelity rule (080) are its refusal and boundary scenarios. Proposal: 070, 073, 074,
   076 and 080 become one SwRS "a table converts between pipe, list-table and HTML forms without loss,
   or is refused with a reason". (L) TABLE-102 (how a row is split into cells) is a boundary scenario
   of TABLE-094: merge.
3. Markers: TABLE-073/074 both on `convertTableAtCaret` (`tableEditActions.ts:162-163`), 076
   (`tableConversion.ts:57/82`), 080 (`tableConversion.ts:268` `gridToListTable` only, while 080 also
   covers HTML and list-table to pipe) and 094 (`markdownTable.ts:267` `serialize`): mostly correct.
   (L) Add 080 on the pipe and HTML writers.
4. Tests: (M) TABLE-073/074/076 markers sit in the file header of `editActions.test.ts:45-47` (X4).
   TABLE-080 has 2 tests (`listTable.test.ts:28`, integration `tableMoves.ts:193`); "Escaped pipes",
   "Canonical round trip" and "List-table read in every fence style" are not visibly asserted under
   its marker. TABLE-094: strong (`markdownTablePreservation.test.ts` corpus). TABLE-102: 2 of its 6
   scenarios have a test.
5. Validation: **registry only, unsupported** (X1, H): no real-input scenario converts a table.
   `test/integration/tableMoves.ts:191-193` (List table in a real preview, TABLE-070/080) could carry
   StRS-TABLE-011.
6. Diagram: **sequence**. Participants: Writer, Palette or Table bar, Page, Converter, Host. Messages:
   List table or Pipe table at the caret, parse into a grid, refusal "Nothing was changed." when
   content would be lost (076), write the target form with cells, escapes and alignment kept (080),
   one edit (073/074), render.

## StRS-TABLE-012: Tables and cell text are formatted, inserted, aligned and captioned (approved)

SwRS: PALETTE-031, TABLE-018, 085, 091, 106, 111, 115, 117, 120.

1. Relevance: real, but (L) **two use cases**: formatting the text of a cell (085, 091) and inserting
   or shaping a table from the palette (106, 111, 115, 117). Consider two StRS; the second one overlaps
   TABLE-011 on HTML table (117 converts).
2. Split: (M) TABLE-120 (a spreadsheet paste fills cells) is neither formatting nor insertion:
   reparent it to TABLE-001 or TABLE-008. TABLE-117 joins convert-to-HTML and insert-HTML: its convert
   half belongs with the conversion SwRS (see TABLE-011). TABLE-018 (commit) and PALETTE-031 (popovers)
   are context only.
3. Markers: TABLE-085 (`tableCellEditor.ts:460`, `textControls.ts:223`), TABLE-106/111
   (`paletteActions.ts:350/469`, `tableEditActions.ts:25/187`), TABLE-115 (`tableEditActions.ts:233`),
   TABLE-117 (`markdownTable.ts:428`, `tableEditActions.ts:86`) and TABLE-120 (`tableGridPaste.ts`,
   paste listener `tableCellEditor.ts:312`): correct. (M) TABLE-091 on `renderTableCellEditor`
   (`tableCellEditor.ts:265`, a 340-line function) is vague; `escapeCellPipes` (`markdownTable.ts:114`)
   and `cellSafeEdit` (`textEditing.ts:278`) are the right sites, and both are marked. Drop the first.
4. Tests: (M) the TABLE-106/111/115/117 markers sit in file headers (`editActions.test.ts:48-51`,
   `tableInsertAfterTable.test.ts:7-9`), detached from the tests that exist (X4). TABLE-106 "Size
   limits" and "Missing, malformed or out-of-range size": not asserted under a marker. (L)
   `slashMenu.test.ts:247` (cell palette contents) is marked TABLE-106; it checks TABLE-085. TABLE-120:
   good.
5. Validation: **registry only, unsupported** (X1, H). No integration or real-input test inserts a
   table, aligns a column or formats a cell. Missing: one real-input scenario (slash menu, then Table
   3x2, then Column alignment, then bold in a cell, then Enter, then the buffer is checked).
6. Diagram: **sequence**. Participants: Writer, Palette or Slash menu, Cell group, Text box, Host.
   Messages: Table 3x2 inserts a pipe table after the selection (106), Column alignment rewrites one
   delimiter cell (111), Table with caption wraps it (115), in a cell Cmd+B formats the cell text
   (085), a pipe is escaped (091), Enter commits (018).

## Orphan SwRS

None. Every in-force SwRS of block-editing and table-editing derives from at least one in-force StRS.
Deprecated children still linked to in-force StRS (normal history, no action): BLOCK-012 (to
BLOCK-001); BLOCK-021, 023 (to BLOCK-003); BLOCK-077 (to BLOCK-008); BLOCK-139 (to BLOCK-014);
BLOCK-227, 232, 233, 235, 252 (to BLOCK-025); TABLE-026, 027, 030 (to TABLE-001); TABLE-044 to 047 (to
TABLE-006). No in-force StRS text cites a deprecated SwRS. No source or test marker cites one.

## Counts by category

| Category | H | M | L | Examples |
|---|---|---|---|---|
| Wrong or weak parent (`derives_from`) | 3 | 6 | 1 | BLOCK-257/258 under BLOCK-001; BLOCK-001/004/254 under BLOCK-016; BLOCK-033/148/169 under BLOCK-006; TABLE-120, 118; BLOCK-003/069 missing TABLE-006 |
| Stale or contradictory StRS text | 2 | 0 | 2 | TABLE-008 (five buttons; column style lost), BLOCK-025 (fixed CRLF known issue) |
| SwRS that are scenarios of one behaviour (merge) | 0 | 5 | 2 | TABLE-003/004/005 into 055; TABLE-070/073/074/076/080; BLOCK-029 and 033; BLOCK-002 into 014; TABLE-102 into 094; TABLE-118 into BLOCK-255 |
| SwRS too wide (split) | 0 | 2 | 1 | TABLE-035 (4 behaviours), BLOCK-258 (2 behaviours), BLOCK-069 |
| SwRS describing internals | 0 | 2 | 2 | BLOCK-236 to 245 (10 validators), BLOCK-191, BLOCK-129, TABLE-013 |
| StRS too broad, thin or doubled | 0 | 4 | 3 | BLOCK-025 (36 children), TABLE-006 (1), TABLE-011 and TABLE-012 (two needs each), BLOCK-006 (verbose), TABLE-001 (18 bullets) |
| Implementation marker placement | 0 | 7 | 4 | CSS headers (X2); hub functions (X3); TABLE-055 buttons unmarked; BLOCK-033 frame unmarked; TABLE-034 dispatcher only; TABLE-091 vague |
| Test markers missing or misattributed | 1 | 5 | 1 | TABLE-013 on the wrong test; BLOCK-148, BLOCK-102, BLOCK-109 tests without marker; header markers (X4); 17-ID `run()` |
| Scenarios with no test found | 0 | 9 | 0 | BLOCK-001 layout; BLOCK-053 IME; BLOCK-079 state; BLOCK-140 mousedown; BLOCK-166 held key; BLOCK-174 empty clipboard; TABLE-018 500 ms; TABLE-035 refusal; TABLE-106 size refusal |
| StRS validation | 5 | 4 | 0 | Registry only: BLOCK-006, TABLE-001, TABLE-006; registry and unsupported: TABLE-011, TABLE-012; partial: BLOCK-001, BLOCK-008, BLOCK-016, TABLE-002 |
| **Total** | **11** | **44** | **16** | |

Phase 6b in numbers: 10 validator SwRS can merge into 1; TABLE-003/004/005/055 into 1;
TABLE-070/073/074/076/080 into 1; BLOCK-029/033 into 1; BLOCK-002 and TABLE-102 become scenarios;
TABLE-118 goes into BLOCK-255. That is 24 SwRS becoming 7 (86 in force would go to about 69), against
2 splits (TABLE-035 into 4, BLOCK-258 into 2), which add 4. Each restructure needs the owner's approval
(supersede, never delete).
