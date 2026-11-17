READ-ONLY analysis of /Users/az02065/Projects/DevTools/markdown-okf-schema-studio (branch dev/gsemet, HEAD 9df67aa "chore: version 0.3.1"). Nothing was modified or run.

## Part A: features

### A1. myst-autodetect (backlog P2 intent; clickable-URL part already done in a6d6d1a)

**Current state**
- The live preview renders in-process with the JS `myst-parser`. `src/render/mystRenderer.ts` `loadEngine()` at lines 72-80. `renderMyst()` at ~1459-1505 calls `mystParse(expandGithubAlerts(...))` at line 1473 with **no options argument**.
- The JS parser's defaults (`node_modules/myst-parser/dist/myst.js`, defaultOptions) are always on: smartquotes, colonFences, frontmatter, math (dollarmath), footnotes, citations, deflist, tasklist, tables, blocks. Only `strikethrough` is off. Nothing in src/ or test/ references `strikethrough`, so `~~x~~` is literal in the live preview. This is a parity gap, found by reading config, not by running.
- Python-only extension names have no JS toggle: `substitution`, `attrs_inline`, `fieldlist`, `html_admonition`, `html_image`, `replacements` (typographer is off). Gating those means detection only, not disabling.
- The per-extension names map to JS `extensions` keys: colon_fence→colonFences, dollarmath→math, deflist, tasklist, smartquotes, strikethrough. So real disabling is possible for those via `mystParse(src, {extensions:{...}})`.
- Nothing reads a user conf.py. `grep conf.py src` finds nothing. `src/build/sphinxBuild.ts` (~169-210) spawns `sphinx-build` against the package's own `sphinx/` folder, and the staged path is not wired into live preview (note at `src/build/sourceTransforms.ts:60-68`). The only `myst_enable_extensions` list is the package's own `sphinx/conf.py` (lines ~15-28, including `substitution`, `attrs_inline`, `fieldlist`, `html_image`, `replacements`, and so on).
- Diagnostics: `normalizeNode` pushes warnings into `RenderDiagnostic[]` (e.g. "Directive {x} is not available outside a full build." at mystRenderer.ts ~1170-1178). `renderPipeline.ts:192-193` tags them `code: "myst-diagnostic"` and attaches the file. They are shown only in the preview status aside (`src/preview/webview.ts` ~84-103, `data-sphinx-preview-diagnostics`). There is **no** `DiagnosticCollection` in src. The only `showWarningMessage` calls are for link failures (extension.ts ~2223-2310).
- Tests: `test/rendering/mystFeatures.test.ts` (37 tests) and the contract fixture `sphinx/tests/fixtures/sphinx-features/feature-contract.md` asserting `result.diagnostics.length === 0`.

**Approach**
1. Discover the closest `conf.py` by walking up from the document, bounded by the workspace folder. Parse `myst_enable_extensions` with a regex over the list literal, stripping `#` comments. Handle `+=` and `extensions` containing `myst_parser` as the "MyST enabled" signal. Do not execute Python.
2. Build a feature→extension table (dollarmath, colon_fence, deflist, substitution `{{ }}`, attrs_inline `{.cls}`, fieldlist `:field:`, html_admonition, html_image, tasklist, replacements). Detect usage from mdast node types or regex on the source, and emit `Warning: ...` diagnostics with the exact wording from the intent.
3. Optionally pass `extensions` to `mystParse` for the mappable ones. This changes rendering and needs tests.

**Files**: `src/render/mystRenderer.ts`, `src/render/renderPipeline.ts`, new `src/configuration/mystConfiguration.ts` (or similar), a conf.py locator, `test/rendering/mystFeatures.test.ts`, `test/configuration/*`, fixtures under `sphinx/tests/fixtures/`.

**Risks**
- Regex parsing of Python misses `myst_enable_extensions` set up dynamically (`+=`, helper functions). Fall back to "unknown" and show no warning.
- Per-file gating "by default" would break today's always-on behaviour (colon fences, admonitions, directives), which `mystFeatures.test.ts` relies on.
- Disabling a JS extension changes rendering for users who have no conf.py.

**Ambiguities**
- No conf.py: plain GFM, or current always-on behaviour? Recommend keeping today's behaviour (no warnings), otherwise every plain `.md` file gets noise.
- The intent says both `config.py` and `conf.py`. Use `conf.py`.
- Warn-only vs actually disable. Warn-only is much smaller.
- Walk-up stop point: the workspace folder, a `.git` root, or the filesystem root?
- Does the `myst_parser` extension check also count when `extensions` is missing?

**Size**: M for warn-only with conf.py discovery and tests. L if features are actually disabled in the renderer.

### A2. local-comment-mode (backlog P2 intent)

**Current state**
- Source mapping is **block-level only**. `src/render/mystRenderer.ts` `sourcePositionProperties()` (~481-490) emits `data-line` and `data-end-line`. `src/security/html-sanitizer.ts` ~325-345 (`rewriteSphinxHtml`) converts these to `data-sphinx-source-file`, `data-sphinx-source-line`, `data-sphinx-source-end-line`, `data-sphinx-preview-document`, `data-sphinx-preview-block`. `src/mapping/sourceMapping.ts` `parseSourceMappings` (~80-141) and `sourceRangeForLines` (~20-52, line→UTF-16 offsets, CRLF-aware) are the helpers.
- Selection: the webview already reads `window.getSelection()` only when saving state (`src/webview/scrollSync.ts` ~147-148). It sends `selectedText` (capped at 4096 chars) in `previewState` (`src/extension.ts` ~148, ~1304). There are no `selectionchange`, `mouseup` or `pointerup` listeners anywhere in src/webview or src/preview (grep confirmed).
- Message protocol: a message type must be added in two places, the union at `src/extension.ts:112` and the `validType` whitelist at ~412-425. Payload validation follows at ~436-481. `previewEditOpen` already passes a line range through `sourceRangeForLines` (`extension.ts:1348`).
- Re-anchoring: `shiftAnchorsForEdits` (`extension.ts:2668`) shifts only the scroll anchor line. `shiftLineForEdits` (`src/webview/anchorPolicy.ts` ~250-262) is line-only. `onDidChangeTextDocument` is at `extension.ts:3263`. `src/mapping/textDiff.ts` `minimalReplacement()` computes a minimal prefix/suffix diff with CRLF and surrogate safety. It is useful for computing a edit delta but does not map offsets through edits.
- Username: **no git access anywhere in src**. `child_process` is used only in `src/render/plantUmlRenderer.ts` and `src/build/sphinxBuild.ts`. Nothing reads `.git/config`.
- Watchers: `extension.ts:302` (stem index `**/*.md`), `:1057` (linked targets, a `RelativePattern(dirname, filename)` pattern to copy for the sidecar), `:2804` (dependency watcher on resourceRoot). `.gitignore` also lists `.agents/changes/` (see Part B).

**Approach**
1. Webview: a new module (not inside the 3668-line `scrollSync.ts`; follow the `linkNavigation.ts`/`mermaidPreview.ts` style, which is stringified into the webview). It shows a floating button on a non-empty selection inside `[data-sphinx-source-line]` blocks, and posts `previewCommentCreate` with `{selectedText, prefix, suffix, blockLine, blockEndLine, documentId}`.
2. Anchor: locate the quote inside the block's source via normalized plain text (rendered text differs from source: `**`, links, entities, escapes). Store the anchor as `{quote, prefix, suffix, startLine, endLine}`, not as raw offsets.
3. Re-anchor on edits: on each `onDidChangeTextDocument`, re-run the quote search in the current block range, falling back to the whole document. Mark the comment "orphaned" if nothing matches.
4. Persistence: `<name>.comments.json` next to the `.md` (`{version, comments:[{id, anchor, thread:[{author, createdAt, text}]}]}`). Write with `vscode.workspace.fs`. Watch the sidecar with `RelativePattern(dirname, basename + ".comments.json")` to reload when another tool or user changes it.
5. Author: a new setting `markdownOkfSchemaStudio.comments.authorName` (default empty), falling back to git `user.name`. Read git config via the built-in git extension API (`vscode.extensions.getExtension('vscode.git')`, verify `getConfig` in the installed version) or by parsing `.git/config`. Spawning `git` is the approach the code already takes for `sphinxBuild`, but workspace trust must gate it.

**Files**: `src/webview/` (new comment module), `src/extension.ts` (message union, validType, watcher, write/read), `src/mapping/sourceMapping.ts`, `src/security/html-sanitizer.ts` (if new attributes are needed), `src/state/` (comment state), `package.json` (new config key), `test/mapping/*`, `test/webview/*`, `test/integration/*`.

**Risks**
- Selections that span blocks, or inside tables, lists and code, have no single block range.
- Duplicate quotes in one document: use prefix/suffix plus block line to disambiguate.
- Saving a sidecar triggers the watcher and a refresh loop. Ignore self-writes.
- Untrusted workspace: sidecar writes and git spawn should be disabled.
- The security tests (`test/security/html-policy.test.ts`) enforce the attribute allowlist.
- Comments must not dirty the `.md`, and the edit lock (`src/state/editLock.ts`) must not block comment saves.

**Ambiguities**
- Is a comment a "thread" that is stored in the sidecar, or a markdown annotation? The intent says sidecar.
- Orphan comments: keep, hide, or delete?
- Sidecar name for `README.md` is `README.comments.json`.
- Should comments be visible in the Open-With editor, or only in the preview?
- Git identity fallback order: setting, then `git config user.name`, then empty?

**Size**: L (new webview UI, message protocol, re-anchoring, sidecar I/O and watcher, git identity, tests).

## Part B: test and gate infrastructure

### Commands (package.json scripts)
- `npm test` = `compile` + `test:unit` + `test:contracts` + `test:security`. Output is in `out/reports/{unit,contract,security}/tests-*.xml`.
- **unit**: `node --test` over `out/test/{build,configuration,frontmatter,mapping,navigation,rendering,site,state,webview}/*.test.js`. Progress says 775 tests. It does **not** include `out/test/integration`, `out/test/visual` or `out/test/security`.
- **contracts**: `out/test/rendering/*.contract.js`. Only `test/rendering/sphinxFeatures.contract.ts` matches (2 tests).
- **security**: `out/test/security/*.test.js` (html-policy, package-contract, resource-policy, userFacingText). Progress says 20 tests.
- **types**: `check-types` = `tsc --noEmit -p .`. `compile` = `tsc -p .`.
- **visual**: `test:visual` = `visual:render` (compile + bundle + `out/test/visual/renderFixtures.js`) then `uv run --no-sync --group docs python test/visual/capture.py`. Progress says 119 scenarios, 114 screenshots. Python Playwright, and Chromium is already in `~/Library/Caches/ms-playwright`. I did not verify whether it runs headless.
- **integration**: `test:integration` = compile + bundle + `node out/test/integration/run-tests.js`. It runs VS Code via `@vscode/test-electron` in this order: scroll-sync, untrusted, trusted, standalone, then the reload campaign. Flags: `--scroll-only`, `--reload-only`, `--trusted-only`. The trusted suite includes `checkboxToggle.test.ts` and `realInput.test.ts`, which drive the real window through CDP (`page.keyboard.type/press`, `test/integration/realInput/harness.ts` ~152-246, `Meta` on macOS).
- **e2e**: `test:e2e` = `scripts/run-e2e.mjs`: `review:begin` → `test:visual` → `test:integration` → `review:finish`. It writes `out/reports/e2e/e2e-manifest.json` and `tests-e2e.xml`. Progress shows the e2e run as "99 static checks, 94 images".
- Other: `gallery:generate`, `site` (`out/test/site/buildSite.js`), `package` (`scripts/package-extension.mjs`), `test:scroll`, `test:reload`, `test:browser` (alias of visual).

### Just targets (justfile)
- `unit`, `contracts`, `security`, `check-types` (`check-types`), `compile`, `integration`, `visual`, `e2e`, `package`: thin wrappers around the npm scripts. `npm` is `fnm exec -- npm --registry=https://registry.npmjs.org/`.
- `check` = `format` (`just --unstable --fmt`, **rewrites the justfile in place**) + compile + unit + contracts + security + `release-tests`.
- `release-tests` = `uv run --group docs --group release pytest test/build/test_release.py`. **No `--no-sync`**.
- `sphinx-check` = `uv run --no-sync --group docs pytest sphinx/tests/test_sphinx_preview_mapping.py`. The test shells out to `python -m sphinx -W --keep-going -b <builder> -c fixture ...`.
- `preflight` = `clean` (`rm -rf out .artifacts .vscode-test .uv_cache .playwright-cli node_modules/.cache` and `__pycache__`) + `format`, then, collecting failures without stopping: `just check`, `just sphinx-check`, `npm run test:e2e`, and only if e2e passed, `site:gallery` and `site`. Exit 1 if any stage failed. AGENTS.md says `just preflight` must pass before a task is complete.
- `release-check` = `npm ci` + check-types + `npm test` + sphinx-check + package.
- `dev`, `update`, `install`: network (see below).

### Keyboard / GUI requirements
- `realInput.test.ts` and `checkboxToggle.test.ts`, both inside the trusted scenario, need an unlocked macOS desktop with a focused VS Code window. Progress.md records that on the locked screen "keyboard injection fails, checkbox undo suite times out". The final verification in progress.md therefore ran everything except those two suites.
- Visual capture and the other integration suites ran while locked.
- The local VS Code app is at `/Applications/Visual Studio Code.app/Contents/MacOS/Code` (exists here). `run-tests.ts` line 12 uses it, so no download is needed on this machine.

### Network / install flags
- `just dev`: `fnm install`, `npm ci` from npmjs.org, `uv sync --group docs --group release` (PyPI), `playwright install chromium`. **Network.**
- `just update`: `ncu` upgrades, `rm -rf node_modules package-lock.json`, `npm install`, `uv sync --upgrade`, `playwright install`. **Network and destructive.** Do not run it casually.
- `release-tests` (in `check` and `preflight`): `uv run` without `--no-sync` can resolve or sync against pypi.org if the venv is stale. **Possible network.**
- `npm ci` triggers `postinstall` (`scripts/patch-myst-imports.mjs`, which patches node_modules files). Only runs on install.
- `integration` falls back to `downloadAndUnzipVSCode({})` if the local VS Code app is missing. **Network fallback.**
- `visual` and `sphinx-check` use `--no-sync`, so they need an existing `.venv`. Chromium is cached in `~/Library/Caches/ms-playwright`. Version drift with the Python playwright package could still need `playwright install`.
- `unit`, `contracts`, `security`, `compile`, `check-types` need no network once node_modules exists.
- Durations: nothing is documented. Progress.md has only one timing ("include-fanout 4: 5.9 s"). Expect unit in seconds to tens of seconds, and visual and integration in minutes (one VS Code launch per integration scenario). These are estimates, not measured.

### Workflow conventions
- `.agents/changes/` is **git-ignored** (`.gitignore:12`) and **untracked** (`git ls-files` is empty for it). Intents, progress and reports exist only locally.
- Layout: `.agents/changes/backlog/P<n>/<name>/01-intent.md` (short intent; some have `01-intend.md` typos). Archive: `.agents/changes/archives/<NNN-name>/` with `01-intent.md`, `report.md`, and optionally `00-index.md`, `evidence/` and numbered bug files.
- Run log: `backlog/P2/progress.md` has a baseline gate table (U, E2E, probes), a task table (`# | Task | Source | Status | Commit`), an out-of-scope list, a per-task log with review verdicts (APPROVE / FIX-REQUIRED) and a final verification table. Tasks are numbered T1–T16, one commit each, in minor-first order.
- `archives/004-auto-link/report.md` format: `# Report — <name>`, a `Status: **done**` line, a "Delivered" table (`Task | Change | Commit`), and a "Proof of completion" section with test counts.
- Commits: `.github/guidelines/git-commit-message.guidelines.md` (Conventional Commits, subject ≤71 chars, body lines ≤79, user-impact wording, `Assisted-by:` trailer for AI-generated messages, no `Signed-off-by` unless asked). Allowed scopes are in `.github/guidelines/git-commit-allowed-scopes.md`. The session attribution reminder asks for a `Co-Authored-By` trailer. Resolve which trailer applies at commit time.
- Note: the P2 bug run's gates were `npm test`, `test:visual` and `test:e2e`, not the full `just preflight` that AGENTS.md requires.

### Representative test files
- **Webview behaviour (unit)**: `test/webview/scrollSync.test.ts` (226 tests), `test/webview/textEditing.test.ts`, `test/webview/contentPatch.test.ts`, `test/webview/linkNavigation.test.ts`, `test/webview/anchorPolicy.test.ts`, `test/webview/markdownTable.test.ts`.
- **Render (unit)**: `test/rendering/mystFeatures.test.ts` (37), `test/rendering/renderPipeline.test.ts`, `test/rendering/checkboxRendering.test.ts`, `test/rendering/includeBudget.test.ts`.
- **Mapping**: `test/mapping/sourceMapping.test.ts`, `test/mapping/textDiff.test.ts`, `test/mapping/insertion.test.ts`.
- **Contract**: `test/rendering/sphinxFeatures.contract.ts`; Python: `sphinx/tests/test_sphinx_preview_mapping.py`.
- **Security**: `test/security/html-policy.test.ts`, `test/security/resource-policy.test.ts`, `test/security/package-contract.test.ts`.
- **Visual**: `test/visual/scenarios.ts` (44 KB, scenario list), `test/visual/capture.py`, `test/visual/renderFixtures.ts`.
- **Integration (VS Code host)**: `test/integration/realInput.test.ts` (keyboard, GUI), `test/integration/checkboxToggle.test.ts` (keyboard), `test/integration/previewEditing.test.ts` (72 KB), `test/integration/lifecycle.test.ts`, `test/integration/sourceMapping.test.ts`, `test/integration/dirtySnapshots.test.ts`, suite runners `trusted-suite.ts`, `scroll-sync-suite.ts`, `reload-suite.ts`, `run-tests.ts`.

Key file paths: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/src/render/mystRenderer.ts, .../src/render/renderPipeline.ts, .../src/security/html-sanitizer.ts, .../src/mapping/sourceMapping.ts, .../src/extension.ts, .../src/webview/scrollSync.ts, .../src/webview/anchorPolicy.ts, .../package.json, .../justfile, .../AGENTS.md, .../.agents/changes/backlog/P2/progress.md.