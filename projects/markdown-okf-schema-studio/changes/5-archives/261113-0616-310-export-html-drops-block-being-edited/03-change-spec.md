# Change Specification: Export to HTML keeps what is under an open editor

Status: automatable (the owner does not review this specification). Code read at `origin/main`
(`cb968299 chore: version 1.7.1`). Cut the worktree from `origin/main`, not from the local `main`.
Project rules: `.agents/constitution.md`, `AGENTS.md`, `requirements/guidelines/requirements.guidelines.md`
and `requirements/guidelines/project.guidelines.md` ("During a change").

## Goal

A reader who exports the page to a single HTML file while an editor is open (a block editor, the
table cell editor, a front matter editor) finds the content under that editor in the file, shown as
it was last rendered. The export does not close or commit the editor. SwRS-MDOKFSTUDIO-TOOLBAR-137
loses its Known issue row and describes this behaviour.

## Premise, corrected (from the advisor report, adopted)

The Known issue in TOOLBAR-137 says "the block being edited is missing from the file". The code
does not match it for a block:

- A block under the block editor stays in the page, hidden by `data-sphinx-preview-editing="true"`
  (`src/page/features/blockEditor.ts`, around line 289; the editor frame is a sibling inserted
  `afterend`). The export removes the frame (`data-sphinx-preview-block-editor`, in
  `REMOVED_BY_ATTRIBUTE` of `src/core/export/exportContent.ts`) and `stripAttributes` drops every
  `data-sphinx-preview-*` attribute not in `KEPT_PREVIEW_ATTRIBUTES`. A hand-made probe exported the
  block. It is not missing.
- A **table cell** under the cell editor is the real loss. `hideTableCellContent`
  (`blockEditor.ts`, line 19) moves the cell's content into
  `<span data-sphinx-table-cell-content="true" aria-hidden="true">`. The export keeps that span and
  its attribute (`data-sphinx-table-cell-content` is not a `data-sphinx-preview-` attribute), and the
  exported style sheet keeps the rule of `src/core/preview/styles/editModeStyles.ts` (line 324):
  `[data-sphinx-table-cell-content="true"] { height: 0; visibility: hidden }`. The cell is in the
  file but cannot be seen.
- A likely third case, found while writing this specification: the front matter key and value
  editors (`src/page/features/frontmatterEditor.ts` line 294, `frontmatterValueEditor.ts` line 297)
  set `hidden` on the display element (`.okf-name-cell`, `[data-okf-value-display]`). The export
  keeps `hidden` (only `unfold` removes it, and only on `data-okf-folded`), so the key or value under
  the editor would be invisible once the properties `details` is opened.

The advisor's probe used hand-written DOM. The reproduction (step 1) is the authority: the
specification's rule holds for whatever case it shows.

## Decisions carried from 02-answers.md

1. **What the file shows (USER-IMPACT, owner approved 2026-11-12):** a block or cell being edited is
   exported in its last rendered state, which is the text already autosaved to the document (about
   400 ms behind the typing). The editor stays open; the export neither closes nor commits it. No
   flush or save is triggered by Export.
2. **First step (INTERNAL, adopted):** reproduce before fixing, with a page-level test that opens the
   real editors and feeds the snapshot to `buildHtmlExport`.
3. **Fix location (INTERNAL, adopted):** host side, in `removeChrome` of
   `src/core/export/exportContent.ts`. The page snapshot (`takeExportSnapshot` in
   `src/page/modules/exportSnapshot.ts`) stays a plain clone.
4. **Other editors in the same test (INTERNAL, adopted):** front matter value editor, a block editor
   opened inside a card, a `{list-table}` edited as raw Markdown (`blockSourceEditor.ts` line 119).
5. **Requirement (INTERNAL, adopted):** TOOLBAR-137 describes the real behaviour; log entry says the
   Known issue was wrong for blocks if the reproduction confirms it.
6. **Visual scenario (INTERNAL, adopted):** one scenario with a cell editor open, because the loss is
   visual (CSS) and a DOM-only test passes with the bug.
7. **Batch:** the release is v1.8.0; this CR's commits are typed `fix:` (and `test:`/`docs:` where
   they only touch those). The batch ships as one stack; this CR's suggested place is after
   `alert-followed-by-heading-taken-as-title` and before `sticky-heading-long-title-wraps`.

## What changes

### 1. Reproduction test (write it first, see it fail)

In `test/page/modules/exportSnapshot.test.ts` (or a new `test/page/exportWhileEditing.test.ts` if
the file grows past the size check), using `createRuntimeHarness` and the helpers of
`test/page/runtimeTestSupport.ts` (`openTableCellEditor`, `openBlockEditorWithSource`; see
`test/page/runtimeTableCellEditor.test.ts` for a cell set up with rendered content):

- open each editor, take `control.snapshot()` (or `takeExportSnapshot`), pass it to
  `buildHtmlExport` (`src/core/export/htmlExport.ts`), and assert on the written body;
- cases: a paragraph under the block editor; a table cell under the cell editor; a front matter
  value under the value editor and a key under the key editor; a block editor opened inside a card;
  a `{list-table}` edited as raw Markdown (the table hidden, the frame after it);
- each case asserts: the rendered text of the edited target is in the body; no editor chrome
  (no `textarea`, no `data-sphinx-preview-block-editor`, no `data-okf-frontmatter-editor`); and the
  target carries nothing that hides it in the file: no `data-sphinx-table-cell-content`, no
  `hidden` on it or an ancestor inside the content, no `aria-hidden="true"` on it;
- after the snapshot, the editor is still open (`state.activeBlockEdit` or the frame still in the
  page) and its text is unchanged: the export neither closes nor commits it.

Record which cases fail on `origin/main` in the CR's work notes; the fix covers every failing one.

### 2. The fix, in `src/core/export/exportContent.ts`

In `removeChrome`, next to the find-mark unwrap:

- unwrap an element with `data-sphinx-table-cell-content` (its children go back into the cell, the
  span goes, so the CSS rule matches nothing);
- for a front matter display element hidden by an open editor (`.okf-name-cell` or
  `[data-okf-value-display]` with `hidden`, inside a cell with `data-okf-editing="true"`), remove
  `hidden`; strip `data-okf-editing` and `data-okf-key-editing` as editing attributes (add them to
  `REMOVED_ATTRIBUTES`);
- any further case the reproduction shows is fixed in the same place by the same rule (the edited
  target shown in its last rendered state, its editor removed).

Keep the `// @implements_req SwRS-MDOKFSTUDIO-TOOLBAR-137` marker on `removeChrome`; update its doc
comment ("content under an open editor is shown as last rendered"). No change to
`src/page/modules/exportSnapshot.ts`, to the editors, or to the style sheets.

### 3. Unit tests, `test/core/export/htmlExport.test.ts`

Add `// @tests_req SwRS-MDOKFSTUDIO-TOOLBAR-137` tests with hand-written content (in the style of
"review comments, controls and editing chrome are left out"):

- a `td` holding `<span data-sphinx-table-cell-content="true" aria-hidden="true"><strong>y</strong></span>`
  and a `div data-sphinx-preview-block-editor` exports as a `td` holding `<strong>y</strong>` and no
  editor;
- a `<p data-sphinx-preview-editing="true">` followed by an editor host exports the paragraph (pins
  the block case that already works);
- a properties value cell with `data-okf-editing="true"`, a hidden `[data-okf-value-display]` and a
  front matter editor exports the display element without `hidden` and without the editor.

### 4. Visual scenario

Add one scenario to `test/visual/exportHtmlScenarios.ts`, next number `toolbar-navigation/v44`,
with `// @tests_req SwRS-MDOKFSTUDIO-TOOLBAR-137`: a page with a table whose cell editor is open
when the file is exported, the exported file opened with JavaScript off, the edited cell's text
visible.

- The export content must hold the real DOM of an open cell editor. Preferred: in
  `test/visual/renderFixtures.ts` (`writeExportFile`), for this scenario open the static page in
  headless Chromium as `drawnContentHtml` (`test/visual/drawnContent.ts`) does, turn edit mode on,
  click the cell (the content is wrapped when the editor opens, before any source arrives), and read
  `#sphinx-myst-preview-content`. If the page script cannot open the editor without a host, apply the
  same markup as `hideTableCellContent` to the static content and say so in the scenario description.
- Use a new small fixture (a table with a known cell text) rather than adding a table to
  `87-export-html.md`, so the baselines of v42 and v43 do not move.
- In `test/visual/capture_export_html.py` (`check_export_html`), add a check that runs only for a
  scenario that declares the edited cell text (a new scenario field, passed through the manifest
  like `exportFile`): the cell's text is visible (`is_visible()`, non-zero height) in the exported
  file. The checks written for fixture 87 (properties, tabs, Mermaid, image) must not run on the new
  fixture: gate them on the fixture or move them behind a scenario field.

### 5. Requirement and log

- `requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-137.md`: replace the row
  "A block editor is open | Known issue: ..." by the behaviour, for example
  "A block, table cell or front matter field is being edited | It is written as last rendered (the
  text autosaved so far); the editor stays open and nothing is saved by the export". Update the
  Verification notes (the new tests, scenario v44) and `tested_in_files` if a new test file is
  added. StRS-MDOKFSTUDIO-TOOLBAR-014 is unchanged.
- `requirements/tiers/log.md`: a dated entry (2026-11-12 section or the day of the change) with the
  CR name: TOOLBAR-137 amended, Known issue removed; state that the Known issue was wrong for a
  block (it was exported) and the real loss was the table cell (and the front matter field, if the
  reproduction confirms it).
- Run `just requirements-update`.

### 6. Changelog

One line under `## Unreleased` in `CHANGELOG.md`, user words, for example: "Export to HTML keeps
the content of a table cell or front matter field that is being edited, as last saved; the editor
stays open." Follow the rule set by `changelog-line-in-each-pr` if it has landed lower in the stack.

## Out of scope

- Closing, flushing or committing an editor on Export (decision 1).
- Exporting the unsaved keystrokes of the last 400 ms.
- Any change to the editors, the page snapshot or the preview and export style sheets.
- The writing skill: no rendered syntax changes.
- Open VSX and the other CRs of the batch.

## Evidence

- The reproduction test fails on `origin/main` for the cell case (and any other case it shows) and
  passes after the fix; the block case passes before and after.
- New unit tests in `test/core/export/htmlExport.test.ts` pass.
- Visual scenario `toolbar-navigation/v44` passes in `just ci-visual`: the edited cell's text is
  visible in the exported file opened with JavaScript off; v42 and v43 unchanged.
- `just requirements-lint` and `just requirements-update` clean; TOOLBAR-137 has no Known issue row.
- `just check`, then `just preflight`, pass.

Scenario steps (manual, in a real VS Code window, for the PR):

1. Open a Markdown file with a table and a front matter, turn edit mode on.
2. Click a table cell, type a word, wait one second (autosave), keep the editor open.
3. Run Export to HTML; save the file. The cell editor is still open, with the caret in place.
4. Open the file in a browser: the cell shows the typed word; no editor control is in the page.
5. Repeat with a front matter value editor open and with a paragraph's block editor open.

## Open questions

None.
