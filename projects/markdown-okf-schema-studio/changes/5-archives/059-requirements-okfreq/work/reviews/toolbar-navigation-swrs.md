Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.3 critic review: toolbar-navigation StRS and SwRS

Scope `toolbar-navigation`: 14 StRS, 133 SwRS (TOOLBAR), reviewed against `inventory/toolbar-navigation.md`,
the sources and tests of `markdown-okf-schema-studio-wt-059-b3`, and the defect classes of
`reviews/layout-width-swrs.md` and `reviews/frontmatter-editing-swrs.md`. Read-only review: no lint, no build,
no test run.

Verdict: REVISE

## What passed

- Structure: heading equals title in all 147 files (SwRS-130's title wraps over two YAML lines, same text);
  description equals the Normative behavior paragraph in all of them; exactly one SHALL each; no leftover
  placeholder; no backlog id, UX id or inventory id in a normative statement or scenario (only SwRS-005's
  Verification note, see defect 16). derived_by / derives_from are consistent in both directions.
- Coverage: F-TOOLBAR-001..054 are all mapped to at least one SwRS (the two sub-lines left over are in defect 19).
- Numbers and texts verified against the code: 13 / 12 buttons and 4-4-5 rows; 70..200 zoom, step 10; defaults
  (zoom 100, margin, toc off, incoming on, comments on, collapsed); depth default 3, range 1..6; toolbar width + 22;
  8 px column offset and 8 px band stop; 240 px column, 16 px gap, 256 px reserve, 760 px media rule; 3 passes;
  180 steps / 18 ms / 650 ms / 2 corrections / 2 px; 50 places; 64 requests of 4096 characters; 4 decode rounds;
  all warning and refusal texts of SwRS-075, 090, 092, 094..100, 109, 111; ANCHOR_PATTERN; fragment forms
  `#L`, `#^`, `(label)=`, `{#id}`, HTML id, slug, setext, fences, CRLF; marker identity rule.
- Known issues confirmed true: SwRS-006 (find widget enabled in `activation.ts`, no avoidance), 014 (only
  `console.error` in `workspaceChoices.ts:setViewPreference`), 041 (band selects h1..h6 of the whole document),
  043 (`aria-label` is `"Fold " + text` in both states), 075 (`history.go` moves the index and posts the state before
  `documents.open`), 087 (no CSS rule on `data-sphinx-preview-link-state`), 131 (`markSourceLine` takes the nearest
  first line), 119 with the reservations of defect 13. StRS-003, 004, 007, 011, 014 Known issues match.
- About 100 of 133 SwRS (75 percent) were read against source or tests; all 8 Known issues were checked. Note: the
  ids given in the brief (006, 015, 040, 043, 067, 092, 121, 133) do not match the files: the 8 Known issues sit in
  SwRS 006, 014, 041, 043, 075, 087, 119, 131; SwRS 015, 040, 067, 092, 121, 133 have none and none is missing there
  except as listed below.
- Test names cited exist: P8, T11, T13, T33, T34, T38, CR 025, `previewHistory.test.ts`, `tocColumn.test.ts`,
  `linkNavigation.test.ts`, `previewNavigator.test.ts`, `previewNavigation.test.ts` and the Python checks
  `check_preview_toolbar_rows`, `check_toolbar_collapse`, `check_fresh_workspace`, `check_tooltip_contrast`,
  `check_sticky_headings`, `stress_sticky_heading_scroll`, `check_toc_column`, `check_toc_shot`; scenario ids v01..v31.

## Defects (24)

1. StRS-TOOLBAR-011 ("never open a file outside the workspace"), SwRS-094, SwRS-095: overclaim. The opt-in setting
   `frontmatter.allowOutsideWorkspaceLinks` makes `links.ts:resolve` call `validateResolvedPreviewNavigation(...,
   allowOutsideRoot = true)` for a document-relative `okf-link:`, which opens a file outside every root
   (`test/session/previewNavigator.test.ts` "allows document-relative resolved targets outside a workspace root only
   in that mode"; SwRS-FMSCHEMA-062 and 081). Fix: StRS-011 "... and never open a file outside the workspace unless
   the reader enabled the frontmatter outside-link setting"; in 094 and 095 add "for a Markdown link" and one line
   citing SwRS-FMSCHEMA-081 for the exception.

2. SwRS-095, Verification notes: wrong evidence. The cited `previewEditing.test.ts` symlink case sends an
   `okf-link:` (`bundle_target`), which goes through `validateResolvedPreviewNavigation` and answers "outside the
   workspace"; the text "escapes the workspace" of this SwRS comes only from `validatePreviewNavigation` (Markdown
   relative link), which no test covers. Fix: "Method: Untested for a Markdown link; the integration test
   `previewEditing.test.ts` (bundle_target symlink) covers the frontmatter path (see FMSCHEMA-054)".

3. SwRS-058, Verification notes: "the current-render gate is covered by the page message gate tests" names a
   nonexistent test. `test/session/previewManager.test.ts` only asserts that each type has one registered handler;
   nothing tests `PAGE_MESSAGE_GATES` or `matchesCurrent`. Fix: "the render gate (`previewHistoryGo: render` in
   `pageMessages.ts`) is untested".

4. Untested claims that are in fact tested, and one reverse:
   - SwRS-006 "no unit test of the rule": `previewStyles.test.ts` lines 113 (z-index 1100) and 423 (position fixed).
     The 12 px / 14 px offsets are the untested part.
   - SwRS-028 / 038 / 039 "no unit test of the rule / of the number": `previewStyles.test.ts` "the TOC column is hidden
     by default, reserves 256px when open and hides on narrow panes" (line 815) asserts display none, the 760 px
     media block, 256 px, `position: fixed`, `inset-block-end: 16px`, `width: 240px` and the band `max-width`.
     Untested remain the exact 760 px boundary (038 scenario 2) and the widening (039 scenario 2).
   - SwRS-048 "the corner radius has a CSS rule and no test": test "T16b: only the current TOC entry loses its rounded
     corners" (line 867) asserts `border-radius: 0` and the 3 px bar.
   - SwRS-024 "no test sets this setting" and SwRS-128 "like the sticky depth": `contentPatch.test.ts` "T34: the
     runtime context key covers the startup settings" (line 180, cases `{ stickyHeadingDepth: 2 }` and
     `{ markEditorSelection: true }`) asserts that the key changes. Fix: cite T34 in both Verification notes; the
     full-page assignment itself stays untested.
   - Reverse, SwRS-003: the unit test counts 13 `data-tooltip` and compares three title/tooltip pairs; "equal to its
     title" for all 13 is not asserted. Say so.

5. SwRS-028 (and F-TOOLBAR-026 inventory text): the claimed visual check is vacuous for the band.
   `check_toc_column` measures `bandRight` after `scrollTo(0, 0)`; on `30-toc.md` the first heading is below the
   top, so `stickyHeadings.hidden` is true and `bandRight` is `null`, and the "band runs under the TOC column"
   assertion never runs (`check_toc_shot` does not test it either). Fix: Verification must say "band vs column
   overlap is asserted only by the CSS unit test (max-width); the visual check never shows a band".

6. SwRS-020, scenario 2 "Invisible heading ... left out of the band" is false for parent lines.
   `stickyHeadings.ts:measureHeadings` drops zero-height headings from `headingTops` (so they are never the active
   heading), but the parent loop in `updateStickyHeadings` walks `headingList`, which still holds them: a hidden
   shallower heading is written as a parent line. Fix: scenario 2 "a heading with zero height is never the current
   heading" and add "Known issue: a zero-height heading still appears as a parent line of the band".

7. SwRS-030: SHALL, scenario and test are inaccurate. `refreshReadingOffset` sets the offset to
   `max(depth x lineHeight + 5, largest band height at this width, visible band bottom)`; at depth 3 the first term
   already equals three lines, so scenario 1 ("stays at the three-line height") holds for that reason, not for the
   remembered height. The cited test "preserves preview scroll when layout changes during sticky heading
   activation" asserts that `scrollY` stays 50; it does not test grow-only. Fix: SHALL "... keep the reading offset
   at least as large as the depth allowance and the largest band height seen at that width"; scenario 1 at depth 6
   with a one-line band, or drop the claim; Verification "grow-only and reset are untested".

8. SwRS-040: "indented by their level" is wrong. `tocColumn.ts:rebuild` sets `--sphinx-preview-toc-depth =
   level - shallowest` (12 px per step in `contentLayoutStyles.ts`), so a document whose top heading is an h2 shows it
   at depth 0; headings with empty text are skipped, and only headings inside `#sphinx-myst-preview-content` count.
   The "Four levels" scenario hides this. Fix: "indented by their level below the shallowest listed heading",
   add a scenario "a document that starts at h2", mention the empty-text skip. Also split chip/glyph label rules
   (cf. SwRS-021) from the list rule.

9. SwRS-052, title and SHALL "Scroll tracking reads no layout": `track()` calls `keepVisible`, which reads
   `getBoundingClientRect` of the nav and the entry whenever the current entry changes. Only heading geometry is
   cached. Fix: title "Scroll tracking reads no heading geometry"; SHALL "... find the current entry from cached
   heading tops ...".

10. SwRS-061 and 131/132, missed behaviours (probable Known issue, verify by a test):
    - `scrollCore.ts:followSourceScroll` returns when `settings.scrollPreviewWithEditor` is false, so Back or Next
      within the same document (host posts `sourceScroll` with `line`, `history.ts:go`) does not scroll the preview
      when the Anchor button is off; the buttons still move the history. SwRS-061 states it always scrolls.
    - `markSourceLine(selectionLine ?? line)`: with `markEditorSelection` on, a `sourceScroll` that has only `line`
      (the Back case) moves the mark to the block at the stored line; SwRS-131 says "with a selection line".
    Fix: add a boundary scenario (Anchor off) to 061 with "Known issue: ... does not scroll", and mention the `line`
    fallback in 131 or 132.

11. SwRS-093 / 090 / 092: missed Known issue. `decodePath` decodes up to four times and rejects any malformed
    result, so a file whose name holds a literal percent sign is unreachable: `100%25.md` -> `100%.md` -> second
    round throws `URIError` -> "The navigation target could not be decoded safely."; `a%2541.md` is decoded to
    `aA.md`. Fix: add to 093 a scenario "a literal percent" and "Known issue: a path that decodes to a lone percent
    sign is refused as undecodable; a doubly encoded percent is decoded twice". Also the Verification "Untested
    directly" is true only for the five-round case; `%00` / `%5C` pass through the same function in
    `previewNavigation.test.ts`.

12. SwRS-098: the SHALL omits the sibling fallback and the precedence of `previewNavigator.resolvePreviewNavigation`:
    the name search runs first; the relative sibling (`local`) is used only when the search finds no candidate
    (test "discovers bare wikilinks before accepting an active-root sibling"). Also `path.extname` decides "has an
    extension", so `[[notes v1.2]]` gets no `.md`. Fix: second sentence "when no file is found by name and a file of
    that name sits next to the document, open that one", scenario for each, and the dotted-name boundary.

13. SwRS-119: Known issue and SHALL. (a) The pattern is `/%[da-f]{2}/iu` (case-insensitive; the host-side
    `decodePath` uses `[\da-f]`); the observable result of a leftover `%41` equals the undecodable case (no element,
    no scroll) except for an id that literally contains `%41`, so say that instead of implying a visible
    difference. (b) "cannot be decoded ... SHALL not scroll" is false when the message carries a `sourceLine` that
    maps to a block: `mappedTarget` wins and the page scrolls. Fix both sentences.

14. Duplicates of other scopes (cite by id, keep one owner):
    - SwRS-070, 071, 072 repeat SwRS-BLOCK-211 ("Following a link right after typing saves first"), 212 ("Back right
      after typing saves first") and SwRS-TABLE-030, with the same tests in `runtimeEditorFlush.test.ts`. Keep only
      the host half here (073 and 114) and the "no handler" default; reference BLOCK-211/212.
    - SwRS-010 scenario 2 repeats SwRS-LAYOUT-013 ("Collapsing the toolbar measures the clearance again"): delete it,
      cite LAYOUT-013.
    - SwRS-013, 014, 015, 016 repeat the zoom and width halves of SwRS-THEME-052 / 053 / 048 / 054 and LAYOUT-021
      (THEME-053 has the same 75/300/10/"wide" cases and the same unit tests). Fix: reduce 013 and 015 to the four
      booleans, the unknown-name refusal and the per-field default rule, and cite THEME-052/053, LAYOUT-021; make
      016 generic (cite THEME-054) or fold it.
    - SwRS-120..127 and 128..133 are inventoried a second time as F-LIFE-056, 057, 066, 068 in lifecycle-sync (the
      orchestrator must pick one owner; the button states 120, 121, 123 and the page marking 131..133 stay here, the
      host sync 127, 129, 130 and the settings 124, 128 move or cite). Not resolvable inside this scope; flagged.
    - SwRS-107, Verification: the cross-reference SwRS-FMSCHEMA-050 is the document-relative rule; the marker rules
      are FMSCHEMA-069 and 073. Also FMSCHEMA-069 says "the marker must start the line", while
      `markdownMarkerLine` accepts any whitespace before it (107's own scenario `# @implements_req ...`): a
      cross-scope contradiction to give to the FMSCHEMA critic.

15. Bundled SHALLs (more than one behaviour):
    - SwRS-010 and 035: keep state, post the preference, re-measure (three outcomes) -> split the re-measure.
    - SwRS-013: six preferences with six value rules; SwRS-015: zoom rounding plus five field defaults.
    - SwRS-026: alignment, 8 px stop before the toolbar, bottom border -> three.
    - SwRS-040: list, order, indent, glyph rule, chip rule.
    - SwRS-084: answer, stale drop and error warning (the SHALL names only the answer).
    - SwRS-092: five refusal classes with five reasons; SwRS-111: the blocked warning and the resolution-failure
      warning ("Resolution throws" scenario).
    - SwRS-127: configuration, loaded context and editor alignment; SwRS-133: outline and forced-colors outline;
      SwRS-003: attribute and visible tooltip; SwRS-125: two triggers.
    Fix: split at least 010/035, 026, 040, 084, 111, 127 into one SwRS each (new ids), or move the secondary outcome
    to its own scenario and out of the SHALL.

16. SwRS-004 and 005: test-harness wording and non-behaviour. "at any pane width, zoom, theme and collapse state of
    the visual scenarios" and "When the pointer rests ... in a visual scenario" make the SHALL depend on the test
    set; SwRS-005 scenario 2 "Hidden tooltip fails ... the scenario is reported as failed" and SwRS-032 scenario 2
    "Runaway fails" describe the harness, not the product; SwRS-005 Verification says "the inventory does not list
    it" (internal pointer). Fix: "When the toolbar is shown at any pane width from 360 px, at zoom 70 and 200, in
    every theme, collapsed or expanded, ...", "When the pointer rests on a toolbar button for 200 ms, the tooltip
    ...", replace the failure scenarios by a boundary (zoom limit disabled button; contrast exactly at 4.5), drop the
    inventory sentence.

17. SwRS-121 scenario 2 "Lost message" tests the host's answer to the ready report (lifecycle-sync, as the
    Verification notes admit). Remove it from this SwRS and cite the lifecycle-sync SwRS once it exists.

18. SwRS-051 scenario 2: pressing the button does not build the column "then"; `apply()` calls `refresh()`, so the
    column is built in the next animation frame. Fix wording ("in the next frame after it opens"). SwRS-010 / 035
    Criteria "callback called": the P8 test does not assert `onChange` (only the visual collapse check does);
    SwRS-035 does (`changes() === 1`). Fix 010's note.

19. Unmapped or unspecified inventory details: (a) F-TOOLBAR-020 note: the column is a `nav` named "Table of
    contents" (`aria-label`, C-CTL-041) - no SwRS (add to 033/036 or a small SwRS); (b) F-TOOLBAR-003: the initial
    Anchor state (`data-anchor-mode="off"`, `aria-pressed="false"`) is not specified (add to 120/123);
    (c) link hints are asked once per request and page (`discovered` is never cleared, `linkNavigation.ts`), so a
    target file created or deleted later keeps its stale tooltip until the page is replaced; add as Known issue to
    079 or 088; (d) the render gate on `previewViewPreferenceChanged` ("render" in `PAGE_MESSAGE_GATES`) drops stale
    preference messages but no TOOLBAR SwRS says so (THEME-054 scenario 2 does for zoom): add one scenario to 014.

20. SwRS-130 and StRS-014: the "no mark update on a cursor move" behaviour is inventoried as the open defect UX-47
    (F-LIFE-068 note, C-AR-103) but is written as plain behaviour. `package.json` documents it as intended, so
    either keep it as a rationale (current) or, if the backlog item is open, add "Known issue: the mark does not
    follow the cursor" to 130. Decide with the orchestrator; no backlog id in the text.

21. StRS-001: the rationale cites a code symbol (`renderPreviewToolbar` in `src/core/preview/previewToolbar.ts`) and
    StRS-005 / 013 give the setting ids; the guideline forbids implementation detail in StRS. Setting ids are
    user-facing and acceptable; remove the code path from StRS-001. Also StRS-008 "a wide pane" is undefined for a
    reader: say "a pane wide enough for the column" and keep 760 in the SwRS.

22. SwRS-009 scenario 2 ("Not a toolbar match") and SwRS-034 scenario 2 restate a CSS-selector trap and a start
    state; neither is a boundary of the behaviour. Replace 009 scenario 2 by "the attribute is written once at start
    and after every press".

23. SwRS-065 .. 068 title/SHALL vs scenario: SwRS-066 scenario 1 "history of three places at the second" and 065
    scenario 2 ("Exactly 50") are fine, but 065 SHALL says "more than 50 places are pushed" while a duplicate or a
    same-document `depart` does not push; add "distinct" or reference 067/068 so that the number of pushes is not
    read as the number of links.

24. SwRS-063 and 064 Verification say "no test"; correct, but 059 omits the lock condition: "records the place
    being left" applies only to a preview that follows the active editor (`links.ts:handleLink`). Fix: add
    "In a preview that follows the active editor" to 059's trigger and cite 063.

Count: 24 defects (3 false or wrong evidence statements, 2 overclaims of the requirement text, 4 missed or
misdescribed behaviours, 5 duplicate or ownership issues, remainder wording, bundling and traceability).

## Re-check

Scope `toolbar-navigation` after the analyst's revision: 14 StRS, 149 SwRS files of which 147 active (070 and 071
deprecated, ignored), checked read-only against `src/` and `test/` of
`markdown-okf-schema-studio-wt-059-b3`. Mechanical pass over all 163 files: derives_from / derived_by consistent in both
directions, no dangling id, heading equals title everywhere, description equals the Normative behavior paragraph,
one SHALL per StRS, no placeholder, no backlog id in normative text or scenarios (test titles in Verification notes such
as `P8` and `CR 025` are real test names).

Verdict: FIX-REQUIRED

### The 24 earlier defects

Verified fixed against code and tests: 1 (StRS-011, 094, 095 name the frontmatter opt-in and cite FMSCHEMA-081), 2, 3, 4,
5, 6 (020 scenario and Known issue true: `updateStickyHeadings` walks `headingList`, which still holds zero-height
headings), 7, 8 (`--sphinx-preview-toc-depth = level - shallowest`), 9, 10 (061 Known issue true: `followSourceScroll`
marks, then returns when `scrollPreviewWithEditor` is false), 11 (093 Known issue true: `100%25.md` throws in round 2,
`a%2541.md` becomes `aA.md`), 12 (content right, SHALL form not, see new defect 2), 13 (119 true: `/%[da-f]{2}/iu` in
`scrollCore.ts`, host side `[\da-f]`; `mappedTarget` wins), 15 (010/035, 026, 040, 084, 092, 111, 127, 133, 003, 125 split
into 134..149), 16, 17, 18, 19 (140, 123 initial scenario, 079 Known issue, 014 render gate scenario), 21, 22, 23, 24.
Partly fixed: 14 (duplicate 072 and its relative reference remain, new defect 3; 107 note, new defect 4), 15 (098, new
defect 2). Defect 20: see the decisions below.

The five new Known issues 061, 079, 093, 020, 119 are all true in code. Numbers, texts and cited tests of the revision
spot-checked again (reason texts of 090..096, 143..146, fragment forms, 64 / 4096 / 50 / 240 / 256 / 760, 12 / 14 px
offsets): all match, every cited test title exists.

### Decisions on the open points

- Defect 20 (editor-selection mark does not follow the cursor, SwRS-130): not a defect of the requirement. The setting
  text in `package.json` and `settingsRegistry.ts` states "refreshed when the editor scrolls or the preview re-renders,
  not on every cursor move" (the fix of UX-47 was to correct the setting wording, commit ce518bd), `activation.ts`
  subscribes only to visible-range changes, and 130 plus StRS-014 describe exactly that. Keep it as stated behaviour with
  the rationale line; no Known issue needed (it would contradict the documented contract). The real Known issue of the
  mark (nearest first line, not the containing block) is already in 131.
- FMSCHEMA-069 "marker must start the line": no contradiction any more. FMSCHEMA-069 now reads "The marker must start the
  line or follow whitespace", which is what `markdownMarkerLine` does (`(?:^|\s)marker\s+identity`, one function shared by
  the line label and the navigation). The wrong text is now TOOLBAR-107's Verification note that still repeats the old
  claim (defect 4). Nothing to change in the frontmatter-schema scope.
- TOOLBAR-062/063/064 vs BLOCK / TABLE ids: no BLOCK, TABLE, FMSCHEMA or other SwRS cites 062, 063 or 064, and they do not
  overlap any of them (BLOCK-211/212 and TABLE-030 are the page-side flush; 062..064 are what the host records in the
  history). Only cross-scope links into this scope are THEME-014, 048 -> TOOLBAR-013, 014, 015. Cross-scope note for
  theme-zoom, not counted here: THEME-048 says "Normalisation of a stored zoom is SwRS-TOOLBAR-015" and "storage and
  validation: TOOLBAR-013 and 014", but 013 and 015 now leave zoom to THEME-052 / 053; reword THEME-048 to cite THEME-052
  and 053 for the zoom rules and TOOLBAR-014 for the storage only.

### Defects (6)

1. SwRS-MDOKFSTUDIO-TOOLBAR-148 (title, SHALL, both scenarios): wrong direction. `ScrollSyncController` on
   `previewAnchorModeChanged` with the mode on calls `syncEditorToPreview(undefined)` (`src/session/features/scrollSync.ts`
   lines 60-74); that method reads each visible editor's `firstVisibleLine` and posts `sourceScroll { line, selectionLine }`
   to the preview (lines 117-147, doc comment "The editor's first visible line moves the pages of its document"). No text
   editor is ever scrolled. Fix: title "Turning the anchor mode on aligns the preview with the text editor"; SHALL "When the
   host receives previewAnchorModeChanged with the mode on, the extension SHALL post to the preview the first visible
   line of each visible text editor that shows its document"; scenario 1 "THEN the preview receives a sourceScroll with
   the editor's first visible line and scrolls there (the page follows the editor now)"; scenario 2 "THEN no sourceScroll
   is posted"; Criteria "syncEditorToPreview runs for the mode on only"; keep "Untested". Also fix the StRS-013
   derivation text if it implies the editor moves (it does not).

2. SwRS-MDOKFSTUDIO-TOOLBAR-098 (SHALL and description): two SHALLs ("... SHALL search ...; when none is found ..., it SHALL
   open that one") and two behaviours. Fix to one SHALL, same content: "... the extension SHALL search every workspace
   root for that name, with .md added when the name has no extension, and open the file when exactly one matches, or the
   file of that name next to the document when none is found." Update the YAML description to the same text.

3. SwRS-MDOKFSTUDIO-TOOLBAR-072, 114 and 059: relative references to a requirement that no longer exists, and a surviving
   duplicate. 072 scenario 2 "THEN the editor is saved first (see the file link requirement)" and 114 Verification "(see
   the file link requirement)" point to deprecated 071; 059 Verification "see the locked preview requirement" names 063
   only by description. 072 itself repeats SwRS-BLOCK-211 scenario "Anchor link" and TABLE-030 scenario "Anchor inside
   the page" (same behaviour, same test `CR 025: an anchor link inside the page keeps the open editor`), the duplicate
   class of defect 14 that was handled for 070 and 071 only. Fix: deprecate 072 like 070 / 071 (BLOCK-211 owns it);
   in 114 write "(page half: SwRS-MDOKFSTUDIO-BLOCK-211 and SwRS-MDOKFSTUDIO-TABLE-030)" without the sentence about the file
   link requirement; in 059 replace "see the locked preview requirement" by "see SwRS-MDOKFSTUDIO-TOOLBAR-063"; in StRS-010
   add to the rationale "The page half is specified in the block-editing and table-editing scopes
   (SwRS-MDOKFSTUDIO-BLOCK-211, 212, SwRS-MDOKFSTUDIO-TABLE-030)" and drop 072 from its derived_by (and 070, 071 if the
   lint allows deprecated ids out of derived_by) and from 072's derives_from.

4. SwRS-MDOKFSTUDIO-TOOLBAR-107, Verification notes, last sentence: false. "The marker rule accepts any whitespace before
   the marker, while SwRS-MDOKFSTUDIO-FMSCHEMA-069 says the marker must start the line" no longer holds: FMSCHEMA-069 Criteria
   now say "The marker must start the line or follow whitespace", the same rule as `markdownMarkerLine`. Fix: delete the
   sentence; keep the cross-reference "marker annotations: SwRS-MDOKFSTUDIO-FMSCHEMA-069 and 073".

5. SwRS-MDOKFSTUDIO-TOOLBAR-101, Verification notes: wrong evidence. The cited test "discovers wikilinks on demand and
   refuses ambiguous or escaping targets" counts calls of the `discover` callback of the navigator (1, then 2 after a name
   with a folder skipped it); it does not test that two requests in flight share one search, which is the
   `discoveries` map of `LinkController.resolve` (`src/session/features/links.ts` lines 165-177) and has no test
   (`test/session/links.test.ts` holds one unrelated frontmatter case). Fix: "Method: Untested: the sharing of one running
   search per name is in LinkController.resolve and no test starts two requests together; the navigator test only shows
   that a name with a folder part runs no search."

6. SwRS-MDOKFSTUDIO-TOOLBAR-010 and 035, title and Criteria: the titles still promise a behaviour the SHALL no longer states.
   010 "Pressing the chevron saves the choice and re-measures" and 035 "Pressing the button saves the choice and re-measures
   the layout" were split (the re-measure is LAYOUT-013 / TOOLBAR-138) but the SHALL only keeps the state and posts the
   preference; 035 Criteria still end with "callback called", which 138 owns. Fix: titles "Pressing the chevron saves the
   choice" and "Pressing the Table of contents button saves the choice" (change the `## ` heading with them); 035 Criteria
   "state saved, one message posted".

Count: 6 defects (1 wrong behaviour, 1 bundled SHALL, 1 relative reference plus surviving duplicate, 1 stale cross-scope
statement, 1 wrong test evidence, 1 title / SHALL mismatch).
