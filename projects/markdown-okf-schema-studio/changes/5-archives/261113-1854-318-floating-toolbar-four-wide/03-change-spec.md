# Change specification: the floating toolbar becomes a 4 × 4 grid

Type: feat (UI layout). Sources: `intake/request.md`, `intake/floating-toolbar-annotated.png`,
`01-intent.md`, `02-answers.md`. Rules: `.agents/constitution.md`, `AGENTS.md`,
`requirements/guidelines/requirements.guidelines.md` and `requirements/guidelines/project.guidelines.md`
("During a change").

## 1. Goal

The owner wants the preview's floating toolbar "four icons wide" (« reorg le menu flottant en 4
icones de large »), "of course in 4x4" (« évidemment en 4x4 »). Today it is a main row of four plus
four rows of three. Afterwards it is four rows of four. It keeps the same 16 buttons, the same
behaviour and the same collapse. Only the order of the buttons and the rows change.

## 2. The layout (decided)

This is the owner's confirmed table (02-answers.md, "mapped to the code", confirmed on 2026-11-13 with
« parfait … passe la dans le batch en cours »). The owner's own words are in brackets:

| Row | Col. 1 | Col. 2 | Col. 3 | Col. 4 |
| --- | --- | --- | --- | --- |
| 1 | Refresh | Edit | Export | Collapse |
| 2 | Anchor ("lien") | Theme ("☕") | Back | Next |
| 3 | Width ("margin") | Fold ("collapse title") | Zoom out | Zoom in |
| 4 | TOC ("table of content") | Side-by-side ("diff") | Diff ("changes") | Comments |

In code terms (the constants of `src/core/preview/previewToolbar.ts`):

| Row | `data-sphinx-preview-toolbar-row` | Buttons, left to right |
| --- | --- | --- |
| 1 (always shown) | `main` | `REFRESH_BUTTON`, `EDIT_BUTTON`, `EXPORT_BUTTON`, `COLLAPSE_BUTTON` |
| 2 | `navigation` | `ANCHOR_BUTTON`, `THEME_BUTTON`, `BACK_BUTTON`, `NEXT_BUTTON` |
| 3 | `view` | `WIDTH_BUTTON`, `FOLD_BUTTON`, `ZOOM_OUT_BUTTON`, `ZOOM_IN_BUTTON` |
| 4 | `review` | `TOC_BUTTON`, `SIDE_BY_SIDE_BUTTON`, `DIFF_BUTTON`, `COMMENTS_BUTTON` |

The new Tab order (the `data-sphinx-preview-*` suffixes, as the unit test lists them) is:
`refresh, edit-toggle, export, toolbar-collapse, anchor, theme-toggle, back, next, width-toggle,
fold-toggle, zoom-out, zoom-in, toc-toggle, sbs-toggle, diff-toggle, comments-toggle`.

The other decisions carried from the answers (the last four were the open questions Q1 to Q4 of
the previous version of this specification; the owner accepted the recommendations on 2026-11-13
with « Ok pour tout ça », see 02-answers.md, "the specification's open questions"):

- Row 1 does not change.
- Rows 2 to 4 stay together in the group the collapse button hides (`data-sphinx-preview-toolbar-more`,
  id `sphinx-preview-toolbar-more`). The collapse behaviour, the saved choice, the load hint and the
  unroll animation do not change. The group now holds three rows instead of four.
- No button's markup changes: attributes, labels, titles, tooltips, icons and default states stay
  as they are.
- The round brown look of Diff and Comments is not a separate kind of button. It is the pressed
  state (`aria-pressed="true"`) of two toggles that are on by default, and it stays as is.
  02-answers.md marked this "to confirm"; the owner then confirmed that whole section with « parfait ».
- The first reading of the screenshot in 02-answers.md ("today's reading order, reflowed") was
  rejected by the owner and is not the layout.
- The toolbar stays four buttons (134 px) wide. Every row is now as wide as row 1, so the expanded
  toolbar is still exactly as wide as the collapsed one and never wider than 134 px.
- Row names (decided, was Q1): `main`, `navigation`, `view`, `review`, as in the table above. The
  same names, capitalised, are the row headings of `docs/user/toolbar.md` (Main, Navigation, View,
  Review).
- Pending overlay (decided, was Q2): it moves up to sit right under the four rows, with today's gap.
  Today the expanded toolbar ends at y 178 (12 px top, 1 px border and 3 px padding on each side,
  five rows of 30 px, four gaps of 2 px) and the overlay starts at 192 px, a 14 px gap. With four
  rows the toolbar ends at y 146 (12 + 2 + 6 + 4 x 30 + 3 x 2), so the expanded offset becomes
  **160 px**. The collapsed offset (62 px, one row) does not change.
- Approved requirement StRS-MDOKFSTUDIO-LAYOUT-003 (decided, was Q3): the owner
  (gaetan@xeberon.net) agreed explicitly on 2026-11-13 to change it so that the Width button is on
  row 3. This specification records that agreement (requirements/guidelines/project.guidelines.md,
  "Approved requirements"). The edit is in section 3.4.
- SwRS-MDOKFSTUDIO-TOOLBAR-007 (decided, was Q4): its wrong collapsed Tab order ("Refresh, Anchor,
  Edit and Show view controls") is fixed in this change to Refresh, Edit, Export to HTML and Show
  view controls, which is the order before and after this change.

## 3. What changes, area by area

### 3.1 Markup: `src/core/preview/previewToolbar.ts`

- In `renderPreviewToolbar()`, build row 1 as it is today, then three rows of four in the order of
  section 2, all inside the `data-sphinx-preview-toolbar-more` group. Keep the `row()` helper and
  the `data-sphinx-preview-toolbar-row="<name>"` attribute with the names of section 2 (`main`,
  `navigation`, `view`, `review`). Rename the local constants to match (`navigationRow`, `viewRow`,
  `reviewRow`; `appearanceRow`, `layoutRow` and `contentRow` go).
- Rewrite the doc comment above the function: four rows of four buttons, with the content of each
  row, rows 2 to 4 in one group that the collapse button hides, and the Tab order following the
  rows. Keep the note that Edit is always enabled.
- Keep the markers `@implements_req SwRS-MDOKFSTUDIO-TOOLBAR-001`, `-005` and `-134`.

### 3.2 Styles: `src/core/preview/styles/pageChromeStyles.ts` and `propertiesStyles.ts`

- No rule needs to change for the grid itself. Each `[data-sphinx-preview-toolbar-row]` is already
  a flex row aligned to the end, and four buttons fit in the width of row 1.
- Update the comments: "Rows 2 to 5" becomes "Rows 2 to 4" (`pageChromeStyles.ts`, above
  `[data-sphinx-preview-toolbar-more]`, and `propertiesStyles.ts`, the motion comment).
- The pending overlay (`[data-sphinx-preview-pending-overlay]`): `inset-block-start: 192px`
  becomes `160px`, so it sits right under the four rows with today's 14 px gap (section 2). The
  collapsed rule keeps `62px`. Its comment becomes "Below the toolbar: four rows, or one row when
  rows 2 to 4 are collapsed."

### 3.3 Other source comments that name a row (wording only, no behaviour change)

- `src/page/modules/toolbarCollapse.ts`: "rows 2 to 5" becomes "rows 2 to 4" (two places).
- `src/page/runtime.ts` (around line 284), `src/core/state/previewViewPreferences.ts` (the
  `toolbarCollapsed` comment): "rows 2 to 5" becomes "rows 2 to 4".
- `src/page/modules/widthMode.ts`: "toolbar row 4" becomes "row 3".
- `src/page/modules/commentsToggle.ts` and `src/page/modules/incomingToggle.ts`: "toolbar row 5"
  becomes "row 4".
- `src/core/protocol/pageToHost.ts` (the side-by-side comment, around line 259): becomes "row 4".
- These stay correct and do not change: `viewControls.ts` (zoom, row 3), `historyControls.ts`,
  `pageToHost.ts` and `pageToHostMessages.ts` (Back and Next, row 2).
- `.agents/glossary/common.md`, "View preference": "changed from toolbar row 2 (zoom, width mode,
  TOC, incoming changes)" becomes "changed from toolbar rows 2 to 4".

### 3.4 Requirements (okfreq)

Every file below is `proposed` or `draft` unless marked otherwise. Edit the authored text only and
regenerate the rest with `just requirements-update`.

- `requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-001.md`: update the title,
  description, normative statement and scenarios "Writable preview" and "Visual order" to four rows
  of four buttons, in the order of section 2, under the row names `main`, `navigation`, `view` and
  `review`. Every row now holds four buttons, so drop "no row other than main holds more than
  three". The new Tab order: row 2 starts with Anchor, row 3 with Width, row 4 with TOC. Keep "as
  wide as its first row, 134 px". In the "Table handle strip" scenario, update the toolbar geometry
  (today "y 12 to 178"; expected "y 12 to 146") to the value the integration test logs after the
  change. Update the verification notes and criteria ("16 buttons in four rows").
- `SwRS-MDOKFSTUDIO-TOOLBAR-005.md` (draft): "the Fold button in row 5" becomes "row 3".
- `SwRS-MDOKFSTUDIO-TOOLBAR-130.md`: "rows 2 to 5" becomes "rows 2 to 4", and "below the five open
  rows" becomes "four open rows".
- `requirements/tiers/strs/toolbar-navigation/StRS-MDOKFSTUDIO-TOOLBAR-001.md`: change "five clearly
  grouped rows" to four rows. Rewrite the first rationale bullet with the new rows and replace "No
  other row holds more than three buttons, so the toolbar stays narrow" with every row holding four
  buttons, no wider than the first row. Also change "rows 2 to 5", and the main-path step "drawn as
  five rows".
- `requirements/tiers/swrs/trust-security/SwRS-MDOKFSTUDIO-TRUST-001.md`: "the same five rows with
  16 buttons" becomes "four rows".
- `requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-049.md`, scenario "Position of the
  pending notice": "192 px from the top (below the five rows of the toolbar)" becomes "160 px from
  the top (right under the four rows of the toolbar)". The 62 px row stays. Its verification note
  already says "the 160 px and 62 px offsets" (out of date today, right after the change): leave it.
- `requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-007.md`: in the scenario
  "Keyboard order when collapsed", "Refresh, Anchor, Edit and Show view controls only" becomes
  "Refresh, Edit, Export to HTML and Show view controls only". In the description and
  the normative statement, "the group that holds the navigation and view rows" becomes "the group
  that holds the navigation, view and review rows". In the verification notes, "rows 2 to 5"
  becomes "rows 2 to 4". The tests already check the right order (`check_toolbar_collapse` compares
  the collapsed order to the main row plus Show view controls), so no test changes for this fix.
- `requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-170.md`: "Toolbar rows 2 to 5"
  becomes "rows 2 to 4".
- `requirements/tiers/swrs/review-annotations/SwRS-MDOKFSTUDIO-REVIEW-008.md`: "the Side-by-side
  button of toolbar row 3" becomes "row 4" (description and normative statement).
- `requirements/tiers/swrs/theme-zoom/SwRS-MDOKFSTUDIO-THEME-001.md`: "the Theme button on toolbar
  row 3" becomes "row 2".
- These stay correct and do not change: `SwRS-MDOKFSTUDIO-THEME-038` and
  `StRS-MDOKFSTUDIO-THEME-011` (zoom, row 3), and `SwRS-MDOKFSTUDIO-TOOLBAR-134` (Export, still the
  last button of the main row but one).
- Approved, changed with the owner's recorded agreement (section 2):
  `requirements/tiers/strs/layout-width/StRS-MDOKFSTUDIO-LAYOUT-003.md`.
  - Rationale bullet "The Width button sits in the fourth toolbar row (the layout row, with Table of
    contents); …" becomes "The Width button sits in the third toolbar row (the view row, with Fold,
    Zoom out and Zoom in); the placement itself is checked by the toolbar-navigation scope."
  - Known issue "the code and docs/user/toolbar.md put the button on row 4, while the file header of
    the width mode module and an older bullet of the Unreleased change-log entry say row 2" becomes
    "the code, docs/user/toolbar.md and the file header of the width mode module put the button on
    row 3, while a bullet of an older released change-log entry says row 2" (the module header is
    fixed in section 3.3; the old bullet is in a released section of CHANGELOG.md and is not
    rewritten).
  - Set `approved_by: gaetan@xeberon.net` and `approved_at` to the date and time of the edit with
    its UTC offset (ISO 8601, for example `'2026-11-13T15:00:00+01:00'`). Leave `req_lifecycle:
    approved`. Do not edit the `verified` block by hand: `just requirements-update` regenerates it
    from the new approval.
  - The PR body lists it under "Approved requirements changed", and the agent that opens the PR
    requests the owner's review.
  - Change nothing else in this file.
- `StRS-MDOKFSTUDIO-LAYOUT-006` is `superseded`: leave it.
- After the edits: `just requirements-update`, then a `### Topic` entry under the
  `## 2026-11-13` heading of `requirements/tiers/log.md` (create the date heading if it is missing).
  The entry lists the requirements changed, their source and test files, and that the approved
  StRS-MDOKFSTUDIO-LAYOUT-003 changed with the owner's agreement of 2026-11-13.

### 3.5 Tests

Each test that asserts the row order changes because the decided layout changes. The intent of
each assertion stays the same: rows, counts, order, Tab order and width. Say so in the commit and
the PR (constitution, section 3).

- `test/core/preview/previewStyles.test.ts`, test "preview toolbar has five rows: …" (around
  line 486): rename it to four rows of four. Split on the row names `navigation`, `view` and
  `review`, assert four buttons in every row, assert each row's controls in the order of section 2,
  and assert the new Tab order of section 2. Replace the loop "no row but the main row holds more
  than three buttons" with "every row holds four buttons". Keep the 16-button count, the collapse attributes, the `aria-pressed`
  defaults (TOC, Side-by-side and Fold false, Diff and Comments true) and the end of the markup
  (Comments is the last button). This test fails on the previous code.
- `test/core/preview/previewStyles.test.ts`, test "T08: zoom scales the content font size and the
  column width together" (around line 906): the expanded offset of the pending overlay becomes
  `inset-block-start: 160px;` (was `192px`); the `62px` assertion stays. The decided value changes
  (section 2), the intent stays: the overlay sits under the expanded toolbar.
- `test/core/preview/contentPatch.test.ts` (around line 289): it asserts
  `data-sphinx-preview-toolbar-row="appearance"`. Point it at `view`, the row that now holds the
  zoom buttons.
- `test/visual/capture_layout_checks.py`:
  - `check_diff_toggle`: read `[data-sphinx-preview-toolbar-row="review"]` (around line 24), the
    row that now holds Diff and Comments, instead of `"content"`. They are still its last two
    buttons. Update the docstring and the message ("row 4").
  - `check_toolbar_collapse`: after "Hide view controls", the Tab order is Anchor, Theme
    (`startswith("Preview theme")`), Back, Next; then Width, Fold or Unfold all sections, Zoom out,
    Zoom in; then Show table of contents, the side-by-side label, the Diff label, the Comments label.
    Update the failure messages and the docstring ("rows 2 to 4"). The width check (expanded as wide
    as collapsed) and the height check stay.
  - The rows check (around line 316): the list of names becomes `["main", "navigation", "view",
    "review"]`. Every row holds 4 buttons (`expected_main` stays as it is for row 1; rows 2 to 4 expect 4, not 3). The
    message becomes "four rows". The 134.5 px width check stays.
- `test/visual/scenarioAssertions.ts`: the message "rows 2 to 5 of the toolbar are hidden" (around
  line 477), the P8 comment (around line 707), and the description of the `toolbar-rows-*`
  scenarios (around lines 728 to 730). The description is already out of date today: replace it
  with the four rows of section 2 and "Rows 2 to 4 are hidden."
- `test/visual/scenarioIds.ts`: the 16 descriptions `toolbar-navigation/v06` to `v21` (around
  lines 491 to 506) say four rows (with the new names) of four buttons each.
- `test/page/runtimePageControls.test.ts`: test name "the collapse button hides rows 2 to 5" and
  the message "rows 2 to 5 are hidden": wording becomes "rows 2 to 4".
- `test/integration/storedChoices.ts` (comment "five rows") and `test/integration/tableMoves.ts`
  (the geometry comment): wording only. The tableMoves assertion (the toolbar does not cover the
  handle strip) is about the width and stays.
- Move the `@tests_req` markers only if a test moves. Every test above keeps its markers.

### 3.6 User documentation and changelog

- `docs/user/toolbar.md`: change the intro to four rows of four buttons and replace the five
  numbered rows with the four rows of section 2, under the headings **Main**, **Navigation**,
  **View** and **Review**. Each button keeps its explanation from today's text (Fold with its link
  to folding.md, Comments with what it hides, Side-by-side and Export "see below"). "rows 2 to 5"
  becomes "rows 2 to 4" (three places), and "five rows of buttons" in the image alt text becomes "four rows".
- `docs/user/README.md`: "the five rows of buttons" becomes "four rows".
- `images/readme/toolbar-expanded.png` and `toolbar-collapsed.png`: regenerate them from the
  scenarios `toolbar-navigation/v18` and `v19` with `scripts/generate-readme-images.py`, after a
  visual run. The expanded image is meant to change. Tighten the crop in `scenarioIds.ts` only if
  the shorter toolbar leaves empty space.
- `CHANGELOG.md`, `## Unreleased`: one line for the reader. The floating toolbar is now four buttons
  wide on four rows, and lists the rows.

### 3.7 Writing skill

`skills/writing-for-markdown-okf-schema-studio/` does not mention the toolbar, and the toolbar is
not a rendered syntax, so the skill does not change.

## 4. Out of scope

- No new or removed button. No change to the icons, labels, titles, tooltips, default states or
  behaviour of any button.
- No change to row 1, the collapse behaviour, the saved `toolbarCollapsed` preference, the load
  hint or the animation.
- No change to the toolbar width, its position (12 px from the top, 14 px from the end) or its
  z-index.
- No change to the pressed look of Diff and Comments.
- The read-only and standalone previews keep the same layout as the writable one (Edit is always
  enabled), so they are not a separate case.

## 5. Evidence

- Unit: `just check` passes with the updated `previewStyles.test.ts` test. That test asserts the
  4 × 4 rows and the Tab order of section 2, and it fails on the previous code.
- Unit: T08 asserts the 160 px and 62 px offsets of the pending overlay.
- Visual: `just ci-visual` passes `check_toolbar_collapse` and the rows check on
  `toolbar-navigation/v06` to `v21`: four rows of four, the new Tab order, no overlap, inside a
  360 px and a 900 px pane, at zoom 70 and 200 percent, in the light, dark, white and cream themes,
  expanded and collapsed, and no wider than 134 px.
- Integration: `just ci-integration` (heavy run: `gh workflow run ci.yml --ref <branch> -f
  heavy=true`). tableMoves still finds the toolbar outside the handle strip. Copy the logged toolbar
  geometry into SwRS-MDOKFSTUDIO-TOOLBAR-001.
- Requirements: `just requirements-lint` and `just requirements-update` are clean.
  `okfreq validate --check-links --project-root .` passes.
- Completion gate: `just preflight` passes.
- Scenario for the reviewer, by hand:
  1. Open a preview with the toolbar expanded. Read the rows: Refresh, Edit, Export, chevron. Then
     Anchor, Theme, Back, Next. Then Width, Fold, Zoom out, Zoom in. Then TOC, Side-by-side, Diff,
     Comments.
  2. Press Tab from Refresh through all 16 buttons. The focus follows that order.
  3. Press the chevron. Only row 1 is left, and Tab reaches only Refresh, Edit, Export and Show view
     controls. Press it again and the three rows unroll as one block.
  4. Hover a button of each row. The tooltip is still right-aligned under its button.
  5. Compare the widths: the expanded toolbar is exactly as wide as the collapsed one.
- The PR shows a before and after screenshot of the expanded toolbar (the regenerated
  `toolbar-expanded.png`).

## 6. Open questions

None. Q1 to Q4 of the previous version were answered by the owner on 2026-11-13 (02-answers.md,
"the specification's open questions") and are folded into section 2.
