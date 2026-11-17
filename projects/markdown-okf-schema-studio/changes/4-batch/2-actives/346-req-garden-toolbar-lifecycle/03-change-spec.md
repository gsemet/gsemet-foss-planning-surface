# Change Specification: garden the requirements of toolbar-navigation and lifecycle-sync

Origin: verbal (requirements gardening audit, CR `requirements-gardening`). No tracker issue.

## Goal

A reviewer understands the toolbar and lifecycle use cases of Studio by reading their StRS.
Each SwRS is one observable behaviour. It is traced by `@implements_req` markers on the code that
does it and by `@tests_req` markers on the tests that check its scenarios. No product behaviour
changes: this CR changes requirement text, relations, markers and tests only (plus one
byte-identical split of CSS constants, so that markers can sit on the rules they name).

Source of every finding below:
`requirements-gardening/evidence/audit-toolbar-lifecycle.md` (next to this CR in `1-inbox/`).
Line numbers are those of `main` at `dedbdb2a`. The sibling CRs land first and may shift them, so
locate each point by the function or constant it names, not by its line number.

## Prerequisites (land first, `depends.json`)

- **req-use-case-diagrams** adds the rule for an authored `### Use case diagram` section in
  `requirements/guidelines/project.guidelines.md`: one Mermaid fence, placed before
  `### Main paths`, a sequence diagram by default, an actors diagram when several roles take part
  and a state diagram for a mode. Follow that rule as it landed.
- **req-marker-gate** extends `scripts/check-marker-companions.mjs`:
  - an in-force SwRS that is not exempt and has no `@implements_req` fails `just check`;
  - a marker comment names at most 3 IDs;
  - a companion file names, for each ID, the scenario that checks it;
  - offenders that exist today sit in a baseline list that can only shrink (ratchet).

  This CR removes from that baseline every entry it clears (see "Marker gate baseline").
- Rebase on `main` after both have merged. If either has not merged, the PR stacks on it, per
  `.agents/guidelines/stacked-prs.guidelines.md`.

## Rules that frame the work (owner decisions, `02-answers.md`)

- Published requirements are never deleted. A merge or a split uses
  `uv run --no-sync --group requirements okfreq supersede OLD NEW [NEW...] --path requirements --yes`.
  An obsolete requirement uses `okfreq archive`. Never `okfreq retire`, never `git rm`, and this
  applies to `draft` requirements too.
- A merge or split proposed below that the Driver doubts after reading the code and the SwRS is not
  done. The Driver brings it back to the owner with the reason; the rest of the CR goes on.
- `draft` -> `proposed` is the owner's decision. This CR does not change the lifecycle of the
  draft StRS TOOLBAR-002 and -003 or of the draft SwRS TOOLBAR-003, -004, -005, -006, -008, -009,
  -010, -011, -012 and -014, unless the owner's answer to open question 1 is recorded before the
  Driver starts.
- An approved StRS whose text changes needs the owner's recorded re-approval. Checked at
  `dedbdb2a`: none of the requirements this CR touches is `approved` (all are `proposed` or
  `draft`; this includes StRS-BLOCK-001, StRS-LIFE-007, SwRS-TRUST-001 and SwRS-FMSCHEMA-060).
  If the Driver finds that one is `approved` when the work starts, the Driver does not change it
  and brings it back to the owner.
- Any requirement created here uses `okfreq new strs|swrs ... --lifecycle proposed`, never `draft`
  (project guideline "Approved requirements").
- What a test reveals is specified as it behaves. If a new test shows that the code differs from
  the SwRS, the SwRS states the behaviour as it is, with a line "Known issue: ...". The test checks
  that behaviour, and the fix is reported for the backlog. No code fix is made in this CR
  (constitution, section 1).
- Spec critic: none (owner: "it changes requirement text, markers and tests, no product
  behaviour").

All work happens in `requirements/` (with `okfreq` and authored text), `src/` (marker comments and
the CSS-constant split only) and `test/` (markers, moved tests and new tests).

## 1. SwRS merges (okfreq supersede)

For each row:

1. Fold the scenarios of OLD into NEW, under the given scenario kind. Use a GIVEN-WHEN-THEN
   scenario, or a row of an existing scenario table. Reword NEW's description when its SHALL no
   longer covers the merged cases.
2. Run `okfreq supersede OLD NEW --yes`.
3. Replace every `@implements_req OLD` and `@tests_req OLD` in `src/` and `test/` by the NEW ID.
   When the same point already carries NEW, drop the duplicate.
4. Replace every citation of OLD in a `### Main paths` section by NEW, keeping or setting the
   scenario kind.
5. Any `depends_on` that names OLD now names NEW.

| Old (superseded) | New | Merged as |
| --- | --- | --- |
| SwRS-TOOLBAR-013 | SwRS-LIFE-169 | refusal rows ("the host accepts only a known view preference with a valid value"); see note A |
| SwRS-TOOLBAR-056, SwRS-TOOLBAR-058 | SwRS-TOOLBAR-054 | refusal scenarios (history state of another render; only back or forward) |
| SwRS-TOOLBAR-065 | SwRS-TOOLBAR-059 | boundary scenarios (last 50 places, no duplicates) |
| SwRS-TOOLBAR-083 | SwRS-TOOLBAR-079 | refusal and boundary scenarios (bounded discovery messages) |
| SwRS-TOOLBAR-113 | SwRS-TOOLBAR-077 | refusal scenario (a link message needs a request) |
| SwRS-TOOLBAR-122, SwRS-TOOLBAR-126 | SwRS-TOOLBAR-120 | refusal scenarios (pairing for another document; non-boolean anchor mode) |
| SwRS-TOOLBAR-133 | SwRS-TOOLBAR-037 | scenarios of "Narrow pane rail and overlay" |
| SwRS-TOOLBAR-022 | SwRS-TOOLBAR-018 | scenarios of the depth setting (a setting is a scenario of the behaviour it drives) |
| SwRS-TOOLBAR-002 | SwRS-TOOLBAR-025 | scenario "shadow under the band only while text scrolls under it" |
| SwRS-TOOLBAR-005 (draft) | SwRS-TOOLBAR-003 (draft) | scenarios: Fold all and Unfold all from the toolbar and the command palette |
| SwRS-TOOLBAR-011 (draft) | SwRS-TOOLBAR-010 (draft) | scenarios: case, whole word, regular expression |
| SwRS-TOOLBAR-132 | SwRS-TOOLBAR-009 (draft) | scenario: native editing keys in the fields |
| SwRS-TOOLBAR-014 (draft), SwRS-TOOLBAR-131 | SwRS-TOOLBAR-012 (draft) | refusal (replace unavailable while a block editor is open) and boundary (Replace all announces the skipped matches; extends "Matches that do not map one-to-one") |
| SwRS-LIFE-010 | SwRS-LIFE-003 | refusal scenario ("Open Preview to Side checks the file it is given", next to "No eligible file") |
| SwRS-LIFE-055 | SwRS-LIFE-049 | refusal scenarios (pending notice with an oversized or malformed field: the 500/501 bound, malformed, hide) |
| SwRS-LIFE-097 | SwRS-LIFE-100 and SwRS-LIFE-108 | `scrollPreviewWithEditor` rows go to LIFE-100; `scrollEditorWithPreview` rows go to LIFE-108; `okfreq supersede SwRS-...-LIFE-097 SwRS-...-LIFE-100 SwRS-...-LIFE-108 --yes`; see note B |
| SwRS-LIFE-171 | SwRS-LIFE-001 | scenario "Manifest contract": the manifest declares Agents window support |

Note A: the CR req-garden-palette-theme-layout supersedes PALETTE-010 and THEME-013 into the same
LIFE-169. Each CR adds only its own rows. The CR that lands second rebases and keeps both sets of
rows.

Note B: LIFE-097 markers are split by setting.

- `src/page/features/scrollCore.ts` (the handler at `:498`, which already carries LIFE-100):
  drop LIFE-097, since LIFE-100 is already there.
- `src/session/features/scrollSync.ts:130`: LIFE-100 or LIFE-108, by which setting the function
  reads.
- `test/integration/sourceMapping.test.ts:106`, `test/page/pageSettings.test.ts:9` and
  `test/page/runtimeScroll.test.ts:731`: by the setting each test checks.
- Remove LIFE-097 from StRS-LIFE-021's path (section 3).

Use full IDs (`SwRS-MDOKFSTUDIO-...`) in commands and markers. StRS-LIFE-003 and SwRS-LIFE-003 are
different requirements, and so are StRS-LIFE-010 and SwRS-LIFE-010: always write the tier prefix.

Expected effect: toolbar-navigation goes from 50 to 34 in-force SwRS, and lifecycle-sync goes from
34 to 30.

## 2. Other SwRS text fixes (same ID)

- **SwRS-LIFE-004:** reword from architecture to observable behaviour: "a long render never
  blocks the text editor; a render that a newer edit supersedes stops". The worker and the abort
  move to the verification notes.
- **SwRS-LIFE-069:** the internal scenarios ("What the key of a block holds", "The loaded page is
  not parsed again" and others like them) move to the verification notes. The observable scenarios
  stay.
- **SwRS-LIFE-156:** the scenarios "Boot context written by the host / read by the page" move to
  the verification notes.
- **SwRS-LIFE-149:** keep the implementation marker at the `createWebviewPanel` call in
  `src/host-vscode/activation.ts`. Set `annotation_exemption: false` and clear its
  `exemption_reason`: the panel that opens beside the built-in preview is a real code point.
- **SwRS-TOOLBAR-007:** add a scenario stating that the collapsed choice is kept for the workspace
  and that a new page starts from it, citing the rules of SwRS-LIFE-169 and SwRS-LIFE-170. Add
  both to its `depends_on`. This lets StRS-TOOLBAR-001's path cite TOOLBAR-007 for that step
  (section 3).
- **SwRS-TOOLBAR-001:** the scenario "Table handle strip at the top of the page" is table-editing
  geometry. If a table-editing SwRS already specifies the handle strip, move the scenario there,
  with its test marker. Otherwise leave it in place and note it in the log entry.

## 3. StRS changes

General, for every StRS of the two scopes:

- **Main paths.** Re-check every `### Main paths` after the merges and the reparenting.
  - Every cited SwRS is in force and derives from that StRS.
  - The last state of a path has no bullet.
  - No step names a behaviour that no cited SwRS specifies.

  `just requirements-lint` (`scripts/check_main_paths.py`) checks the citations.
- **Use case diagram.** Write one `### Use case diagram` per StRS (section 6).
- **Stray headings.** Remove the stray `## User Need` heading under "Preserved stakeholder intent"
  in StRS-TOOLBAR-002, -003 and -014.

Per StRS:

- **StRS-LIFE-001 (open previews):**
  - Drop StRS-LIFE-001 from the `derives_from` of SwRS-LIFE-026, -032 and -049. They stay derived
    by StRS-LIFE-003, and LIFE-049 also by StRS-LIFE-007.
  - Drop StRS-LIFE-001 from SwRS-LIFE-156, which belongs to StRS-LIFE-021 only.
  - Path 1 step 2 (follow the active editor) is StRS-LIFE-003's path, so replace it with an opening
    step (side, Open With, coexistence, group lock, several previews).
  - LIFE-171 is merged (section 1).
- **StRS-LIFE-003 (side preview follows, refresh):** scope = follow, refresh and title. Drop it from
  the `derives_from` of SwRS-LIFE-100, -119 and -125 (the scroll and reading state of LIFE-010). It
  receives the LIFE-010 refusal (section 1).
- **StRS-LIFE-005 (updates in place):**
  - Drop it from SwRS-LIFE-100.
  - The 3 glow bullets of the rationale become one sentence.
  - SwRS-LIFE-004 is reworded (section 2).
- **StRS-LIFE-007 (render state):**
  - Drop it from SwRS-LIFE-018 and SwRS-LIFE-069.
  - Path 1's last state ("The status reads Preview ready") loses its Option bullet. Move that option
    to the previous state.
  - SwRS-LIFE-002 now derives from StRS-LIFE-007 instead of StRS-LIFE-014 (a background failure is
    a diagnostic of the render state, not a reload behaviour).
- **StRS-LIFE-010 (scroll together):**
  - Drop it from SwRS-LIFE-026, -069, -071 and -156.
  - The rationale bullet about the Anchor button moves out (the button is StRS-TOOLBAR-013's).
  - LIFE-097 is merged into LIFE-100 and LIFE-108 (section 1).
- **StRS-LIFE-014, kept and narrowed.** New title: "Previews come back after a reload, and each
  document keeps its reading place and view choices". Wording is the Driver's, true to the derived
  SwRS.
  - It keeps SwRS-LIFE-038, -125, -127, -169, -170 and FMSCHEMA-014, and its Paths 1 and 2.
  - The closing need moves to the new StRS below.
  - Drop it from SwRS-LIFE-071 (that SwRS belongs to StRS-LIFE-005; make sure LIFE-071 derives from
    StRS-LIFE-005) and from SwRS-LIFE-172.
- **New StRS (lifecycle-sync), "Closing a preview or a folder leaves nothing behind".**
  - Create it with `okfreq new strs ... --lifecycle proposed`, with a `--description` and
    `--user-need` taken from SwRS-LIFE-143: closing a panel or a document, removing a workspace
    folder or deactivating stops the preview's work and leaves no watcher, Problems entry or late
    result; a preview whose folder is removed keeps its panel with restricted reads.
  - Write its rationale and Main paths.
  - SwRS-LIFE-143 derives from it instead of from StRS-LIFE-014.
  - Its validation test is `test/integration/workspaceDisposal.test.ts:28`: move the
    `@tests_req StRS-...-LIFE-014` there to the new StRS ID. StRS-LIFE-014 keeps its validations at
    `reload-suite.ts:112` and `serializer.test.ts:28`.
- **SwRS-LIFE-172 (preview mode, E switches to edit mode):** reparent to StRS-BLOCK-001 (the
  edit-mode use case). Only the `derives_from` of LIFE-172 changes; StRS-BLOCK-001's text belongs
  to req-garden-block-table.
- **StRS-LIFE-021 (settings editor):**
  - Drop it from SwRS-LIFE-069 and SwRS-LIFE-097.
  - Rewrite Path 1 as: open the settings editor -> the groups in fixed order (Preview, Editing,
    Frontmatter, Comments, PlantUML) -> a default and a description per setting.
  - Remove the "description at most 700 characters" option, which is a build-time limit.
  - Add one or two rationale bullets so that the use case reads on its own.
- **StRS-TOOLBAR-001 (toolbar):**
  - Scope = rows, collapse and motion. The persistence of the other view choices goes to
    StRS-LIFE-014.
  - Reword the description and user need: only the collapsed toolbar is remembered here, and the
    zoom, width, TOC and other view choices are cited as the StRS-LIFE-014 rule.
  - Drop StRS-TOOLBAR-001 from the `derives_from` of SwRS-LIFE-169, SwRS-LIFE-170 and SwRS-TRUST-001.
    The Restricted Mode rationale bullet is TRUST-006's; keep TRUST-006 as it is, its fate belongs
    to req-garden-core-diagrams-trust.
  - Rewrite Path 1 to cite TOOLBAR-001, TOOLBAR-007 (collapse, Tab order, choice kept per section 2)
    and TOOLBAR-130 (load hint).
- **StRS-TOOLBAR-002 (fold, draft):** text fixes only. Its lifecycle is open question 1.
- **StRS-TOOLBAR-003 (find and replace, draft):** text fixes only. After the merges it has 3 SwRS
  (009, 010, 012).
- **StRS-TOOLBAR-004 (sticky band):** the merges only (022 into 018, 002 into 025).
- **StRS-TOOLBAR-006 (TOC):**
  - Split the 70-word user need into short sentences.
  - Drop StRS-TOOLBAR-006 from the `derives_from` of SwRS-LIFE-169 and -170. TOOLBAR-033 already
    has them in `depends_on`.
- **StRS-TOOLBAR-009 (Back and Next):** after the merges it has TOOLBAR-054 and TOOLBAR-059, plus
  BLOCK-205 and TRUST-006 as they are.
- **StRS-TOOLBAR-011 (links):**
  - Split the 90-word user need into short sentences.
  - Fix the clause "never open a file outside the workspace unless the reader enabled the
    frontmatter outside-link setting". At `dedbdb2a`, `allowOutsideWorkspaceLinks` is read only on
    the frontmatter-link path (`src/session/features/links.ts:150-153`,
    `src/core/frontmatter/fileLinks.ts:205,219`). The Driver confirms this in the code:
    - If only frontmatter links use it: the clause becomes "a link in the page never opens a file
      outside the workspace roots", in the description and the user need. Frontmatter links are
      the use case of StRS-FMSCHEMA-014.
    - If body links use it too: keep the clause, and add `SwRS-FMSCHEMA-060` to the `depends_on`
      of SwRS-TOOLBAR-094.
- **StRS-TOOLBAR-013 (Anchor and cursor block):**
  - Drop StRS-TOOLBAR-013 from the `derives_from` of SwRS-LIFE-169 and -170. TOOLBAR-120 already
    has them in `depends_on`.
  - Rewrite Path 1 step 2: TOOLBAR-120 keeps the choice for the panel, with Option TOOLBAR-120
    (refusal) for the non-boolean value. TOOLBAR-126 is gone.
  - The Anchor-button wording leaves StRS-LIFE-010 and lives here only.
- **StRS-TOOLBAR-014 (export HTML):**
  - Path 1's last state ("The HTML file is written") loses its bullet, and a final state follows
    when needed.
  - SwRS-DIAG-128's missing implementation marker is fixed by req-marker-gate, not here.

Left as they are, owned by other CRs: the other-scope StRS that derive LIFE-169/170
(BLOCK-001, LAYOUT-003, PALETTE-002, REVIEW-012, THEME-004, THEME-011). Their Main paths cite
LIFE-169/170, so removing them belongs to the CR that rewrites those paths. Also left: LIFE-026
under StRS-TRUST-001 and LIFE-062 under StRS-TRUST-004 (req-garden-core-diagrams-trust).

## 4. Markers onto the code and the tests they name

Implementation markers (`src/`). The other-scope IDs in the same blocks stay for their own CRs.

| Today | Move to |
| --- | --- |
| `src/core/preview/styles/pageChromeStyles.ts:2-3` (TOOLBAR-129, -130, file header) | the tooltip keyframes (`:508-530`) and the animating-rows rule (`:244-257`), carved out as named constants (below) |
| `src/core/preview/styles/propertiesStyles.ts:3-4` (TOOLBAR-129, -130 on the properties/motion constant) | the motion rules of that file that do these behaviours, carved out; if no rule there does them, drop the markers |
| `pageChromeStyles.ts:146-151` block on `PAGE_CHROME_CSS` (LIFE-049, TOOLBAR-001, TOOLBAR-025) | LIFE-049: drop it (its code points `previewStatus.ts:27`, `statusRegion.ts:29`, `pageDocument.ts:44` already carry it); TOOLBAR-001 and TOOLBAR-025: the toolbar-rows rules and the sticky-band rules, carved out |
| `src/core/preview/styles/contentLayoutStyles.ts:82-90` (TOOLBAR-003, -025, -037, -045, -133) | the fold chevron rules (003), the band alignment (025), the TOC column and rail (037, which takes 133's ID), the TOC entry rules (045), carved out |
| `src/page/modules/toolbarCollapse.ts:13-16` on `installToolbarCollapse` (TOOLBAR-007, -130, LIFE-169, -170) | TOOLBAR-007 -> `apply` (`:52`); TOOLBAR-130 -> `markAnimating` / `startHint` (`:78`, `:114`); LIFE-169 -> the line that posts the preference; LIFE-170 -> the line that reads the initial value |
| `src/page/modules/tocColumn.ts:8-12` on `installTocColumn` | TOOLBAR-033 -> `apply` (`:380`) and the toggle handler; LIFE-169 / LIFE-170 -> the posting and initial-read lines; the specific markers at `:74`, `:145`, `:193`, `:229` stay |
| `src/page/modules/headingFold.ts:49-52` on `installHeadingFold` | 003 -> `toggle` (`:190`) / `setToggle` (`:118`); 004 -> `persist` (`:112`); 005 (now 003) -> `foldAll` / `unfoldAll` (`:198`, `:209`); 006 -> `reveal` (`:258`) |
| `src/page/modules/findBar.ts:113-118` on `installFindBar` | 010 -> `paint` / `findMatches` / `move` (`:243`, `:275`, `:362`); 011 (now 010) -> `toggleOption` (`:375`); 012 -> `runReplace` (`:423`); 014 (now 012) -> `updateReplaceState` (`:207`); 131 (now 012) -> `updateNote` and `scheduleDryRun` (`:192`, `:337`); 009 -> the open/keydown handler |
| `src/session/sessionFactory.ts:51` (LIFE-049 on `createSession`) | drop LIFE-049 there; LIFE-038, TRUST-001 and TRUST-007 stay |
| `src/host-memory/memoryLogger.ts:18` (LIFE-002 on the in-memory test host) | drop it; the product points `src/host-api/logger.ts:25` and `src/host-vscode/vscodeHost.ts:334` keep it |

**CSS split.** Carve each named rule group out of its constant as its own module-local constant
(for example `TOOLBAR_TOOLTIP_CSS` and `TOOLBAR_ROWS_MOTION_CSS`). Each new constant gets its
markers in a comment above it, never inside the CSS string. The parent constant interpolates the
pieces at the exact place the rules were, so the cascade order is unchanged.

- Proof: the joined `PREVIEW_THEME_CSS` (`src/core/preview/previewStyles.ts`) is byte-identical
  before and after. Compare it once with a scratch script; do not add a test for it.
- Keep the new constants unexported unless a test already imports the parent (the unused-exports
  check).
- Keep each file under the file-size ratchet (800 lines in `src/`).

Test markers (`test/`):

- **No marker today.** Add a marker beside each test that checks a scenario:
  - `test/core/state/navigationHistory.test.ts` lines 31, 42 and 62 -> `@tests_req` TOOLBAR-059,
    which takes TOOLBAR-065's ID;
  - `test/page/modules/tocColumn.test.ts`:
    - lines 160, 203, 226, 305, 351, 388, 401 and 415 -> TOOLBAR-033, -040 or -045, by the scenario
      each checks;
    - line 240 (the toggle opens the TOC) gains TOOLBAR-033 next to LIFE-169.
- **Header blocks.** Spread each block onto the tests it names; each test gets the IDs of the
  scenarios it checks:
  - `test/security/package-contract.test.ts:34-40`: LIFE-003, -018, -032, -001 and -156, in the
    blocks of this CR; DIAG-024 and PALETTE-001 belong to other CRs;
  - `test/integration/findInPreview.test.ts:72-76`: 009, 010 and 012 after the merges;
  - `test/integration/exportHtml.test.ts:46-47`.
- **Companion file `test/integration/realInput/markers.ts`.** Remove the entries of this CR and put
  each marker on the scenario function that checks it, or name that scenario in the companion,
  following the format of the req-marker-gate rule:
  - `SwRS-LIFE-151` -> `scenarioPreviewGroupLock` (`previewWindow.ts:445`);
  - `SwRS-TOOLBAR-077` -> `scenarioLinkClickEditsInEditMode` (`linkEditMode.ts:75`), or
    `scenarioFlushBeforeLink` (`flushBeforeNavigate.ts:235`), whichever clicks a link;
  - `StRS-LIFE-001` -> `scenarioPreviewGroupLock` or `scenarioTitleBarButton` (`previewWindow.ts:200`);
  - `StRS-TOOLBAR-013` -> `scenarioToolbarState` (`previewWindow.ts:216`, RI-T38 anchor button).
- **Moved tests:**
  - the host-side replace tests in `test/session/reviewReqThreads.requirements.test.ts:117,128,148`
    move to a find/replace test file in `test/session/` (new or existing), with their markers;
  - the TOOLBAR-090 test at `test/core/preview/toolbarReq.requirements.test.ts:25` moves to the
    link-navigation tests.
- **Duplicates.** `src/page/features/scrollCore.ts:498-499` and `hostToPage.ts:369-371` carry
  merged IDs: after the supersede, one marker per ID per point.

**Marker gate baseline.** Remove from the req-marker-gate baseline every entry this CR clears.
`just check` passes with the smaller baseline, and no entry of the two scopes is left unless it is
listed in the PR body with its reason.

## 5. Validation tests and scenario tests

StRS validation markers (`@tests_req StRS-MDOKFSTUDIO-...`) go on a real scenario, never in a
companion list:

| StRS | Validation test |
| --- | --- |
| LIFE-021 | `test/security/package-contract.test.ts`: the test at `:39` that reads the contributed configuration (groups and their order). VS Code draws the settings editor from that contract, and no integration test opens the settings editor. |
| TOOLBAR-002 | `check_heading_fold` in `test/visual/capture_layout_checks.py:207` (Fold button, folded block height, chevron) |
| TOOLBAR-003 | `run()` of `test/integration/findInPreview.test.ts` (`:77`, real VS Code window, find and replace) |
| TOOLBAR-014 | `test/integration/exportHtml.test.ts` (command, warning, embedded image and diagram, cancel writes nothing) |
| New closing StRS | `test/integration/workspaceDisposal.test.ts:28` (moved from LIFE-014) |
| TOOLBAR-001 (extra) | `test/integration/reload-suite.ts` `runReloadCampaign`, only if a step there asserts the collapsed toolbar after the reload; otherwise none is added |

The 12 other StRS keep their validation tests (the audit's table, column "Validation test?").

Add tests for the scenarios that no test checks. Each new test carries the `@tests_req` of its
SwRS. Place it in the existing test file of that behaviour (unit, page, session or integration, as
the scenario needs).

- SwRS-LIFE-038: "Two previews" and "Same document twice".
- SwRS-LIFE-024: the title after a switch of the active file.
- SwRS-LIFE-026: the text "Following the active Markdown editor." and the came-back branch
  (`watchPageEditor`).
- SwRS-LIFE-032: the `previewRefresh` handler, for a current render and for a stale render.
- SwRS-LIFE-039: "Source gone".
- SwRS-LIFE-044: the settings scenarios beyond reading the configuration.
- SwRS-LIFE-069: the `incrementalUpdates` off path.
- SwRS-LIFE-119: the host rule (stored anchor, else the editor's first visible line, else none).
- SwRS-LIFE-125: the field bounds of an invalid state report.
- SwRS-LIFE-108: the accepted shape of `previewScroll` / `previewReveal`.
- SwRS-LIFE-169: the stale-message drop; the palette mode in Restricted Mode.
- SwRS-LIFE-127: "File outside a folder".
- SwRS-LIFE-004: idle stop. SwRS-LIFE-049: the exact pending message of a first Open With render.
  SwRS-LIFE-170: Cream for an unknown stored theme.
- SwRS-LIFE-149: the "Studio settings" scenario (today checked by reading only).
- SwRS-TOOLBAR-001:
  - title = tooltip for every toolbar button, not 3;
  - the keyboard-focus tooltip;
  - where a visual check can measure them: the 12/14 px offsets and the covering of scrolled text.
- SwRS-TOOLBAR-054: the render gate "Another render" (from 058) and the nominal "current render" row
  (from 056).
- SwRS-TOOLBAR-077: the auxclick button-2 refusal; the warning text.
- SwRS-TOOLBAR-094: the second-root relative case. SwRS-TOOLBAR-090: the malformed-escape row.
- SwRS-TOOLBAR-120: the initial state; "Own document" (from 122).
- SwRS-TOOLBAR-030: "Scroll to the end".
- SwRS-TOOLBAR-006: "The browser find opens the section", only if a page or visual test can drive
  it.

A scenario that no test can check at a reasonable cost is not forced. Its SwRS verification note
says so in one line, and the PR body lists it.

## 6. Use case diagrams (one per StRS, 17)

Write them per the req-use-case-diagrams rule, from the audit's sketch (section 6 of each StRS):

| StRS | Kind | Content |
| --- | --- | --- |
| LIFE-001 | actors | Writer, Reader, VS Code built-in preview; Open Preview to Side (command, Explorer, title, key), Open With tab, refused file, coexistence, several previews |
| LIFE-003 | sequence | active editor changes -> eligibility -> newest following preview pending -> render -> title -> Refresh -> render from buffer -> place kept |
| LIFE-005 | sequence | edit or outside change -> debounce -> worker render (stop if superseded) -> patch in place and glow / new page -> ready (timeout: full document) |
| LIFE-007 | state | Pending, Ready, Pending notice, Failed (last good page kept), Recovered, Source missing |
| LIFE-010 | sequence | editor scroll -> first visible line -> page scrolls -> echo ignored -> preview scroll or click -> top line -> editor reveals -> anchor restored after a patch |
| LIFE-014 | state | Open -> Serialized (reload) -> Restored at its place, or Source missing; view choices stored and read back |
| New closing StRS | state | Open -> Closed (render stopped, watchers and Problems entries removed); Open -> Folder removed (restricted reads) -> Folder added back |
| LIFE-021 | sequence | Reader opens Settings -> VS Code lists the contributed groups in order, with defaults and descriptions |
| TOOLBAR-001 | state | Expanded <-> Collapsed; stored for the workspace; initial state panel > workspace > collapsed; load hint once |
| TOOLBAR-002 | state | Open <-> Folded; Fold all / Unfold all; folded -> open when find or navigation targets inside; kept across patch and reload |
| TOOLBAR-003 | sequence | Cmd/Ctrl+F -> bar -> matches and count -> Enter walks -> Replace all dry run, skipped count -> host edits the source spans in one undo step (refused while a block editor is open) -> counts |
| TOOLBAR-004 | sequence | scroll -> heading path up to the depth -> band, one line each -> shadow -> setting change gives a new page |
| TOOLBAR-006 | state | Closed <-> Open column / Open rail (pane < 760 px); current entry follows; click; twisty; stored |
| TOOLBAR-009 | sequence | typing in a block editor, link click -> save flushed -> place recorded -> target opened -> history state -> Back / Next |
| TOOLBAR-011 | sequence | link in view -> batches of up to 64 -> host classifies and resolves -> tooltip or warning icon -> click -> open, hand to the OS, or warn |
| TOOLBAR-013 | sequence | pairing -> Anchor pressed -> mode stored, preview aligned -> editor scroll -> cursor line (setting on) -> block outlined |
| TOOLBAR-014 | sequence | Export -> diagrams awaited, snapshot -> link warning (cancel) -> save dialog (cancel) -> styles, theme, images, math embedded, no script -> one file |

Each diagram states what the code does today, and no arrow names a behaviour that no SwRS of the
StRS specifies.

## 7. Records

- `just requirements-update`. Commit the generated fields, indexes and Links blocks; never edit
  them by hand.
- One dated entry in `requirements/tiers/log.md`, in a `### Topic` sub-heading under `## 2026-MM-DD`
  of the day. It holds the old-to-new mapping of section 1, the reparenting, the new StRS, the
  markers moved, the tests added, and what was not done and why.
- Commits use the types `docs`, `test` or `refactor` (no scope; the scopes are for `feat` and `fix`).
- No `CHANGELOG.md` line ("No user-facing change").
- The PR body's Tests section lists the requirement IDs added or changed, with their source and
  test files. It has no "Approved requirements changed" section unless open question 3 changes
  that.

## Out of scope

- Deleting any requirement (owner: never), and `okfreq retire`.
- Lifecycle `draft` -> `proposed` without the owner's word (open question 1).
- The `derives_from` of the 13 deprecated LIFE and 3 deprecated TOOLBAR SwRS that still list
  in-force StRS (audit, finding L). Retired requirements are not edited.
- SwRS-DIAG-128's implementation marker (req-marker-gate).
- The StRS of other scopes, and their derivations of LIFE-169/170, LIFE-026 and LIFE-062
  (section 3, "Left as they are").
- TRUST-006 and TRUST-063/065 (req-garden-core-diagrams-trust), and moving SwRS-LIFE-173 to
  block-editing (open question 2).
- The missing "published site" StRS of the cross-cutting audit (req-garden-core-diagrams-trust).
- Any product behaviour change; a bug found on the way goes to the backlog as "Known issue".

## Evidence that proves it

Run in the CR's worktree, after `just dev`:

- `uv run --no-sync --group requirements okfreq validate --check-links --project-root .` and
  `just requirements-lint`. Both pass. The last line of `check_main_paths` is
  `main paths: <n> StRS checked, ... all valid`, where `<n>` is the count before plus the new StRS
  if it has a path.
- `just requirements-update` leaves no diff after the commit (`okfreq update-coverage --check`
  and `okfreq lint --check` clean).
- `uv run --no-sync --group requirements okfreq trace requirements --json`:
  - each superseded ID of section 1 has no marker left;
  - every in-force SwRS of the two scopes has at least one `@implements_req` (or a justified
    exemption) and one `@tests_req`;
  - every in-force StRS of the two scopes has a validation marker on a real test.
- `grep -rn "@implements_req\|@tests_req" src test`: no marker of the two scopes sits on a file
  header, on an `install*` function or on a whole CSS aggregate.
- `just check` passes: marker gate with the smaller baseline, unused exports, file size and
  boundaries.
- The scratch comparison shows `PREVIEW_THEME_CSS` byte-identical before and after the CSS split.
- The new tests pass. Each was seen to fail on purpose once (a broken assertion) before it was
  kept, as the evidence that it checks something.
- `just preflight` passes; on Windows that is the static stage, and CI runs the others.
- The PR's CI is green on the simulated jobs.
- Counts in the PR body: toolbar-navigation and lifecycle-sync in-force SwRS before and after
  (50 -> 34, 34 -> 30 expected), 16 -> 17 in-force StRS, and 17 diagrams.

No CI job is added or changed.

## Open questions (for the owner)

1. **Draft -> proposed.** StRS-TOOLBAR-002 and -003, and SwRS-TOOLBAR-003, -004, -006, -008, -009,
   -010 and -012 (and -005, -011 and -014 before their merge), are `draft` yet implemented and
   tested. Should this CR set them to `proposed`? Recommendation: yes, which closes the "draft on
   the default branch is a gap" finding.
2. **SwRS-LIFE-173 (Save key)** sits in lifecycle-sync but derives only from StRS-BLOCK-008. Keep
   the scope mismatch, or move it to block-editing (a new ID by `okfreq new`, then supersede)?
   Recommendation: keep it, since a new ID only to change folders adds churn. req-garden-block-table
   may decide the same.
3. **SwRS-TOOLBAR-002 into SwRS-TOOLBAR-025.** The audit marks this merge "optional" (the shadow is
   part of the band's look). This specification merges it. Keep the merge, or leave TOOLBAR-002 on
   its own?
