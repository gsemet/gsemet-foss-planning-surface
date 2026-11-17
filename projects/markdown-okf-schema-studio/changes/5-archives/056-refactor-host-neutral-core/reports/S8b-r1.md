# S8b, round 1: internals and tests (coder report)

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-056`, branch
`changes-requests/056-refactor-host-neutral-core` (HEAD 2516aa1). Nothing is committed, stashed or
pushed. `just preflight` was not run.

## Summary

- The renderer is now an ordered list of named passes, with a dispatch table per node kind. The
  frontmatter module is split into parse, validate and serialize, and reads schema files through a
  new `SchemaFiles` port. renderPipeline uses the global `performance`.
- The CSS is split into 8 per-feature modules. The bundled `preview.css` is byte-identical to the
  HEAD build: same SHA-256.
- editActions, editPalette, mystFeatures.test, scenarios and capture.py are split. Every new file
  is under its limit. The size baseline goes from 9 entries to 1 (`realInput.test.ts`, left on
  purpose; see below).
- Boundaries: one exception removed (`RENDERER_SPLIT`) and two narrowed (okfFrontmatter loses
  `fs` and `util`, renderPipeline loses `perf_hooks`). None added.
- Gates are green: tsc, unit tests (2 305 of 2 305), `just check`, `just visual` (320 scenarios,
  210 screenshots, no PNG changed) and the bundle. The integration run was not done because the
  screen was locked.

## What moved where (line counts)

### Renderer (`src/core/render/`, mystRenderer.ts was 1 934 lines)

| File | Lines | Contents |
| --- | --- | --- |
| `mystRenderer.ts` | 439 | include expansion, `RenderState`, `TREE_PASSES`, `HTML_PASSES`, `renderMyst`, `stripFrontmatter`, re-exports |
| `mystTypes.ts` | 54 | public types |
| `mystEngine.ts` | 44 | MyST parse options, engine loading, `parseMystSource`, `preloadMystEngine` |
| `mystNormalize.ts` | 525 | `NODE_RULES`, `RULES_BY_KIND`, `normalizeNode`, walk, diagrams, PlantUML file requests, image size, figure alignment |
| `mystBlockTransforms.ts` | 296 | block-level tree passes |
| `mystInlineTransforms.ts` | 279 | inline tree passes |
| `mystContextTags.ts` | 233 | context tag passes |
| `mystTables.ts` | 297 | raw HTML tables, table alignments |
| `mystGithubAlerts.ts` | 89 | GitHub alert source pass |

The `TREE_PASSES` order is the HEAD order:

1. shift source lines
2. grids
3. context tags
4. MyST extension check
5. includes
6. toctrees
7. figure captions
8. caption-less references
9. version admonitions
10. wiki links
11. checkboxes
12. bare URLs
13. comment markers
14. raw details and kbd
15. context tag containers
16. bare block images
17. anchors
18. normalize nodes
19. table alignments

`HTML_PASSES` are table alignments, then code highlighting, then anchor ids.

The `normalizeNode` dispatch: if a rule changes the node kind without finishing the node, the
remaining rules of the new kind run. This covers html becoming `rawHtmlTableBlock`, as on HEAD.

### Frontmatter (`src/core/frontmatter/`, okfFrontmatter.ts was 1 720 lines)

| File | Lines | Contents |
| --- | --- | --- |
| `okfFrontmatter.ts` | 516 | schema discovery (`findSchemaDirectory(files, …)`, `matchSchemaFile(files, …)`, `resolveSchemaRefs(files, …)`), `FrontmatterOptions` (new required `schemaFiles`), `analyzeFrontmatter`, `frontmatterLinkIdentity`, re-exports |
| `frontmatterParse.ts` | 158 | block matching, `extractFrontmatter`, YAML value parsing, `stripJson5Comments` |
| `frontmatterValidate.ts` | 374 | field types, effective properties, enums, docs, defaults, `fieldsFromYaml` |
| `frontmatterSerialize.ts` | 746 | the properties-editor patch builders (`verified()` now uses `isSameData`) |
| `sameData.ts` | 81 | `isSameData`, a host-neutral `util.isDeepStrictEqual` |
| `schemaFiles.ts` | 19 | the `SchemaFiles` port: `isDirectory`, `isFile`, `listFiles`, `readText` |
| `src/node-services/schemaFiles.ts` | 47 | `nodeSchemaFiles`: sync fs, same try/catch behaviour as HEAD |

Wiring:

- `HostServices.schemaFiles` is added in `src/host-api/index.ts`, and the VS Code host sets it to
  `nodeSchemaFiles` (`src/host-vscode/vscodeHost.ts`).
- The session callers pass `host.schemaFiles`: `features/frontmatter.ts`, `features/rendering.ts`
  and `features/links.ts`.
- `renderPipeline.ts` (265 lines) uses the global `performance.now()`. It also gained TSDoc on its
  exports.

### CSS (`src/core/preview/`, previewStyles.ts was 4 179 lines)

`previewStyles.ts` is now 119 lines. It keeps the accessibility CSS and the content width CSS, and
builds `PREVIEW_THEME_CSS` by joining these modules of `styles/` in cascade order:

| File | Lines |
| --- | --- |
| `pageChromeStyles.ts` | 487 |
| `editModeStyles.ts` | 384 |
| `editPaletteStyles.ts` | 765 |
| `frontmatterEditorStyles.ts` | 461 |
| `contentLayoutStyles.ts` | 370 |
| `commentStyles.ts` | 539 |
| `contentBlockStyles.ts` | 675 |
| `propertiesStyles.ts` | 472 |

### Edit actions and palette (`src/page/modules/`)

editActions.ts was 1 746 lines. It is now split as follows:

| File | Lines | Notes |
| --- | --- | --- |
| `editActions.ts` | 307 | types, handlers table, shortcuts |
| `editActionHelpers.ts` | 120 | |
| `inlineEditActions.ts` | 385 | |
| `blockEditActions.ts` | 472 | |
| `linkEditActions.ts` | 136 | |
| `tableEditActions.ts` | 240 | `createTableEditActions(tableTools)` |
| `colourEditActions.ts` | 210 | `createColourEditActions(isSafeColor)` |

editPalette.ts was 1 191 lines. It is now `editPalette.ts` (766) plus `editPalettePopovers.ts`
(515), which holds the grid, emoji, choices and colour popovers. They share a
`PalettePopoverContext`, and the popover state is a single `popover` object.

### Tests

- **`test/core/render/mystFeatures.test.ts`:** was 1 711 lines, now 1 256. The palette rendering
  tests moved to `mystPaletteRendering.test.ts` (444), and the fixture helpers to
  `mystFeaturesSupport.ts` (34). There are 75 tests before and after, and only the import and
  export lines differ.
- **`test/visual/scenarios.ts`:** was 2 984 lines, now 261 (types and `SCENARIOS`). The rest went
  to `scenarioAssertions.ts` (611), `scenarioDefinitions1.ts` (1 074) and
  `scenarioDefinitions2.ts` (1 118). The `SCENARIOS` JSON dump is identical to HEAD.
- **`test/visual/capture.py`:** was 6 577 lines. It now holds only the campaign driver: 513 lines
  with `run_scenario`, `capture_scenarios` and `main`. The rest went to:

  | File | Lines | Contents |
  | --- | --- | --- |
  | `capture_support.py` | 593 | paths, fixture counters, in-page check scripts, `STEP_NAMES`, `save_step`, `StepRecorder`, `CheckTrace` |
  | `capture_page_checks.py` | 1 109 | |
  | `capture_layout_checks.py` | 1 397 | |
  | `capture_comment_checks.py` | 1 236 | |
  | `capture_edit_checks.py` | 1 273 | |
  | `capture_final_checks.py` | 626 | |

  A script made the split. Each module holds a verbatim slice of the original lines, and the
  script checked that the slices cover every original line exactly once. Each module gets explicit
  imports that the script generated from the AST, and the script asserted that no module uses a
  name from a later module. A symtable check found no unresolved global and no unused import.
  Function names are unchanged (the trace keys on `check.__name__`).
- **Tests that read the capture source:** two site tests read it, and they now read the new files
  with the same assertions:
  - `test/site/e2eGroups.test.ts` scans the check code for scenario-id branching. It now scans all
    the `capture_*.py` modules plus `capture.py` before `def capture_scenarios`, and asserts that at
    least one module exists.
  - `test/site/scenarioInvariants.test.ts` reads `STEP_NAMES` from `capture_support.py`.
- **`test/integration/realInput.test.ts` (4 580 lines): left on the baseline.**
  - The integration runner only imports its `run`, so a split would be picked up through that
    import. But the scenarios share module-level mutable state (`workbenchPage`, and the
    `reloadsBefore` / `patchesBefore` counters), so a split would have to turn that state into
    shared setters across modules.
  - The skill's `coverage-map.py` parses `^async function scenario` from this one file.
  - Unlike every other split here, this one cannot be proven equivalent offline. The only check is
    the real-window run, and that run was not possible this round (screen locked).
- **New test:** `test/core/frontmatter/sameData.test.ts` compares `isSameData` with
  `util.isDeepStrictEqual` on more than 2 000 pairs of parsed YAML values (1.2 and 1.1 types,
  clones and near misses).
- **New test in `test/core/directives/registry.test.ts`:** the attribute rules accept only
  `data-*` names.
- **Setup-only changes (no assertion changed):** `okfFrontmatter.test.ts`,
  `schemaRegistry.test.ts`, `test/session/links.test.ts`, `test/visual/renderFixtures.ts` and
  `test/probe/previewProbe.ts` pass `nodeSchemaFiles`.
- **Protocol tests:** `hostToPage.test.ts` and `router.test.ts` use direct imports. The router test
  is renamed to "the router works as the page runtime bundles it", with identical assertions.

## Equivalence proofs

Each harness compared the HEAD compiled `out/src` with the new one.

- **Renderer:** HTML and diagnostics are identical on 117 repository Markdown files plus 703
  Markdown inputs harvested from the tests, each with and without a render context.
- **Frontmatter:** analysis and patch results are identical on 54 files, 18 of them with a schema.
- **Edit actions:** about 197 000 cases are identical, with a fixed clock for thread timestamps.
- **Styles:** a dump of every previewStyles export is identical.
- **Scenarios:** the `SCENARIOS` JSON dump is identical.

## CSS byte-identity proof

`npm run bundle` on the worktree, compared with the HEAD build in the scratchpad:

```text
SAME preview.css            (cmp -s)
0b733642762cbbe978641e4599ab98c6b55ab4846bd4ddd066d04d62be27fd6b  out/bundle/preview.css
0b733642762cbbe978641e4599ab98c6b55ab4846bd4ddd066d04d62be27fd6b  <HEAD build>/preview.css
SAME mermaidPreview.js
SAME plantumlPreview.js
```

`preview.js` (287.9 kB on HEAD, 287.1 kB now) and `extension.js` differ because the code moved.

## Exceptions removed (`.dependency-cruiser.cjs`)

- `RENDERER_SPLIT` is removed.
- `src/core/frontmatter/okfFrontmatter.ts` goes from `fs`, `path`, `util` to `path` only
  (`PATH_SHIM`).
- `src/core/render/renderPipeline.ts` goes from `path`, `perf_hooks` to `path` only (`PATH_SHIM`).
- No entry was added. The new core files import no Node built-in.
- `check-boundaries` passes on 252 modules.

## Size baseline (`scripts/file-size-baseline.json`)

| File | Before | After |
| --- | --- | --- |
| `src/core/frontmatter/okfFrontmatter.ts` | 1 720 | removed (516) |
| `src/core/preview/previewStyles.ts` | 4 179 | removed (119) |
| `src/core/render/mystRenderer.ts` | 1 934 | removed (439) |
| `src/page/modules/editActions.ts` | 1 746 | removed (307) |
| `src/page/modules/editPalette.ts` | 1 191 | removed (766) |
| `test/core/render/mystFeatures.test.ts` | 1 711 | removed (1 256) |
| `test/integration/realInput.test.ts` | 4 580 | 4 580 (kept, see above) |
| `test/visual/capture.py` | 6 577 | removed (513) |
| `test/visual/scenarios.ts` | 2 984 | removed (261) |

The baseline goes from 9 entries to 1. It was produced with
`node scripts/check-file-sizes.mjs --update` and only removes entries.

## Small items

- **Directive attribute rules:** limited to `data-*`. `directiveAttributeAllowed` in
  `src/core/directives/registry.ts` refuses other names when the registry loads. It also refuses
  the three sanitizer-owned names (`data-myst-table-style`, `data-okf-color`,
  `data-okf-background`). The `directive.ts` doc says so.
- **CONTRIBUTING:**
  - "Add a setting": a `liveSetting` still needs its own update message in `hostToPage.ts`, posted
    by the session and handled in `hostHandlers.ts`, as `preview.showComments` does. Boot settings
    are the `startupSetting` and `liveSetting` entries of `PREVIEW_SETTINGS`.
  - New section "Inside the core": the renderer passes and the `NODE_RULES` dispatch, the
    frontmatter split and the `SchemaFiles` port, and the `styles/` folder with why it is
    TypeScript.
  - The boundaries text now gives the removal plans and the example of the port. The directive
    recipe now names `styles/contentBlockStyles.ts`, the `data-*` rule and the two rendering test
    files.
- **justfile:** the ci-static comment now lists the settings schema check.
- **coverage-map.py:** the stale path is fixed (`src/page/(runtime\.ts|features/)`). It now reads
  every `scenario*.ts` and `capture*.py`, and gets the same counts as HEAD: 150 scenario ids and
  56 machine checks.
- **Stale comments fixed:** `test/visual/scenarioIds.ts`, `test/visual/scenarios.ts` and
  `test/shared/geometry-checks.js`.
- **README:** it has no architecture section and only points to CONTRIBUTING, so it is unchanged.
- **CHANGELOG:** unchanged. It already has the single Unreleased contributor bullet, which points
  to "Architecture" in CONTRIBUTING.

## Gates (worktree, foreground, nothing left running)

- `fnm exec -- npx tsc -p .`: exit 0, no output.
- `fnm exec -- npm run test:unit`: 2 305 tests, 2 305 passed, 0 failed. HEAD of S8b had 2 302;
  the 3 new ones are 2 for sameData and 1 for the registry.
- `UV_NO_CONFIG=1 UV_OFFLINE=1 just check`: exit 0.
  - check-boundaries: passed (252 modules)
  - check-limits: passed (600 files, 1 on the size baseline)
  - check-settings: passed (18 settings)
  - pytest: 31 passed
- `UV_NO_CONFIG=1 UV_OFFLINE=1 just visual`: exit 0, `{"status": "passed", "scenario_count": 320,
  "screenshot_count": 210}`. No baseline PNG changed (`git status` shows no `.png`).
- `fnm exec -- npm run bundle`: exit 0. `preview.css` is byte-identical (see above).
- `npm run test:integration`: **not run.** `ioreg -n Root -d1 -a | grep -A1
  CGSSessionScreenIsLocked` printed `<true/>`, so the screen was locked. The window lock was not
  taken.

## Autonomous decisions

- **CSS stays as TypeScript modules, not `.css` files.** The unit tests,
  `test/visual/renderFixtures.ts` and the integration `stockCoexistence.test.ts` (inside the VS
  Code extension host) import the stylesheet from the tsc-compiled `out/` tree, where a `.css`
  import would not resolve. The stylesheet is split into per-feature template-literal modules, and
  their joined output is byte-identical.
- **The `SchemaFiles` port is synchronous and read-only**, because the frontmatter analysis is
  synchronous today. Making it async would change timing, which does not belong in a pure move. It
  sits on `HostServices` next to the other ports.
- **Path arithmetic keeps its `PATH_SHIM` entries** in okfFrontmatter, mystRenderer and
  renderPipeline. Only `fs`, `util` and `perf_hooks` were removed.
- **Test setup now passes `schemaFiles`**, because the option is required.
- **The router test is renamed**, because it no longer re-implements the bundle.
- **`realInput.test.ts` is not split**, for the reasons above.
- **The remaining directives stay where they are:** version admonitions, `{include}`, `{uml}` and
  the table-style branch. The brief makes them optional, and each is wired into a tree pass whose
  order is part of the output.
- **Instruction conflict:** the workspace AGENTS.md asks for `just preflight` before a commit, but
  the brief forbids it. It was not run.

## Open points

- Run `npm run test:integration` on an unlocked screen, under the window lock.
- Optional follow-up: move version admonitions, `{include}`, `{uml}` and the table-style branch to
  directive plug-ins.
- `realInput.test.ts` stays at 4 580 lines on the baseline. A split needs the module state turned
  into shared setters and a real-window run to prove it.
- Python now writes `test/visual/__pycache__/` for the capture modules. It is git-ignored, and
  `just clean` does not remove it.
- `git status` lists the `.venv` symlink as untracked: do not stage it.

## Paths to stage (75; excludes node_modules and .venv)

```text
.agents/skills/markdown-studio-exploratory-qa-claude/scripts/coverage-map.py
.dependency-cruiser.cjs
CONTRIBUTING.md
justfile
scripts/file-size-baseline.json
src/core/directives/directive.ts
src/core/directives/registry.ts
src/core/frontmatter/frontmatterParse.ts
src/core/frontmatter/frontmatterSerialize.ts
src/core/frontmatter/frontmatterValidate.ts
src/core/frontmatter/okfFrontmatter.ts
src/core/frontmatter/sameData.ts
src/core/frontmatter/schemaFiles.ts
src/core/preview/previewStyles.ts
src/core/preview/styles/commentStyles.ts
src/core/preview/styles/contentBlockStyles.ts
src/core/preview/styles/contentLayoutStyles.ts
src/core/preview/styles/editModeStyles.ts
src/core/preview/styles/editPaletteStyles.ts
src/core/preview/styles/frontmatterEditorStyles.ts
src/core/preview/styles/pageChromeStyles.ts
src/core/preview/styles/propertiesStyles.ts
src/core/protocol/hostToPage.ts
src/core/render/mystBlockTransforms.ts
src/core/render/mystContextTags.ts
src/core/render/mystEngine.ts
src/core/render/mystGithubAlerts.ts
src/core/render/mystInlineTransforms.ts
src/core/render/mystNormalize.ts
src/core/render/mystRenderer.ts
src/core/render/mystTables.ts
src/core/render/mystTypes.ts
src/core/render/renderPipeline.ts
src/host-api/index.ts
src/host-vscode/vscodeHost.ts
src/node-services/schemaFiles.ts
src/page/modules/blockEditActions.ts
src/page/modules/colourEditActions.ts
src/page/modules/editActionHelpers.ts
src/page/modules/editActions.ts
src/page/modules/editPalette.ts
src/page/modules/editPalettePopovers.ts
src/page/modules/inlineEditActions.ts
src/page/modules/linkEditActions.ts
src/page/modules/tableEditActions.ts
src/session/features/frontmatter.ts
src/session/features/links.ts
src/session/features/rendering.ts
test/core/directives/registry.test.ts
test/core/frontmatter/okfFrontmatter.test.ts
test/core/frontmatter/sameData.test.ts
test/core/frontmatter/schemaRegistry.test.ts
test/core/protocol/hostToPage.test.ts
test/core/protocol/router.test.ts
test/core/render/mystFeatures.test.ts
test/core/render/mystFeaturesSupport.ts
test/core/render/mystPaletteRendering.test.ts
test/probe/previewProbe.ts
test/session/links.test.ts
test/shared/geometry-checks.js
test/site/e2eGroups.test.ts
test/site/scenarioInvariants.test.ts
test/visual/capture.py
test/visual/capture_comment_checks.py
test/visual/capture_edit_checks.py
test/visual/capture_final_checks.py
test/visual/capture_layout_checks.py
test/visual/capture_page_checks.py
test/visual/capture_support.py
test/visual/renderFixtures.ts
test/visual/scenarioAssertions.ts
test/visual/scenarioDefinitions1.ts
test/visual/scenarioDefinitions2.ts
test/visual/scenarioIds.ts
test/visual/scenarios.ts
```
