# VS Code Sphinx/MyST Live View: Evaluation and Plan

Status: original proposal, superseded for scope by `03-spec.md`. The approved first release
previews the currently open Markdown file; book-wide and fixed-file requirements below are historical.
No extension, build logic, or editor settings have been changed.

## Decision

Build a small, opt-in VS Code extension in this repository, backed by the **existing Sphinx
project and build configuration**. Do not import `executablebooks/myst-vs-code` wholesale,
replace VS Code's built-in Markdown preview, or implement another MyST renderer.

| Approach | Strength | Durability / fit | Decision |
| --- | --- | --- | --- |
| Import `myst-vs-code` | Already integrates with VS Code's stock Markdown preview and inherits its scrolling | Its `extendMarkdownIt` pipeline uses `markdown-it-docutils`, not this book's Sphinx configuration. Version 0.11.0 was last published in 2021; dependencies and VS Code API baseline are old. Maintaining a fork still means building a second, incomplete Sphinx implementation. | Do not import. Consult its MIT-licensed code for isolated ideas if useful, retaining attribution if any code is copied. |
| Rewrite the whole renderer | Full control over the preview | Duplicates MyST, Sphinx directives, roles, cross-references, citations, extension hooks, output tags, and future changes. Violates the project's full-Sphinx principle. | Reject. |
| Base an extension on the existing Sphinx pipeline | Uses exactly the parser, HTML builder, extensions, theme, assets, and project configuration that publish the book | Requires a VS Code bridge for dirty buffers, preview navigation, source mapping, and scrolling. The renderer remains maintained upstream and in this repository. | Recommend, subject to feasibility gates below. |

`mystmd` is actively maintained and has `myst start`, but it is a distinct renderer and
project configuration, so it cannot guarantee parity with this Sphinx book. VS Code's
documented Markdown API adds `markdown-it` plugins, styles, and scripts to the **existing**
renderer; it does not provide a supported way to replace that renderer with Sphinx while
retaining all of its internal behavior. A separate preview is therefore intentional.

## Product Contract

- The stock Markdown editor and preview remain unchanged for all `.md` files. No global
  `markdown.markdownItPlugins`, `markdown.previewScripts`, default custom editor, or
  workspace setting that overrides stock preview. The new view opens only via an explicit
  `Sphinx: Open MyST Preview to Side` command for files under `book/chapters/`.
- The new view renders with the **HTML** Sphinx builder in development mode using
  `sphinx/conf.py` and staged equivalents of the `book-prepare` inputs used by
  `just book-serve-multipage`. Never invoke the source-writing `book-prepare` recipe
  from the preview: it writes three files under `book/chapters/`.
  HTML output is the visual target. PDF/Confluence/RevealJS-only content is not expected
  to appear in the HTML view; separate existing live servers cover those targets.
- Honor every MyST/Sphinx extension configured in `sphinx/conf.py`, including local
  extensions and theme hooks. Test citations, xrefs, `{include}`, admonitions, figures,
  Mermaid, animation, `{only}`/`{exclude}`, and generated assets as **actual output**, not
  merely recognized syntax. An extension requiring network services or external runtime
  assets may need explicit support and must be reported, not silently omitted.
- Live rendering must respond to **unsaved text edits**, not only file saves; also react to
  dependent files and configuration changes. Debounce/cancel obsolete builds and show a
  pending state. On build failure show diagnostics and retain the last successful render,
  clearly marked stale. Use a versioned overlay of all relevant dirty documents and
  invalidate Sphinx dependencies when they change. Do not mutate source files or
  auto-save the user's buffer. Never start Sphinx (which executes `sphinx/conf.py`
  and extensions), `just`, Python or a local server in an untrusted workspace.
- Match the user-facing behavior of the stock side-by-side preview: editor-to-preview and
  preview-to-editor scrolling, reveal source position on preview click, internal links and
  anchors, search/find, selectable text, keyboard navigation, accessibility, theme support,
  image/media rendering, state restoration, dynamic following/locking, opt-in fixed-file
  preview, and multiple documents/editor groups. Use `02-stock-livepreview-spec.md`
  (P01-P24) as the parity contract, including native rendered-diff limitations.
  These are acceptance targets, not capabilities inherited from VS Code's stock preview.
- Optional Obsidian-like live editing is a **separate mode** after read-only preview parity.
  Rendering and editing must share the `TextDocument` model, preserve Markdown bytes and
  undo/redo, and avoid making a rendered DOM the source of truth. Decide whether the desired
  behavior is editable rendered blocks, source-on-current-line, or only visual line wrapping
  before designing this phase; these are different products.

## Implementation Boundary

Place the VS Code extension under `` with its own
`package.json`, TypeScript source, tests, and packaged webview assets. `.github/` is for
repository automation, not extension source. Keep Sphinx integration close to its owner
(`sphinx/` for any minimal source-position hook) and add a targeted `just` entry for
development/build/check only when needed. Do not vendor the upstream extension. Preserve
its MIT license and notice if any substantial upstream code is reused.

1. **Feasibility spike (stop/go):** Run an isolated VS Code extension development host.
   Render one real chapter via the existing HTML Sphinx builder into a separate derived
   output directory. Prove that a VS Code webview can display its theme, relative images,
   CSS, JS, citations, and links under a restrictive CSP, using supported resource URIs or
  a constrained local bridge. Reject execution in untrusted workspaces. Probe raw HTML,
  SVG active content, `srcset`, CSS imports/URLs, fonts, media, hostile URI schemes,
  encoded traversal and symlink escapes with an explicit resource allowlist.
   No default-editor registration. If displaying authentic Sphinx HTML is incompatible
   with webview security or required scripts, assess an embedded browser/server alternative
   and document the resulting scrolling limitations before choosing it.
2. **Unsaved-content spike:** Feed versioned snapshots of relevant dirty `TextDocument`s
  into an isolated Sphinx preview build; stage required generated inputs outside the
  worktree. Prove unsaved chapter and included-partial edits with normal relative paths,
  plus concurrent dirty documents, bibliography/config changes and dependency-cache
  invalidation. Validate latency on a representative large chapter. Never run source-
  writing generators on keystrokes or overwrite their outputs in the repository.
3. **Source mapping spike:** Attach source-file/line identities to rendered Sphinx nodes
   through a preview-only doctree/HTML hook, retaining origin information across includes
   and the existing draft-banner injection. Establish a mapping for headings, paragraphs,
   directives, figures, and citations; identify unmappable generated fragments. Prove
   stable two-way scroll on a long chapter and after content insertion. If Sphinx source
   positions cannot meet this bar, pause rather than claiming stock-preview parity.
4. **Extension integration:** Separate dynamic follow/lock panel and optional fixed-file
  preview modes, explicit commands, process lifecycle, debounced/cancelable builds,
  safe error reporting, file/config/dependency watching, navigation and link routing,
  state persistence, and cleanup. Keep
   generated preview content isolated from production build outputs. Bind assets and link
   targets to the workspace; avoid arbitrary local-file access or executing untrusted HTML.
5. **Parity and optional edit mode:** Implement/test P01-P24 against the current
   built-in Markdown preview on macOS with small and long documents, dirty buffers,
   multiple groups, reopening, focus/scroll loops, images, and theme changes. Only then
   prototype a separate opt-in `CustomTextEditorProvider` for live editing, using
  `WorkspaceEdit` and VS Code's undo/save model; never make it the default `.md` editor.
  Native rendered-diff custom-editor APIs are proposed; decide whether to require exact
  native diff integration, accept an opt-in standalone visual diff, or wait for a stable
  API before advertising full parity.

## Verification / Release Gates

- Capture baseline native preview behavior before installation; repeat with the new
  extension enabled but unopened and with both views open. Native preview output,
  scroll behavior, Markdown commands, and unrelated `.md` files must not change.
- Compare generated HTML from the new preview against `just book-serve-multipage` for a
  representative chapter and fixture containing every configured MyST extension and
  project-local Sphinx feature. Any unsupported syntax is a release blocker for the
  stated goal, not a silent fallback to Markdown rendering.
- Extension-host integration tests for unsaved edits, cross-file invalidation, stale build
  cancellation, diagnostics, disposal/reopen, click navigation, and bidirectional scroll;
  browser screenshots on long pages to catch mapping drift. Include restricted workspace
  and hostile Markdown/resource-URI cases for webview security.
- Run the extension's focused tests and build, then `just book-check` and `just preflight`
  for any change to Sphinx configuration, hooks, or book output. Do not require the new
  extension to run for the existing book build or publishing workflow.

## Open Decisions Before Implementation

1. Is the required scroll sync **bidirectional** and pixel-precise, or is block/line-level
   synchronization acceptable? This determines whether the source-map spike can pass.
2. Does "all features" mean exact parity with the installed VS Code version's private
   Markdown preview implementation, or the explicit user-visible behavior matrix above?
   Exact implementation parity cannot be promised with a supported extension API.
3. For the bonus editor, which interaction is intended: rendered blocks except the active
   raw line, editable rendered blocks, or a source editor with visual wrapping only?

## Evidence

- Project: `CONSTITUTION.md` full-Sphinx rule; `sphinx/conf.py` extensions, MyST settings,
  theme, and source-read hooks; `justfile` `book-prepare` and `book-serve-multipage`.
- [Upstream extension source and MIT license](https://github.com/executablebooks/myst-vs-code).
- [VS Code Markdown extension API](https://code.visualstudio.com/api/extension-guides/markdown-extension).
- [VS Code webviews](https://code.visualstudio.com/api/extension-guides/webview) and
  [custom text editors](https://code.visualstudio.com/api/extension-guides/custom-editors).
- [Alternative MyST CLI](https://github.com/jupyter-book/mystmd).
