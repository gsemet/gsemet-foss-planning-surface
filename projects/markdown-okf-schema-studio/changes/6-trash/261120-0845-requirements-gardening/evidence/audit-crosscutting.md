# Requirements gardening: cross-cutting audit (A missing StRS, B diagrams, C deletion)

Read-only audit of `markdown-okf-schema-studio` at `main` (dedbdb2a), 2026-11-17. Nothing was changed in
the repository; experiments ran on a scratch copy (`src test sphinx skills requirements` +
`scripts/check_main_paths.py`) with the repo's own `uv run --no-sync --group requirements okfreq`.
Paths are repository-relative.

Baseline (scratch copy, identical to main): `okfreq validate --check-links` = 1124 requirements,
0 errors, 27 W2 warnings (broken placeholder cross-links such as `<url>` in SwRS-PALETTE-264,
-109, -153, -203, -217); `lint --check` and `update-coverage --check` clean;
`check_main_paths.py` = "78 StRS checked, 536 SwRS citations, all valid". Inventory: StRS
62 proposed + 16 approved + 2 draft = 80 in force; SwRS 465 proposed + 10 draft = 475 in force;
retired 61 deprecated (2 StRS, 59 SwRS) + 508 superseded (51 StRS, 457 SwRS) = 569.

## A. Missing StRS

Product surface read: `README.md:30-200`, `package.json` `contributes` (11 commands, 1 custom
editor `markdown-okf-schema-studio.editor`, 8 keybindings, 19 settings in 5 groups, 3 menus),
`docs/user/*.md`, `test/shared/e2eGroups.ts:21-37` (16 groups) and its `INTEGRATION_TESTS`.
At SwRS level almost every surfaced feature is covered; the gaps are at StRS level: features
filed under an StRS whose title and user_need do not mention them, so a reviewer reading the
use cases never learns they exist.

### A1. Use cases with no StRS of their own (proposed new StRS)

| # | Proposed title / scope | user_need sketch | Today's SwRS (wrong parent) | Code and tests to trace |
| --- | --- | --- | --- | --- |
| 1 | "A writer draws Vega-Lite and Vega charts from inline data or a CSV file" / diagrams | As a writer, I put a chart fence in my document and see a themed chart, from inline data or a data file next to the document, with nothing executed or fetched | SwRS-DIAG-121..124 derive from StRS-DIAG-001 ("…Mermaid diagrams…"); palette side SwRS-PALETTE-265 | `src/page/modules/vegaPreview.ts`, `src/core/render/mystNormalize.ts:54-58` (vega kind); docs `docs/user/charts.md`; README "Charts, no executable" |
| 2 | "A writer or reviewer decides between the options of a plan with one click" / gfm | As a reviewer of an agent's plan, I pick one of the `( )`/`(x)` options in the preview and at most two source lines change in one undo; on GitHub the text stays readable | SwRS-GFM-039 derives from StRS-GFM-003 ("toggles task checkboxes") | grep `@implements_req SwRS-MDOKFSTUDIO-GFM-039` in `src/`; README "Decide in the page" |
| 3 | "An agent writes Markdown that Studio renders well, from the shipped writing skill" / rendering-core | As a writer working with a coding agent, I install the Studio plugin in my agent host and the agent writes cards, tabs, admonitions, charts and diagrams that Studio renders without error | SwRS-CORE-073, -074, -075 derive from StRS-CORE-001 ("reads a faithful rendering") | `skills/writing-for-markdown-okf-schema-studio/`, `plugin.json`, `.github/plugin/marketplace.json`, `test/build/test_plugin_manifests.py`; README "Usage with coding agent" |
| 4 | "A reviewer reads the requirements, the reports and the screenshot gallery on the published site" / rendering-core (or toolbar-navigation) | As a reviewer, I browse use cases, behaviours, coverage and the e2e gallery on GitHub Pages without building anything | SwRS-CORE-069, -080..-086 derive from StRS-TRUST-014 ("built from pinned dependencies") — wrong scope and wrong need | `test/site/buildSite.ts`, `test/site/requirementsViewer/*` and their `*.test.ts` |
| 5 | "A maintainer releases a version only after green checks and reviewed release notes" / rendering-core (or trust-security next to TRUST-014) | As a maintainer, a version is tagged only after the heavy CI run is green and its release notes are reviewed | SwRS-CORE-076, -078 derive from StRS-CORE-001 | `.github/workflows/ci.yml`, `test/build/test_release.py`, `just release-notes-check` |

Edge cases, not new StRS but retitle candidates: `Save` from the preview (SwRS-LIFE-173, folder
lifecycle-sync) hangs under StRS-BLOCK-008 "types and moves between blocks with text editor keys";
inline SVG blocks and click-to-source on any picture (SwRS-DIAG-125, -126, -127) hang under the
Mermaid StRS-DIAG-001 — the cleanest fix is to retitle DIAG-001 to "A writer reads and inserts
Mermaid diagrams and SVG pictures that follow the theme" once charts leave it (A1-1).

### A2. Shipped features whose StRS is still `draft`

StRS-TOOLBAR-002 (fold sections) and StRS-TOOLBAR-003 (find and replace) and their SwRS
TOOLBAR-003, -004, -005, -006, -008, -009, -010, -011, -012, -014 are `draft`, yet the commands
`foldAll`, `unfoldAll`, `find` are in `package.json`, `docs/user/folding.md` and
`docs/user/find.md` document them, and markers exist (e.g. `src/core/state/headingFold.ts:25,63`,
`src/core/find/findMatches.ts:51,69`, `src/core/edits/findReplace.ts:203`; tests
`test/integration/findInPreview.test.ts`, `test/page/modules/headingFold.test.ts`). The shared
guideline (`requirements.guidelines.md:124-126`) says a draft on the default branch is a gap:
candidates for `proposed`, owner decision.

### A3. Use cases spread confusingly / over-broad StRS

- StRS-CORE-001 is a grab-bag (52 derived): rendering, performance (SwRS-CORE-070), find
  (CORE-043), writing skill and plugin (CORE-073..075), CI tagging (CORE-076), release notes
  (CORE-078), glow (LIFE-094), protocol envelope (TRUST-052). Moving A1-3 and A1-5 out leaves a
  coherent "faithful rendering" use case.
- StRS-DIAG-001 holds Mermaid + charts + SVG pictures + two review SwRS (SwRS-REVIEW-017 quote
  highlight, -038 Comment button, both also deriving from DIAG-006): the review ones are odd
  parents and should drop DIAG-001/006 from `derives_from` unless the diagram exclusion is the point.
- Very large StRS (by in-force + retired derived_by): PALETTE-001 (54), CORE-001 (52), MYST-001
  (50), FMEDIT-008 (44), DIAG-007 (43). Splitting is for the per-scope auditors; flagged only.
- StRS-GFM-003 user_need speaks of checkboxes only although it also carries radio choices (A1-2).

### A4. StRS whose scope folder looks wrong

- StRS-TRUST-014 (trust-security) parents eight rendering-core SwRS about the site viewer
  (CORE-069, -080..-086): the site needs its own StRS (A1-4); TRUST-014 keeps TRUST-074/-075.
- StRS-TRUST-012 "Visible text and the icon speak of the product" is branding, not trust; it fits
  rendering-core. TRUST-012 and TRUST-014 are also the 2 in-force StRS without `### Main paths`
  (hence 78/80 in `check_main_paths`).
- Cross-scope derivations are frequent and mostly legitimate (trust SwRS deriving from feature
  StRS: 12 to block-editing, 8 to palette-slash, 7 to toolbar-navigation); not a finding by itself.

## B. Diagrams on GitHub Pages

### What a use-case page renders today

`test/site/requirementsViewer/model.ts:254-286` reads the okfreq report JSON
(`out/reports/requirements/requirements-report.json`, `model.ts:376-377`): per requirement it
keeps `title`, `description`, `user_need` (frontmatter), and from the body `entry.text` only the
scenarios (`parseScenarios`, `model.ts:153`), the `Known issue:` lines (`model.ts:176`) and, for
an active StRS, the `### Main paths` section (`model.ts:327-334`, parser `mainPaths.ts:31-58`).
`useCasePage` (`pages.ts:80-107`) then emits: eyebrow + title (`pages.ts:92-93`), the user_need
as a blockquote (`pages.ts:94`), the metro map drawn from Main paths (`pages.ts:66-78`, `metroSvg`
in `layout.ts`), the behaviour list and retired rows (`pages.ts:89-97`). The StRS `description`,
"Normative behavior", "Preserved stakeholder intent", "Rationale and constraints" and any other
Markdown of the body are not shown (description only feeds the meta description when there is no
map, `pages.ts:99-101`). So today the body is invisible except Main paths.

### What exists to draw with

- Runtime deps: `mermaid ^12.2.0`, `@plantuml/core 1.2026.9`, `vega`, `vega-lite`
  (`package.json` dependencies); `node_modules/mermaid/dist/mermaid.min.js` and `.esm.min.mjs`
  exist. Studio's Mermaid bundle is `src/page/modules/mermaidPreview.ts` (webview-bound, theme via
  `themeVariables` at `mermaidPreview.ts:72-93`), built by `scripts/page-bundle.mjs:96`.
- The site build already launches headless Chromium (`playwright-core`) for social cards:
  `test/site/socialCard.ts:130` (`chromium.launch()`), and fails clearly when Chromium is absent.
- Site pages are plain static files, no CSP meta (`shell.ts:62-92`), one `viewer.js` +
  `search-index.js`; `write.ts:64-65` copies `viewer.css`/`viewer.js`, nothing else from the bundle.
- Docs pages go through `renderMyst` (`buildSite.ts:129-141`), which turns a `mermaid` fence into a
  figure placeholder (`mystNormalize.ts:143-146`) that only the webview draws: the site today draws
  no Mermaid anywhere.

### okfreq constraints (tested on the scratch copy)

Adding to StRS-TABLE-002 a `### Use case diagram` section with a ```` ```mermaid ```` fence and
`![Use case diagram](StRS-MDOKFSTUDIO-TABLE-002.svg)`, plus that SVG next to the file and a
`diagrams/` subfolder with an SVG: `validate --check-links` 0 errors (warnings unchanged),
`lint --check` "0 indexes would change", `update-coverage --check` "0 files would change",
`check_main_paths` unchanged. A link to a missing SVG is only a W2 warning, not an error, so a
project check would have to enforce it. Constraint: `mainPaths.ts:37` and
`check_main_paths.py:58` end the Main paths section at the next `### ` heading, so the diagram
section must sit before `### Main paths` (or after it, before the links block), never inside.

### Options

| Option | GitHub view | Plain OKF / text | Site | Cost / risk |
| --- | --- | --- | --- | --- |
| Mermaid fence in the StRS | Rendered natively by GitHub | Readable text | Needs Mermaid at build or in the browser | Low; one source of truth |
| PlantUML fence | Not rendered by GitHub (shows code) | Readable text | Needs the PlantUML engine with a DOM | Fails the GitHub requirement: reject |
| Committed SVG next to the StRS | Rendered as image | Image link only | Copy file in `write.ts` | Generated file to keep in sync with its source; drift; binary-ish diffs |

### Recommendation

Mermaid fence in an authored `### Use case diagram` section placed just before `### Main paths`
(one diagram per StRS, a flowchart of the use case's states, in the reader's words). On the site,
pre-render it at build time to inline SVG: in `model.ts`, extract the first ```` ```mermaid ````
block of that section into `Requirement.diagram`; in `write.ts`, open one Chromium page (same
pattern as `socialCard.ts:120-145`) that loads `node_modules/mermaid/dist/mermaid.min.js`, call
`mermaid.render()` per StRS with the site's cream `themeVariables`, and inline the SVG in
`useCasePage` under the user_need; on failure, show the source in a `<pre>` and fail the build in
CI (or count it in the home). Result: static SVG, no JS needed, no 3 MB runtime per page, works with
`noscript`. Cost: about 80-120 lines in `test/site/requirementsViewer/` + a unit test on extraction
and a build test on one fixture, plus a guideline paragraph in `project.guidelines.md` ("Use case
diagram of a StRS") and optionally a check in `check_main_paths.py` that every in-force StRS has
exactly one fence. Cheaper fallback (about 20 lines): copy `mermaid.min.js` to the site and call
`mermaid.run()` client-side; costs a ~3 MB download on each use-case page. Also worth deciding in
the same change: render the StRS "Normative behavior" and "Rationale and constraints" on the page,
since the reviewer cannot read them there today. Risk: a hand-drawn diagram can drift from Main
paths, which the existing metro map already draws from verified SwRS citations; keep the diagram
at use-case level (no SwRS IDs) so it does not compete with the map.

## C. Deleting retired requirements

### What the rules say

- Shared guideline: "Retire published requirements with `okfreq archive` or `okfreq supersede`,
  never by deleting the file" (`requirements.guidelines.md:75-76`); `okfreq retire` only for a
  never-published draft (`:77-82`); "Never delete a file without `okfreq retire`" (`:83-84`).
- Skill: "Never delete a published requirement; supersede or archive it"
  (`.agents/skills/okfreq-gardening/SKILL.md:234-236`, also `:217-221`).
- `okfreq retire --help`: refuses non-draft. Verified: `retire SwRS-…-DIAG-010` → "is deprecated,
  not draft; use archive or supersede"; same for superseded DIAG-002. After hand-flipping
  `req_lifecycle` to `draft`, `retire` succeeded: deleted the file, appended
  `retired_ids: [SwRS-…-DIAG-002]` to `config.yml`, added one line to `tiers/log.md` under today's
  date — but it also re-flowed the whole `config.yml` (144 lines changed, flow mappings re-wrapped).
- `config.yml` has no `retired_ids` today.

### Impact measured

References from in-force files to retired IDs: only generated fields. (a) deprecated: 59
`derived_by` entries in 30 in-force StRS; (b) superseded: 508 `supersedes` entries in 142 in-force
SwRS/StRS and 483 `derived_by` entries in 28 StRS (plus their generated Links blocks). No authored
`derives_from`, `depends_on`, `relates_to`, `superseded_by` or body text of an in-force file cites a
retired ID; no Main paths bullet does (`check_main_paths` all valid). No retired `superseded_by`
points to another retired ID. Among retired files: SwRS-BLOCK-249/-250 derive from deprecated
StRS-BLOCK-026 (delete them first); 5 body mentions inside deprecated files (THEME-024, BLOCK-227,
TRUST-050) vanish with them.

Markers: one stale `@tests_req SwRS-MDOKFSTUDIO-LAYOUT-021` (superseded by LIFE-169) at
`test/session/diagReq.viewState.requirements.test.ts:107`; the same test already carries
`@tests_req SwRS-MDOKFSTUDIO-LIFE-169` at `:106`, so the line is simply removed. After deletion
`okfreq trace --json` reports `missing_ids: [SwRS-MDOKFSTUDIO-LAYOUT-021]`; `validate` does not.
Other mention: `test/core/frontmatter/requirementSchemas.test.ts:50,56` uses
`SwRS-MDOKFSTUDIO-BLOCK-012` as a literal in a schema test (AJV only, unaffected).
`tiers/log.md`: 12 retired IDs mentioned (3 deprecated, 9 superseded), plain text in authored
history; keep them (log is never rewritten, `requirements.guidelines.md:268-271`).

Simulation on the scratch copy (delete files, append `retired_ids`, then `update-coverage`, `lint`):

| | (a) 61 deprecated | (b) all 569 retired |
| --- | --- | --- |
| `validate` right after deletion | 59 errors (E10 stale `derived_by`) | 1050 errors (stale `derived_by`/`supersedes`) |
| `update-coverage` | 30 files updated | 170 files updated |
| After `update-coverage` + `lint` | `validate` 1063 requirements, 0 errors, 27 warnings; both `--check` clean; main paths valid | `validate` 555 requirements, 0 errors, 26 warnings; both `--check` clean; main paths valid |
| Diff | 107 files, -3626 lines | 766 files, +712 / -36208 lines |

Site viewer: `RETIRED_LIFECYCLES` (`model.ts:9`), `retiredBehavioursOf` (`model.ts:385-387`),
`replacementsOf` (`model.ts:390-394`), `retiredNote` and retired rows (`pages.ts:17-24, 39-40,
89-90, 186-189`), the History toggle (`shell.ts:78-80`), the retired table on the home
(`home.ts:109-128`) and the `· retired` search tag (`viewer.js:26`) all become empty but keep
working (home shows "None"). Their tests use the synthetic `requirementsViewer/fixture.ts`, so they
stay green. SwRS-CORE-083 "The site requirements viewer keeps retired requirements behind History"
stays true but vacuous; keep it (future supersessions will produce retired files again) unless the
owner also decides "delete at supersession" from now on, in which case CORE-083 and that code are
retired in the same change.

### Proposed procedure (one PR, owner-approved exception)

1. Record the decision in `requirements/guidelines/project.guidelines.md` (project rule wins over the
   shared text), e.g.: "### Deleting retired requirements — Superseded and deprecated requirements
   are deleted from `tiers/` once their replacements are in force; git history keeps them. The
   deletion records every ID in `retired_ids` of `config.yml` so no number is reused, and one
   `tiers/log.md` entry lists the IDs. This replaces, for this bundle, the shared rule 'never
   delete a published requirement'." Log the owner's agreement in the change spec; the 16 approved
   StRS only lose generated fields (no meaning change), so no re-approval is needed.
2. Remove the stale marker at `test/session/diagReq.viewState.requirements.test.ts:107`.
3. Delete with a small script, not 569 `okfreq retire` calls: `git rm` each retired file
   (BLOCK-249/-250 before BLOCK-026), append a sorted `retired_ids:` list to `config.yml` by text
   (avoids okfreq's full re-flow), one dated `tiers/log.md` entry (`## YYYY-MM-DD` / `### Topic`)
   with the counts and the ID list or a pointer to the commit.
   Alternative staying inside the tool: flip each to `draft` then `okfreq retire ID --reason … --yes`
   (works, verified), at the price of 569 log lines, a re-flowed `config.yml`, and abusing the
   "never published draft" semantics; not recommended.
4. `just requirements-update` (update-coverage + lint), then `just requirements-lint`,
   `uv run --no-sync --group requirements okfreq trace requirements --json` (missing_ids empty),
   `just requirements-report`, `just preflight`.
5. Do (a) and (b) in the same PR, or (a) first if the owner wants a smaller review; the procedure is
   identical.

### Risks

- The shared guideline and skill forbid it; `okfreq init --force` will not undo the project rule,
  but future agents loading only the skill may flag the deletion — the project guideline must say it.
- Lost on-tree history: the viewer's "superseded by" trail and the History view disappear; rationale
  for old decisions lives only in git and `log.md`.
- `retired_ids` adds 569 lines to `config.yml`; required, because `okfreq new` numbers from the
  highest ID ever used (`requirements.guidelines.md:71-74`) and a deleted highest number would be
  reused otherwise.
- Hand deletion without `retired_ids` would pass `validate` silently; the simulation shows the
  checks catch stale generated fields but not a missing `retired_ids` entry.
- Open PRs or branches citing a deleted ID in markers or `derives_from` break on rebase: run the
  deletion when no requirement-touching PR is open.
- Validation-test counts and the home "retired" table change; any doc or screenshot quoting
  "1124 requirements" or the retired counts needs a refresh.
