# Autonomous Remediation Plan — Markdown OKF-Schema Studio

Prepared 2026-10-09. Status: ready to run.
This plan executes the [deep analysis review](00-index.md) as 22 sequential implementation tasks
(T01–T22) framed by a preflight (T00) and a final verification (T23). It covers every finding of
rubrics 01–07 except SUP-01, which the owner excluded.

The plan is written for the orchestrating Claude Code session that runs it. The owner reads it
before triggering and may edit section 4 (decisions) or skip tasks in section 8.

## 1. How to trigger

1. Open Claude Code at the repository root, on the branch that should receive the commits.
2. Use a permission mode that lets edits and shell commands run unattended (auto mode, or
   accept-edits plus an allowlist for `git`, `fnm`, `npm`, `node`, `uv`, `just`, `unzip`).
3. Be on the Renault network or VPN (only needed if `node_modules/` must be reinstalled, and for
   T21).
4. Send:

```text
Exécute le plan .agents/changes/requests/deep-analysis-review/plan.md en mode autonome.
```

Variants: "… de T05 à T12 seulement", "… reprends à partir de progress.md".
All run state lives in [progress.md](progress.md) next to this file, so the run can be resumed after
an interruption or a context compaction.

Note: `.agents/changes/requests/` is git-ignored. This plan, the rubrics, `progress.md`, and the
probes stay local; only code and extension documentation are committed.

## 2. Roles

| Role | Who | Responsibilities |
| --- | --- | --- |
| Orchestrator | The main session | Runs T00 and T23, launches agents, runs gates, commits, keeps `progress.md`. Writes no production code itself. |
| Implementer | One `general-purpose` sub-agent per task | Implements one task card, adds its tests, runs the unit gate, reports. Never commits. |
| Reviewer | One `general-purpose` sub-agent, read-only | For tasks with **Review: yes**, checks the uncommitted diff against the card and the rubric. |

Launch every sub-agent with the Agent tool, `subagent_type: "general-purpose"`, **no `isolation`**
(never `worktree`), `run_in_background: false`, and a description such as `T07 implement` or
`T07 review`. Exactly one sub-agent runs at a time. Use `SendMessage` to the same implementer for
fix rounds so it keeps its context.

## 3. Hard rules (orchestrator and every sub-agent)

1. Work in the current checkout and on the current branch. No worktree, no branch switch, no rebase,
   no push, no `--amend` of a commit created before this run, no `--no-verify`.
2. Never run `git add -A`, `git add .`, `git commit -a`, `git clean`, `git reset --hard`,
   `git checkout -- .`, or `git restore .`.
3. **Protected paths**: every path that is dirty or untracked at T00 is the owner's work in
   progress. Never edit, stage, stash, or restore them.
4. Write scope: `**`, excluding `node_modules/`, `out/`,
   `.artifacts/`, and `.vscode-test/`. Extra paths only where a task card lists them (`justfile`,
   `AGENTS.md`). Never touch `book/`, `diagrams/`, `sphinx/`, `scripts/`, or other packages.
5. No new npm dependency unless the card allows it. No `npm install`; `npm ci` only in T00.
6. Rubric line numbers refer to commit `e1b4ad0` and drift as tasks land; locate code by symbol
   name.
7. Every fix ships the tests listed under "Tests to add" in its rubric, unless the card narrows
   them.
8. Match the surrounding code: TypeScript strict mode, existing naming and comment density, no
   reformatting of untouched code.
9. A user-visible change adds one bullet under `## Unreleased` at the top of
   `CHANGELOG.md` (create the section on first use). A breaking
   change starts its bullet with `**Breaking:**`. Added or changed settings are documented in the
   extension `README.md`.
10. Markdown is wrapped at 100 characters (`.agents/guidelines/documentation.guideline.md`).

## 4. Decisions applied by default

Edit this table before triggering if a different choice is wanted.

| ID | Decision | Task |
| --- | --- | --- |
| D1 | PlantUML runs with `PLANTUML_SECURITY_PROFILE=SANDBOX`. New setting `markdownOkfSchemaStudio.plantuml.allowWorkspaceIncludes` (boolean, default `false`, scope `machine`): when `true`, the profile is `ALLOWLIST` with `plantuml.allowlist.path` set to the workspace folders. | T03 |
| D2 | PlantUML is disabled for documents outside workspace folders (standalone previews show a placeholder). | T03 |
| D3 | `plantuml.jarPath` gets scope `machine` and must be absolute; a relative value produces an error diagnostic and no spawn. | T03 |
| D4 | The manifest declares `untrustedWorkspaces.supported: "limited"` with `restrictedConfigurations` for `plantuml.jarPath`, `plantuml.allowWorkspaceIncludes`, `frontmatter.bundleRoot`, `frontmatter.projectRoot`, `frontmatter.allowOutsideWorkspaceLinks`. | T20 |
| D5 | `allowOutsideWorkspaceLinks` gets scope `application`; workspace-level `bundleRoot` and `projectRoot` are honoured only inside workspace folders. | T20 |
| D6 | `retainContextWhenHidden` is removed for the custom editor only; the side panel keeps it. | T15 |
| D7 | SEC-08 is solved by validating in the render worker with a time budget; no native `re2` module. | T18 |
| D8 | The retired Sphinx modules and their tests are deleted, not quarantined. | T22 |
| D9 | SUP-02 adds `just vscode-markdown-okf-schema-studio-audit` (`npm audit --omit=dev --audit-level=high` and `npm sbom`). It joins the release check only if it succeeds on this machine. | T21 |
| D10 | SUP-01 is excluded: `.npmrc` keeps `strict-ssl=false`. | — |
| D11 | One commit per task, Conventional Commits with scope `vscode` (section 9.3). | all |
| D12 | In-place content updates use a small in-repo keyed DOM patcher; no `morphdom` dependency. | T16 |

## 5. Gates

Run gates from `src/markdown-okf-schema-studio` with the proxy bypass the `justfile` uses:

```bash
cd src/markdown-okf-schema-studio
export NO_PROXY=artifactory.tls.renault.fr,localhost,127.0.0.1
export no_proxy="$NO_PROXY"
```

| Gate | Command | Notes |
| --- | --- | --- |
| U | `fnm exec -- npm test` | Compile with type checking, unit tests, contract tests |
| I | `fnm exec -- npm run test:integration` | VS Code through `@vscode/test-electron` (cached in `.vscode-test/`); several minutes |
| V | `fnm exec -- npm run test:visual` | Renders fixtures, then `test/visual/capture.py` through `uv`; rewrites tracked screenshots |
| P | `fnm exec -- npm run package`, then `unzip -l .artifacts/markdown-okf-schema-studio.vsix` | Packaging and VSIX content |
| J | `just check-justfile` (repository root) | Only when the `justfile` changes |

- A gate **passes** when it reports no failure beyond the pre-existing failures recorded at T00.
- Long gates: use the Bash tool's maximum timeout (600000 ms); if a gate needs longer, run it in the
  background and wait for the completion notification instead of polling.
- Screenshots: gate V rewrites `test/visual/screenshots/**`. Commit those changes only when the card
  says **V: update**; otherwise run
  `git restore -- test/visual/screenshots` (regenerable output, never
  a protected path).
- Do not use `just vscode-markdown-okf-schema-studio-check` per task: it runs `npm ci` every time.

## 6. Per-task loop (orchestrator)

For each task of section 8, in order, skipping `done` and `skipped` ones:

1. Re-read `progress.md`. If a dependency is `failed` or `blocked`, mark the task `blocked` and
   continue.
2. `git status --porcelain=v1 --untracked-files=all` must list only protected paths; otherwise
   **STOP**.
3. Record `START=$(git rev-parse HEAD)` in `progress.md` and mark the task `running`.
4. Launch the implementer with the template of section 9.1 and the task card pasted verbatim. Wait.
5. Scope check with `git status --porcelain=v1 --untracked-files=all`: a protected path changed →
   **STOP**; a non-protected path outside the card's scope → ask the implementer to revert it.
6. Run the card's gates yourself; append the last lines of each gate to `progress.md`.
7. Gate failure → `SendMessage` to the implementer with the failing output; at most two fix rounds,
   then go to step 10.
8. **Review: yes** → launch the reviewer (section 9.2). `VERDICT: FIX-REQUIRED` → one `SendMessage`
   round to the implementer with the blocking items, re-run the gates, launch the reviewer once
   more. Still `FIX-REQUIRED` → step 10.
9. Commit: `git add -- <paths from step 5>`; confirm `git diff --cached --name-only` contains no
   protected path; commit with the message of section 9.3; record the SHA; mark the task `done`.
10. Failure: `git stash push --include-untracked -m "deep-review <ID> failed" -- <task paths>`;
    record the stash reference and the reason; mark the task `failed`; continue with the next task
    whose dependencies are met.

### Stop conditions

Write the reason in `progress.md`, then end the turn with a short summary for the owner.

- A protected path was modified, or the working tree shows unexpected changes at step 2.
- Two consecutive tasks ended `failed`.
- T00 cannot run gate U, or `node_modules/` is missing and `npm ci` fails.
- Gate I or V fails twice for an environmental reason (VS Code download, display, Playwright).
  Mark the gate `not runnable` in `progress.md` and continue with the remaining gates; stop at the
  third task affected.

## 7. Progress log

The orchestrator creates [progress.md](progress.md) at T00 with this structure:

```markdown
# Progress — deep analysis remediation

Run started: <date> · Branch: <branch> · Start commit: <sha>

## Protected paths
- <path>

## Baseline
| Gate | Result | Pre-existing failures |
| --- | --- | --- |

| Probe | Output |
| --- | --- |

## Tasks
| Task | Status | Commit | Gates | Notes |
| --- | --- | --- | --- | --- |
```

Status values: `pending`, `running`, `done`, `failed` (with stash reference), `blocked`, `skipped`.

## 8. Tasks

### Overview

| Task | Title | Findings | Depends on | Gates | Review |
| --- | --- | --- | --- | --- | --- |
| T00 | Preflight and baseline | — | — | U I V | — |
| **Phase A** | **Data integrity, leaks, process safety** | | | | |
| T01 | Frontmatter fences | STAB-01 | — | U I | yes |
| T02 | Schema registry and validator cache | PERF-12, PERF-13 | — | U I | yes |
| T03 | PlantUML process hardening | SEC-01, SEC-02, STAB-04 | — | U I | yes |
| T04 | Edit lock and save-triggered renders | STAB-02, PERF-06, STAB-03 (deferral) | — | U I | yes |
| T05 | Include budget | SEC-05 | — | U I | yes |
| **Phase B** | **Bounded work per edit** | | | | |
| T06 | PlantUML cache and concurrency | PERF-03 | T03 | U I | no |
| T07 | Stem index and wikilinks | PERF-15, PERF-09 | — | U I | no |
| T08 | One frontmatter analysis per version | PERF-14 | T02 | U I V | yes |
| T09 | Read caps, message bounds, relative paths | SEC-09, SEC-10, SEC-11 | — | U I | yes |
| T10 | Small correctness fixes | STAB-07, STAB-08, STAB-09 | T01 | U I | no |
| **Phase C** | **Webview without reloads** | | | | |
| T11 | CSP and allowlist sanitizer | SEC-06, SEC-12 | — | U I V | yes |
| T12 | Status updates by message | PERF-05 (step 1) | T04 | U I V | yes |
| T13 | Runtime as bundled assets | PERF-11 | T12 | U I V P | yes |
| T14 | Webview runtime efficiency | PERF-08, PERF-07 | T13 | U I V | no |
| T15 | Panel lifecycle | PERF-10, STAB-05 | — | U I | no |
| T16 | In-place content updates | PERF-05 (step 2), STAB-03, STAB-06 | T12, T13, T14 | U I V | yes |
| **Phase D** | **Pipeline refactor** | | | | |
| T17 | Single HAST pipeline and memoisation | PERF-02, PERF-04 | T05, T11 | U I V | yes |
| T18 | Worker-thread rendering | PERF-01, SEC-08 | T17 | U I V P | yes |
| T19 | Dependency-scoped watchers | PERF-16, PERF-17, SEC-07 | — | U I | no |
| **Phase E** | **Trust, release gate, documentation** | | | | |
| T20 | Restricted Mode and setting scopes | SEC-03, SEC-04 | T03 | U I | yes |
| T21 | Release gate: audit, SBOM, VSIX content | SUP-02, SUP-03 | — | U P J | no |
| T22 | Dead code and documentation | SUP-04, SUP-05 | all done tasks | U I P | yes |
| T23 | Final verification and report | — | — | release check | yes |

Paths in the cards are relative to `` unless they start with `/`
(repository root).

### T00 — Preflight and baseline (orchestrator only)

1. Record the branch (`git rev-parse --abbrev-ref HEAD`; detached HEAD → STOP) and
   `git rev-parse HEAD`.
2. Record protected paths from `git status --porcelain=v1 --untracked-files=all`. If one of them is
   under `` → **STOP** and ask the owner, because their work in
   progress could not be separated from task changes.
3. Toolchain: `fnm exec -- node --version`, `uv --version`, `just --version`. If `node_modules/` is
   missing, run `fnm exec -- npm ci`; failure → STOP.
4. Baseline gates U, I, V. Record failing test names as pre-existing failures. Restore screenshots
   after gate V.
5. Probes: `fnm exec -- npm run compile`, then every probe listed in
   [probes/README.md](probes/README.md); record each JSON output in the baseline table.
6. Create `progress.md` with every task `pending`.

### T01 — Frontmatter fences

- **Findings**: STAB-01 ([07](07-stability-and-correctness.md)).
- **Scope**: `src/frontmatter/okfFrontmatter.ts`, `src/render/mystRenderer.ts` (`stripFrontmatter`),
  `src/frontmatter/fileLinks.ts` (`linkedFileDetails`), `test/frontmatter/`, `test/rendering/`.
- **Instructions**: export one fence matcher (for example `matchFrontmatterBlock(source)` returning
  offsets and the line ending) built on the regex given in the rubric, and use it at all five call
  sites. Add the patch guard: re-parse the patched document and refuse the patch (existing error
  path) when an original key is missing or duplicated.
- **Probe**: `frontmatter-fence.cjs` reports `allKeysExtracted: true` and
  `editIsSingleLineChange: true`.
- **Gates**: U, I. **Review**: yes. **V**: not run.
- **Commit**: `fix(vscode): anchor frontmatter fences to line starts`.
- **CHANGELOG**: frontmatter values ending with `...` or `---` no longer truncate the properties
  table or corrupt table edits.

### T02 — Schema registry and validator cache

- **Findings**: PERF-12, PERF-13 ([06](06-performance-frontmatter-and-filesystem.md)).
- **Scope**: `src/frontmatter/okfFrontmatter.ts`, `src/frontmatter/schemaValidator.ts`,
  `src/frontmatter/fileLinks.ts`, new `src/frontmatter/schemaRegistry.ts`, `src/extension.ts`
  (watcher wiring and disposal), `test/frontmatter/`.
- **Instructions**: the registry returns the same resolved schema object until the `(mtimeMs, size)`
  of the schema or of an inlined `$ref` target changes, or until a `**/_schema{,s}/**` watcher per
  workspace folder fires; on invalidation call `sharedSchemaValidator.removeSchema(previous)`. Cache
  the schema-directory lookup per document directory and the directory listings under the same
  invalidation. Cache `if` and branch validators under the resolved-schema entry. Keep
  `setSchemaFileReaderForTests` working and add `resetSchemaRegistryForTests`.
- **Probe**: `ajv-cache.cjs` reports at most 5 cache entries and under 1 MB heap growth.
- **Gates**: U, I. **Review**: yes.
- **Commit**: `perf(vscode): cache resolved OKF schemas and their validators`.
- **CHANGELOG**: long editing sessions no longer accumulate memory from schema validation.

### T03 — PlantUML process hardening

- **Findings**: SEC-01, SEC-02 ([01](01-security-process-execution-and-trust.md)),
  STAB-04 ([07](07-stability-and-correctness.md)). Decisions D1, D2, D3.
- **Scope**: `src/render/plantUmlRenderer.ts`, `src/render/renderPipeline.ts`,
  `src/configuration/plantUmlConfiguration.ts`, `src/extension.ts`, `package.json`, `README.md`,
  `CHANGELOG.md`, `test/rendering/`, `test/configuration/`.
- **Instructions**:
  - Child environment limited to `PATH`, `HOME` or `USERPROFILE`, `JAVA_HOME` (if set), `TMPDIR`,
    `TEMP`, `TMP`, `LANG`, `LC_ALL`, plus `PLANTUML_SECURITY_PROFILE`.
  - JAR form: `java -DPLANTUML_SECURITY_PROFILE=<profile>`, then
    `-Dplantuml.allowlist.path=<roots>` in `ALLOWLIST` mode only (roots joined by `path.delimiter`),
    then `-jar <jar> -pipe -tsvg`.
  - `cwd`: a private temporary directory created once (`fs.mkdtempSync`) and removed on deactivate;
    workspace folder only in `ALLOWLIST` mode.
  - Resolve `java` and `plantuml` by scanning `PATH` entries explicitly, skipping empty or relative
    entries and entries inside workspace folders (honour `PATHEXT` on Windows).
  - STAB-04: `stdin` error handler, `Buffer` chunks decoded once, `stderr` capped at 64 KiB,
    exported 15 s timeout, `detached: true` with process-group kill on POSIX, `child.kill()` on
    Windows.
- **Tests**: spawner-hook tests for environment, `cwd`, arguments, and profile; standalone document
  → placeholder with zero spawns; relative `jarPath` → error with zero spawns; early-exit child
  without uncaught exception; UTF-8 split across chunks; timeout kill.
- **Probe**: `plantuml-epipe.cjs` reports `uncaughtExceptions: 0`.
- **Gates**: U, I. **Review**: yes.
- **Commit**: `fix(vscode): sandbox and harden PlantUML rendering`.
- **CHANGELOG** (breaking): PlantUML `!include` of local files and URLs is blocked unless
  `plantuml.allowWorkspaceIncludes` is enabled; `plantuml.jarPath` must be an absolute path set in
  user settings; PlantUML is disabled for files outside workspace folders.

### T04 — Edit lock and save-triggered renders

- **Findings**: STAB-02, the deferral part of STAB-03 ([07](07-stability-and-correctness.md)),
  PERF-06 ([05](05-performance-webview-lifecycle.md)).
- **Scope**: `src/extension.ts`, the webview runtime in `src/webview/` only if `previewReady` needs
  a new field, `test/integration/previewEditing.test.ts`, `test/webview/`.
- **Instructions**: release `activeBlockEdit` when `previewReady` arrives with another `requestId`,
  on panel dispose, and after 30 s without edit messages. In `refreshReferencedPath`, skip the
  render when the changed path is the open active document and its version equals the rendered stage
  version. While a block edit is active, queue PlantUML injection, link-enrichment replacement, and
  save-triggered renders, then flush them when the edit completes.
- **Tests**: autosave once, simulate a save, then open another block (succeeds); saving an unchanged
  buffer creates no new request; PlantUML injection is deferred during an edit (render override).
- **Gates**: U, I. **Review**: yes.
- **Commit**: `fix(vscode): keep inline editing usable across preview reloads`.
- **CHANGELOG**: saving no longer closes or locks the inline editor.

### T05 — Include budget

- **Findings**: SEC-05 ([02](02-security-webview-and-content.md)).
- **Scope**: `src/render/mystRenderer.ts`, `src/render/renderPipeline.ts`, `test/rendering/`.
- **Instructions**: one budget object per render (exported constants: 200 expansions, 10 MiB of
  included text); memoise `resolveInclude` and the parsed AST per canonical path within a render,
  and `structuredClone` the AST before `setIncludedSourceLine` mutates it; emit one diagnostic when
  the budget is exhausted and leave the remaining include directives as placeholders.
- **Probe**: `include-fanout.mjs 5` completes in under 1 s with a budget diagnostic.
- **Gates**: U, I. **Review**: yes.
- **Commit**: `fix(vscode): bound include expansion per render`.
- **CHANGELOG**: documents with very many includes show a warning instead of freezing the editor.

### T06 — PlantUML cache and concurrency

- **Findings**: PERF-03 ([04](04-performance-render-pipeline.md)). **Depends on**: T03.
- **Scope**: `src/render/plantUmlRenderer.ts`, `src/render/renderPipeline.ts`, `src/extension.ts`,
  `test/rendering/`.
- **Instructions**: module-level LRU (200 entries) keyed by `sha256(source, command, arguments)`;
  a concurrency limiter of 2 shared by all previews; queued jobs are dropped when their render is
  aborted. PlantUML batch mode is optional and only if it stays simple.
- **Tests**: an unchanged diagram across two renders spawns once; eight diagrams never exceed two
  concurrent processes; aborting a render cancels its queued jobs.
- **Gates**: U, I. **Review**: no.
- **Commit**: `perf(vscode): cache PlantUML diagrams and cap concurrent renders`.
- **CHANGELOG**: PlantUML diagrams no longer re-render on every keystroke.

### T07 — Stem index and wikilinks

- **Findings**: PERF-15 ([06](06-performance-frontmatter-and-filesystem.md)),
  PERF-09 ([05](05-performance-webview-lifecycle.md)).
- **Scope**: `src/frontmatter/stemIndex.ts`, `src/frontmatter/fileLinks.ts`, `src/extension.ts`,
  `src/navigation/previewNavigation.ts`, `test/frontmatter/`, `test/navigation/`.
- **Instructions**: drop the `onDidChange` invalidation; apply create and delete events
  incrementally. Implement the wikilink `discover` callback on top of `getCachedMarkdownStemIndex`,
  keeping the existing ambiguity and containment semantics. Cache `resolvePreviewLink` results per
  `(document URI, version, request)` and clear the cache on stem changes. An asynchronous first
  build is optional; record it as a follow-up if not done.
- **Tests**: a change event keeps the index; create adds and delete removes one path; wikilink
  discovery calls no `findFiles` (spy).
- **Gates**: U, I. **Review**: no.
- **Commit**: `perf(vscode): keep the Markdown stem index across saves`.
- **CHANGELOG**: none.

### T08 — One frontmatter analysis per version

- **Findings**: PERF-14 ([06](06-performance-frontmatter-and-filesystem.md)). **Depends on**: T02.
- **Scope**: `src/extension.ts`, `src/frontmatter/okfFrontmatter.ts`,
  `src/frontmatter/propertiesTable.ts`, `test/frontmatter/`, `test/integration/`.
- **Instructions**: memoise `analyzeFrontmatter` per `(URI, version, options)` on the preview (keep
  the last two entries). Remove the `refreshFrontmatter` pass that duplicates the render's analysis;
  keep the function for settings changes. Key link resolution on the link-bearing values; when
  unchanged, reuse the previous results and render the linked table directly in `updatePreview`,
  which removes the pending-to-resolved flicker.
- **Tests**: typing in the body performs one analysis and no link resolution after the first;
  editing a link value performs exactly one resolution.
- **Gates**: U, I, V (no visual change expected). **Review**: yes.
- **Commit**: `perf(vscode): analyse frontmatter once per document version`.
- **CHANGELOG**: frontmatter links no longer flicker while typing.

### T09 — Read caps, message bounds, relative paths

- **Findings**: SEC-09, SEC-10, SEC-11 ([02](02-security-webview-and-content.md)).
- **Scope**: `src/frontmatter/fileLinks.ts`, `src/frontmatter/okfFrontmatter.ts`,
  `src/extension.ts`, `src/webview/linkNavigation.ts`, `src/preview/webview.ts`, `test/security/`,
  `test/frontmatter/`.
- **Instructions**: 5 MiB cap for schema and `$ref` reads; linked targets read only their first 64
  KiB; message caps (block texts 1 MiB, field names 256 characters, requests 4096, frontmatter value
  depth 32 and 256 KiB); external links parsed strictly, scheme re-checked, `openExternal` inside
  the existing error handling; workspace-relative paths in link titles and diagnostics.
- **Tests**: one per cap; oversized messages rejected by `isPreviewSyncMessage`; an encoded scheme
  is blocked.
- **Gates**: U, I. **Review**: yes.
- **Commit**: `fix(vscode): bound content reads and webview message payloads`.
- **CHANGELOG**: link tooltips and diagnostics show workspace-relative paths.

### T10 — Small correctness fixes

- **Findings**: STAB-07, STAB-08, STAB-09 ([07](07-stability-and-correctness.md)). **Depends on**:
  T01.
- **Scope**: `src/render/mystRenderer.ts`, `src/frontmatter/okfFrontmatter.ts`,
  `src/frontmatter/fileLinks.ts`, `src/extension.ts`, matching tests.
- **Instructions**: CRLF-safe `expandGithubAlerts` and fence helpers; `Object.hasOwn` for every
  frontmatter and schema record probe; one bounded LRU (200 URIs) for `descriptionsCollapsed` under
  a single `workspaceState` key, migrating and deleting the old per-URI keys; cap the `states` map.
- **Probe**: `crlf-alerts.mjs` reports `crlfAdmonition: true`.
- **Gates**: U, I. **Review**: no.
- **Commit**: `fix(vscode): render alerts in CRLF files and bound per-document state`.
- **CHANGELOG**: GitHub alerts render in files with Windows line endings.

### T11 — CSP and allowlist sanitizer

- **Findings**: SEC-06, SEC-12 ([02](02-security-webview-and-content.md)).
- **Scope**: `src/security/csp.ts`, `src/security/html-sanitizer.ts`, `src/preview/webview.ts`,
  `src/render/mathRenderer.ts`, `src/extension.ts`, `test/security/`.
- **Instructions**: `script-src` with the nonce only; remove content `<script>` and stylesheet
  pass-through and the `allowExternalScripts` parameter. Build the allowlist from what is really
  emitted: render every `/book/chapters/*.md` and the test fixtures, collect element and attribute
  names, add the extension's own injected markup, and keep URL attributes on the existing policy.
  Reject generated KaTeX declarations containing `{`, `}`, `<`, `@`, or `\`.
- **Tests**: as listed in the rubric; rendering all book chapters yields the same diagnostic codes
  as before the change.
- **Gates**: U, I, V (no visual change expected). **Review**: yes.
- **Commit**: `fix(vscode): enforce nonce-only scripts and an allowlist sanitizer`.
- **CHANGELOG**: none.

### T12 — Status updates by message

- **Findings**: PERF-05 step 1 ([05](05-performance-webview-lifecycle.md)). **Depends on**: T04.
- **Scope**: `src/extension.ts`, the webview runtime, `src/preview/webview.ts`, tests.
- **Instructions**: while a live preview document exists, status changes (debouncing, building,
  stale, error) are posted as `previewStatus` messages carrying the context identity and rendered
  with `textContent`; `webview.html` is assigned only when no live document exists. Expose an
  assignment counter through `getActivePreviewForTests`.
- **Tests**: ten keystrokes produce as many `html` assignments as completed renders, and none for
  status.
- **Gates**: U, I, V (**V: update** if the status area changes). **Review**: yes.
- **Commit**: `perf(vscode): update preview status without reloading the webview`.
- **CHANGELOG**: less flicker while typing.

### T13 — Runtime as bundled assets

- **Findings**: PERF-11 ([05](05-performance-webview-lifecycle.md)). **Depends on**: T12.
- **Scope**: `esbuild.mjs`, `src/webview/` (new runtime entry), `src/preview/previewStyles.ts`,
  `src/preview/webview.ts`, `src/extension.ts`, tests.
- **Instructions**: bundle the runtime as `out/bundle/preview.js` (browser IIFE) and
  `out/bundle/preview.css`; pass the per-render context in
  `<script type="application/json" id="sphinx-preview-context">`; replace the `toString()`
  serialisation of helpers with normal imports; add `out/bundle` to `localResourceRoots` for every
  page.
- **Gates**: U, I, V, P (the VSIX contains `preview.js` and `preview.css`). **Review**: yes.
- **Commit**: `perf(vscode): load the preview runtime from bundled assets`.
- **CHANGELOG**: none.

### T14 — Webview runtime efficiency

- **Findings**: PERF-08, PERF-07 ([05](05-performance-webview-lifecycle.md)). **Depends on**: T13.
- **Scope**: the webview runtime, `src/webview/mermaidPreview.ts`, `test/webview/`.
- **Instructions**: heading offsets computed in `measure()` with binary search per scroll frame;
  `setState` and host scroll messages on a trailing 100 ms throttle, flushed on `pagehide`; resize
  and image-load work coalesced in one animation frame; `measureLineTops` only near the viewport.
  Mermaid: lazy rendering through `IntersectionObserver`, sequential rendering, SVG cache keyed by
  source and theme variables, persisted in `setState` (at most 50 entries, none above 200 KB).
- **Gates**: U, I, V. **Review**: no.
- **Commit**: `perf(vscode): reduce layout work while scrolling and render Mermaid lazily`.
- **CHANGELOG**: Mermaid diagrams render when they scroll into view.

### T15 — Panel lifecycle

- **Findings**: PERF-10 ([05](05-performance-webview-lifecycle.md)),
  STAB-05 ([07](07-stability-and-correctness.md)). Decision D6.
- **Scope**: `src/extension.ts`, `test/integration/`.
- **Instructions**: drop `retainContextWhenHidden` for the custom editor. When several panels are
  restored, each keeps a live session; only the most recently restored follows the active editor.
- **Gates**: U, I. **Review**: no.
- **Commit**: `fix(vscode): restore every preview panel with a live session`.
- **CHANGELOG**: restored preview panels no longer freeze; hidden custom-editor tabs use less
  memory.

### T16 — In-place content updates

- **Findings**: PERF-05 step 2 ([05](05-performance-webview-lifecycle.md)),
  STAB-03 and STAB-06 ([07](07-stability-and-correctness.md)). Decision D12.
  **Depends on**: T12, T13, T14.
- **Scope**: `src/extension.ts`, the webview runtime, `src/preview/webview.ts`,
  `src/frontmatter/propertiesTable.ts`, tests.
- **Instructions**: after the first load, post `previewContent` with the sanitised main content, the
  properties-table fragment, and the new context identity (document version, request ID); the
  runtime parses it with `DOMParser`, patches blocks keyed by `data-sphinx-preview-block` plus a
  content hash, updates its context, discovers only new links, then runs `measure()` and re-applies
  the anchor. The block under an open inline editor is kept. Full reloads remain for nonce or CSP
  changes and document switches. STAB-06: track the edited block as a range updated from
  `contentChanges`, and answer stale edit messages with an explicit error.
- **Risk**: highest of the plan. A failure here leaves T12–T15 intact.
- **Gates**: U, I, V (**V: update** allowed). **Review**: yes.
- **Commit**: `perf(vscode): patch preview content in place instead of reloading`.
- **CHANGELOG**: the preview no longer reloads while typing; scroll position and inline editors are
  kept.

### T17 — Single HAST pipeline and memoisation

- **Findings**: PERF-02, PERF-04 ([04](04-performance-render-pipeline.md)). **Depends on**: T05,
  T11.
- **Scope**: `src/render/`, `src/security/html-sanitizer.ts`, `src/mapping/sourceMapping.ts`,
  `src/preview/webview.ts`, `src/frontmatter/propertiesTable.ts`, tests.
- **Instructions**: build one HAST tree from `mystToHast`, apply table alignment, source mapping,
  the T11 allowlist, the URL policy, highlighting, math, and PlantUML placeholders as tree
  transforms, and stringify once. Prefer packages already in `node_modules`; declare any directly
  imported package in `package.json` at the locked version and update the lockfile with
  `npm install --package-lock-only --offline`. If that fails, keep using the stringifier that
  `myst-to-html` already wires. Memoise highlight.js and KaTeX output (LRU of 500 each). Build the
  page shell and the CSP meta from a string template.
- **Tests**: existing rendering, security, and contract suites pass; a spy confirms one
  stringification; memo hits are tested; normalised HTML of every book chapter is unchanged.
- **Gates**: U, I, V. **Review**: yes.
- **Commit**: `refactor(vscode): render MyST through a single HAST pipeline`.
- **CHANGELOG**: none.

### T18 — Worker-thread rendering

- **Findings**: PERF-01 ([04](04-performance-render-pipeline.md)),
  SEC-08 ([02](02-security-webview-and-content.md)). Decision D7. **Depends on**: T17.
- **Scope**: new `src/render/renderWorker.ts`, `src/render/renderPipeline.ts`,
  `src/build/buildQueue.ts`, `src/extension.ts`, `esbuild.mjs`, the frontmatter validation call
  path, tests.
- **Instructions**: one worker per window, bundled as `out/bundle/renderWorker.js`; include reads
  with `fs.promises` in the worker; cancellation by terminating and respawning the worker; adaptive
  debounce `max(40 ms, 1.5 × last render)` capped at 400 ms. SEC-08: run Ajv validation in the
  worker with a 2 s budget that yields a diagnostic. If moving validation proves too invasive, ship
  PERF-01 alone and record SEC-08 as deferred.
- **Tests**: superseded requests are cancelled; event-loop delay p95 under 50 ms while typing into
  chapter 08 in the integration suite; a catastrophic schema pattern returns a diagnostic in time.
- **Gates**: U, I, V, P (the VSIX contains the worker bundle). **Review**: yes.
- **Commit**: `perf(vscode): render previews in a worker thread`.
- **CHANGELOG**: VS Code stays responsive while typing in large documents.

### T19 — Dependency-scoped watchers

- **Findings**: PERF-16, PERF-17 ([06](06-performance-frontmatter-and-filesystem.md)),
  SEC-07 ([02](02-security-webview-and-content.md)).
- **Scope**: `src/extension.ts`, `src/build/buildQueue.ts`, `src/render/`,
  `src/security/resource-policy.ts`, tests.
- **Instructions**: as in the rubrics: watchers built from the stage dependencies, a
  pre-canonicalised dependency set, no recursive watcher outside workspace folders, cached canonical
  roots, filtered `onDidChangeTextDocument`, narrow standalone resource roots.
- **Gates**: U, I. **Review**: no.
- **Commit**: `perf(vscode): watch only rendered dependencies`.
- **CHANGELOG**: none.

### T20 — Restricted Mode and setting scopes

- **Findings**: SEC-03, SEC-04 ([01](01-security-process-execution-and-trust.md)). Decisions D4, D5.
  **Depends on**: T03.
- **Scope**: `package.json`, `src/extension.ts`, `src/frontmatter/fileLinks.ts`, `README.md`,
  `test/integration/untrusted-suite.ts`, `test/frontmatter/`.
- **Instructions**: in Restricted Mode the preview is read-only, PlantUML is off, includes stay in
  the document directory, and schemas are not resolved (the existing `readOnly` branches);
  `onDidGrantWorkspaceTrust` re-creates open previews.
- **Gates**: U, I. **Review**: yes.
- **Commit**: `feat(vscode): support Restricted Mode with a read-only preview`.
- **CHANGELOG**: the preview opens read-only in untrusted folders; `allowOutsideWorkspaceLinks` is a
  user-level setting.

### T21 — Release gate: audit, SBOM, VSIX content

- **Findings**: SUP-02, SUP-03 ([03](03-security-supply-chain-and-packaging.md)). Decision D9.
- **Scope**: `/justfile`, `.vscodeignore`, `test/release/`, `package.json` scripts.
- **Instructions**: add the audit target and run it once; wire it into
  `vscode-markdown-okf-schema-studio-release-check` only if it succeeds here, otherwise record why
  in the card's report. Rewrite `.vscodeignore` as an allowlist (no source maps, no `docs/`, no
  `.playwright-cli/`, no `*.orig`, no `spec.md`) and add a VSIX listing assertion to the release
  check.
- **Gates**: U, P, J. **Review**: no.
- **Commit**: `build(vscode): scan dependencies and pin VSIX contents in the release gate`.
- **CHANGELOG**: none.

### T22 — Dead code and documentation

- **Findings**: SUP-04, SUP-05 ([03](03-security-supply-chain-and-packaging.md)).
  **Depends on**: every task marked `done`; documentation describes only what landed.
- **Scope**: `src/build/sphinxBuild.ts`, `src/build/snapshotWorkspace.ts`,
  `src/build/sourceTransforms.ts`, their tests (check `test/rendering/sphinxFeatures.contract.ts`),
  unused sanitizer helpers, `esbuild.mjs` (`punycode` alias), `docs/security-evidence.md`,
  `docs/known-limitations.md`, `README.md`, `/AGENTS.md` (only the "VS Code Extension — Markdown
  OKF-Schema Studio" section and its project-structure lines).
- **Instructions**: read `progress.md` first and never document a failed or skipped task as done.
  Confirm that `DEP0040` disappears (`node --trace-deprecation` on a render).
- **Gates**: U, I, P. **Review**: yes (documentation checked against the code).
- **Commit**: `chore(vscode): remove the retired Sphinx pipeline and refresh docs`.
- **CHANGELOG**: none.

### T23 — Final verification and report (orchestrator)

1. Run `just vscode-markdown-okf-schema-studio-release-check` from the repository root. If `npm ci`
   fails for network reasons, run its remaining steps individually and note it.
2. Recompile and run every probe; fill a before/after table in `progress.md`.
3. Launch a reviewer on
   `git diff <T00 commit>..HEAD -- src/markdown-okf-schema-studio justfile AGENTS.md` to look for
   cross-task regressions.
4. Add a `- **Status**:` line to every finding of rubrics 01–07: `Fixed in <sha>`,
   `Failed (<stash>)`, `Deferred`, or `Excluded`.
5. Write [report.md](report.md): outcome per task, metrics before and after, the user-visible
   changes to announce (copied from `CHANGELOG.md`, breaking changes first), failed tasks with stash
   references, and next steps. Do not install the VSIX; give the owner the command
   `just vscode-markdown-okf-schema-studio-install`, followed by **Developer: Reload Window**.
6. Do not push.

## 9. Templates

### 9.1 Implementer prompt

```text
You are the implementer for task <ID> of the deep-analysis remediation of the VS Code extension in
src/markdown-okf-schema-studio. Repository: /Users/az02065/Projects/Nestor/agentic-coding-white-paper.

You work directly in the shared git checkout, on branch <branch>. No other agent runs at the same
time. Do not commit, stash, switch branches, or push: the orchestrator verifies and commits your work.

Read first:
1. AGENTS.md at the repository root: "VS Code Extension — Markdown OKF-Schema Studio" and
   "Writing & Editing Guidelines".
2. .agents/changes/requests/deep-analysis-review/<rubric file(s)>: the sections of <finding IDs>
   (What happens, Fix, Tests to add, Done when). Line numbers refer to commit e1b4ad0; locate code by
   symbol name.
3. .agents/changes/requests/deep-analysis-review/plan.md: section 3 (hard rules) and section 4
   (decisions).
4. .agents/changes/requests/deep-analysis-review/progress.md: notes left by earlier tasks.

Task card:
<card pasted verbatim>

Protected paths (never edit, stage, stash, or restore):
<list from progress.md>

Work loop: implement the change and its tests, then from src/markdown-okf-schema-studio run
`fnm exec -- npm test` (export NO_PROXY and no_proxy as in plan.md section 5) until it passes, and run
any probe named in the card. Do not run the integration or visual suites unless the card asks; the
orchestrator runs them.

Your final message is the only thing the orchestrator reads. Keep it under 300 words:
- Summary of the change
- Files changed
- Tests added
- Commands run, with their final result lines
- Deviations from the card, and why
- CHANGELOG bullet text, if user-visible
- Open risks or follow-ups
```

### 9.2 Reviewer prompt

```text
You are a read-only reviewer for task <ID> of the deep-analysis remediation of
src/markdown-okf-schema-studio. Repository: /Users/az02065/Projects/Nestor/agentic-coding-white-paper.
Do not edit files and do not run git commands that change state.

Inputs: the task card below, the rubric sections of <finding IDs> in
.agents/changes/requests/deep-analysis-review/, `git diff HEAD -- <scope paths>`, and the new files
listed by `git status --porcelain=v1 --untracked-files=all` (read them).

Task card:
<card pasted verbatim>

Check:
1. The change satisfies the "Done when" criterion of every finding.
2. Correctness: logic errors, races, error handling, resource cleanup, regressions of existing behaviour.
3. Security: trust gating, CSP, path containment, process spawning, message validation.
4. Tests cover the card's tests and would fail without the fix.
5. Every user-visible behaviour change appears in the CHANGELOG bullet.
6. No protected or out-of-scope path is touched. Protected paths: <list>.

Answer in under 400 words. First line: `VERDICT: PASS` or `VERDICT: FIX-REQUIRED`.
Then numbered blocking issues (file:line, problem, concrete fix), substantiated from the code only.
Then non-blocking notes.
```

### 9.3 Commit message

```text
<type>(vscode): <subject from the task card>

<Two to four lines: what changed and why.>

Findings: <IDs> (deep analysis review, 2026-10-08)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

## 10. Duration and checkpoints

These are rough estimates of agent wall time, including integration and visual runs:
Phase A 3–5 h, Phase B 3–5 h, Phase C 5–8 h, Phase D 5–8 h, Phase E 2–3 h.
A full run likely exceeds one working day. The owner can run one phase per trigger and review its
commits in between (`git log --oneline <T00 commit>..HEAD`); the plan resumes from `progress.md`.
