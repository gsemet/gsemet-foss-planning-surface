---
title: Export a single page as one self-contained HTML file
cr: 288
date: 2026-11-11
issue: none
priority: P2
source: owner request (01-intent.md), grill 2026-11-11 (02-answers.md)
---

# Change spec: export a single page as one self-contained HTML file

> [!IMPORTANT]
> Owner's answers (2026-11-11), binding over the text below: Q1 the Export button goes in the
> **main row** (Refresh, Edit, Export, collapse; four buttons in that row only, TOOLBAR-001 amended
> accordingly; no sixth row). Q2 zoom not kept (100 %). Q3 export allowed in Restricted Mode.

## Problem

A writer cannot share what the Studio shows. Today the only way out of the preview is the
Markdown source, and a reader without the extension sees neither the theme, nor the diagrams,
nor the properties table.

Owner's decisions (2026-11-11, `02-answers.md`, binding):

- One self-contained `.html` file. It uses the current preview theme and width, with its CSS
  inline. Local images become data URIs. Mermaid, PlantUML and Vega diagrams are frozen as SVG.
  The file has no JavaScript at all, so tabs and dropdowns work in plain HTML and CSS.
- URL links are kept. Relative links to other files are removed, and a warning lists them before
  the export.
- The front matter properties table is collapsed by default. When it is expanded, the field
  descriptions from the OKF schema are shown, when the schema gives them.
- Review comments (TODO and THREAD chips) and all editing chrome are left out.
- Entry points: an "Export to HTML" command and a toolbar button. A save dialog opens next to the
  `.md` file.
- No GitHub issue. Blast radius 2: the Inspector uses Opus.

## Target behaviour

### Entry points

- A new command, `markdown-okf-schema-studio.exportHtml`, titled **Export to HTML**. It is in
  the Command Palette when a preview is focused or the active editor is a `.md` file. It acts on
  the focused preview. Otherwise it acts on the open preview of the active `.md` document. When
  neither exists, an information message says "Open the preview of this file to export it." and
  nothing else happens.
- A toolbar button, **Export to HTML** (aria-label, title and `data-tooltip` all the same), with
  `data-sphinx-preview-export`. Toolbar rows hold at most three buttons and all five rows are
  full, so the button goes in a **sixth row, `export`**, inside the collapsible group after the
  `content` row. It is the last stop in the Tab order. See open question Q1.
- Both entry points take the same path. The page takes a snapshot and sends it to the host in one
  host request. The host builds the file, warns about removed links, opens the save dialog and
  writes the file.
- Order of the dialogs:
  1. If the page has relative links, a **modal warning** comes first. It says how many links will
     be removed and lists their targets (unique, in document order, at most 20, then "and N more").
     Its buttons are **Export** and Cancel. Cancel stops: no save dialog, no file.
  2. The **save dialog**. It defaults to `<folder of the .md>/<stem>.html` (`notes.md` gives
     `notes.html`), has the filter `HTML: ["html"]` and the button label "Export". When the
     document has no local folder (an untitled or virtual document), it opens in the first
     workspace folder. The OS confirms an overwrite. Cancel writes nothing.
  3. After the write, an information message: "Exported to `<file name>`." If some images could
     not be embedded, the message names how many (see Images).
- A failed write (permissions, disk) shows an error message with the reason. The preview is left
  as it was.
- The page itself does not change. No mode, scroll, fold, tab or theme state is altered by an
  export.

### What the file contains

- **One file, no JavaScript.** The file has no `<script>` element, no `on*` event attribute, no
  `javascript:` URL, no `<link rel="stylesheet">`, no `@import` and no `vscode-webview:` or
  `vscode-resource` URL. Every style is inline in `<head>` `<style>` elements. Nothing is fetched
  when it opens: the only URLs left are the targets of external links.
- **Theme.** The colours are the ones the preview shows now (host theme, or the forced Dark,
  White or Cream mode). The page reads the resolved value of every `--studio-*` token
  (`THEME_TOKEN_NAMES` in `src/core/preview/themeTokens.ts`). The file writes those values in a
  `:root` rule placed after the preview stylesheet, so they no longer depend on the `--vscode-*`
  variables. The root attributes the CSS reads for the theme are kept on `<html>`:
  `data-sphinx-preview-theme-mode` and `data-okf-code-dark-background`. `color-scheme` is set to
  the theme kind (light or dark).
- **Width.** The width mode (Margin, Auto or Full, `data-sphinx-preview-width`) and the max
  content width setting (`previewContentWidthCss`) are those of the preview. In Auto mode, the
  breakout state the page measured (the attributes and properties on the content elements) is
  frozen as it was at the pane width of the export.
- **Zoom** is not kept: the file is at 100 %. The `--sphinx-preview-zoom` property and the
  first-clearance properties (room for the floating toolbar, `firstClearance.ts`) are dropped. See
  open question Q2.
- **Stylesheet.** The file holds `previewStylesheet()` (the same text as `out/bundle/preview.css`,
  `src/core/preview/pageBuildEntry.ts`), the width rule, the token rule, the per-page math class
  rules (`style[data-studio-math-styles]`) and a small export sheet (tabs, properties `details`).
  When the page has math, it also holds `katex.min.css` with its `woff2` fonts as data URIs; the
  `woff` and `ttf` sources are dropped. Without math, KaTeX is left out.
- **Title.** `<title>` is the front matter `title` when there is one, else the text of the first
  `h1`, else the file stem. `<meta charset="utf-8">` and a viewport meta tag are added.

### Content rules

- **Diagrams.** Mermaid, PlantUML and Vega diagrams are already `<img src="data:image/svg+xml,...">`
  in the page (`mermaidPreview.ts`, `plantumlDiagram.ts`, `vegaPreview.ts`). They are exported as
  they are. That is SVG, inline in the file, drawn in the theme of the export, and with no clash
  between the ids and styles of two diagrams. A diagram the page shows as drawn is drawn in the
  file. A diagram that is still rendering is awaited (bounded wait, 10 s). A diagram in error is
  exported as the preview shows it (its error box). SVG pictures (` ```svg ` fences and raw
  `<svg>`, CR 272) stay inline `<svg>` and keep their themed `var(--...)` colours through the
  token rule.
- **Images.** Every local image (`img src`, and every candidate of `srcset`) is replaced by a data
  URI with the original bytes and a MIME type taken from the extension (png, jpg/jpeg, gif, webp,
  svg, avif, bmp, ico). Only an image the page already shows can be embedded. The session keeps
  the `uri → path` map that `buildPreviewWebviewHtml` already computes in `resolveResource`, and
  the export reads only paths in that map, through the `FileSystem` port. An image the host
  cannot map or read loses its `src`, keeps its `alt`, and is counted in the closing message.
- **Links.** The page keeps each link's request in `data-sphinx-preview-navigation`
  (`html-sanitizer.ts`, around line 455). The export classifies it with `classifyPreviewReference`
  (`src/core/navigation/previewNavigation.ts`):
  - `external` (http, https, mailto): `href` is set to the URL;
  - `anchor` (`#id`): kept, so it jumps inside the file;
  - `relative`, `wiki` and `blocked`: the `<a>` is unwrapped (its text stays, the link goes) and
    the target is added to the warning list. A link to another heading of the same file written
    as a path (`./this.md#x`) counts as relative; that is a known limit.
  - The `data-sphinx-preview-navigation` attribute is removed in every case.
- **Properties table.** The `section[data-okf-properties]` becomes
  `<details data-okf-properties>`, closed by default. Its `<summary>` is the title "Frontmatter
  properties" with the issue badge text when there is one. The table follows the summary.
  When the schema was found (`okf-properties-docs`), the Description column is shown, whatever the
  Description toggle state in the preview (`html[data-okf-descriptions-collapsed]` is not
  copied). With no schema, the table keeps its two columns. The collapse and description toggle
  buttons are removed. The `data-okf-*` value attributes are removed (`data-okf-value`,
  `data-okf-value-yaml`, `data-okf-enums`, `data-okf-link-*`, `data-okf-available-*`); they only
  feed the editors.
- **Tabs.** Each `.myst-tab-set` becomes a CSS-only tab set. Each tab is a hidden radio input
  (`name` unique per set) followed by a `<label>` with the tab title. The panels are shown with
  `:checked` sibling selectors, with no `hidden` attribute. The tab the preview shows is checked.
  Nested tab sets work the same way. Tab sync groups (`data-myst-tab-sync`) do not follow each
  other in the file, because that needs JavaScript. Keyboard: the radios stay focusable and the
  arrow keys move between them natively.
- **Dropdowns** are already `<details>` (`mystNormalize.ts` line 360). They keep their current
  open state.
- **Left out (editing chrome and review).**
  - every `<button>` (code copy, heading fold toggles, properties toggles, comment actions, chart
    and diagram controls);
  - every `<input>`, `<textarea>` and `<select>` except the tab radios. Task-list checkboxes stay
    as `disabled` checkboxes, so a list still shows its ticks;
  - review comments: every element with a `data-okf-comment*` attribute (TODO and THREAD chips,
    badges, threads, popovers, compose boxes), the inline thread markers, and
    `html[data-okf-show-comments]`;
  - find marks (`data-sphinx-preview-find*`; a `<mark>` added by find is unwrapped), the Diff
    (baseline) and incoming-change marks, block selection and current-block outlines
    (`data-sphinx-preview-current`);
  - the toolbar, sticky headings, the TOC column, the status banners, the side-by-side pane, and
    every edit-mode attribute (`data-sphinx-preview-edit-mode`, `contenteditable`, insert points,
    handles);
  - the source-mapping attributes (`data-sphinx-source-file`, `-line`, `data-sphinx-preview-block`)
    and the `tabindex="0"` the sanitizer adds to mapped blocks.
- **Folded sections** are exported unfolded: the file has the whole document.

## Code anchors (origin/main, 33fb65ef)

- Toolbar: `src/core/preview/previewToolbar.ts` (52 lines). `renderPreviewToolbar()` builds five
  rows; its comment carries `@implements_req SwRS-MDOKFSTUDIO-TOOLBAR-001` and `-005`.
- Command registration: `src/host-vscode/activation.ts` (335 lines). See `FOLD_COMMAND_IDS` and
  `FIND_COMMAND_ID` (lines 42-48) and the registrations at lines 99-110. `package.json`
  `contributes.commands` and `menus.commandPalette` follow the `find` entry.
- Host to page command: `src/session/previewManager.ts` (624 lines), with `runFoldCommand` and
  `runFindCommand` (lines 225-262) posting `previewFoldCommand` and `previewFindCommand`. The
  message types and validators are in `src/core/protocol/hostToPage.ts` (472 lines, see
  `PREVIEW_FOLD_COMMANDS` line 279 and the validator near line 451). The page handlers are in
  `src/page/features/hostHandlers.ts` (109 lines).
- Page to host request: the `previewCopyText` pattern. The message is in
  `src/core/protocol/pageToHostMessages.ts` (line 227), the validator in
  `src/core/protocol/pageToHost.ts` (line 244, a transport bound and `userGesture`), the page side
  is `hostRequests.ask(...)` in `src/page/runtime.ts` (line 196), the host side is `router.on(...)`
  in `src/session/features/hostRequests.ts` (line 120, 367 lines), and the result type is in
  `hostToPage.ts` (line 415).
- Host UI port: `src/host-api/hostUi.ts` (45 lines) has `pickFile` but no save dialog and no
  modal confirm. The VS Code adapter is `src/host-vscode/vscodeHost.ts` (line 152,
  `showOpenDialog`).
- Webview assembly: `src/session/webview.ts` (297 lines). `resolveResource` (line 184) is where
  the `uri → path` map is made. The stylesheet `@import` and the width rule are at lines 240-249,
  KaTeX at line 253, and the diagram renderers are injected at lines 256-276.
- Styles: `src/core/preview/previewStyles.ts` and `pageBuildEntry.ts` (`previewStylesheet()`),
  `themeTokens.ts` (`THEME_TOKEN_NAMES`, `STUDIO_TOKEN_PREFIX`),
  `styles/propertiesStyles.ts` (555 lines; the collapse rules at lines 239-275).
- Properties table markup: `src/core/frontmatter/propertiesTable.ts` (405 lines). `withDocs`
  (line 213), the toggles (lines 228-230) and the `<section data-okf-properties>` (line 299).
- Diagrams: `src/page/modules/mermaidPreview.ts` (line 135, a data image),
  `plantumlDiagram.ts` (`showImage`, line 429), `vegaPreview.ts` (line 63, a data image).
- Tabs: `src/page/modules/tabs.ts` (the markup is described at the top of the file).
- Root properties the page sets: `src/page/modules/viewControls.ts` (zoom, line 38) and
  `firstClearance.ts` (lines 240-268).
- Link classification: `src/core/navigation/previewNavigation.ts` (`classifyPreviewReference`,
  line 116, `@implements_req TOOLBAR-090`).
- Test hooks for the real window: `src/host-vscode/testHooks.ts`, through
  `test/integration/extensionApi.ts`.

## Recommended approach

Four layers, each testable on its own. The developer may choose differently if the criteria
below still hold and no dependency-cruiser exception is added (constitution, section 2).

1. **Core, pure (`src/core/export/`, new):** `htmlExport.ts` (and `exportTabs.ts` if it gets
   long). It holds `buildHtmlExport(snapshot, inputs): { html, removedLinks, missingImages }`.
   - `snapshot` is what the page sent: the content `outerHTML`, the root attributes, the token
     values, the math styles, the shown tab of each set, and the document title.
   - `inputs` are the stylesheet text, the width CSS, the KaTeX CSS with its fonts, and an image
     lookup `src → data URI | undefined`.
   - It parses with `parse5`, as `propertiesTable.ts` does, and applies every content rule above.
   - It needs no Node built-ins, so it stays out of the dependency-cruiser `NODE_DEBT` list.
2. **Page (`src/page/modules/exportSnapshot.ts`, new):**
   - It takes the snapshot: it clones `main#sphinx-myst-preview-content`, reads the
     `getComputedStyle(documentElement)` value of every `--studio-*` token and the root
     attributes, waits for pending diagram renders, and records the shown tab of each set.
   - It sends the snapshot with `hostRequests.ask("previewExportHtml", { snapshot, userGesture }, ...)`.
   - The toolbar button and the new `previewExportCommand` host message both call it.
   - Wire it from `runtime.ts` or a small feature file. `pageRuntime.ts` is 694 lines (limit 800),
     so keep its share to a few lines.
3. **Session (`src/session/features/htmlExport.ts`, new):**
   - It handles `previewExportHtml`. It reads the images through the `FileSystem` port, using the
     map kept from the last `buildPreviewWebviewHtml`; the map is added to `PreviewWebviewResult`
     and kept on the stage.
   - It calls `buildHtmlExport`, shows the warning, asks for the save path and writes the file.
   - It refuses a snapshot with no user gesture unless it follows a `previewExportCommand` that this
     session sent. A page can never open the dialog by itself.
   - The transport bound is new: `MAX_EXPORT_SNAPSHOT_TRANSPORT_LENGTH`, 50 MB, enforced like
     `MAX_COPY_TEXT_TRANSPORT_LENGTH`.
   - KaTeX CSS and fonts are read from the bundle. `AssetResolver.bundleUri` serves webview URIs
     only, so the session needs a read path for bundle files, through `FileSystem` and the
     extension root that `node-services/paths.ts` or the host already knows. Do not import
     `vscode` outside `host-vscode`.
4. **Host API and VS Code:**
   - `HostUi` gains `pickSaveFile({ defaultPath, filters, saveLabel }): PromiseLike<string | undefined>`
     and `confirm({ message, detail, confirmLabel }): PromiseLike<boolean>` (modal).
   - `vscodeHost.ts` implements them with `showSaveDialog` and
     `showWarningMessage(..., { modal: true, detail }, label)`.
   - `activation.ts` registers the command, which calls `manager.runExportCommand(activeDocument)`.
   - `testHooks.ts` adds a hook to answer the confirm and the save dialog in integration tests.
   - `package.json` gets the command and its palette `when`.
   - Every other `HostUi` implementation in the tests (the inline stubs in `test/session/`) gains
     the two methods.

## Requirements

No `approved` requirement changes, so no owner approval is needed. The changed SwRS are
`proposed`, and the StRS this work would sit under, `StRS-MDOKFSTUDIO-CORE-001`, is approved, so
the new SwRS do **not** derive from it. Create every new requirement with
`uv run --no-sync --group requirements okfreq new ... --lifecycle proposed`. The IDs below are
the next free ones on origin/main at the time of writing. `okfreq new` allocates the real ones;
see the stack note.

- **New StRS (toolbar-navigation), expected `StRS-MDOKFSTUDIO-TOOLBAR-014`:** "A writer shares
  one page as a self-contained HTML file." User need: send a rendered page, with its theme,
  diagrams and properties, to a reader who has no editor.
- **New SwRS, all deriving from it:**
  - `SwRS-MDOKFSTUDIO-TOOLBAR-134`: the entry points. The command and its availability, the
    sixth toolbar row and its button, the acting preview, the save dialog default and filter,
    Cancel writes nothing, the closing message, the write error. Implemented in
    `previewToolbar.ts`, `activation.ts`, `previewManager.ts`, `session/features/htmlExport.ts`
    and `page/modules/exportSnapshot.ts`.
  - `SwRS-MDOKFSTUDIO-TOOLBAR-135`: the links. External and anchor links are kept; relative,
    wiki and blocked links are unwrapped. The modal warning lists them before the save dialog,
    and Cancel stops the export.
  - `SwRS-MDOKFSTUDIO-TOOLBAR-136`: the file is self-contained and has no script. It keeps the
    preview theme (resolved tokens, forced modes) and the width mode and max width, at 100 % zoom.
    It embeds local images as data URIs and counts the missing ones. It embeds KaTeX only with
    math.
  - `SwRS-MDOKFSTUDIO-TOOLBAR-137`: the content. Review comments and editing chrome are left out,
    sections are unfolded, tabs work in CSS only with the shown tab checked, and dropdowns keep
    their state.
  - `SwRS-MDOKFSTUDIO-FMSCHEMA-091`: in the export, the properties table is a closed `<details>`;
    when it is expanded, the Description column is shown if the schema was found.
  - `SwRS-MDOKFSTUDIO-DIAG-128`: in the export, Mermaid, PlantUML and Vega diagrams are SVG
    images drawn in the theme of the export, a pending render is awaited, and a diagram in error
    is shown as its error box.
- **Changed SwRS:**
  - `SwRS-MDOKFSTUDIO-TOOLBAR-001` (proposed, stable; amend). The toolbar becomes **six rows**:
    the five existing rows and an `export` row with one button, **16 buttons**. Update the
    description, the normative text, the "Writable preview", "Visual order" and tooltip scenarios
    (15 becomes 16, the row list gains `export`), and the boundary table: the rows stay inside a
    360 px pane with the sixth row. The width claim does not change: the toolbar is as wide as its
    first row.
  - `SwRS-MDOKFSTUDIO-TOOLBAR-133` (proposed, stable): check it only. The overlay is placed 40 px
    under the column top to clear the TOC button tooltip (row 4). A sixth row does not move
    row 4, so no change is expected. If `capture_toc_rail.py` fails, report it; do not change the
    number.
  - `SwRS-MDOKFSTUDIO-TOOLBAR-090` (the link classification) is reused, not changed.
- Markers: `@implements_req` next to each new function and the toolbar row, and `@tests_req` at
  each test listed below. Then run `just requirements-update` and add a dated entry in
  `requirements/tiers/log.md`.
- **Writing skill:** no change. No rendered syntax is added or changed: the export renders what
  the preview renders (constitution, section 6). The skill could say "export the page to share
  it", but that is not a syntax and the skill stays minimal.

## Tests first (each fails on origin/main)

1. **Unit, core builder:** `test/core/export/htmlExport.test.ts` (new), tagged with the SwRS of
   each case.
   - **TOOLBAR-135, the links:** a snapshot with an `https:` link, a `mailto:` link, an `#anchor`,
     `other.md`, `./sub/x.md#h`, `wiki:Page` and a blocked `file:` link. The external and anchor
     links keep their `href`. The others are plain text with no `<a>`. `removedLinks` lists the
     four, unique, in order. No `data-sphinx-preview-navigation` is left.
   - **TOOLBAR-136, self-contained:** the output has no `<script`, no ` on[a-z]+=`, no
     `javascript:`, no `<link`, no `@import`, no `vscode-`. The `:root` token rule follows the
     preview sheet and holds every name of `THEME_TOKEN_NAMES`. The theme mode and width
     attributes are on `<html>`; the zoom and clearance properties are not. An image `src` in the
     lookup becomes its data URI. An image not in the lookup loses its `src`, keeps its `alt`, and
     is counted. A `srcset` is rewritten the same way.
   - **TOOLBAR-137, the content:** a snapshot with a code copy button, a heading fold toggle, a
     TODO chip, a THREAD chip and its popover, a find `<mark>`, a block with source-mapping
     attributes and `tabindex="0"`, and a task-list checkbox. None of the chrome is left, the
     checkbox stays `disabled`, and the text of the marked words stays. A two-set tab snapshot,
     one set nested, with the second tab shown: radios and labels, the second tab `checked`, no
     `hidden` panel, the radio names unique per set. A dropdown `<details open>` stays open.
   - **FMSCHEMA-091, the properties:** a properties section with a schema becomes
     `<details data-okf-properties>` with no `open`, its summary is "Frontmatter properties", the
     Description header and cells are there, there is no toggle button, and no `data-okf-value*`
     attribute is left. With no schema, the table has two columns. With
     `data-okf-descriptions-collapsed="true"` in the snapshot, the column is still shown.
   - **The title:** front matter title, then the first `h1`, then the stem.
2. **Unit, page snapshot:** `test/page/modules/exportSnapshot.test.ts` (new), on the runtime
   harness (`test/page/runtimeHarness.ts`).
   - **TOOLBAR-134:** a click on the Export button asks `previewExportHtml` with
     `userGesture: true`, and a `previewExportCommand` message asks it too.
   - **TOOLBAR-136:** the snapshot holds a value for each token and the root attributes, and
     leaves out zoom.
   - **DIAG-128:** a Mermaid figure whose render is pending is awaited, then exported as
     `data:image/svg+xml`. A diagram in error is exported as its message.
   - **TOOLBAR-137:** the shown tab index is recorded, and an export changes no page state: the
     edit mode, folds, tabs and scroll are the same before and after.
3. **Unit, session:** `test/session/htmlExport.test.ts` (new), with a stub `HostUi` and an
   in-memory `FileSystem`.
   - **TOOLBAR-135:** with relative links, `confirm` is called before `pickSaveFile`, and its
     detail lists the targets, capped at 20 plus "and N more". When `confirm` answers false,
     `pickSaveFile` is not called and nothing is written. Without relative links, `confirm` is not
     called.
   - **TOOLBAR-134:** the save default is `<dir>/notes.html` with the HTML filter; a cancelled
     dialog writes nothing; the written bytes equal the builder output; a write error shows
     `showError`; the information message names the file (and the missing images).
   - **TOOLBAR-134:** a snapshot without a gesture and without a pending command is refused.
     `runExportCommand` uses the focused preview, else the preview of the active document, else
     shows the information message.
4. **Unit, protocol:** in the existing protocol tests (`test/core/protocol/`), the new
   `previewExportCommand` and `previewExportHtml` validators. A snapshot over the transport bound,
   or with a field of the wrong type, is refused. Tag them `@tests_req TOOLBAR-134`.
5. **Unit, toolbar CSS and markup:** `test/core/preview/previewStyles.test.ts` (lines 488-534)
   asserts 15 buttons and five rows. It now asserts 16 buttons, a sixth `export` row after
   `content`, and 16 tooltips. The assertion changes because the owner's decision adds a button
   (CR 288); say so in the commit body (constitution, section 3). Keep the change to a few lines.
6. **Visual, headless, group `toolbar-navigation`:**
   - A new fixture, `test/visual/fixtures/84-export-html.md`. It has front matter with the
     `08-okf-schema` schema, a `{tab-set}` with two tabs, a `{dropdown}`, an external link, a
     relative `.md` link, a local image, a math line, a Mermaid fence and a TODO comment.
   - `renderFixtures.ts` gets an export step for scenarios that ask for it. It renders the
     fixture as today, builds a snapshot from the rendered page and the theme variables of
     `test/visual/themes.ts`, calls `buildHtmlExport`, and writes `<scenario>.export.html` next
     to the page.
   - New scenarios `toolbar-navigation/v41-export-html-cream-900` and
     `toolbar-navigation/v42-export-html-dark-900`. Map them in `scenarioIds.ts` with a
     description. The new module `test/visual/capture_export_html.py` opens the export file in
     Playwright **with JavaScript disabled** and checks:
     - there is no `script` element;
     - the body background equals the theme's editor background;
     - the content column is as wide as in the preview scenario of the same theme;
     - the properties `details` is closed; a click on its summary opens it and shows a
       Description column;
     - a click on the second tab label shows the second panel and hides the first;
     - the external link has its `href`, and the relative link is plain text;
     - no `[data-okf-comment-kind]` and no `button` are left;
     - the image `src` starts with `data:`.
     Tag it `@tests_req` TOOLBAR-135, -136, -137, FMSCHEMA-091. Save a full-page shot.
   - Existing toolbar checks: `capture_layout_checks.py` line 315 (the row list) gains `export`.
     The toolbar screenshot `toolbar-navigation/v18-toolbar-expanded-cream-900` changes (new
     row); update its crop height in `scenarioIds.ts` if the row falls outside it.
7. **Real VS Code (heavy CI):** `test/integration/exportHtml.test.ts` (new), in the trusted suite,
   with an `INTEGRATION_TESTS` row in `test/shared/e2eGroups.ts` (group `toolbar-navigation`).
   - It opens a fixture with a Mermaid diagram, a PNG image and a relative link
     (`test/integration/fixtures/`), and sets the test hook to accept the warning and to save in a
     temporary folder.
   - It runs `markdown-okf-schema-studio.exportHtml`, then checks the file:
     - it exists and has no `<script`;
     - it has a `data:image/svg+xml` image for the diagram and a `data:image/png;base64,` image;
     - the relative link text is there, without its `<a href`;
     - the warning hook received the relative target.
   - A second case cancels the warning, and no file is written.
   - Tag it TOOLBAR-134, TOOLBAR-135, DIAG-128. It needs no real-input scenario, so
     `test/integration/realInput/run.ts` is not touched unless the developer adds one.

## Files expected to change

- New: `src/core/export/htmlExport.ts` (and `exportTabs.ts` if needed),
  `src/page/modules/exportSnapshot.ts`, `src/session/features/htmlExport.ts`.
- `src/core/preview/previewToolbar.ts` (export button, sixth row, comment and markers)
- `src/core/preview/styles/pageChromeStyles.ts` or the toolbar's style module (the sixth row and
  its icon, if a rule is needed)
- `src/core/protocol/hostToPage.ts`, `pageToHost.ts`, `pageToHostMessages.ts` (two messages and
  a result)
- `src/page/features/hostHandlers.ts`, `src/page/runtime.ts` (wiring; a few lines)
- `src/session/previewManager.ts` (`runExportCommand`), `src/session/webview.ts` (the
  `uri → path` map in the result), `src/session/features/rendering.ts` (keep the map on the
  stage), `src/session/features/hostRequests.ts` or the session factory (register the handler)
- `src/host-api/hostUi.ts` (two methods), `src/host-vscode/vscodeHost.ts`,
  `src/host-vscode/activation.ts`, `src/host-vscode/testHooks.ts`
- `package.json` (command and palette entry)
- Tests: the new files listed above, `test/core/preview/previewStyles.test.ts`,
  `test/visual/renderFixtures.ts`, `test/visual/scenarioIds.ts`, the new scenario module (for
  example `test/visual/exportHtmlScenarios.ts`, registered in `scenarios.ts`),
  `test/visual/capture_layout_checks.py`, `test/visual/capture.py` (to import the new check),
  `test/visual/fixtures/84-export-html.md`, `test/integration/exportHtml.test.ts` and its
  fixture, `test/integration/extensionApi.ts`, `test/shared/e2eGroups.ts`, and the session test
  stubs of `HostUi`
- `requirements/tiers/strs/toolbar-navigation/` (new StRS),
  `requirements/tiers/swrs/toolbar-navigation/` (TOOLBAR-001 amended, TOOLBAR-134 to 137 new),
  `swrs/frontmatter-schema/` (FMSCHEMA-091), `swrs/diagrams/` (DIAG-128),
  `requirements/tiers/log.md`, and the files `just requirements-update` regenerates
- `CHANGELOG.md`, under "Unreleased":
  "- Export to HTML (a command and a toolbar button) saves the page as one self-contained `.html`
  file in the preview's theme and width: images and Mermaid, PlantUML and Vega diagrams are
  embedded, tabs and dropdowns work without JavaScript, the properties table opens on a click,
  links to other files are removed after a warning, and comments and editing controls are left
  out."
- `docs/releases-notes/`: only if the release process asks for an entry per change (it is written
  at release time).

## Blast radius

**2, so the Inspector uses Opus.** This is a new rendered output and a new write path to disk.

- The live preview changes only by one toolbar button. This changes the toolbar height, its
  rows, its Tab order and the toolbar screenshots, and it touches every toolbar layout check
  (TOOLBAR-001, the first-clearance measures that use the toolbar height, and the TOC rail
  tooltip clearance).
- The protocol gets two new messages. A bad validator could let a page open a save dialog or send
  a huge payload; the gesture and command check and the transport bound cover that.
- `PreviewWebviewResult` gains a field. `baselineDiff.ts` also calls `buildPreviewWebviewHtml`:
  check that it ignores the field.
- The file write goes only to the path the user picked in the save dialog. The image reads go
  only to paths the resource policy already allowed for the page.

## Gates

- `just check` (formatting, types, boundaries, file-size ratchet, unused exports, markers, unit,
  contract and security tests, requirements lint).
- Focused unit runs:
  `npm run compile && node scripts/node-test.mjs unit "out/test/core/export/*.test.js" "out/test/page/modules/exportSnapshot.test.js" "out/test/session/htmlExport.test.js"`.
- Headless visual:
  `npm run visual:render && uv run --no-sync --group docs python test/visual/capture.py --group toolbar-navigation --group theme-zoom --group layout-width`.
  This covers v41/v42, v18/v19 and the row and first-clearance checks.
- Requirements: `uv run --no-sync --group requirements okfreq validate --check-links --project-root .`
  and `just requirements-update` leave no diff.
- Heavy CI on the branch: `gh workflow run ci.yml --ref <branch> -f heavy=true`. The real VS Code
  integration includes `exportHtml.test.ts`.
- `just preflight` before the PR is marked ready.

## Acceptance checks (the Verifier, at the pushed head)

1. `git grep -n '"markdown-okf-schema-studio.exportHtml"' -- package.json src/host-vscode/activation.ts`
   shows the command in `contributes.commands` (title "Export to HTML"), in
   `menus.commandPalette`, and in the registration.
2. `git grep -n 'data-sphinx-preview-toolbar-row="export"\|data-sphinx-preview-export' -- src/core/preview/previewToolbar.ts`
   shows the sixth row and the button.
3. The focused unit run above passes, and each new test file carries the `@tests_req` tags named
   in "Tests first".
4. After the visual run, the export files of v41 and v42 (next to the rendered pages, in the
   manifest's `pageDirectory`) give no match for
   `grep -c -E '<script|<link|@import|vscode-|javascript:| on[a-z]+=' <file>`. The v41 and v42
   checks pass, and the v18 toolbar shot shows six rows.
5. `okfreq validate --check-links` passes. The new SwRS IDs are linked from the code
   (`@implements_req`) and the tests (`@tests_req`). TOOLBAR-001 says 16 buttons and six rows.
6. The heavy CI run is green, `exportHtml.test.ts` among the integration tests.
7. `just preflight` passes.

## Screenshots expected in the PR

- The toolbar expanded, cream, 900 px (v18): the sixth row with the Export button and its
  tooltip.
- The modal warning that lists the removed links. This is a real VS Code capture from the
  integration test's evidence, or a manual capture.
- The exported file opened in a browser, cream (v41) and dark (v42): properties collapsed. Then
  the same file with the properties expanded (Description column) and the second tab selected.
- The fixture page in the preview next to the exported file, same theme and width, to show they
  match.

## Stack note (CRs 290, 289, 293, 292, 291, 288)

This CR is the top of the stack and is rebased last. Files it shares with the CRs below:

- `requirements/tiers/log.md` and the files `just requirements-update` regenerates (indexes,
  coverage, StRS link lists). These always conflict: regenerate them after the rebase, never
  merge them by hand.
- `CHANGELOG.md` "Unreleased": add this line after the lines of the CRs below.
- `test/integration/realInput/run.ts`: only if the developer adds a real-input scenario (not
  planned). The lower CRs are likely to touch it.
- Requirement IDs: the table CRs mostly add TABLE SwRS. 289 (find) and 293 (keyboard row add) may
  take TOOLBAR or TABLE IDs. If one of them takes TOOLBAR-134 or a later ID first, this CR takes
  the next free ones with `okfreq new` when it rebases. The IDs in this spec are expected values,
  not reservations.
- The visual fixture number (84) and the scenario numbers `toolbar-navigation/v41-v42`: if a lower
  CR takes one first, this CR takes the next free one.
- Likely code overlaps:
  - `src/core/protocol/*` and `src/page/runtime.ts`: 292 (TSV paste) may add a page message;
  - `src/core/preview/previewToolbar.ts` and `previewStyles.test.ts`: 293 if its hint goes in the
    toolbar;
  - `test/visual/scenarioIds.ts`: every CR that adds a scenario.

## Risks

- **The toolbar gets taller.** At 360 px and in the collapsed state, check that the sixth row
  stays inside the pane and that the first-clearance measures still clear the first block
  (TOOLBAR-001 boundary table, layout-width group).
- **Auto width is frozen.** The breakout the page measured fits the pane width at export time, so
  a reader with a much narrower window may see a wide table scroll. This is accepted: the
  export uses the width of the preview.
- **File size.** A page with many diagrams and large images can reach tens of MB; the transport
  bound is 50 MB. A bigger page shows the error "This page is too large to export". KaTeX fonts
  add about 300 KB, only when the page has math.
- **Tab sync groups** do not follow each other in the file, because that would need JavaScript.
- **Restricted Mode and standalone previews.** The export is allowed: it writes only to the
  path the user picked, and it reads only images the page already shows. If the owner wants it
  off in Restricted Mode, that is one `when` clause and one check (see Q3).
- **Selector drift.** The chrome is removed by attribute and element lists. A future chip or
  control that uses a new attribute would leak into the file. Removing every `<button>`, together
  with the `<script>`, `on*`, `contenteditable` and `data-okf-comment` assertions of test 1, is
  the safety net.

## Open questions (owner)

- **Q1. Where does the toolbar button go?** All five rows are full (three buttons each).
  Recommended: a sixth row, `export`, with one button, in the collapsible group (hidden when the
  toolbar is collapsed). The alternative is a fourth button in the main row, which breaks the
  "at most three per row" rule of TOOLBAR-001 and widens the toolbar.
- **Q2. Is the zoom kept?** The intent said "theme and size", the grill said "theme and width".
  Recommended: no, the file is at 100 % and the reader's browser zooms. The width mode and the max
  content width are kept.
- **Q3. Is export allowed in Restricted Mode (untrusted workspace)?** Recommended: yes. It
  writes only where the user chooses and embeds only what the preview already shows.
