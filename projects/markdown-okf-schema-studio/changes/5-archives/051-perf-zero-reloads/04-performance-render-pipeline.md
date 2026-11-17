# 04 — Performance: Render Pipeline on the Extension Host

Part of the [deep analysis review](00-index.md) of `src/markdown-okf-schema-studio`.
This file covers CPU spent turning a buffer into HTML on the extension host:
threading, redundant HTML passes, PlantUML processes, and missing memoisation.
Webview reloads are in [05](05-performance-webview-lifecycle.md); frontmatter and filesystem costs
are in [06](06-performance-frontmatter-and-filesystem.md). Lines refer to `e1b4ad0`.

## Baseline measurement

Chapter `book/chapters/08-research-plan-implement.md` (2,403 lines, 107 KB) is the largest
document in the repository. Average of ten renders, Node 25.4 on Apple Silicon (arm64), compiled
`out/src`; the extension host's Electron Node differs, so treat the numbers as relative:

| Stage | ms per render |
| --- | --- |
| `renderMyst` (parse, normalise, `mystToHtml`, table alignment, highlight.js) | 54.3 |
| `annotateSourceMappings` (parse5 fragment parse + serialize) | 5.9 |
| `rewriteSphinxHtml` (parse5 document parse + serialize) | 11.2 |
| `renderMathHtml` (parse5 document parse + serialize when math is present) | 0.2 |
| `injectContentSecurityPolicy` (parse5 parse + serialize of the full page) | 13.5 |
| **Total measured** | **85.1** |

The resulting page is 488 KB, of which 102 KB is inline script and 51 KB inline CSS.
The measurement excludes three `analyzeFrontmatter` passes, `setPreviewStatus` regex passes,
PlantUML collection and injection, and `replacePropertiesTableMarkup`, which all run on the same
thread for the same keystroke. All of it is synchronous.

To reproduce, run `npm run compile` in `src/markdown-okf-schema-studio`, then time `renderMyst`,
`annotateSourceMappings`, `rewriteSphinxHtml`, `renderMathHtml`, and `injectContentSecurityPolicy`
from `out/src/**` on the chapter above.

## Findings

### PERF-01 — The whole render runs on the extension host main thread

- **Severity**: High
- **Confidence**: Confirmed by measurement
- **Effort**: L
- **Location**:
  [renderPipeline.ts:133-236](../../../../src/render/renderPipeline.ts#L133),
  [mystRenderer.ts:1220-1257](../../../../src/render/mystRenderer.ts#L1220),
  [extension.ts:1949-1963](../../../../src/extension.ts#L1949)

**What happens.**
`renderPreviewDocument` is `async`, but after the first `loadEngine()` it never yields: parsing,
normalisation, HTML generation, highlighting, sanitising, and include I/O run in one synchronous
block. With a 40 ms debounce, a sustained typing session on chapter 08 blocks the shared extension
host for roughly 100 ms per render. Every other extension (language servers' clients, Copilot, Git)
stalls for that duration, and VS Code may flag the host as unresponsive on larger files. The
`AbortSignal` is only checked after the work is done, so a superseded render cannot be stopped.

**Fix.**
Move `renderMyst` and the HTML post-processing into a `worker_threads` worker bundled by esbuild
(`out/bundle/renderWorker.js`). The worker receives `{ text, sourcePath, roots, budget }` and
returns `{ html, diagnostics, dependencies }`; include reads happen in the worker with
`fs.promises`. Terminate and respawn the worker to cancel a superseded render, or check a shared
`Int32Array` cancellation flag between pipeline stages. Keep a single worker per window. Make the
debounce adaptive: `max(40 ms, 1.5 × last render duration)`, capped at 400 ms.

**Tests to add.**
Unit test with a fake worker asserting that a superseded request is cancelled and that the queue
publishes only the latest result. Integration benchmark: typing 50 characters into chapter 08 keeps
the extension-host event-loop delay p95 under 50 ms (`perf_hooks.monitorEventLoopDelay`).

**Done when.**
No render stage runs on the extension host thread, and event-loop delay stays bounded while typing.

### PERF-02 — The HTML is parsed and serialised six or more times per render

- **Severity**: Medium
- **Confidence**: Confirmed by code reading and measurement
- **Effort**: M
- **Location**:
  [mystRenderer.ts:793-848](../../../../src/render/mystRenderer.ts#L793),
  [sourceMapping.ts:80-107](../../../../src/mapping/sourceMapping.ts#L80),
  [html-sanitizer.ts:354-405](../../../../src/security/html-sanitizer.ts#L354),
  [mathRenderer.ts:16-95](../../../../src/render/mathRenderer.ts#L16),
  [plantUmlRenderer.ts:245-355](../../../../src/render/plantUmlRenderer.ts#L245),
  [propertiesTable.ts:256-293](../../../../src/frontmatter/propertiesTable.ts#L256),
  [webview.ts:174-286](../../../../src/preview/webview.ts#L174)

**What happens.**
Each stage takes a string and returns a string: `applyTableAlignments`, `highlightCodeBlocks`
(regex), `annotateSourceMappings`, `rewriteSphinxHtml`, `renderMathHtml`,
`injectContentSecurityPolicy`, then later `collectSources` (PlantUML), `injectPlantUmlDiagrams`, and
`replacePropertiesTableMarkup` (with `sourceCodeLocationInfo`). The last three parse the *full
page*, including the 102 KB script and 51 KB of CSS that never change. `injectSourceMappings` in the
sanitizer repeats what `annotateSourceMappings` already did.

**Fix.**
Build one HAST tree: call `mystToHast` (exported by `myst-to-html`) instead of `mystToHtml`, apply
table alignment, source mapping, sanitisation, highlighting, math, and PlantUML placeholders as tree
transforms, and stringify once with `hast-util-to-html`. Assemble the page shell (toolbar, CSP meta,
script and style tags) with a fixed string template around the content, never by re-parsing it.
Keep the properties table as a separate fragment with stable markers so it can be swapped without a
parse (see [PERF-14](06-performance-frontmatter-and-filesystem.md#perf-14--frontmatter-is-analysed-three-times-per-edit)).

**Done when.**
One render performs at most one HTML stringification and zero parses of its own output.

### PERF-03 — PlantUML spawns one JVM per diagram on every render

- **Severity**: High (for documents with diagrams)
- **Confidence**: Confirmed by code reading
- **Effort**: M
- **Location**:
  [plantUmlRenderer.ts:285-298](../../../../src/render/plantUmlRenderer.ts#L285),
  [extension.ts:646-675](../../../../src/extension.ts#L646),
  [renderPipeline.ts:195-211](../../../../src/render/renderPipeline.ts#L195)

**What happens.**
After every successful render, `scheduleDeferredPreviewWork` calls `resolvePlantUml`, which spawns
`java -jar plantuml.jar -pipe` once per diagram, all concurrently through `Promise.all`.
Nothing is cached, so an unchanged diagram is re-rendered on every keystroke anywhere in the
document. A JVM start costs roughly 0.5–2 s of CPU and 150–300 MB of memory; ten diagrams mean ten
concurrent JVMs per render. The previous render's processes are only killed when its stage is
disposed, so sustained typing keeps a rolling set of JVMs alive. There is no timeout.

**Fix.**

1. Cache SVG results by `sha256(source + jarPath + themeKind)` in an LRU (for example 200 entries);
   only uncached diagrams reach the process pool.
2. Limit concurrency to one or two processes, queued per preview, cancelled per render.
3. Use PlantUML's batch mode (`-pipe -pipedelimitor`) to render all uncached diagrams in one JVM,
   or keep one long-lived PlantUML process (`-pipe` loop or `-picoweb` bound to `127.0.0.1`).
4. Enforce a timeout (for example 15 s) and kill the process group (`detached: true` +
   `process.kill(-pid)`), because the Homebrew `plantuml` wrapper may not forward `SIGTERM`.

**Tests to add.**
Spawner-hook unit tests: two renders with an unchanged diagram spawn once; eight diagrams never
exceed the configured concurrency; a hung fake process is killed at the timeout.

**Done when.**
Typing in a document with N unchanged diagrams spawns zero processes.

### PERF-04 — Code highlighting and math are recomputed for every block on every render

- **Severity**: Low (Medium for code- or math-heavy chapters)
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [highlight.ts:231-294](../../../../src/render/highlight.ts#L231),
  [mathRenderer.ts:40-71](../../../../src/render/mathRenderer.ts#L40)

**What happens.**
highlight.js and KaTeX are deterministic per input, but each keystroke re-highlights every code
block and re-typesets every equation of the document.

**Fix.**
Memoise `hljs.highlight` by `(language, code)` and `katex.renderToString` by `(tex, displayMode)` in
bounded LRU maps (for example 500 entries each). With PERF-02, the cache can sit inside the HAST
transforms.

**Done when.**
A keystroke outside a code block or equation triggers no highlight.js or KaTeX work for it.

## Related findings

- Include fan-out is both a performance and a denial-of-service issue:
  [SEC-05](02-security-webview-and-content.md#sec-05--include-expansion-has-no-global-budget-exponential-fan-out).
- Synchronous filesystem calls on the same thread:
  [PERF-16](06-performance-frontmatter-and-filesystem.md#perf-16--recursive-file-watchers-and-per-event-realpath-calls),
  [PERF-17](06-performance-frontmatter-and-filesystem.md#perf-17--per-keystroke-synchronous-filesystem-calls).
