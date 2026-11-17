# 05 — Performance: Webview Lifecycle and Runtime Script

Part of the [deep analysis review](00-index.md) of `src/markdown-okf-schema-studio`.
This file covers how often the webview document is replaced, what each replacement costs, and the
work the injected runtime script
([scrollSync.ts](../../../../src/webview/scrollSync.ts))
does while the user scrolls and edits. Lines refer to `e1b4ad0`.

## Context

Every assignment to `panel.webview.html` (directly or through `setPanelHtml`) discards the webview
document and loads a new one: the renderer re-parses the page, re-executes the inline script,
re-applies the CSS, re-downloads and re-runs `mermaidPreview.js` when a diagram is present, and
re-measures the layout. The improvement proposal in
[editor-improvements/01-improvement-proposal.md](../../editor-improvements/work/01-improvement-proposal.md)
set "0 webview reloads per keystroke" as its first milestone; the current code still reloads several
times per edit.

## Findings

### PERF-05 — Each keystroke replaces the webview document three to six times

- **Severity**: High
- **Confidence**: Confirmed by code reading
- **Effort**: M (status) to L (content patching)
- **Location**:
  [extension.ts:749-792](../../../../src/extension.ts#L749),
  [extension.ts:456-486](../../../../src/extension.ts#L456),
  [extension.ts:589](../../../../src/extension.ts#L589),
  [extension.ts:646-675](../../../../src/extension.ts#L646),
  [extension.ts:691-747](../../../../src/extension.ts#L691),
  [extension.ts:2450-2492](../../../../src/extension.ts#L2450)

**What happens.**
For one edit, the following each assign a different HTML string:

| Trigger | Code path | When |
| --- | --- | --- |
| Queue enters `debouncing` | `handleQueueState` → `setStatus("pending", "Waiting for the latest edit.")` | immediately |
| Queue enters `building` | `setStatus("pending", "Rendering the active buffer.")` | +40 ms |
| Render ready | `updatePreview` → `panel.webview.html = html` | after render |
| PlantUML resolved | `scheduleDeferredPreviewWork` → `setPanelHtml` | after JVMs, if diagrams |
| Frontmatter refresh | `refreshFrontmatter` → `setPanelHtml` | +300 ms, if the table changed |
| Link enrichment | `scheduleLinkEnrichment` → `setPanelHtml` | +150 ms, if links resolved |

The status-only reloads exist to change one `<aside>` element. The frontmatter refresh produces the
same table as the one `updatePreview` just rendered without links, so the enrichment pass then
replaces it again with a linked version: frontmatter links visibly flicker between "pending" and
"resolved" on each edit. With the 488 KB page of chapter 08, each reload transfers and re-executes
roughly 150 KB of inline script and CSS before any content work.

**Fix.**
Proceed in two steps.

1. **Status by message.** Send `{ type: "previewStatus", status, message, diagnostics }` through
   `postMessage` and update the `<aside>` in the webview. Reassign `html` only when there is no live
   document (first render, error page, document switch).
2. **Content by message.** After the first load, send the sanitised `<main>` content (and the
   properties-table fragment separately) by `postMessage`, and apply it in the webview with a keyed
   DOM morph (for example `morphdom`, keyed on `data-sphinx-preview-block`), then re-run `measure()`
   and re-apply the anchor. The content is already sanitised on the host; parse it in the webview
   with `DOMParser` into an inert document before moving nodes. Keep the full reload path for CSP or
   nonce changes only.

Step 1 alone removes two of the three unconditional reloads. Step 2 removes the rest and also fixes
[STAB-02](07-stability-and-correctness.md#stab-02--the-inline-edit-lock-survives-a-webview-reload)
and [STAB-03](07-stability-and-correctness.md#stab-03--any-reload-destroys-an-open-inline-editor).

**Tests to add.**
Integration test counting `html` assignments (wrap the panel in a test spy): typing ten characters
produces at most one assignment (the first render) after step 2, and zero status-driven assignments
after step 1.

**Done when.**
Steady-state typing performs zero webview document replacements.

### PERF-06 — Saving the active document triggers a redundant full render

- **Severity**: Medium
- **Confidence**: Confirmed by code reading
- **Effort**: XS
- **Location**:
  [extension.ts:1801-1819](../../../../src/extension.ts#L1801),
  [extension.ts:1964-1984](../../../../src/extension.ts#L1964)

**What happens.**
The workspace watcher fires `onDidChange` for the active file when it is saved.
`refreshReferencedPath` sees that the path is the active document and calls
`refreshPreviewDocument`,
although the buffer that was just rendered is byte-identical to what was written. With
`files.autoSave: afterDelay`, this adds a render and a reload roughly every second while typing, and
it is also what destroys an open inline editor
([STAB-03](07-stability-and-correctness.md#stab-03--any-reload-destroys-an-open-inline-editor)).

**Fix.**
When the changed path is the active document and `preview.document` is open, skip the refresh if
`preview.document.version === preview.stage?.activeDocumentVersion`. Only an external modification
of a document that is *not* open (or a reload from disk, which bumps the version) needs a render.

**Done when.**
Saving an unchanged buffer performs no render.

### PERF-07 — The 5 MB Mermaid bundle is reloaded and every diagram re-rendered on each reload

- **Severity**: Medium
- **Confidence**: Confirmed by bundle size and code reading
- **Effort**: M
- **Location**:
  [mermaidPreview.ts](../../../../src/webview/mermaidPreview.ts),
  [webview.ts:256-266](../../../../src/preview/webview.ts#L256),
  [esbuild.mjs:21-29](../../../../esbuild.mjs#L21)

**What happens.**
`out/bundle/mermaidPreview.js` is 5.0 MB minified. Each document reload parses and compiles it again
and re-renders every diagram concurrently, including unchanged ones far outside the viewport.

**Fix.**
PERF-05 removes most reloads. In addition: render diagrams lazily when they approach the viewport
(`IntersectionObserver`); cache rendered SVG data URIs in the webview by `hash(source + theme)` and,
across reloads, in `vscode.setState`; render sequentially to avoid Mermaid's shared-state issues;
evaluate splitting diagram types with esbuild `splitting` (ESM output) so a flowchart does not load
every grammar.

**Done when.**
An edit outside a Mermaid block causes no Mermaid work.

### PERF-08 — Scrolling forces synchronous layout several times per frame

- **Severity**: Medium (High for long documents)
- **Confidence**: Confirmed by code reading
- **Effort**: M
- **Location**:
  [scrollSync.ts:411-447](../../../../src/webview/scrollSync.ts#L411),
  [scrollSync.ts:353-409](../../../../src/webview/scrollSync.ts#L353),
  [scrollSync.ts:103-129](../../../../src/webview/scrollSync.ts#L103),
  [scrollSync.ts:152-211](../../../../src/webview/scrollSync.ts#L152)

**What happens.**
Each animation frame during a scroll runs `postScroll`, which:

- calls `updateStickyHeadings`: `querySelectorAll` of every heading, then `getBoundingClientRect` on
  each of them, up to three passes with `textContent` writes between passes, forcing a layout per
  pass;
- calls `stateSnapshot`: `querySelectorAll("details")`, `getSelection().toString()`, and
  `vscode.setState`, which serialises the state to the host on every frame;
- posts `previewScroll` or `previewState` to the host, which validates it, may write
  `workspaceState`, and may reveal an editor range.

`measure()` (on resize, on every image load, and on every `ResizeObserver` callback) calls
`parseMappings`, which runs `getComputedStyle`, `getClientRects`, and `getBoundingClientRect` per
mapped block and, through `measureLineTops`, creates a DOM range and reads its rectangle for every
first character after a newline in every multi-line paragraph.

**Fix.**
Compute heading offsets in `measure()` and look up the active heading by binary search on `scrollY`,
so a scroll frame reads no geometry. Throttle `setState` and the host message to a trailing 100 ms,
always flushing on `pagehide`. Defer `measureLineTops` to blocks near the viewport, and coalesce
`ResizeObserver` and image-load callbacks into one `requestAnimationFrame`.

**Tests to add.**
Webview unit test with a counting fake DOM: one scroll frame performs zero `getBoundingClientRect`
calls on headings and at most one `setState` per 100 ms.

**Done when.**
A scroll frame on chapter 08 stays under 4 ms of script time in the webview DevTools profile.

### PERF-09 — Link discovery is repeated on every reload and runs uncached `findFiles`

- **Severity**: Medium
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [linkNavigation.ts:13-50](../../../../src/webview/linkNavigation.ts#L13),
  [extension.ts:1463-1490](../../../../src/extension.ts#L1463)

**What happens.**
`installLinkNavigation` starts with an empty `discovered` set on every page load, so each reload
re-posts every visible link. For each wikilink the host calls `vscode.workspace.findFiles` with
`**/<name>` once per navigation root. `linkDiscoveries` only de-duplicates requests that are in
flight and deletes the entry in `finally`. Every keystroke therefore runs a fresh workspace search
per visible wikilink.

**Fix.**
Resolve wikilinks with the existing `MarkdownStemIndex` instead of `findFiles`, and cache resolved
targets per `(request, document version)` on the host, invalidated by the stem watchers.
After PERF-05 step 2 the webview keeps its `discovered` set across content updates.

**Done when.**
Typing in a document with wikilinks issues no `findFiles` call once targets are known.

### PERF-10 — `retainContextWhenHidden` keeps every hidden preview alive

- **Severity**: Low
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [extension.ts:2093-2103](../../../../src/extension.ts#L2093),
  [extension.ts:2250-2252](../../../../src/extension.ts#L2250)

**What happens.**
Both the side panel and the custom editor set `retainContextWhenHidden: true`.
Each Markdown file opened with **Open With → Markdown OKF-Schema Studio** keeps a renderer, its DOM,
and possibly a loaded Mermaid instance in memory while its tab is hidden. VS Code documents this
option as having a high memory overhead. The runtime already persists scroll, disclosure, and edit
mode with `getState`/`setState`.

**Fix.**
Drop the option for the custom editor and rely on `getState`; keep it for the single side panel only
if the restore latency is unacceptable without it.

### PERF-11 — The runtime script and CSS are inlined in every page

- **Severity**: Low
- **Confidence**: Confirmed by measurement
- **Effort**: S
- **Location**:
  [scrollSync.ts:41-63](../../../../src/webview/scrollSync.ts#L41),
  [webview.ts:120-145](../../../../src/preview/webview.ts#L120)

**What happens.**
`createScrollSyncScript` rebuilds a 102 KB script string per render, including helper functions
serialised with `Function.prototype.toString()` from the minified bundle; 51 KB of CSS is inlined as
well. The strings are regenerated, re-parsed by parse5 (PERF-02), and re-executed by the webview on
each reload. Serialising functions with `toString()` also breaks silently if esbuild ever injects a
helper (for example `__name` with `keepNames`) that the serialised body references.

**Fix.**
Bundle the runtime as `out/bundle/preview.js` and `out/bundle/preview.css`, load them with the nonce
through `asWebviewUri`, and pass the per-render context as a `<script type="application/json">`
element read with `JSON.parse`.

**Done when.**
The per-render HTML contains no inline runtime code, and the runtime is a normal bundled module.
