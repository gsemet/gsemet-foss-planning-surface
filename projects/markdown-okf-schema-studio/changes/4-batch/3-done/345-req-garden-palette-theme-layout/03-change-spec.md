# Change specification: garden the requirements of palette-slash, theme-zoom and layout-width

## Goal

A human reviewer understands the palette, slash menu, theme, zoom and column-width use cases by
reading their StRS alone. Each SwRS is one observable behaviour. Each SwRS is traced by markers on
the code that does it and on the tests that check its scenarios. Each StRS has a validation test
on a real scenario and a use-case diagram.

This CR changes requirement text, markers and tests. It changes no product behaviour.

Source: the read-only audit of CR `requirements-gardening`, `evidence/audit-palette-theme-layout.md`
(at `main` dedbdb2a), and `evidence/audit-synthesis.md`. The `file:line` references below were
checked at dedbdb2a. If a line has moved, find the code by the symbol named next to it.

## Rules and decisions this specification carries

- Project rules: `.agents/constitution.md` (section 1, requirements anchored to the code),
  `requirements/guidelines/requirements.guidelines.md` and
  `requirements/guidelines/project.guidelines.md` ("Main paths of a StRS", "During a change",
  "Approved requirements"). Run okfreq as `uv run --no-sync --group requirements okfreq`.
- Owner, 2026-11-17: **published requirements are never deleted.** A merge or split uses
  `okfreq supersede OLD NEW [NEW...] --path requirements --yes` (or `okfreq archive`). There is
  no `git rm`, no `okfreq retire` and no `retired_ids` change.
- Owner, 2026-11-17: these decisions stay with the owner, and the Driver brings them back:
  1. the re-approval of any approved StRS whose text changes;
  2. any `draft` -> `proposed` change (none is in scope: every StRS and SwRS here is
     `proposed` or `approved`);
  3. a merge or split proposed below that the Driver doubts once it reads the code.

  Ask the owner. Never decide one of these alone.
- Owner, 2026-11-17: the work runs without an owner review of this specification, and there is
  no spec critic.
- Tests added for scenarios no test checks today must pass on today's code. Sometimes such a test
  shows that the code does not do what the SwRS says. In that case, write the SwRS as the code
  behaves, add a line "Known issue: …", and report the bug for the backlog. Do not fix the code in
  this CR (constitution, section 1).
- New requirements are created with `okfreq new … --lifecycle proposed`, never `draft`.
- Approved StRS in scope: **StRS-LAYOUT-001, StRS-LAYOUT-003 and StRS-PALETTE-015.** No SwRS in
  scope is approved. See section 9 for how each approved StRS is handled.

## Prerequisites

- Sibling CRs **req-use-case-diagrams** and **req-marker-gate** have merged (`depends.json`). This
  CR uses the rules they add:
  - **Diagram section.** A StRS can carry an authored `### Use case diagram` section. It holds
    one Mermaid fence (sequence by default, an actors diagram when several roles take part, a
    state diagram for a mode) and sits before `### Main paths`.
  - **Marker gate.** A marker comment names at most 3 IDs. A companion file names, for each ID,
    the scenario that checks it. A ratchet baseline lists today's offenders and can only shrink.
- This CR removes from that baseline every entry it fixes. Use the file and format that
  req-marker-gate defines.
- In the worktree, run `just dev` first (`.agents/guidelines/local-worktree.guidelines.md`).

## What changes

The scope is 13 in-force StRS: LAYOUT-001, 003, 004; PALETTE-001, 002, 005, 007, 013, 015, 018;
THEME-002, 004, 011. They derive 93 in-force SwRS in these three scopes, plus the cross-scope
SwRS named below. All IDs are `SwRS-MDOKFSTUDIO-…` / `StRS-MDOKFSTUDIO-…`. The prefix is omitted
below.

### 1. StRS text

Fix the text where it contradicts its SwRS or the code. Keep the reader-level promise in the StRS
and leave numbers to the SwRS.

- **PALETTE-001** is superseded (see 2). Its stale rationale goes with it: it says the documented
  shortcuts are bold, italic, link and TODO comment, but SwRS-PALETTE-086 is deprecated and
  SwRS-PALETTE-266 says Cmd/Ctrl+/ toggles a plain HTML comment.
- **PALETTE-002:** name the four modes (Strict, GFM, MyST, Full) and say that the sets are nested,
  each containing the one before.
- **PALETTE-005:** keep the three ideas (in reach, soft, never closes by accident) and make the
  title and normative text read as one use case.
- **PALETTE-018:** add two things to the normative text:
  - files dropped from the Explorer (SwRS-PALETTE-004);
  - a pasted URL becoming a link, autolink or image (SwRS-PALETTE-264).

  Remove the self-referential first rationale bullet ("belong to the palette and paste use
  cases").
- **LAYOUT-004:** remove the history: "Earlier values (56 px…, 24 px…) are superseded" and the
  CHANGELOG known issue.
- **THEME-002:** remove the internal rationale bullet "this scope records the reduced-motion
  preference on the page".
- **LAYOUT-001 (approved)**, proposed text: remove the maintainer half of the user need ("As a
  maintainer, I can run machine layout checks", inherited from the superseded LAYOUT-009). It is
  test tooling. Owner re-approval is needed (section 9).
- **LAYOUT-003 (approved)**, proposed text: trim the 16 rationale bullets (12 KB) to the
  reader-level promises. Leave the numbers to the SwRS (16 px gutter, 256 px TOC, rounding up,
  1 px tolerance). Owner re-approval is needed (section 9).

### 2. New StRS: split the PALETTE-001 umbrella

Create three StRS with `okfreq new` (scope `palette-slash`, `--lifecycle proposed`), then run
`okfreq supersede StRS-MDOKFSTUDIO-PALETTE-001 <A> <B> <C> --path requirements --yes`.

**StRS A, "A writer formats text with buttons and shortcuts":** 039, 043, 045, 048, 049, 050,
052, 053, 083, 266, 003, and 002 (edit bar tooltips).

- Main path: take the current PALETTE-001 Path 1, "Bold a word, then take it back", with each
  cited ID updated to its merged ID from section 4.

**StRS B, "A writer inserts GitHub Flavored Markdown constructs":** 115, 123, 124, 125, 126,
267, and 269 (alert part).

**StRS C, "A writer inserts MyST constructs":** 127, 132, 133, 135, 136, 138, 270, 271, 272, 265,
273, 274, and 269 (admonition part). 130 and 137 are merged into 127 (section 4).

The other SwRS that derive from PALETTE-001 today:

- **Drop PALETTE-001 from `derives_from`,** because another StRS already owns them: 004, 021, 054,
  058, 072, 089, 092, 109, 150, 153, 160, 213, 238, 242, 263, 264.
- **The current PALETTE-001 Path 2, "Write a link"** (089, 092), moves to StRS-PALETTE-007 as a
  path, if PALETTE-007 has fewer than two paths. Otherwise it is dropped.
- **SwRS-PALETTE-001** (mode table) derives from StRS-PALETTE-002 only.
- **SwRS-PALETTE-275** derives from StRS-PALETTE-015. See section 4 for its wording.
- **SwRS-PALETTE-114** (Thread) leaves the palette use cases. Its proposed parent is
  StRS-REVIEW-015, "A writer keeps a discussion in the Markdown source…". REVIEW-015 is approved,
  so see open question 3.
- **TABLE-111** (column alignment) keeps only StRS-TABLE-012.

Name each new StRS in reader terms. Give it a `--description` SHALL statement and a `--user-need`.
Write the normative behavior, user need and rationale sections.

### 3. Reparenting

A shared rule is cited with `depends_on` on the SwRS that uses it. It is not derived. Each SwRS
derives from the use case it serves. `derives_from`, `depends_on` and `relates_to` are authored on
the child SwRS. `derived_by` is generated, so never edit it.

| SwRS | Change |
| --- | --- |
| PALETTE-115 (Alert) | drop StRS-PALETTE-005; it derives from StRS B |
| TRUST-001 | drop StRS-PALETTE-002; add `relates_to: StRS-PALETTE-002` only if the Driver sees a real link, otherwise nothing |
| TRUST-005, TRUST-065 | drop StRS-PALETTE-007 and StRS-PALETTE-013; the palette SwRS that post messages to the host cite them in `depends_on` (PALETTE-010 already does) |
| TRUST-006 | drop StRS-THEME-011 |
| CORE-028 (typography) | drop StRS-THEME-002 |
| TABLE-085 (table bar cell group) | drop StRS-PALETTE-015 |
| TABLE-111 | drop StRS-PALETTE-001 (done by section 2) |
| LAYOUT-022 | add `depends_on: SwRS-LAYOUT-032` and remove its own "Wide table in Margin" scenario text that repeats 032 |
| THEME-001 | its refusal table for an unknown mode at boot repeats LIFE-170: replace it with `depends_on: SwRS-LIFE-170` |
| 192, 196, 203 | keep them under PALETTE-007 / PALETTE-018 only: drop StRS-PALETTE-013 |

- **Keep LIFE-169 and LIFE-170 derived by LAYOUT-003, PALETTE-002, THEME-004 and THEME-011.** Each
  of these StRS cites them in its `### Main paths`. `scripts/check_main_paths.py` requires that a
  cited SwRS derives from the StRS. Keeping the choice is part of each of these use cases (see
  open question 2).
- **Keep CORE-050 under PALETTE-005 and THEME-002, and BLOCK-047 under PALETTE-005,** for the same
  reason.
- **After each removal, check that no SwRS is left without a `derives_from`.** `just
  requirements-lint` reports orphans.

### 4. SwRS merges and splits

Make the new SwRS with `okfreq new --lifecycle proposed --derives-from …`. Write their scenarios
from the old SwRS, without losing any scenario, refusal or boundary. Then supersede each old SwRS
into the new one. When a target already exists, extend its text with the scenarios it takes over.

| Old | New | How |
| --- | --- | --- |
| 045, 048, 135, 138, 126 | new SwRS "Inline marker buttons toggle their markers around the selection" (one scenario table: Bold/Italic `*`, Strikethrough `~~`, Subscript/Superscript role, Key MyST role, Key `<kbd>`); derives from A, B, C | supersede each into the new ID |
| 049, 052, 053, 123, 267 | new SwRS "Line-prefix buttons toggle their prefix on the touched lines" (quote, bullet, number, checkbox, option); derives from A, B | supersede each into the new ID |
| 130, 137 | 127 (Admonition), which gains the Custom and Dropdown scenarios | supersede into 127 |
| 265, 273, 274 | mode-membership refusals become rows of the SwRS-PALETTE-001 table; the insertion scenarios go to a new SwRS "Starter blocks insert a chart, a diagram or content tabs" (derives from C) | supersede each into 001 + the new ID |
| 268 | 238 gets the scenario "MyST admonitions are listed with their icons" | supersede into 238 |
| PALETTE-010 | LIFE-169 (its Palette mode row already says "Dropped unless the mode is one of the four") | supersede into LIFE-169 |
| THEME-013 | LIFE-169 (Theme row) | supersede into LIFE-169 |
| LAYOUT-018 | 011 gets the scenario "the clearance follows layout changes (resize, font, collapse, width mode)"; the burst limit (200 updates per second, one trailing timer) becomes a verification note of 011; the `describe()` diagnostic and the CI run number are dropped | supersede into 011 |
| PALETTE-021 | stays "palette docked above the editor, sticky over a tall editor"; new SwRS "The page does not follow an editor scroll caused by an edit" (derives from PALETTE-005) takes the scroll-sync scenario | split: 021 is edited, the new ID is added |
| PALETTE-002 | 002 keeps "every edit bar button shows its title and shortcut in the slide-in tooltip"; new SwRS for the rule button icon (derives from A) | split: 002 is edited, the new ID is added |

Edits made in place, with no new ID:

- **LAYOUT-023 / LAYOUT-044:**
  - LAYOUT-023 keeps Auto breakout of figures, images, code and Mermaid, plus the re-measure.
  - Its table scenarios move to 044: uncapped and rounded up, row handles, cell editor.
  - "Several triggers in one frame" becomes a verification note.
- **LAYOUT-001 / LAYOUT-032:**
  - LAYOUT-001 keeps "no page-level sideways scroll" and "long words and URLs wrap".
  - Remove its "Narrow table and long words" duplicate. LAYOUT-032 owns the table scroll box,
    shaded edges and short identifiers.
  - Remove the "(boundary): Machine geometry checks" scenario. The four checks of
    `test/page/geometryChecks.test.ts` stay as test infrastructure.
- **THEME-034:** reword it to its observable part: "a host colour that is set is used; an unset
  one keeps the fallback".
- **PALETTE-275:** reword it in user terms: "every syntax the preview renders can be inserted
  from the slash menu, except the documented exceptions". It keeps its test
  (`test/page/slashSyntaxCoverage.test.ts:123`).

Markers that cite a superseded ID move to the new ID in the same commit. Do not leave markers on
superseded IDs. For example, `test/integration/paletteMode.test.ts:41` marks PALETTE-010, and
LIFE-169 is already marked there.

### 5. Implementation markers

Move each marker to the declaration or rule that does the behaviour, with at most 3 IDs per
comment.

- `src/page/modules/editPalette.ts:23-39`, a 17-ID header (001, 002, 017, 031, 036, 039, 069, 078,
  083, 109, 115, 148, 150, 238, 242, 269, LIFE-169): move each ID to its builder or handler in that
  file. Drop an ID whose code already carries a correct marker elsewhere.
- `src/core/palette/paletteActions.ts:209-211` (001, 263, 275 on `PALETTE_ACTIONS`): put 263 on
  the `aliases` entries, 001 on the mode membership and 275 on the slash-entry data.
- `src/page/features/blockSourceEditor.ts:44-51`, an 8-ID cluster (001, 021): spread the IDs to
  their functions. `:332` (031) and `:361` (017) are correct.
- `src/core/preview/styles/pageChromeStyles.ts`:
  - 002, on the import line at `:1`: move it to the tooltip rule.
  - LAYOUT-002, in the cluster at `:145-151`: move it to the `--sphinx-preview-content-max-width`
    rule at `:164`.
  - THEME-031, in the cluster at `:148`: move it to the Cream block of `FORCED_THEME_MODES_CSS`
    at `:7`.
  - THEME-043, in the cluster at `:149`: move it to the zoom rules at `:168`.
- `src/core/preview/styles/contentLayoutStyles.ts:80-90`, an 11-ID cluster on
  `CONTENT_LAYOUT_CSS`:
  - LAYOUT-001: move it to the wrapping rules (`:314`, `:407`, and `contentBlockStyles.ts:161`).
  - LAYOUT-022: move it to the Margin and Full width rules.
  - THEME-001 at `:87`: drop it. `themeMode.ts:88` is correct.
- `src/core/preview/styles/tableStyles.ts:1-3`: move LAYOUT-032 to the scroll-box /
  overflow-shadow rule.
- `src/core/preview/styles/contentBlockStyles.ts:6-19`: drop the LAYOUT-043 marker at `:19`. It is
  redundant with `contentLayoutStyles.ts:41` (`TOOLBAR_FLOAT_CSS`).
- `src/core/preview/styles/propertiesStyles.ts:1`: move CORE-050 to the reduced-motion `@media`
  rule at `:535`.
- `src/page/modules/editPalettePopovers.ts:397` (`buildColor`): move 036 to the mousedown-cancel
  point. `linkPanel.ts:39` is already correct.
- `src/page/features/blockEditor.ts:41` (`closeBlockEdit`, a generic helper): move 089 to the link
  panel's own close or commit path.
- `src/page/runtime.ts:283` and `src/page/features/firstClearance.ts:308` (LAYOUT-018): change the
  ID to LAYOUT-011 (section 4).
- New SwRS of section 4: mark the code of each one. The old per-action markers in
  `blockEditActions.ts` and `inlineEditActions.ts` change to the merged ID, one per action
  function.

Generated CSS strings cannot hold markers: put the marker on the line before the constant or rule
block.

### 6. Test markers

Put each marker next to the test that checks the scenario.

- **`test/page/modules/editActions.test.ts:9-48`,** a header of 40 `@tests_req` lines. It is the
  only test link of 045, 048, 049, 050, 114, 123, 124, 125, 127, 130, 132, 133, 135, 136, 137,
  138, 147 and 149. Move each marker, with merged IDs from section 4, to its test:

  | Test | Line |
  | --- | --- |
  | strikethrough | `:325` |
  | quote | `:346` |
  | rule | `:383` |
  | checkbox | `:711-749` |
  | details | `:847` |
  | footnote | `:859` |
  | kbd | `:913` |
  | admonition | `:943-972` |
  | custom | `:977` |
  | deflist | `:986` |
  | math | `:995` |
  | sub/sup | `:1009` |
  | label | `:1017` |
  | ref (147) | `:1039` |
  | cite (149) | `:1055` |
  | dropdown | `:1062` |
  | roleKbd | `:1095` |
  | thread (114) | `:1381` |

  Mark the 092 safety cases at `:519-542`. IDs of other scopes in that header are moved by their
  own req-garden CR. If they are still there when this CR lands, leave them.
- **PALETTE-264:** remove the marker from `test/build/integrationEditModeRestore.test.ts:10`, a meta
  test about edit-mode restore. Mark `test/page/…/pasteUrl.test.ts:12-69` (unit) and
  `test/integration/pasteUrl.test.ts:59`.
- **PALETTE-001:** remove the marker from `test/security/package-contract.test.ts:40`. Fix the test
  title at `test/…/paletteReq.requirements.test.ts:155`: it says "outside the three modes", and
  there are four.
- **THEME-016:** remove the marker from `test/core/state/editLock.test.ts:24`, a generic EditLock
  test. It is replaced by the new tests in section 8.
- **PALETTE-240:** mark `test/page/slashMenu.test.ts:762` (MyST wins a near tie) and `:783` (a loose
  best match leaves Enter and Tab).
- **PALETTE-256:** mark each test of its 6 scenarios in `slashMenu.test.ts` (one is marked today
  at `:680`). A scenario with no test goes to section 8.
- **`test/integration/realInput/markers.ts`:** remove the IDs of these scopes. Today these are
  StRS-PALETTE-001, 005, 007 and 015, StRS-THEME-002, and the SwRS of these scopes listed there.
  Each ID goes on its scenario function (section 7), or is kept in the companion format that
  req-marker-gate defines (ID and scenario name).
- Remove the fixed offenders from the marker-gate baseline.

### 7. StRS validation tests

Each StRS gets a `@tests_req StRS-…` on a real end-to-end scenario that walks its main path.

| StRS | Marker goes on |
| --- | --- |
| A (formatting) | `scenarioPalette`, `test/integration/realInput/textEditing.ts:612` (Bold, typing between markers, Heading 2, one undo) |
| B (GFM) | an existing real-window or integration scenario that inserts a GFM construct; if none exists, add one step to `scenarioPalette` (insert an alert, one undo) |
| C (MyST) | `test/integration/mystPickers.test.ts`, or a real-input step that inserts an admonition; if none exists, add it as for B |
| PALETTE-002 | `test/integration/paletteMode.test.ts:39` (already OK) |
| PALETTE-005 | `scenarioPalette` (focus stays in the textarea after Bold; Escape closes the list first), plus `test/integration/editToolbarCover.test.ts:86` |
| PALETTE-007 | `test/integration/imagePicker.test.ts:26` (path 1, already OK); add `scenarioLinkPanel` (`textEditing.ts:730`) if the link path moves to 007 |
| PALETTE-013 | `test/integration/mystPickers.test.ts:8` (already OK) |
| PALETTE-015 | `scenarioSlashMenu`, `textEditing.ts:495` (`/h2` Enter, one undo, `/tab` grid, Escape keeps the text); the visual `scenarioDefinitions2.ts:1124` keeps its marker |
| PALETTE-018 | already OK (`imagePaste.test.ts:26`, `realWindowGaps.ts:556`) |
| LAYOUT-001 | keep `scenarioDefinitions1.ts:198`; add the width-mode visuals v78-v80 at 460 px (path 2) |
| LAYOUT-003 | path 1 (Width button cycle, stored for the workspace): `test/visual/capture_layout_checks.py:763` `check_width_modes` (v66-v71), or an integration assertion that stores `widthMode` and reopens |
| LAYOUT-004 | already OK (`scenarioAssertions.ts:673`, `scenarioDefinitions1.ts:1217`) |
| THEME-002 | the real theme cycle, check `38-toolbar-{host}-{mode}` in `test/integration/realInput/previewWindow.ts:352` |
| THEME-004 | `test/integration/lifecycle.test.ts:77-83` (`previewThemeModeChanged` dark stored and carried by the next page); add the "next page" assertion if the test does not check it |
| THEME-011 | `test/integration/reload-suite.ts:196-219` (zoom 130 survives the window reload and close/reopen); the audit missed this test |

### 8. Scenarios not checked by any test

Add one test per scenario, marked with its SwRS. Prefer a unit test. Use an integration test only
when the scenario needs VS Code.

- **LAYOUT-002:**
  - decimal rounding of `maxContentWidth`;
  - negative input;
  - the rendered column at 0;
  - the update in an open preview (unit test exists at
    `test/session/diagReq.settings.requirements.test.ts:95`; add an integration assertion only if
    cheap).
- **LAYOUT-022:** centring (unit); the negative figure mark.
- **LAYOUT-023:**
  - %, em and rem figure widths;
  - the Mermaid wrapper;
  - the re-measure after a content patch, an image load and a TOC toggle.
- **LAYOUT-011:** the narrow-table fallback; the layout-change re-measure taken over from 018.
- **LAYOUT-032:** a unit test of the scroll-box rule.
- **THEME-016:** theme kinds default, 1, 3 and 4.
- **THEME-043:** the toolbar does not scale with the zoom.
- **PALETTE-256:** the scenarios found unmarked or untested in section 6.
- **LIFE-169:** the stale-message drop. This test is in the toolbar-lifecycle scope: add it here
  only if req-garden-toolbar-lifecycle has not, and mark only LIFE-169.

If a scenario turns out to be untestable without heavy machinery, say so in the SwRS verification
notes. Do not mark a test that does not check it.

### 9. Approved StRS: LAYOUT-001, LAYOUT-003, PALETTE-015

Owner: `gaetan@xeberon.net` (`default_owner_email`).

- **Before you edit these files,** show the owner the exact text diff of each one: section 1 for
  LAYOUT-001 and LAYOUT-003, and the diagram of section 10 for all three. Ask for agreement.
  Record the answer in this CR's folder, in `02-answers.md`, through whoever grills the CR.
- **With agreement,** set `approved_by: gaetan@xeberon.net` and `approved_at` to the current time
  with its UTC offset. List the three StRS under "Approved requirements changed" in the PR body,
  and request the owner's review.
- **Without agreement,** leave those files as they are. Moving markers and tests (sections 5 to
  8) does not edit the StRS files and goes ahead.
- **Changes to the `derives_from` of child SwRS** (section 3) change only generated fields of
  these StRS. They are not text changes.

### 10. Use-case diagrams

Add one `### Use case diagram` section with one Mermaid fence to every in-force StRS of this
scope: the 12 that remain, plus A, B and C. Place it before `### Main paths`. A diagram states
only what a cited SwRS specifies.

| StRS | Kind | Content |
| --- | --- | --- |
| A | sequence | Writer -> palette button, slash or shortcut -> action -> one native edit in the text box (autosave) -> undo restores the text. Alt branch: the action returns nothing, the text is unchanged and the status line gives the reason. |
| B, C | sequence | Same shape, for a GFM construct (alert) and a MyST construct (admonition with a type list). |
| PALETTE-002 | state + sequence | Nested sets Strict ⊂ GFM ⊂ MyST ⊂ Full. Sequence: Cmd/Ctrl+Shift+M -> mode select -> page posts `previewPaletteModeChanged` -> host validates and stores -> the next panel boots in the stored mode, else the one in the setting. |
| PALETTE-005 | state | Editor closed -> Editing (palette docked or sticky) -> Popover open (one at a time) -> Escape -> Editing. Done, Cmd/Ctrl+Enter or leaving the frame -> Committed. Mark the transitions that never commit: a palette press, the native file dialog. |
| PALETTE-007 | sequence | Image button -> page asks the host -> native dialog (the editor stays open) -> path relative to the document, or cancel -> insert or replace `![alt](path)` in one undo step. |
| PALETTE-013 | sequence | Reference button -> "Loading…" -> host lists the `(name)=` targets, or scans at most 20 bib files of at most 2 MiB each -> list, possibly cut, with a note -> pick -> `{ref}` or `{cite}` written. Alt branch: empty list or host error. |
| PALETTE-015 | state | Closed -> (slash at line start or after a space) Open -> Filtered (by alias or label) -> Enter, Tab or click runs the command in one edit -> Closed. Escape or caret out -> Closed, text kept. A slash inside a word -> stays Closed. |
| PALETTE-018 | sequence | Paste -> page paste handler -> image only: the host saves `image-N.ext`; HTML: the host converts it to the safe subset; URL: link, autolink or image; Explorer drop -> one undoable edit. Alt branch: text on the clipboard wins, plain paste. |
| LAYOUT-001 | state | Rendered -> measure each block -> table wider than the box: scrolls in its box with shaded edges; table fits: left as is; long word or URL: wraps. Every branch ends in "no horizontal page overflow (≤ 1 px)". |
| LAYOUT-003 | state | Margin -> Auto -> Full -> Margin (Width button). Entry notes: blocks kept in the column; wide blocks break out; no limit with a 16 px gutter. Transitions: `maxContentWidth` changed; reopen -> stored mode. |
| LAYOUT-004 | sequence | Page runtime -> clearance measure -> reads the toolbar, column and first-control rectangles -> publishes `--sphinx-preview-first-clearance`, `-first-inset` and `-toolbar-bottom` -> CSS moves or narrows the control. Loop on resize, font, collapse and width mode. |
| THEME-002 | state | Current -> Dark -> White -> Cream -> Current (Theme button). Each state paints the page, toolbar, heading band and notes. Current follows the VS Code theme; the redraw waits while a block editor is open. |
| THEME-004 | sequence | Theme button -> `previewThemeModeChanged` -> host validates (drops an unknown mode) -> workspace state. Reopen -> stored workspace value, else saved panel, else Cream. |
| THEME-011 | state | Zoom 70 … 200 in steps of 10. At 70, Zoom out is disabled; at 200, Zoom in is disabled. Reopen -> panel zoom, else workspace zoom, else 100. |

### 11. Bookkeeping

- `just requirements-update`, then commit the generated fields, indexes and Links blocks.
- Add one entry to `requirements/tiers/log.md` under `## 2026-11-17` (or the date of the change),
  with a `### Topic` sub-heading. Give the full old-to-new mapping (sections 2 and 4), the
  reparenting (section 3), the owner's answer on the approved StRS, and the checks actually run.
- Commits follow `.agents/guidelines/git-commit-message.guidelines.md` (scope from
  `git-commit-allowed-scopes.md`). Several commits are fine, for example one per area. Each one
  stays green on `just requirements-lint`.
- In the PR body's Tests section, list every requirement ID added, superseded or changed, with its
  source and test files.

## Coordination with the sibling req-garden CRs

The six req-garden CRs touch some of the same files.

- This CR edits a SwRS of another scope only to remove or replace a parent of these scopes:
  - TRUST-001, 005, 006, 065 and CORE-028 (owned by req-garden-core-diagrams-trust);
  - TABLE-085 and 111 (req-garden-block-table);
  - LIFE-169 (req-garden-toolbar-lifecycle).
- On LIFE-169, this CR also supersedes PALETTE-010 and THEME-013 into it. TOOLBAR-013's merge into
  LIFE-169 belongs to req-garden-toolbar-lifecycle.
- When a rebase conflicts on these frontmatter lists or on `editActions.test.ts` /
  `realInput/markers.ts`, keep both CRs' edits.

## Out of scope

- Deleting any requirement file, `okfreq retire`, or `retired_ids`.
- Any change to product behaviour in `src/` other than moving marker comments. A bug found on the
  way is recorded as a Known issue and reported for the backlog.
- The scopes of the other five req-garden CRs, beyond the parent edits named above.
- Making the diagram section mandatory (req-use-case-diagrams, after all six CRs).
- The writing skill: no rendered syntax changes.

## Evidence

The checks, all green:

- `just requirements-lint`. The main-paths line reads
  `main paths: <n> StRS checked, <m> SwRS citations, all valid`, and there are no orphan SwRS.
- `just requirements-update` leaves no diff, and `okfreq lint --check` and
  `okfreq update-coverage --check` are clean.
- `uv run --no-sync --group requirements okfreq validate --check-links --project-root .` reports
  0 errors.
- `okfreq trace requirements --json` shows the following:
  - no `missing_ids`;
  - every in-force SwRS of the three scopes has at least one implementation file and one test
    file;
  - every in-force StRS of the three scopes has a test marker outside
    `test/integration/realInput/markers.ts`.
- `just check-markers` and the marker gate (`just check`) pass, with the baseline entries of these
  scopes removed.
- `just check` (unit and contract tests, including the new tests of section 8). On Windows,
  `just preflight` runs the static stage.
- New or changed integration and real-window assertions (sections 7 and 8) run in CI: the PR's
  simulated jobs, then the heavy run with `gh workflow run ci.yml --ref <branch> -f heavy=true`.

The scenario steps, read by a reviewer:

1. Open StRS A, B, C, PALETTE-002 and THEME-011 on GitHub. The Mermaid diagram renders. The text
   describes the use case without SwRS numbers in the rationale.
2. Open SwRS-PALETTE-045 and SwRS-LAYOUT-018. They are `superseded`, and `superseded_by` points to
   the merged SwRS, whose scenario table holds their scenarios.
3. Search `@tests_req SwRS-MDOKFSTUDIO-PALETTE-264`. It sits only on paste-URL tests.
4. Open `src/page/modules/editPalette.ts`. No marker comment names more than 3 IDs, and each sits on
   the function it names.

## Open questions

1. **Approved StRS.** Does the owner agree to the text changes of StRS-LAYOUT-001 (drop the
   maintainer half of the user need) and StRS-LAYOUT-003 (trimmed rationale)? Does the owner
   agree to adding a use-case diagram to the three approved StRS (LAYOUT-001, LAYOUT-003,
   PALETTE-015)? If an added diagram counts as an editorial change, it needs no re-approval;
   the owner decides.
2. **Conflict with req-garden-toolbar-lifecycle.** That CR's audit proposes that LIFE-169 and
   LIFE-170 derive from LIFE-014 only. This CR keeps them derived by LAYOUT-003, PALETTE-002,
   THEME-004 and THEME-011, because their Main paths cite them and the main-paths check requires
   it. Which rule wins? The other choice is to cite them with `depends_on` and remove the "keep
   the choice" steps from those four main paths. That changes approved LAYOUT-003.
3. **SwRS-PALETTE-114 (Thread).** Its proposed parent is StRS-REVIEW-015, which is approved. This
   changes only that StRS's generated `derived_by`. Is a re-approval needed, or should
   req-garden-review-frontmatter choose the parent?
