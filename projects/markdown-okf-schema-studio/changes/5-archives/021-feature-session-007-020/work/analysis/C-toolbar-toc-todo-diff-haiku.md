Read-only analysis of /Users/az02065/Projects/DevTools/markdown-okf-schema-studio (branch dev/gsemet). Nothing was modified and no builds or tests were run. Line numbers are from the current tree.

Cross-cutting facts
- The extension never uses git. There is no vscode.git reference, no extensionDependencies in package.json, and no git spawn (child_process is used only for uv in build/sphinxBuild.ts:203 and PlantUML). The engine requires vscode ^1.95.0 (package.json engines).
- No zoom feature exists anywhere in src.
- No TODO syntax exists in src, docs, or sphinx. No test covers HTML comments.
- Preview headings carry data-line / data-end-line (test/rendering/mystFeatures.test.ts:816-818) and no id attribute. Slugs are computed only in src/navigation/previewNavigation.ts:40 (markdownFragmentRange).
- Renderer: parse with myst-parser, emit HTML with myst-to-html (src/render/mystRenderer.ts:72-77, renderMyst at :1462). Source-line mapping is attached as data-sphinx-source-file / data-sphinx-source-line / data-sphinx-source-end-line (src/mapping/sourceMapping.ts:9-12).

1. Toolbar additions (back, next, zoom, margin toggle, "split on 2 lines")

(a) Current state
- Toolbar markup is in src/preview/previewToolbar.ts (REFRESH, ANCHOR, EDIT, THEME buttons; renderPreviewToolbar at :9-11). It is fixed top-right (src/preview/previewStyles.ts:271-283, inset-block-start 12px, inset-inline-end 14px).
- Button wiring is in scrollSync.ts:88-91 (querySelector on data attributes). Theme cycling is cyclePreviewThemeMode at :753.
- Link click path: linkNavigation.ts installLinkNavigation (click/auxclick/Enter/Space, :40-53) posts previewLink. Its handler is extension.ts:2447 → handlePreviewLink at :2227.
  - Anchor (#frag) links: no navigation is pushed. The host posts navigateAnchor (:2255-2270) and scrollSync.ts:3382-3420 scrolls with programmaticScroll. Nothing is recorded.
  - Local .md links (including wiki links, resolved by resolvePreviewNavigation in previewNavigation.ts:130): the host calls vscode.open on the target in ViewColumn.One with preview:false (extension.ts:2304). That opens a text editor tab. The preview then retargets because it follows the active editor: onDidChangeActiveTextEditor → followActiveEditor (:3220) → switchPreviewDocument (:2514), which reuses the same panel.
  - A locked preview (followsActiveEditor=false, set at :3172) does not retarget. The link still opens the file in the text editor.
  - Per-document scroll/state is kept in preview.states (BoundedMap, :202, :2539-2545). It is in-memory only, not persisted.
- Persistence today: edit mode in workspaceState (EDIT_MODE_STORAGE_KEY, extension.ts:283, :2363); theme mode in workspaceState (previewTheme.ts). Anchor mode is in webview vscode.getState only.

(b) Approach
- Back/Next: keep a host-side stack per ActivePreview: { documentUri, line/scroll, sourceLine }. Push in switchPreviewDocument before retargeting, and in navigateAnchor. Back/next post previewNavigate{direction} from the webview. The host either openTextDocument + showTextDocument (which re-triggers follow) or calls switchPreviewDocument directly. Clear forward on a new push. Cap at about 50 entries (BoundedMap pattern). Anchor jumps should push too, so back returns to the previous scroll position.
- Zoom in/out: CSS variable on the content (font-size scaling via a :root var on the same pattern as previewContentWidthCss, webview.ts:196/previewStyles.ts:2194). Store the value in webview getState, or workspaceState if it must be global. Keep scroll sync by recomputing layout (refreshReadingOffset already handles width changes).
- Margin on/off: toggle --sphinx-preview-content-max-width (previewStyles.ts:1226-1231; 0 means none, as in normalizePreviewContentWidth). Same mechanism as the existing maxContentWidth setting.
- "Split on 2 lines": undefined. Ask the user.
- The toolbar is a single flex row (:271). Five or more buttons will need overflow or a second row. Note --sphinx-preview-controls-height: 116px (previewStyles.ts:117).

(c) Files: src/preview/previewToolbar.ts, src/webview/scrollSync.ts, src/webview/linkNavigation.ts, src/extension.ts (handlePreviewLink, switchPreviewDocument, new stack), src/preview/previewStyles.ts, src/preview/webview.ts (CSS var injection), src/state/ (new history/zoom state module).

(d) Risks
- Back must not record host-initiated retargets as user history, or back/next will loop.
- Pushing on every switch can race the content-patch chain (contentPatch.ts, previewReady handling at extension.ts:2330-2340).
- The echo guard (EditorEchoGuard, anchorPolicy.ts:201) must still hold when history reveals a text editor.
- Zoom changes line heights, so the anchor map must be remeasured. The reading offset depends on the sticky band.
- Narrow widths: the toolbar grows and the sticky band's padding uses --sphinx-preview-toolbar-width (scrollSync.ts:423-428).

(e) Tests to mimic
- test/navigation/previewNavigation.test.ts (host resolution)
- test/webview/linkNavigation.test.ts (click/post shape, harness at :1-45)
- test/state/previewTheme.test.ts (storage pattern)
- test/webview/previewStyles.test.ts (toolbar CSS)
- test/webview/scrollSync.test.ts:1072 ("cycles preview theme modes and restores the saved selection") as the template for button state.
- test/integration/previewEditing.test.ts for the host round trip.

(f) Ambiguities: meaning of "split on 2 lines"; whether back/next history is per panel or global; whether zoom and margin persist globally or per document; whether a locked preview should also push history.

(g) Size: margin toggle XS; zoom S; back/next M (history stack plus anchor pushes); overall M.

2. TOC aside (toc-in-vscode-markdown-studio)

(a) Current state
- The renderer treats {toc} as build-only. It is listed in BUILD_ONLY_TYPES (mystRenderer.ts:457) and renders nothing in preview.
- Heading ids: none in preview. Anchors resolve by source line (markdownFragmentRange), then scroll via scrollTopForLine (scrollSync.ts:3382-3420).
- Heading enumeration already exists: updateStickyHeadings (scrollSync.ts:606-664) queries h1-h6 and reads tagName and textContent. Sticky band is fixed (previewStyles.ts:414-445). Its depth comes from stickyHeadingDepth (previewConfiguration.ts:17, default 3, max 6).
- Layout: content is #sphinx-myst-preview-content with max-width 960 and centred margin-inline auto (previewStyles.ts:1226-1231). Gutter clamp(16px, 8vw, 78px) (:118). The toolbar is fixed top-right at 12px, so an aside under it at the right edge is possible.
- Marksharp reference: not available offline, so not checked.

(b) Approach
- Build the TOC at runtime from the DOM (h1-h6 with data-sphinx-source-line), reusing the updateStickyHeadings enumeration. Click posts a scroll using scrollTopForLine, so no ids are needed. Alternative: generate it in mystRenderer from the AST, which is more testable but needs a shell change.
- Layout: make the content a two-column grid when the aside is on (content + 220-240px aside, sticky top below the toolbar at top: 116px). Hide it below about 900px.
- Toggle: a button in the toolbar (5th button). Persist in workspaceState (new key) or webview getState. Send a message for the host to set a runtime flag.

(c) Files: src/preview/previewToolbar.ts, src/webview/scrollSync.ts, src/preview/previewStyles.ts, src/preview/webview.ts, src/configuration/previewConfiguration.ts (if a setting is added: package.json :91-131 pattern), src/preview/contentPatch.ts (runtimeContextKey :164).

(d) Risks
- Shell comparison (contentPatch.ts:60-95, planContentPatch :122): anything outside #sphinx-myst-preview-content is part of the shell key. If the aside is rendered into the host HTML outside the content container, every render becomes a full reload and loses incremental updates. Generate the aside in the runtime, or keep it inside the content container.
- Any new setting that changes the HTML must be added to runtimeContextKey (contentPatch.ts:164-176), otherwise stale runtime context is reused.
- Scroll anchoring: the aside is a fixed element and must not change content flow (the rule the existing sticky band follows, previewStyles.ts:412-413).
- Narrow widths and sticky band overlap; themes (four modes, previewStyles.ts:154-235) need aside colors for each.
- Frontmatter table and table toolbars already use fixed or absolute positioning.

(e) Tests: test/webview/previewStyles.test.ts (CSS shape), test/webview/scrollSync.test.ts (sticky tests at :841-1072 as templates), test/webview/contentPatch.test.ts (shell key), test/configuration/previewConfiguration.test.ts (if a setting is added), test/state/previewTheme.test.ts (storage).

(f) Ambiguities: setting or toolbar-only toggle; default on or off; should the TOC be a host setting shared by all panels or per panel; whether h1 is included.

(g) Size: M (runtime TOC + toolbar button + grid CSS); L if generated in the renderer and the shell is changed.

3. TODO and comment markers (todo-comments)

(a) Current state
- HTML comments pass through the renderer as html nodes. renderMyst copies them to the output (only table fragments are rewritten; #comment nodes are dropped only inside rawHtmlChildren, mystRenderer.ts:563-568).
- The sanitizer (src/security/html-sanitizer.ts) has no comment branch. rewriteNode (:156) only handles removed elements, script, and resource attributes, so comments survive into the DOM invisibly.
- No TODO syntax exists. Admonition support exists (ADMONITION_TITLES, mystRenderer.ts:44-60ish; GitHub alerts at :1081-1115; details/summary for dropdown admonitions at :1115), which can be reused for the expanded zone.
- Raw HTML: parse5 is used (mystRenderer.ts:2; sanitizeTableStyle only for table styles).

(b) Approach
- Renderer: in renderMyst, before parsing (or as a post-pass over the html nodes), detect `<!-- ... -->` and `TODO:` / `TODO ` markers. Convert them into a dedicated node (for example a container with class myst-todo or myst-comment) that carries the source line.
- Webview: render a small inline chip (gray "<!--", green "TODO"). Click toggles a details-like zone (reuse the descriptionsCollapsed pattern for persistence, previewState.ts:9 and extension.ts:280-290). Do not rely on the sanitizer for HTML comments; the chip is generated markup.
- Ctrl+/ self-activation (from the block-edition-palette intent) is out of scope here.
- Persistence: the expanded state per document, via the existing collapsed-map pattern (workspaceState).

(c) Files: src/render/mystRenderer.ts, src/render/renderPipeline.ts (nothing else), src/security/html-sanitizer.ts (only if raw comment text must be shown), src/webview/scrollSync.ts (toggle), src/preview/previewStyles.ts, src/extension.ts (collapsed storage).

(d) Risks
- Exposing comment text: comments may contain sensitive text. Keep it in the DOM only when expanded, or escape it.
- Matching inside code fences and inline code must be excluded (renderMyst handles code via the AST; match on text nodes only).
- Incremental patch: new markup is inside the content container, so it patches normally. Expanded state must survive patches.
- Block editing: the chip sits inside a source block, which affects source mapping (sourceMapping.ts:80-108).
- The "--" inside comments and multi-line comments span several source lines.

(e) Tests: test/rendering/mystFeatures.test.ts (feature-level asserts), test/rendering/checkboxRendering.test.ts (a similar small marker feature to copy), test/rendering/checkboxMarkers.test.ts, test/security/html-policy.test.ts (ensure comment output stays safe), test/webview/scrollSync.test.ts for the toggle.

(f) Ambiguities: whether `TODO` must be a word boundary match; whether plain text TODO (not in a comment) counts; whether the comment body is shown or only its existence; whether expanded state is per document or global.

(g) Size: M.

4. Incoming (changed-line) markers (show-incoming-diff)

(a) Current state
- No git dependency at all. textDiff.ts only has minimalReplacement (:19), a prefix/suffix diff used for edits. It is not a line diff.
- Blocks map to source lines via data-sphinx-source-line (sourceMapping.ts). Multi-line paragraphs have lineTops measured in scrollSync (measureLineTops :329), so line-level marking is possible.
- Existing green marking: .myst-diff-line-addition for fenced diff code blocks (highlight.ts:195; previewStyles.ts:1559-1570). Reusing this class name would collide, so use a new one.
- The preview uses the live buffer (document.getText(), extension.ts:2255), so dirty buffers are already supported for navigation.

(b) Approach
- Baseline: vscode.extensions.getExtension("vscode.git")?.exports.getAPI(1) → repository for the document (getRepository(uri)), then repository.show("HEAD", relativePath) to get the baseline text. Verify method names and signatures against the installed vscode.git typings before relying on them. Do not add extensionDependencies; treat the API as optional.
- Alternative (no extension dependency): spawn git show HEAD:path in a child_process call. This is a new trust surface and would be blocked in untrusted workspaces (the extension already gates on workspace trust, extension.ts readOnly logic).
- Diff: implement a line diff (Myers or LCS) on the two texts. Produce added and modified line sets in current-buffer coordinates. Keep source line numbering identical to the renderer (lineOffset handles frontmatter, mystRenderer.ts:1433-1440).
- Mapping: mark a block when any of its [line, endLine] range is changed. Use lineTops to mark only the changed wrapped line when measurable.
- Messages: host computes the change set on render and on document change (debounced), and posts previewIncomingDiff{lines}. Webview applies data-sphinx-preview-changed attributes. Store the toggle in workspaceState.
- Refresh on git state change: repository.state.onDidChange, or on save/change of the buffer.

(c) Files: new src/mapping/lineDiff.ts (or extend textDiff.ts), src/extension.ts (git API, messages, toggle), src/webview/scrollSync.ts (apply marks, reapply after applyContentPatch at :254), src/preview/previewStyles.ts, src/preview/previewToolbar.ts (optional toggle), package.json (setting, if needed).

(d) Risks
- Dirty buffers: diff the live buffer against HEAD. The built-in gutter does the same.
- Untracked files: repository.show fails. Decide whether all lines are "added" (the built-in gutter typically shows them as added) or no marks.
- Files outside a repo, or submodules: no baseline, so no marks. Files outside the workspace in read-only mode (extension.ts readOnly) must not trigger git.
- Incremental patch: marks must be reapplied after applyContentPatch (scrollSync.ts:254) and re-rendered content.
- Performance: a full-file LCS is O(n*m). Use Myers, and cap size.
- CRLF handling (the renderer normalizes \r\n); compare normalized lines.
- Tests against a real git repo need a fixture; existing integration tests run in VS Code (test/integration/trusted-suite.ts).

(e) Tests: test/mapping/textDiff.test.ts (for a new line diff), test/mapping/sourceMapping.test.ts (line-to-block marks), test/webview/scrollSync.test.ts (marks applied and survive patch), test/integration/previewEditing.test.ts (as a template for the integration harness), test/state/previewTheme.test.ts (toggle storage).

(f) Ambiguities: whether to show deleted lines (a red marker at the adjacent block, as the sidebar does); whether untracked files count as all-added; whether the baseline is HEAD or the index; whether the feature depends on the vscode.git extension being present (the built-in ships with VS Code, but it can be disabled); whether the toggle is global.

(g) Size: L (git API plus a line diff, mapping marks, refresh on git change). M if only HEAD vs buffer with the built-in extension and no untracked support.

Summary of sizes: back/next M, zoom S, margin XS, TOC M (L if the shell changes), TODO M, incoming diff L.