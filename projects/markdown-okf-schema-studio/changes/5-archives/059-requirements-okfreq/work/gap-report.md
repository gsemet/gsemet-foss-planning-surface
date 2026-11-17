Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Gap report (P10.5)

Coverage after P10.4, P10.5 and the audit fix pass (okfreq report; archived SwRS and 22 declarative SwRS are exempt): SwRS source 100% (1841/1841), SwRS test links 99.73% (1836/1841), StRS validation tests 60.0% (138/230 per okfreq), combined 99.73%.
Before this change: no marker existed (0%).

## SwRS exempt from the implementation marker (22, exemption_reason set; behaviour has no TypeScript/JavaScript/Python line)
BLOCK-007 absence of code (edit mode changes no wrapping); DIAG-079 pinned PlantUML version in package.json;
FMSCHEMA-028 absence of a watcher; LAYOUT-035 geometry checks are test tooling (test/shared/geometry-checks.js);
LIFE-002, 014, 015, 016, 017, 167, 168 package.json declarations (engines, menus, keybinding, contributes, setting
descriptions); LIFE-149 absence of code (no markdown.* write); MYST-052 whole renderer plus stylesheet (visual only);
MYST-095 produced by the myst parser/writer library; TRUST-070 negative rule over all strings; TRUST-071, 074, 075,
076, 077, 078, 080 package.json, .nvmrc, lock file, .vscodeignore, esbuild.mjs, icon file.
Decision needed: annotation_exemption with a reason, or a marker file per declarative area.

## SwRS without a test marker (5, need a browser/Playwright test)
DIAG-012, 013, 014, 116 (Mermaid browser entry point: queue, unique ids, late results); DIAG-031 (built-in PlantUML
engine needs nothing outside the extension: real engine in a browser, request log).

## Tests that only approximate the requirement
CORE-030, CORE-039 (stylesheet text, not computed layout), CORE-046 (determinism), BLOCK-019/090/113 (CSS text),
FMEDIT-051 (untrusted branch only), FMEDIT-055 (no real undo), TABLE-072 (no-table branch only), TOOLBAR-087/130/149
(source scans, not browser), LIFE-005/031/105/154/165 (fake host events), THEME/LAYOUT-040/045 (asserted as observed).

## StRS without a stakeholder-validation test (92)
No integration, real-input or visual scenario exercises the use case end to end:
- BLOCK-001 Switch edit mode on and off from the preview
- BLOCK-002 Find edit mode as I left it
- BLOCK-003 Click a block to edit its raw Markdown
- BLOCK-008 Type Markdown with the keys of a text editor
- BLOCK-015 Reorder blocks with the keyboard
- BLOCK-019 Typed text survives updates of the page
- BLOCK-021 Know why an edit, move or paste was refused
- BLOCK-024 Keep the line endings of my document
- BLOCK-025 Preview edits land exactly or not at all
- BLOCK-026 Diagnose an editor that closed by itself
- DIAG-001 Read Mermaid diagrams in the preview
- DIAG-003 Mermaid diagrams stay in place while typing
- DIAG-005 Insert a Mermaid diagram from the edit tools
- DIAG-006 Read PlantUML diagrams without any setup
- DIAG-010 Keep PlantUML pictures in place while typing
- DIAG-014 A runaway PlantUML process cannot hang the preview
- FMEDIT-002 Edit each kind of metadata value with a fitting control
- FMEDIT-009 Refuse metadata edits that break the schema or the document state
- FMEDIT-011 Keep metadata editing separate from other editing
- FMSCHEMA-007 Schema files can be written in several formats and share parts
- FMSCHEMA-009 Schema edits are picked up on the next analysis
- FMSCHEMA-018 Frontmatter links can be followed
- LAYOUT-007 Auto width lets wide content break out of the column
- LAYOUT-009 Layout measurements stay trustworthy for maintainers
- LIFE-001 The writer opens a preview beside the Markdown editor
- LIFE-004 The reader refreshes the preview on demand
- LIFE-006 The preview follows the files and the settings it depends on
- LIFE-008 The preview updates in place
- LIFE-010 Scrolling the text editor scrolls the preview
- LIFE-011 Scrolling or clicking in the preview shows the source line
- LIFE-013 The reader chooses how the panes follow each other
- LIFE-014 The reader finds the previews again after reloading VS Code
- LIFE-016 The Studio runs beside the built-in Markdown preview
- LIFE-018 The preview remembers the reading state of recent documents
- LIFE-019 A preview outside a trusted workspace is safe to read
- LIFE-021 The settings editor lists the Studio settings in clear groups
- LIFE-023 A preview that cannot update in place loads again without losing the place
- MYST-003 Definition lists and inline text roles are typeset
- MYST-006 Maths is typeset offline and bad formulas stay readable
- PALETTE-004 A writer reaches the palette mode choice from the keyboard
- PALETTE-005 The edition palette stays in reach of a long editor
- PALETTE-009 A writer colours text and inserts emoji from pickers
- PALETTE-010 A writer inserts a table of a chosen size from a grid
- PALETTE-011 A writer inserts GitHub Flavored Markdown constructs from buttons
- PALETTE-017 A writer formats text in a table cell from the slash menu
- PALETTE-020 Pasted rich text never brings active content
- PALETTE-021 A writer is told why a picker, list or paste cannot be completed
- PALETTE-022 A writer picks the language of a code block from the languages the preview highlights
- PALETTE-023 A reader of a read-only preview is offered no editing buttons
- PALETTE-024 The palette and its menus appear softly
- PALETTE-025 A palette action that cannot apply leaves the text unchanged and says why
- PALETTE-026 A writer can undo any palette edit in one step
- PALETTE-027 A writer formats with keyboard shortcuts
- CORE-001 Read a faithful rendering of the document
- CORE-002 Compose a document from included files
- CORE-005 Keep the preview usable when a render fails
- REVIEW-005 A comment that cannot be saved keeps its typed text and says why
- REVIEW-014 A writer toggles a TODO note from the keyboard
- REVIEW-015 A writer keeps a discussion in the Markdown source and answers it from the preview
- REVIEW-016 An inline thread is never changed under an open edit
- TABLE-004 A cell edit is cancelled with Escape or Cancel
- TABLE-005 Typed cell text is never lost when the preview leaves the document
- TABLE-007 The usual editing keys work in a table cell
- TABLE-009 Rows and columns are added and removed from the bar
- TABLE-011 A table is converted between pipe, list-table and HTML forms
- TABLE-014 A table is inserted, aligned and captioned from the palette or the slash menu
- TABLE-015 A refused cell open or save is explained in the cell
- THEME-001 Follow the VS Code theme
- THEME-004 Keep my theme choice for the workspace
- THEME-005 Choose a theme or zoom in a read-only preview
- THEME-006 See the whole page in the chosen theme
- THEME-008 Switch themes without animation when motion is reduced
- THEME-009 Get the right colours when the preview loads slowly
- THEME-010 Map the page colours to another host
- THEME-012 Keep my zoom for the workspace
- THEME-013 Ignore a damaged theme setting
- TOOLBAR-003 View choices are remembered for the workspace
- TOOLBAR-010 Back, Next and links never lose typed text
- TOOLBAR-012 The reader sees where a link leads before clicking it
- TRUST-001 A document outside a trusted workspace opens read-only
- TRUST-003 A read-only preview keeps the viewing actions
- TRUST-005 An untrusted workspace runs no script of a document
- TRUST-006 The preview page cannot run foreign code or reach the network
- TRUST-007 Local files display only from the allowed folders
- TRUST-008 Unsafe HTML in a document is removed or made inert
- TRUST-009 What the preview page asks of the extension is checked first
- TRUST-010 The preview page ignores answers not meant for it
- TRUST-011 A message about an older version is never applied to a newer one
- TRUST-012 Visible text speaks of the product, not of its build tool
- TRUST-013 The extension shows its own icon in VS Code
- TRUST-014 The extension is built from pinned and official dependencies
- TRUST-015 The package keeps what the preview loads

# Gaps of block-editing (name: block)

## SwRS not closed by a test
None: the 44 `notest` ids are covered by new tests (page, host session and stylesheet files below).
Some are covered in the unit layer only; the real-browser behaviour stays with the visual and real-input
scenarios already named in their Verification notes (BLOCK-019, -090, -113: the stylesheet rules are
asserted from the CSS text, not computed in a browser).

## noimpl handled by recording (no marker possible)
- BLOCK-007 "Turning edit mode on does not reflow the reading layout": absence of code. Nothing in
  src/ changes the wrapping of rendered paragraphs when edit mode turns on (edit mode adds only the cursor,
  the hover outline and the insert points through CSS and DOM attributes); the soft line breaks of the
  source are collapsed by the HTML rendering itself. Verified by the real-input scenario
  scenarioEditModeNoReflow and the visual scenario block-editing/v04 (real browser needed).

## Known issues asserted
- BLOCK-018 (a link inside a paragraph does not stop the outline of the paragraph)
- BLOCK-024 (a click on a link inside a paragraph opens the editor of the paragraph)
- BLOCK-015 (Enter on a link inside a paragraph opens the editor of the paragraph)
- BLOCK-039 (the "Loading Markdown source…" status line of a block editor is not attached to the frame)
- BLOCK-216 (after a refused open the status line with the reason is not attached to the frame)

## Notes
- The page test file needs `repositoryRoot = path.resolve(__dirname, "../../..")` to be the repository:
  compiled into another outDir it only worked with symlinks of scripts, src, node_modules and package.json next to that outDir.
- StRS-BLOCK-002 and -021 are only partly covered by the located tests (read-only half; refused requests leave the
  document and the clipboard unchanged, the refusal text is not asserted by the integration test).
- No real stakeholder test found for StRS-BLOCK-019, -024, -026 (omitted from the json).
# Gap file of diag (scopes: diagrams, frontmatter-schema, layout-width, theme-zoom)

## SwRS without a new test (notest)

| SwRS | Title | Why no unit test fits | Test needed |
|---|---|---|---|
| DIAG-012 | Mermaid draw passes run one at a time | `mermaidPreview.ts` is a browser entry point (top-level DOM, MutationObserver, native `import("mermaid")`); under `module: NodeNext` the dynamic import stays native and cannot be faked without `--experimental-test-module-mocks` | Page-level test with a Mermaid stub bundle in a real browser (Playwright / visual scenario with a queue probe) |
| DIAG-013 | Mermaid element ids stay unique for the page life | Same entry point (`diagramCounter` is module state, ids are passed to the real Mermaid) | Playwright page test that records the ids given to `mermaid.render` |
| DIAG-014 | A late Mermaid result for a replaced theme is not shown | Same entry point; needs a controlled slow `mermaid.render` and a theme change in between | Playwright test with a delayed Mermaid stub |
| DIAG-116 | A late Mermaid error for a replaced key is not shown | Same entry point; needs a failing, delayed `mermaid.render` | Playwright test with a delayed failing Mermaid stub |
| DIAG-031 | The built-in engine needs nothing outside the extension | Needs the real `@plantuml/core` engine in a browser (theme library, OpenIconic sprite, Smetana layout) and a network/Graphviz absence check | Visual scenario (Playwright) with a themed + icon diagram and a request log |

## SwRS without an `@implements_req` marker (noimpl)

| SwRS | Reason |
|---|---|
| DIAG-079 | Purely declarative: the exact `@plantuml/core` version lives in `package.json` / lock file (tested by `test/security/package-contract.test.ts`); no TypeScript produces it |
| DIAG-080 | Handled: marker in the new `src/page/modules/plantumlBundle.markers.ts` (the behaviour is `esbuild.mjs`, outside the marker source directories) |
| FMSCHEMA-028 | An absence of code: no watcher observes `_schema` folders (tested by `diagReq.settings.requirements.test.ts`, no source line produces the behaviour) |
| LAYOUT-035 | Test tooling: the four geometry checks are `test/shared/geometry-checks.js`, not in a source directory |

## Known issues asserted

- FMSCHEMA-025: a YAML syntax error of a schema is not reported as "Schema could not be parsed" (the test asserts that no such row appears)
- FMSCHEMA-018: an empty frontmatter block still gets the not-a-mapping error row
- FMSCHEMA-028: a schema edit alone refreshes nothing
- FMSCHEMA-045: a preview whose document is not the active editor's is only redrawn, not re-analysed
- DIAG-093: the missing-java message says to set jarPath although it is set (message asserted as written)
- DIAG-104: one process per diagram, all at once
- THEME-014: a failed write of the theme mode is only logged
- LAYOUT-040 / THEME-045: with no anchor yet, the page takes the line at the scroll position (not at the reading line offset); asserted as observed (350 after a 100 px reflow, where an existing anchor gives the resize result)

## Notes

- Page runtime tests (`test/page/diagReq.*.test.ts`) build the page bundle from `repositoryRoot = ../../..` of the compiled file; under a scratch outDir they need symlinks of `scripts`, `src`, `test`, `node_modules`, `package.json`, `tsconfig.json` in the folder two levels above `out/` (done in the scratch dir; no issue under the repo's own `out/`).
- No SwRS text had to be corrected.
# fmtable gap file (frontmatter-editing, table-editing)

## SwRS not closed

None. All 16 `notest` ids of frontmatter-editing (FMEDIT-002, 007, 021, 050, 051, 052, 053, 055, 056, 057, 058, 059, 061, 062, 066, 073) and all 13 of table-editing (TABLE-002, 012, 020, 033, 034, 063, 066, 071, 072, 078, 093, 120, 123) have a new test. The 4 `noimpl` ids of table-editing (TABLE-006, 053, 054, 123) are CSS in the `EDIT_MODE_CSS` template literal: `@implements_req` markers were added in the header of src/core/preview/styles/editModeStyles.ts (above the doc comment of the exported const, not inside the template literal).

Partial coverage worth knowing:
- SwRS-MDOKFSTUDIO-FMEDIT-055: the test asserts one text edit per save (one WorkspaceEdit entry for a value save, add, rename, remove). The Undo step itself (one Cmd+Z reverts) needs a real VS Code window (integration).
- SwRS-MDOKFSTUDIO-FMEDIT-051: the test covers the untrusted-workspace branch (workspace.isTrusted false); the "file outside the workspace" and standalone branch is not run (the host harness opens files inside its workspace).
- SwRS-MDOKFSTUDIO-TABLE-072: the refusal branch of the List table button cannot run (Known issue of the SwRS); only the no-table branch is asserted.

## Known issues asserted

- SwRS-MDOKFSTUDIO-FMEDIT-007 (a date-time field is a plain text input)
- SwRS-MDOKFSTUDIO-FMEDIT-021 (edit mode off discards a typed field value, block editors save)
- SwRS-MDOKFSTUDIO-FMEDIT-050 (no min/max on the number input; out-of-range value refused at save)
- SwRS-MDOKFSTUDIO-FMEDIT-061 (a content patch closes the field editor and loses its text)
- SwRS-MDOKFSTUDIO-TABLE-034 (refused open: only the message shows, no text box)
- SwRS-MDOKFSTUDIO-TABLE-063 (picker, link panel closed at every re-render)
- SwRS-MDOKFSTUDIO-TABLE-072 (button silent when the table text no longer parses)
- SwRS-MDOKFSTUDIO-TABLE-093 (pasted line break splits the row; no paste handler)

## Notes

- Running a custom --outDir needs the repo symlinks next to it (node_modules, src, scripts, tsconfig.json) because the page harness bundles src/page/main.ts relative to the out directory's parent.
# lifecycle-sync (LIFE) gaps

## No @implements_req marker possible (purely declarative, behaviour lives in package.json or is an absence of code)
- LIFE-002 The extension declares VS Code 1.95 as its minimum version: `engines.vscode` in package.json. Tested by test/security/lifeReq.requirements.test.ts.
- LIFE-014 The Command Palette lists the two commands only for .md resources: `menus.commandPalette` when clauses in package.json (tested by package-contract.test.ts).
- LIFE-015 The Explorer context menu offers Open Preview to Side for .md files: `menus["explorer/context"]` in package.json.
- LIFE-016 The editor title bar shows a book button for .md text editors: `menus["editor/title"]` in package.json.
- LIFE-017 Ctrl+K Shift+V opens the preview to the side: `keybindings` in package.json (the command itself is marked LIFE-003/004 in activation.ts).
- LIFE-167 No language and no grammar contributed: an absence in package.json `contributes`.
- LIFE-168 Setting markdownDescription at most 700 characters: package.json settings and the contract test only.
- LIFE-149 Built-in Markdown preview settings not changed: an absence of code (no markdown.* write anywhere); checked by the integration test stockCoexistence.test.ts.

## SwRS without a new test
None: all 41 `notest` ids have a new test (host: test/host/lifeReq.requirements.test.ts with test/host/lifeReqHarness.ts; session: test/session/lifeReq.requirements.test.ts; page: test/page/lifeReq.requirements.test.ts; security: test/security/lifeReq.requirements.test.ts).
Limits of the new tests (the fake host stands in for VS Code; a real-window check would still be manual or integration):
- LIFE-005 only asserts retainContextWhenHidden in the options the panels are created with; that a hidden real webview keeps its page needs a real window.
- LIFE-165 hidden block: the page harness has no per-element display, so a block without height (rectangle.height 0) stands in for display none.
- LIFE-154 / LIFE-031 / LIFE-105 drive the fake panel's view-state and tab-group events; the real VS Code events are integration level.

## Known issues asserted
- LIFE-155 (readOnly stays after trust is granted)
- LIFE-138 (switching back does not restore the remembered state; session.state is undefined)
- LIFE-045 (the ignore check reads the whole absolute path: a path below a tmp folder is ignored)
- LIFE-010 (no text editor active, for example a Studio Open With tab: the command is refused with the message)

## SwRS text corrected
- LIFE-133 scenario "Fixed older panel" described a case that cannot occur (every restored panel follows at the moment it is restored); replaced by "Older panel after a newer restore" and the verification notes updated.

## Environment notes
- Page tests need `scripts/` and `src/` next to the out dir (the runtime harness bundles `src/page/main.ts` relative to the out root); with `--outDir <scratch>/out` symlink both into the scratch dir, and `package.json` for test/security.
# palette-slash gaps

## SwRS not closed
None. All 24 notest ids have a test; the one noimpl id has a marker.

## noimpl
- PALETTE-212 (paste into a table cell stays native): marker added in src/page/features/blockSourceEditor.ts above the block text box paste listener (the cell editor has no paste listener).

## Known issues asserted
None.

## Notes
- Page runtime tests (test/page/paletteReq.requirements.test.ts) need ../../scripts, ../../src next to the outDir (page bundle build); I symlinked them in my scratch dir. NODE_PATH=<worktree>/node_modules was also needed to run from a foreign outDir.
# Gap file: render (code-blocks, rendering-core, gfm, myst)

## SwRS not closed (no @implements_req marker possible)

- SwRS-MDOKFSTUDIO-MYST-095 (Doc and download roles render as plain links): no code of the repo produces it; the
  links and the `reference role unhandled` placeholder come from the myst-to-html writer, and the Known issue is
  precisely that the preview adds no resolution of its own (absence of code). The behaviour IS tested
  (test/core/render/renderReq.myst.requirements.test.ts). Needed: nothing, or an exemption.
- SwRS-MDOKFSTUDIO-MYST-052 (MyST gallery renders without sideways scroll): the SwRS names a visual scenario
  (test/visual/scenarioDefinitions2.ts) and no source file; the result is the composition of the whole renderer and
  stylesheet. Needed: visual (Playwright) scenario `myst/v20..21-myst-gallery-full-*`; no single implementation point.

## Tests that only approximate the requirement

- SwRS-MDOKFSTUDIO-CORE-039 (CJK wrap) and CORE-030 (list spacing): asserted as stylesheet rules (overflow-wrap
  and the 2em / 0.3em rules in PREVIEW_THEME_CSS). The computed layout at 900 px and 460 px needs a visual run
  (the rendering-core cjk-rtl scenarios cover CJK).
- SwRS-MDOKFSTUDIO-CORE-046 (identical HTML in every palette mode): the palette mode is not an input of the render
  (it only reaches the boot context), so the test renders the same document three times and compares; a real
  per-mode check would need the page.
- SwRS-MDOKFSTUDIO-CORE-027 (warm the engine): the "retry after a failed warm-up" part could not be tested (the
  ESM dynamic import cannot be made to fail in the unit runner). The SwRS text was corrected (see below).
- SwRS-MDOKFSTUDIO-CODE-025 (copy in read-only previews): covered at the dispatcher/controller level on a fake
  manager; the untrusted and standalone integration suites (real VS Code clipboard) would still be needed for the
  end-to-end check named in its Verification notes.

## Known issues asserted

- SwRS-MDOKFSTUDIO-CORE-014: an `{include}` with an empty argument makes renderMyst/renderPreviewDocument throw a
  TypeError (the whole render is refused) instead of leaving a placeholder. Known issue added to the SwRS.
- SwRS-MDOKFSTUDIO-CODE-027: the host drop is asserted (the "Copied" feedback part of the Known issue is page-side
  and not asserted).
- SwRS-MDOKFSTUDIO-MYST-094: a label starting with `_`, `.` or `-` swallows the click and opens nothing.
- SwRS-MDOKFSTUDIO-MYST-095: empty link for a role without a label, numref never resolved.
- SwRS-MDOKFSTUDIO-CORE-027: Known issue added (a failed engine load is cached, no retry) but NOT asserted (see above).

## SwRS text corrections

- CODE-005 (diff scenario: the block keeps the hljs class because diff is a registered grammar).
- CORE-014 (Known issue for the empty argument).
- CORE-027 (normative text and description: no retry on the first render; the failure is swallowed; Known issue).
- MYST-043 (the host refuses on a block edit only; a frontmatter edit is refused by the page, scenario rewritten).
- MYST-095 (the label syntax of the examples is `Label <target>`; verification notes now name the unit test).

## Environment note

Page-harness tests that bundle the page (runtimeHarness) resolve the repository root from `__dirname`; with another
outDir they need symlinks of scripts/, src/, package.json, node_modules/ in the out dir's parent. None of the new
tests uses the runtime harness.
# review-annotations gap file

All 22 `notest` SwRS now have an @tests_req marker in a new test file (all pass; run with NODE_PATH=<worktree>/node_modules because the scratch outDir cannot resolve `yaml` otherwise). No `noimpl`.

## Not fully closed
- REVIEW-198 (marks posted at once when HEAD, trust, setting or page changes): tested for the HEAD watch, onTrustGranted and onSettingsChanged. The page-load trigger (`previewReady` handler in rendering.ts calling `incoming.schedule(preview, 0)`) is not asserted: it is not observable without a Git extension, and the host harness (test/host/hostHarness.ts) cannot run under another outDir (needs the repo `out/` bundles). Kind of test needed: host-harness test with a fake Git extension, or integration (real window).
- REVIEW-155 (showComments posted on page load): tested for the settings-change trigger and for postShowComments directly. The page-load trigger is not asserted for the same harness reason (a host-harness test `host.ready()` then expect one `previewShowComments` was written, failed to start under the scratch outDir and was removed).

## Known issues asserted
- REVIEW-180: the test asserts the refusal "Editing a thread needs a trusted workspace." for a read-only preview (the Known issue: the text blames trust even when the preview is read-only for another reason is not distinguishable in the stub).
# toolbar-navigation gap file

All 32 `notest` SwRS are closed by new tests; none is left open. `noimpl` was empty.

New files (all pass when run from the worktree with NODE_PATH=<worktree>/node_modules and a scratch outDir):
- test/session/toolbarReq.requirements.test.ts (25 tests, real PreviewManager over a fake host)
- test/page/modules/toolbarReq.requirements.test.ts (5 tests)
- test/core/preview/toolbarReq.requirements.test.ts (2 tests)

Notes on how a few are covered (weaker than a real window, but green on today's code):
- TOOLBAR-130 "no selection listener": asserted by reading src/host-vscode/activation.ts and vscodeHost.ts for the absence of onDidChangeTextEditorSelection (needs process.cwd() = worktree).
- TOOLBAR-087 "no stylesheet rule": asserted by scanning src/ for a `[data-sphinx-preview-link-state` selector (needs process.cwd() = worktree).
- TOOLBAR-149: asserted on the CSS text (PREVIEW_ACCESSIBILITY_CSS); the real forced-colors rendering would need a visual run.

## Known issues asserted
None.
# trust-security gap file

## SwRS without a new test
None: all 20 `notest` ids (TRUST-010, 016, 017, 018, 021, 022, 028, 032, 039, 042, 048, 051, 065, 067, 068, 069, 071, 079, 087, 088)
now have a `@tests_req` marker in test/security/trustReq.requirements.test.ts, test/session/trustReq.requirements.test.ts or
test/host/trustReq.requirements.test.ts.

Remarks:
- TRUST-010: the real VS Code panel options (`localResourceRoots: []` of a new panel in src/host-vscode/activation.ts) are not
  covered by the unit test (it covers showPending(clearContent) and setMissingSource through RenderingController with a fake session);
  the fake vscode of test/host ignores the options of createWebviewPanel. A real-window check would read
  `localResourceRoots` of a new panel (testHooks.ts).
- TRUST-079: the record of the page (`preview.webview.diagnostics`) is not reachable in the host harness; the test checks the
  diagnostics returned by buildPreviewWebviewHtml, which updatePreview stores in the record.
- TRUST-087: the unreadable-file case is skipped (t.diagnostic) when the process reads files without permission (superuser).
- Run note: tests were run from a scratch outDir with `node_modules` and `package.json` symlinked next to `out/`
  (needed for ESM package resolution and for the manifest test, which reads `<out>/../package.json`).

## noimpl SwRS not marked in code (declarative or absence of code)
- TRUST-070 No visible text mentions Sphinx: absence of a string, no producing code (tested by test/security/userFacingText.test.ts).
- TRUST-071 No capabilities entry in the manifest: absence of a key in package.json.
- TRUST-074 Icon `images/logo.png`: `icon` key of package.json.
- TRUST-075 Node 24 pin: `.nvmrc` file.
- TRUST-076 Lock file resolves from registry.npmjs.org: package-lock.json.
- TRUST-077 `@plantuml/core` exact version: dependency entry of package.json.
- TRUST-078 `out/bundle` not excluded from the VSIX: `.vscodeignore` content (absence of an exclusion).
- TRUST-080 `images/logo.png` is 256x256: binary file.

## Known issues asserted
- TRUST-048 (deny-list sanitizer: `<base>` and an unknown attribute stay).
- TRUST-071 (manifest has no `capabilities`; the Restricted Mode Known issue itself, packaged VSIX disabled, is not asserted: needs a packaged-build/real-window check).
