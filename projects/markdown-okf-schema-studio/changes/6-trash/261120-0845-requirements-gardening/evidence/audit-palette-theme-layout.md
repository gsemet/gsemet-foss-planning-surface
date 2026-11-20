# Audit: palette-slash, theme-zoom, layout-width (read-only)

Repository `markdown-okf-schema-studio` at `main` (dedbdb2a), 2026-11-17. Gardening phases 4, 6
and 6b, read-only: nothing in the repository was edited. Evidence: `okfreq trace requirements
--json`, frontmatter of every requirement, and a scan of every `@implements_req` / `@tests_req`
line with the code that follows it. Paths are relative to the repository root; `file:line` is the
marker line.

Scope: 13 StRS in force (LAYOUT-001, 003, 004; PALETTE-001, 002, 005, 007, 013, 015, 018;
THEME-002, 004, 011). LAYOUT-002 and 005 to 009 are superseded, and each points to an in-force
StRS. They derive 106 distinct in-force SwRS: 93 in these scopes (palette 74, theme 8,
layout 11) and 13 from other scopes (BLOCK-047, CORE-028, CORE-050, LIFE-169, LIFE-170,
TABLE-085, TABLE-111, TOOLBAR-013, TRUST-001, 005, 006, 065, 090). Every one of the 93 has at
least one implementation marker and one test marker. **Orphans: none.** Each in-force SwRS of
these scopes is derived by an in-force StRS. Deprecated SwRS that are still listed in
`derived_by` (PALETTE-086, 174, THEME-018, 024, 055, 056, DIAG-021) are not cited in any Main path.

Approved StRS (LAYOUT-001, LAYOUT-003, PALETTE-015): any change below needs the owner's recorded
agreement (project.guidelines.md, "Approved requirements").

## Summary

| StRS | Title (short) | #SwRS in force | Relevance | Split OK? | Markers OK? | Tests OK? | Validation test? | Diagram |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LAYOUT-001 (appr.) | Never scrolls sideways, wide content scrolls in its box | 2 | Real; mixes in a maintainer-tooling need | Partly: 001 and 032 overlap; 001 holds test tooling | No: 001 is only in a CSS cluster | Mostly | Partial (one visual scenario, path 1 only) | State/activity |
| LAYOUT-003 (appr.) | Reader chooses column width | 7 (incl. LIFE-169/170) | Real; too verbose (12 KB) | Partly: 023 too big, 023/044 and 022/032 overlap | Partly: 002 and 022 in clusters | Gaps (setting edge cases, %/em, Mermaid) | Partial (setting path only) | State |
| LAYOUT-004 | First element clear of top and toolbar | 4 | Real; carries history | Partly: 018 mostly internal | Mostly: 043 in a cluster | Minor gaps | Yes (visual gap family) | Sequence |
| PALETTE-001 | Formats and inserts Markdown, GFM, MyST from the palette | 53 | Real but far too broad; stale shortcut text | No: umbrella that overlaps 4 StRS; 3 families to merge | No: 17-ID header cluster, registry cluster | Tests exist, but 18 SwRS are marked only in a file header | Only through the companion file | Sequence |
| PALETTE-002 | Chooses which palette buttons are offered | 7 | Real; the text omits the Full mode | 010 duplicates LIFE-169 | Mostly | OK | Yes (integration paletteMode) | State + sequence |
| PALETTE-005 | Palette stays in reach, soft, never closes by accident | 6 | Real; three ideas in one | 021 overloaded; 115 has the wrong parent | Mostly | OK | Only through the companion file | State |
| PALETTE-007 | Links, images, figures, tables, colours, emoji through pickers | 16 | Real; overlaps PALETTE-001 | OK | Mostly | OK; 092 marked only in the header | Yes (imagePicker, path 1) | Sequence |
| PALETTE-013 | Labels, documents, citations, code languages from host lists | 16 | Real; code languages overlap 001 | OK | OK | 147 and 149 marked only in the header | Yes (mystPickers) | Sequence |
| PALETTE-015 (appr.) | Runs any command from an accessible slash menu | 11 | Good | Good (268 could be a scenario of 238) | Mostly | 240 and 256 tests not marked | Companion file + visual v21 | State |
| PALETTE-018 | Pastes screenshots and rich text safely | 8 | Real; text omits the Explorer drop and URL paste | OK | OK | 264 has a misplaced test marker | Yes (imagePaste, realWindowGaps, visual) | Sequence |
| THEME-002 | Chooses a theme that paints the whole page | 7 | Good | 034 is internal | No: 001 and 031 in clusters, CORE-050 on a file header | 016 values partly untested | Visual + companion file | State |
| THEME-004 | Theme choice holds for the workspace | 5 | Good | 013 duplicates LIFE-169 | OK | OK | Partial (default Cream only) | Sequence |
| THEME-011 | Zooms text and column and keeps the zoom | 7 | Good, concise | TOOLBAR-013 duplicates LIFE-169 | 043 in a cluster | Toolbar size not asserted | Partial (scaling only) | State |

## StRS-MDOKFSTUDIO-LAYOUT-001 (approved)

- **Relevance (medium):** the user_need adds "As a maintainer, I can run machine layout checks"
  (inherited from the superseded LAYOUT-009). That is test tooling, not a reader use case. In
  SwRS-LAYOUT-001, the scenario "(boundary): Machine geometry checks" describes the four check ids
  of `test/page/geometryChecks.test.ts:92`. Its own known issue says it has "no user-visible
  effect". Proposal: drop the maintainer half from the StRS and the scenario from the SwRS, and
  keep the checks as test infrastructure.
- **Split (medium):** the SwRS-LAYOUT-001 scenario "Narrow table and long words" (visual v01)
  repeats the SwRS-LAYOUT-032 scenario "Service-level table at 460 px". Both are test-marked on
  the same visual scenario (`test/visual/scenarioDefinitions1.ts:198-200`). Mapping: LAYOUT-001 =
  no page-level sideways scroll + long words and URLs wrap; LAYOUT-032 = table scroll box, shaded
  edges and short identifiers.
- **Markers (medium):** the only implementation marker of LAYOUT-001 is in an 11-ID cluster on
  `CONTENT_LAYOUT_CSS` (`src/core/preview/styles/contentLayoutStyles.ts:80-90`). Move it to the
  wrapping rules (`contentLayoutStyles.ts:314`, `:407`; `contentBlockStyles.ts:161`). The
  LAYOUT-032 marker sits in the 3-ID header of `TABLE_CSS` (`tableStyles.ts:1-3`): move it to the
  scroll-box / overflow-shadow rule. `scrollCore.ts:392` (`markWideTables`) is correct.
- **Tests (low):** LAYOUT-001 is covered (K1 `previewStyles.test.ts:1172`, visuals v01, v66-v71,
  v78-v83, gfm/v02-v04). LAYOUT-032: the scroll-box rule itself has no unit test (known issue).
  The refusal "table that fits" is covered by the 1 px tolerance test
  (`runtimeScroll.test.ts:1034`).
- **Validation (low):** `@tests_req StRS-LAYOUT-001` is on `scenarioDefinitions1.ts:198`
  (handbook-narrow-table) only, which is path 1. Also mark the width-mode visuals v78-v80 at
  460 px (path 2).
- **Diagram:** a state/activity diagram. Document rendered → the page measures each block → three
  branches: table wider than the box → scrolls in its box, edges shaded; table fits → left as is;
  long word or URL → wraps. All three end in "page has no horizontal overflow" (≤ 1 px).

## StRS-MDOKFSTUDIO-LAYOUT-003 (approved)

- **Readability (low/medium):** 12 KB, 16 rationale bullets that repeat SwRS numbers (16 px
  gutter, 256 px TOC, rounding up, 1 px tolerance). Trim to the reader-level promises and leave
  the numbers to the SwRS. The normative text covers two actors (team setting, reader button),
  which is acceptable.
- **Split (medium):** SwRS-LAYOUT-023 is 12 KB with 10 scenarios, some of them internal:
  "Several triggers in one frame" is the P-08 frame coalescing (`runtimeScroll.test.ts:1170`).
  LAYOUT-044 refines the table case of 023. Mapping: 023 = Auto breakout of figures, images,
  code and Mermaid, plus re-measure; move the table scenarios of 023 (uncapped and rounded up,
  row handles, cell editor) into 044; turn "one frame" into a verification note. SwRS-LAYOUT-022
  "Wide table in Margin" overlaps LAYOUT-032: cite 032 through `depends_on`.
- **Markers (medium):** LAYOUT-002 is in a 7-ID cluster on `PAGE_CHROME_CSS`
  (`pageChromeStyles.ts:145-151`); move it next to the `--sphinx-preview-content-max-width` rule
  (`pageChromeStyles.ts:164`). LAYOUT-022 is in the `contentLayoutStyles.ts:85` cluster; move it
  to the Margin and Full width rules. Correct: `settingsRegistry.ts:127`, `previewStyles.ts:129`,
  `hostEvents.ts:399`, `widthMode.ts:8`, `runtime.ts:291`, `widthMode.ts:160/189` (044),
  `scrollCore.ts:416`.
- **Tests (medium):** LAYOUT-002: decimal rounding and negative input are not unit-tested, and
  the rendered column at 0 is not checked (self-declared). The open-preview update has a unit test
  (`test/session/diagReq.settings.requirements.test.ts:95`) but no integration test. LAYOUT-022:
  centring is checked only visually, and the negative figure mark is untested. LAYOUT-023:
  %/em/rem figures, the Mermaid wrapper and the re-measure after a patch, image load or TOC toggle
  are untested.
- **Validation (medium):** the StRS markers are on two visual scenarios of the setting
  (`scenarioDefinitions1.ts:622`, `scenarioDefinitions2.ts:1138`), which is path 2 only. Path 1
  (Width button cycle, stored for the workspace) has no stakeholder test. Candidates:
  `capture_layout_checks.py:763` `check_width_modes` (v66-v71), or an integration test that stores
  `widthMode` and reopens.
- **Diagram:** a state diagram Margin → Auto → Full width → Margin (button press), with entry
  notes: Margin = blocks kept in the column; Auto = wide blocks break out to the available area;
  Full = no limit, 16 px gutter. Add the transition "setting maxContentWidth changed → column
  width", and "reopen → stored mode".

## StRS-MDOKFSTUDIO-LAYOUT-004

- **Readability (low):** the rationale keeps history ("Earlier values (56 px…, 24 px…) are
  superseded") and a CHANGELOG known issue. Remove the history.
- **Split (medium):** SwRS-LAYOUT-018 is mostly internal: more than 200 updates per second, one
  trailing timer, a `describe()` diagnostic, a CI run number. Mapping: merge its observable part
  into LAYOUT-011 as the scenario "the clearance follows layout changes (resize, font, collapse,
  width mode)", and keep the burst limit as a verification note. 007 (gap), 011 (controls) and
  043 (text float) are a good observable split.
- **Markers (low):** LAYOUT-043 `contentBlockStyles.ts:19` ends a 14-ID cluster on
  `CONTENT_BLOCK_CSS` (lines 6-19); it is redundant with the correct marker at
  `contentLayoutStyles.ts:41` (`TOOLBAR_FLOAT_CSS`). Correct: 007 at `contentLayoutStyles.ts:3`
  and `:14`, 011 at `firstClearance.ts:85`, 018 at `runtime.ts:283` and `firstClearance.ts:308`,
  043 at `firstClearance.ts:146`.
- **Tests (low):** the 011 narrow-table fallback is untested, and so is the 018 animation-frame
  settle (60 or 300 frames); both are self-declared.
- **Validation:** OK. `scenarioAssertions.ts:673` (first-element-gap family) and
  `scenarioDefinitions1.ts:1217` (edit-first-block-top-wide).
- **Diagram:** a sequence diagram. Page runtime → firstClearance.measure → reads the rectangles
  of the floating toolbar, the column and the first control → publishes
  `--sphinx-preview-first-clearance`, `-first-inset`, `-toolbar-bottom` → CSS moves or narrows the
  control. A loop on resize, font, collapse and width mode.

## StRS-MDOKFSTUDIO-PALETTE-001

- **Relevance (high):** the use case is real but works as an umbrella. It derives 54 SwRS
  (53 in force) and overlaps PALETTE-005 (021, 115), PALETTE-007 (058, 072, 089, 092, 109, 150,
  153, 160), PALETTE-013 (054), PALETTE-015 (039, 052, 238, 242, 263), PALETTE-018 (004, 213,
  264) and the table scope (TABLE-111). Its rationale is stale and misleading: "the documented
  shortcuts are for bold, italic, link and TODO comment", but SwRS-PALETTE-086 (TODO shortcut) is
  deprecated and SwRS-PALETTE-266 says Cmd/Ctrl+/ toggles a plain HTML comment. The normative
  text names the GFM and MyST modes only, not Full.
- **Proposed restructure (medium):**
  - New StRS A, "formats text with buttons and shortcuts": 039, 043, 045, 048, 049, 050, 052,
    053, 083, 266, 003.
  - New StRS B, "inserts GFM constructs": 115, 123, 124, 125, 126, 267, 269 (alert part).
  - New StRS C, "inserts MyST constructs": 127, 130, 132, 133, 135, 136, 137, 138, 270, 271,
    272, 273, 274, 265, 269 (admonition part).
  - Drop PALETTE-001 from `derives_from` where another StRS already owns the SwRS: 004, 021, 054,
    058, 072, 089, 092, 109, 150, 153, 160, 213, 238, 242, 263, 264.
- **SwRS merges (medium):**
  - Inline marker toggles: 045, 048, 135, 138, 126 become one table-driven SwRS.
  - Line-prefix toggles: 049, 052, 053, 123, 267 become one SwRS.
  - 130 and 137 merge into 127 (both already `depends_on` 127).
  - The mode-membership refusals of 265, 273 and 274 become rows of the table in 001; keep their
    insertion scenarios as one "starter block" SwRS.
- **Wrong or internal (medium):**
  - 002 mixes the tooltip and the rule icon: split it, or reword it as "edit bar buttons show
    their title and shortcut".
  - 275 ("every rendered syntax has a slash entry or a documented exception") is a
    maintainer-consistency rule (`slashSyntaxCoverage.test.ts:123`): exempt it or move it to
    tooling.
  - 114 (Thread) belongs to the review scope.
  - TABLE-111 (column alignment) has PALETTE-001 as a questionable parent.
  - 021 (17 KB, 8 scenarios) hides a scroll-sync behaviour, "the page does not follow the
    editor's scroll caused by an edit" (`session/features/blockEdits.ts:346`,
    `scrollSync.ts:146`, tested at `toolbarReq.requirements.test.ts:679`). Split it out.
- **Markers (medium):**
  - `src/page/modules/editPalette.ts:23-39` is a module-header cluster of 17 IDs (001, 002, 017,
    031, 036, 039, 069, 078, 083, 109, 115, 148, 150, 238, 242, 269, LIFE-169) on a 747-line file.
    Move each ID to its builder or handler.
  - `src/core/palette/paletteActions.ts:209-211` puts 001, 263 and 275 on `PALETTE_ACTIONS`.
    Move 263 to the `aliases` entries.
  - `src/page/features/blockSourceEditor.ts:44-51` is an 8-ID cluster (001, 021).
  - 002 is on the import line of `pageChromeStyles.ts:1`: move it to the tooltip rule.
  - 089 is on `closeBlockEdit` (`src/page/features/blockEditor.ts:41`), a generic helper.
  - Correct: one marker per action function in `blockEditActions.ts` and `inlineEditActions.ts`
    (043, 045, 048, 049, 050, 053, 123-138).
- **Tests (medium):** `test/page/modules/editActions.test.ts:9-48` is a block of 40
  `@tests_req` lines at the file header. It is the **only** test marker of 18 SwRS (045, 048,
  049, 050, 114, 123, 124, 125, 127, 130, 132, 133, 135, 136, 137, 138, 147, 149). The tests do
  check their scenarios. Move each marker next to its test: strikethrough `:325`, quote `:346`,
  rule `:383`, checkbox `:711-749`, details `:847`, footnote `:859`, kbd `:913`, admonition
  `:943-972`, custom `:977`, deflist `:986`, math `:995`, sub/sup `:1009`, label `:1017`, ref
  `:1039`, cite `:1055`, dropdown `:1062`, roleKbd `:1095`, thread `:1381`. Misplaced test
  markers:
  - PALETTE-264 on `test/build/integrationEditModeRestore.test.ts:10`, a meta test about edit
    mode restore between scenarios. **High (misleading).**
  - PALETTE-001 on `test/security/package-contract.test.ts:40` ("contributes only opt-in
    commands").
  - 001's refusal test title says "outside the three modes" (`paletteReq.requirements.test.ts:155`)
    while there are four modes.
- **Validation (medium):** the StRS marker sits only in the companion file
  `test/integration/realInput/markers.ts:57` (`export {}`). The real validation is `scenarioPalette`
  (`test/integration/realInput/textEditing.ts:612`: Bold, typing between markers, Heading 2 and
  one undo). Path 2 is `scenarioLinkPanel` (`:730`). Move the marker there.
- **Diagram:** a sequence diagram. Writer → Palette button / slash / shortcut → action registry
  → action returns a TextEdit → text box applies one native edit (autosave) → Writer presses undo
  → text restored. An alt branch: action returns nothing → text unchanged, reason in the status
  line.

## StRS-MDOKFSTUDIO-PALETTE-002

- **Wording (medium):** the description says "a strict Markdown, a GitHub Flavored Markdown and
  a MyST set", but the Full mode exists (SwRS-001 and the select offers four modes; 265 and 274).
  Add Full and state that the sets are nested.
- **Split (medium):** SwRS-PALETTE-010 ("unknown palette mode is refused") repeats the Palette
  mode row of LIFE-169 ("Dropped unless the mode is one of the four"). Keep one of them. Proposal:
  keep the LIFE-169 row and supersede 010 into it. TRUST-001 derived from 002 is a weak link
  (trust is not part of choosing the button sets): use `relates_to`.
- **Markers:** correct: 010 at `pageToHost.ts:261`, 017 at `blockSourceEditor.ts:361`. The rest
  are in the editPalette cluster above.
- **Tests:** OK (`pageToHost.test.ts:130`, `runtimeEditPalette.test.ts:933`,
  `editPalette.test.ts:92`).
- **Validation:** OK. `test/integration/paletteMode.test.ts:39` (the stored mode wins over the
  setting in the next panel).
- **Diagram:** a nested-set state diagram Strict ⊂ GFM ⊂ MyST ⊂ Full, plus a short sequence:
  Writer (Cmd/Ctrl+Shift+M) → mode select → page posts `previewPaletteModeChanged` → host
  validates and stores → new panel boots with the stored mode, else the setting.

## StRS-MDOKFSTUDIO-PALETTE-005

- **Relevance (low):** the title carries three ideas (in reach, soft, never closes). CORE-050 is
  shared with THEME-002, which is fine.
- **Split (medium):** 021 is overloaded (see PALETTE-001). PALETTE-115 (Alert) deriving from 005
  is not explained by this use case: drop the link.
- **Markers:** 031 is correct at `blockSourceEditor.ts:332`, `linkPanel.ts:89` and
  `figurePanel.ts:41`. 036 is at `editPalettePopovers.ts:397` (`buildColor`), shared with 058:
  move it to the mousedown-cancel point (`linkPanel.ts:39` is correct).
- **Tests:** OK. 031 and 036 have targeted tests (`runtimeEditPalette.test.ts:108`, `:170`;
  `editPalette.test.ts:439`). 031 is also in the companion file.
- **Validation (medium):** only the companion file `markers.ts:58`. Real candidates:
  `scenarioPalette` (`textEditing.ts:612`, focus stays in the textarea after Bold; Escape closes
  the list first), `test/integration/editToolbarCover.test.ts:86` and
  `tallBlockScroll.test.ts:136`.
- **Diagram:** a state diagram. Editor closed → Editing (palette docked or sticky) → Popover open
  (one at a time) → Escape → Editing → Done, Cmd/Ctrl+Enter or leaving the frame → Committed. Note
  the transitions that never commit: palette press, native file dialog.

## StRS-MDOKFSTUDIO-PALETTE-007

- **Relevance (low):** clear. 13 of its 16 SwRS also derive from PALETTE-001 (see that section).
- **Split:** good (089/092 link, 109/192 image, 150/153/160 figure, 058/069 colour, 072, 078).
  TRUST-005 and TRUST-065 are internal gates (page message matched to the render). Use
  `depends_on`, not `derives_from`.
- **Markers:** mostly correct (`linkEditActions.ts:23`, `:130`; `figureDirective.ts:106`,
  `:154`; `colourEditActions.ts:102`, `:178`). 109 and 150 are also in the editPalette cluster.
- **Tests:** OK. 092 is marked in the header and at `runtimeEditPalette.test.ts:499`. Its safety
  cases are in `editActions.test.ts:519-542` without a marker.
- **Validation:** `test/integration/imagePicker.test.ts:26` covers path 1. Path 2 (colour) has
  only unit tests (T34).
- **Diagram:** a sequence diagram. Writer → Image button → page asks the host → host opens the
  native dialog (editor stays open) → host answers a path relative to the document, or cancel →
  page inserts or replaces `![alt](path)` in one undo step.

## StRS-MDOKFSTUDIO-PALETTE-013

- **Relevance (low):** good. The code-block languages (054) also sit in PALETTE-001. "Answer
  every request within a bounded time" rests on TRUST-090 (another scope).
- **Split:** good (140 list UI, 147/148/149 roles, 178 labels, 183 bounded bib scan). 192, 196
  and 203 fit PALETTE-007 and PALETTE-018 better. Keep them there only.
- **Markers:** correct (`mystTargets.ts:38`, `:85`; `bibScan.ts:32`; `hostRequests.ts:184`,
  `:209`).
- **Tests:** 147 and 149 have only the editActions header marker (tests at `:1039` and `:1055`).
  183 has bounds tests (`session/paletteReq.requirements.test.ts:48`, `:71`).
- **Validation:** OK. `test/integration/mystPickers.test.ts:8`.
- **Diagram:** a sequence diagram. Writer → Reference button → popover "Loading…" → host lists
  the `(name)=` targets, or scans at most 20 bib files of 2 MiB or less → list, possibly cut,
  with a note → Writer picks → `{ref}` or `{cite}` written. Alt branch: empty list or host error.

## StRS-MDOKFSTUDIO-PALETTE-015 (approved)

- **Relevance:** good and readable.
- **Split (low):** well split (232 open, 238 list, 240 rank, 242 keys, 252 ARIA, 256 placement,
  263 aliases). 268 (MyST admonitions listed with icons) could be a scenario of 238. TABLE-085
  (the table bar's cell group) deriving from 015 is questionable.
- **Markers (low):** 263 is on the registry header (`paletteActions.ts:209`). 238 and 242 are
  also in the editPalette cluster. The `slashMenu.ts` markers are correct (`:190`, `:249`, `:330`,
  `:370`, `:471`, `:489`).
- **Tests (medium):** PALETTE-240 has one marker (`slashMenu.test.ts:323`). Its scenarios "MyST
  wins a near tie" and "a loose best match leaves Enter and Tab" are tested at
  `slashMenu.test.ts:762` and `:783` without markers. PALETTE-256 has 6 scenarios and one marked
  test (`:680`).
- **Validation (medium):** the companion file `markers.ts:60` and the visual
  `scenarioDefinitions2.ts:1124` (menu appearance only). Real validation: `scenarioSlashMenu`
  (`textEditing.ts:495`: `/h2` Enter, one undo, `/tab` grid, Escape keeps the text). Move the
  marker there.
- **Diagram:** a state diagram. Closed → (slash at line start or after a space) Open, listing
  the mode's commands → typing → Filtered (alias or label) → Enter, Tab or click → command runs in
  one edit → Closed. Escape or caret out → Closed, text kept. Slash in a word → stays Closed.

## StRS-MDOKFSTUDIO-PALETTE-018

- **Relevance (medium):** the title and the normative text cover image and rich-text paste only,
  yet the StRS derives 004 (files dropped from the Explorer) and 264 (pasted URL becomes a
  link). Add both to the normative text, or move 004 to PALETTE-007. The first rationale bullet is
  self-referential ("belong to the palette and paste use cases"). Low.
- **Split:** good (203/196 image, 213/217/229 HTML, 264 URL, 004 drop).
- **Markers:** correct (`pasteImage.ts:84`, `pasteHtml.ts:45`, `pasteUrl.ts:102`,
  `htmlToMarkdown.ts:33`, `:279`, `hostRequests.ts:285`, `:358`, `dropReferences.ts:91`).
- **Tests (high for 264):** see the misplaced marker in `integrationEditModeRestore.test.ts:10`.
  The real tests of 264 are `pasteUrl.test.ts:12-69` and `test/integration/pasteUrl.test.ts:59`.
  229 relies on one parametrized table test (`htmlToMarkdown.test.ts:85`), which is acceptable.
- **Validation:** OK. `imagePaste.test.ts:26`, `realWindowGaps.ts:556`, visuals.
- **Diagram:** a sequence diagram. Writer pastes → page paste handler → image-only? host saves
  `image-N.ext` next to the document and the page inserts a paragraph; HTML? host converts, safe
  subset; URL? link, autolink or image → one undoable edit in the same text box. Alt: text on the
  clipboard wins, plain paste.

## StRS-MDOKFSTUDIO-THEME-002

- **Relevance:** good. One rationale bullet is internal ("this scope records the reduced-motion
  preference on the page"). Low.
- **Split (medium):** SwRS-THEME-034 ("Page colours go through one token map") describes the
  stylesheet structure. Its observable part is "a host colour that is set is used; an unset one
  keeps the fallback". Reword it to that, or exempt it. CORE-028 (typography) deriving from
  THEME-002 is weak.
- **Markers (medium):**
  - THEME-001 at `contentLayoutStyles.ts:87` (cluster). `themeMode.ts:88` is correct.
  - THEME-031 at `pageChromeStyles.ts:148` (cluster): move it to the Cream block of
    `FORCED_THEME_MODES_CSS` (`pageChromeStyles.ts:7`).
  - CORE-050 on the file header of `propertiesStyles.ts:1`: move it to the reduced-motion
    `@media` rule at `propertiesStyles.ts:535`.
  - 025 at `pageChromeStyles.ts:7`, 016 at `hostEvents.ts:472` and `viewState.ts:124`, and 034 at
    `themeTokens.ts:88` are correct.
- **Tests (low):** THEME-016: the theme-kind values default, 1, 3 and 4 are untested
  (self-declared). Its marker at `test/core/state/editLock.test.ts:24` (generic EditLock
  deferral) is only an indirect check.
- **Validation (low):** the visuals `scenarioDefinitions1.ts:101` (forced White) and
  `scenarioDefinitions2.ts:962` (forced Dark), plus the companion file `markers.ts:66`. The real
  cycle is check `38-toolbar-{host}-{mode}` in `test/integration/realInput/previewWindow.ts`
  (captures r01-r08): put the StRS marker there.
- **Diagram:** a state diagram Current → Dark → White → Cream → Current (Theme button). Each state
  is annotated "paints page, toolbar, heading band, notes". Current listens to the VS Code theme
  change (redraw deferred while a block editor is open).

## StRS-MDOKFSTUDIO-THEME-004

- **Relevance:** good. The normative clause about a page that "finishes loading late" is served
  by THEME-016 (ready answer) but is not on the Main path. That is acceptable ("also serves").
- **Split (medium):** SwRS-THEME-013 (host drops an unknown theme mode) repeats the Theme row of
  LIFE-169. Merge it into LIFE-169. The THEME-001 refusal table (unknown mode at boot) repeats the
  LIFE-170 normalisation: cite LIFE-170 instead.
- **Markers:** correct (`pageToHost.ts:215`, `viewState.ts:57`).
- **Tests:** OK. 013 is covered by `pageStateMessages.test.ts:226`. The LIFE-169 stale-message
  drop is untested (self-declared in LIFE-169).
- **Validation (medium):** `scenarioDefinitions2.ts:990` checks only the fresh-workspace Cream
  default. "Pick, reopen, same theme" has an integration test (`test/integration/lifecycle.test.ts`,
  "previewThemeModeChanged dark is stored and carried by the next page"). Add
  `@tests_req StRS-THEME-004` there.
- **Diagram:** a sequence diagram. Reader → Theme button → page posts
  `previewThemeModeChanged` → host validates (drop if unknown) → workspace state. Reopen → host
  boot context → page picks stored workspace > saved panel > Cream.

## StRS-MDOKFSTUDIO-THEME-011

- **Relevance:** good and concise.
- **Split (medium):** SwRS-TOOLBAR-013 (host accepts only a known view preference) repeats the
  Zoom, Width, TOC and other rows of LIFE-169. Merge it. TRUST-006 deriving from 011 is weak.
- **Markers (medium):** THEME-043 at `pageChromeStyles.ts:149` (cluster): move it to the zoom
  rules (`pageChromeStyles.ts:168`, column width `calc(... * --sphinx-preview-zoom)`).
  `contentPatch.ts:173` (shell key ignores the zoom) and THEME-038 at `viewControls.ts:52` are
  correct.
- **Tests (low):** "the toolbar does not scale" is not asserted (self-declared). The limits and
  tooltips are tested in T08 (`runtimePageControls.test.ts:261`).
- **Validation (medium):** the visual zoom scenarios (`scenarioDefinitions2.ts:975`) prove the
  scaling but not "keeps the zoom". No stakeholder test reopens at the saved zoom.
- **Diagram:** a state diagram, Zoom 70 … 100 … 200 in steps of 10. At 70 Zoom out is disabled,
  at 200 Zoom in is disabled. A side transition "reopen → panel zoom > workspace zoom > 100".

## Orphan SwRS

None. All 93 in-force SwRS of palette-slash, theme-zoom and layout-width are derived by at least
one in-force StRS of these scopes.

## Counts by category

| Category | Count | Examples |
| --- | --- | --- |
| StRS audited / SwRS audited | 13 / 106 (93 in scope + 13 cross-scope) | — |
| StRS relevance or wording issues | 7 (1 high, 4 medium, 2 low) | PALETTE-001 (too broad, stale shortcut text: high), PALETTE-002 (no Full), PALETTE-018 (no drop/URL), LAYOUT-001 (maintainer need), LAYOUT-003 (verbose), LAYOUT-004 (history), THEME-002 |
| SwRS that are scenarios of one behaviour (merge) | 15 SwRS into 5 targets | inline toggles 045/048/135/138/126; line prefixes 049/052/053/123/267; 130/137 into 127; 265/273/274 rows into 001; 268 into 238 |
| Repeated rule (duplicates LIFE-169) | 3 | PALETTE-010, THEME-013, TOOLBAR-013 |
| Overlapping SwRS | 3 pairs | LAYOUT-001/032, LAYOUT-023/044, LAYOUT-022/032 |
| SwRS describing internals or tooling | 5 | LAYOUT-001 geometry-check scenario, LAYOUT-018, LAYOUT-023 "one frame", THEME-034, PALETTE-275 |
| SwRS to split | 2 | PALETTE-021 (palette placement + scroll sync), PALETTE-002 (tooltip + rule icon) |
| Questionable `derives_from` | 8 links | 114 (review), TABLE-111←PALETTE-001, TABLE-085←PALETTE-015, 115←PALETTE-005, TRUST-001←PALETTE-002, TRUST-005/065←PALETTE-007/013, CORE-028←THEME-002 |
| Misplaced implementation markers (clusters, headers, helpers) | 10 locations, ~25 IDs of these scopes | `editPalette.ts:23-39` (17 IDs), `contentLayoutStyles.ts:80-90`, `pageChromeStyles.ts:145-151`, `pageChromeStyles.ts:1`, `paletteActions.ts:209-211`, `blockSourceEditor.ts:44-51`, `contentBlockStyles.ts:6-19`, `propertiesStyles.ts:1`, `tableStyles.ts:1-3`, `blockEditor.ts:41` |
| Misplaced test markers | 5 locations | `editActions.test.ts:9-48` (sole marker of 18 SwRS), `realInput/markers.ts` (8 SwRS + 5 StRS), `integrationEditModeRestore.test.ts:10` (PALETTE-264, high), `package-contract.test.ts:40` (PALETTE-001), `editLock.test.ts:24` (THEME-016) |
| Tests present but unmarked | 3 SwRS | PALETTE-240 (`slashMenu.test.ts:762`, `:783`), PALETTE-256, PALETTE-092 safety cases |
| Scenarios not checked by any test | ~14 scenarios in 9 SwRS | LAYOUT-002 (decimal, negative, rendered 0), LAYOUT-022 (centring unit, negative figure mark), LAYOUT-023 (%/em/rem, Mermaid, re-measure after patch/image/TOC), LAYOUT-011 (narrow fallback), LAYOUT-018 (frame settle), THEME-016 (kinds 1/3/4), THEME-043 (toolbar size), LAYOUT-032 (scroll-box unit), LIFE-169 (stale drop) |
| StRS validation | 13/13 have a marker; 6 good, 4 partial (LAYOUT-001, LAYOUT-003, THEME-004, THEME-011), 3 only through the companion file (PALETTE-001, PALETTE-005, PALETTE-015 + visual) | — |
| Severity totals | high 3, medium 27, low 13 | high: PALETTE-001 scope and stale shortcut text; PALETTE-264 test marker on an unrelated build test; 18 SwRS whose only test link is a file-header block (traceability does not point at the test) |
