# P10.0 setup plan (to apply in the studio repo after the PR exists)

Prepared 2026-10-22 from the okf-schema reference (`/Users/az02065/Projects/DevTools/okf-schema`,
branch `feat/schema-file-links` at `648729d`, tag `v0.13.0` = `62e4e88`) and a trial
`okfreq init` / `new` / `trace` / `update-coverage` / `generate-report` run in a scratch project.
Nothing here has been applied. Apply in this order, as one `build:` commit (plus one `docs:`
commit for AGENTS.md and the guideline if preferred), after D33 allows commits.

## 1. Prerequisite: okfreq 0.13.0 or newer (blocking)

The `okfreq` on PATH is **okf-schema 0.12.0** (`uv tool list`). Compared with the reference repo
(0.13.0 and HEAD), 0.12.0:

| Feature used by the okf-schema setup | 0.12.0 | ≥ 0.13.0 |
| --- | --- | --- |
| `lint --check` / `--diff` (stale navigation fails CI) | missing | yes |
| `lint/validate --check-links --project-root .` (x-okf-link targets) | missing | yes |
| `update-coverage --check` exits 1 when stale | exits 0 (verified) | exits 1 |
| Generated tier/scope `index.md` navigation (SwRS-OKFSCHEMA-OKFREQ-009) | no | yes |
| Schemas with `x-okf-link`, descriptions, `implemented_in_files`/`tested_in_files`/`verification_*` | minimal schemas | full |
| `okfreq init` guideline text (bundle `index.md`, log rules) | older | current |
| Installed `okfreq` skill ships `references/operations.md` | no (2 files) | yes |

Actions:

1. Local: `uv tool upgrade okf-schema` (or `uv tool install --force okf-schema==0.13.0`; if PyPI has
   no 0.13.0 yet: `UV_NO_CONFIG=1 uv tool install --force --from /Users/az02065/Projects/DevTools/okf-schema okf-schema`).
   Check: `okfreq lint --help` lists `--check` and `--check-links`.
2. Repo/CI: pin it in the project so CI does not depend on a user tool. Add to `pyproject.toml`
   `[dependency-groups]`: `requirements = ["okf-schema>=0.13.0"]`, run `uv lock`, and in
   `.github/workflows/ci.yml` change `uv sync --group docs` to `uv sync --group docs --group requirements`.
   (If 0.13.0 is not on PyPI: `okf-schema @ git+https://github.com/gsemet/okf-schema@v0.13.0`.)
   The justfile calls it through `uv run --no-sync --group requirements okfreq` (see §6).
3. Re-run `okfreq init` with the new version in a scratch dir and diff the schemas with
   `okf-schema/requirements/tiers/_schema/` before step 2 below (the trial here used 0.12.0).

## 2. Bundle location and init

- Bundle at **`requirements/`** in the repo root (same as okf-schema; `okfreq init .` would choose
  `.agents/requirements/`, which hides product contracts among agent files).
- `okfreq init requirements` creates `config.yml`, `guidelines/requirements.guidelines.md` (shipped
  baseline), `tiers/_schema/{base,strs,swrs}.schema.yaml`, `tiers/index.md`, `tiers/log.md`.
- Add `requirements/**` to `.vscodeignore` (not shipped in the VSIX; `test/security/package-contract.test.ts`
  may need its expected list updated).
- Add an authored `requirements/index.md` overview (copy the okf-schema one, adapted: two tiers,
  StRS = user use cases, SwRS = directly testable behaviour, link to `checklists` is NOT added
  because `.agents/changes/` is git-ignored).
- Dogfooding: the studio itself renders these files with schema validation and x-okf-link
  navigation (`_schema/` next to `tiers/`); open a few in the Studio editor as a manual check.

## 3. `requirements/config.yml`

```yaml
version: 1
levels:
  StRS: {folder: strs, prefix: StRS-MDOKFSTUDIO, derives_from: []}
  SwRS: {folder: swrs, prefix: SwRS-MDOKFSTUDIO, derives_from: [StRS]}
id_policy: scope-prefix-sequence
strs_test_coverage_mode: linked-swrs-and-validation-test
lifecycle:
  values: [draft, proposed, approved, deprecated, superseded]
markers:
  implements: '@implements_req'
  tests: '@tests_req'
  id_pattern: '[A-Za-z][A-Za-z0-9_-]*'
generated_fields: [derived_by, implemented_in_files, tested_in_files]
# scopes: generated from tools/scope-map.json, see below
```

IDs come out as `StRS-MDOKFSTUDIO-<TOKEN>-NNN` / `SwRS-MDOKFSTUDIO-<TOKEN>-NNN` (verified:
`okfreq new swrs … --scope gfm` → `tiers/swrs/gfm/SwRS-MDOKFSTUDIO-GFM-001.md`). Hyphenated scope
names (`frontmatter-editing`) work; `source_dirs: []` is accepted.

The `scopes:` block is generated from `tools/scope-map.json` (single source of truth; run
`node .agents/changes/archives/021-feature-session-007-020/p10-requirements/tools/scope-map.mjs` to check that
every tracked `src/`, `test/`, `sphinx/` file maps to exactly one scope or to tooling, and
`… scope-map.mjs --config` to print the block). Current output (append it to config.yml):

```yaml
scopes:
  rendering-core:
    id_token: CORE
    folder: rendering-core
    source_dirs:
      - src/render/renderPipeline.ts
      - src/render/mystRenderer.ts
      - src/preview/previewStyles.ts
      - src/build/sphinxBuild.ts
      - src/build/snapshotWorkspace.ts
      - src/build/sourceTransforms.ts
      - sphinx/conf.py
      - sphinx/preview_source_mapping.py
    test_dirs:
      - test/rendering/renderPipeline.test.ts
      - test/rendering/includeBudget.test.ts
      - test/rendering/includeMapping.test.ts
      - test/rendering/sphinxFeatures.contract.ts
      - test/build/sphinxBuild.test.ts
      - test/build/snapshotWorkspace.test.ts
      - test/build/sourceTransforms.test.ts
      - test/webview/inlineCode.test.ts
      - test/webview/previewStyles.test.ts
      - test/integration/projectFeatures.test.ts
      - test/visual/scenarios.ts
      - test/visual/scenarioIds.ts
      - test/visual/capture.py
      - test/visual/renderFixtures.ts
      - test/visual/themes.ts
      - sphinx/tests/test_sphinx_preview_mapping.py
      - test/visual/generatedFixtures.ts
      - test/visual/renderOptions.ts
  code-blocks:
    id_token: CODE
    folder: code-blocks
    source_dirs:
      - src/render/highlight.ts
      - src/webview/codeCopy.ts
    test_dirs:
      - test/rendering/highlight.test.ts
      - test/webview/codeCopy.test.ts
  gfm:
    id_token: GFM
    folder: gfm
    source_dirs:
      - src/render/checkboxMarkers.ts
      - src/webview/spanColors.ts
    test_dirs:
      - test/rendering/bareUrlAutolink.test.ts
      - test/rendering/checkboxMarkers.test.ts
      - test/rendering/checkboxRendering.test.ts
      - test/rendering/crlfAlerts.test.ts
      - test/webview/spanColors.test.ts
      - test/integration/checkboxToggle.test.ts
  myst:
    id_token: MYST
    folder: myst
    source_dirs:
      - src/myst/confLocator.ts
      - src/myst/confParser.ts
      - src/render/mystSyntaxDetect.ts
      - src/render/mathRenderer.ts
      - src/mapping/labelRename.ts
      - src/webview/labelRename.ts
      - src/webview/figureSizes.ts
    test_dirs:
      - test/rendering/mystFeatures.test.ts
      - test/rendering/mathRenderer.test.ts
      - test/rendering/mystSyntaxDetect.test.ts
      - test/rendering/confLocator.test.ts
      - test/rendering/confParser.test.ts
      - test/mapping/labelRename.test.ts
      - test/webview/labelRename.test.ts
      - test/integration/labelRename.test.ts
      - test/integration/mystDiagnostics.test.ts
  diagrams:
    id_token: DIAG
    folder: diagrams
    source_dirs:
      - src/render/plantUmlRenderer.ts
      - src/webview/mermaidPreview.ts
      - src/configuration/plantUmlConfiguration.ts
    test_dirs:
      - test/rendering/plantUmlRenderer.test.ts
      - test/configuration/plantUmlConfiguration.test.ts
  frontmatter-schema:
    id_token: FMSCHEMA
    folder: frontmatter-schema
    source_dirs:
      - src/frontmatter/okfFrontmatter.ts
      - src/frontmatter/propertiesTable.ts
      - src/frontmatter/schemaRegistry.ts
      - src/frontmatter/schemaValidator.ts
      - src/frontmatter/fileLinks.ts
      - src/frontmatter/stemIndex.ts
      - src/configuration/frontmatterConfiguration.ts
    test_dirs:
      - test/frontmatter/okfFrontmatter.test.ts
      - test/frontmatter/propertiesTable.test.ts
      - test/frontmatter/schemaRegistry.test.ts
      - test/frontmatter/schemaValidator.test.ts
      - test/frontmatter/fileLinks.test.ts
      - test/frontmatter/stemIndex.test.ts
      - test/frontmatter/fixtures.ts
      - test/configuration/frontmatterConfiguration.test.ts
      - test/integration/genericMarkdown.test.ts
  frontmatter-editing:
    id_token: FMEDIT
    folder: frontmatter-editing
    source_dirs: []
    test_dirs:
      - test/frontmatter/frontmatterPreservation.test.ts
      - test/frontmatter/frontmatterFence.test.ts
      - test/integration/previewEditing.test.ts
  layout-width:
    id_token: LAYOUT
    folder: layout-width
    source_dirs:
      - src/webview/widthMode.ts
      - src/webview/firstClearance.ts
    test_dirs:
      - test/webview/firstClearance.test.ts
      - test/webview/geometryChecks.test.ts
      - test/shared/geometry-checks.js
  theme-zoom:
    id_token: THEME
    folder: theme-zoom
    source_dirs:
      - src/state/previewTheme.ts
      - src/webview/viewControls.ts
    test_dirs:
      - test/state/previewTheme.test.ts
      - test/webview/creamTheme.test.ts
  toolbar-navigation:
    id_token: TOOLBAR
    folder: toolbar-navigation
    source_dirs:
      - src/preview/previewToolbar.ts
      - src/webview/toolbarCollapse.ts
      - src/webview/tocColumn.ts
      - src/webview/historyControls.ts
      - src/webview/linkNavigation.ts
      - src/state/navigationHistory.ts
      - src/state/previewViewPreferences.ts
      - src/navigation/previewNavigation.ts
    test_dirs:
      - test/webview/tocColumn.test.ts
      - test/webview/linkNavigation.test.ts
      - test/state/navigationHistory.test.ts
      - test/state/previewViewPreferences.test.ts
      - test/navigation/previewNavigation.test.ts
      - test/integration/previewHistory.test.ts
  block-editing:
    id_token: BLOCK
    folder: block-editing
    source_dirs:
      - src/webview/textEditing.ts
      - src/webview/blockSelection.ts
      - src/mapping/blockMove.ts
      - src/mapping/blockRange.ts
      - src/mapping/insertion.ts
      - src/mapping/textDiff.ts
      - src/state/editLock.ts
    test_dirs:
      - test/webview/textEditing.test.ts
      - test/webview/blockSelection.test.ts
      - test/mapping/blockMove.test.ts
      - test/mapping/blockRange.test.ts
      - test/mapping/insertion.test.ts
      - test/mapping/textDiff.test.ts
      - test/state/editLock.test.ts
      - test/integration/blockMove.test.ts
      - test/integration/blockClipboard.test.ts
      - test/integration/realInput.test.ts
      - test/integration/realInput/harness.ts
  palette-slash:
    id_token: PALETTE
    folder: palette-slash
    source_dirs:
      - src/webview/editActions.ts
      - src/webview/editPalette.ts
      - src/webview/slashMenu.ts
      - src/webview/linkPanel.ts
      - src/webview/figurePanel.ts
      - src/webview/figureDirective.ts
      - src/webview/pasteImage.ts
      - src/webview/hostRequests.ts
      - src/webview/caretRect.ts
      - src/mapping/imageReference.ts
      - src/mapping/pastedImage.ts
      - src/mapping/mystTargets.ts
      - src/preview/bibScan.ts
      - src/configuration/editingConfiguration.ts
    test_dirs:
      - test/webview/editActions.test.ts
      - test/webview/editPalette.test.ts
      - test/webview/slashMenu.test.ts
      - test/webview/figureDirective.test.ts
      - test/webview/caretReveal.test.ts
      - test/webview/hostRequests.test.ts
      - test/mapping/imageReference.test.ts
      - test/mapping/pastedImage.test.ts
      - test/mapping/mystTargets.test.ts
      - test/configuration/editingConfiguration.test.ts
      - test/integration/paletteMode.test.ts
      - test/integration/mystPickers.test.ts
      - test/integration/imagePicker.test.ts
      - test/integration/imagePaste.test.ts
  table-editing:
    id_token: TABLE
    folder: table-editing
    source_dirs:
      - src/webview/markdownTable.ts
    test_dirs:
      - test/webview/markdownTable.test.ts
      - test/webview/markdownTablePreservation.test.ts
  review-annotations:
    id_token: REVIEW
    folder: review-annotations
    source_dirs:
      - src/comments/anchoring.ts
      - src/comments/author.ts
      - src/comments/commentModel.ts
      - src/comments/commentStore.ts
      - src/render/commentMarkers.ts
      - src/webview/chipToggle.ts
      - src/webview/commentCompose.ts
      - src/webview/commentThreads.ts
      - src/webview/incomingChanges.ts
      - src/webview/incomingToggle.ts
      - src/git/headBaseline.ts
      - src/mapping/lineDiff.ts
      - src/configuration/commentsConfiguration.ts
    test_dirs:
      - test/comments/anchoring.test.ts
      - test/comments/commentEditing.test.ts
      - test/comments/commentModel.test.ts
      - test/rendering/commentMarkers.test.ts
      - test/webview/chipToggle.test.ts
      - test/webview/commentCompose.test.ts
      - test/webview/commentThreads.test.ts
      - test/webview/incomingChanges.test.ts
      - test/state/headBaseline.test.ts
      - test/state/headBaselineUserName.test.ts
      - test/mapping/lineDiff.test.ts
      - test/configuration/commentsConfiguration.test.ts
      - test/integration/incomingChanges.test.ts
      - test/integration/reviewComments.test.ts
      - test/integration/commentWrite.test.ts
      - test/integration/commentAnchors.test.ts
  lifecycle-sync:
    id_token: LIFE
    folder: lifecycle-sync
    source_dirs:
      - src/extension.ts
      - src/build/buildQueue.ts
      - src/preview/contentPatch.ts
      - src/preview/webview.ts
      - src/webview/scrollSync.ts
      - src/webview/anchorPolicy.ts
      - src/mapping/sourceMapping.ts
      - src/state/boundedState.ts
      - src/state/previewState.ts
      - src/configuration/previewConfiguration.ts
    test_dirs:
      - test/build/buildQueue.test.ts
      - test/mapping/sourceMapping.test.ts
      - test/state/boundedState.test.ts
      - test/state/previewState.test.ts
      - test/webview/scrollSync.test.ts
      - test/webview/anchorPolicy.test.ts
      - test/webview/contentPatch.test.ts
      - test/configuration/previewConfiguration.test.ts
      - test/shared/lineDelta.ts
      - test/integration/stockCoexistence.test.ts
      - test/integration/dirtySnapshots.test.ts
      - test/integration/sourceMapping.test.ts
      - test/integration/lifecycle.test.ts
      - test/integration/serializer.test.ts
      - test/integration/workspaceDisposal.test.ts
      - test/integration/scroll-sync-suite.ts
      - test/integration/reload-suite.ts
      - test/integration/extensionApi.ts
  trust-security:
    id_token: TRUST
    folder: trust-security
    source_dirs:
      - src/security/csp.ts
      - src/security/html-sanitizer.ts
      - src/security/resource-policy.ts
      - src/preview/previewMessages.ts
    test_dirs:
      - test/security/html-policy.test.ts
      - test/security/package-contract.test.ts
      - test/security/resource-policy.test.ts
      - test/security/userFacingText.test.ts
      - test/webview/previewMessages.test.ts
      - test/integration/trusted-suite.ts
      - test/integration/untrusted-suite.ts
      - test/integration/standalone-suite.ts
```

Tokens: CORE, CODE, GFM, MYST, DIAG, FMSCHEMA, FMEDIT, LAYOUT, THEME, TOOLBAR, BLOCK, PALETTE,
TABLE, REVIEW, LIFE, TRUST (folders = scope ids, as in `test/shared/e2eGroups.ts`).

### Scope mapping decisions (ambiguous files)

Key fact (from `marker_scan` in `okf_schema/okfreq/core.py`): markers are counted **globally**.
A marker for `SwRS-MDOKFSTUDIO-GFM-007` in `src/extension.ts` counts even though that file belongs
to `lifecycle-sync`. The scope mapping only decides *which files are scanned* (and the
documentation of ownership); each file is scanned once. So the "exactly one scope" rule is for
clarity, not a coverage constraint.

| File | Scope chosen | Why / caveat |
| --- | --- | --- |
| `src/extension.ts` (5023 lines) | lifecycle-sync | Host for every scope; markers of all scopes go next to their handler. |
| `src/webview/scrollSync.ts` (5206 lines) | lifecycle-sync | Page runtime for every scope (edit mode, editors, dispatch). |
| `src/preview/previewStyles.ts` | rendering-core | One stylesheet for rendering, layout, theme, toolbar, palette. |
| `src/security/html-sanitizer.ts` | trust-security | e2eGroups lists it under rendering-core too; the allow-list is a security control. |
| `src/render/mystRenderer.ts` | rendering-core | Single engine for CommonMark, GFM and MyST. |
| `src/frontmatter/okfFrontmatter.ts`, `propertiesTable.ts` | frontmatter-schema | Also hold the edit patch builders / edit controls ⇒ **frontmatter-editing has no exclusive source file** (`source_dirs: []`); its SwRS mark these files, `extension.ts` and `scrollSync.ts`. |
| `src/build/sphinxBuild.ts`, `snapshotWorkspace.ts`, `sourceTransforms.ts` | rendering-core | Not imported by `extension.ts` (only `buildQueue.ts` is); used by the Sphinx equivalence contract. Inventory must decide: product requirement, contract tooling, or dead code to flag. |
| `sphinx/conf.py`, `sphinx/preview_source_mapping.py`, `sphinx/tests/` | rendering-core | Python Sphinx source-mapping extension and its contract test (`# @…` markers). |
| `src/navigation/previewNavigation.ts` | toolbar-navigation | Link following; x-okf-link marker-line navigation SwRS (frontmatter-schema) mark it too. |
| `src/state/previewViewPreferences.ts` | toolbar-navigation | Persists all row 2–3 view preferences. |
| `src/mapping/mystTargets.ts`, `src/preview/bibScan.ts` | palette-slash | Feed the MyST pickers. |
| `src/mapping/lineDiff.ts` | review-annotations | Only used for incoming changes since HEAD. |
| `src/mapping/textDiff.ts` | block-editing | Minimal replacement for block, table and frontmatter edits. |
| `src/webview/caretRect.ts` | palette-slash | Caret anchor for slash menu and popovers. |
| `src/webview/spanColors.ts` | gfm | Colour spans; colour palette SwRS mark it too. |
| `test/visual/{scenarios,scenarioIds,renderFixtures,generatedFixtures,renderOptions,themes}.ts`, `capture.py` | rendering-core | One campaign for all groups; `// @tests_req` lines go above each scenario entry in `scenarios.ts` and `# @tests_req` above page-wide checks in `capture.py`. |
| `test/shared/geometry-checks.js` | layout-width | Page-wide geometry checks. |

Tooling (not scanned, no requirements): `test/site/`, `test/build/test_release.py`,
`test/build/marketplaceReadme.test.ts`, `test/build/cleanup.test.ts`, `test/release/`,
`test/reportPaths.ts`, `test/integration/run-tests.ts`, `test/integration/review-index.ts`,
`test/shared/e2eGroups.ts`, test helpers (`fakeDom.ts`, `rendering/dom.ts`) and fixture folders.
`scripts/` and `esbuild.mjs` are also out of scope. If the user wants release/packaging/gallery
behaviour under requirements, that needs a 17th scope (`dev-tooling`), which D32 does not
include: ask before adding it.

## 4. Schemas

Copy the three schemas from `/Users/az02065/Projects/DevTools/okf-schema/requirements/tiers/_schema/`
(or keep the ones `okfreq ≥ 0.13 init` generates if they are identical: check with `diff`) and
replace in their `examples:` and `description` texts `StRS-OKFSCHEMA-CORE-001` →
`StRS-MDOKFSTUDIO-CORE-001`, `SwRS-OKFSCHEMA-CORE-001` → `SwRS-MDOKFSTUDIO-CORE-001`,
`project: okf-schema` → `project: markdown-okf-schema-studio`,
`implemented_in_files: [src/okf_schema/okfreq/core.py]` → `[src/render/renderPipeline.ts]`,
`tested_in_files: [tests/test_okfreq.py]` → `[test/rendering/renderPipeline.test.ts]`,
`verification_criteria: The focused okfreq test suite passes.` → `The focused unit suite passes.`
No new fields are needed. Authored evidence fields to use from base.schema.yaml:
`documentation_files` (README.md, docs/*.md, CHANGELOG.md), `example_files` (test/visual/fixtures/*.md
showcasing the behaviour), `depends_on` (cross-scope dependencies), `owner: markdown-okf-schema-studio maintainers`,
`verification_method` / `verification_criteria` on every SwRS.

## 5. Guidelines

- `requirements/guidelines/requirements.guidelines.md`: the okfreq-shipped baseline written by
  `okfreq init` (do not edit; it is the same file as
  `okf-schema/src/okf_schema/data/requirements/guidelines/requirements.guidelines.md`).
  Unlike okf-schema (which links to its own source copy), the studio keeps the baseline in the
  bundle and adds the overlay as a second file.
- Local overlay `requirements/guidelines/project.guidelines.md` (text below). The `okfreq` skill
  only knows `requirements.guidelines.md` as the local guideline, so add one line at the very top
  of the baseline file pointing to the overlay — or (preferred, mirrors okf-schema) rename: keep
  the overlay as `requirements.guidelines.md` and store the baseline as
  `requirements/guidelines/okfreq-baseline.guidelines.md`, the overlay linking to it first.

Overlay text (preferred layout: this is `requirements/guidelines/requirements.guidelines.md`):

````markdown
# Requirements guidelines

This file specializes the [okfreq baseline](okfreq-baseline.guidelines.md) for the Markdown
OKF-Schema Studio VS Code extension. Read and follow the baseline first; the rules below supply
our paths, scopes, marker syntax and checks.

## Before editing

- The bundle is `requirements/`, documents under `requirements/tiers/`.
- Read `requirements/config.yml` and every schema under `requirements/tiers/_schema/`.
- Scopes are the 16 e2e groups of `test/shared/e2eGroups.ts` (frozen ids): rendering-core,
  code-blocks, gfm, myst, diagrams, frontmatter-schema, frontmatter-editing, layout-width,
  theme-zoom, toolbar-navigation, block-editing, palette-slash, table-editing,
  review-annotations, lifecycle-sync, trust-security. A new e2e group needs a new scope in the
  same change.
- Preserve requirement IDs, UUIDs, authored fields, unknown metadata and Markdown bodies.
- Use the shared vocabulary of `.agents/glossary/common.md` (palette, insert point, block editor,
  anchor icon, slash menu…) in titles and statements.

## Levels

- **StRS** (`StRS-MDOKFSTUDIO-<TOKEN>-NNN`): a user use case observable in VS Code (what a writer,
  reviewer or maintainer can do and see), with `--user-need`. No implementation detail, no
  message names, no pixel values.
- **SwRS** (`SwRS-MDOKFSTUDIO-<TOKEN>-NNN`): one bounded, directly testable behaviour of the
  extension (host, page or renderer), with `--derives-from` one or more StRS (any scope) and two
  GIVEN-WHEN-THEN scenarios (nominal and boundary/refusal). Settings, commands, messages,
  palette actions, slash entries and toolbar buttons each need their SwRS (accepted values,
  default, refusal of invalid/stale input).
- Page-wide properties checked on every visual scenario (no horizontal overflow, toolbar row
  layout per zoom, tooltip contrast, white/cream palette) are ONE SwRS each, in the scope of their
  subject (layout-width, toolbar-navigation, theme-zoom), not one per scenario.
- Families of equivalent assertions (code-blocks v05–v12, admonition galleries) map to one SwRS;
  a long scenario lock line is split into atomic SwRS.

## Creating

```console
okfreq new strs "<title>" --path . --project markdown-okf-schema-studio --scope <scope> \
  --description "When <trigger>, the Studio SHALL <observable outcome>." --user-need "<need>"
okfreq new swrs "<title>" --path . --project markdown-okf-schema-studio --scope <scope> \
  --description "When <trigger>, the extension SHALL <one bounded response>." \
  --derives-from StRS-MDOKFSTUDIO-<TOKEN>-NNN
```

Never write requirement frontmatter by hand and never reuse an ID; retire with
`okfreq archive <ID> --path . --yes` or `okfreq supersede <OLD> <NEW> --path . --yes`.
Use the frontmatter `title` verbatim as the first `##` heading (replace the generated
`## EARS Expression`). Replace every `<placeholder>`.

## Traceability markers (TypeScript, JavaScript, Python)

okfreq recognises a marker only at the **start of a line**, after optional indentation and one
comment opener (`//`, `#`, `/*`, `*`, `<!--`), followed by the ID:

```ts
// @implements_req SwRS-MDOKFSTUDIO-GFM-003
export function toggleCheckbox(...) { ... }

test("toggles the clicked box only", () => {
  // @tests_req SwRS-MDOKFSTUDIO-GFM-003
  ...
});
```

```python
# @tests_req SwRS-MDOKFSTUDIO-LAYOUT-001
def check_no_horizontal_overflow(page): ...
```

- Not recognised: a marker after code on the same line (`foo(); // @implements_req …`) and
  `/** @tests_req …` on the opening line of a JSDoc block (use `/*` or put it on a ` * ` line).
- Inside code that is stringified into the webview (`.toString()` factories in `src/webview/`),
  comments are kept in the page script: that is acceptable (no runtime effect) but keep markers
  out of template literals that produce HTML/CSS.
- One marker per ID per file (a second one is reported as a duplicate); put it next to the main
  implementation point or the first test of the behaviour.
- `@implements_req` only in configured `source_dirs`, `@tests_req` only in `test_dirs` (other
  occurrences are ignored). Only SwRS get `@implements_req`.
- StRS test markers only on real stakeholder validation tests: integration suites under
  `test/integration/`, the real-input harness, and visual scenarios (`test/visual/scenarios.ts`),
  as required by `strs_test_coverage_mode: linked-swrs-and-validation-test`.
- `package.json` contributes (JSON, no comments): mark the TypeScript that reads the setting or
  registers the command (`src/configuration/*.ts`, `src/extension.ts`), and list `package.json` in
  the SwRS `documentation_files` only when it documents the setting text.
- A visual scenario's `@tests_req` goes on its own line directly above the scenario entry in
  `test/visual/scenarios.ts`; page-wide checks get theirs above the check function in
  `test/visual/capture.py` or `test/shared/geometry-checks.js`.

## After editing

```console
okfreq update-coverage requirements
okfreq validate requirements --prose --check-links --project-root .
okfreq lint requirements --prose --check-links --project-root .
okfreq trace requirements --json
just requirements-report
just check
```

`just preflight` remains the completion gate. Do not claim traceability when a non-exempt SwRS
lacks source or test markers, a marker names an unknown ID, or tests fail. An SwRS that cannot be
tested in this repository (for example a manual check on a locked screen) sets
`annotation_exemption: true` with an `exemption_reason`.

## Navigation and history

- `requirements/index.md` is authored; `okfreq lint requirements` regenerates the marked blocks of
  `requirements/tiers/**/index.md` (never hand-edit between the `okfreq:index` markers).
- Append substantive changes (IDs, why, verification results) to `requirements/tiers/log.md`,
  newest date first; never invent approvals or results.
- Every behaviour change (feature or fix) updates its SwRS (or adds one), the markers, README /
  CHANGELOG and tests in the same change.
````

## 6. justfile recipes and wiring

```just
okfreq := env("STUDIO_OKFREQ", "uv run --no-sync --group requirements okfreq")

# Validate the okfreq requirements bundle: schemas, links, navigation and generated coverage.
requirements-lint:
    {{ okfreq }} validate requirements --check-links --project-root .
    {{ okfreq }} lint requirements --check --check-links --project-root .
    {{ okfreq }} update-coverage requirements --check

# Refresh generated coverage fields and navigation after adding requirements or markers.
requirements-update:
    {{ okfreq }} update-coverage requirements
    {{ okfreq }} lint requirements --prose --check-links --project-root .

# Write the requirements traceability report (JSON + Markdown) under out/reports/requirements/.
requirements-report:
    mkdir -p out/reports/requirements
    {{ okfreq }} generate-report requirements \
        --output-json out/reports/requirements/requirements-report.json \
        --output-summary-md out/reports/requirements/requirements-report.md
    {{ okfreq }} status requirements
```

Wiring (like okf-schema, which runs `requirements-lint` early and `requirements-report` late):

- `check: format compile unit contracts security release-tests requirements-lint`
- `preflight`: after `just sphinx-check || …`, add `just requirements-report || failures=$((failures + 1))`.
- `dev`/`update`: `uv sync --group docs --group release --group requirements`.
- CI: `uv sync --group docs --group requirements` (§1); `out/reports/` is already uploaded as the
  `studio-reports` artifact, so the report is downloadable from every run.
- Run `just format` and check the formatted justfile (CI diffs it).
- Optional: link `out/reports/requirements/requirements-report.md` from the site built by
  `test/site/buildSite.ts` (tooling change, not required for P10).

Stats report location: `out/reports/requirements/requirements-report.{json,md}` plus the
`.schema.json` okfreq writes next to the JSON. It contains the summary (SwRS source coverage,
SwRS test-link coverage, StRS test coverage under the configured mode, combined traceability),
per-scope table, per-StRS and per-SwRS tables (verified in the trial). Never write reports into
`requirements/`.

## 7. okfreq limitations found for a TypeScript project, and workarounds

| Limitation (verified on 0.12.0, same code on HEAD) | Workaround |
| --- | --- |
| Scanner reads every file under a listed path (`rglob("*")`, any extension, binary read with `errors="ignore"`), skips only `__pycache__`. Directory entries would also scan PNGs/fixtures. | List files, not directories (scope-map does). Keep fixtures out of `test_dirs`. |
| Marker must start the line after optional `#`, `//`, `/*`, `*`, `<!--`; trailing markers and `/** @…` are silently ignored (no warning). | Overlay rule + Sonnet review checks `okfreq trace --json` output against intended markers. |
| Same ID twice in one file ⇒ reported in `duplicates` (not an error). | One marker per ID per file. |
| Markers are not checked against the scope of the file (global counting). | Desired here (extension.ts, scrollSync.ts, scenarios.ts are multi-scope). |
| `@implements_req` only counted in `source_dirs`, `@tests_req` only in `test_dirs`; a marker in an unmapped file is silently ignored. | `scope-map.mjs` keeps every tracked src/test file mapped; tooling list is explicit. |
| JSON has no comments (`package.json` contributes cannot carry markers). | Mark the reading/registering TS code; checklist C-PKG rows link to the SwRS. |
| No test-result awareness: a marker is a link, not a pass. | `just preflight` stays the gate; P10.6 audits that tested_in_files suites run in CI (integration suites under xvfb). |
| StRS validation markers must also be in `test_dirs`; visual scenarios live in `test/visual/scenarios.ts` (mapped to rendering-core) ⇒ fine. | — |
| `okfreq new --scope` default is `default`: forgetting `--scope` creates `SwRS-MDOKFSTUDIO-…` in an unknown scope. | Always pass `--scope`; `validate` catches unknown scopes. |
| 0.12.0 only: no `--check`/`--check-links`, `update-coverage --check` exits 0. | Upgrade (§1). |

## 8. Skills

`okfreq install-skills --local-agents` (with okfreq ≥ 0.13) → `.agents/skills/okfreq/`
(`SKILL.md`, `references/operations.md`, `references/requirements.guidelines.md`) and
`.agents/skills/okfreq-gardening/SKILL.md`, next to the existing
`markdown-studio-exploratory-qa*` skills. Commit them (they are the maintenance skills the user
asked for). `--local-copilot` (`.github/skills`) is not used: this repo keeps skills in
`.agents/skills`. Re-run after each okfreq upgrade.

## 9. AGENTS.md section (insert after "Guidelines")

```markdown
## Requirements (okfreq)

- The product contract lives in `requirements/` (okfreq bundle, two tiers): StRS = user use
  cases, SwRS = directly testable behaviour. IDs `StRS-MDOKFSTUDIO-<TOKEN>-NNN` /
  `SwRS-MDOKFSTUDIO-<TOKEN>-NNN`; scopes = the 16 e2e groups of `test/shared/e2eGroups.ts`.
- Before touching requirements, read `requirements/guidelines/requirements.guidelines.md` (local
  rules, marker syntax for TypeScript/Python) and the okfreq baseline it links to. Skills:
  `.agents/skills/okfreq` (authoring, traceability) and `.agents/skills/okfreq-gardening` (audits).
- Every feature or fix updates its SwRS (or creates one with `okfreq new`), adds
  `// @implements_req <SwRS-ID>` next to the implementation and `// @tests_req <SwRS-ID>` next to
  the test, then runs `just requirements-update`; append a dated entry to
  `requirements/tiers/log.md` for substantive changes.
- Never reuse or hand-allocate IDs, never hand-edit `derived_by`, `implemented_in_files`,
  `tested_in_files` or the generated index blocks.
- `just check` runs `just requirements-lint`; `just requirements-report` writes the traceability
  report to `out/reports/requirements/` (also run by `just preflight` and published by CI).
```

Also add to the main targets list: `- Validate requirements: just requirements-lint`,
`- Requirements traceability report: just requirements-report`.

## 10. `requirements/tiers/log.md` initial entry

```markdown
# Update Log

## 2026-10-2X

- Created the okfreq requirements bundle for the Markdown OKF-Schema Studio (post-plan P10, U30):
  two tiers (StRS, SwRS) with prefixes `StRS-MDOKFSTUDIO` / `SwRS-MDOKFSTUDIO` (U31), 16 scopes
  mapped to the e2e groups of `test/shared/e2eGroups.ts` (D32), strict StRS coverage mode
  `linked-swrs-and-validation-test`, generated coverage fields, local guideline overlay with the
  TypeScript/Python marker syntax, `just requirements-lint` in `just check` and
  `just requirements-report` in `just preflight`. No requirements yet; they are backfilled scope by
  scope from the inventories of the existing behaviour.
  Verification: <actual okfreq validate/lint output and `just check` result>.
```

## 11. Commit plan (after the PR exists)

1. `build: add okfreq requirements bundle and checks` — pyproject/uv.lock group, ci.yml, justfile,
   `.vscodeignore`, `requirements/` (config, schemas, guidelines, indexes, log), `.agents/skills/okfreq*`.
2. `docs: describe the requirements workflow in AGENTS.md`.
3. Per scope: `docs: add <scope> stakeholder and software requirements`, then
   `test: trace <scope> requirements in code and tests` (markers), then gap tests.
Each commit ends with `Assisted-by: Claude:Sonnet-5.5` and no Co-Authored-By (user's repo rule, D35).
okfreq binary: `/Users/az02065/Projects/DevTools/okf-schema/.venv/bin/okfreq` locally (D34); the
uv group pin + CI wiring in commit 1 is deferred until the user approves the install.
