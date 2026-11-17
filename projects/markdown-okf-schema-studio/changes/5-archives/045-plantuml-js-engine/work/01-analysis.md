# PlantUML JavaScript renderer instead of plantuml.jar — analysis

Date: 2026-10-21. Status: research only, no code changed.
Question: replace the `plantuml.jar` (Java) pipeline by the official JavaScript PlantUML, keeping
the jar as a configurable fallback?

## 1. Recommendation (short)

**Yes, it makes sense, as option (b): JS engine by default, jar kept as opt-in fallback.**
The official engine now exists, is published by the PlantUML project itself, and since
1.2026.6 it is MIT-licensed, which is compatible with this extension (MIT). It removes the
Java requirement, the child process, and most of the open security and performance findings
(SEC-01, SEC-02, STAB-04, PERF-03). The cost is a real architecture change: the engine needs a
DOM, so it must run in the **webview**, not in the extension host (verified, see 3.4), and the
render result flow (today host-side HTML injection) has to be reversed. Do it as a
`plantuml.renderer` setting with `auto` as default.

Do not go "JS only" (c) now: the package is five months old (first npm release 2026-05-22),
fidelity against Graphviz-based layouts is unproven for this project, and users with a
corporate jar (custom `!include`, DITAA, GPL-only features) need the escape hatch.

## 2. Current pipeline in the repo

| Aspect | Today |
|---|---|
| Detection | `src/render/mystRenderer.ts` (l.512, 974) turns `plantuml` fences / `{plantuml}` directives into `<... class="myst-plantuml-diagram">` placeholders. |
| Renderer | `src/render/plantUmlRenderer.ts` (409 lines), extension host (Node). `renderPlantUmlDiagrams(html, opts)` parses HTML with parse5, collects sources, spawns one process per diagram via `Promise.all`. |
| Config | One setting `markdownOkfSchemaStudio.plantuml.jarPath` (`package.json` l.167, string, default `""`, not scoped `machine`). Read by `src/configuration/plantUmlConfiguration.ts`. Empty = `plantuml` command on PATH; set = `java -jar <jarPath> -pipe -tsvg`. Relative paths resolve against the workspace root. |
| Java lookup | Bare `java` / `plantuml` names resolved by `child_process.spawn` with `cwd = workspaceRoot` (no explicit PATH scan, no JAVA_HOME). |
| Spawn | `stdio: pipe`, `detached` on POSIX, source written to stdin, SVG read from stdout (sliced from first `<svg` to last `</svg>`). Limits: 1 MiB source, 8 MiB output, 64 KiB stderr, 30 s timeout (`PLANTUML_TIMEOUT_MS`), AbortSignal cancel, process-group kill (`kill(-pid)`), stdin `error` handler for EPIPE, settle-once guard. |
| Cache | None. Re-spawned on every render (PERF-03). |
| Trust | `trusted === false` returns "PlantUML preview is disabled in an untrusted workspace". |
| Wiring | `renderPipeline.ts` l.195-212 lazily builds `resolvePlantUml()`; `extension.ts` l.1153-1173 (`applyPlantUml`) calls `injectPlantUmlDiagrams` on the panel HTML and re-sets it, deferred while editing. SVG is embedded as `<img src="data:image/svg+xml;...">` (so SVG scripts never run). |
| CSP | `src/security/csp.ts`: `default-src 'none'`, `img-src cspSource data:`, `script-src cspSource 'nonce-..'`, `connect-src 'none'`, `worker-src 'none'`. No `wasm-unsafe-eval`. |
| Packaging | Jar is **not** shipped; user must provide Java + jar or `plantuml` on PATH. Mermaid is already bundled into the webview as `out/bundle/mermaidPreview.js` (5.0 MB, esbuild IIFE, `esbuild.mjs`), which is a direct precedent for bundling a browser engine. |
| Tests | `test/rendering/plantUmlRenderer.test.ts` (fake spawner: JAR vs PATH, ENOENT, malformed output, cancel, EPIPE, stdin error, multibyte chunking, stderr cap, timeout, process-group kill, settle-once), `test/configuration/plantUmlConfiguration.test.ts`, `test/security/package-contract.test.ts`, `test/webview/contentPatch.test.ts`, `test/state/editLock.test.ts`, `test/rendering/mystFeatures.test.ts`, visual fixtures `12-plantuml-optional.md`, `13-plantuml-executable-not-found.md`. |
| Known issues | Backlog `.agents/changes/backlog/P3/deep-analysis-review/`: SEC-01 (no `PLANTUML_SECURITY_PROFILE=SANDBOX`, includes can read local files / fetch URLs), SEC-02 (`jarPath` workspace-overridable, bare-name PATH/cwd hijack), STAB-04 (process handling; partly fixed in code already: EPIPE, timeout, group kill), PERF-03 (one JVM per diagram per render, 0.5-2 s CPU and 150-300 MB each, no cache). Plan decisions D1-D4 in `plan.md`. |

A JS engine would make SEC-01 (file read through `!include`/`%getenv` etc. is only possible if the
host chooses to serve files), SEC-02, the PATH/cwd hijack, and the JVM cost disappear for the
default path. They stay relevant for the jar fallback.

## 3. The official JavaScript implementation

### 3.1 What it is
- PlantUML's own engine compiled to JavaScript with **TeaVM**, published on npm as
  **`@plantuml/core`**. Announced by the project on 2026-05-26 ("the engine runs entirely in the
  browser and can be imported straight from a CDN, with no server and no Java").
  Source: https://plantuml.com/news ; package README
  https://cdn.jsdelivr.net/npm/@plantuml/core@1.2026.9/README.md ;
  tracking issue https://github.com/plantuml/plantuml/issues/2715 (closed 2026-05-22).
- Not the old third-party projects (the unscoped `plantuml` npm name belongs to someone else, per
  issue #2715; older `plantuml-wasm`/CheerpJ-style ports are unrelated).
- Versions: 1.2026.5 (2026-05-22) ... 1.2026.9 (2026-10-17, latest at time of writing).
  Source: https://registry.npmjs.org/@plantuml/core . Release notes:
  https://plantuml.com/en/changes (1.2026.4 OpenIconic, 1.2026.6 `%load_json`, 1.2026.8
  "fall back to Smetana when viz-global.js is not loaded", 1.2026.9 "render by attempts, without
  worker thread nor coroutine").
- API (two functions, ES2015 module): `render(lines, targetId, opts)` writes into a DOM element
  asynchronously (only the latest pending call is kept); `renderToString(lines, onSuccess,
  onError, opts)` returns the SVG string, calls are queued independently. Options: `dark`,
  `maxSvgSize` (default 8192 px, error above it). `lines` is `string[]`. Source:
  https://cdn.jsdelivr.net/npm/@plantuml/core@1.2026.9/GITHUB_INTEGRATION.md

### 3.2 Licence
- `@plantuml/core` **>= 1.2026.6 is MIT**; earlier versions (1.2026.5) are GPL-3.0-or-later.
  Source: README above; npm registry reports `license: MIT` for 1.2026.9; changes page: "enable
  TeaVM JS build for the MIT license flavor (#2741)" (1.2026.6, 2026-06-08).
- This repo is MIT (`LICENSE`, `package.json` `"license": "MIT"`), so bundling >= 1.2026.6 is
  compatible. Never pin 1.2026.5 or lower (GPL would contaminate the VSIX).
- The jar is GPL by default; PlantUML also ships LGPL/Apache/EPL/MIT jars that "miss few
  features (DITAA for example)" (https://plantuml.com/faq). We do not ship the jar, so no
  licence impact for the fallback.
- Must ship the package `LICENSE` file in the VSIX (as is already done for KaTeX).

### 3.3 Size and files (1.2026.9, jsDelivr / unpacked, measured)
| File | Size |
|---|---|
| `plantuml.js` (engine, ES module) | 3.36 MB |
| `viz-global.js` (Graphviz/Viz.js, contains wasm) | 1.45 MB |
| `themes.js` | 0.33 MB (optional) |
| `emoji.js` | 1.88 MB (optional) |
| `openiconic.js` | 0.05 MB (optional) |
Whole npm package unpacked: about 7.2 MB (registry, 1.2026.9). Minimum useful bundle:
~3.4 MB (+1.4 MB with Graphviz), comparable to the 5 MB mermaid bundle already shipped.
Sprite libraries (AWS, IBM, tupadr3...) are **not** bundled (README). Stdlib includes
(`!include <C4/...>`) lazy-load bundles from a configurable base URL
(`window.PLANTUML_STDLIB_BASE`, default points at plantuml.github.io), i.e. **network** unless we
host the bundles ourselves (their size is unverified).

### 3.4 Runtime requirements (partly verified experimentally)
- Designed for browsers; uses `window`/`document`. I tested `@plantuml/core@1.2026.9` in
  Node (`import()` works in 150 ms, exports `render`, `renderToString`) but every render failed
  with `ReferenceError: window is not defined`, then `document is not defined` even with
  `globalThis.window = globalThis`. **Conclusion: not usable in the extension host without a DOM
  shim** (a worker_thread + jsdom-like shim is conceivable but unverified and fragile; the
  official `plantuml-mcp-js` Node server exists per the changes page, but I did not inspect how
  it works: unverified).
- Graphviz: `viz-global.js` defines a global `Viz` (wasm via `WebAssembly.instantiate`). Without
  it, since 1.2026.8 the engine **falls back to Smetana** (PlantUML's own Java port of Graphviz
  layout, compiled in) and logs "viz-global.js is not loaded, falling back to the Smetana layout
  engine" (observed). A bundler can inject it with `globalThis.PLANTUML_VIZ = Viz`.
  Source: GITHUB_INTEGRATION.md "Graphviz When Bundled". The PlantUML-for-GitHub extension ships
  Smetana only, no wasm (https://github.com/plantuml/plantuml-for-github).
- CSP implications (static grep of both files): neither file contains `eval(`, `new Function`,
  `new Worker`, `importScripts`, `createObjectURL` or `new Blob`. The only wasm use is
  `WebAssembly.instantiate` in `viz-global.js`. So:
  - Smetana-only mode: **no CSP change** besides loading the script (already allowed by
    `script-src cspSource 'nonce-..'`). `worker-src 'none'` can stay (1.2026.9 removed the
    internal worker: "without worker thread nor coroutine").
  - With Graphviz: add `'wasm-unsafe-eval'` to `script-src`. Needs a runtime test in a real VS
    Code webview: unverified.
  - `connect-src 'none'` blocks stdlib / URL includes by design: good for privacy, but those
    diagrams then need the jar or a host-side loader.
- Local `!include`: the engine has no file system; the host must supply a loader callback
  (documented in GITHUB_INTEGRATION.md, "local include" section, async loader, 60 s timeout). This
  is a clean place to enforce our existing `createPreviewResourcePolicy` (workspace-bounded,
  5 MiB cap) instead of giving the renderer free file access (fixes SEC-01 by construction).
- Performance: not benchmarked by me. Rendering in-process removes the 0.5-2 s JVM start per
  diagram; first-call engine init cost in a webview is unverified (engine module load in Node was
  150 ms). Main-thread blocking on big diagrams is the main risk; the doc suggests a Web Worker
  or iframe per diagram for that. `maxSvgSize` gives a built-in guard.

### 3.5 Feature coverage vs the jar
Documented/observed: sequence and other diagrams (all non-Graphviz ones), dark mode option,
`%load_json`, OpenIconic, emoji and themes via optional scripts, stdlib via lazy bundles.
Not verified (no authoritative compatibility matrix found; the project docs list none):
class/component/deployment/state/activity layout fidelity with Smetana vs Graphviz `dot`; fonts
(browser fonts vs Java AWT metrics, so text widths and wrapping can differ from the jar output);
DITAA, `!pragma graphviz_dot`, `-DSVG` specifics, skinparam edge cases, `!include` of arbitrary
URLs. Treat "visual parity with the jar" as unproven until a fixture comparison is done (see
tests). Known third-party report that Graphviz-based diagram types need `viz-global.js` wasm for
best layout: https://github.com/plantuml/plantuml-for-github (Smetana described as the compiled-in
alternative).

### 3.6 Maturity
Young (about 5 months, 5 releases, active: 1.2026.9 four days before this analysis), published and
maintained by the PlantUML core team, MIT, with CDN pinning recommended by the maintainer (issue
#2715). The API surface is tiny and stable-looking, but the engine is still changing
(worker model removed in 1.2026.9, Smetana fallback added in 1.2026.8): pin an exact version.

## 4. Options compared

| | (a) Jar only (today) | (b) JS default + jar fallback | (c) JS only | (d) Server / Kroki |
|---|---|---|---|---|
| Setup friction | Java + jar needed; works out of the box for no-one | Zero for most users; jar only for edge cases | Zero | Zero, but needs a server |
| Fidelity | Reference (Graphviz `dot`, AWT fonts) | Same as jar when falling back; JS may differ in layout/fonts | JS only; gaps unfixable by user | Reference if server runs real PlantUML |
| Security | Child process, full FS/network (SEC-01/02) | Default path has no process, includes under our policy; fallback keeps today's risk (mitigate with D1-D4) | Best: no process, no Workspace Trust dependency for rendering | Source diagrams leave the machine (privacy, corporate policy); SSRF/availability |
| Workspace trust | Required (spawns) | JS path can run in Restricted Mode (no spawn); jar path only when trusted | Same as JS | Not related, but network egress |
| VSIX size | +0 | +3.4 to 4.8 MB | same | +0 |
| Maintenance | Nothing to bundle, but support burden on Java/PATH | Bump pinned `@plantuml/core` regularly; keep process code | Bump only | Server ops |
| Test impact | Existing | New engine tests + keep spawner tests | Spawner tests deleted | Network mocks |
| Risks | UX, security backlog, perf | Two code paths, layout differences, webview refactor | Missing features, no escape hatch | Privacy, offline, availability |

Kroki or the public PlantUML server (d) is not recommended as default for this extension: diagram
text (often internal architecture) would be sent to a third party, and `connect-src 'none'` is
a deliberate property of the webview. If ever added it must be explicit opt-in with a
self-hosted URL.

## 5. Migration sketch for (b)

### 5.1 Where the engine runs
**In the webview**, bundled like Mermaid: new esbuild entry
`src/webview/plantumlPreview.ts` -> `out/bundle/plantumlPreview.js` (IIFE, browser), importing
`@plantuml/core` (`render`/`renderToString`). Reasons: needs DOM (verified), mermaid precedent,
CSP already has script-src for bundle files, no extra process.
Flow change: instead of host-side `renderPlantUmlDiagrams` + `injectPlantUmlDiagrams`, the host
emits the placeholder with the source (already there: text of `.myst-plantuml-diagram`) and a
"renderer" mode flag; the webview script finds placeholders, calls `renderToString` one at a
time (serialized, cached), converts the SVG to `<img src="data:image/svg+xml,...">` (same safe
embedding as today, so SVG scripts stay inert), and reports errors back through a message so the
host adds a `plantuml-render` diagnostic. The content-patch mechanism (`contentPatch.test.ts`,
edit lock, `deferWhileEditing`) must preserve already rendered diagram nodes between patches
(cache keyed by source hash + dark flag + engine version), otherwise diagrams flicker on each
keystroke; this is the largest piece of work.

Alternative if the webview flow is too invasive: keep host-side injection and call out to a
hidden webview/`WebviewPanel`-less renderer: rejected (more moving parts, no Node DOM).

### 5.2 Settings
```
markdownOkfSchemaStudio.plantuml.renderer: "auto" | "javascript" | "jar"   (default "auto")
markdownOkfSchemaStudio.plantuml.jarPath:  existing (make scope "machine", absolute only: D3)
markdownOkfSchemaStudio.plantuml.javaPath: optional, machine scope (replaces bare `java`)
markdownOkfSchemaStudio.plantuml.graphviz: "smetana" | "viz"   (default "smetana" until wasm CSP is validated)
```
- `auto`: JS first; if the engine reports an unsupported/failed diagram **and** a jar/`plantuml`
  is configured and the workspace is trusted, re-render that diagram with the jar; otherwise show
  the JS error with a hint ("set plantuml.renderer to jar and configure jarPath").
- `javascript`: never spawn. `jar`: today's behaviour (also the right choice for byte-exact
  output with corporate skinparams/includes).
- Keep the empty-`jarPath` => `plantuml` on PATH behaviour only for `jar` mode; in `auto` an
  empty `jarPath` means "no fallback available". Do not silently probe PATH (hijack risk, SEC-02).
- Back-compat: users with `jarPath` already set and no `renderer` set: decide (open question 2).

### 5.3 Unsupported diagrams
Classify errors from `onError`: syntax errors are real errors (show them, do not fall back, the
jar would fail too); "cannot include", stdlib/URL fetch blocked, `maxSvgSize` exceeded, and
engine exceptions are fallback candidates. Fallback runs through the existing host renderer
(`plantUmlRenderer.ts`, unchanged) via a message round trip webview -> host -> webview. Without a
configured jar, show a clear placeholder (reuse `myst-plantuml-error`, `data-render-state`).

### 5.4 Includes, stdlib, themes
- Local `!include`: implement the loader with the existing resource policy (workspace/document
  bounded, 5 MiB cap), host-served via messages. Default off if it is more than S effort; then
  `auto` falls back to the jar for diagrams with local includes.
- Stdlib/URL includes and `!theme` from library: blocked by `connect-src 'none'`. Either fall
  back to jar, or later bundle selected stdlib bundles locally and set `PLANTUML_STDLIB_BASE` to a
  webview URI. Do not open `connect-src` to plantuml.github.io by default (offline + privacy).
- Dark mode: pass `{ dark }` from the preview theme (needs re-render on theme change; include
  `dark` in the cache key).

### 5.5 Caching
LRU keyed by `sha256(source + dark + engineVersion + graphviz mode)`, in the webview (and host
cache for the jar path, which also resolves PERF-03). Limit concurrency to 1 for JS
(`renderToString` queues anyway).

### 5.6 CSP and packaging
- Smetana default: no CSP change. Graphviz mode: add `'wasm-unsafe-eval'` to `script-src` only
  when `graphviz: "viz"`; keep `worker-src 'none'`, `connect-src 'none'`.
- Update `package-contract.test.ts` expectations for the new setting and CSP; add LICENSE copy of
  `@plantuml/core` to `out/bundle/` in `esbuild.mjs`; add dependency pinned exactly
  (`"@plantuml/core": "1.2026.9"`, never `^`, never < 1.2026.6). Check `.vscodeignore` keeps
  `out/bundle/**`.
- npm install is needed to implement this; also corporate artifactory note from memory
  (`UV_NO_CONFIG` concerns uv only; for npm verify the registry is reachable).

### 5.7 Tests to add
1. Unit: renderer-mode resolution (`auto/javascript/jar` x jar configured/not x trusted/untrusted)
   and error classification; config reader + `package.json` contract for the new settings.
2. Unit (jsdom or real engine in a browser-like env): the webview module renders sequence and
   class fixtures to SVG, caches by hash, converts to data-URI img, reports errors.
3. Content patch: rendered diagram nodes survive a patch when source unchanged (extends
   `contentPatch.test.ts` / `editLock.test.ts`).
4. Security: no `child_process.spawn` call in `javascript` mode (spawner hook asserts zero
   spawns, as proposed in SEC-01 tests); local include loader rejects paths outside the policy;
   CSP unchanged for Smetana mode.
5. Visual fixtures (`test/visual`): add JS-vs-jar comparison fixtures (sequence, class,
   activity, component, state, with skinparam and theme) to decide the real fidelity gap; update
   `12-plantuml-optional.md` and `13-plantuml-executable-not-found.md`.
6. Keep all existing spawner tests: the jar path is retained.
7. Manual check in a real VS Code webview for wasm CSP and first-render latency (cannot be
   covered by unit tests).

### 5.8 Effort and risks
**Effort: L** (about 5-8 days): webview module and message protocol (M), patch/cache integration
without flicker (M), settings/trust/fallback plumbing and tests (M), include loader (S-M, can be
deferred), visual fidelity triage (S-M, unknown).
Smaller variant, **M**: `renderer: "javascript"` opt-in only (experimental), no auto-fallback, no
include loader; ship, gather fidelity feedback, then flip the default to `auto`.

Main risks:
1. Layout/font differences vs jar for Graphviz-class diagrams (Smetana) may annoy users who
   compare outputs; mitigate with `graphviz: "viz"` and visual fixtures.
2. Main-thread blocking on large diagrams (engine in webview); mitigate with `maxSvgSize`,
   serialization, possibly one hidden iframe/worker later.
3. Young dependency with moving internals (worker model changed in 1.2026.9): exact pin, upgrade
   test gate.
4. Webview refactor around content patching and edit lock (flicker, stale diagrams).
5. Wasm CSP in VS Code webview unverified.
6. Bundle +3.4-4.8 MB.

## 6. Open questions for the user
1. Default for existing users who already set `jarPath`: keep jar (no behaviour change) or
   switch to `auto` (JS first)? Proposed: if `jarPath` is set and `renderer` unset, treat as `jar`.
2. Is Smetana-only layout acceptable for the default (smaller, no wasm CSP change), or do you
   want Graphviz (viz wasm) from day one?
3. Do you rely on local `!include`, stdlib (`C4`, AWS sprites) or `!theme` from the library? These
   need either the include loader, bundled stdlib, or the jar.
4. Offline/privacy policy: confirm the webview must stay at `connect-src 'none'` (so no
   plantuml.github.io fetches).
5. Ship as experimental opt-in first (effort M) or go straight to `auto` default (L)?
6. Should the JS path be allowed in Restricted Mode (no process spawned), unlike the jar?
7. Acceptable VSIX growth of about 3.4-4.8 MB?

## 7. Sources
- https://plantuml.com/news (2026-05-26 npm announcement)
- https://plantuml.com/en/changes (TeaVM/MIT/Smetana/worker changelog entries)
- https://plantuml.com/faq (licences, Graphviz)
- https://github.com/plantuml/plantuml/issues/2715 (npm publishing, closed)
- https://cdn.jsdelivr.net/npm/@plantuml/core@1.2026.9/README.md and `GITHUB_INTEGRATION.md`
  (API, options, includes loader, Graphviz/Smetana, worker/iframe advice)
- https://registry.npmjs.org/@plantuml/core (versions, dates, MIT, exports, unpacked size) and
  https://data.jsdelivr.com/v1/packages/npm/@plantuml/core@1.2026.6 (file sizes)
- https://github.com/plantuml/plantuml-for-github (Smetana-only, no wasm, MV3 CSP)
- Own measurements: file sizes via curl; Node import test (window/document missing); grep of
  bundles for eval/Function/Worker/Blob/WebAssembly.
- Unverified: real-webview behaviour (wasm CSP, latency), JS-vs-jar fidelity per diagram type,
  stdlib bundle sizes, how `plantuml-mcp-js` runs under Node.
