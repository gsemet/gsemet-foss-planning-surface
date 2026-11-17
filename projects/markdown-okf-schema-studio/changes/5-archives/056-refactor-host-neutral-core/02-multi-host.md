# Multi-host readiness (Tauri, pywebview, JetBrains, Copilot canvas) — analysis

Date: 2026-10-21. Status: research only, no code changed. Complements `01-analysis.md` and the
intent in `../refacto-for-future-expansion/01-intent.md`.
Question: what refactoring isolates the renderer, the edit logic and the page UI so the product
can also ship as a standalone app (Tauri or pywebview), a JetBrains plugin, or a canvas for VS
Code chat or the GitHub Copilot app?

## Decisions (user, 2026-10-21)

- **M1 Preview and editing** both ship outside VS Code later: edit operations, not only
  rendering, belong to the host-neutral core.
- **M2 Next host**: a **standalone app**, Tauri or pywebview (compared in 2.4, recommendation
  in 4.1). Canvas, MCP App and JetBrains come later.
- **M3 Same behavior as the VS Code extension** in the standalone app. Rendering location is
  chosen for least risk: keep it where it is today (Node, host side), see 3.3.
- **M4 Feature parity**: every host keeps all features (MyST, Sphinx, PlantUML, comments,
  incoming changes, ...). No desktop-only reduction for the standalone app.
- **M5 Undo, save, file navigation outside VS Code**: an ad-hoc mechanism, **designed later**.
  Only the seams are prepared now (3.4).
- **M6 Folders + lint-enforced import boundaries, no npm workspaces** for now.
- **M7 TSDoc** on every exported symbol of the core, the service interfaces and the protocol, as
  part of each phase's definition of done (see `01-analysis.md` section 5).
- **M8 CSP**: change script loading only when it raises security with no visible effect.

## 1. Recommendation (short)

**Feasible. Build a host-neutral core first, then a typed page bundle and one message protocol,
then thin hosts.** About 60% of `src/` is already host-neutral TypeScript. The real coupling is
in `extension.ts` (VS Code document/edit/undo model, trust, settings, watchers) and in the page
script built as a string. Target order (after M2):
**VS Code (refactored) → standalone app (pywebview first, see 4.1) → Copilot app canvas / MCP
App → JetBrains**. Key enabler: a **Node host process** that runs the host-neutral controllers
behind the same protocol, so a standalone shell only opens a window and relays messages.

## 2. External research (checked 2026-10-21)

### 2.1 GitHub Copilot app "Canvas"

- The **GitHub Copilot app** (desktop: Windows, macOS, Linux) is in technical preview, widened to
  Pro/Pro+ on 2026-06-02; Business/Enterprise need an admin policy. **Canvas** is one of its main
  features, and the **Copilot SDK** became GA (Node/TS, Python, Go, .NET, Rust, Java) the same
  day. Source: https://gihyo.jp/article/2026/06/github-copilot-updates (2026-06-03).
- A canvas is a shared, interactive surface (plan, board, dashboard) that humans and the agent
  both edit; it opens in the app's right side panel inside a session. Packaged as a folder with
  `package.json` + entry `extension.mjs` under `.github/extensions/<name>` (project scope) or
  `~/.copilot/extensions/<name>` (user scope); optional JSON state in `artifacts/`; can ship in a
  plugin with skills and MCP servers. Agent-callable "capabilities" (e.g. `get_board`,
  `add_card`). Source:
  https://docs.github.com/en/copilot/how-tos/github-copilot-app/working-with-canvas-extensions
- Mechanics (from the official `create-canvas` skill, not from reference docs): the extension
  calls `joinSession` of the Copilot SDK with `canvases: [createCanvas({...})]`; the runtime
  routes `canvas.open` and `canvas.action.invoke` to it; the scaffold starts a **loopback HTTP
  server** per canvas instance and `open` returns its URL, which the app renders; `actions[]`
  are what the agent invokes. Source:
  https://www.skills.sh/github/gh-aw/create-canvas
  ; real example: gh-aw weekly update 2026-06-29
  (https://github.github.com/gh-aw/blog/2026-06-29-weekly-update/).
- **Unverified**: no formal API reference found; how the rendered URL is sandboxed, which CSP
  applies, whether file writes need approval, and the canvas lifecycle are not documented.
  Requires Node >= 20.19 (per a community example). Treat it as a moving preview target.

### 2.2 MCP Apps (UI inside VS Code Copilot Chat and other chat hosts)

- An MCP tool declares `_meta.ui.resourceUri` pointing to a `ui://` resource with MIME
  `text/html;profile=mcp-app`; the host renders it in a **sandboxed iframe with CSP**
  (`connectDomains`, `resourceDomains`, `frameDomains`); the page talks back through the MCP
  Apps SDK (`App.connect()`, `callServerTool(name, args)`, `sendMessage`, `ontoolresult`). In
  VS Code only the `inline` display mode is supported. Source:
  https://code.visualstudio.com/api/extension-guides/ai/mcp
- Spec: SEP-1865, status Final; full spec in https://github.com/modelcontextprotocol/ext-apps
  (still described as a draft there). Announcement:
  https://blog.modelcontextprotocol.io/posts/2025-11-21-mcp-apps/
  Same UI then works in Claude, ChatGPT, Goose and others (secondary sources, unverified).
- Fit: an inline, chat-sized view (render a document or a section, accept/reject an edit); not a
  full editing surface.

### 2.3 Other hosts

- **VS Code custom editor vs webview panel**: the extension already contributes a
  `customEditors` entry (`package.json`) and also uses webview panels. A custom *text* editor is
  the natural "canvas" inside VS Code: VS Code keeps the `TextDocument`, save and undo.
- **Tauri 2**: system webview (WebView2 / WKWebView / WebKitGTK) + Rust core; JS calls Rust
  through `invoke`; external binaries ship as **sidecars** (`bundle.externalBin`, target-triple
  names, `shell:allow-spawn` capability), including a Node.js sidecar recipe. Source:
  https://v2.tauri.app/develop/sidecar/ . Rendering differences between WebKit and Chromium are a
  risk for the visual baselines.
- **JetBrains**: `JBCefBrowser` (Chromium) embedded in Swing; JS → Kotlin via `JBCefJSQuery`,
  Kotlin → JS via `executeJavaScript`; local assets served by a `CefRequestHandler`; must check
  `JBCefApp.isSupported()` and declare `com.intellij.modules.jcef` (2026.2+). Remote Development
  not covered by the docs. Source:
  https://plugins.jetbrains.com/docs/intellij/embedded-browser-jcef.html
  The host is JVM: the TypeScript core runs either in a bundled Node sidecar or inside the
  browser itself (see 3.3).

### 2.4 pywebview vs Tauri (standalone)

- **pywebview**: Python host + system webview (WebView2 on Windows, WKWebView on macOS,
  WebKitGTK or Qt on Linux). JS → Python through `js_api` / `expose` as `pywebview.api.*`
  (promises, functions run on separate threads), Python → JS through `evaluate_js` / `run_js`,
  `pywebviewready` event, per-window shared `state` (6.0). Source:
  https://pywebview.flowrl.com/guide/interdomain.html . Packaging with PyInstaller or similar
  (not checked). Renderer list from project docs, not re-verified today.
- **Tauri 2**: Rust host, same system webviews, `invoke` / events, capability-based permissions,
  sidecars, bundler, signing and updater built in (2.3).
- **Running the TypeScript core**: neither host runs Node in-process. Options: (a) a **Node
  sidecar** running the existing host-side code (render pipeline, controllers, node-services),
  talking JSON over stdio or a loopback websocket; (b) port the core to the page (browser
  build); (c) port to Python/Rust (rejected: rewrite, behavior drift).
- **Runtimes to ship (M4: all features)**: Node (core), Python + Sphinx (Sphinx build), Java or
  the JS engine (PlantUML). pywebview reuses the Python that Sphinx needs anyway; Tauri adds a
  compiled shell but still needs Python for Sphinx.
- **Comparison**: pywebview is cheaper to build (team already uses Python/uv, Sphinx in-process
  possible, no Rust); Tauri is stronger on packaging, signing, auto-update, footprint and
  permission model. Both use the same webviews, so WebKit rendering differences (macOS, Linux)
  apply to both.

## 3. Mapping the codebase onto a hostable core

### 3.1 Already host-neutral (reusable as is or nearly)

- `mapping/*`, `comments/*` (model, anchoring, store format), `state/*` (pure reducers/bounds),
  `configuration/*` readers (pure normalizers), `security/html-sanitizer.ts`, `security/csp.ts`,
  `preview/previewMessages.ts`, `preview/contentPatch.ts`, `frontmatter/propertiesTable.ts`,
  `schemaValidator.ts`, `myst/confParser.ts`, `render/highlight.ts`, `mathRenderer.ts`,
  `commentMarkers.ts`, `checkboxMarkers.ts`, `mystSyntaxDetect.ts`.
- `render/mystRenderer.ts`: only `node:path` + `parse5` + MyST engine; portable to browser with a
  path shim. `renderPipeline.ts` already takes a structural document (`uri`, `version`,
  `getText()`), not `vscode.TextDocument`, but reads `fs` directly.
- Page modules in `src/webview/*` are DOM-only and host-agnostic except for the `vscode` object
  from `acquireVsCodeApi()` and the stringification pattern.

### 3.2 Leaks (must go behind ports)

| Concern | Where | Port |
| --- | --- | --- |
| Sync file reads, `realpath`, `stat`, `readdir` | `renderPipeline`, `okfFrontmatter`, `fileLinks`, `stemIndex`, `previewNavigation`, `resource-policy`, `confLocator`, `bibScan`, `imageReference`, `mystTargets` (path) | `FileSystem` (async, root-scoped) + path utils |
| Process spawn | `plantUmlRenderer`, `sphinxBuild` | `ProcessRunner` (optional capability) |
| Document text, version, edits, undo | `extension.ts` (`WorkspaceEdit`, `applyEdit` x8) | `DocumentStore` (read, apply text edits, version events) |
| Workspace trust, roots | `extension.ts` (`isTrusted`, workspace folders) | `WorkspaceInfo` |
| Settings and stored choices | `extension.ts` + `package.json` schema | `Settings` (schema owned by core, host maps it) |
| Clipboard, dialogs/pickers, notifications | `extension.ts` | `HostUi` |
| Git user / HEAD baseline | `git/headBaseline.ts`, `comments/author.ts` | `VcsInfo` |
| Diagnostics | `extension.ts` (`DiagnosticCollection`) | `Diagnostics` sink |
| File watching | `extension.ts` (watchers, sidecars, conf files) | `Watcher` |
| Webview URIs, CSP nonce, resource roots | `preview/webview.ts` | `AssetResolver` |
| Page → host transport | `acquireVsCodeApi().postMessage` in the page string | `HostTransport` (page side) |

### 3.3 Target layering

1. **`core`** (pure TS, no Node built-ins except via ports): parse, render, sanitize, source
   mapping, edit operations (block move, label rename, checkbox, frontmatter, comments), schema
   validation, settings schema + normalization, message protocol types and validators.
2. **`host-api`**: the port interfaces of 3.2, plus a capability set (`canSpawn`, `canWatch`,
   `hasUndo`, `trusted`) so features degrade instead of failing.
3. **`page`** (UI package): the page runtime as a typed esbuild bundle, one `HostTransport`
   abstraction (VS Code postMessage, Tauri `invoke`/events, JCEF query, MCP Apps SDK, canvas
   HTTP/websocket), assets (CSS, KaTeX, Mermaid) as files.
4. **`node-services`**: Node implementations of ports (fs, PlantUML, Sphinx, git) reusable by
   VS Code, the canvas extension, a Tauri Node sidecar and a JetBrains Node sidecar.
5. **Thin hosts**: `host-vscode` (today's extension), `host-tauri`, `host-jetbrains`,
   `host-copilot-canvas`, `host-mcp-app`.

6. **`host-node`** (new, for M2/M3): a headless Node process that runs the same controllers
   with Node port implementations and a file-backed `DocumentStore`, and speaks the page
   protocol over stdio / loopback websocket. Standalone shells (pywebview, Tauri) and later the
   canvas extension and a JetBrains sidecar reuse it.

**Rendering location (M3)**: keep rendering **host-side in Node**, as today. It preserves the
current output byte for byte (same MyST engine, sanitizer, PlantUML/Sphinx processes, same
tests), and all features need processes anyway (M4). Running the core inside the page stays an
option for later (precedent: Mermaid already renders in the page; PlantUML JS analysis), not a
prerequisite.

### 3.4 Hard parts

- **Source of truth and undo (M5, deferred design)**: VS Code owns `TextDocument`, dirty
  state, undo/redo and save; other hosts need an ad-hoc mechanism, designed later. Seams to
  prepare now: edit ops emit text edits only (never write files); a `DocumentStore` port
  (`read`, `applyEdits` → new revision, change events, `save`, dirty flag); capabilities
  `hasUndo` / `hasSave`; a `Navigation` port (open document, reveal line, history) instead of
  direct `showTextDocument`; no controller assumes a paired text editor.
- **Version / stale-message gate** relies on VS Code document versions: generalize to a core
  revision counter.
- **Workspace trust**: only VS Code has it; others need an explicit "trusted folder" decision
  (PlantUML, Sphinx, includes outside root).
- **Settings schema** lives in `package.json` contributes: generate host schemas (VS Code
  `package.json`, JetBrains settings UI, Tauri prefs) from one core table.
- **PlantUML / Sphinx processes (M4: kept everywhere)**: the standalone app ships or locates
  Java (or uses the JS PlantUML engine) and a Python env with Sphinx; MCP Apps and canvas need
  a host-side process for them (canvas has Node; MCP App would delegate to its MCP server).
- **CSP / nonce / resource URIs**: VS Code `asWebviewUri` + nonce, Tauri asset protocol, JCEF
  scheme handler, MCP Apps CSP metadata, canvas loopback server: one `AssetResolver` per host.
- **File watching** (dependencies, comment sidecars, conf files, git HEAD): per-host
  implementations, polling fallback.
- **Synchronous fs** in core modules blocks a browser build: needs an async conversion.
- **Theme tokens**: CSS uses `--vscode-*` variables; needs a neutral token layer mapped per host.
- **Editor pairing / scroll sync with a text editor** exists only in IDE hosts; standalone and
  canvas run "preview-as-editor" only.

## 4. Per target

| Target | Feasibility | Effort | Reuse as is | Blockers | First step |
| --- | --- | --- | --- | --- | --- |
| VS Code custom editor / webview (refactored) | High | M (part of 01 phases) | everything | none | ports + protocol inside the current extension |
| Copilot app canvas | Medium (preview API) | M | core, page bundle, node-services (Node runtime available) | undocumented API, sandbox/CSP unknown, document ownership (no IDE buffer), loopback server security | spike: read-only canvas rendering a repo `.md`, one `render` action |
| MCP App (VS Code chat, Claude, ...) | Medium | S-M | core render + sanitized HTML + light page | inline only, small viewport, no processes, CSP | tool `render_markdown` returning a `ui://` preview with accept/reject of an edit |
| pywebview standalone | High | L | core, page, `host-node` sidecar; Sphinx in the same Python | ad-hoc undo/save (M5), packaging Node + Python + Java, WebKit differences | pywebview window loading the page bundle, relaying to `host-node` |
| Tauri standalone | High | L | core, page, `host-node` sidecar | same as pywebview + Python env as a second sidecar, Rust skills | same spike with a Tauri shell |
| JetBrains plugin | Medium | XL | page bundle, core (in page or Node sidecar) | Kotlin host, JCEF availability, Node runtime distribution, IDE `Document`/undo mapping, settings UI, Remote Dev | JCEF tool window rendering the page bundle in read-only mode |

### 4.1 Standalone recommendation

**Build `host-node` first, then a pywebview shell; keep Tauri as the production option.** The
shell is thin (window, menus, file dialogs, message relay), so switching from pywebview to Tauri
later costs little. pywebview wins the first step because Python is already required for
Sphinx (M4) and the team toolchain is Python/uv; reconsider Tauri when signing, auto-update and
footprint matter for distribution.

## 5. Impact on the phases of `01-analysis.md`

The phases in `01-analysis.md` section 5 already follow this order (seams before splits):
safety net, protocol (transport-agnostic, revision counter), service interfaces (including
`DocumentStore`, `Navigation`, capabilities for M5), host extraction on ports only, page bundle
with `HostTransport` and neutral theme tokens, folder layout + lint (M6). Then, after the
VS Code refactor:

- **H1 `host-node`** (M-L): headless host over stdio/websocket, file-backed `DocumentStore`,
  Node watchers; protected by reusing the integration scenarios against it.
- **H2 Standalone spike** (M): pywebview shell, then the M5 design (undo, save, navigation).

The test campaign keeps its value: unit tests target `core`; integration and real-input tests
target `host-vscode`; visual tests target the `page` bundle and can later run per host.

## 6. Open questions

Answered (see Decisions): next host (M2), rendering location (M3), undo/save owner (M5,
deferred), Sphinx/PlantUML outside VS Code (M4), npm workspaces (M6).

1. Is the Copilot app preview (no formal API reference yet) acceptable as a later target, or
   wait for documented APIs?
2. Standalone distribution: ship Node, Python/Sphinx and Java inside the app, or detect user
   installs (as the extension does for PlantUML today)?
3. Should the standalone app also offer a plain text editor pane (paired scroll sync), or only
   the preview-as-editor?
