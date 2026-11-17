# Audit report: performance, security, modularity and maintainability

Audit 2026-10-27 of `markdown-okf-schema-studio` 0.3.1 (branch state at commit `e874e51b`).
Read-only: no repository file was changed, nothing installed, no VS Code window. Paths are
relative to the repository root. Every finding is **CONFIRMED** (code path read by the lead and,
where stated, measured) or **PLAUSIBLE** (consistent with the code, needs a test or a
measurement). Effort: S (under a day), M (days), L (a week or more). The scripts and raw numbers
are in [measurements/](./measurements/) (see its README).

Method: six focused sub-audits (security threat analysis, memory and lifecycle, render-path
design review, benchmarks, DOM-side inventory, modularity and supply chain), each finding then
re-read in the source by the lead before being kept. Findings the sub-audits raised that the code
did not support were dropped.

## 1. Performance

### Reference numbers (measured, `measurements/render/results.md`)

| document | parse | `renderMyst` | `renderPreviewDocument` | `annotateSourceMappings` | `rewriteSphinxHtml` | HTML out |
|---|---|---|---|---|---|---|
| 1.2k lines, 25 KB | 7 ms | 24 ms | 21-26 ms | 3 ms | 6-9 ms | 80 KB |
| 11k lines, 315 KB | 160 ms | 440-480 ms | 430-460 ms | 40 ms | 70 ms | 838 KB |
| 55k lines, 1.6 MB | 2,261 ms | 3,777 ms | 3,539 ms | 644 ms | 386 ms | 4.2 MB |
| 110k lines, 3.2 MB | 8,101 ms | | 13,501 ms | | | |

Typing at 11k lines (50 single-character edits, no debounce): 418 ms median per edit for the
render, about 518 ms with mapping and sanitising. Comment anchoring (`createDocumentIndex` 30 ms,
100 `reanchor` calls 15 ms at 55k lines) and `changedLineRanges` (0.5 ms) are not a concern.
Loading the extension bundle takes about 50 ms.

### P-01. One synchronous, uncancellable, full-document render per keystroke and per preview

- Severity: **high**. CONFIRMED (code and measurement).
- Evidence: `src/session/previewManager.ts:293-297` (`BuildQueue` per session, 40 ms debounce);
  `src/node-services/build/buildQueue.ts:129-131` ("an in-flight render is left alone");
  `src/core/render/renderPipeline.ts:258-260` (the abort signal is only read after the render);
  `src/session/hostEvents.ts:240-266` (one render per session of the same document); no
  visibility check before a render (only `restorePreviewState` reads visibility,
  `previewManager.ts:339-349`). Measured: 418 ms per edit at 11k lines, 3.5 s at 55k lines.
- Impact: the extension host (shared with every other extension) freezes for the render time
  after each pause in typing; at 10k+ lines typing feels blocked; with N previews of one document
  the cost is N x; hidden panels render as much as visible ones.
- Recommendation: (a) gate renders on panel visibility with a dirty flag flushed on
  `onDidChangeViewState` (M); (b) share one render result per `(document id, revision,
  options key)` across sessions (M); (c) move `renderMyst` + sanitising into a `worker_threads`
  worker with strings in and strings out, so an abort can terminate a stale render, and use an
  adaptive debounce such as `max(40, 2 x lastRenderMs)` (L). Core has no Node built-in on the
  render path except the `NODE_DEBT` list, which helps a worker build.

### P-02. `computeBlockTightness` of `markdown-it-myst` is half the parse time

- Severity: **high**. CONFIRMED (CPU profile, `measurements/README.md`).
- Evidence: `node_modules/markdown-it-myst/dist/directives.js:6-13` does `src.split('\n')` of the
  whole source for every directive fence; 5,058 ms self time of 10.4 s sampled at 55k lines
  (48.6%). Parse time grows 14x from 11k to 55k lines (5x the size).
- Impact: any document with many `{note}`, `{figure}`, `{code-block}`, `{mermaid}` fences pays
  O(directives x size) on every render.
- Recommendation: cache the line array on `state` (one split per parse) by a postinstall patch,
  the pattern of `scripts/patch-myst-imports.mjs`, and send the fix upstream. Effort S. Prove it
  with `measurements/render/bench-render.mjs` (expect parse at 55k lines to drop by about 2x).

### P-03. Five to seven redundant whole-page parse5 cycles per render

- Severity: **high**. CONFIRMED (code and measurement).
- Evidence: `src/session/webview.ts:211-215` runs `annotateSourceMappings`
  (`src/core/mapping/sourceMapping.ts:80`, parse + serialise, 644 ms at 55k lines) and then
  `rewriteSphinxHtml` whose `injectSourceMappings` (`src/core/security/html-sanitizer.ts:455,
  492`) writes the same attributes; `applyTableAlignments` re-parses the body for any table
  (`src/core/render/mystTables.ts:242-302`); `renderMathHtml` parses the full page when the
  document has math (`src/core/render/mathRenderer.ts:17-96`); `injectContentSecurityPolicy`
  parses and serialises to add one `<meta>` (`html-sanitizer.ts:518-537`); `planContentPatch`
  parses both the previous and the next page with `sourceCodeLocationInfo`
  (`src/core/preview/contentPatch.ts:67-70, 132-139`, called at
  `src/session/features/rendering.ts:475`), re-parsing the previous page on every render.
- Impact: at 55k lines about 1 s of the 4.2 s page build is spent re-parsing the same HTML.
- Recommendation: delete `annotateSourceMappings` (the sanitizer already does it), make the CSP
  injection a string splice, cache the previous page's shell key on the session, build shell and
  content separately so no analysis of the previous page is needed, apply table alignments on the
  tree instead of the HTML. Effort S to M. Prove with `bench-render.mjs` and the existing
  `test/core/render` contract tests.

### P-04. Per-block work is recomputed on every render

- Severity: **medium**. CONFIRMED (code); magnitude PLAUSIBLE.
- Evidence: `src/core/render/highlight.ts:273` (`hljs.highlight` per block, no cache);
  `src/core/render/mathRenderer.ts:52-58` (`katex.renderToString` per equation, no cache);
  `src/core/security/resource-policy.ts:193-196` (`statSync` + `realpathSync` per image, link and
  stylesheet, uncached); `src/core/render/mystGridToctree.ts:364` (each toctree entry's file is
  read on every render); `src/core/frontmatter/okfFrontmatter.ts:359-394` and
  `src/node-services/schemaFiles.ts:29-31` (schema directory listed with `statSync` per file on
  every analysis, which runs per render, per 300 ms refresh and per link enrichment).
- Impact: documents with hundreds of code blocks, equations or images pay the full cost after
  every keystroke; on network or Windows file systems the synchronous stats dominate.
- Recommendation: LRU caches keyed by `(language, body)` and `(displayMode, source)`; a stat and
  realpath cache per render (or per session, invalidated by the existing dependency watcher);
  memoise the schema directory listing for about 500 ms or by watcher event. Effort S each.

### P-05. Hidden webviews keep their full runtime alive

- Severity: **high** (memory with 10-50 previews). CONFIRMED (configuration); size PLAUSIBLE.
- Evidence: `src/host-vscode/activation.ts:74` and `:194` (`retainContextWhenHidden: true` on the
  custom editor and the side panel); `src/session/webview.ts:245-255` injects
  `mermaidPreview.js` (5.3 MB) and `plantumlPreview.js` (3.4 MB) when a diagram exists; page-side
  LRU caches of 64 SVG data URIs each (`src/page/modules/mermaidCache.ts:27`,
  `src/page/modules/plantumlDiagram.ts:210`).
- Impact: every hidden diagram-heavy preview keeps a parsed 5-8 MB engine, its DOM and caches,
  and still receives and applies every content patch (P-01).
- Recommendation: drop `retainContextWhenHidden` (state already survives through
  `vscode.setState` and `restorePreviewState`) or keep it for the N most recently visible panels.
  Effort M. Prove with the stress suite (`just ci-stress`) and a process-memory reading of the
  webview host with 20 hidden previews.

### P-06. Event fan-out scales with the number of previews

- Severity: **medium**. CONFIRMED (code).
- Evidence: `src/session/previewManager.ts:312` (a recursive `**/*` watcher per session, on the
  workspace folder, or on the document's folder for read-only previews, possibly `~`);
  `src/session/hostEvents.ts:210-266` (`onDocumentChanged` handles every text document with no
  scheme or language filter and runs `refreshReferencedPath` for every other session, each with
  `realpathSync` calls, `buildQueue.ts:105-113`); `hostEvents.ts:172-183` (the stem index is
  invalidated on `onDidChange` too, so saving any `.md` triggers a full `readdirSync` rebuild on
  the next link resolution, `src/core/frontmatter/stemIndex.ts`); `src/session/features/links.ts:
  171-178` (`findFiles("**/name")` without `exclude` or `maxResults`); `src/session/features/
  frontmatter.ts:114-143` plus `src/node-services/linkedTargetWatch.ts:54` (one VS Code watcher,
  three subscriptions and one `fs.watch` per linked target per preview, not shared, not capped).
- Impact: with 50 previews, typing in any file costs about 100 synchronous syscalls per keystroke;
  a `git checkout` delivers every file event 50 times; 50 previews with 50 links each create about
  2,500 watchers.
- Recommendation: early return in `onDocumentChanged` unless the path is in a precomputed canonical
  dependency `Set`; one shared watcher per root with refcounts; invalidate the stem index on create
  and delete only; pass excludes and `maxResults` to `findFiles`; cap and share linked-target
  watches. Effort S to M. Prove with `measurements/leaks/churn.js` extended with a document-change
  loop (count syscalls or time per change).

### P-07. The page patch rebuilds the whole tail on any line-count change

- Severity: **medium**. CONFIRMED (code).
- Evidence: the morph key is the block's HTML with only auto link titles removed
  (`src/page/modules/contentMorph.ts:44-53`), and that HTML carries `data-line`,
  `data-sphinx-source-line`, `data-sphinx-source-end-line` and `data-sphinx-preview-block=
  "source-block-N"` from `injectSourceMappings`; the host posts the full `contentHtml` each time
  (`src/session/features/rendering.ts:343-361`, limit 20 MB `src/core/preview/contentPatch.ts:
  30`); `initializeContent` re-runs every whole-document pass after each patch, including the
  re-creation of all insert points (`src/page/features/contentPatch.ts:96-138`,
  `src/page/features/insertPoints.ts:52-91`); `morphKey` serialises `outerHTML` of every incoming
  and every recorded node per patch (`contentMorph.ts:70, 82`).
- Impact: pressing Enter at the top of a 10k-block document replaces every block below (new DOM,
  image decode, Mermaid redraw except for the source cache), then runs O(blocks) init passes.
- Recommendation: strip the line and block attributes from the key and patch them in place on
  kept nodes (M); send only changed top-level children (the page already keys them) (M); make
  insert-point creation incremental and store a hash instead of `outerHTML` as the key (S).
  Prove with `test/page/runtimeContentPatch.test.ts` counting kept nodes after a line insert.

### P-08. Page layout work is not coalesced

- Severity: **medium**. CONFIRMED (code); cost PLAUSIBLE.
- Evidence: `src/page/features/scrollCore.ts:394-427` (`stabilizeLayout` schedules its own
  `requestAnimationFrame` per call and runs `markWideTables`, which writes attributes then reads
  `scrollWidth` per table at `:377-392`, then a full `measure()`); it is called from every image
  `load` and `decode()` (`src/page/features/contentPatch.ts:108-109`), window resize and a
  `ResizeObserver` (`scrollCore.ts:539-545`); `src/page/modules/codeCopy.ts:191-195` runs
  `place()` (three rect reads, two `querySelector`, style writes) on every scroll event without
  rAF; `src/page/features/stickyHeadings.ts:46-58, 161-178` reads and writes per scroll frame;
  `src/page/features/mappedBlocks.ts:17-39` rebuilds and sorts the block list on each key or
  click event; `src/page/features/blockSourceEditor.ts:114-117` forces a layout per keystroke
  (`height = auto` then `scrollHeight`).
- Impact: a document with hundreds of images triggers up to 2N full re-measures with write-then-
  read thrash after each patch; scrolling a large page does layout per event.
- Recommendation: a single pending-frame flag in `stabilizeLayout`; rAF-throttle `codeCopy.place`;
  cache `topLevelMappedBlocks` per content generation; resize the textarea only when the line
  count changes or use `field-sizing: content`. Effort S each. Prove with the visual suite's
  Playwright timing of a 500-image fixture.

### P-09. Sanitizer: quadratic sibling removal and recursion depth

- Severity: **medium** (also a denial-of-service surface, see S-09). CONFIRMED (measured).
- Evidence: `src/core/security/html-sanitizer.ts:262-266` (`removeNode` filters
  `parent.childNodes` per removal): 5k unknown tags 109 ms, 20k 1,260 ms, 50k 39.2 s; the
  recursive walk overflows the stack at 5,000 nested `<ul>`.
- Recommendation: collect removals per parent and rebuild `childNodes` once, or iterate with an
  explicit stack and a depth cap that truncates with a diagnostic. Effort S. Prove with
  `measurements/render/bench-sanitizer2.mjs` and a security test.

### P-10. PlantUML JAR mode: one JVM per diagram per render, no cache

- Severity: **high when `plantuml.useJar` is on** (off by default). CONFIRMED (code).
- Evidence: `src/core/render/plantUmlRenderer.ts:208` (spawn per source) and `:343`
  (`Promise.all` over all diagrams); no SVG cache; the data URI inflates the SVG by about 3x in
  each session's page (`:375`). Superseded runs are killed with the stage
  (`renderPipeline.ts:176-179`), so processes do not leak.
- Recommendation: cache SVG by `(source, engine, jar)` hash, a global concurrency limit of 1-2,
  and a long-lived `-pipe` JVM. Effort M.

### P-11. Built-in PlantUML queue never drops superseded work

- Severity: **medium**. CONFIRMED (code).
- Evidence: `src/page/modules/plantumlDiagram.ts:346-349` (serial promise chain) and `:393`
  (the stale check happens after the engine ran).
- Impact: typing in a `{uml}` block queues one engine run per patch; the backlog grows with typing
  speed and holds every intermediate source and SVG.
- Recommendation: before `run`, skip when no live element wants the key; keep one pending run per
  element. Effort S.

### P-12. Front matter and source passes repeated per edit

- Severity: **low-medium**. CONFIRMED (code).
- Evidence: YAML is parsed four times per edit: `stripFrontmatter` runs a full `parseDocument`
  only to decide whether to strip (`src/core/frontmatter/frontmatterParse.ts:54-84`,
  `src/core/render/mystRenderer.ts:454-461`), `analyzeFrontmatter` in `updatePreview`
  (`rendering.ts:418`), the 300 ms refresh (`features/frontmatter.ts:213-240`) and the 150 ms
  link enrichment (`:203`); `prepareDollarAmounts` is a char-by-char string concatenation over the
  whole text when the document has a `$` (`src/core/render/mystInlineTransforms.ts:366-400`);
  the "grids" pass splits `parsedText` even without a grid (`mystRenderer.ts:311`);
  `resolveAnchorIds` runs `html.includes` per anchor (`mystInlineTransforms.ts:104-108`).
- Recommendation: `matchFrontmatterBlock` in `stripFrontmatter`; one parsed front matter per
  `(document, revision)` shared by the three consumers; early exits for the grid and dollar passes.
  Effort S.

### P-13. Bundle weight and shipped artefacts

- Severity: **low-medium**. CONFIRMED (metafile, `vsce ls`).
- Evidence: `extension.js` 1.8 MB carries katex 263 KB, highlight.js 118 KB, parse5 125 KB and two
  YAML libraries (yaml 112 KB, js-yaml 44 KB, json5 29 KB), `he` 85 KB and csv-parse 51 KB; the
  6.5 MB `extension.js.map` with `sourcesContent` is in the VSIX (`.vscodeignore` has no `*.map`
  rule), as are `docs/*.md` (internal feasibility and evidence notes), `.claude/` and
  `pyproject.toml`; `mermaidPreview.js` bundles a second katex (267 KB) and elkjs (1.4 MB).
- Recommendation: exclude `**/*.map`, `docs/**` (or move user docs), `.claude/**` and
  `pyproject.toml` in `.vscodeignore` (S); lazy `import()` of katex and highlight.js on first use
  (S-M); check what pulls `he`, `csv-parse` and `js-yaml` (S); an ES-module Mermaid build with
  code splitting so only used diagram types load (M).

### P-14. Smaller items

- `src/core/mapping/lineDiff.ts:9-32`: the Myers trace keeps up to 2000 x `Int32Array(4000)`
  (about 32 MB transient) every 300 ms per preview with incoming changes on. Low. S.
- `src/session/features/blockEdits.ts:277-298` with `src/core/mapping/sourceMapping.ts:44-49`:
  `lineStarts` of the whole document rebuilt on each autosave. Low. S.
- `src/session/features/flushWait.ts:17-33`: `waitForSettled` polls every 5 ms for up to 1.5 s.
  Low. S.
- `src/session/features/scrollSync.ts:148-155`: `sourceScroll` posted per visible-range change
  without host-side throttling (the page coalesces). Low.

### Good designs to keep

Lazy activation events and an async engine preload (`src/core/render/mystEngine.ts:23-57`); the
edit path applies one minimal `TextEdit` and the preview's own edits do not re-render
(`hostEvents.ts:245-247`); keyed top-level morph keeps unchanged nodes; Mermaid and PlantUML LRU
caches; comment and incoming-change posts are hash-gated; `BuildQueue` coalesces to the latest
request; Ajv validators cached per schema (`src/core/frontmatter/schemaValidator.ts:17-24`);
scroll messages rAF- and time-throttled; `bibScan` and `documentGlob` bounded; the page bundle is
301 KB with no highlight.js; diagram engines load only when a diagram exists; `conf.py` lookup
cached 2 s; every host cache is bounded (`BoundedMap` 200, HEAD baseline 64 x 1 MB, navigation
history 50, include watch 1024).

## 2. Security

### S-01. Percent-encoded scheme reaches `openExternal` as a `file:` URI

- Severity: **high**. PLAUSIBLE (classification confirmed by probe; the launch needs a VS Code
  test).
- Evidence: `src/core/navigation/previewNavigation.ts:134-141` checks the scheme of the
  **decoded** path but returns the **raw** string (`value: trimmed`); the same pattern is in
  `src/core/security/resource-policy.ts:238-241`; `src/session/features/links.ts:258-259` calls
  `host.navigation.openExternal(navigation.value)`; `src/host-vscode/vscodeHost.ts:226` is
  `vscode.env.openExternal(vscode.Uri.parse(url))`. Probe:
  `classifyPreviewReference("https%3A/../../System/Applications/Calculator.app")` returns
  `{kind: "external", value: "https%3A/../../..."}`, and the Markdown link survives the pipeline
  with `data-sphinx-preview-navigation`. `Uri.parse` sees no scheme before the first `/` and
  defaults to `file:`; the dot segments are then normalised by the URL layer.
- Impact: one click on a link in an untrusted Markdown file opens a local file or application with
  the OS handler, Restricted Mode included (`handleLink` has no read-only check).
- Recommendation: in the host, `const u = vscode.Uri.parse(value, true)` and require
  `u.scheme` in `{http, https, mailto}` immediately before `openExternal`; also check the scheme
  on the raw string, or refuse `%` before the first `:`. Effort S. Prove with a unit test on
  `classifyPreviewReference` and an integration test that asserts `openExternal` is never called
  with a `file:` URI.

### S-02. The resource and include root is the document's folder for read-only previews

- Severity: **medium**. CONFIRMED.
- Evidence: `src/session/previewManager.ts:252-254` (`resourceRoot = readOnly ? documentDirectory
  : workspaceFolder.path`), used as `localResourceRoots` (`rendering.ts:410`) and as the include
  policy root (`src/core/render/renderPipeline.ts:182-185`).
- Impact: opening `~/notes.md` without a workspace, or any file in Restricted Mode, makes the
  whole folder (possibly `$HOME`) readable: `{include} .ssh/id_rsa` renders the key, and the
  webview can load any file under it. No network exfiltration (`connect-src 'none'`), so this is
  local exposure plus S-01 or a screenshot.
- Recommendation: refuse includes and narrow the resource root when the folder is `$HOME`, a
  file-system root or a drive root; deny dot-directories (`.ssh`, `.aws`, `.gnupg`, `.config`).
  Effort S. Prove with a unit test of the policy roots.

### S-03. The PlantUML JAR runs without a security profile

- Severity: **medium** (trusted workspaces only). CONFIRMED.
- Evidence: `src/core/render/plantUmlRenderer.ts:208-213, 328-340` spawn `java -jar <jar> -pipe
  -tsvg` or `plantuml -pipe -tsvg` with no `PLANTUML_SECURITY_PROFILE` and no `-DPLANTUML_LIMIT_
  SIZE` (grep of `src/` and `package.json` is empty). `shell: false` and JAR mode refused when
  untrusted are correct (`src/node-services/processRunner.ts:20`, `plantUmlRenderer.ts:313-319`).
- Impact: a document's `!include /etc/passwd` or `!includeurl http://...` reads any absolute path
  or reaches the network (SSRF) through the JVM.
- Recommendation: set `PLANTUML_SECURITY_PROFILE=ALLOWLIST` (or `INTERNET` with an allowlist of
  the workspace) in the spawn environment and `-DPLANTUML_LIMIT_SIZE`. Effort S. Prove with a
  `processRunner` stub test asserting the environment.

### S-04. The comments sidecar write follows a dangling symlink

- Severity: **medium** (trusted workspaces only). CONFIRMED in code; effect untested.
- Evidence: `src/session/features/comments.ts:75-77` derives the sidecar path, `:85-87` writes it
  through `host.files.writeFile` with no `lstat`; an invalid or missing file reads as `undefined`
  (`src/core/comments/commentStore.ts:64-67`).
- Impact: a repository can ship `doc.comments.json` as a symlink to `~/.zshenv` or a LaunchAgents
  path; the first comment creates or overwrites the target with JSON whose quoted text the
  attacker's document controls.
- Recommendation: `lstat` and refuse symlinks (or realpath-check the parent as the image paste
  does, `src/session/features/hostRequests.ts:283-318`) and write through the temp-file-and-
  rename helper. Effort S.

### S-05. The sanitizer keeps `<script src>` with the page nonce in trusted previews

- Severity: **medium** (latent). CONFIRMED.
- Evidence: `src/core/security/html-sanitizer.ts:263-282` keeps a script whose `src` resolves
  inside the roots and sets `nonce` to the page nonce; `"nonce"` is in the attribute allowlist
  (`:79`); `allowExternalScripts = !preview.readOnly` (`src/session/features/rendering.ts:454`).
  It is unreachable today only because `myst-to-html` drops raw `<script>` first (14 probes found
  no bypass).
- Impact: any future HTML pass that re-emits raw HTML (the kbd, span, image and table passes
  already do, selectively) would execute workspace JavaScript in the preview with full message-
  channel access.
- Recommendation: always remove `<script>` in the live preview, drop `nonce` from the allowlist,
  add a regression test with a raw `<script src>`. Effort S.

### S-06. What a script in the page could still do

- Severity: **low-medium**. CONFIRMED.
- Evidence: the gates (`src/session/pageMessages.ts:45-90`) stop stale messages, not a script
  that knows the boot context; `previewPlantUmlInclude` accepts a page-supplied absolute `from`
  and reads up to 5 MB inside the roots without checking that the built-in engine is active
  (`src/session/features/plantUml.ts:125-135`, `src/core/render/plantUmlIncludes.ts:86-96`);
  `previewCopyText` writes the clipboard without a user gesture, even read-only
  (`src/session/features/hostRequests.ts:148-157`); `previewBlocksPaste` reads the clipboard into
  the document (`src/session/features/sourceEdits.ts:421`); `previewLinkDiscover` probes file
  existence (64 per request). No `executeCommand` takes page arguments; pasted images are
  magic-sniffed, capped at 10 MB and canonical-checked.
- Recommendation: gate `previewPlantUmlInclude` on the built-in engine and on ids the host
  issued; require a recent user-gesture flag for `previewCopyText`. Effort S-M.

### S-07. Frontmatter path settings are not restricted

- Severity: **low**. PLAUSIBLE.
- Evidence: `frontmatter.bundleRoot`, `frontmatter.projectRoot` and
  `frontmatter.allowOutsideWorkspaceLinks` (`package.json:197-213`) widen link resolution and
  target reads but are absent from `capabilities.untrustedWorkspaces.restrictedConfigurations`
  (`package.json:30-33`). Schema resolution is off in read-only mode (`features/frontmatter.ts:
  78`); whether link enrichment also stops was not confirmed.
- Recommendation: add the three to `restrictedConfigurations`. Effort S.

### S-08. KaTeX style declarations copied unescaped into the nonce stylesheet

- Severity: **low**. PLAUSIBLE.
- Evidence: `src/core/render/mathRenderer.ts:23-37, 85-89` copies `style` attribute values into
  `.cls{decl}` as is; safe today only because KaTeX (`trust: false`, `:54`) validates its values.
- Recommendation: reject declarations containing `{`, `}`, `<` or `@`. Effort S.

### S-09. Sanitizer denial of service

- Severity: **medium**. CONFIRMED (measured, see P-09).
- A document with 50k raw unknown tags freezes the extension host for 39 s on every render; a
  5,000-deep nesting throws and the preview falls back. Fix with P-09.

### S-10. Supply chain and packaging

- Severity: **low-medium**. CONFIRMED.
- `npm audit --offline` reports nothing because it has no advisory data; no online audit runs in
  CI (`.github/workflows/ci.yml`). Lock file: 502 entries, 245 runtime, all on
  registry.npmjs.org with integrity hashes, no git or file dependencies. Recommendation: an
  `npm audit --audit-level=high` step (or Dependabot) in `ci-static`. S.
- GitHub Actions are pinned by tag, not SHA (`actions/*@v4`, `astral-sh/setup-uv@v5`,
  `extractions/setup-just@v2`, `softprops/action-gh-release@v2`); `release.yml:20-21` grants
  `contents: write` to the whole workflow, including the `package` job that runs `npm ci` with
  install scripts; `pages.yml:58` installs unpinned apt packages. Recommendation: SHA pins,
  per-job permissions, `--ignore-scripts` where the postinstall is not needed. S.
- The VSIX ships `out/bundle/extension.js.map` (6.5 MB, `sourcesContent` of 700 sources, 144 of
  them project files), internal `docs/*.md`, `.claude/skills/`, `pyproject.toml` and
  `sphinx/*.py` (`.vscodeignore`, `vsce ls`: 131 files, about 20 MB). Information disclosure of
  internal notes, not a vulnerability. Recommendation: `.vscodeignore` entries. S.
- `scripts/patch-myst-imports.mjs` (postinstall) rewrites two files in `node_modules` to keep
  `myst-to-html@1.7.4` working on `markdown-it` 14 (forced by the `overrides`,
  `package.json:296`); it hard-fails on any version drift of `myst-to-html` (`^1.7.4`,
  `package.json:290`) and is skipped by `--ignore-scripts`. Recommendation: pin exact versions or
  replace by an esbuild alias or `patch-package`. S-M.
- `plantuml.jarPath` accepts any file and `java` is resolved with `cwd = workspaceRoot` (on
  Windows libuv searches the cwd first) (`plantUmlRenderer.ts:145-159`). Trusted only. Low. S.
- Duplicate runtime copies: katex 0.19.0 and 0.18.10 (under mermaid), parse5 8.0.1 and 6.0.1,
  marked 16.4.2 and commander 15 nested. Low.

### What is sound

CSP `default-src 'none'`, `script-src`/`style-src` = cspSource + nonce, `connect-src`,
`frame-src`, `object-src`, `worker-src`, `base-uri`, `form-action` all `'none'`, `img-src`
cspSource + `data:` (`src/core/security/csp.ts:9-25`); nonce from `randomBytes(18)`, fresh on
every full load, every injected script and style carries it; `enableCommandUris` never set; the
boot JSON escapes `<`; two sanitising layers (myst-to-html then the parse5 allowlist), no bypass
in 14 payloads; Mermaid `securityLevel: "strict"` and both diagram engines output `<img
src="data:">`, never `innerHTML`; `Object.hasOwn` validator lookup and a gate per message type;
origin check on the page (`src/page/hostTransport.ts:49-61`); every write handler checks
`readOnly`; `useJar`/`jarPath` are restricted configurations; the include policy allows relative
paths only, decodes up to four times, rejects NUL and backslash, realpath-checks containment and
caps 5 MB per file, 2,000 expansions, 10 Mi chars; the comments sidecar is size-capped before
reading and rebuilt field by field (no prototype pollution); no `eval`, `new Function` or
`document.write` anywhere; every `innerHTML` site on the page takes host-sanitised or constant
markup.

## 3. Modularity

### M-01. The session to node-services debt is wider than its exception list

- Severity: **medium**. CONFIRMED.
- Evidence: `.dependency-cruiser.cjs` `SESSION_NODE_SERVICES_DEBT` lists three files, but the
  sites are `src/session/previewManager.ts:12` (the concrete `BuildQueue` class, a value import)
  and `:25` (`canonicalPath`, `sourceExists`), `src/session/hostEvents.ts:29`,
  `src/session/features/comments.ts:28`, `src/session/features/sourceEdits.ts:26`,
  `src/session/workspaceChoices.ts:13` (`osUserName`), `src/session/features/rendering.ts:8`,
  `src/session/features/frontmatter.ts:10` (`watchLinkedTargetDirectly`).
- Impact: the session layer cannot run on the memory host without Node, which blocks the headless
  host the architecture promises and a worker-based renderer (P-01).
- Recommendation: add `realpath`, `exists` and `userName` to the `WorkspaceInfo` or `FileSystem`
  port, a render-queue factory and a linked-target-watch port on `HostServices`. Effort M.

### M-02. Import cycles and hub modules

- Severity: **medium**. CONFIRMED (`measurements/modularity/graph*.mjs`).
- Evidence: one value-import cycle, `src/core/frontmatter/fileLinks.ts:5` <->
  `src/core/frontmatter/okfFrontmatter.ts:21`; three type-only strongly connected components
  (the 18-file session set around `PreviewSession`, the 7 edit-action modules of `src/page/
  modules/`, `editPalette.ts` <-> `editPalettePopovers.ts`). Hubs: `src/page/features/
  pageRuntime.ts` (fan-in 20, fan-out 42, 39 exports, 610 lines) and `src/session/
  previewManager.ts` (16 / 36, `createSession` alone is 140 lines at `:234-372`).
- Recommendation: extract shared types (`fileLinkTypes.ts`, `SessionContext`,
  `pageRuntimeTypes.ts`); extract a `SessionFactory` from `previewManager.ts`. Effort S to M.

### M-03. Files near the 800-line ratchet mix responsibilities

- Severity: **medium**. CONFIRMED.
- Evidence: nine files between 700 and 782 lines. `src/page/modules/editPalette.ts` (782) holds
  popover lifecycle, command execution, availability, tooltips, mode, menu entries and the DOM
  build in one closure; `src/page/modules/markdownTable.ts` (755) is parser, operations,
  serialiser and conversions (20 non-null assertions); `src/session/features/rendering.ts` (747)
  is the controller plus patch planning, overlay, full-load fallback and ready report;
  `src/core/frontmatter/fileLinks.ts` (718) mixes link parsing with synchronous resolution (the
  `NODE_DEBT` part); `src/core/protocol/pageToHost.ts` (712) holds 40+ message interfaces and the
  validators.
- Recommendation: split by responsibility before the ratchet forces an ad hoc split; `fileLinks`
  into parse (pure) and resolve (fs) isolates the Node debt. Effort M each.

### M-04. Duplicated syntax primitives with divergent behaviour

- Severity: **medium**. CONFIRMED.
- Evidence: the code-fence regex exists five times with different indent rules
  (`src/core/mapping/mystTargets.ts:30`, `src/core/comments/anchoring.ts:141`,
  `src/core/navigation/previewNavigation.ts:50`, `src/core/render/mystGridToctree.ts:324`,
  `src/core/render/mystGithubAlerts.ts:27` with unbounded `\s*`, which treats a 4-space indented
  block as a fence); front-matter end detection five times (`src/core/render/mystSyntaxDetect.ts:
  71`, `anchoring.ts:166-170`, `mystGridToctree.ts:317`, `src/page/modules/figureDirective.ts:
  123`, `markdownTable.ts:427-429, 528`), only two accepting the `...` end marker; `escapeHtml`
  three times (`src/core/preview/previewStatus.ts:35`, `src/core/frontmatter/propertiesTable.ts:
  16`, `src/core/render/highlight.ts:165`); `escapeRegExp` twice (`previewNavigation.ts:86`,
  `src/core/mapping/labelRename.ts:60`).
- Impact: the preview, comment anchoring and navigation can disagree on where a fence or the
  front matter ends.
- Recommendation: one `FENCE_OPEN`, one `frontmatterRange(lines)`, one `escapeHtml` and
  `escapeRegExp` in `src/core/`. Effort S-M. Prove with a shared table test.

## 4. Maintainability

### N-01. No logging port; fire-and-forget promises without a catch

- Severity: **medium**. CONFIRMED.
- Evidence: 8 `console.error` calls in `src/session/` (`workspaceChoices.ts:75, 124, 155`,
  `features/comments.ts:345, 371`, `hostEvents.ts:283`, `features/incomingChanges.ts:92`,
  `previewManager.ts:443`); 74 `void fn(...)` statements in `src/` against 12 `.catch(`
  (top: `features/comments.ts` 7, `features/blockEdits.ts` 7, `workspaceChoices.ts` 6,
  `hostEvents.ts` 6). The `Diagnostics` port is for document problems, not logs.
- Impact: errors reach neither the Output channel nor tests; a rejected `void` promise becomes an
  unhandled rejection.
- Recommendation: a `Logger` port on `HostServices` (OutputChannel in VS Code, array in the memory
  host) and a `fireAndForget(promise, label)` helper routed to it. Effort S, then M to roll out.

### N-02. Test structure and flakiness hot spots

- Severity: **medium**. CONFIRMED.
- Evidence: `test/integration/realInput.test.ts` is 4,580 lines (the only ratchet exception), 92
  scenario functions and 508 timing-keyword hits (33 literal `setTimeout`/`waitForTimeout`); five
  test files within 20 lines of the 1,500 limit (`scenarioDefinitions2.ts` 1,494,
  `okfFrontmatter.test.ts` 1,484, `editActions.test.ts` 1,482, `previewEditing.test.ts` 1,452);
  `test/integration/standalone-suite.ts:45` creates its fixture in `os.homedir()` (also
  `imagePicker.test.ts:36-37`); the unit globs in `package.json` `test:unit` are fixed-depth
  (`out/test/core/*/*.test.js`), so a test three levels deep is silently skipped; the stress job
  is advisory (`ci.yml:159`, `continue-on-error`) and there is no retry mechanism, so flakes fail
  loudly (good). Suite sizes: core 96 files / 855 cases, page 79 / 1,127, session 22 / 129,
  security 6 / 47, integration 44 files.
- Recommendation: split `realInput.test.ts` by feature into `test/integration/realInput/*.ts`
  with a thin runner (L, mechanical); use `os.tmpdir()` for the fixtures (S); recursive globs or
  a guard test (S).

### N-03. Fragile postinstall patch

- Severity: **medium**. CONFIRMED. See S-10. A `^1.7.4` bump of `myst-to-html` breaks `npm ci`
  for everyone, and `--ignore-scripts` yields a runtime import error. Effort S-M.

### N-04. Typing gaps

- Severity: **low**. CONFIRMED.
- Evidence: `any` only in the paste modules (`src/page/modules/pasteImage.ts:55, 58, 71`,
  `pasteHtml.ts:19, 21`, untyped clipboard events); 20 `as unknown as` (mostly mdast nodes;
  `src/core/protocol/router.ts` has one on the message path); non-null assertions concentrated in
  `src/page/features/tableCellEditor.ts` (33) and `markdownTable.ts` (20);
  `src/page/bootContext.ts:10` casts `JSON.parse` of the boot context without a guard; `src/core/
  frontmatter/okfFrontmatter.ts:172-180` casts a user schema file to `Record<string, unknown>`.
  No `@ts-ignore` or `@ts-expect-error` anywhere.
- Recommendation: `ClipboardEvent` types, a `must(el)` helper, a guard on the boot context. S.

### N-05. Small lifecycle defects

- Severity: **low**. CONFIRMED (measured).
- `src/session/features/comments.ts:356-358` discards the three `watcher.onDid*` disposables
  (only the watcher is disposed): 3 leaked closures per sidecar switch on hosts that do not
  release listeners with the watcher (`measurements/leaks/churn.js`: +150 subscriptions per 50
  closes). `frontmatter.ts:134` does it right. S.
- `src/page/modules/linkNavigation.ts:83-105`: `rescan` observes new links but does not
  unobserve detached ones (only `refresh` does). S.
- `src/session/workspaceChoices.ts:52`: `dismissedWarningBanners` is an unbounded `Map`
  (tiny values). S.

### N-06. Over-exported surface

- Severity: **low**. CONFIRMED (`measurements/modularity/dead.mjs`).
- About 190 exported types and interfaces are used only in their own file, and seven exported
  functions are used only locally (`src/core/preview/pageBuildEntry.ts:11`,
  `src/core/security/html-sanitizer.ts:613`, `src/node-services/build/snapshotWorkspace.ts:449`,
  `src/node-services/build/sphinxBuild.ts:356`, `src/core/state/previewViewPreferences.ts:25`,
  `src/core/protocol/hostToPage.ts:272`, `src/core/comments/commentModel.ts:42`). The Sphinx
  build (`sphinxBuild.ts`) is not wired into the live preview at all (bundle has no
  `sphinx-build` string), yet is kept with its tests. Recommendation: an unused-exports check in
  `just check`, and a decision on the Sphinx build path. S.

## 5. Proposed change requests

One line each: title; scope; files; suggested priority; how to prove it.

**Security**

1. **Scheme re-check before `openExternal`**; reject encoded-scheme links on both the raw string
   and the parsed URI; `src/core/navigation/previewNavigation.ts`, `src/core/security/
   resource-policy.ts`, `src/host-vscode/vscodeHost.ts`, `src/session/features/links.ts`; **P1**;
   unit test on `classifyPreviewReference("https%3A/..")` = blocked, integration test that
   `openExternal` never receives a `file:` URI.
2. **Narrow the read-only resource root**; refuse `$HOME`, FS roots and dot-directories as
   include/resource roots; `src/session/previewManager.ts`, `src/core/security/resource-policy.ts`;
   **P2**; policy unit tests with a document in `$HOME`.
3. **PlantUML JAR security profile and limits**; `PLANTUML_SECURITY_PROFILE`, `-DPLANTUML_LIMIT_
   SIZE`, explicit `java` resolution; `src/core/render/plantUmlRenderer.ts`; **P2**; spawn-stub
   test on env and args.
4. **Symlink-safe sidecar write**; `lstat` + atomic rename; `src/session/features/comments.ts`,
   `src/core/comments/commentStore.ts`; **P2**; test with a dangling symlink in the memory FS.
5. **Sanitizer hardening**; drop `<script>` always in the live preview, remove `nonce` from the
   allowlist, linear `removeNode`, depth cap, KaTeX style validation; `src/core/security/
   html-sanitizer.ts`, `src/core/render/mathRenderer.ts`; **P2**; security tests + `bench-
   sanitizer2.mjs` (50k removals under 500 ms, depth 10k no throw).
6. **Restricted-mode settings and page-callable capabilities**; add the frontmatter path settings
   to `restrictedConfigurations`, gate `previewPlantUmlInclude` on the engine and host-issued
   ids, user-gesture flag for `previewCopyText`; `package.json` (via `generate-settings`),
   `src/session/features/plantUml.ts`, `hostRequests.ts`; **P3**; validator and gate tests.
7. **Supply-chain CI**; online `npm audit` step, SHA-pinned actions, per-job permissions,
   `--ignore-scripts` where possible; `.github/workflows/*.yml`, `justfile`; **P3**; CI green with
   the new step.
8. **VSIX contents**; exclude `**/*.map`, `docs/**` (or keep `docs/user/` only), `.claude/**`,
   `pyproject.toml`; `.vscodeignore`; **P3**; `vsce ls` shows under 15 MB and no `.map`.

**Performance**

9. **Patch `computeBlockTightness`**; cache the split lines per parse; `scripts/patch-myst-
   imports.mjs` (plus an upstream PR to `markdown-it-myst`); **P1**; `bench-render.mjs` parse at
   55k lines at least 2x faster, contract tests unchanged.
10. **One parse5 pass per page build**; delete `annotateSourceMappings`, string-splice the CSP,
    cache the shell key, tree-level table alignment; `src/session/webview.ts`, `src/core/mapping/
    sourceMapping.ts`, `src/core/security/html-sanitizer.ts`, `src/core/preview/contentPatch.ts`,
    `src/core/render/mystTables.ts`; **P2**; `bench-render.mjs` page build at 55k lines
    down by about 1 s, contract tests unchanged.
11. **Visibility-gated and shared renders**; dirty flag per hidden panel, one render per
    `(document, revision, options)`; `src/session/previewManager.ts`, `src/session/hostEvents.ts`,
    `src/session/features/rendering.ts`; **P2**; `previewManager.test.ts` counts renders with two
    sessions of one document (1) and a hidden panel (0 until shown).
12. **Drop `retainContextWhenHidden`**; rely on `setState` and `restorePreviewState`;
    `src/host-vscode/activation.ts`; **P2**; reload suite and stress suite green, webview host
    memory with 20 hidden previews measured before and after.
13. **Worker-thread renderer with cancellation and adaptive debounce**; `src/node-services/build/
    buildQueue.ts`, `src/core/render/renderPipeline.ts`, a new `src/node-services/renderWorker.ts`;
    **P3** (after 9-11); `bench-typing.mjs` shows the host thread free during a render; abort test.
14. **Content-addressed caches**; highlight, KaTeX, stat/realpath per render, toctree reads,
    schema listing; `src/core/render/highlight.ts`, `mathRenderer.ts`, `src/core/security/
    resource-policy.ts`, `src/core/render/mystGridToctree.ts`, `src/core/frontmatter/
    okfFrontmatter.ts`; **P3**; `bench-typing.mjs` second render of an unchanged document under
    50% of the first.
15. **PlantUML JAR cache and concurrency**; SVG cache by hash, limit 2 JVMs, optional long-lived
    pipe; `src/core/render/plantUmlRenderer.ts`; **P3**; spawn-stub test counting spawns across
    two renders of the same source (second: 0).
16. **Stable morph keys and incremental init**; keys without line attributes, hash keys,
    incremental insert points, single-flight `stabilizeLayout`, rAF-throttled `codeCopy.place`;
    `src/page/modules/contentMorph.ts`, `src/page/features/contentPatch.ts`, `insertPoints.ts`,
    `scrollCore.ts`, `src/page/modules/codeCopy.ts`; **P3**; `runtimeContentPatch.test.ts` keeps
    all blocks below an inserted line.
17. **Event fan-out**; canonical dependency `Set` and early return in `onDocumentChanged`, one
    shared watcher per root, stem index on create/delete only, `findFiles` excludes, capped and
    shared linked-target watches; `src/session/hostEvents.ts`, `previewManager.ts`, `features/
    links.ts`, `features/frontmatter.ts`; **P3**; `churn.js` extended: time per foreign document
    change with 50 sessions.
18. **Page PlantUML queue drops superseded runs**; `src/page/modules/plantumlDiagram.ts`; **P4**;
    page test: 10 patches of one block run the engine at most twice.
19. **Front matter parsed once per revision**; `src/core/render/mystRenderer.ts`, `src/session/
    features/rendering.ts`, `frontmatter.ts`; **P4**; unit test counting `parseDocument` calls.
20. **Bundle trims**; lazy katex and highlight.js, one YAML library, split Mermaid build; `esbuild.
    mjs`, `scripts/page-bundle.mjs`, `package.json`; **P4**; `bundle-meta.mjs` sizes.

**Modularity and maintainability**

21. **Logger port and `fireAndForget`**; `src/host-api/`, `src/host-vscode/vscodeHost.ts`,
    `src/host-memory/`, the 8 `console.error` and 74 `void` sites; **P3**; memory-host test
    asserting a rejected handler is logged, `grep console.` in `src/` empty.
22. **Shared syntax primitives**; `FENCE_OPEN`, `frontmatterRange`, `escapeHtml`, `escapeRegExp`
    in `src/core/`; the five fence sites, five front-matter sites, three/two escape sites; **P3**;
    one table test shared by anchoring, navigation and rendering.
23. **Retire the session to node-services debt and break the `fileLinks` cycle**; ports for
    realpath/exists/userName, render queue, linked-target watch; `fileLinkTypes.ts`; `.dependency-
    cruiser.cjs` exception list shrinks to zero; **P3**; `just check-boundaries` with the
    exceptions removed, memory-host session tests.
24. **Split `realInput.test.ts` and the near-limit tests, fix fixture locations and globs**;
    `test/integration/realInput/`, `standalone-suite.ts`, `package.json` `test:unit`; **P3**;
    ratchet baseline empty, suite counts unchanged.
25. **De-risk the postinstall patch**; exact pins or esbuild alias; `scripts/patch-myst-
    imports.mjs`, `package.json`; **P3**; `npm ci --ignore-scripts && just check` passes.
26. **Split the 700+ line modules**; `editPalette.ts`, `rendering.ts`, `fileLinks.ts`,
    `pageToHost.ts`, `markdownTable.ts`, `SessionFactory` out of `previewManager.ts`; **P4**;
    tests unchanged, `check-limits` margins over 100 lines.
27. **Lifecycle nits and typing**; comments watcher disposables, `linkNavigation.rescan`
    unobserve, bounded `dismissedWarningBanners`, `ClipboardEvent` types, boot-context guard;
    **P4**; `churn.js` shows 0 subscription growth.
28. **Unused-exports check and the Sphinx build decision**; `just check` step; `src/node-services/
    build/sphinxBuild.ts` kept or removed; **P4**; check green.
