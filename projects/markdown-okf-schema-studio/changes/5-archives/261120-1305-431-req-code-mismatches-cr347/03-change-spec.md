# Change Specification: settle the five code/requirement mismatches left by CR-347

## Goal

CR-347 (PR 418, merged 2026-11-20) wrote five SwRS as the code behaves today, each with a
"Known issue" line, instead of fixing them: SwRS-MDOKFSTUDIO-CORE-010, CORE-025, DIAG-005,
DIAG-009 and TRUST-042. In the owner's words, for each one: decide whether the code or the SwRS is
right, and fix the other. After this CR, none of the five carries the CR-347 known issue: either
the code (and its test) now does what the SwRS said, or the SwRS states the current behaviour as
intended, with no "Known issue" line.

## Decisions carried from `02-answers.md`

- For each of the five, the Driver decides, with evidence (code, tests, git history, docs), whether
  the code or the SwRS is right, and fixes the other.
- The owner is asked only when an approved StRS or a real behaviour choice is at stake. Otherwise
  the Driver decides alone. Approved StRS that sit above these SwRS: StRS-MDOKFSTUDIO-CORE-001
  (above CORE-010) and StRS-MDOKFSTUDIO-DIAG-001 (above DIAG-005 and DIAG-009). Their text does not
  mention any of the five points, so a verdict should not need to touch them. If one does, the
  Driver stops and asks through the Foreman before changing the StRS.

## How each item is settled (applies to all five)

The project rules (constitution, section 1; `requirements/guidelines/requirements.guidelines.md`,
"Anchored to the code"; `requirements/guidelines/project.guidelines.md`, "During a change") give
two ways to close a known issue:

- **Code is wrong:** change the code, change the test that pinned the known-issue behaviour so it
  checks the SwRS behaviour, and remove the "Known issue" line from the SwRS, all in the same
  change. Per constitution section 3, the new or changed test fails on the previous code, and the
  PR body says why the assertion changed (it pinned a known bug).
- **SwRS is wrong (the behaviour is intended):** reword the SwRS's normative text, description and
  scenario rows so they state the current behaviour, remove the "Known issue" line, and keep or
  adjust the test that already checks it (drop the "Known issue" comment in the test).

For each item, the Driver writes its verdict and evidence in one or two lines. These lines go in
the PR body ("Tests" section, with the requirement IDs and their source and test files) and in the
dated entry of `requirements/tiers/log.md`.

Edit the SwRS files by hand only in their prose (normative text, `description`, `title` if
needed, scenarios, Known issues, Verification notes). Never edit generated fields or the
`okf:links` block. Then run `just requirements-update` and commit what it generates.

## The five items

### 1. SwRS-MDOKFSTUDIO-CORE-010: wikilinks between inline HTML tags

- File: `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-010.md`.
- The SwRS says: `[[...]]` stays unconverted in "raw HTML". The known issue says that
  `<span>[[Note]]</span>` inside a paragraph is converted, because the text between two inline
  HTML tags is a plain `text` node for the parser.
- Code: `expandWikiLinks` in `src/core/render/mystInlineTransforms.ts` skips nodes of type `html`
  (an HTML block, or one inline tag on its own), so the text between inline tags is converted.
  `autolinkBareUrls` in the same file follows the same rule for bare URLs (GFM-001), and CommonMark
  renders Markdown (emphasis, links) between inline tags in the same way.
- Test that pins the known issue: "wikilink syntax inside a link, an image, math, raw HTML or an
  embed is not converted" in `test/core/render/renderReq.coreRows.requirements.test.ts` (the
  `<span>[[InRawInline]]</span>` case).
- Evidence to weigh: whether converting matches the other inline transforms and CommonMark (if so,
  the SwRS is wrong: "raw HTML" means an HTML block or a tag itself, and text between inline tags
  is converted like any text); or whether some doc or history shows that inline HTML content was
  meant to stay literal. If the code changes, the rendered syntax changes: check
  `skills/writing-for-markdown-okf-schema-studio/` per
  `.agents/guidelines/writing-skill-maintenance.guideline.md` (today it does not mention
  wikilinks; update it only if the change concerns something it says or should say).

### 2. SwRS-MDOKFSTUDIO-CORE-025: the fallback message of a failed render

- File: `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-025.md`.
- The SwRS says: a first render that fails without a message shows "The render failed." on the
  "Preview unavailable" page, and a later failure without a message keeps "The latest render
  failed." on the stale page.
- Code: `renderPreviewDocument` in `src/core/render/renderPipeline.ts` (the `catch` around line
  320) wraps every failure in a `RenderError` whose message is `String(error)` when the thrown value
  is not an `Error`. `showRenderFailure` in `src/session/features/rendering.ts` and the first-render
  path in `src/session/previewManager.ts` (around line 424) use the fallback strings only when the
  error is not an `Error`, which never happens after the wrap, so both fallbacks are dead and the
  page shows for example "undefined". An `Error` with an empty message shows an empty message.
- Test that pins the known issue: "a first render that throws a value without a message shows the
  error page with that value as text" in `test/host/coreReq.requirements.test.ts`.
- Evidence to weigh: the fallback strings exist in the code and in the SwRS, so their intent is
  plain. If the code is fixed (for example, the pipeline keeps an empty message for a failure
  without one, and the callers use the fallback when the message is empty), the test checks "The
  render failed." for the first render; add a check for "The latest render failed." on the stale
  path if no test covers it (`test/node-services/build/buildQueue.test.ts` or the host harness),
  as the SwRS scenario "Failure after a good render" names it.

### 3. SwRS-MDOKFSTUDIO-DIAG-005: Mermaid border, secondary and tertiary colours in the picture

- File: `requirements/tiers/swrs/diagrams/SwRS-MDOKFSTUDIO-DIAG-005.md`.
- The SwRS's nominal scenario says that each part of the picture (node fill, text and lines,
  border, secondary and tertiary colours, background) takes its value from the theme variable in
  its table. The first known issue says that the visual check covers only node fills, and that the
  border, secondary and tertiary colours are checked only as the values given to Mermaid
  (`themeVariables` in `src/page/modules/mermaidPreview.ts`, test `the Mermaid border, secondary and
  tertiary colours come from their theme variables, with fixed fallbacks` in
  `test/page/modules/diagReq.pageDiagrams.requirements.test.ts`), not in the drawn picture.
- Drawn-picture check today: `check_mermaid_theme_switch` in `test/visual/capture_final_checks.py`
  (scenario `mermaid-map-dark` in `test/visual/scenarioDefinitions1.ts`, flag
  `mermaidThemeSwitch`). It checks the fill of a probe `g.node` against
  `--studio-textCodeBlock-background` in each theme mode.
- Two ways to settle it: extend that check so it also reads, in the drawn SVG, the stroke of the
  probe node against `--sphinx-preview-border`, and the colours Mermaid derives from
  `secondaryColor` and `tertiaryColor` for the parts the fixture `06-mermaid-map` draws (for
  example a cluster background), then remove the known issue. Or, if Mermaid does not draw those
  colours in a way the picture can check (for example, the fixture draws no part that uses them),
  reword the scenario so the picture claim covers only what is drawn, and state that the other
  values are checked as the values given to Mermaid. The other three DIAG-005 known issues (light
  mode redraw, fixed light fallbacks, edge labels checked by the visual campaign only) are not part
  of this CR and stay.

### 4. SwRS-MDOKFSTUDIO-DIAG-009: the Mermaid late-result guards cannot be reached

- File: `requirements/tiers/swrs/diagrams/SwRS-MDOKFSTUDIO-DIAG-009.md`.
- The known issue says that the guard against a late error for a replaced key in
  `src/page/modules/mermaidPreview.ts` (the `catch` around line 141:
  `if (drawnKeys.get(diagram) !== key) return;`) cannot be reached: draw passes run one at a time
  (`renderQueue`) and a pass plans each node once, so no node changes key while its drawing runs.
  The "replaced key" row of the scenario "A late error for a replaced key is not shown" is tested on
  the built-in PlantUML engine instead (`a PlantUML drawing that fails after a newer render took the
  element shows no error` in `test/page/modules/diagReq.pageDiagrams.requirements.test.ts`).
- The same reasoning applies to the picture guard just above
  (`if (drawnKeys.get(diagram) === key) showImage(diagram, src);`, around line 139) and to the first
  row of the scenario "A late picture for a replaced key is not shown" (dark drawing finishing after
  the cream pass was planned). The test `a Mermaid drawing finished for an earlier theme never
  replaces the picture of the current one` in `test/page/modules/mermaidPreviewEntry.test.ts`
  (around line 129) resolves the dark drawing before the cream pass starts, so it does not show a
  late result being dropped. The Driver checks this guard too and settles both together.
- Two ways to settle it: make the guards reachable and test them on Mermaid (only if there is a
  real path where a node changes key during a drawing), or remove the dead guards (or keep them as
  plain defence with a comment) and reword the Mermaid rows of both scenarios to what happens:
  passes are serialised, so a later theme is drawn only after the running pass ends, and the rows
  for a replaced key hold for PlantUML and charts. The normative sentence "drop a result that
  arrives for a key the node no longer has" is rewritten to match. Move or remove the
  `@implements_req SwRS-MDOKFSTUDIO-DIAG-009` and `@tests_req` markers with the code and tests.
  The other four DIAG-009 known issues are not part of this CR and stay.

### 5. SwRS-MDOKFSTUDIO-TRUST-042: SVG `xlink:href` links get the navigation attribute

- File: `requirements/tiers/swrs/trust-security/SwRS-MDOKFSTUDIO-TRUST-042.md`.
- The SwRS rows say: an `xlink:href` the link rules block is removed without the navigation
  attribute; one they allow keeps its address without the navigation attribute.
- Code: the `href`/`xlink:href` branch of the attribute loop in
  `src/core/security/html-sanitizer.ts` (around line 457) gives `data-sphinx-preview-navigation`
  only when `name === "href"`. parse5 gives `xlink:href` the name `href` (with the prefix `xlink`),
  so the branch `name === "xlink:href"` is never taken and both SVG links get the attribute with
  their address, including the blocked `javascript:` one. Page code selects links with
  `a[data-sphinx-preview-navigation]` (`src/page/modules/linkNavigation.ts`,
  `src/page/features/linkEditing.ts`, `src/page/features/contentPatch.ts`), which also matches an
  SVG `a`, so these SVG links are routed by the host on a click.
- Test that pins the known issue: "an xlink:href the link rules block is removed; one they allow
  keeps its address" in `test/security/trustReq.pageBuild.requirements.test.ts`.
- Evidence to weigh: whether host routing of SVG links is wanted (then the SwRS rows are wrong and
  say the SVG link gets the attribute like an HTML link), or whether the code means to treat
  `xlink:href` apart (then the sanitizer must tell them apart, for example by the attribute's
  `prefix` or namespace, and the test checks that neither SVG link gets the attribute). A code fix
  changes what a click on an SVG link does in the preview: if the evidence does not settle it, it is
  a behaviour choice for the owner (see the decisions above).

## Requirements and traceability work

- For every SwRS touched: markers stay on the code and tests that carry the behaviour
  (`@implements_req`, `@tests_req` at each test), at most 3 IDs per marker block.
- Run `just requirements-update` and commit its generated files. Add a dated entry in
  `requirements/tiers/log.md` naming the five SwRS, each verdict (code or SwRS fixed) and the
  sources and tests.
- Before the PR opens: `uv run --no-sync --group requirements okfreq validate --check-links
  --project-root .` and coverage, as CI runs them.

## Out of scope

- The other known issues of DIAG-005 and DIAG-009, and every known issue of other SwRS.
- CR-430's MYST-019 numref mismatch, and other mismatches found by CR-348 or later CRs.
- The owner questions of PR 418 (CORE-002, TRUST-025 and the rest).
- Any change to the text of an approved StRS (CORE-001, DIAG-001) without the owner's word.

## Evidence

- Per item: the test named above, changed or kept per the verdict. A code fix comes with a test
  that fails on the previous code (constitution, section 3); the Driver runs it on the previous code
  once and writes the failure in its round notes.
- `just check` (unit, contract, security, markers, file size), `just requirements-lint`,
  `just requirements-update` with nothing left to commit.
- If DIAG-005's visual check is extended: the visual job (`just ci-visual`) proves it; on Windows
  `just preflight` runs only the static stage, so the PR's CI visual job is the proof, and the
  Driver names that job's run in the PR body.
- `just preflight` passes (constitution, section 4).
- PR body: one line per item with its verdict and evidence, and the requirement IDs with their
  source and test files.

## Open questions

None for now. The answers leave each verdict to the Driver. The only case for the owner is a real
behaviour choice the evidence does not settle (TRUST-042 and CORE-010 are the likely candidates),
or a change to an approved StRS.
