# Refactoring feasibility study (structure, interfaces, modularity) — analysis

Date: 2026-10-21. Status: research only, no code changed. Branch surveyed: `dev/gsemet`.
Question: can the extension be refactored to improve structure, interfaces, extensibility and
modularity, reduce complexity and oversized files, and fix serious SOLID or other principle
violations? Broad survey, no implementation detail. Related intent:
`../refacto-for-future-expansion/01-intent.md` (renderer reuse in other hosts), detailed in
`02-multi-host.md` (Tauri, pywebview, JetBrains, Copilot app canvas, MCP Apps).

## Decisions (user, 2026-10-21)

- **D1 Multi-host is a driver**: preview **and editing** will ship outside VS Code later, so
  the host-neutral split covers edit operations, not only rendering. Seams first (see 5).
- **D2 CSP / script loading**: change it only if security improves with no visible effect for
  the user (e.g. no inline script, bundle loaded by `script src` + nonce); otherwise keep it.
- **D3 Feature freeze** during the refactor.
- **D4 Tests are reorganised** as part of the refactor (monolith splits included).
- **D5 Import boundaries** are enforced by lint over plain folders; **no npm workspaces** now.
- **D6 TSDoc required**: the internal API stays undocumented as a manual, but every exported
  symbol of the core, the service interfaces and the message protocol gets TSDoc. This is part
  of each phase's definition of done.
- Multi-host specifics (next host, rendering location, undo/save, feature parity) are recorded
  in `02-multi-host.md`.

## 1. Verdict (short)

**Feasible, worth doing, but only incrementally. Overall effort L (XL if the page script is
fully moved to a typed bundle). Risk medium, well mitigated by the test campaign.**

The pure core is already in good shape: of ~90 `src/` modules only 3 import `vscode`
(`extension.ts`, `preview/webview.ts`, `preview/bibScan.ts`). `mapping/`, `comments/`, `state/`,
`frontmatter/`, `configuration/`, `security/` are small, `vscode`-free and unit tested. The debt
concentrates in two god files and one pattern:

- `src/extension.ts` (5 023 lines, ~170 functions, module-level mutable state): the whole host.
- `src/webview/scrollSync.ts` (5 206 lines): the whole page runtime as one template literal,
  with ~30 modules injected through `Function.prototype.toString()`.
- Large inline CSS (`previewStyles.ts`, 3 782 lines) and test monoliths that mirror the above.

Splitting these is mostly mechanical move-and-wire work behind stable seams; no rewrite needed.

## 2. Hotspots

| File | Lines | Main problems |
| --- | --- | --- |
| `src/webview/scrollSync.ts` | 5 206 | God script: scroll sync, editing, toolbar, comments, TOC, patching, message loop all in one closure. Untyped JS inside a string: no type check, no lint, no tree-shaking, no source maps. `if (message.type === ...)` chain for host messages. |
| `src/extension.ts` | 5 023 | God module: activation, commands, panel lifecycle, render scheduling, message validation and dispatch, every edit handler (blocks, labels, checkboxes, frontmatter, images, comments), link resolution, history, incoming changes, file watchers, diagnostics, editor-group locking, 18 `*ForTests` exports. ~12 module-level `let`/`Map` singletons. |
| `src/preview/previewStyles.ts` | 3 782 | Eight CSS blobs in template strings; no CSS tooling, hard to find the rule for a feature. |
| `src/webview/editActions.ts` | 2 086 | One factory closure holding every palette action; must stay self-contained because it is stringified. |
| `src/render/mystRenderer.ts` | 1 836 | Many AST passes in one file; `normalizeNode` (~285 lines, ~40 branches) is a type/name switch over all node kinds. |
| `src/frontmatter/okfFrontmatter.ts` | 1 720 | ~60 functions: parse, schema rules, validation, serialization and preservation mixed. |
| `src/webview/editPalette.ts` | 1 208 | UI, layout and action wiring in one factory. |
| `src/webview/commentThreads.ts`, `fileLinks.ts`, `html-sanitizer.ts`, `anchoring.ts` | 520-740 | Acceptable size; watch growth. |
| `ActivePreview` interface (`extension.ts` l.239) | ~70 fields | God object: panel, queue, watchers, timers, edit lock, pins, comments, incoming marks, test counters. |
| Tests: `test/webview/scrollSync.test.ts` 10 275, `test/integration/realInput.test.ts` 3 959, `test/visual/capture.py` 5 390, `previewEditing.test.ts` 1 409 | | Monoliths mirroring the god files; slow to navigate, merge-conflict magnets. |

## 3. Findings by theme

### 3.1 Structure and layering

- Three layers exist implicitly (pure model / host shell / page runtime) but are not visible in
  the tree: `src/webview/` mixes page-only modules with pure helpers also used by the host;
  `src/preview/` mixes host glue (`webview.ts`) with pure contracts (`previewMessages.ts`).
- The host has no "feature" boundary: comments, blocks, frontmatter, links, history, incoming
  changes each live as loose functions in `extension.ts` sharing globals.
- Rendering (`render/`), build (`build/`) and preview orchestration are separate modules, but the
  orchestration (`updatePreview`, `applyPlantUml`, content patch, pending overlay) sits in
  `extension.ts` instead of a preview controller.
- No explicit layering rule enforced by tooling (e.g. "core must not import vscode or DOM").

### 3.2 Interfaces and contracts

- Webview → host: two coexisting validation styles. New messages use the registry in
  `previewMessages.ts` (good: one validator per type); legacy messages still go through the
  hand-written `isPreviewSyncMessage` boolean chain and a large `handlePreviewSyncMessage`.
- Registration is split: validator in `previewMessages.ts`, handler in `registeredMessageHandlers`
  inside `extension.ts`, sender in the page string. Nothing ties the three together by type.
- Host → webview: ~20 message types (`previewContentPatch`, `previewComments`, `sourceScroll`,
  `themeChanged`, ...) are built as ad hoc object literals; no shared union type, no validator
  on the page side beyond `sameContext` checks.
- Payloads are `Record<string, unknown>` with `as` casts in handlers (`message.text as string`).
  A discriminated union per direction would remove the casts and give exhaustiveness checks.
- `PreviewRuntimeContext` (page boot config) is a flat bag of optional flags; settings are
  normalized twice (host and page, e.g. `stickyHeadingDepth`).

### 3.3 Extensibility (cost of common additions today)

- **Palette action**: edit `editActions.ts` (closure), often `editPalette.ts`, `slashMenu.ts`,
  styles, and sometimes host handlers. No action descriptor/registry with id, label, mode
  (strict/gfm/myst), icon and handler.
- **MyST directive**: touch `mystRenderer.ts` (`normalizeNode` branch), sanitizer allow-lists,
  `previewStyles.ts`, palette/slash menu, maybe `mystTargets.ts` and the Sphinx extension. No
  directive plug-in shape (render, style, edit-action, syntax-detect in one place).
- **Setting**: `package.json` contributes, a `configuration/*` reader, `ActivePreview` field,
  `runtimeContextSettings`, `PreviewRuntimeContext`, page-side normalization. Five-plus places.
- **Message**: three files plus page string (see 3.2); the registry comment documents the two
  host steps but the page side is unchecked.
- **Host** (refacto intent): page runtime calls `acquireVsCodeApi()` directly and the host logic
  is bound to `vscode` types; no transport/port interface to plug another host.

### 3.4 Modularity and dependency direction

- Good: pure modules never import `vscode`; `previewMessages.ts` documents "no vscode import".
- `scrollSync.ts` imports ~30 page modules only to stringify them: the dependency graph is real
  at build time but invisible at runtime (one flat scope, shared free variables).
- Stringified modules must be "self-contained" (documented in `editActions.ts`): they cannot
  import helpers, which forces duplication and big closures (see 3.6).
- `extension.ts` is a hub that every feature depends on and that depends on every feature; any
  change touches it (26 commits on it since 2026-09-01).

### 3.5 Complexity

- Long functions: `handlePreviewSyncMessage` (~190 lines), `updatePreview` (~130),
  `createPreview` (~170), `normalizeNode` (~285), the page message listener and the page boot.
- Timer/flag state machines (pending overlay, content-patch fallback, edit lock, pending pin,
  deferred PlantUML, frontmatter refresh, link enrichment) are coordinated by fields on
  `ActivePreview` and by call order, not by explicit states.
- 18 `*ForTests` exports and test counters (`activePathChanges`, `restoreCalls`) on production
  state show the host is hard to test from the outside.

### 3.6 SOLID and other principles

- **SRP** (serious): `extension.ts`, `scrollSync.ts`, `ActivePreview`, `okfFrontmatter.ts`,
  `editActions.ts` each own many reasons to change.
- **OCP** (serious): adding a message, directive, palette action or host-message type means
  editing central `if`/`switch` chains (`isPreviewSyncMessage`, `normalizeNode`, page listener).
- **ISP**: handlers receive the whole `ActivePreview` though each needs 2-5 fields; the page
  runtime context is one wide interface.
- **DIP**: host features call `vscode.workspace`, `vscode.env.clipboard`, `fs` directly instead
  of narrow ports (document store, clipboard, file system, git); the page calls
  `vscode.postMessage` directly instead of a transport.
- **LSP**: no notable issue (little inheritance).
- **DRY**: line/pin validation repeated across `isPreviewSyncMessage` and the registry;
  setting normalization repeated host/page; `post*Result` helpers near-identical (~10 of them).
- **Pure core / imperative shell**: respected below `src/` folders, broken in the two god files
  where decision logic (which edit to apply, whether a render is stale) is mixed with I/O.
- **State management**: module-level singletons in `extension.ts` (`activePreview`,
  `sessionViewPreferences`, storages, watchers) make lifetime and test isolation implicit.
- **Error handling**: ~80 bare/ignored `catch` blocks across `src/`; no common result/error
  type for host operations; user-facing errors posted through per-feature messages.
- **Page-script injection limits**: no type checking or lint of the generated script body,
  `toString()` output depends on the bundler/minifier (helpers renamed or hoisted can break),
  CSP nonce applies to one huge inline script, no per-module source maps, debugging in the
  webview shows one anonymous blob, no code-splitting or lazy loading.
- **Testability**: page logic is tested by evaluating the string in `node:vm`, so a 10k-line
  test mirrors the 5k-line script; integration tests drive the host via `*ForTests` hooks.

## 4. Target directions (short)

- **Host**: split `extension.ts` into `activation` (commands, registrations), a
  `PreviewManager` (set of previews, active tracking, editor-group lock), a per-panel
  `PreviewSession` (owns its state and disposables), and feature controllers
  (`comments`, `blocks`, `frontmatter`, `links/history`, `incomingChanges`, `diagnostics`,
  `plantUml`) each registering their own message handlers.
- **Contracts**: one `messages/` module with discriminated unions for both directions,
  validators derived from or co-located with the types, and a typed `MessageRouter` on each
  side (`on(type, handler)`); retire `isPreviewSyncMessage`.
- **Page runtime**: bundle the page as a real esbuild IIFE (precedent: `mermaidPreview.js`)
  with normal imports; keep only the boot context injected as JSON. Then split by feature
  (`scroll`, `editing`, `toolbar`, `comments`, `toc`, `patching`) around a small page bus.
- **Extension points**: registries for palette actions (descriptor + handler), MyST directives
  (render pass + sanitizer rule + style + palette entry), and settings (one table that drives
  reading, runtime context and normalization).
- **Ports**: narrow interfaces for document access, clipboard, file system, git baseline, and
  host transport; the VS Code adapter implements them (also serves the multi-host intent).
- **Renderer**: `mystRenderer.ts` as an ordered list of named passes; `normalizeNode` as a
  dispatch table per node kind. `okfFrontmatter.ts` split into parse / validate / serialize.
- **Styles**: move CSS to `.css` files loaded as text by esbuild (or per feature), keep the
  contract tests on the resulting strings.
- **Tooling**: an import-boundary lint rule (core ↛ vscode/DOM, webview ↛ host).

## 5. Suggested incremental order

Ordered so the core and protocol seams exist before any large split (D1). Features are frozen
for the whole sequence (D3).

**Definition of done for every phase**: `just preflight` green; no visible behavior change
(visual baselines and real-input tests unchanged); TSDoc on every exported symbol added or
touched in the core, the service interfaces and the message protocol (D6); the test files of the
touched area reorganised to mirror the new modules (D4); import-boundary lint passing once it
exists (D5).

0. **Safety net (S)**: focused tests for what the campaign covers poorly (timer/race ordering,
   page-side message validation, `toString()`-sensitive code) before moving code.
1. **Protocol (S-M)**: one typed, transport-agnostic message protocol for both directions,
   including all edit messages; legacy messages moved to the registry; typed routers; a core
   revision counter instead of VS Code document versions. Protected by `previewMessages`,
   security/contract and integration tests. Low risk.
2. **Service interfaces (M)**: host-api ports (documents + text edits, files, settings, trust,
   clipboard, dialogs, git, diagnostics, watchers, processes) with a VS Code adapter; core file
   access made async. Edit operations become pure core functions returning text edits.
   Protected by unit and integration tests. Risk: async conversion of sync fs paths.
3. **Host extraction (M-L)**: feature controllers, `PreviewSession`, `PreviewManager`, all
   depending on ports only; globals removed. Protected by integration (`lifecycle`,
   `previewEditing`, `commentWrite`, `blockMove`, ...) and real-input tests. Risk:
   lifecycle/timer ordering (reload, dispose, edit lock).
4. **Page bundle (L)**: page runtime as a typed esbuild bundle with a `HostTransport`; assets
   (CSS, KaTeX, Mermaid) as files; inline script removed only under D2. `vm`-based tests load
   the bundle. Protected by `scrollSync.test.ts`, visual scenarios, scroll-sync and real-input
   suites. Highest value, highest risk (load order, CSP, test harness rewrite).
5. **Folder layout + lint (S-M)**: `src/core`, `src/host-api`, `src/page`,
   `src/node-services`, `src/host-vscode`, with lint-enforced import rules (D5).
6. **Page split (M)**: feature modules on a page bus. Same protection as 4.
7. **Extension registries (M)**: palette actions, MyST directives, settings (one table that also
   generates the `package.json` schema). Protected by `editActions`, `editPalette`,
   `slashMenu`, `mystFeatures` and visual fixtures.
8. **Renderer and frontmatter internals, CSS files, remaining test splits (M)** including
   `test/visual/capture.py`: low risk.

Weak spots of the campaign (covered by phase 0): timing/race behavior across timers, page-side
message validation, and bundler-dependent `toString()` output.

## 6. Open questions

Answered (see Decisions): multi-host driver (D1), CSP change (D2), feature freeze (D3), test
split timing (D4), lint vs grep for import boundaries (D5: lint).

1. Target size budget per file (e.g. 600 lines src, 1 000 tests) enforced in `just check`?
2. Which lint tool for boundaries (ESLint `no-restricted-imports` / `import/no-restricted-paths`,
   or `dependency-cruiser`)? Both add a dev dependency.

> Decided 2026-10-22: after the okfreq requirements (backlog/P3/requirements-okfreq), which lock behaviour first.
