# 08 — Remediation Plan

Part of the [deep analysis review](00-index.md) of `src/markdown-okf-schema-studio`.
This file orders the findings of rubrics 01–07 into deliverable increments, with dependencies,
the tests that prove each increment, and the metrics that tell whether the work paid off.
Each increment is sized to be one merge request.
SUP-01 is excluded (owner decision, 2026-10-09). The executable, task-level version of this plan is
[plan.md](plan.md).

## Ordering principles

1. Stop data loss and code-execution paths before optimising anything.
2. Fix the two leaks that degrade a session over time (Ajv memory, edit lock) early, because they
   make every later benchmark noisy.
3. Remove webview reloads before moving work to a worker: reloads dominate perceived latency, and
   the worker design is simpler once content is delivered by message.
4. Land documentation and packaging changes with the code they describe.

## Increment 1 — Hotfixes (about 1–2 days)

| Finding | Change |
| --- | --- |
| [STAB-01](07-stability-and-correctness.md#stab-01--frontmatter-fence-detection-truncates-the-block-and-table-edits-corrupt-the-file) | One shared fence regex; patch re-parse guard |
| [PERF-12](06-performance-frontmatter-and-filesystem.md#perf-12--the-ajv-validator-cache-never-hits-and-every-compile-is-retained-memory-leak) | Stable resolved-schema identity; validator cache keyed on it |
| [SEC-01](01-security-process-execution-and-trust.md#sec-01--plantuml-runs-with-full-file-and-network-access-on-any-previewed-document) | `SANDBOX` profile, minimal `env`, temporary `cwd`, no PlantUML in standalone mode |
| [SEC-02](01-security-process-execution-and-trust.md#sec-02--plantumljarpath-is-workspace-overridable-and-resolved-against-the-workspace) | `scope: machine`, absolute-only `jarPath`, explicit `PATH` resolution |
| [STAB-04](07-stability-and-correctness.md#stab-04--plantuml-child-process-handling-is-fragile) | `stdin` error handler, buffered UTF-8 decode, timeout, process-group kill |
| [STAB-02](07-stability-and-correctness.md#stab-02--the-inline-edit-lock-survives-a-webview-reload) | Release stale locks on `previewReady` |
| [PERF-06](05-performance-webview-lifecycle.md#perf-06--saving-the-active-document-triggers-a-redundant-full-render) | Skip save-triggered renders of an unchanged buffer |

**Exit criteria.**
The STAB-01 fixtures pass; 1,000 analyses keep Ajv `_cache.size` constant; PlantUML spawns carry the
sandbox profile and never inherit `process.env`; the early-exit spawner test raises no uncaught
exception; saving an unchanged buffer performs no render.

## Increment 2 — Bounded work per edit (about 1 week)

| Finding | Change |
| --- | --- |
| [SEC-05](02-security-webview-and-content.md#sec-05--include-expansion-has-no-global-budget-exponential-fan-out) | Include budget (count, bytes) and per-render memoisation |
| [PERF-03](04-performance-render-pipeline.md#perf-03--plantuml-spawns-one-jvm-per-diagram-on-every-render) | SVG cache by source hash, concurrency cap, batch or long-lived process |
| [PERF-15](06-performance-frontmatter-and-filesystem.md#perf-15--any-markdown-save-invalidates-the-stem-index-and-forces-a-synchronous-rebuild) | Invalidate on create/delete/rename only; incremental updates |
| [PERF-13](06-performance-frontmatter-and-filesystem.md#perf-13--schema-discovery-and-parsing-are-not-cached), [PERF-14](06-performance-frontmatter-and-filesystem.md#perf-14--frontmatter-is-analysed-three-times-per-edit) | `SchemaRegistry` with watcher invalidation; one analysis per version |
| [PERF-09](05-performance-webview-lifecycle.md#perf-09--link-discovery-is-repeated-on-every-reload-and-runs-uncached-findfiles) | Wikilinks via the stem index; host-side result cache |
| [SEC-09](02-security-webview-and-content.md#sec-09--unbounded-synchronous-file-reads-driven-by-content), [SEC-10](02-security-webview-and-content.md#sec-10--host-message-handling-missing-size-caps-and-an-unguarded-openexternal) | Read caps; message size caps; guarded `openExternal` |
| [STAB-07](07-stability-and-correctness.md#stab-07--github-alerts-are-not-recognised-in-crlf-documents), [STAB-08](07-stability-and-correctness.md#stab-08--inherited-object-keys-are-treated-as-frontmatter-fields) | CRLF-safe line helpers; `Object.hasOwn` |

**Exit criteria.**
The depth-5 include fixture renders in under 1 s with a budget diagnostic; typing in a document with
unchanged diagrams spawns no process; saving a Markdown file performs no directory walk; one edit
performs at most one link resolution.

## Increment 3 — Zero reloads per keystroke (about 1–2 weeks)

| Finding | Change |
| --- | --- |
| [PERF-05](05-performance-webview-lifecycle.md#perf-05--each-keystroke-replaces-the-webview-document-three-to-six-times) step 1 | Status updates by `postMessage` |
| [PERF-11](05-performance-webview-lifecycle.md#perf-11--the-runtime-script-and-css-are-inlined-in-every-page) | Runtime as bundled `preview.js` / `preview.css` files |
| PERF-05 step 2 | Content and properties table by `postMessage` with keyed DOM morph |
| [STAB-03](07-stability-and-correctness.md#stab-03--any-reload-destroys-an-open-inline-editor), [STAB-06](07-stability-and-correctness.md#stab-06--inline-block-edits-rely-on-absolute-offsets-and-can-be-dropped-silently) | No reload during edits; range tracking; explicit stale-edit errors |
| [PERF-07](05-performance-webview-lifecycle.md#perf-07--the-5-mb-mermaid-bundle-is-reloaded-and-every-diagram-re-rendered-on-each-reload), [PERF-08](05-performance-webview-lifecycle.md#perf-08--scrolling-forces-synchronous-layout-several-times-per-frame) | Lazy cached Mermaid; geometry-free scroll frames; throttled state |
| [PERF-10](05-performance-webview-lifecycle.md#perf-10--retaincontextwhenhidden-keeps-every-hidden-preview-alive), [STAB-05](07-stability-and-correctness.md#stab-05--restoring-a-serialised-panel-orphans-the-previous-side-preview) | Drop `retainContextWhenHidden` for the custom editor; fix panel restore |

**Exit criteria.**
Typing ten characters performs zero `webview.html` assignments after the first render; an open
inline editor survives save, theme change, and diagram completion; a scroll frame on chapter 08
stays under 4 ms of script time.

## Increment 4 — Off-thread rendering and a single HTML pass (about 2 weeks)

| Finding | Change |
| --- | --- |
| [PERF-01](04-performance-render-pipeline.md#perf-01--the-whole-render-runs-on-the-extension-host-main-thread) | `worker_threads` render with cancellation and adaptive debounce |
| [PERF-02](04-performance-render-pipeline.md#perf-02--the-html-is-parsed-and-serialised-six-or-more-times-per-render) | HAST pipeline from `mystToHast`; one stringification |
| [PERF-04](04-performance-render-pipeline.md#perf-04--code-highlighting-and-math-are-recomputed-for-every-block-on-every-render) | Highlight and KaTeX memoisation inside the HAST transforms |
| [SEC-06](02-security-webview-and-content.md#sec-06--script-and-stylesheet-policy-relies-on-a-single-layer) | Nonce-only `script-src`; allowlist sanitizer as a HAST transform |
| [SEC-08](02-security-webview-and-content.md#sec-08--schema-supplied-regular-expressions-can-hang-the-extension-host) | Linear-time regex engine or time-boxed validation in the worker |
| [SEC-12](02-security-webview-and-content.md#sec-12--generated-css-is-not-escaped) | Escaped generated CSS |
| [PERF-16](06-performance-frontmatter-and-filesystem.md#perf-16--recursive-file-watchers-and-per-event-realpath-calls), [PERF-17](06-performance-frontmatter-and-filesystem.md#perf-17--per-keystroke-synchronous-filesystem-calls), [SEC-07](02-security-webview-and-content.md#sec-07--broad-resource-roots-and-recursive-watching-in-standalone-mode) | Dependency-scoped watchers; cached canonical roots; narrow standalone roots |

**Exit criteria.**
Extension-host event-loop delay p95 stays under 50 ms while typing in chapter 08; the page HTML is
stringified once per render; a resolvable `<script src>` in content never reaches the page.

## Increment 5 — Trust model, supply chain, and documentation (about 3–4 days, parallelisable)

| Finding | Change |
| --- | --- |
| [SEC-03](01-security-process-execution-and-trust.md#sec-03--the-manifest-does-not-declare-a-workspace-trust-capability), [SEC-04](01-security-process-execution-and-trust.md#sec-04--link-containment-settings-can-be-weakened-by-the-repository-itself) | `untrustedWorkspaces: limited` with `restrictedConfigurations`; scoped settings |
| [SUP-02](03-security-supply-chain-and-packaging.md#sup-02--the-release-gate-does-not-scan-for-known-vulnerabilities) | Vulnerability scan and SBOM in the release gate |
| [SUP-03](03-security-supply-chain-and-packaging.md#sup-03--the-vsix-ships-files-that-are-not-part-of-the-runtime) | Allowlist `.vscodeignore`; VSIX content assertion |
| [SUP-04](03-security-supply-chain-and-packaging.md#sup-04--dead-sphinx-pipeline-code-and-stale-security-evidence), [SUP-05](03-security-supply-chain-and-packaging.md#sup-05--runtime-deprecation-warning-from-a-dependency) | Remove dead Sphinx modules; rewrite security evidence, limitations, AGENTS.md section |
| [SEC-11](02-security-webview-and-content.md#sec-11--absolute-filesystem-paths-are-exposed-in-the-preview), [STAB-09](07-stability-and-correctness.md#stab-09--per-document-state-grows-without-bound) | Relative paths in titles and diagnostics; bounded state |

**Exit criteria.**
The extension runs read-only in Restricted Mode with PlantUML disabled; the release gate fails on a
high-severity runtime advisory and on unexpected VSIX content; every claim in
`docs/security-evidence.md` maps to a test of the shipped code path.

## Tracking metrics

Record these before Increment 1 and after each increment, on chapter 08 and on a synthetic document
with ten PlantUML and ten Mermaid diagrams.

| Metric | Baseline (`e1b4ad0`) | Target |
| --- | --- | --- |
| `webview.html` assignments per keystroke | 3 to 6 | 0 |
| Main-thread render time per keystroke (chapter 08) | about 85 ms measured, more with frontmatter passes | 0 ms (worker) |
| Extension-host event-loop delay p95 while typing | not measured | under 50 ms |
| Heap growth per 1,000 frontmatter analyses | about 27 MB | under 1 MB |
| PlantUML processes per keystroke with unchanged diagrams | one per diagram | 0 |
| Filesystem directory walks per Markdown save | one full workspace walk when stems are used | 0 |
| Include reads for the depth-5 fan-out fixture | 111,110 | at most the budget (for example 200) |
