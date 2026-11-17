# Improvement Proposal — `markdown-okf-schema-studio`

Date: 2026-09-25
Companion: [00-competitive-analysis.md](./00-competitive-analysis.md)
Goal: match Mark Sharp's *perceived* responsiveness and visual polish while keeping full
Sphinx/MyST fidelity. **Direct editing / WYSIWYG is explicitly out of scope.**

---

## Targets

| Metric | Today | M1 | M2 | M3 |
|---|---|---|---|---|
| Webview document reloads per keystroke | 3 | **0** | 0 | 0 |
| Scroll position survives a render | no | **yes** | yes | yes |
| Keystroke → paint (p50, one chapter) | ~1.4 s | ~1.2 s | **< 600 ms** | **< 200 ms** |
| Math typeset | no | no | **yes** | yes |
| Hung build recovery | never | **timeout + retry** | ✓ | ✓ |

---

## Tier 0 — Stop the bleeding (no architecture change)

Highest value per unit of risk. None of these touch Sphinx.

### T0-1 — Eliminate the triple webview reload  ⭐ highest priority

**Problem.** `setPanelHtml()` in `src/extension.ts` assigns `panel.webview.html` on every state
change. `handleQueueState` fires for `debouncing` **and** `building` (both call
`setStatus(preview, "pending", …)`), then `updatePreview` fires for `ready`. One keystroke ⇒ three
full document reloads, three DOM teardowns, three scroll restorations from a *stale* serialized
state.

**Design.**

- Assign `panel.webview.html` **once**, when the preview is created or the document is switched.
  That HTML is a stable *shell*: `<head>` with the CSP, the accessibility/theme `<style>`, the
  scroll-sync script, and the resolved `<link rel=stylesheet>` set; `<body>` with an empty
  `#sphinx-myst-preview-content` and the status `<aside>`.
- Subsequent renders `postMessage({ type: "render", body, diagnostics, status, stylesheets })`.
  The in-page script:
  1. captures `window.scrollY`, the focused block id, and open `<details>`;
  2. swaps `#sphinx-myst-preview-content.innerHTML = body`;
  3. adds any `<link>` not already present in `<head>`;
  4. re-runs `parseMappings()` and `stabilizeLayout()`;
  5. restores scroll **by source line**, not by pixel offset, so a reflow does not jump;
  6. restores focus and disclosure state.
- Status transitions (`debouncing`, `building`, `stale`, `error`) become
  `postMessage({ type: "status", … })` that only touches the status `<aside>` and a CSS class
  on `<html>` — no content swap at all.

**Why this is now safe.** It was not safe before the persistent staging root landed: every render
produced a new `mkdtemp` output directory, so `localResourceRoots` and every stylesheet URI
changed and the shell could not be reused. With `createStageRoot()` reused across builds the
output paths are stable, so the shell's `<link>` hrefs stay valid.

**Touches.** `src/extension.ts` (`setPanelHtml`, `setStatus`, `updatePreview`, `handleQueueState`),
`src/preview/webview.ts` (split `buildPreviewWebviewHtml` into `buildPreviewShellHtml` +
`buildPreviewBodyFragment`), `src/webview/scrollSync.ts` (message handlers, `applyRender`).

**Risks.** The scroll-sync mapping cache must be invalidated on every patch — do it inside
`applyRender` before restore. `innerHTML` assignment is acceptable because the fragment has
already been through `rewriteSphinxHtml`; keep the CSP unchanged (`script-src` nonce-only means
injected `<script>` in the fragment still cannot execute).

**Tests.** New `test/integration/incrementalRender.test.ts`: assert the webview document is
assigned exactly once across N edits; assert scroll position is preserved across a render; assert
a `building` status does not clear the content.

---

### T0-2 — Cache stylesheet sanitization across renders

`buildPreviewWebviewHtml` creates a fresh `resolvedStylesheets` `Set` per call, so the whole
Shibuya + `pygments.css` + custom stylesheet set is re-read, regex-sanitized and re-written to
disk on **every** render.

Introduce a module-level cache keyed by `absolutePath → { mtimeMs, size }`. Skip `sanitizeCss` and
the write-back when the entry is unchanged. Clear it in `disposePreview`. With T0-1 this becomes
mostly moot for the steady state (the shell is built once), but it still matters on document
switch and on `_static` refresh.

---

### T0-3 — Single parse5 pass

`rewriteSphinxHtml` parses and serializes, then `injectContentSecurityPolicy` parses and
serializes the whole document again, and `injectAccessibilityStyles` / `injectScrollSyncScript`
do regex string splicing on top. Fold CSP, style and script injection into the **existing**
`rewriteSphinxHtml` tree walk and serialize exactly once.

---

### T0-4 — Spawn timeout and watchdog in `runSphinx`

**Problem.** `runSphinx` in `src/build/sphinxBuild.ts` has no timeout. A hung `uv` or
`sphinx-build` wedges the `active` slot of `BuildQueue` forever; `startPending()` early-returns
while `active` is set, so the preview freezes permanently with no recovery short of closing the
panel.

Add a configurable timeout (default 30 s, new setting `sphinxMystLiveview.build.timeoutMs`).
On expiry: `SIGTERM`, then `SIGKILL` after 2 s, reject with a `SphinxTimeoutError`, publish a
`failed` phase carrying an actionable diagnostic, and let `drainPending()` free the slot.
Retain `lastGood` so the preview degrades to `stale` rather than blank.

**Tests.** `test/build/sphinxBuild.test.ts` — fake a never-resolving child process, assert the
timeout fires, the process is killed, and the queue slot is released.

---

### T0-5 — Narrow the file watcher

`new vscode.RelativePattern(workspaceFolder, "**/*")` makes the OS watch the entire repository
(including `_build/`, `output/`, `node_modules/`, `.venv/`), and `IGNORED_WATCH_SEGMENTS` filters
only *after* the event has already cost us. Replace with a small set of targeted patterns derived
from the current stage's `dependencies` (images, includes, `refs.bib`, `_static`) plus
`**/*.{md,bib,yml,png,svg,jpg}`, and keep the segment blacklist as a second line of defence.

---

### T0-6 — Theme and settings changes should not rebuild

`notifyTheme()` posts `themeChanged` **and** forces a full rebuild. Every
`sphinxMystLiveview.preview.*` change calls `updatePreview(lastGood)`, regenerating the whole
HTML. Both should be pure `postMessage` + CSS-variable flips; nothing in the Sphinx output depends
on the VS Code theme.

---

## Tier 1 — Cut the Sphinx cost

### T1-1 — Preview-only Sphinx configuration

Add `sphinx/preview_conf.py` that imports `conf.py` and then **removes extensions irrelevant to an
HTML preview**: `sphinx_revealjs`, `sphinxcontrib.confluencebuilder`, `sphinx_tippy` (its JS is
stripped by the sanitizer anyway), and `sphinxcontrib.mermaid` once T2-4 lands. Point the build at
`-c sphinx` with `SPHINX_PREVIEW_MODE=1` selecting the slim path.

Also short-circuit the per-render `conf.py` side effects (reading `book/release.yml`,
`book/abstract.txt`, registering three pybtex plugins) when `SPHINX_PREVIEW_MODE=1` — the preview
does not render a title page.

**Measure before and after.** This is the cheapest large win before committing to a worker.

### T1-2 — Fix the `{only}` tag inversion  🐞

`sphinx/conf.py` reads `pdf_mode = os.environ.get("SPHINX_PDF_MODE", "book")` and then
unconditionally `tags.add("latex")` for `book`/`academic`. The preview never unsets it, so the
preview build carries **both** `html` and `latex` tags. Consequence: `{only} not latex` content is
**hidden** and `{only} latex` content is **shown** — the preview lies. The same branch appends
`16-glossary.md` to `exclude_patterns`, breaking every `{term}` reference.

Guard the branch with `if not os.environ.get("SPHINX_PREVIEW_MODE")`. Add a rendering test
asserting that `{only} html` content appears and `{only} latex` content does not.

### T1-3 — Persistent Sphinx worker

The single largest fixed cost is process spawn + interpreter start + importing a dozen Sphinx
extensions, paid in full on every render. Replace the per-render `spawn("uv", ["run", …])` with a
long-lived worker:

- `sphinx/preview_server.py`, launched once per preview as
  `uv run --no-sync -- python -m preview_server`, speaking **JSON lines over stdio**.
- Request: `{ id, sourcePath, documentId, sourceOrigins, stageRoot }`.
  Response: `{ id, html, diagnostics, durationMs }` or `{ id, error }`.
- The worker holds a warm `Sphinx` application bound to the reused stage root, so the environment,
  the parsed `refs.bib`, and all extension imports survive between renders. Per render it only
  re-reads the changed source and runs an incremental `app.build()`.
- **Lifecycle.** Spawn lazily on first build; kill in `disposePreview`; respawn on crash with
  exponential backoff; recreate the `Sphinx` app (not the process) when `conf.py` or `refs.bib`
  changes. Health-check with a `ping` request. Keep the existing one-shot `spawn` path as a
  fallback behind `sphinxMystLiveview.build.useWorker` (default `true`) so a worker regression
  cannot brick the extension.

**Prerequisite already satisfied:** the persistent staging root landed in the previous work item.

**Risk.** Sphinx's `Sphinx` object is not formally designed for unbounded repeated builds; memory
growth and env staleness are real. Mitigate with a rebuild counter (recycle the app every N
builds) and a memory watchdog.

### T1-4 — Incremental staging

`clearStagedSources()` wipes and `copyReferencedInput()` re-copies every referenced image and
include on every keystroke, and `collectReferences` runs four regexes over the buffer plus
recursively over every referenced Markdown file, with an `fs.realpathSync` per reference. Copy
only when the source `mtimeMs`/`size` differs from the staged copy, and memoize `realpathSync`
per render.

---

## Tier 2 — Rendering parity and polish

These are the features the user explicitly liked in Mark Sharp, plus the outright bugs that make
us weaker than a GFM-only tool.

### T2-1 — Math must actually typeset  🐞

Sphinx defaults to MathJax loaded from a CDN. `ResourcePolicy.resolveResource` rejects any
schemed URL, so the script is stripped as `blocked-script-resource` and the reader sees raw TeX:
`\(e^{i\pi}+1=0\)`.

Bundle **KaTeX locally**: vendor `katex.min.js`, `katex.min.css` and the KaTeX fonts into
`sphinx/_static/katex/`, set `html_math_renderer` accordingly (or `mathjax_path` to a staged local
MathJax bundle). Staged local assets already pass the resource policy and get a nonce; `font-src`
already allows `cspSource`. Prefer KaTeX over MathJax: smaller, synchronous, and it is what Mark
Sharp uses.

**Test gap to close.** The current rendering test only asserts a `span.math` element exists. Add
an assertion that a `.katex` element is produced — the existing test would pass today even though
math is visibly broken.

### T2-2 — Admonition rendering (called out by the user)

Current state: correct semantics, flat presentation — accent colours mapped to `--vscode-charts-*`
and nothing else. Bring `PREVIEW_THEME_CSS` in `src/preview/previewStyles.ts` up to Mark Sharp's
standard:

- **Icons.** One inline SVG per admonition type as a `background-image: url("data:image/svg+xml,…")`
  on `.admonition-title::before` — data URIs need no resource-policy exception and no extra
  request. Cover the MyST set: note, tip, hint, important, warning, caution, attention, danger,
  error, seealso, admonition (generic).
- **Left accent bar** (4 px) plus a low-alpha tinted background via `color-mix()` against the
  editor background, instead of a flat border box.
- **Tighter vertical rhythm**: title `margin-block: 0`, body `margin-block-start: .5rem`, no
  double margin on a leading paragraph.
- **Nested content**: code blocks and lists inside admonitions must inherit the tint, not stack
  a second background.
- **`sphinx-design` dropdowns / `togglebutton`**: style the `<details>` summary to match.

### T2-3 — Code block rendering (called out by the user)

- **Background alignment**: use `--vscode-textCodeBlock-background` so blocks match the stock
  preview and the editor, rather than the Shibuya theme colour.
- **Language badge**: a small right-aligned label derived from the `highlight-<lang>` class,
  rendered in CSS via an attribute selector — no HTML change needed.
- **Copy button**: `sphinx_copybutton` is loaded and its `_static` script *should* survive the
  sanitizer with a nonce. **Verify this end to end** — if the button is absent today, either
  re-enable it or drop the extension from the preview config (T1-1) and re-implement the button
  in the injected preview script, which is cheaper and themeable.
- **Caption**, **line numbers**, and **`:emphasize-lines:`** styling.
- **Horizontal overflow affordance**: `overflow-x: auto` with a subtle inset shadow, and
  `scrollbar-width: thin` so long lines do not silently clip.
- **Inline code**: match `--vscode-textPreformat-foreground`/`-background`.

### T2-4 — Mermaid client-side instead of `mmdc`

`sphinxcontrib.mermaid` with `mermaid_output_format = "png"` spawns the `mmdc` Node CLI **per
diagram, per build** — the single most expensive item in a diagram-heavy chapter, and it fails
outright when `mmdc` is not installed. In preview mode, emit the raw `<pre class="mermaid">`
source and render it in-page with a locally staged `mermaid.min.js` (nonced, theme-derived from
the VS Code colour theme, exactly as Mark Sharp does). Non-preview builds keep the PNG path.

### T2-5 — `{animation}` poster fallback  🐞

`src/sphinx_animation/__init__.py` emits `<figure><div id=…></div><script type="module">…` with a
root-absolute `/_static/...` import. Inline scripts are stripped and the absolute path would be
rejected anyway, so the preview shows an empty box with a caption. The companion PNGs already
exist in `book/animations/<name>-{light,dark}.png`. When `SPHINX_PREVIEW_MODE=1`, emit the poster
`<img>` (both variants, selected by `data-sphinx-preview-theme`) instead of the script.

### T2-6 — Cross-document references

Only the active buffer is staged as `index.md`, so `{ref}`/`{doc}`/`{term}` targets in other
chapters become `myst.xref_missing` warnings and render as plain text with diagnostic noise.
Two options, in order of cost:

- **Cheap**: classify `xref_missing` as *informational* in `parseDiagnostics` and style unresolved
  references with a muted dotted underline plus a tooltip, instead of surfacing a warning banner.
- **Better**: stage a lightweight stub document set — for each referenced label, a generated
  target-only file — so the reference resolves to a non-navigable anchor. Bounded work, and it
  makes citations and glossary terms behave.

### T2-7 — Outline via `DocumentSymbolProvider`

Mark Sharp ships a custom outline panel. We can get the same thing for free and better integrated
by contributing a `DocumentSymbolProvider` for Markdown headings — it populates the native VS Code
Outline view, breadcrumbs, and `Ctrl+Shift+O`, and it works in the text editor too, not just in
the preview. Note the stock Markdown extension already provides one; only add ours if MyST
headings inside directives are being missed.

### T2-8 — Reading mode, width and font controls

Cheap CSS-variable work with high perceived polish:

- `sphinxMystLiveview.display.documentWidth`: `"fullPage"` (default) | `"letter"` (centred,
  ~72 ch measure).
- `sphinxMystLiveview.display.fontSize` (6–100, default inherits the editor).
- `sphinxMystLiveview.display.fontFamily` (defaults to VS Code's).
- `sphinxMystLiveview.display.readingMode`: hides the status aside, disables click-to-reveal,
  widens the line height. Toggled by a command and a status-bar item.

All of these must be applied via `postMessage` + CSS custom properties — never a rebuild (T0-6).

---

## Out of scope for this document

- WYSIWYG / direct editing in the preview, slash commands, draggable blocks, table editing,
  drag-and-drop images. These are addressed separately in
  [02-wysiwyg-architecture.md](./02-wysiwyg-architecture.md).
- Note that two enablers already exist and should be preserved:
  `sphinxMystLiveview.preview.markEditorSelection` and `.doubleClickToSwitchToEditor`.

---

## Sequencing

| Milestone | Contents | Outcome |
|---|---|---|
| **M1 — Responsiveness** | T0-1, T0-2, T0-3, T0-4, T0-5, T0-6 | Zero flicker, scroll survives, no permanent hangs. Perceived latency becomes *only* the Sphinx build. |
| **M2 — Correctness** | T1-1, T1-2, T2-1, T2-5, T2-6 | Preview stops lying (`{only}`, math, animations, xrefs); build drops toward ~600 ms. |
| **M3 — Speed** | T1-3, T1-4, T2-4 | Sub-200 ms keystroke-to-paint; no `mmdc` spawns. |
| **M4 — Polish** | T2-2, T2-3, T2-7, T2-8 | Visual parity with Mark Sharp on admonitions and code. |

M1 is independently shippable and delivers most of the perceived improvement.

---

## Measurement plan

There is **no performance test today** — latency is only `console.log`'d in
`test/integration/dirtySnapshots.test.ts`. Before starting M1, add `test/performance/`:

- A fixture chapter representative of the book (admonitions, code, math, figures, citations).
- A harness recording p50/p95 for: stage, Sphinx spawn, Sphinx build, HTML post-process, webview
  apply — reported separately so a regression is attributable.
- Emit `perf-report.json` from `just vscode-sphinx-liveview-release-check` and fail the gate on a
  >20 % p95 regression against a committed baseline.

Without this, none of the Tier 1 claims are verifiable.

---

## Risk register

| Risk | Mitigation |
|---|---|
| DOM patching breaks scroll-sync mapping | Re-run `parseMappings()` + `stabilizeLayout()` inside `applyRender`; restore by source line, not pixel |
| Bundling KaTeX/Mermaid weakens the security posture | Local staged assets only, nonced, `connect-src 'none'` unchanged, no CDN, no `unsafe-inline` |
| Sphinx worker leaks memory or goes stale | Recycle the app every N builds, `ping` health check, crash respawn with backoff, one-shot fallback behind a setting |
| Preview-only `conf.py` diverges from the book build | Preview conf *imports* the book conf and subtracts; never a parallel copy. Rendering tests run against both |
| `{only}` fix changes what authors see | Intended — it is currently inverted. Add a regression test both ways |
| Shell reuse breaks on document switch | Rebuild the shell on `switchPreviewDocument`; keep the one-assignment invariant asserted in tests |
