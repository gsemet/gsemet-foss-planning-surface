Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Critic review: frontmatter-editing StRS and SwRS (P10.3)

Scope `frontmatter-editing` (FMEDIT): 11 StRS, 71 SwRS in `markdown-okf-schema-studio-wt-059`,
reviewed against `src/`, `test/`, `inventory/frontmatter-editing.md` and the batch 1 defect lists.

Verdict: REVISE

## Mechanical checks (scripted)

- First `##` heading equals the frontmatter title in all 82 files; no glued headings (`.+###` scan
  clean); description equals the "Normative behavior" text in all 82; exactly one SHALL in every
  normative sentence; every SwRS has two scenarios; no placeholders; every `derives_from` target
  exists and `derived_by` back-links are consistent (checked for all 11 StRS).
- Inventory: all 35 F-FMEDIT rows have at least one SwRS in the last column; no unmapped row. No
  skipped row.

## Spot check against code and tests (about 50 of 71 SwRS)

Read in `src/page/features/frontmatter{ValueEditor,Editor,Menu,ListEditor}.ts`, `pageInput.ts`,
`editMode.ts`, `hostHandlers.ts`, `contentPatch.ts`, `checkboxes.ts`, `scrollCore.ts`,
`src/core/edits/frontmatterEdit.ts`, `frontmatterSerialize.ts` (placement), `pageToHost.ts`
(validators), `session/pageMessages.ts`, `session/features/frontmatter.ts`, `flushWait.ts`.
Confirmed true: 001, 003, 004-009, 013, 016-017, 019-027, 029-043, 047-054, 056, 058-064, 067-069,
071 and the Known issues of 007, 009, 010, 021, 023, 034, 037, 047, 050, 061. The four items the
analyst flagged:

- F-003 enum commit: SwRS-003 is right (no `change` listener on the select; save on blur or Enter,
  test uses `select.dispatch("blur")`). The inventory row ("picking a value saves it at once") is
  wrong, see D14.
- F-024: SwRS-050 is right (only `step = "any"` is set; no min, max or pattern anywhere).
- F-029 pin: code pins the whole properties section at source line 1
  (`frontmatterPinFields` returns `pinFields(1, properties)`), not "the edited row". SwRS-057 body
  is right, its title and StRS-004 are not, see D2.
- F-002 guard: `openFrontmatterValueEditor`, `openFrontmatterKeyEditor`, `blockMoves`,
  `blockSelectionView` and `insertPoints` check `activeFrontmatterEdit`, but `openBlockEditor` only
  checks `activeBlockEdit` and `editMode.openMappedEditor` has no frontmatter guard. A block
  editor can therefore open while a field editor is open. See D1.

## Defects (blocking)

1. **SwRS-MDOKFSTUDIO-FMEDIT-002 is false in its title and bundled.** Title "Other editors and block
   operations ignore input while a field editor is open": block editors do not (see F-002 above).
   The SHALL lists four independent inputs (open another field editor, extend a block selection,
   move a block, open the figure editor); the boundary scenario tests the reverse direction (a block
   editor gating field editors), which the SHALL does not state; the "+" insert points and block
   copy/cut of the inventory row are not stated either. Fix: retitle to "Block selection, block
   moves and other field editors ignore input while a field editor is open"; split into (a) no
   second field editor opens while any editor is open (both directions, using the boundary), (b)
   block selection and block moves ignore input, (c) the figure editor and "+" insert points; add a
   Known issue "a block editor still opens while a field editor is open" (or the verified
   behaviour) to (a)/(b). Same correction in StRS-011: "block operations" is too broad, say "block
   selection and block moves", and StRS-001 rationale line "a field editor does not open while a
   block editor is open" stays (that direction is true).
2. **SwRS-057 title and StRS-004 say "the edited row" keeps its place; the code pins the properties
   section.** Retitle to "The properties section keeps its place across the save" and reword
   StRS-004 normative text and description ("keep the edited row in place") to "keep the properties
   table in place". Add to the boundary that pinLine is always 1.
3. **SwRS-MDOKFSTUDIO-FMEDIT-004 bundles** Enter-saves, Shift+Enter-adds-a-line and the multi-line
   rule (Enter adds a line, Cmd/Ctrl+Enter saves) in one SHALL plus a three-way boundary. Fix:
   004 = Enter saves a one-line value (boundary: Enter during IME composition is ignored); new SwRS
   = Shift+Enter (or Alt+Enter) adds a line without saving; new SwRS = in a multi-line value Enter
   adds a line and Cmd/Ctrl+Enter saves. Use `okfreq new`, derive from StRS-002.
4. **SwRS-MDOKFSTUDIO-FMEDIT-011 bundles three keys** (Enter inserts, Backspace removes an empty
   item, Cmd/Ctrl+Enter saves) "respectively". Split into three SwRS (the empty-last-item Enter
   removal stays a boundary of the Enter one), keep the IME/Shift/Alt boundary on each.
5. **SwRS-MDOKFSTUDIO-FMEDIT-022 bundles** disabling the controls, the "Saving frontmatter..."
   status and the "Saved. Refreshing preview..." status. Split: (a) in flight, controls disabled
   and "Saving frontmatter…" shown (boundary: key / add / remove texts), (b) accepted result shows
   "Saved. Refreshing preview…".
6. **SwRS-MDOKFSTUDIO-FMEDIT-052 is vague and bundled.** "an explicit message" is not testable
   and two refusals with two different messages are joined: an older render ("The preview changed
   while this field was being edited. Reopen the field.", from `reportStaleEdit`) and a missing
   document, revision or field (the stale-field message). Split into two SwRS and quote the
   message in each SHALL.
7. **SwRS-MDOKFSTUDIO-FMEDIT-065 is scenario-specific and bundles three behaviours** (open the
   status editor, Escape closes it, tall table scrolls to both ends and syncs to line 1) at one
   width; its derives_from (StRS-001 and 004) is weak and the scroll part belongs to the layout
   scope. Fix: reduce to "At a 460 px preview width in edit mode, the field editor SHALL open and
   close on Escape without horizontal overflow" or drop it as duplicate of 001/020 and keep the
   visual scenario as an extra test marker on those; move the scroll sync to layout-width.
8. **SwRS-MDOKFSTUDIO-FMEDIT-003 mixes display and save and the SHALL is vague.** "save ... when the
   select is committed" hides the rule that a pick alone does not save (the criteria say "not on
   the change event"). Fix: SHALL "...show a select offering the schema values; the extension SHALL
   post the chosen value when the select loses focus or Enter is pressed in it"; consider
   splitting the placeholder behaviour (boundary) from the save trigger.
9. **SwRS-MDOKFSTUDIO-FMEDIT-018** bundles two refusals (not nullable, conditional rule forbids)
   and the boundary THEN "refused by the schema check of the edited document" names no observable
   result. Fix: split, or at least state the message ("Schema validation failed: <message>") for
   the conditional case (`checkFrontmatterCandidate`).
10. **Coverage gap: flush on pagehide or hidden page.** `blockEditor.ts:flushHiddenPage` (bound by
    `bindPageHide` on `pagehide` and `visibilitychange` hidden) saves an open field editor as a
    flush; `runtimeEditorFlush.test.ts` "pagehide and a hidden page save an open frontmatter
    editor as a flush" covers it. Neither the inventory nor any SwRS states it (067 names only a
    navigation and a host flush request). Add a SwRS "Hiding or closing the page saves the open
    field editor as a flush" derived from StRS-010 and add it to the inventory column (new row or
    F-FMEDIT-034).
11. **SwRS-MDOKFSTUDIO-FMEDIT-028 mixes layout into a unit-tested SHALL.** The nominal THEN "covering
    neither the value nor other rows" is not what the cited unit test checks (visual and real-input
    scenarios do) and the inventory claim that the menu and tooltips wrap inside the row at about
    520 px (F-FMEDIT-015) is in no SwRS. Fix: keep 028 to presence and position (inside the edited
    row, after the control) and add a layout SwRS for the no-overlap and 520 px wrap rule with the
    visual and RI-T23 markers.
12. **SwRS-MDOKFSTUDIO-FMEDIT-035 lacks its condition.** "Custom key..." exists only in the select,
    which is shown only when schema fields are left to add; with none left the text input of 034
    is used. State the condition in the SHALL ("When the Add field picker lists schema fields and
    the schema allows additional properties...") and use it as the boundary instead of the
    forbidden case only.
13. **StRS-MDOKFSTUDIO-FMEDIT-001 leaks an internal id** ("001 UX-38" in the Known issue line).
    Remove the id (batch 1 myst D4 precedent); the SwRS-002 Known issue already states the
    behaviour.
14. **Inventory rows are stale against the code** (only the rows, the SwRS are right): F-FMEDIT-002
    ("block editors ... ignore input while a field editor is open" is false), F-FMEDIT-003
    ("picking a value saves it at once": it saves on blur or Enter), F-FMEDIT-029 ("the row's
    line": it is line 1 of the properties section). Correct the three rows so the traceability
    text matches the SwRS.

## Advisory (non-blocking)

- SwRS-025 (post a rename plus keeps comments), 039 (one line plus compact list plus CRLF) and 041
  (three drop triggers) are borderline bundles; acceptable as families, split if a test needs
  them apart.
- SwRS-070 verifies a protocol flag (no `flush` property): implementation detail, observable only
  through 068; consider merging it into 067 as a boundary.
- SwRS-044 boundary (a value edited as an object) does not exercise the anchor or alias fallback.
- SwRS-055 and 057 have no test for the Undo step or the frontmatter pin (stated in notes);
  plan: the implementation step must add them or set `annotation_exemption`.
- Verification notes quote test titles with internal ids (T24, T41, CR 025); accepted, they are
  test names.

## Re-check

Revised scope: 11 StRS, 85 SwRS (080 and 081 archived). Checked every one of the 14 defects and the
new SwRS 072-085 against `src/page/features/*`, `src/session/*` and `src/core/edits/frontmatterEdit.ts`.

Fixed and verified: D1 (002 retitled, its Known issue "a block editor can still be opened" is true:
`openBlockEditor` and `openInsertPoint` have no `activeFrontmatterEdit` guard; 072 true:
`blockMoves`, `blockSelectionView` guard), D2 (057 and StRS-004 now say the properties table; pinLine
1 confirmed in `frontmatterPinFields`), D3 (004/075/076 true against `frontmatterValueEditor.ts`
keydown), D4 (011/077/078 true against `frontmatterListEditor.ts`), D5 (022/082; "Saved. Refreshing
preview…" in `receiveFrontmatterResult`), D6 (052/083 true: gate `reportStaleEdit` vs
`currentPreviewDocument`), D8 (003/074), D9 (018/079), D10 (085), D11 (028/084), D12 (035 SHALL has
its condition), D13 (no "UX-38" left). Also fine: StRS wording (descriptions equal normative text,
single SHALL, no internal ids), 034 and 083 Known issues, 007/009/010 Known issues.

Remaining defects:

1. **SwRS-MDOKFSTUDIO-FMEDIT-073 is false.** Title and SHALL say the "Enter key on an insert point"
   is ignored while a field editor is open and the boundary says "Enter on a plus insert point →
   no block editor opens". In `insertPoints.ts:bindKeys` the guarded keydown is the document-wide
   Enter shortcut of the empty-document "Start writing" point only; the "+" insert point button
   (`createInsertPoint` click → `openInsertPoint` → `openBlockEditor`) has no frontmatter guard and
   opens a block editor. Fix: retitle "The figure editor and the Start writing Enter shortcut ignore
   input while a field editor is open", reword SHALL and boundary accordingly (boundary: empty
   document, Enter, no block editor), and extend the Known issue of SwRS-002 to "a block editor can
   still be opened by clicking a block or a "+" insert point while a field editor is open". Correct
   inventory row F-FMEDIT-002 ("the "+" insert points ... ignore input") and its evidence in the
   same way. (SwRS-080, the archived copy, carries the same false text; leave it archived.)
2. **SwRS-MDOKFSTUDIO-FMEDIT-035 does not cover the behaviour dropped from FMSCHEMA-041.** The
   "section flag / no custom key" rule (a schema root with `additionalProperties: false` sets
   `data-okf-additional-properties="false"` on the properties section, and the Add field picker then
   shows no "Custom key…" entry, `frontmatterMenu.ts` l.104) is stated by no SwRS in FMEDIT or
   FMSCHEMA (grep of both scopes: only FMSCHEMA-041 error row, FMSCHEMA-046 annotations). The 035
   boundary tests "no schema field left" (that is 034), not the forbidden case. Fix: replace the 035
   boundary with "GIVEN a schema root with additionalProperties false and schema fields left to
   add, WHEN the picker renders, THEN it lists the fields and has no Custom key entry", and add a
   SwRS (derived from StRS-006, FMSCHEMA-011) "A closed schema flags the properties section" for
   the `data-okf-additional-properties` attribute (test: `propertiesTable.test.ts` "the section
   flags a schema that forbids additional properties"); map F-FMSCHEMA-023 to it in the inventory.
3. **SwRS-MDOKFSTUDIO-FMEDIT-065 is still scenario-specific.** The SHALL is bound to the "status"
   field at 460 px; the nominal THEN ("it opens, then closes") and the boundary ("closed layout")
   are not testable statements, and the 460 px claim is its only differentiator. Fix: "When the
   preview is 460 px wide in edit mode, the extension SHALL open a field editor on click and close it
   on Escape without horizontal overflow of the page", boundary = the cell shows the original value
   and the page has no horizontal scroll; or drop it and add the visual scenario as an extra
   `@tests_req` marker on 001/020.
4. **Scroll gap (reported, as expected).** Inventory F-FMEDIT-032 (the tall table at 460 px scrolls to
   both ends and back to line 1 on source sync) maps only to 065, and layout-width has no SwRS for
   it (grep "both ends", "stress", "tall table" over layout-width: no hit). Add a layout-width SwRS
   "A tall properties table scrolls to both ends at 460 px and returns to line 1 on source sync"
   (marker on `v06-okf-schema-narrow-scroll-stress-edit-dark-460`) and add it to F-FMEDIT-032's
   last column.

Decisions and advisory (non-blocking):

- FMEDIT-080 and 081 in `derived_by` of StRS-002 and StRS-011: not a defect. Both are `lifecycle:
  deprecated`, the validator passes, and the same pattern exists elsewhere (DIAG-021 in
  StRS-DIAG-001). They only add noise to the index; remove them if okfreq offers a supported way.
- Inventory row F-FMEDIT-029 still opens with "The edited row keeps its place on screen"; make it
  "The properties section keeps its place" (the parenthesis is right).
- SwRS-003 verification criteria ends "Escape cancels", which belongs to 020; trivial.
- 072 and 073 each bundle two inputs in one SHALL (family style); acceptable once 073 is fixed.

Verdict: FIX-REQUIRED

## Re-check 2

Checked in the worktree (`okfreq validate`: 0 errors, 0 warnings) against `insertPoints.ts` (line 110), `editorChrome.ts` (line 375), `frontmatterMenu.ts` (lines 104-109), `propertiesTable.ts` (line 267), `okfFrontmatter.ts` (line 514) and the T25 tests.

Re-check 1 defects:

1. FMEDIT-073: fixed. Retitled "The figure editor and the Start writing Enter shortcut ignore input while a field editor is open"; SHALL and boundary now name the empty-document Enter shortcut; both guards exist (`insertPoints.ts:110`, `editorChrome.ts:375`). The Known issue about the "+" insert point is in 073 and in FMEDIT-002 ("a block editor can still be opened by clicking a block or a plus insert point"). Inventory F-FMEDIT-002 corrected.
2. FMEDIT-035 and the flag: fixed. 035's boundary is now "schema root with additionalProperties false and fields left: lists the fields, no Custom key..." (matches `frontmatterMenu.ts:104` and test "T25: the picker offers Custom key only when additional properties are allowed", which asserts both cases). New FMEDIT-086 states the flag (`propertiesTable.ts:267`; test "T25: the section flags a schema that forbids additional properties" covers false, true and undefined; `okfFrontmatter.ts:514` gives `additionalPropertiesAllowed = additionalProperties !== false`). 035, 086 and FMSCHEMA-041 together cover "closed schema: no custom key", with cross-references both ways; no gap and no contradiction.
3. FMEDIT-065: fixed (one generic SHALL at 460 px, testable boundary: original value shown, no horizontal scroll).
4. Scroll gap: fixed by new FMEDIT-087 (derives from StRS-FMEDIT-004, cites the v06 scenario, whose id text says three scroll cycles, both ends, return to top, source line 1); 065 Criteria points to it; F-FMEDIT-032 maps to 065 and 087. 087 lists two outcomes in one SHALL (scrollable to both ends, return to line 1 on sync); accepted because re-check 1 proposed that wording, the scenarios split them.
5. Advisory items: F-FMEDIT-029 wording fixed. SwRS-003 Criteria still ends with "Escape cancels" (belongs to 020): trivial, not blocking.

Remaining defect (inventory only, no requirement edit):

1. `inventory/frontmatter-schema.md` row F-FMSCHEMA-023 (last column: only SwRS-MDOKFSTUDIO-FMSCHEMA-041) still says "the section is flagged so the editor offers no custom key" without mapping the flag to FMEDIT-086 / FMEDIT-035. Fix: add `SwRS-MDOKFSTUDIO-FMEDIT-086, SwRS-MDOKFSTUDIO-FMEDIT-035` to the last column (re-check 1 defect 2 asked for it).

Note: StRS-FMEDIT-002 and StRS-FMEDIT-011 still list the deprecated FMEDIT-080 and FMEDIT-081 in `derived_by`; okfreq does not prune it. Same STATE.md remark as in the diagrams re-check 2, not a defect on its own.

Verdict: FIX-REQUIRED

Fixed after Re-check 2 (one pass): DIAG-004 parenthesis removed, inventory row F-FMSCHEMA-023 mapped to FMEDIT-086/035, deprecated-in-index noted in STATE.md. Verdict after fix: APPROVE
