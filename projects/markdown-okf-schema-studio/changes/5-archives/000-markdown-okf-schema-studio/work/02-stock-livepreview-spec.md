# Stock VS Code Markdown Preview: Behavioral Specification

Status: stock-preview research inventory. The P01-P24 acceptance contract below is superseded
by the active-file scope in `03-spec.md`; it is not an implementation or claim of tested parity.
Target: VS Code 1.139.0, bundled `vscode.markdown-language-features` 10.0.0 on macOS.
The installed application manifest establishes command IDs, defaults, menus and editor
contributions. Upstream implementation evidence was reviewed at VS Code 1.105.1 and
commit `4f2dfc552c95b9ff4729fa13f109bfda5f886d69` (see Evidence); details marked
"source-derived" must be verified experimentally on 1.139.0 before claiming parity.

## Scope and Invariant

"Stock preview" means the bundled rendered Markdown Webview, both the dynamic preview
(`markdown.preview`) and the optional fixed-file custom preview
(`vscode.markdown.preview.editor`). The experimental editable Markdown Editor
(`vscode.markdown.editor`), notebook renderer, and third-party plugins are **distinct**
surfaces; the Obsidian-like mode remains a separate bonus. The new MyST/Sphinx view
must be opt-in. Installation, activation and use must not alter the stock preview's
commands, default editor associations, rendering, scripts, styles, security settings,
keyboard bindings or behavior for unrelated Markdown files. Existing optional
Markdown-It plugins and preview styles must still work in the **stock** preview.

"At least the same" has two testable parts: (A) the stock preview itself remains
unchanged; (B) the opt-in MyST preview meets each applicable behavior below, plus
renders this project's Sphinx HTML correctly. The latter is **not inherited** from a
Webview panel. Every deviation must be documented as an explicit gap and must block
a claim of full parity. A separate Sphinx renderer cannot automatically execute
third-party Markdown-It syntax plugins; rendering their extra syntax in the MyST view
requires an explicit compatibility decision and tests, not a silent promise.

## Feature Inventory and Parity Tests

Evidence tags: **L** = installed 1.139.0 manifest; **D** = official user/API docs;
**S** = upstream source (revision-qualified); **T** = still needs hands-on local testing.
Each `P` item is an acceptance test for the new view, unless explicitly scoped to
stock-preview non-regression. The expected stock behavior is separate from the
proposed MyST implementation.

### Opening, Identity and Lifecycle

| ID | Stock behavior | Required verification | Evidence |
| --- | --- | --- | --- |
| P01 | Open Preview in current group; Open Preview to the Side beside source; source can be reopened from preview. Mac side shortcut is `Cmd+K V`. | Source/preview are side-by-side and the source can be recovered with one command. Stock commands/shortcuts remain untouched. | L, D |
| P02 | The installed `Shift+Cmd+V` binding calls `markdown.togglePreview` (not `markdown.showPreview`). `markdown.showPreview`, `markdown.showPreviewToSide`, `markdown.showLockedPreviewToSide`, `markdown.showSource`, `markdown.reopenAsPreview`, and `markdown.reopenAsSource` are contributed commands. | Verify stock toggle in both directions before and after enabling the new extension; provide distinct MyST commands without shadowing these IDs. | L |
| P03 | Dynamic unlocked preview follows the active Markdown editor; a locked preview stays with its file. Explicit link navigation can still replace a locked preview's content. | Switch source files and editor groups; lock/unlock and open Markdown links. Preserve per-file and per-panel identity. | S, T |
| P04 | Optional fixed-file rendered custom editor is separate from dynamic preview, works through Reopen With, and is not the default `.md` association. Multiple instances and previews can coexist; dynamic previews may be reused in the same column. | Open, split, move, close, reopen and restore multiple previews. Test an opt-in fixed MyST view without changing the default editor. | L, S, T |
| P05 | Commands appear in the editor title, explorer/context menus and command palette according to Markdown context. Native Refresh refreshes all managed dynamic and static previews; Lock and Security actions target the active preview. | Verify discoverability, refresh fan-out, active-view targeting for other actions and cleanup. New actions use their own context/command IDs. | L, S, T |
| P06 | Dynamic preview serializes resource, lock status, source column and scroll state across hidden panels/window reload; missing or deleted source shows an error rather than another file's content. | Hide/show, reload VS Code, delete/move source, reopen. Never show stale content as current. | S, T |

### Live Updates and Scroll

| ID | Stock behavior | Required verification | Evidence |
| --- | --- | --- | --- |
| P07 | Preview updates from the in-memory `TextDocument`, including unsaved edits, without saving it. First render is immediate; later refreshes are coalesced (about 300 ms in inspected source); explicit Refresh is available. | Edit without saving; type quickly, undo, save and request manual refresh. Newest document version wins; no source file is modified by preview. | S, T |
| P08 | Document/configuration/contribution changes and local resource changes can refresh the stock view. Local images are watched; HTTP/data images are not watched by the upstream implementation. | Edit a referenced image, included file and Sphinx configuration; observe correct invalidation in the MyST view without rebuild loops. | S, T |
| P09 | `markdown.preview.scrollPreviewWithEditor` defaults `true`: source viewport scroll positions the preview, using block source lines and fractional interpolation. Image loading is accounted for before initial positioning. | Top/middle/end of a long chapter; after inserting paragraphs, slow and rapid scrolling, images, code fences, hidden blocks and includes. Check scroll drift visually. | L, S, T |
| P10 | `markdown.preview.scrollEditorWithPreview` defaults `true`: scrolling the preview reveals the corresponding editor line; feedback loops are suppressed (about 50 ms throttling and 200 ms echo guard in inspected source). | Scroll both directions repeatedly, drag scrollbar, resize columns, change zoom; no oscillation or wrong editor targeted. | L, S, T |
| P11 | `markdown.preview.markEditorSelection` defaults **false** locally; when enabled it marks the current source line in the preview, not the exact selected text. | Test both setting states, cursor movement and selections without scrolling. A MyST equivalent may use its own setting, without changing stock defaults. | L, S, T |
| P12 | `markdown.preview.doubleClickToSwitchToEditor` defaults **false** locally; when enabled double-clicking rendered content reveals the mapped source line (link clicks remain link clicks). | Test disabled/enabled, ordinary paragraphs, headings, directives, and generated content with no source line. | L, S, T |
| P13 | The inspected Webview incrementally replaces the rendered body, preserves scroll and open `<details>` state, and discards responses for stale URI/document versions. | Expand/collapse content, edit nearby text, switch files during a slow build; preserve state and avoid cross-panel or stale updates. | S, T |

### Rendering, Navigation and Interaction

| ID | Stock behavior | Required verification | Evidence |
| --- | --- | --- | --- |
| P14 | Stock renderer supports CommonMark-oriented Markdown, tables and Markdown extensions; built-in math (KaTeX) and Mermaid rendering. Markdown-It syntax contributions may enhance the stock renderer. It does **not** render every Sphinx directive. | Compare headings, lists, tables, fenced code, footnotes, math, Mermaid, and representative MyST-only directives. Sphinx output must win for project chapters; stock stays unchanged. | D, S, T |
| P15 | Source links, local images and assets resolve relative to the source; headings and fragments navigate within preview, including cross-file Markdown links. Browser-safe URIs retain the underlying original link target. | Test same-file fragment, other chapter, heading with punctuation, local SVG/PNG, references and deep links; prevent path traversal. | D, S, T |
| P16 | `markdown.preview.openMarkdownLinks` defaults `inPreview` (alternative `inEditor`); `markdown.links.openLocation` defaults `currentGroup` (alternative `beside`). External links, local non-Markdown files and folders are routed appropriately. | Cover both settings, missing targets, `#L` fragments, `mailto:`, HTTPS and `vscode:` links. A Sphinx cross-reference must navigate to the intended chapter/anchor. | L, S, T |
| P17 | Preview renders syntax-highlighted code blocks and headings with stable anchors; it provides selectable/copyable rendered text, code-copy action and image-copy/open actions where available. | Test code copy, image context menu and keyboard text selection/copy, including Sphinx-produced figures. | S, T |
| P18 | Both stock preview variants enable the Webview find widget; `Cmd+F` searches rendered output, not raw source. Preview scroll state and current anchor survive ordinary updates. | Search text, find next/previous, navigate from results, edit, search again; verify no unexpected focus loss. | S, T |
| P19 | The installed manifest offers the optional Markdown Preview for both normal and diff editors. Inspected source also supports inline/side-by-side rendered diffs, change markers, inner highlights and synchronized scrolling via line mappings. | Baseline native diff preview. A project-local side-by-side diff Webview using stable APIs might approximate visual behavior, but native custom-editor diff integration currently uses proposed APIs. Treat identical native diff workflow as blocked on Stable until proven otherwise; never advertise parity based on a standalone approximation. | L, S, T |

### Configuration, Safety and Accessibility

| ID | Stock behavior | Required verification | Evidence |
| --- | --- | --- | --- |
| P20 | Installed defaults: `markdown.preview.breaks=false`, `linkify=true`, `typographer=false`, `frontMatter=table` (`hide`/`codeBlock` alternatives), font size `14`, line height `1.6`, platform font stack; `markdown.styles=[]`. | Baseline each stock setting. Decide MyST-specific equivalents when Sphinx semantics differ; changing a stock setting must still affect stock preview as before. | L |
| P21 | Built-in Markdown contributions can register preview CSS, scripts and Markdown-It plugins; user CSS can be set with `markdown.styles`. Built-in preview tracks theme/high-contrast appearance. | With representative third-party preview CSS/plugin installed, stock remains unchanged. Evaluate separately whether and how the Sphinx view supports customization without breaking its published theme. | D, S, T |
| P22 | Stock preview has a security selector and workspace-scoped security modes. It controls CSP, script execution, external/local resources and image/script warnings; Workspace Trust restricts some behavior. | Restrict the MyST renderer command itself in untrusted workspaces: `sphinx/conf.py` and extensions are executable Python, regardless of Webview CSP. With trust, require bounded asset roots, allowlisted schemes/elements, nonce-protected scripts and blocked-content errors. Never copy permissive stock modes blindly. | L, D, S, T |
| P23 | Stock Webview supports keyboard navigation, native semantic HTML, focus indications, theme/high contrast, screen reader and reduced-motion integration as available. No upstream WCAG conformance promise was found. | Navigate and use find/actions by keyboard; check focus, headings, links, images' alt text, reduced motion, zoom and contrast on both views. | D, S, T |
| P24 | The stock preview handles empty, missing and malformed documents without swapping another document's content. The new Sphinx preview additionally needs build progress, actionable diagnostics and last-good content marked stale. | Render empty/invalid directive; fail Sphinx; recover; close panel during build. Do not mistake an error fallback for feature parity. | S, T |

## Source-Derived Mechanics (Not Public Extension APIs)

The upstream Markdown renderer tags block elements with a zero-based `data-line`,
preserves raw link/image targets in `data-href`/`data-src`, and appends a final line
marker. Its Webview maps visible `.code-line` elements to fractional source positions,
skipping collapsed/invisible nodes; code blocks need special geometry handling.
Preview host/webview messages carry a document URI and version and are rejected if
stale. The inspected Webview uses incremental DOM morphing, image-size caching and
serialized scroll progress. Rendered diff previews additionally need an original-to-
modified line map and side-to-side scroll protocol. These techniques are *design
references*, not an obligation to copy internal/private code or exact timing values.
The supported VS Code APIs expose Webviews and editor events, not a reusable stock
preview controller or a Sphinx renderer. Re-test details against the local build.

## Project-Specific Superset

Stock parity alone cannot satisfy the user's MyST goal. The additional MyST view
must use this repository's Sphinx HTML builder and actual `sphinx/conf.py`, including
`myst_parser`, `sphinx_animation`, `sphinx_figure_layout`, `sphinx_design`,
`sphinx_copybutton`, `sphinx_togglebutton`, `sphinxcontrib.bibtex`,
`sphinxcontrib.mermaid`, `sphinx_tippy`, and local rendering hooks (including
HTML postprocessing). Also account for loaded but non-HTML-specific extensions:
`sphinx_revealjs` and `sphinxcontrib.confluencebuilder`. Build a fixture matrix
that classifies each configured extension and hook as HTML-visible, loaded-only,
or specific to another output target. Test an expected artifact for each HTML-visible
entry, as well as every **enabled** MyST extension
and every project-used directive/role: `{only}`/`{exclude}` HTML visibility,
`{cite}`, xrefs, `{include}`, figures, admonitions, animations, math, Mermaid,
substitutions and references. Render both dirty chapter buffers and dependent
content; Sphinx-generated fragments may have no direct editable source line and
must not navigate to a fabricated location. Full parity with non-HTML export
targets is a separate workflow, not a feature of the HTML preview.

## Alignment with the Existing Plan

| Goal | `01-plan.md` today | Verdict / required update before implementation |
| --- | --- | --- |
| No regression in native Markdown preview | Explicit opt-in, no global Markdown contribution or default editor | Aligned in design; verify P01-P24 in the native preview after installation and while both views coexist. |
| Full project MyST/Sphinx rendering | Reuse Sphinx, dedicated HTML view, representative fixtures | Aligned in architecture; build a complete configured-extension and used-directive matrix, not a single chapter smoke test. |
| Live unsaved render | Staged inputs, versioned dirty-document overlays, dependency invalidation and build cancellation | Aligned as a feasibility gate, not yet demonstrated. `book-prepare` writes `_nav.md`, `_toc_table.md`, and `index_latex.md` in chapter sources; the preview must instead stage equivalent inputs outside the worktree. |
| At least stock preview behavior | P01-P24 are gated; dynamic and fixed modes are explicit | Aligned as a contract, not yet achieved. Native rendered diff needs proposed VS Code APIs; a separate diff Webview is not identical integration. Obtain an explicit decision before claiming exact parity. |
| Bidirectional synchronized scrolling | Source-map feasibility spike | Direction is aligned, fidelity unproven; require P09-P13 on real long MyST pages with source-read transformations and includes. |
| Obsidian-like editing bonus | Delayed opt-in `CustomTextEditorProvider` | Appropriately separate; define interaction/undo contract after baseline read-only parity. |
| Restricted workspaces and safe assets | Trust is a hard gate; asset allowlist and hostile-input probes are required | Aligned as a security contract, not yet tested. Confirm that Sphinx, `just`, Python and local servers never start without trust, and test raw HTML, event attributes, SVG, `srcset`, CSS URLs, fonts, and hostile URI schemes/path escapes. |

**Decision gate:** a project-specific Webview can keep the native preview unmodified,
but cannot automatically be "exactly the same" as the native implementation.
If P01-P24 (including rendered diff) are non-negotiable, expand the implementation
plan and budget accordingly; stop at a failed feasibility gate instead of shipping
a partial replacement described as equivalent. Native custom-editor diff APIs are
[proposed APIs](https://code.visualstudio.com/api/advanced-topics/using-proposed-api)
not available for an ordinary Stable VS Code extension. A custom standalone diff
panel may offer equivalent visual interactions but not the exact native workflow.
The Obsidian-like editor needs its own specification for source-line/caret mapping,
IME, paste/drop, undo, multi-view synchronization, and accessibility before it can
be evaluated; it does not count toward read-only preview parity.

## Evidence and Limits

- **L:** Installed VS Code app `package.json` version 1.139.0 and bundled
  `extensions/markdown-language-features/package.json` version 10.0.0, inspected
  locally on 2026-09-25. They prove registrations/defaults, not runtime behavior.
- **D:** [VS Code Markdown user guide](https://code.visualstudio.com/docs/languages/markdown),
  [Markdown extension API](https://code.visualstudio.com/api/extension-guides/markdown-extension),
  [Webview API](https://code.visualstudio.com/api/extension-guides/webview), and
  [custom editor API](https://code.visualstudio.com/api/extension-guides/custom-editors).
- **S:** [Preview manager](https://github.com/microsoft/vscode/blob/4f2dfc552c95b9ff4729fa13f109bfda5f886d69/extensions/markdown-language-features/src/preview/previewManager.ts),
  [preview host](https://github.com/microsoft/vscode/blob/4f2dfc552c95b9ff4729fa13f109bfda5f886d69/extensions/markdown-language-features/src/preview/preview.ts),
  [renderer](https://github.com/microsoft/vscode/blob/4f2dfc552c95b9ff4729fa13f109bfda5f886d69/extensions/markdown-language-features/src/preview/documentRenderer.ts),
  [scroll Webview](https://github.com/microsoft/vscode/blob/4f2dfc552c95b9ff4729fa13f109bfda5f886d69/extensions/markdown-language-features/preview-src/scroll-sync.ts),
  [message types](https://github.com/microsoft/vscode/blob/4f2dfc552c95b9ff4729fa13f109bfda5f886d69/extensions/markdown-language-features/types/previewMessaging.d.ts),
  [diff sync](https://github.com/microsoft/vscode/blob/4f2dfc552c95b9ff4729fa13f109bfda5f886d69/extensions/markdown-language-features/preview-src/diffScrollSync.ts).
- **T:** No automated stock-preview interaction baseline was run; version-specific
  internals and menus must be measured in the local editor before development starts.
