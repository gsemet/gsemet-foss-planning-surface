# Audit: toolbar-navigation and lifecycle-sync (okfreq gardening, read-only)

Repository: `markdown-okf-schema-studio`, `main` at `dedbdb2a`, clean worktree. Phases 4, 6 and 6b of
`.agents/skills/okfreq-gardening/SKILL.md`, read-only. Evidence: `okfreq trace requirements --json`,
the frontmatter of every requirement and a grep of every `@implements_req` / `@tests_req` (one ID
per marker, no multi-ID markers found). Line numbers are those of `main` at `dedbdb2a`.

Scope: 16 in-force StRS (toolbar-navigation 9, lifecycle-sync 7; StRS-LIFE-019 is deprecated and
ignored). 93 in-force SwRS audited: 84 of these two scopes (TOOLBAR 40 proposed + 10 draft,
LIFE 34 proposed) and 9 of other scopes that an audited StRS derives (BLOCK-205, DIAG-128,
FMSCHEMA-014, FMSCHEMA-091, TRUST-001, -006, -007, -063, -065: noted here, owned by their own
scope's audit). No structural error: `missing_ids`, `non_leaf` and `warnings` are empty.

Severities: **H** = wrong or misleading traceability, or missing behaviour; **M** = split or marker
placement to fix; **L** = wording.

## Summary

| StRS | Title (short) | #SwRS in force | Relevance | Split OK? | Markers OK? | Tests OK? | Validation test? | Diagram |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIFE-001 | Open previews beside the editor or as tabs | 13 | real; overlaps LIFE-003 | no (LIFE-010 is part of LIFE-003; LIFE-171 is part of LIFE-001) | yes | partial | yes (lifecycle, stockCoexistence) | use case (actors) |
| LIFE-003 | Side preview follows the active file, refresh | 8 | real; overlaps LIFE-001 and LIFE-010 | over-derived (3 scroll SwRS) | mostly | partial | yes (lifecycle) | sequence |
| LIFE-005 | Preview updates in place | 10 | real | mostly (LIFE-004 is internal) | mostly | partial | yes (dirtySnapshots, updateGlow) | sequence |
| LIFE-007 | Render state and missing source | 7 | real | LIFE-055 is a scenario of LIFE-049 | yes | partial | yes (lifecycle, serializer) | state |
| LIFE-010 | Panes scroll together, position survives | 9 | real | LIFE-097 is a setting, not a behaviour | yes | partial | yes (scroll-sync, sourceMapping) | sequence |
| LIFE-014 | Reload, remember recent docs, leave nothing | 10 | real but 3 needs in one; misfit SwRS | no (LIFE-002, LIFE-172 misfit) | yes | partial | yes (reload, serializer, disposal) | state |
| LIFE-021 | Settings editor lists Studio settings | 3 | thin; overlaps LIFE-001/010 | no (path cites unrelated SwRS) | yes | yes | **no** | none needed (or a 2-step sequence) |
| TOOLBAR-001 | Toolbar rows, collapse, remembered choices | 9 | real; persistence overlaps LIFE-014 | no (TOOLBAR-013 duplicates LIFE-169; TRUST-001 misfit) | **no** (file-header markers) | partial | yes (visual) | state |
| TOOLBAR-002 (draft) | Fold sections | 5 | real | TOOLBAR-005 is a scenario of TOOLBAR-003 | **no** (install cluster) | yes | **no** | state |
| TOOLBAR-003 (draft) | Find and replace | 7 | real | no (7 SwRS for 3 behaviours) | **no** (6 markers on one installer) | yes | **no** | sequence |
| TOOLBAR-004 | Sticky heading band | 5 | real | TOOLBAR-022 (setting) and -002 (shadow) are scenarios | **no** (CSS cluster) | mostly | yes (visual) | sequence |
| TOOLBAR-006 | Table of contents column | 8 | real | TOOLBAR-133 near-duplicates TOOLBAR-037 | **no** (header and CSS clusters) | partial (unmarked tests) | yes (visual) | state |
| TOOLBAR-009 | Back and Next | 7 | real | no (056, 058, 065 are scenarios of 054/059) | yes | partial | yes (previewHistory) | sequence |
| TOOLBAR-011 | Links open, show target, or are refused | 14 | real; long | no (083, 113 are validators of 079/077) | yes | partial | yes (previewHistory) | sequence |
| TOOLBAR-013 | Anchor button and cursor block | 6 | real; overlaps LIFE-010 | no (122, 126 are validators of 120) | yes | partial | yes (scroll-sync, visual) | sequence |
| TOOLBAR-014 | Export one page to HTML | 6 | real | yes | yes (DIAG-128 has none) | yes | **no** | sequence |

## Cross-cutting findings

- **M, misleading derivation (over-derivation).** Shared SwRS are derived by many StRS instead of
  being cited with `depends_on`, contrary to the granularity rule ("a rule shared by many features
  ... is cited by `depends_on`"): LIFE-169 by 9 StRS, LIFE-170 by 10, LIFE-026/049/069 by 4,
  LIFE-032/100/125/127/156 by 3. The SwRS list of each StRS then mixes its own behaviours with
  generic plumbing, which hurts the "read the StRS to understand Studio" goal. Proposal: LIFE-169
  and LIFE-170 derive from LIFE-014 only; the feature SwRS that use them (TOOLBAR-007, -033, -120,
  and the THEME, LAYOUT, PALETTE ones) keep or gain `depends_on` (TOOLBAR-033 and -120 already do).
- **M, repeated validator SwRS.** Seven SwRS restate the shared message gate (TRUST-052, -059,
  -065) for one message each: TOOLBAR-013, -056, -058, -083, -113, -122, -126, plus LIFE-055.
  Each is a refusal scenario of the feature it guards. Merge them (mapping below).
- **M, tests that check a scenario carry no marker.** The project guideline asks for a marker
  beside each test. Examples: `test/core/state/navigationHistory.test.ts` lines 31, 42 and 62
  check TOOLBAR-065 (new place after Back, duplicate refused, leaving a place) and have no marker;
  only line 51 does. `test/page/modules/tocColumn.test.ts` lines 160, 203, 226, 305, 351, 388, 401
  and 415 check TOOLBAR-033/040/045 scenarios (saved state wins, No headings, click, folding,
  self-scroll, click after a patch, same text twice) and have no marker.
- **M, markers on CSS aggregates and file headers.** `pageChromeStyles.ts:2-3` and
  `propertiesStyles.ts:3-4` put TOOLBAR-129/130 above the imports (a file header).
  `pageChromeStyles.ts:146-151` (LIFE-049, TOOLBAR-001, TOOLBAR-025) and
  `contentLayoutStyles.ts:82-90` (TOOLBAR-003, -025, -037, -045, -133) put 5 to 11 markers of
  unrelated requirements on a single 450 to 600-line CSS constant. Fix: split the constant into
  named parts (for example `TOOLBAR_TOOLTIP_CSS` and `TOOLBAR_ROWS_MOTION_CSS`, the rules at
  `pageChromeStyles.ts:244-257` and `:508-530`) and mark each part.
- **M, markers on module installers.** `findBar.ts:113-118` (6 IDs), `headingFold.ts:49-52` (4),
  `tocColumn.ts:8-12` (5), `toolbarCollapse.ts:13-16` (4) mark the `install*` function of a module of
  160 to 690 lines. Precise targets are listed per StRS below.
- **M, draft requirements that are implemented and tested.** StRS TOOLBAR-002 and -003, and SwRS
  TOOLBAR-003, -004, -005, -006, -008, -009, -010, -011, -012, -014 are `draft`, yet all have
  implementation and test markers. They are candidates for `proposed`; the owner decides.
- **L, deprecated SwRS still listed.** 13 deprecated LIFE and 3 deprecated TOOLBAR SwRS keep
  `derives_from` on in-force StRS, so they still appear in those StRS's `derived_by` and in their
  Links block (for example LIFE-074, -081, -082, -089, -090, -091, -093 under LIFE-005). No
  deprecated SwRS is cited in a Main path.
- **L, honest verification notes.** Many SwRS already state their own gaps ("untested", "checked
  by reading"). They are the source of the "scenarios not checked" lists below.

## StRS-MDOKFSTUDIO-LIFE-001: Open previews beside the editor or as tabs

1. Relevance: a clear use case. **M**: Path 1 step 2 (LIFE-026, follow the active editor) repeats
   LIFE-003 Path 1, and the StRS derives LIFE-026, -032 and -049, which are LIFE-003 behaviours.
   Keep LIFE-001 for opening (side, Open With, coexistence, group lock, several previews) and drop
   LIFE-026/032/049 from its `derives_from` links (they stay derived by LIFE-003).
2. Split: LIFE-001, -003, -010, -018, -026, -032, -038, -049, -127, -149, -151, -156, -171.
   **M**: LIFE-010 (checks the file given) is the refusal side of LIFE-003, which already has a
   "No eligible file" refusal; merge LIFE-010 into LIFE-003. **L**: LIFE-171 (manifest declares
   Agents window support) is a scenario of LIFE-001 "Manifest contract"; merge. **L**: LIFE-156
   (settings groups) belongs to LIFE-021 only.
3. Markers: `activation.ts` carries 14 markers, each on its own registration (`:95`, `:97`,
   `:101`, `:212`, `:231`, `:282`, `:317`): correct. **L**: LIFE-149 is
   `annotation_exemption: true` ("absence of code") yet carries a marker at `activation.ts:231`
   (`createWebviewPanel`); keep one or the other. LIFE-171 has no marker, exempt (package.json): OK.
4. Tests: **M** LIFE-038: one assertion only (`serializer.test.ts:113`, two restored panels);
   "Two previews" and "Same document twice" are not checked. LIFE-010: well covered
   (`lifeReq.requirements.test.ts:257,275`, `lifecycle.test.ts:233`). LIFE-149: "Studio settings"
   checked by reading only. LIFE-151: complete (`groupFocus.test.ts`, `lifeReq...:397`, `realInput`).
5. Validation: yes, `test/integration/lifecycle.test.ts:43`, `stockCoexistence.test.ts:76`,
   `serializer.test.ts:29`, `realInput/markers.ts:56`. They mark a whole `run()`: acceptable for an
   e2e suite.
6. Diagram: use case. Actors: Writer, Reader, VS Code (built-in preview). Use cases: Open Preview to
   Side (command, Explorer, editor title, key), Open With tab, refused file (not saved .md), coexist
   with the built-in preview, several previews each with its own state.

## StRS-MDOKFSTUDIO-LIFE-003: Side preview follows the active file and refreshes on demand

1. Relevance: real. **M**: overlaps LIFE-001 (same Path 1) and LIFE-010 (it derives LIFE-100,
   -119, -125, scroll and reading state). Proposal: LIFE-003 = follow plus refresh plus title; drop
   the 3 scroll SwRS from it.
2. Split: LIFE-003, -024, -026, -032, -049, -100, -119, -125. LIFE-024 (title) and LIFE-026
   (follow) are good, observable SwRS.
3. Markers: **L**: LIFE-032 at `previewManager.ts:147` sits on the `get active()` getter; the
   behaviour is `activation.ts:101` (command), `pageInput.ts:48` and `viewState.ts:73` (button and
   message) and `previewManager.ts:675` (`prepareRefresh`). The getter is the "which preview"
   boundary only; acceptable, but a second marker on the same function is not needed.
4. Tests: **M** LIFE-024: the title after a switch is untested (its own note).
   **M** LIFE-026: the "Following the active Markdown editor." text and the came-back branch
   (`watchPageEditor`) are untested. **M** LIFE-032: the `previewRefresh` handler (current versus
   stale render) is untested; refresh with anchorLine and focus restore is only partly asserted
   (`runtimeScroll.test.ts:495`).
5. Validation: yes, `lifecycle.test.ts:44`.
6. Diagram: sequence. Writer, VS Code editor, Host (PreviewManager), Page. 1 active editor
   changes; 2 host checks eligibility; 3 newest following preview shows "Preview pending"; 4 render;
   5 title "Studio · file.md"; 6 Refresh command or button; 7 render from buffer; 8 page keeps the
   reading place.

## StRS-MDOKFSTUDIO-LIFE-005: The preview updates in place

1. Relevance: real and well written. **L**: the rationale is 11 bullets; the glow (3 bullets)
   could become one sentence.
2. Split: LIFE-004, -032, -039, -044, -049, -059, -069, -071, -094, -100. **M**: LIFE-004
   ("render in a worker thread that an abort stops") describes an architecture; reword it as
   observable ("a long render never blocks the editor; a superseded render stops"). **L**: LIFE-069
   has 12 scenarios, including internals ("What the key of a block holds", "The loaded page is not
   parsed again"); move them to verification notes. LIFE-032, -049, -059 and -100 also serve other
   StRS: drop LIFE-100 here (it is LIFE-010).
3. Markers: all on specific functions (`buildQueue.ts:180,317`, `renderPipeline.ts:275`,
   `contentPatch.ts:172,190`, `updatedRanges.ts:28,56`, `motion.ts:81`): good. **L**:
   `rendering.ts:469` and `:483` (LIFE-039) mark the hidden-panel deferral: OK.
4. Tests: **M** LIFE-039: "Source gone" is untested. **M** LIFE-044: settings scenarios untested at
   integration level, only the config read (`previewConfiguration.test.ts:76`). **M** LIFE-069: the
   `incrementalUpdates` off path is never exercised. **L** LIFE-004: idle stop untested. LIFE-071
   and LIFE-094: good coverage (`contentPatch.test.ts`, `previewTiming.test.ts`,
   `updatedRanges.test.ts`, `updateGlow.test.ts`).
5. Validation: yes, `dirtySnapshots.test.ts:67`, `updateGlow.test.ts:52`.
6. Diagram: sequence. Writer/Agent, VS Code document, Host (build queue), Render worker, Page.
   1 edit (or outside change); 2 debounce 40 ms; 3 render in worker (abort if superseded); 4 host
   plans a patch; 5a page applies the patch in place and glows outside changes / 5b shell change:
   new page document; 6 page reports ready (2 s timeout: full document).

## StRS-MDOKFSTUDIO-LIFE-007: The reader knows the render state and why a preview has no source

1. Relevance: real, concise.
2. Split: LIFE-018, -049, -055, -059, -062, -069, -127. **M**: LIFE-055 (page ignores an oversized
   pending notice) is a refusal scenario of LIFE-049 (pending notice), an instance of TRUST-059;
   merge. **L**: LIFE-018 and LIFE-069 belong to LIFE-001/LIFE-005; drop them here.
   **L**: Path 1's last state ("The status reads Preview ready") carries an Option bullet; the
   project rule says the last state has none.
3. Markers: **M**: LIFE-049 at `pageChromeStyles.ts:146` (CSS aggregate, see cross-cutting) and
   at `sessionFactory.ts:51` on `createSession` together with LIFE-038, TRUST-001 and TRUST-007:
   point LIFE-049 to `previewStatus.ts:27`, `statusRegion.ts:29` and `pageDocument.ts:44`, which
   it already has, and drop the `createSession` marker. LIFE-055 at `statusRegion.ts:30`: correct.
4. Tests: LIFE-055 fully checked (`page/lifeReq.requirements.test.ts:12`, 500/501 bound, malformed,
   hide). **L** LIFE-049: the exact pending message of a first Open With render is untested.
   LIFE-062: good (`lifeReq...:80`, `serializer.test.ts:82`).
5. Validation: yes, `lifecycle.test.ts:45`, `serializer.test.ts:30`.
6. Diagram: state. Pending → Ready; Ready → Pending notice (render over 1.5 s) → Ready; Ready →
   Failed (stale, last good page kept) → Recovered → Ready; any → Source missing (deleted, renamed,
   not Markdown, cannot restore) → Ready when the file comes back.

## StRS-MDOKFSTUDIO-LIFE-010: The panes scroll together and the reading position survives updates

1. Relevance: real. **L**: overlaps TOOLBAR-013 on the Anchor button (rationale bullet "The Anchor
   button ... overrides"); keep the button in TOOLBAR-013 only.
2. Split: LIFE-026, -069, -071, -097, -100, -108, -119, -125, -156. **M**: LIFE-097 ("Two settings
   decide how the panes follow each other") is a setting, which the guideline makes a scenario of
   the behaviour it drives: move its rows into LIFE-100 (preview follows the editor) and LIFE-108
   (editor follows the preview, double click). **L**: LIFE-026, -069, -071 and -156 are not this
   use case; drop them here.
3. Markers: good, on specific functions (`scrollCore.ts:85,349,498-499`, `scrollSync.ts:90,100,130,228`,
   `anchorPolicy.ts:76,192`, `html-sanitizer.ts:503` for "every mapped block carries its source
   mapping"). **L**: `scrollCore.ts:498-499` puts LIFE-097 and LIFE-100 on one handler, consistent
   with the merge above.
4. Tests: **M** LIFE-119: the host rule (stored anchor, then the editor's first visible line, then
   none) is untested. **M** LIFE-125: the field bounds of an invalid state report are untested.
   **M** LIFE-108: the accepted shape of `previewScroll`/`previewReveal` is untested.
   LIFE-100: 8 test locations, good.
5. Validation: yes, `scroll-sync-suite.ts:273`, `sourceMapping.test.ts:29`.
6. Diagram: sequence. Writer, Text editor, Host (scrollSync, EditorEchoGuard), Page. 1 editor
   scroll; 2 host posts the first visible line; 3 page scrolls to the line (anchor); 4 echo of its
   own reveal ignored; 5 reader scrolls or clicks the preview; 6 page posts the top line; 7 host
   reveals it in the editor; 8 after a patch the page restores the same anchor line.

## StRS-MDOKFSTUDIO-LIFE-014: Previews come back after a reload, remember recent documents, leave nothing behind

1. Relevance: real, but the title and normative text bundle three needs (restore after reload,
   per-document reading state, clean close) plus, in Path 2, workspace view choices. **M**: split
   in two StRS: "Previews come back after a reload at their place" (LIFE-127, -125, -038, -170)
   and "Closing a preview or folder leaves nothing behind" (LIFE-143). The view choices of Path 2
   overlap TOOLBAR-001 Path 1 (same LIFE-169/170 steps): keep them in one StRS only.
2. Split: FMSCHEMA-014, LIFE-002, -038, -071, -125, -127, -143, -169, -170, -172.
   **H**: LIFE-172 ("A document opens in preview mode and E switches to edit mode") is not a reload
   or memory behaviour; it belongs to the edit-mode use case (BLOCK-001). **M**: LIFE-002 ("A
   background failure is logged to the output channel") is a cross-cutting diagnostic, not a reload
   behaviour; derive it from LIFE-007 or keep it as an infrastructure SwRS with a stated reason.
   **L**: LIFE-071 belongs to LIFE-005.
3. Markers: LIFE-143 on 7 precise locations (`previewManager.ts:522,545,627`, `sharedWatchers.ts:29`,
   `diagnostics.ts:59`, `hostEvents.ts:368`, `activation.ts:154`): good. LIFE-127 at
   `previewState.ts:24` and `activation.ts:282`: good. **M**: LIFE-169/170 are marked in 13 files
   each; the per-page markers are right, but the header markers `tocColumn.ts:9-10` and
   `toolbarCollapse.ts:15-16` (install functions) should move to the line that posts the
   preference and the line that reads the initial value. **L**: LIFE-002 at
   `memoryLogger.ts:18` marks the in-memory test host's logger, not the product behaviour.
4. Tests: **M** LIFE-169: the stale-message drop and the palette mode in Restricted Mode are
   untested. **M** LIFE-127: "File outside a folder" untested. **L** LIFE-170: Cream for an unknown
   stored theme not asserted. LIFE-172: 5 tests in `runtimeOpenInPreview.test.ts`, complete.
5. Validation: yes, `reload-suite.ts:112`, `serializer.test.ts:28`, `workspaceDisposal.test.ts:28`.
6. Diagram: state of a preview panel: Open (live session) → Serialized (window reload) → Restored on
   its document at its place, or Source missing with a reason; Open → Closed (render aborted,
   watchers and Problems entries removed); Open → Folder removed (restricted reads) → Folder added
   back.

## StRS-MDOKFSTUDIO-LIFE-021: The settings editor lists the Studio settings in clear groups

1. Relevance: real but thin (one rationale bullet). **M**: Path 1 steps 2 and 3 cite LIFE-097 (scroll
   settings) and LIFE-069 (`incrementalUpdates`) and end on "The panes scroll together", which is
   not this use case. The Option "a description is at most 700 characters" is a build-time limit,
   not something the reader sees. Rewrite the path as "open settings → groups in fixed order → a
   default and a description per setting".
2. Split: LIFE-156 (the right SwRS), LIFE-069, LIFE-097. Drop LIFE-069 and LIFE-097. **L**:
   LIFE-156's scenarios "Boot context written by the host / read by the page" are internals.
3. Markers: LIFE-156 at `settingsRegistry.ts:351` (`SETTING_CATEGORIES`),
   `previewConfiguration.ts:49`, `bootContext.ts:8`: good.
4. Tests: LIFE-156 covered (`settingsRegistry.test.ts:36`, `package-contract.test.ts:39`,
   `bootContext.test.ts:12`, `pageSettings.test.ts:10`).
5. Validation: **none**. Candidate: `test/security/package-contract.test.ts:39` (it reads the
   contributed configuration of `package.json`) for the groups and their order; no integration test
   opens the settings editor.
6. Diagram: none needed; at most a 2-message sequence (Reader opens Settings → VS Code lists the
   contributed groups from `package.json`).

## StRS-MDOKFSTUDIO-TOOLBAR-001: The toolbar groups its controls, collapses and remembers view choices

1. Relevance: real. **M**: it mixes the toolbar (rows, collapse, motion) with the persistence of
   all view choices (LIFE-169/170), which is LIFE-014's Path 2. Keep only the toolbar-collapse
   choice here. **H**: TRUST-001 ("A document is editable whatever the trust") is derived from it,
   which is not a toolbar behaviour (the rationale bullet "Restricted Mode shows the same rows with
   Edit enabled" is what TRUST-006 covers).
2. Split: LIFE-169, -170, TOOLBAR-001, -007, -013, -129, -130, TRUST-001, -006.
   **M**: TOOLBAR-013 (host accepts only a known view preference with a valid value) duplicates
   LIFE-169's refusal scenario "The host refuses a value outside the table"; merge into LIFE-169.
   **L**: TOOLBAR-001 has 8 scenarios, one ("Table handle strip at the top of the page") is a
   table-editing geometry check; move it to the table-editing scope. **L**: TOOLBAR-130 holds two
   behaviours (rows unroll, load hint); acceptable.
3. Markers: **M**: TOOLBAR-129/130 at `pageChromeStyles.ts:2-3` and `propertiesStyles.ts:3-4`
   are file headers; move them to the tooltip keyframes (`pageChromeStyles.ts:508-530`) and the
   animating rows rule (`:244-257`). TOOLBAR-001 at `pageChromeStyles.ts:150` (CSS aggregate) and
   `previewToolbar.ts:33` (`renderPreviewToolbar`, right). **M**: `toolbarCollapse.ts:13-16`
   put TOOLBAR-007, -130, LIFE-169, -170 on `installToolbarCollapse`: move TOOLBAR-007 to `apply`
   (`:52`), TOOLBAR-130 to `markAnimating`/`startHint` (`:78`, `:114`). TOOLBAR-013 at
   `pageToHost.ts:51` (`VIEW_PREFERENCE_VALIDATORS`): right.
4. Tests: TOOLBAR-007: `runtimePageControls.test.ts:664` checks collapse, aria, root attribute,
   posted preference and saved state; Tab order checked by `capture_layout_checks.py:83`. Good.
   **M** TOOLBAR-001: the keyboard-focus tooltip is not measured; the 12/14 px offsets and the
   covering of scrolled text are untested; equality title = tooltip is checked for 3 buttons only
   (its own note). TOOLBAR-013: `pageToHost.test.ts:91`, all rows checked. TOOLBAR-129/130: CSS
   tests at `previewStyles.test.ts:1333,1353,1374` plus `toolbarCollapse.test.ts` (10 tests), good.
5. Validation: yes, `test/visual/scenarioAssertions.ts:720` (16 visual toolbar-row scenarios). It
   does not cover the remembered collapse across a reload; `reload-suite.ts:113` (LIFE-170) could
   also carry this StRS marker.
6. Diagram: state. Expanded ↔ Collapsed (chevron; rows 2-4 hidden and out of the Tab order);
   each change → stored for the workspace; new page → initial state from panel state, else workspace,
   else default (collapsed); fresh collapsed page → load hint unrolls once and rolls up.

## StRS-MDOKFSTUDIO-TOOLBAR-002 (draft): The reader folds and unfolds the sections

1. Relevance: real. **L**: body has a stray `## User Need` heading under "Preserved stakeholder
   intent" (same in TOOLBAR-003 and -014).
2. Split: TOOLBAR-003, -004, -005, -006, -008 (all draft). **M**: TOOLBAR-005 (Fold all and unfold
   all from the toolbar and the command palette) is the button/command form of the fold behaviour;
   per the guideline, merge into TOOLBAR-003. Others are distinct.
3. Markers: **M**: `headingFold.ts:49-52` puts TOOLBAR-003/004/005/006 on `installHeadingFold`.
   Move: 003 → `toggle` (`:190`) / `setToggle` (`:118`); 004 → `persist` (`:112`); 005 →
   `foldAll`/`unfoldAll` (`:198`, `:209`); 006 → `reveal` (`:258`). The other markers
   (`headingFold.ts` core `:25,63`, `scrollCore.ts:474,553`, `mappedBlocks.ts:63`) are right.
   `contentLayoutStyles.ts:82` (TOOLBAR-003) is in the CSS aggregate.
4. Tests: good unit coverage (`headingFold.test.ts` 8 tests, `core/state/headingFold.test.ts`,
   `mappedBlocks.test.ts:24,32`). **L** TOOLBAR-006: "The browser find opens the section" has no
   browser-level test.
5. Validation: **none**. Candidate: the fold scenario of `test/visual/capture_layout_checks.py:205`
   or an integration step (no integration suite folds a section today).
6. Diagram: state of a section: Open ↔ Folded (chevron); all ↔ (Fold all / Unfold all); Folded →
   Open when find or navigation targets a block inside; Folded state kept across patch and reload.

## StRS-MDOKFSTUDIO-TOOLBAR-003 (draft): The reader finds and replaces text in the preview

1. Relevance: real, concise.
2. Split: TOOLBAR-009, -010, -011, -012, -014, -131, -132 for three behaviours (open the bar,
   find, replace). **M** mapping: 132 (native editing keys in the fields) → 009; 011 (case, whole
   word, regex) → 010; 014 (replace unavailable with an open editor) and 131 (replace all
   announces skipped matches) → 012, whose boundary "Matches that do not map one-to-one" already
   covers skipped matches. Result: 3 SwRS.
3. Markers: **M**: `findBar.ts:113-118` puts 6 IDs on `installFindBar` (560 lines). Move: 010 →
   `paint`/`findMatches`/`move` (`:243`, `:275`, `:362`); 011 → `toggleOption` (`:375`); 012 →
   `runReplace` (`:423`); 014 → `updateReplaceState` (`:207`); 131 → `updateNote` and
   `scheduleDryRun` (`:192`, `:337`); 009 → the open/keydown handler. Core markers
   (`findMatches.ts:34,51,69`, `findReplace.ts:203`, `sourceEdits.ts:278-279`) are right.
4. Tests: rich (`findBar.test.ts` 20+, `findMatches.test.ts`, `findReplace.test.ts` 15,
   `findInPreview.test.ts:72-76`). **L**: host-side replace tests live in
   `test/session/reviewReqThreads.requirements.test.ts:117,128,148` (a review-scope file); move
   them to a find/replace test file.
5. Validation: **none**. Ready candidate: `test/integration/findInPreview.test.ts` (`run()` at
   `:77`, real VS Code window, find and replace).
6. Diagram: sequence. Reader, Page (find bar), Host. 1 Cmd/Ctrl+F; 2 bar opens, field focused; 3
   query → matches painted, count; 4 Enter walks matches (unfolds sections, scrolls tables); 5
   Replace all → page asks a dry run, note shows skipped count; 6 page posts `previewFindReplace`;
   7 host edits the source spans in one undo step (refused while a block editor is open); 8 answer
   with replaced/skipped counts.

## StRS-MDOKFSTUDIO-TOOLBAR-004: The reader always sees the section being read

1. Relevance: real, clear.
2. Split: TOOLBAR-002, -018, -022, -025, -030. **M**: TOOLBAR-022 (the depth setting) is the
   setting of TOOLBAR-018 (band shows the heading path); merge as scenarios. **L**: TOOLBAR-002 (the
   shadow) is part of the band's look; merge into TOOLBAR-025 or keep (small).
3. Markers: `stickyHeadings.ts:28,52,63,148-149`, `settingsRegistry.ts:136`, `pageSettings.ts:45`:
   right. **M**: TOOLBAR-025 at `contentLayoutStyles.ts:88` and `pageChromeStyles.ts:151` (CSS
   aggregates). **L**: TOOLBAR-022 at `contentPatch.ts:234` (`runtimeContextKey`) marks the
   "setting changed reloads the page" scenario: OK.
4. Tests: good (`toolbarReq.requirements.test.ts:166-212`, `runtimeScroll.test.ts`, visual).
   **L** TOOLBAR-030: "Scroll to the end" not measured separately.
5. Validation: yes, visual scenarios `scenarioDefinitions1.ts:1284`, `scenarioDefinitions2.ts:253,1064,1078,1092`.
6. Diagram: sequence. Reader, Page (scroll handler), Sticky band. 1 scroll; 2 find heading at the
   reading line and its parents up to the depth; 3 band shows them, one line each with ellipsis;
   4 shadow when text is under the band; 5 reading offset settles; 6 setting change → new page with
   the new depth.

## StRS-MDOKFSTUDIO-TOOLBAR-006: The reader uses a table of contents beside the document

1. Relevance: real. **L**: the user need is one 70-word sentence; split it.
2. Split: LIFE-169, -170, TOOLBAR-025, -033, -037, -040, -045, -133. **M**: TOOLBAR-133 (the
   narrow-pane rail keeps the text and Escape handlers clear) near-duplicates TOOLBAR-037's
   "Narrow pane rail and overlay"; merge into 037.
3. Markers: **M**: `tocColumn.ts:8-12` (5 IDs on `installTocColumn`); TOOLBAR-033 should move to
   `apply` (`:380`) and the toggle handler; LIFE-169/170 to the posting and initial-read lines.
   Specific markers `:74`, `:145`, `:193`, `:229` are right. `contentLayoutStyles.ts:89-90`: CSS
   aggregate.
4. Tests: **M**: several tests that check scenarios carry no marker (see cross-cutting; e.g.
   `tocColumn.test.ts:203` "No headings" for 040 refusal, `:226` click for 045, `:240` toggle opens
   the TOC marked only LIFE-169, not TOOLBAR-033). Coverage itself is good, plus visual
   `capture_toc_checks.py:33-36`, `capture_toc_rail.py`.
5. Validation: yes, `scenarioDefinitions2.ts:609` (visual).
6. Diagram: state. Closed ↔ Open column (wide pane) / Open rail (pane < 760 px, overlay on hover or
   focus); in Open: current entry follows the reading line; click → heading at the reading line;
   twisty folds a subtree; choice stored for the workspace.

## StRS-MDOKFSTUDIO-TOOLBAR-009: The reader goes Back and Next through followed links

1. Relevance: real, clear.
2. Split: BLOCK-205, TOOLBAR-054, -056, -058, -059, -065, TRUST-006. **M** mapping: 056 (history
   state of another render ignored) and 058 (host accepts only back or forward) → refusal
   scenarios of 054; 065 (last 50 places, no duplicates) → boundary scenarios of 059. Result: 054,
   059 (+ BLOCK-205, TRUST-006).
3. Markers: right (`history.ts:70,80`, `historyControls.ts:7`, `navigationHistory.ts:17`,
   `pageToHost.ts:251`). **L**: `hostToPage.ts:369-371` puts TOOLBAR-056, -122 and TRUST-059 on
   `createHostMessageFilter` (the shared filter): fine for the shared rule, another sign that 056
   and 122 are instances of TRUST-059.
4. Tests: **M** TOOLBAR-058: the render gate ("Another render") is untested. **M** TOOLBAR-065: 3 of
   4 scenarios are tested at `navigationHistory.test.ts:31,42,62` without a marker. TOOLBAR-056:
   only "another render" (`runtimePageControls.test.ts:740`); the nominal "current render" row is
   untested. TOOLBAR-054/059: good (`previewHistory.test.ts`, `toolbarReq.requirements.test.ts`).
5. Validation: yes, `previewHistory.test.ts:41`.
6. Diagram: sequence. Reader, Page, Host (history), VS Code. 1 reader types in a block editor and
   clicks a link; 2 page flushes the save; 3 host records the place and opens the target; 4 host
   posts `previewHistoryState` (canBack); 5 Back pressed → `previewHistoryGo back`; 6 host opens
   the stored document and selects the line, or scrolls the preview; 7 Next symmetric.

## StRS-MDOKFSTUDIO-TOOLBAR-011: Links open the right target, show where they lead, or are refused

1. Relevance: real. **L**: the user need is one 90-word sentence. **H**: the normative statement
   promises "never open a file outside the workspace unless the reader enabled the frontmatter
   outside-link setting", but the SwRS of that exception (FMSCHEMA-050/060/061/062/073/074/081
   mention it) are not derived from or linked to this StRS; either derive the relevant one or drop
   the clause.
2. Split: TOOLBAR-077, -079, -083, -085, -090, -094, -098, -102, -113, -117, TRUST-006, -007,
   -063, -065 (14). **M** mapping: 083 (bounded discovery messages) → 079; 113 (link message needs
   a request) → 077. **L**: TRUST-063 is also a gate instance (links targets array of the current
   render), owned by trust-security.
3. Markers: right and specific (`linkNavigation.ts:116,166,191,200`, `links.ts:70,81,195,214-217`,
   `previewNavigator.ts:66,150`, `previewNavigation.ts:27,110`, `resource-policy.ts:380`). **L**:
   `links.ts:27` marks TOOLBAR-079 on `DISCOVERY_EXCLUDE` (the search exclusions): OK for "Search by
   name".
4. Tests: **M** TOOLBAR-077: the auxclick button 2 refusal has no test; the warning text is not
   asserted. **M** TOOLBAR-094: the second-root relative case is untested. **L** TOOLBAR-090: the
   malformed-escape row is untested; one TOOLBAR-090 test sits in
   `test/core/preview/toolbarReq.requirements.test.ts:25` instead of the navigation tests.
   TOOLBAR-083: tested only by an oracle-equivalence test (`pageStateMessages.test.ts:227`) whose
   variants do include 65 requests and 4097 characters: acceptable.
5. Validation: yes, `previewHistory.test.ts:42` (same `run()` as TOOLBAR-009; it follows a
   relative link, an external link and a `javascript:` link).
6. Diagram: sequence. Reader, Page, Host (navigator), File system / OS. 1 link scrolls into view;
   2 page batches up to 64 requests; 3 host classifies (anchor, external, local, wikilink, blocked)
   and resolves inside the workspace; 4 page sets the tooltip or a warning icon; 5 click/Enter →
   `previewLink`; 6 host opens the file at the fragment line, hands an external URL to the OS, or
   warns with the reason.

## StRS-MDOKFSTUDIO-TOOLBAR-013: The reader decides how the panes scroll together and sees the cursor block

1. Relevance: real; overlaps LIFE-010 on the anchor mode (see LIFE-010).
2. Split: LIFE-169, -170, TOOLBAR-120, -122, -126, -128. **M** mapping: 122 (pairing message for
   another document ignored) and 126 (host accepts only a boolean anchor mode) → refusal scenarios
   of 120. **M**: Path 1 step 2 uses the validator TOOLBAR-126 as the transition to "The choice is
   kept for the panel"; the step that keeps the choice is LIFE-169 / `scrollSync.ts:70`.
3. Markers: right (`anchorMode.ts:60`, `scrollSync.ts:71,131`, `scrollCore.ts:157`,
   `pageToHost.ts:219`, `settingsRegistry.ts:172`, `previewStyles.ts:31`).
4. Tests: **L** TOOLBAR-120: the initial state is untested (its own note). TOOLBAR-122: only the
   foreign-document refusal; "Own document" not asserted at that marker. TOOLBAR-128: 10 test
   locations, good. TOOLBAR-126: oracle test only (`pageStateMessages.test.ts:228`).
5. Validation: yes, `scroll-sync-suite.ts:274`, `realInput/markers.ts:67`, visual
   `scenarioDefinitions1.ts:1298`, `scenarioDefinitions2.ts:1048`.
6. Diagram: sequence. Reader, Page (Anchor button), Host, Text editor. 1 host posts pairing (text
   editor shows the file? button enabled/disabled); 2 reader presses Anchor; 3 page posts
   `previewAnchorModeChanged`; 4 host stores the mode and aligns the preview to the editor's first
   visible line; 5 editor scroll or render → host posts the cursor line (setting on); 6 page
   outlines the block that holds it.

## StRS-MDOKFSTUDIO-TOOLBAR-014: A writer shares one page as a self-contained HTML file

1. Relevance: real, concise. **L**: stray `## User Need` heading; Path 1's last state ("The HTML
   file is written") carries a bullet and no final state follows.
2. Split: DIAG-128, FMSCHEMA-091, TOOLBAR-134, -135, -136, -137. Good: four distinct behaviours.
3. Markers: specific (`exportContent.ts:95,164,214,257`, `htmlExport.ts:38,44,52`,
   `exportSnapshot.ts:52,84,105`, `htmlExport` session `:74,87,105,139-140`). **H** (other scope):
   DIAG-128 (proposed, `annotation_exemption: false`) has **no** `@implements_req` anywhere, while
   tests mark it (`exportHtml.test.ts:48`, `exportSnapshot.test.ts:166-205`).
4. Tests: good on all four (`htmlExport.test.ts`, `exportSnapshot.test.ts`,
   `exportWhileEditing.test.ts`, `session/htmlExport.test.ts`, `exportHtml.test.ts`, visual).
5. Validation: **none**. Ready candidate: `test/integration/exportHtml.test.ts` (real host:
   command, warning, file with embedded image and diagram, cancel writes nothing).
6. Diagram: sequence. Writer, Page, Host, Save dialog, File. 1 Export button or command; 2 page
   waits for diagrams and takes a snapshot (sections unfolded, no comments or edit controls); 3
   host warns about links to other files (cancel stops); 4 save dialog (cancel stops); 5 host
   embeds styles, theme, width, images and math, no script; 6 one HTML file written.

## Orphan SwRS

- No in-force SwRS of these scopes lacks an in-force StRS parent.
- **L**: LIFE-173 ("Save key saves the previewed document") is in lifecycle-sync but derives only
  from StRS-BLOCK-008 (block editing). Markers (`blockEditor.ts:415`, `previewManager.ts:268`,
  `blockEdits.ts:599`, protocol entries) and tests (`saveCommand.test.ts`, `runtimeSaveKey.test.ts`,
  `saveKey.test.ts:64`) are good. Move it to the block-editing scope (new ID, supersede) or accept
  the scope mismatch.
- SwRS of these scopes that also derive from another scope's StRS (not orphans, noted only):
  LIFE-026 (TRUST-001), LIFE-062 (TRUST-004), LIFE-094 (CORE-001), LIFE-169/170 (BLOCK, LAYOUT,
  PALETTE, THEME, REVIEW), TOOLBAR-013 (THEME-011), TOOLBAR-113 (FMSCHEMA-014).

## Proposed restructure (Phase 6b, needs owner approval)

| Old | New | Why |
| --- | --- | --- |
| TOOLBAR-013 | LIFE-169 (refusal rows) | duplicate refusal |
| TOOLBAR-056, TOOLBAR-058 | TOOLBAR-054 (refusals) | gate instances |
| TOOLBAR-065 | TOOLBAR-059 (boundaries) | scenario of the history |
| TOOLBAR-083 | TOOLBAR-079 | gate instance |
| TOOLBAR-113 | TOOLBAR-077 | gate instance |
| TOOLBAR-122, TOOLBAR-126 | TOOLBAR-120 (refusals) | gate instances |
| TOOLBAR-133 | TOOLBAR-037 | near-duplicate |
| TOOLBAR-022 | TOOLBAR-018 | a setting is a scenario |
| TOOLBAR-002 | TOOLBAR-025 (optional) | look of the band |
| TOOLBAR-005 | TOOLBAR-003 | button/command of fold |
| TOOLBAR-011 | TOOLBAR-010 | options of find |
| TOOLBAR-132 | TOOLBAR-009 | keys of the bar |
| TOOLBAR-014, TOOLBAR-131 | TOOLBAR-012 | refusal and skipped count of replace |
| LIFE-010 | LIFE-003 | refusal of opening |
| LIFE-055 | LIFE-049 | gate instance |
| LIFE-097 | LIFE-100 + LIFE-108 | a setting is a scenario |
| LIFE-171 | LIFE-001 | manifest contract |

Effect: toolbar-navigation 50 → 34 in-force SwRS, lifecycle-sync 34 → 30. StRS: split LIFE-014 in
two; LIFE-021 path rewritten; derivations trimmed as listed per StRS.

## Counts by category

| Category | H | M | L | Examples |
| --- | --- | --- | --- | --- |
| StRS relevance, overlap, wording | 1 | 6 | 8 | TOOLBAR-011 clause without SwRS (H); LIFE-001/003, LIFE-014 bundle, LIFE-021 path (M) |
| Wrong derivation | 2 | 2 | 6 | LIFE-172 under LIFE-014, TRUST-001 under TOOLBAR-001 (H); LIFE-169/170 over-derived, LIFE-002 (M) |
| SwRS split (merge, setting, internals) | 0 | 18 | 4 | 17 old → new mappings above, LIFE-004 internal |
| Marker placement | 1 | 9 | 5 | DIAG-128 has no implementation marker (H); CSS aggregates, file headers, 4 installers (M) |
| Test gaps (scenarios not checked) | 0 | 17 | 8 | LIFE-038, -039, -044, -069, -119, -125, -127, -169; TOOLBAR-058, -077, -094, -001 |
| Tests without marker | 0 | 2 | 0 | navigationHistory (3 tests), tocColumn (8 tests) |
| StRS without validation test | 0 | 4 | 0 | LIFE-021, TOOLBAR-002, -003, -014 |
| Lifecycle (draft implemented, candidates for proposed) | 0 | 0 | 12 | StRS TOOLBAR-002/003, 10 TOOLBAR SwRS |
| Main-path rule | 0 | 2 | 2 | LIFE-021 and TOOLBAR-013 path steps (M); last state with a bullet in LIFE-007, TOOLBAR-014 (L) |
| **Total** | **4** | **60** | **45** | |

Validation tests: 12 of 16 StRS have one (LIFE-021, TOOLBAR-002, -003, -014 do not).
Diagrams proposed: 9 sequence, 5 state, 1 use case, 1 none.
