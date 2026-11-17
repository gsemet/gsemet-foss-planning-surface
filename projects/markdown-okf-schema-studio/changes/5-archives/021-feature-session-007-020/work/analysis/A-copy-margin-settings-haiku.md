Read-only analysis of markdown-okf-schema-studio (branch dev/gsemet, HEAD 9df67aa). Nothing was modified; no builds or tests were run.

## 1. copy-code-block

(a) Current state: there is no copy affordance and no clipboard code anywhere in src/ or test/ (grep "clipboard|writeText" returns nothing). Code blocks are rendered in src/render/mystRenderer.ts (code node handling ~L956-975, highlight call at L1503). src/render/highlight.ts `highlightCodeBlocks` (L231-296) rewrites `<pre><code>`; it returns early for unlabelled blocks with no line numbers or filename (`if (!language && !shouldWrapLines && filename === undefined) return match;`), so plain blocks would be skipped. The CSS is `#sphinx-myst-preview-content pre` in src/preview/previewStyles.ts (~L1499-1510): `overflow-x: auto`, no `position`. The page CSP (src/security/csp.ts) has no clipboard directive and `script-src` only allows the nonce, so inline `onclick` is blocked; use a delegated listener.

(b) Approach:
- Server side: after `highlightCodeBlocks` (mystRenderer.ts:1503), inject a button for every `<pre><code>` (not only highlighted ones). Put it in a small wrapper `div` with `position: relative`, so it sits outside the `overflow-x:auto` box and does not scroll away. Use `data-*` attributes and no inline handler. `button` is already in the sanitizer allowlist (html-sanitizer.ts:63). Server-side injection survives the incremental patch (src/preview/contentPatch.ts replaces the inner HTML of `<main>`; it refuses content containing `<script` or `nonce`).
- Webview: add a document-level delegated click listener in src/webview/scrollSync.ts. Register it before the block-edit handler at ~L2189 (`target.closest?.("pre")`), and call `stopImmediatePropagation`, following the checkbox pattern at ~L3489. Copy `code.textContent` (not `pre`, which contains the filename label). Line numbers are data attributes, so textContent is clean.
- Clipboard: `navigator.clipboard.writeText` is not blocked by the CSP. Whether the webview iframe grants clipboard-write permission is not verifiable from this repo. The robust route is `postMessage({type:"previewCopyCode", text})` to the host, validated in the chain in src/extension.ts (union at L112; validator ~L411-550; cap length like the 4096 limit used for `previewLinkDiscover`), then `vscode.env.clipboard.writeText`. Recommend the host route.

(c) Files: src/render/mystRenderer.ts, src/render/highlight.ts (optional), src/preview/previewStyles.ts, src/webview/scrollSync.ts, src/extension.ts.

(d) Risks: edit mode (a click on a `pre` opens the whole-block editor at scrollSync ~L2189, so the button must stop propagation); the double-click reveal at ~L3580 when edit mode is off; the wrapper changes the DOM around `pre`, and scrollSync uses `closest("pre")` at ~L2189, ~L2856 and ~L2972; the visible button must not show over diagrams (mermaid/plantuml are not `pre`); dark, light and cream contrast; narrow widths; text selection.

(e) Tests to mimic: test/rendering/highlight.test.ts (regex-on-HTML style), test/rendering/renderPipeline.test.ts, test/webview/previewStyles.test.ts (CSS regex asserts), test/webview/scrollSync.test.ts (vm harness with RuntimeElement, `createScrollSyncScript`), test/integration/previewEditing.test.ts (host message handling), test/visual/scenarios.ts plus test/visual/capture.py.

(f) Decisions: show the button in edit mode too? Copy the raw source or the rendered text? Include plain (unlabelled) blocks? Show on hover only or always? Copy feedback (checkmark, toast)?

(g) Size: S (about M if the host message route is added).

## 2. bug-one-line-top-margin-missing

(a) Current state (preview mode):
- `#sphinx-myst-preview-content` (previewStyles.ts ~L1226-1232) has `padding: 0 gutter ...`, with no top padding. `body` margin is 0, and nothing sets margin-top on the container.
- A paragraph gets `margin: 0 0 1em` (~L1293). So a text-first document has zero top margin.
- `h1` has `margin-top: 0.6em` (~L1277), which is about 16.8px at 28px. `h2` keeps `1.6em` from the generic heading rule (~L1269), about 33.6px. `h3` is about 28px. Margins collapse through `main` and `body`, so the first heading's margin is the page offset. This explains the three different heading-first offsets.
- Empty document: `.sphinx-preview-insert-point--start.sphinx-preview-insert-point--first { margin-top: 24px }` (~L509-511, added in 47d3c55).
- The properties table: `[data-okf-properties] { margin: 0 0 1.5em }` (~L1255-1258), so zero top margin.
- The edit-mode first block editor: `.sphinx-preview-block-editor--first { margin-top: 56px }` (~L540). It is applied in scrollSync.ts ~L2196-2200 only when there is no properties section.
- The toolbar is `position: fixed; top: 12px; right: 14px` (previewStyles.ts ~L271-282), about 38px tall. A zero-margin first line or table top-right therefore sits under it.
- commit 47d3c55 changed only the edit-mode editor frame and the empty-document button. It did not touch preview-mode text or heading spacing. Its changelog says the owner asked for 20-40px, and 56px was chosen for the frame.

(b) Approach: unify with one rule on the first in-flow child, for example `#sphinx-myst-preview-content > :first-child { margin-top: var(--sphinx-preview-first-block-top) }`, with that variable set to a single value, and reset the `h1`, `h2`, and `p` cases so they do not collapse differently. Alternatively, use `padding-top` on `main`. Either way, add the rule to the PREVIEW_THEME_CSS block so the properties table, paragraph, heading, and insert point are all covered. Check `scrollSync` scroll geometry (L256, L890) if `padding-top` is used on `main`.

(c) Files: src/preview/previewStyles.ts only, plus scrollSync.ts ~L2196 if the edit-frame constant changes.

(d) Risks: scroll anchoring and the anchor map use element offsets (scrollSync L256/L890); the visual baseline is already known to fail in places; the sticky headings band (fixed, top 0) and the reading offset (`--sphinx-preview-reading-offset`, scrollSync ~L455-465); the properties-table case, where the toolbar overlaps the badge; the content patch changes only inner HTML, so CSS changes are safe.

(e) Tests: test/webview/previewStyles.test.ts (the test at ~L663 for 56px and 24px is the pattern to extend); test/visual/scenarios.ts with the `topSpacingChecks` mode (~L60-63 and ~L833-871) and test/visual/capture.py `check_top_spacing` (~L1471).

(f) Decision: the target value, and whether it should be 24 or 56px (or 20-40px per the owner's note) for all first blocks.

(g) Size: S.

## 3. vscode-setting-rework

(a) All 13 settings are in package.json `contributes.configuration` (`"title": "Markdown OKF-Schema Studio"`). None declares `scope`, `order`, `enum`, `enumDescriptions`, `markdownDescription`, or `deprecationMessage`. The VS Code default scope applies. Read sites: src/configuration/*.ts, consumed in src/extension.ts.

| Key | Type / default | Read at | What it does |
|---|---|---|---|
| preview.scrollPreviewWithEditor | bool true | extension.ts 558, 1980-1987, 2063, 2451, 3411; scrollSync 97-104 (anchorToEditor default) | Editor scroll moves the preview. Description "Follow the editor viewport from the MyST preview" is inverted. The toolbar anchor button overrides it per panel. |
| preview.scrollEditorWithPreview | bool true | extension.ts 1918, 1947, 2454 | Preview scroll and reveal move the editor. Also gates double-click. |
| preview.markEditorSelection | bool false | extension.ts 1984, 2073 | Marks the active source line in the preview; works even when scrollPreviewWithEditor is off. |
| preview.doubleClickToSwitchToEditor | bool false | scrollSync ~3580 (ignored in edit mode); extension.ts 2457 | Double-click reveal. Also requires scrollEditorWithPreview, which the description does not say. |
| preview.maxContentWidth | number 960, 0-2400, step 50 | extension.ts 963; webview.ts (buildPreviewWebviewHtml); previewStyles.ts 2194 | Column width; 0 is full width. Normalization accepts any integer, so the step is not enforced. |
| preview.stickyHeadingDepth | number 3, 1-6 | scrollSync L65-70; extension.ts 562 | Sticky heading band depth. The description does not say "band". |
| preview.incrementalUpdates | bool true | extension.ts 975, 1111, 3421 | Kill switch for in-place content patch. |
| plantuml.jarPath | string "" | extension.ts 2799; plantUmlRenderer.ts 145-147 | Description says "Absolute path", but relative paths resolve against the workspace root. An empty value uses the `plantuml` executable from PATH. |
| frontmatter.propertiesTable | bool true | extension.ts 734, 960 | Shows the OKF properties table. |
| frontmatter.strictAdditionalProperties | bool false | extension.ts 931, 1173, 1506, 2130; okfFrontmatter.ts 1424 | Warns on fields missing from the schema. |
| frontmatter.bundleRoot | string "" | extension.ts 932 etc.; okfFrontmatter.ts 1426 | Bundle root for x-okf-link. |
| frontmatter.projectRoot | string "" | extension.ts 933 etc.; okfFrontmatter.ts 1427 | Project root for x-okf-link. |
| frontmatter.allowOutsideWorkspaceLinks | bool false | extension.ts 934, 2174; okfFrontmatter.ts 1429 | Allows document-relative x-okf-link outside workspace folders. |

(b) Approach: rewrite the descriptions in plain language. Use `markdownDescription` and `enumDescriptions` where they help. Group by a title prefix. Fix the inverted and wrong wording (scrollPreviewWithEditor, jarPath "Absolute", doubleClick preconditions). Consider `order` (supported by VS Code) for grouping. A real settings "UI" would be a separate webview, which is a larger project.

(c) Files: package.json; README/docs if they mirror the settings; test/security/package-contract.test.ts (contract test on contributes); test/configuration/*.test.ts (behaviour tests).

(d) Risks: the words "preview", "anchor", and "scroll" overlap with the toolbar's anchor button. Renaming keys breaks users, so keep keys and only change text.

(e) Tests: test/security/package-contract.test.ts (~L21 pattern), test/configuration/previewConfiguration.test.ts.

(f) Decisions: keep or rename keys; whether a settings webview is wanted; whether to reflect the toolbar anchor button in the setting description.

(g) Size: S for descriptions only; L for a custom settings UI.

## 4. clever-margin-break

(a) Current state: the column is set by `--sphinx-preview-content-max-width` on `:root` (previewStyles.ts 2194-2198, from `previewContentWidthCss(maxContentWidth)`). `#sphinx-myst-preview-content` uses `max-width: var(...)`, `margin-inline: auto`, and `width: 100%` (~L1226-1232). Tables use `display:block; width:max-content; max-width:100%; overflow-x:auto` (~L1710-1717). The overflow detection `markWideTables` (scrollSync ~L707-720) sets `data-sphinx-table-overflow`, which drives the edge shadows. `img` is `max-width:100%` (~L1347), so figures and images never widen. The attached image.png shows a wide table clipped at the column edge with the shaded scroll edge, which confirms the current behaviour.

Toolbar state today: the theme button cycles `themeModes` (scrollSync L86, L752-767). It is persisted in two places. The host keeps it in `workspaceState` through src/state/previewTheme.ts (`PREVIEW_THEME_MODE_STORAGE_KEY`, read/write/clear), and the webview keeps it with `vscode.setState`. The host validates the message in extension.ts (`isPreviewThemeModeChangedMessage`, L2355-2357, validator L535) and sends the initial value through `scrollContext` (L565). `anchorToEditor` and `editMode` use only webview state.

(b) Approach:
- Add a mode button in `renderPreviewToolbar` (src/preview/previewToolbar.ts) that cycles margin, auto, full. Keep it on `documentElement` as `data-sphinx-preview-width-mode`, like the theme attribute, so it survives content patches.
- CSS: for `table` and `figure`, when the mode is full, use `width: 100vw` (or the 100vw minus a 12px scrollbar, since the webview's scrollbar is 12px) and `margin-inline: calc(50% - 50vw)` relative to the container. For auto, apply only when `data-sphinx-table-overflow="true"`, which markWideTables already sets.
- Host: add the new message type to the union (extension.ts L112) and the validator, and send the initial mode through scrollContext (L565). Persist it with a new state module modelled on src/state/previewTheme.ts, or with webview `setState` for per-panel use.

(c) Files: src/preview/previewToolbar.ts, src/preview/previewStyles.ts, src/webview/scrollSync.ts, src/extension.ts, src/state/ (new module), src/preview/webview.ts (if the initial attribute is set server-side).

(d) Risks: breakout changes the heights of wrapped content, so the anchor map and scroll sync must be re-measured (the ResizeObserver path, stabilizeLayout). Table cell editors (`sphinx-preview-table-cell-editor`) move. The sticky band uses the same width variable but must not break out. On narrow panes, full equals the pane width, so the gutter is lost. With `maxContentWidth` 0, the modes are no-ops. Overlay scrollbars on macOS versus classic scrollbars on Windows affect the `100vw` maths, which is also relevant to the Windows item.

(e) Tests: test/state/previewTheme.test.ts (persistence), test/webview/previewStyles.test.ts (CSS asserts), test/webview/scrollSync.test.ts (toolbar state, vm harness), test/integration/previewEditing.test.ts or lifecycle.test.ts (message validation), test/visual/scenarios.ts with a new scenario and a capture.py check.

(f) Decisions: what "auto-margin" means. My reading is "break only when a table is wider than the column". What "large figure" means: a figure box, or an image enlarged past the column (which needs the `img max-width` rule lifted). Whether the state is global, per workspace, or per panel. The default mode. Whether breakout applies in edit mode.

(g) Size: M (L if the figure enlargement and edit-mode geometry are in scope).

## 5. rendering-difference-on-windows

The screenshot is not viewable. `.agents/changes/backlog/P2/rendering-difference-on-windows/Capture d'écran 2026-10-15 165830.png` is 0 bytes. The `.agents/changes/` directory is gitignored (.gitignore line 12). No copy was found in Desktop, Downloads, or Pictures. The intent file (01-intent.md) only embeds the file.

Commit dfb64f7 ("fix: UI discrepancies with Windows") touches src/preview/previewStyles.ts (~27 lines) and test/webview/previewStyles.test.ts (+6). Its main source change is:
- `--sphinx-preview-border` moved from `:root` to a `body` rule (previewStyles.ts ~L116-126). The test at test/webview/previewStyles.test.ts:29-31 pins it. Custom properties that use `var()` resolve at the element that declares them. The `:root` copy therefore resolved against the host's root colours and ignored the body-level dark/white overrides.
- The dark and white theme blocks gained about 11 `--vscode-*` overrides each (widget, input, button, error colours).

The rest of the commit (images, pyproject.toml, test/build/test_release.py, a fixtures folder) is unrelated noise.

Verdict: the border part is a plausible root-cause fix and is test-pinned. The toolbar and input colour overrides were not tested visually in this commit. Whether the screenshot's issue is fixed cannot be confirmed without the image. A new 0-byte image was checked and no other copy exists locally. Next step: re-capture the screenshot on Windows, or re-add the file.