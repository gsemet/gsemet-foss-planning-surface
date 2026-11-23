# Audit sample: do direct StRS test markers walk a main path?

- Date: 2026-11-23
- Repository read: `markdown-okf-schema-studio` at `main` (d762a732), read-only.
- Method: systematic 1-in-6 sample of the 185 `@tests_req StRS-` markers under `test/`
  (31 of 185, list in `01-audit-sample-list.txt`). For each marker: the annotated test (function,
  scenario object, or the check block the inline marker heads) was read, then the `### Main paths`
  of the StRS. For visual scenarios the runner was read once: `test/visual/scenarios.ts` (fields),
  the `capture_*.py` checks (`codeCopyChecks`, `figureAnchorChecks`, `pasteImageChecks`,
  `topSpacingChecks`), `contentAssertions` (DOM assertions on one rendered state) and `pageActions`
  (clicks, keys). `scroll` only sets the captured position. Host answers in visual scenarios are
  faked by the Python check (`window.visualMessages`, injected result messages).
- Bench: `real VS Code` = `test/integration/**`, run by `just ci-integration` ->
  `npm run test:integration` -> `out/test/integration/run-tests.js`, which launches VS Code for
  `scroll-sync-suite`, `untrusted-suite`, `trusted-suite` (imports the `*.test.ts` files and
  `realInput/run.ts`, which runs `realWindowGaps.ts` too) and `standalone-suite`. `simulated` =
  visual/Playwright static page, Python build tests, Node contract tests.

## Rubric

- `path`: the test walks one StRS main path from its first step to its final result (all or nearly
  all steps exercised in sequence), asserting the end result. Rows marked "1-step" walk a path that
  has a single step: there the path and its one SwRS are the same check.
- `partial-path`: it chains two or more steps of a path but not the whole path.
- `snapshot`: it sets up one state (fixture, scroll position, theme) and checks/captures that single
  state; no user step sequence.
- `swrs-duplicate`: it checks one transition, which a SwRS marker on the same test or a SwRS test
  elsewhere already covers.
- `other`: anything else (said in the reason).

## Table

| # | file:line | StRS | paths | class | bench | other markers on the test | reason |
|---|---|---|---|---|---|---|---|
| 1 | test/build/test_plugin_manifests.py:93 | CORE-006 | 1 | swrs-duplicate | simulated | SwRS-CORE-074, CORE-075 (module level) | Static check that the manifests name one plugin and one skill folder: step 1 only, which is SwRS-CORE-074 on the same module. |
| 2 | test/integration/blockMove.test.ts:36 | BLOCK-025 | 2 | other | real VS Code | StRS-BLOCK-014; SwRS-BLOCK-117, TRUST-065, BLOCK-124, BLOCK-127, BLOCK-156; inline StRS-TRUST-009 | Walks a block move (refusals, swap, inverse move, one undo) sent as page messages; neither BLOCK-025 path (type-and-undo, cut-and-paste) is a move. Overlap only with the refusal options SwRS-BLOCK-124/127, marked on the same test. |
| 3 | test/integration/commentWrite.test.ts:121 | TRUST-009 | 2 | swrs-duplicate | real VS Code | run(): StRS-REVIEW-001, REVIEW-003; SwRS-REVIEW-004, REVIEW-012, REVIEW-054, REVIEW-065, REVIEW-074, TRUST-065, TRUST-090 | Inline block: a comment create for another document is dropped. That is the refusal option of path 1 step 2, SwRS-TRUST-065, marked on the same run(). |
| 4 | test/integration/editToolbarCover.test.ts:86 | PALETTE-005 | 2 | swrs-duplicate | real VS Code | SwRS-PALETTE-021 | Opens a text box and the figure form, measures that the palette sits above the frame, closes with Escape. Path 1 step 1 only (SwRS-PALETTE-021 on the same test); no control pressed, no commit. |
| 5 | test/integration/labelRename.test.ts:35 | MYST-009 | 2 | partial-path | real VS Code | SwRS-TRUST-065, MYST-045 | Path 2 steps 2 to 4: an injected rename message, the label line changes, one undo, stale line refused. Step 1 (click the anchor icon, popover) is skipped; steps 2 and 3 both name SwRS-MYST-045, marked here. |
| 6 | test/integration/mystDiagnostics.test.ts:47 | MYST-007 | 2 | path | real VS Code | SwRS-MYST-078 | Path 1: document using colon_fence plus conf.py, preview opened, one warning in the Problems view at the first use line naming the extension; then conf.py edits and close/reopen. |
| 7 | test/integration/previewEditing.test.ts:44 | FMSCHEMA-001 | 2 | swrs-duplicate | real VS Code | SwRS-FMSCHEMA-001 | Step function asserting the rendered HTML has the properties table rows: path 1 step 1 only, SwRS-FMSCHEMA-001 on the same function; no fold toggle. |
| 8 | test/integration/radioChoice.test.ts:187 | GFM-005 | 1 | path | real VS Code | SwRS-GFM-041, BLOCK-041 | Radio group rendered (3 radios asserted), real click on an unselected option, two source lines change, selection shown; then undo, keyboard and editor-open refusal. |
| 9 | test/integration/realInput/blockKeys.ts:606 | TABLE-015 | 1 | path | real VS Code | SwRS-TABLE-085 | Real keys: cell editor opened, text selected, Ctrl/Cmd+B (a shortcut, not the bar button), Enter, buffer holds `**one**`, editor closed. |
| 10 | test/integration/realInput/editorWidgets.ts:770 | BLOCK-001 | 2 | swrs-duplicate | real VS Code | SwRS-BLOCK-001, LIFE-172 | Turns edit mode on and checks no reflow, then checks a reopened preview starts off (LIFE-172, not a path step). Path 1 step 2 (Edit again, save, clear) not walked; step 1 is SwRS-BLOCK-001 on the same test. |
| 11 | test/integration/realInput/flushBeforeNavigate.ts:309 | TABLE-001 | 2 | path | real VS Code | none | Path 1 with real input: click a cell, editor opens, type, leave the cell by switching the editor tab, the typed text reaches the buffer. Then a frontmatter field (another StRS). |
| 12 | test/integration/realInput/previewWindow.ts:200 | LIFE-001 | 2 | swrs-duplicate | real VS Code | none | Clicks the title-bar book icon and waits for the side preview: path 1 step 1 only (group lock not checked). Step 1 is SwRS-LIFE-003, tested in test/host/lifeReq.requirements.test.ts and diffPreview.requirements.test.ts. |
| 13 | test/integration/realInput/tableInsertSlash.ts:41 | TABLE-016 | 1 | path | real VS Code | SwRS-TABLE-106, TABLE-111 | Real keys: `/tab` with a 3 x 2 size, `/align` Center on the first column, Ctrl/Cmd+Enter; the buffer holds the aligned table once. |
| 14 | test/integration/realInput/textEditing.ts:742 | PALETTE-007 | 2 | other | real VS Code | none | Walks the link panel (Ctrl/Cmd+K, Escape, reopen, insert, undo). The StRS normative text covers links, but its two main paths are Insert an image and Colour a selection. |
| 15 | test/integration/realWindowGaps.ts:669 | TRUST-001 | 1 | swrs-duplicate | real VS Code | StRS-BLOCK-001 | Restricted Mode window: Edit button enabled, edit mode turns on, capture. Step 1 only, no write (step 2); SwRS-TRUST-001 is tested in commentWrite.test.ts runUntrusted and untrusted-suite.ts run(). |
| 16 | test/integration/serializer.test.ts:28 | LIFE-014 | 2 | path (1-step) | real VS Code | StRS-LIFE-001, LIFE-007; inline SwRS-LIFE-127, LIFE-062, LIFE-038, LIFE-024 | Path 1 has one step: the deserializer is called (through a test hook, not a real reload) with a saved state, and the preview shows the file at the saved line and scroll. Same check as inline SwRS-LIFE-127. |
| 17 | test/integration/stockCoexistence.test.ts:76 | LIFE-001 | 2 | path (1-step) | real VS Code | inline SwRS-LIFE-059, LIFE-001, LIFE-149, LIFE-018, LIFE-049 | Path 2 (one step): Open With puts the file in an active Studio tab (inline SwRS-LIFE-018). Path 1 only partly: preview opened beside the stock preview, stock settings unchanged (option LIFE-149); group lock not checked. |
| 18 | test/integration/untrusted-suite.ts:89 | TRUST-004 | 1 | path | real VS Code | SwRS-TRUST-025 | Render-only path: inside image gets a webview address and its folder is a resource root; outside image is absent, its folder not a root, and a diagnostic names it. |
| 19 | test/security/package-contract.test.ts:380 | TRUST-014 | 0 | other | simulated | SwRS-TRUST-092 | The StRS has no `### Main paths` section. The test reads `.vscodeignore` patterns, the same check as SwRS-TRUST-092 on it. |
| 20 | test/visual/releaseShowcaseScenarios.ts:16 | DIAG-015 | 2 | snapshot | simulated | StRS-CORE-001 | One full-page fixture capture; contentAssertions check the chart is drawn as an image and no error state. The steps of path 1 (collapsed source section, page colours) are not asserted. |
| 21 | test/visual/scenarioDefinitions1.ts:1272 | BLOCK-011 | 2 | path (1-step) | simulated | none | Path 2 (one step) through its Enter option (BLOCK-253): empty document in edit mode, Enter, new-block editor open with the focus and Start writing gone (`topSpacingChecks: empty-open`). |
| 22 | test/visual/scenarioDefinitions1.ts:219 | MYST-015 | 2 | snapshot | simulated | SwRS-MYST-001 | Full-page capture of the admonition gallery fixture; no contentAssertions or check flag, only the standard page checks. |
| 23 | test/visual/scenarioDefinitions1.ts:451 | CODE-004 | 1 | path | simulated | SwRS-CODE-017 | `codeCopyChecks`: no button before hover, hover shows it at the corner, click posts the exact code, Copied after the faked host answer. The clipboard itself is host side and not checked. |
| 24 | test/visual/scenarioDefinitions1.ts:784 | FMSCHEMA-006 | 2 | snapshot | simulated | StRS-FMSCHEMA-001; SwRS-FMSCHEMA-006, FMSCHEMA-029 | Capture of the schema-typed frontmatter table; no contentAssertions or check flag. Path 1 step 3 (schema edit used at next analysis) not exercised. |
| 25 | test/visual/scenarioDefinitions2.ts:1092 | TOOLBAR-004 | 2 | snapshot | simulated | SwRS-TOOLBAR-025 | `scroll: stickyHeading` sets one position; `expectedStickyHeadings` and STICKY_SHADOW_ASSERTIONS check the band and its shadow in that state. |
| 26 | test/visual/scenarioDefinitions2.ts:1330 | PALETTE-018 | 2 | path | simulated | none | `pasteImageChecks`: editor opened, synthetic image paste, page posts previewPasteImage, faked host result, reference on its own paragraph with the name selected, undo. Step 2 (host saves the file) is stubbed. |
| 27 | test/visual/scenarioDefinitions2.ts:1475 | TABLE-002 | 2 | snapshot | simulated | SwRS-TABLE-002 | Edit mode on a wide scrolled table; WIDE_ROW_HANDLE_ASSERTIONS check the row handles' place. Path precondition only; no row is moved. |
| 28 | test/visual/scenarioDefinitions2.ts:538 | CORE-001 | 2 | snapshot | simulated | none | README hero capture of one fixture at one scroll position; no contentAssertions. No buffer change (path 1) and no right-to-left text (path 2). |
| 29 | test/visual/scenarioDefinitions2.ts:699 | MYST-009 | 2 | path | simulated | StRS-MYST-017; SwRS-MYST-036 | Render-only path 1: `figureAnchorChecks` asserts the anchor icons (margin, tooltip, text not moved) and that the `{ref}` is an in-page link, then a navigateAnchor message scrolls to the label. |
| 30 | test/visual/scenarioDefinitions2.ts:844 | DIAG-001 | 2 | path (1-step) | simulated | SwRS-DIAG-015 | Path 2 (one step): MERMAID_ERROR_ASSERTIONS check one message, closed parser details, no picture, source kept; plus a theme cycle. Same check as SwRS-DIAG-015 on it. |
| 31 | test/visual/scenarioDefinitions2.ts:975 | THEME-011 | 1 | swrs-duplicate | simulated | SwRS-THEME-043 | Zoom set by `render.zoom`, not by pressing Zoom in; zoomAssertions check font size and column scale (step 2 to 3), which is SwRS-THEME-043 on it. Storage and reopen (steps 3 to 5) not walked. |

## Totals

| class | total | real VS Code | simulated |
|---|---|---|---|
| path | 13 (4 of them 1-step) | 8 (2 of them 1-step) | 5 (2 of them 1-step) |
| partial-path | 1 | 1 | 0 |
| snapshot | 6 | 0 | 6 |
| swrs-duplicate | 8 | 6 | 2 |
| other | 3 | 2 | 1 |
| all | 31 | 17 | 14 |

Paths of more than one step walked end to end: 9 of 31 (rows 6, 8, 9, 11, 13, 18, 23, 26, 29).

## Observations

- Every `snapshot` is a visual scenario (rows 20, 22, 24, 25, 27, 28): one fixture at one scroll
  position, sometimes with no assertion beyond the standard page checks (rows 22, 24, 28). Visual
  scenarios reach `path` only when a check flag runs a scripted sequence (rows 21, 23, 26, 29) or the
  path is render-only (row 30).
- The real VS Code `path` rows that walk several steps are the real-input scenarios and the
  integration tests driven by real clicks or keys (rows 8, 9, 11, 13), plus render-only paths
  checked through the host state (rows 6, 18).
- In the integration tests, `swrs-duplicate` rows are of two kinds: an inline StRS marker heading one
  refusal check inside a larger test (row 3), or a test that stops after step 1 of its path
  (rows 4, 7, 10, 12, 15).
- 4 of the 13 `path` rows walk a path of a single step (rows 16, 17, 21, 30); there the path and its
  SwRS are one check, and rows 16, 17 and 30 also carry that SwRS marker.
- Simulated `path` rows stub the host step with a faked answer (rows 23, 26); row 16 calls the
  deserializer through a test hook instead of a real panel restore.
- Not classifiable as a path walk: row 19 (TRUST-014 has no `### Main paths` section). Rows 2 and 14
  exercise a flow the StRS cares about (block move, link panel) that is not one of its main paths.
  Every sampled marker was read and classified.
