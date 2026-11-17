# P10 scope briefs

One section per okfreq scope (= e2e group of `test/shared/e2eGroups.ts`, D32). Each gives what
the scope covers, its mapped files (`tools/scope-map.json`, the single source of truth), its
checklist load (rows of `checklists/*.md` with this scope, `?` rows included), and the brief to
hand to the per-scope Opus analyst for P10.1.

## Common brief (prepend to every per-scope brief)

> You are the P10.1 inventory analyst for scope `<scope>` (token `<TOKEN>`) of the Markdown
> OKF-Schema Studio VS Code extension, repo `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio`.
> Read-only: do not edit anything outside
> `.agents/changes/archives/021-feature-session-007-020/p10-requirements/inventory/`; no builds, tests or VS
> Code (other agents run gates). Write `inventory/<scope>.md`: one line per observable behaviour,
> id `F-<TOKEN>-NNN` (never reuse; append new lines at the end), columns: behaviour (user-visible
> words from `.agents/glossary/common.md`), evidence (source `file:symbol`, tests `file:test name`,
> README/CHANGELOG/docs line, archive report row), coverage state (`tested` unit/integration/visual,
> `untested`, `doc-only`), checklist ids it covers (`C-…`), candidate StRS (use case) and notes
> (edge/error/refusal paths, settings interplay, Restricted Mode / read-only / standalone variants,
> CRLF, undo, stale versions). Include behaviours that no test covers and behaviours present in
> code but absent from README/CHANGELOG (flag them `undocumented`). Every checklist row of your
> scope must be cited by at least one F line, or moved to another scope with a reason (write the
> move in a "Checklist corrections" section; do not edit the checklist files). Apply followups P9
> B2c: page-wide checks are one global behaviour, assertion-equivalent scenario families are one
> behaviour, long lock lines are split into atomic behaviours.
>
> Read first: `p10-requirements/STATE.md` (rules), `setup-plan.md` §5 (levels, marker rules),
> `checklists/index.md`, then the scope-specific list below, then
> `archives/021-feature-session-007-020/p9-e2e/inventory.md` (rows of your group), `README.md`, `CHANGELOG.md`,
> `docs/known-limitations.md`, the archives cited by your checklist rows and
> `.agents/changes/archives/001-deep-UX-analysis/fix-plan/RESULTS.md` for 001 findings.
> Shared hosts: behaviours of every scope are implemented in `src/extension.ts` (message handlers,
> `registeredMessageHandlers`) and `src/webview/scrollSync.ts` (page runtime): search them for
> your messages, settings and DOM attributes. End with counts: behaviours, tested, untested,
> doc-only, undocumented, checklist rows covered / total.

Sonnet critic brief (per scope, after the inventory): "Read `inventory/<scope>.md` and the
checklist rows of `<scope>`; list every checklist row not cited, every behaviour of the mapped
files missing from the inventory (error paths, settings, refusals, keyboard), every claim whose
evidence does not exist; write `reviews/<scope>-inventory.md`, verdict APPROVE / REVISE."

## Load summary

| Scope | Token | src | tests | Checklist rows | Split |
| --- | --- | ---: | ---: | ---: | --- |
| rendering-core | CORE | 8 | 18 | 53 | page-controls 11, changelog 5, archives 16, visual 20, integration 1 |
| code-blocks | CODE | 2 | 2 | 21 | messages 1, page-controls 2, changelog 5, visual 13 |
| gfm | GFM | 2 | 6 | 16 | messages 2, changelog 6, archives 4, visual 4 |
| myst | MYST | 7 | 9 | 40 | messages 2, page-controls 2, changelog 3, archives 10, visual 21, integration 2 |
| diagrams | DIAG | 3 | 2 | 18 | contributes 1, palette 1, slash 1, changelog 3, archives 3, visual 9 |
| frontmatter-schema | FMSCHEMA | 7 | 9 | 54 | contributes 5, messages 1, page-controls 8, changelog 6, archives 11, visual 22, integration 1 |
| frontmatter-editing | FMEDIT | 0 | 3 | 16 | messages 2, page-controls 1, changelog 2, archives 4, visual 6, integration 1 |
| layout-width | LAYOUT | 2 | 3 | 92 | contributes 1, toolbar 1, changelog 4, archives 2, visual 84 |
| theme-zoom | THEME | 2 | 2 | 17 | messages 2, toolbar 3, page-controls 1, changelog 1, archives 3, visual 7 |
| toolbar-navigation | TOOLBAR | 8 | 6 | 56 | contributes 3, messages 8, toolbar 6, page-controls 2, changelog 1, archives 6, visual 29, integration 1 |
| block-editing | BLOCK | 7 | 11 | 48 | messages 11, toolbar 1, changelog 2, archives 18, visual 14, integration 2 |
| palette-slash | PALETTE | 14 | 14 | 150 | contributes 1, messages 11, palette 30, slash 53, page-controls 10, changelog 13, archives 11, visual 17, integration 4 |
| table-editing | TABLE | 1 | 2 | 23 | palette 3, slash 3, page-controls 1, changelog 5, archives 6, visual 5 |
| review-annotations | REVIEW | 13 | 16 | 50 | contributes 3, messages 8, palette 1, slash 1, toolbar 1, page-controls 7, changelog 10, archives 11, visual 4, integration 4 |
| lifecycle-sync | LIFE | 10 | 18 | 38 | contributes 16, messages 9, toolbar 1, page-controls 1, changelog 1, archives 3, integration 7 |
| trust-security | TRUST | 4 | 8 | 11 | contributes 1, changelog 6, archives 1, integration 3 |

CHANGELOG and archive rows were assigned by keyword (`?`): expect many moves, notably towards
block-editing, table-editing and lifecycle-sync (keywords such as "label", "Enter", "table" pull
rows into myst/gfm/table-editing). lifecycle-sync and trust-security have no visual scenarios:
their evidence is integration-only. The analyst for palette-slash carries the heaviest load
(150 rows): give it the highest effort or split it in two runs (palette buttons + popovers/panels,
then slash menu + host pickers/image paste).

## 1. rendering-core (CORE)

Covers CommonMark rendering through the MyST engine: headings, paragraphs, lists, block quotes,
inline code, long documents, CJK/RTL text, missing images, `{include}` (budget and source
mapping), the Sphinx source-mapping equivalence contract, and the preview stylesheet as far as
rendering goes (admonition colours and layouts belong to `myst`). Also owns the visual campaign
harness files (markers of all scopes live there) and the Python `sphinx/` extension.

- src: `src/render/renderPipeline.ts`, `src/render/mystRenderer.ts`, `src/preview/previewStyles.ts`,
  `src/build/sphinxBuild.ts`, `src/build/snapshotWorkspace.ts`, `src/build/sourceTransforms.ts`,
  `sphinx/conf.py`, `sphinx/preview_source_mapping.py`
- tests: `test/rendering/{renderPipeline,includeBudget,includeMapping}.test.ts`,
  `test/rendering/sphinxFeatures.contract.ts`, `test/build/{sphinxBuild,snapshotWorkspace,sourceTransforms}.test.ts`,
  `test/webview/{inlineCode,previewStyles}.test.ts`, `test/integration/projectFeatures.test.ts`,
  `test/visual/{scenarios,scenarioIds,renderFixtures,generatedFixtures,renderOptions,themes}.ts`,
  `test/visual/capture.py`, `sphinx/tests/test_sphinx_preview_mapping.py`
- Checklist rows: 53.
- Brief: read `renderPipeline.ts` (render result, diagnostics, include handling) and the
  CommonMark/include parts of `mystRenderer.ts`; decide for `src/build/sphinx*`/`snapshotWorkspace`
  whether they are product behaviour (no import from `extension.ts`) or contract tooling; list the
  diagnostics shown on the status page; list the stylesheet rules that are behaviour (font sizes,
  radius, missing-image placeholder) vs cosmetics. Fixtures: `test/visual/fixtures/01-05,20-23`.
  Docs: `docs/active-file-rendering.md`, `docs/feasibility-authentic-html.md`,
  `docs/feasibility-source-mapping.md`, README "What This Extension Adds", "Sphinx Projects".

## 2. code-blocks (CODE)

Fenced code, syntax highlighting (highlight.js languages, unknown grammar fallback), diff
fences, the hover copy button and its message.

- src: `src/render/highlight.ts`, `src/webview/codeCopy.ts`
- tests: `test/rendering/highlight.test.ts`, `test/webview/codeCopy.test.ts`
- Checklist rows: 21 (13 visual: v05–v12 are one assertion family per B2c).
- Brief: list supported/aliased languages and the fallback, the diff colouring rules, copy
  button states (hover, Copied, keyboard focus, read-only previews), the `previewCopyText` bound
  (1 000 000 chars) and refusal. Fixture `06-syntax-highlighting.md`, `04-code-and-tables.md`.

## 3. gfm (GFM)

GitHub Flavored Markdown: autolinks and bare URLs, task lists and checkbox toggles (prose,
lists, table cells; one undo), strikethrough, alerts (incl. CRLF), footnotes, raw HTML subset
(details/summary/kbd), colour spans.

- src: `src/render/checkboxMarkers.ts`, `src/webview/spanColors.ts` (GFM rendering itself is in
  `mystRenderer.ts`, sanitizer rules in `html-sanitizer.ts`: mark them)
- tests: `test/rendering/{bareUrlAutolink,checkboxMarkers,checkboxRendering,crlfAlerts}.test.ts`,
  `test/webview/spanColors.test.ts`, `test/integration/checkboxToggle.test.ts`
- Checklist rows: 16.
- Brief: inventory the checkbox toggle round trip (`previewCheckboxToggle` → `previewCheckboxResult`,
  stale refusal, read-only refusal, undo), which raw HTML is kept or stripped, the colour grammar
  (hex, rgb/rgba only), autolink exclusions (code spans, URLs in links). Archives 004, 009, 016
  (T06, T25, T26, T33). Fixture `21-bare-urls.md`.

## 4. myst (MYST)

MyST syntax: directives, roles, admonitions (all types, custom titles, nested content,
context tags), math (inline/display/aligned, offline KaTeX, `$19` not math), figures with
width/align/labels, `{ref}`/`{doc}`/`{cite}`, conf.py-driven extension warnings (preview and
Problems panel), label rename from the anchor icon.

- src: `src/myst/confLocator.ts`, `src/myst/confParser.ts`, `src/render/mystSyntaxDetect.ts`,
  `src/render/mathRenderer.ts`, `src/mapping/labelRename.ts`, `src/webview/labelRename.ts`,
  `src/webview/figureSizes.ts`
- tests: `test/rendering/{mystFeatures,mathRenderer,mystSyntaxDetect,confLocator,confParser}.test.ts`,
  `test/mapping/labelRename.test.ts`, `test/webview/labelRename.test.ts`,
  `test/integration/{labelRename,mystDiagnostics}.test.ts`
- Checklist rows: 40 (admonition galleries = one family).
- Brief: list each directive/role the renderer supports and its unsupported fallback
  (`03-unresolved-constructs.md`), the conf.py search order (D29) and caching, the diagnostic
  wording (U17), untrusted behaviour, label rename refusals (stale line, invalid name, one undo).
  Archives 015, 016 (T27–T30). Docs: README "Sphinx Projects".

## 5. diagrams (DIAG)

Mermaid (themes per host theme, fallback, render errors) and PlantUML (rendered, unconfigured,
executable not found, `plantuml.jarPath`).

- src: `src/render/plantUmlRenderer.ts`, `src/webview/mermaidPreview.ts`,
  `src/configuration/plantUmlConfiguration.ts`
- tests: `test/rendering/plantUmlRenderer.test.ts`, `test/configuration/plantUmlConfiguration.test.ts`
  (no unit test for `mermaidPreview.ts`: visual only — flag it)
- Checklist rows: 18.
- Brief: PlantUML process handling (spawn, timeout, Restricted Mode, missing Java/jar, Graphviz),
  Mermaid bundle loading under CSP, theme switching, error display; the Mermaid palette/slash
  action. Fixtures `06-mermaid-map.md`, `12-*`, `13-*`.

## 6. frontmatter-schema (FMSCHEMA)

YAML frontmatter rendering as the properties table, OKF schema discovery (`_schema/`), `$ref`
resolution, validation and error display, strict additional properties, generic (non-OKF)
YAML, x-okf-link fields (resolution modes, tooltips/preview fields, marker-line navigation,
outside-workspace links), the five `frontmatter.*` settings.

- src: `src/frontmatter/{okfFrontmatter,propertiesTable,schemaRegistry,schemaValidator,fileLinks,stemIndex}.ts`,
  `src/configuration/frontmatterConfiguration.ts`
- tests: `test/frontmatter/{okfFrontmatter,propertiesTable,schemaRegistry,schemaValidator,fileLinks,stemIndex}.test.ts`,
  `test/frontmatter/fixtures.ts`, `test/configuration/frontmatterConfiguration.test.ts`,
  `test/integration/genericMarkdown.test.ts`
- Checklist rows: 54.
- Brief: settings `bundleRoot`, `projectRoot`, `allowOutsideWorkspaceLinks`, `propertiesTable`,
  `strictAdditionalProperties` (defaults, effect); schema cache invalidation; diagnostics wording
  (UX-23); the 001 findings UX-22/UX-24 (not approved: decide requirement or known limitation).
  Docs: README "Open Kownledge Format", "Linked-File Annotations". Fixtures `07-10, 14`,
  `test/visual/fixtures/_schema/`.

## 7. frontmatter-editing (FMEDIT)

Editing the properties table: field values, lists, nullable values, booleans in one click,
enum and key suggestions, add/remove/rename field, title, minimal diffs (only the field
changes), Enter/Escape conventions, saves refused when stale or invalid.

- src: none exclusive (`source_dirs: []`): implementation is in `okfFrontmatter.ts`
  (`createFrontmatterField*Patch`, `guardedPatch`, `frontmatterAddPlacement`), `propertiesTable.ts`
  (edit controls), `src/extension.ts` (`previewFrontmatterSave` handler, `postFrontmatterEditError`)
  and `src/webview/scrollSync.ts` (page editors). Markers go there.
- tests: `test/frontmatter/{frontmatterPreservation,frontmatterFence}.test.ts`,
  `test/integration/previewEditing.test.ts`
- Checklist rows: 16.
- Brief: inventory each field type editor and its keyboard behaviour, every error message of
  `postFrontmatterEditError`, preservation guarantees (comments, quoting, order, CRLF), the 001
  findings UX-16..UX-21, UX-38, UX-39 and their fix status.

## 8. layout-width (LAYOUT)

First-element gap (40 px everywhere, toolbar clearance), Margin/Auto/Full width modes, max
content width setting, breakout of wide tables/figures/code in Auto, 16 px side margins in Full,
overflow, narrow (≤ 480 px) and wide panes.

- src: `src/webview/widthMode.ts`, `src/webview/firstClearance.ts`
- tests: `test/webview/{firstClearance,geometryChecks}.test.ts`, `test/shared/geometry-checks.js`
- Checklist rows: 92 (84 visual: the largest family; most lines repeat page-wide checks).
- Brief: write the page-wide properties as global behaviours first (no horizontal overflow,
  first gap, toolbar clearance), then the per-mode/per-element ones; dedupe the 84 scenario lines
  by assertion, not by fixture. Setting `preview.maxContentWidth` (0..2400, default 960). Archives
  010, 011. Fixtures `23-29, 32, 34`.

## 9. theme-zoom (THEME)

Host themes (light, dark, high contrast), forced Current → Dark → White → Cream cycle, cream
palette and contrast ≥ 4.5:1, zoom 70–200 % from the toolbar, persisted per workspace.

- src: `src/state/previewTheme.ts`, `src/webview/viewControls.ts`
- tests: `test/state/previewTheme.test.ts`, `test/webview/creamTheme.test.ts`
- Checklist rows: 17.
- Brief: theme mode storage key and `previewThemeModeChanged` validation, `themeChanged` from the
  host, zoom bounds and step, what is re-rendered on theme change (Mermaid). Archive 005. README
  "Preview Themes".

## 10. toolbar-navigation (TOOLBAR)

Floating toolbar (three rows, collapse chevron remembered per workspace, Tab order), sticky
headings (depth setting), TOC column, Back/Next history (documents, anchors, `(label)=`), link
following (relative, fragments, external not recorded), anchor button, editor title-bar and
explorer entries, Quick Open placement.

- src: `src/preview/previewToolbar.ts`, `src/webview/{toolbarCollapse,tocColumn,historyControls,linkNavigation}.ts`,
  `src/state/{navigationHistory,previewViewPreferences}.ts`, `src/navigation/previewNavigation.ts`
- tests: `test/webview/{tocColumn,linkNavigation}.test.ts`, `test/state/{navigationHistory,previewViewPreferences}.test.ts`,
  `test/navigation/previewNavigation.test.ts`, `test/integration/previewHistory.test.ts`
- Checklist rows: 56.
- Brief: every toolbar button (C-TB) with state transitions, tooltips and keyboard; `previewLink`,
  `previewLinkDiscover`, `previewLinkTargets`, `navigateAnchor`, `previewHistoryGo/State`; refusals
  while a block editor is open; menus in package.json. Archive 012, 016 (T08, T11). README
  "Floating Toolbar".

## 11. block-editing (BLOCK)

Edit mode toggle, block editors (raw Markdown, monospace, autosave/commit, Escape/Cancel,
Cmd/Ctrl+Enter, Home/End, wrapped lines, undo as one step), insert points and "Start writing",
move up/down, multi-block selection, copy/cut/paste as exact Markdown, edit lock after reload,
real typing behaviour.

- src: `src/webview/{textEditing,blockSelection}.ts`, `src/mapping/{blockMove,blockRange,insertion,textDiff}.ts`,
  `src/state/editLock.ts`
- tests: `test/webview/{textEditing,blockSelection}.test.ts`, `test/mapping/{blockMove,blockRange,insertion,textDiff}.test.ts`,
  `test/state/editLock.test.ts`, `test/integration/{blockMove,blockClipboard,realInput}.test.ts`,
  `test/integration/realInput/harness.ts`
- Checklist rows: 48 (expect more from `?` rows moved in).
- Brief: messages `previewEditOpen/Save/Cancel/ModeChanged`, `previewEditSource`,
  `previewBlockMove(Result)`, `previewBlocks*`; refusal rules (stale, frontmatter, `{include}`,
  bounds); 001 findings UX-01..UX-11, UX-35..UX-37; archives 002, 003, 017, 019. Docs
  `docs/interaction-parity-evidence.md`, `docs/scroll-anchoring.md`.

## 12. palette-slash (PALETTE)

Edition palette (Strict/GFM/MyST modes, additive; mode select per workspace and
`editing.defaultPaletteMode`; Cmd/Ctrl+Shift+M), every palette button and popover (heading,
colour, link panel Cmd/Ctrl+K, table grid, emoji, alert, code language, figure form, `{ref}`,
`{doc}`, `{cite}` pickers), sticky placement above tall edit boxes, slash menu (completion,
aliases, variants, ranking, keyboard, no-match, viewport flip), image picker and image paste.

- src: `src/webview/{editActions,editPalette,slashMenu,linkPanel,figurePanel,figureDirective,pasteImage,hostRequests,caretRect}.ts`,
  `src/mapping/{imageReference,pastedImage,mystTargets}.ts`, `src/preview/bibScan.ts`,
  `src/configuration/editingConfiguration.ts`
- tests: `test/webview/{editActions,editPalette,slashMenu,figureDirective,caretReveal,hostRequests}.test.ts`,
  `test/mapping/{imageReference,pastedImage,mystTargets}.test.ts`, `test/configuration/editingConfiguration.test.ts`,
  `test/integration/{paletteMode,mystPickers,imagePicker,imagePaste}.test.ts`
- Checklist rows: 150 (30 palette buttons, 53 slash entries, 11 messages).
- Brief: one behaviour per action (output Markdown, toggling, selection handling, mode/scope
  visibility), per popover/panel (fields, validation, focus), per host request (bounds, refusal,
  `<type>Result`); slash menu rules from post-plan P11; the open question "MyST mode shows both
  `<kbd>` and `{kbd}`". Archives 016, 018. README "Slash Menu".

## 13. table-editing (TABLE)

Cell editors and cell bar (cell-scope palette actions), Tab/Enter/arrow navigation, add/remove
rows and columns, column alignment, `|` escaping, minimal diffs (only the edited cell's line).

- src: `src/webview/markdownTable.ts` (page wiring in `scrollSync.ts`)
- tests: `test/webview/{markdownTable,markdownTablePreservation}.test.ts`
- Checklist rows: 23.
- Brief: parse/serialize preservation rules, every cell-bar control, keyboard map, 001 findings
  UX-12..UX-15, archives 002 T5, 016 T35; the 360 px cell-bar gap (followups).

## 14. review-annotations (REVIEW)

Comment and TODO chips (`<!-- -->`, Ctrl+/ TODO toggle, show-comments setting), review threads
in `<name>.comments.json` (create on selection, Cmd/Ctrl+Alt+M, reply, resolve/reopen, delete
with confirmation, author from setting → Git → OS), re-anchoring and orphans, sidecar renames,
incoming changes since HEAD (green bars, Diff button, setting).

- src: `src/comments/{anchoring,author,commentModel,commentStore}.ts`, `src/render/commentMarkers.ts`,
  `src/webview/{chipToggle,commentCompose,commentThreads,incomingChanges,incomingToggle}.ts`,
  `src/git/headBaseline.ts`, `src/mapping/lineDiff.ts`, `src/configuration/commentsConfiguration.ts`
- tests: `test/comments/*.test.ts`, `test/rendering/commentMarkers.test.ts`,
  `test/webview/{chipToggle,commentCompose,commentThreads,incomingChanges}.test.ts`,
  `test/state/{headBaseline,headBaselineUserName}.test.ts`, `test/mapping/lineDiff.test.ts`,
  `test/configuration/commentsConfiguration.test.ts`,
  `test/integration/{incomingChanges,reviewComments,commentWrite,commentAnchors}.test.ts`
- Checklist rows: 50.
- Brief: sidecar format v1 and validation, write queue and refusals (dirty/invalid sidecar,
  read-only), re-anchoring algorithm limits (D30, ≥ 12 chars, fuzzy rules), incoming-change
  computation limits (MAX_DIFF_LINES/EDITS, untracked file: only negative case tested), archives
  013, 014, 020. README "Review Comments".

## 15. lifecycle-sync (LIFE)

Activation, Open Preview to Side (command, keybinding, menus), Open With custom editor, refresh,
panel title, reload/restore (serializer, missing source), dirty snapshots, incremental content
patches (setting), status pages, scroll sync both ways and its settings, mark editor selection,
double-click to editor, coexistence with the built-in preview, workspace folder removal.

- src: `src/extension.ts`, `src/build/buildQueue.ts`, `src/preview/{contentPatch,webview}.ts`,
  `src/webview/{scrollSync,anchorPolicy}.ts`, `src/mapping/sourceMapping.ts`,
  `src/state/{boundedState,previewState}.ts`, `src/configuration/previewConfiguration.ts`
- tests: `test/build/buildQueue.test.ts`, `test/mapping/sourceMapping.test.ts`,
  `test/state/{boundedState,previewState}.test.ts`, `test/webview/{scrollSync,anchorPolicy,contentPatch}.test.ts`,
  `test/configuration/previewConfiguration.test.ts`, `test/shared/lineDelta.ts`,
  `test/integration/{stockCoexistence,dirtySnapshots,sourceMapping,lifecycle,serializer,workspaceDisposal}.test.ts`,
  `test/integration/{scroll-sync-suite,reload-suite,extensionApi}.ts`
- Checklist rows: 38 (16 contributes; no visual scenario).
- Brief: only the lifecycle/sync behaviours of `extension.ts` and `scrollSync.ts` belong here (the
  other scopes' handlers are inventoried by their owners); render queue states, pending overlay,
  pairing, status page labels (`PREVIEW_STATUS_LABELS`), bounded state limits, 001 findings
  UX-25..UX-32. Docs `docs/preview-lifecycle.md`, `docs/scroll-anchoring.md`,
  `docs/feasibility-dirty-snapshots.md`.

## 16. trust-security (TRUST)

Restricted Mode (read-only previews, no Edit button, refused messages), standalone files outside
the workspace (read-only, resource root), CSP with nonce and no unsafe-inline, HTML sanitizer
allow-list, resource policy (local roots, images), message validation envelope, user-facing text
contract, package contract.

- src: `src/security/{csp,html-sanitizer,resource-policy}.ts`, `src/preview/previewMessages.ts`
- tests: `test/security/{html-policy,package-contract,resource-policy,userFacingText}.test.ts`,
  `test/webview/previewMessages.test.ts`, `test/integration/{trusted,untrusted,standalone}-suite.ts`
- Checklist rows: 11 (each C-MSG row also needs a refusal SwRS here or in its owner scope:
  decide one rule and apply it to all 57 messages).
- Brief: list every refusal path per message type in trusted/untrusted/standalone previews, every
  sanitizer rule (tags, attributes, URL schemes, colours), the CSP directives, the absence of a
  `capabilities` entry in package.json (C-PKG). Docs `docs/security-evidence.md`,
  `docs/release-evidence.md`.
