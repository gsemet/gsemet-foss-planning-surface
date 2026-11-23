# Investigation CR-469: render and security file lookups behind the async FileSystem port

## Files and entry points
- `src/core/myst/confLocator.ts` (165 l): `createConfLocator({now,readFile,statFile})`, sync `enabledMystExtensions` / `locate`, caches (2 s recheck). Default stat/read use `fs.statSync/readFileSync`. Callers: `renderPipeline.ts:308` (`enabledMystExtensionsFor`, inside the already-async `renderPreviewDocument`), `session/hostEvents.ts:192-194` (`locateConfFor` before/after `invalidateConfCache`, sync in `onConfFileEvent`). Tests inject `readFile/statFile` (confLocator.test.ts, confLocator.holes.test.ts, SwRS MYST-066).
- `src/core/render/documentGlob.ts` (98 l): `listGlobDocuments` sync recursive `readdirSync(withFileTypes)`; only caller `renderPipeline.ts:223` (the `listDocuments` callback of the render context). `globToRegExp` is pure. SwRS MYST-057.
- `src/core/security/resource-policy.ts` (467 l): `fs` used in 5 places: `realOrResolved` (l.121, check whether it is still used), ctor `fs.realpathSync(root)` (l.207), `realFile` (`statSync` + `realpathSync`, memoized in `fileFacts`, l.227-230), `readBoundedText` (`statSync().size`, `readFileSync`, l.460-463). Callers of `resolveResource[Detailed]`: `readBoundedText`; `renderPipeline.ts` (include, readDiagramFile, glob `allow`); `plantUmlIncludes.ts` (l.103,109,176,209); `session/webview.ts:184-190` (the sanitizer's `resolveResource`, sync, called per attribute from `html-sanitizer.ts:293,432,446`); `core/navigation/previewNavigation.ts`. SwRS CORE-013, TRUST-025, TRUST-002.
- Port `src/host-api/fileSystem.ts`: `stat` (follows links; kind, size, mtime), `readFile`, `readDirectory` (name, kind), `isSymbolicLink`, `realpath`, `isFileNotFound`, `readTextFile`. Already enough for the three files; no port extension strictly needed.
- Node impl `src/node-services/nodeFileSystem.ts` (`createNodeFileSystem`; its JS `realpath` equals `realpathSync`). Memory impl `src/host-memory/memoryFileSystem.ts`: no symlinks (`isSymbolicLink` false, `realpath` = normalise + exists). Precedents of the port used outside node-services: `session/previewNavigator.ts` (`Pick<FileSystem,"realpath"|"stat">`), `session/bibScan.ts`, `core/frontmatter/schemaFiles.ts`.
- `.dependency-cruiser.cjs` NODE_DEBT l.54-57 and l.69-70: `["fs","path"]` becomes `["path"]`, with reason/removal `PATH_SHIM`, for the three files. Check: `just check-boundaries` (justfile l.155).

## The hard part (the real size of the CR)
The render callbacks are synchronous inside sync tree passes. `mystRenderer.ts` `TREE_PASSES` (include expansion `resolveIncludeOnce` l.128-140 and l.307, `readDiagramFile` l.180 and l.234, glob `context.list` l.474 and `mystGridToctree.ts` l.678) call `context.resolveInclude / readDiagramFile / listDocuments` (types `mystTypes.ts:42-47`) synchronously; `renderMyst` is async only at `loadEngine`. The sanitizer (`html-sanitizer.ts`, one sync parse) calls `policy.resolveResource` synchronously through `webview.ts`. A naive async policy means async passes and an async sanitizer.

Two designs:
1. Full async: callbacks return Promises, tree passes and include recursion become async, sanitizer `resolveResource` async. Large blast radius (mystRenderer, mystGridToctree, sanitizer, webview, plantUmlIncludes, about 35 test files that build a policy or render).
2. Recommended (smaller): keep the sync decision logic, move only the I/O.
   - `ResourcePolicy`: async factory (awaits the root realpaths), async `resolveResourceDetailed`/`resolveResource` for the include, diagram-file, glob and `readBoundedText` paths (make only those three passes async: `expandIncludes` recursion, diagram file read, glob list; `renderMyst` is already async).
   - Sanitizer: pre-resolve. Before the sync sanitize in `buildPreviewWebviewHtml`, collect the candidate resource requests and `await policy.prime(requests)` so the sync lookup hits the `fileFacts` memo (a miss refuses, never reads sync). `buildPreviewWebviewHtml` callers (`rendering.ts:224`, `baselineDiff.ts:50`) become async.
- Worker: `renderPreviewSource(input)` is plain-data and runs in `node-services/renderWorker.ts` (plus an in-process fallback). It must take a `FileSystem` (worker and fallback pass `createNodeFileSystem()`; the core receives it, never imports it).
- confLocator: `locate` / `enabledMystExtensions` become async over an injected `FileSystem` (replaces the `readFile/statFile` options; the two test files move to MemoryFileSystem). `hostEvents.onConfFileEvent` becomes async, keeping the before / invalidate / after order.

## Smallest change
1. Port: unchanged. `MemoryFileSystem` gains `addSymlink(path, target)` (realpath, stat, isSymbolicLink, readFile follow it), needed for the requested symlink escape test.
2. confLocator, documentGlob, resource-policy take a `FileSystem`.
3. renderPipeline, renderWorker, hostEvents, webview and its two callers, plantUmlIncludes adapted.
4. NODE_DEBT: drop `fs` from the three entries.

## Risks
- Parity of the glob: `readdirSync` Dirent `isDirectory()/isFile()` are false for a symlink (links skipped), while the port's `readDirectory` reports the link target's kind, so a symlinked `.md` or folder would newly be listed or walked. Keep parity with `isSymbolicLink` per entry, or accept it (the policy still refuses an escape). Test it either way.
- `realFile`: stat follows links then realpath: same through the port. Root realpath failure keeps the `missing-root` diagnostic. Windows case: Node port uses the JS realpath, same as today.
- Render timing: awaits per file in includes, glob (400 directories, 200 matches, 2000 facts) vs sync. Batch independent calls; measure `renderMs` before and after.
- Races: `fileFacts` memo and include budget counters mutate across awaits: keep passes sequential per render. Conf locator `invalidate` while a lookup is in flight can write a stale entry: use a generation counter. Two conf events must not interleave in `onConfFileEvent`.
- Sanitizer pre-prime must cover every attribute the sanitizer resolves (src, srcset, poster, local href, stylesheet) or a legit image silently disappears (visible regression, not a security one). Cover with visual fixtures.
- No size or value that other code measures from changes; `path` import stays (path-facade CR).
- Project rules: SwRS markers move with the code (MYST-066, MYST-057, CORE-013, TRUST-025, TRUST-002); run `just requirements-update`; log entry in `requirements/tiers/log.md` only if an SwRS wording changes. `check-limits` file size (resource-policy is 467 l, may need a split) and `check-exports` (unused exports) apply.

## Questions only the user can answer
None. Design 1 vs 2 and symlink parity in the glob are technical (default: parity with today).

## Tests to add or change
- New `test/host-memory/memoryFileSystem.symlink.test.ts`: addSymlink, realpath, stat, isSymbolicLink, dangling link, link loop.
- `test/security/resource-policy.test.ts`, `readOnlyRoot.requirements.test.ts`, `trustReq.requirements.test.ts`, `html-policy.test.ts`: run the policy on MemoryFileSystem including a symlink escape (`symlink-escape` code); keep one Node-disk test with real symlinks (`needsSymlinks`).
- `test/core/myst/confLocator*.test.ts`: swap `readFile/statFile` stubs for MemoryFileSystem; keep cache and recheck cases (injected `now`).
- New documentGlob unit on MemoryFileSystem (limits, skipped dirs, dot files, excludePath, sorted).
- About 35 render tests go through `renderPreviewSource`/policy: adapt shared helpers (`test/session/mappedHtmlDom.ts`, `test/visual/renderFixtures.ts`); `test/node-services/renderWorker.test.ts` for the FileSystem in the worker.

## Evidence plan
Kind: internal refactor, behaviour unchanged; nothing visible in the UI (no screenshot).
- Logs in `work/gates/` or `evidence/*.log`: `just check-boundaries` (NODE_DEBT without `fs` for the three files; `grep node:fs` on the three files empty), `just check`, targeted unit suites, and the security suite showing the symlink-escape case passes on MemoryFileSystem and on Node disk.
- Parity: a script that renders the toctree-glob, include and conf.py fixtures through `renderPreviewSource` on base `origin/main` and on the branch, then `diff -r` of the generated HTML (proves same conf.py, same expansion, same resources).
- Timing: `renderMs` of the largest fixture, median of several runs, before and after.
- Gate: `just preflight` (static stage on Windows).
Cannot be shown: real VS Code integration and stress runs (CI only: `gh workflow run ci.yml --ref <branch> -f heavy=true`); symlink creation on Windows may need privileges (`needsSymlinks` skips).
