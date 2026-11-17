# Change specification: garden the requirements of rendering-core, diagrams and trust-security

Short name: `garden-cdt`

## Goal

A human reviewer understands the use cases of the rendering core, the diagrams and the trust and
security of Studio by reading their StRS, and can trust each StRS down to the code:

- each StRS states one use case, at a readable length, with a use-case diagram, and no text that
  contradicts its SwRS or the code;
- each SwRS is one observable behaviour, derived from the use case it serves; a shared rule is
  written once and cited with `depends_on`;
- each `@implements_req` sits on the code that does the behaviour, each `@tests_req` on a test that
  checks one of its scenarios, and every StRS has a validation test on a real scenario.

This change touches requirement text, markers and tests. It changes no product behaviour.

## Sources and authority

- The findings and the old-to-new mappings come from the audit of this group:
  `<planning>/changes/1-inbox/requirements-gardening/evidence/audit-core-diagrams-trust.md`
  (repository at `main` dedbdb2a). Line numbers below are from that commit: re-locate them by the
  function or test name, never by number alone.
- The missing use cases come from `audit-crosscutting.md` section A1 (rows 1, 3, 4, 5). Where the
  two reports differ, this specification follows the group report, as the owner's answers ask:
  the inline SVG pictures (DIAG-125..127) go with the charts into one new StRS (DIAG-001 is not
  retitled), and CORE-075 goes with the release StRS, not with the writing skill.
- `<planning>` is `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio`.
- Project rules that govern every step (read them before starting, do not restate them in
  commits): `.agents/constitution.md` (sections 1 and 3), `AGENTS.md` "Requirements (okfreq)",
  `requirements/guidelines/requirements.guidelines.md`, `requirements/guidelines/project.guidelines.md`
  ("Main paths of a StRS", "During a change", "Approved requirements"), the okfreq skills
  `.agents/skills/okfreq` and `.agents/skills/okfreq-gardening`.
- In this document IDs drop the `MDOKFSTUDIO-` part: `CORE-001` is `SwRS-MDOKFSTUDIO-CORE-001` or
  `StRS-MDOKFSTUDIO-CORE-001` as the column or sentence says.

## Decisions carried from 02-answers.md

1. Published requirements are never deleted. A merge supersedes the absorbed SwRS with
   `okfreq supersede OLD NEW --path requirements --yes`; a requirement that leaves the contract is
   archived with `okfreq archive`. No `git rm`, no `okfreq retire` (every requirement touched here
   is published).
2. The split into this CR and its six siblings is approved. This CR runs after
   `req-use-case-diagrams` and `req-marker-gate` and builds on what they add (see "Dependencies").
3. The specification follows the group audit; the owner did not review it before the run.
4. The owner keeps three decisions, which the Driver brings back and never takes alone:
   - re-approval of an approved StRS whose text changes (here CORE-001, DIAG-001, DIAG-006);
   - any `draft` to `proposed` change (none is planned here: every in-force SwRS of these scopes
     is already `proposed`);
   - a merge or split of this specification that the Driver doubts once it reads the code.
5. No spec critic: requirement text, markers and tests only.

## Dependencies

- `req-use-case-diagrams` adds to `requirements/guidelines/project.guidelines.md` the rule of the
  authored `### Use case diagram` section (one Mermaid fence, a sequence, actors or state diagram,
  placed before `### Main paths`) and its rendering on the requirements site. This CR writes the
  diagrams by that rule, as merged.
- `req-marker-gate` adds to `just check-markers` (`scripts/check-marker-companions.mjs`) a check
  that fails on an in-force, non-exempt SwRS without `@implements_req`, a cap of 3 IDs per marker
  comment, a companion rule (each ID names the scenario that checks it) and a baseline list of
  today's offenders that can only shrink. It also fixes DIAG-128 and the stale LAYOUT-021 marker.
  This CR removes from that baseline every entry of its own scopes it fixes, and must leave
  `just check-markers` green.
- The branch of this CR sits in the stack above those two (see `stacked-prs.guidelines.md`). When
  a rebase conflicts on generated blocks of the bundle, rerun `just requirements-update`.

## Ownership against the sibling CRs

The six req-garden CRs run in the same stack and touch shared files (`tiers/log.md`, indexes, a few
SwRS of shared rules). To avoid two CRs editing the same text:

- This CR owns the 13 in-force StRS of rendering-core, diagrams and trust-security (CORE-001, 002,
  003; DIAG-001, 006, 007, 009; TRUST-001, 004, 006, 009, 012, 014), the four new StRS below, and
  the body of every SwRS whose scope is one of these three, plus GFM-027 and GFM-029 (named only in
  this audit).
- For an SwRS of another scope (LIFE-026, LIFE-062, LIFE-094, REVIEW-017, REVIEW-038, BLOCK-238,
  FMEDIT-054), this CR changes only the `derives_from` / `depends_on` entries that point at a StRS
  or SwRS of its scopes, as the mapping says. Its body and markers belong to its scope's CR.
- A sibling CR may drop one of its own StRS from the `derives_from` of a TRUST SwRS (TRUST-001,
  005, 065...). This CR accepts that edit on rebase and keeps its own.

## What changes

All requirement creation, supersession and archiving goes through okfreq
(`uv run --no-sync --group requirements okfreq ... --path requirements`). New requirements are
created `--lifecycle proposed` (they describe code that ships today). Generated fields
(`derived_by`, `supersedes`, `implemented_in_files`, `tested_in_files`, `status`, `verified`, the
Links block, indexes) are never hand-edited: run `just requirements-update` after each step.

### 1. New StRS (missing use cases)

Create each with `okfreq new strs "<title>" --description "<SHALL>" --user-need "<need>" --project
markdown-okf-schema-studio --scope <scope> --lifecycle proposed --path requirements`, fill
Normative behavior, User need, Rationale and constraints, then Main paths (when the SwRS form a
path) and the use-case diagram. Then move the SwRS listed: replace their old parent in
`derives_from` with the new StRS.

| New StRS | Scope | User need (sketch, from the audits) | SwRS moved in | Old parent dropped | Validation test |
|---|---|---|---|---|---|
| A writer reads charts and drawings in the page | diagrams | I put a Vega-Lite or Vega chart fence (inline data or a CSV file next to the document) or an inline SVG in my document and see it themed in the page, with nothing executed or fetched, and a click on a picture leads to its source | DIAG-121, 122, 123, 124, 125, 126, 127 | StRS-DIAG-001 | `test/visual/releaseShowcaseScenarios.ts` (chart drawn, `releaseShowcaseScenarios.ts:26`) and the SVG visual scenario v22 (`test/visual/scenarioDefinitions*.ts`) |
| An agent writes Markdown for Studio with the shipped writing skill | rendering-core | As a writer working with a coding agent, I install the Studio plugin in my agent host and the agent writes cards, tabs, admonitions, charts and diagrams that Studio renders without error | CORE-073, CORE-074 | StRS-CORE-001 | `test/core/render/writingSkill.test.ts` (examples render) and `test/build/test_plugin_manifests.py` |
| A maintainer ships a version only after green checks and reviewed release notes | rendering-core | As a maintainer, a version is tagged only after the heavy CI run is green, its manifests carry the package version and its release notes are reviewed | CORE-075, CORE-076, CORE-078 | StRS-CORE-001 | `test/build/test_release.py` |
| A reviewer reads the published site and its requirements | rendering-core | As a reviewer, I browse use cases, behaviours, coverage and the e2e gallery on GitHub Pages without building anything | CORE-069, CORE-080, 081, 082, 083, 084, 085, 086 | StRS-TRUST-014 | `test/site/requirementsViewer/write.test.ts` (site written from a fixture bundle) |

DIAG-127 (click on a picture leads to its source) is page-side: its `@implements_req` moves from
`renderSvgNodes` (`src/core/render/svgPictures.ts:156`) to the page handler that reacts to the
click, and a unit or page test of that handler gets `@tests_req` (today only visual v22 tests it).

### 2. StRS text fixes

| StRS | Fix | Approved? |
|---|---|---|
| CORE-001 | Remove the Main path 1 option "CORE-001 (refusal): the render is refused when trust is required" (a pipeline guard, contradicts TRUST-001). Remove any mention of the writing skill, plugin, release, CI tagging and release notes (moved out). Keep a faithful-rendering use case. | Yes: owner re-approval |
| CORE-002 | The normative text promises "let the writer edit it from the include location", which no SwRS specifies (BLOCK-127 forbids moving an included block). Reword the StRS to what the code does today (included content is rendered and mapped to the include directive lines; a refused include stays a placeholder). Do not add an SwRS for a behaviour the code may not have: if the Driver finds that editing from the include location does exist in the code, it brings the choice (new SwRS or reword) back to the owner. | No |
| DIAG-001 | Remove charts and SVG from the text (moved to the new StRS). Trim the rationale to the need, the constraints and the Main paths: SwRS-level details (the 64 drawings, exact message strings, known issues) move to the SwRS that owns each, if not already there. Nothing normative is lost. | Yes: owner re-approval |
| DIAG-006 | Trim the rationale the same way (SwRS-level limits and messages to their SwRS). | Yes: owner re-approval |
| DIAG-007 | Replace "one process is started per diagram in parallel" with what the code does: one process per diagram, at most 2 at once (`PLANTUML_MAX_CONCURRENT_RENDERS = 2`, `acquireRenderSlot` in `src/core/render/plantUmlRenderer.ts`). Trim the rationale (1748 words today). | No |
| DIAG-009 | Trim. Fix the half-stale known-issue sentence: the "budget exhausted" message is tested (`test/core/render/diagReq.pipeline.requirements.test.ts:67`); only "too large" was untested, and this CR adds its test (section 6). | No |
| TRUST-009 | Fix the stale pointer "the rendering-core record for ignored messages": the rule is TRUST-052. Main path cites TRUST-061: replace with TRUST-059 after the merge (section 3). | No |
| TRUST-012, TRUST-014, CORE-002 | Thin: fill the rationale enough to read on its own; TRUST-014 keeps TRUST-074 (bundle part) and TRUST-075 only. | No |

An approved StRS changes only with the owner's recorded agreement (`project.guidelines.md`,
"Approved requirements"). The Driver puts the text changes of CORE-001, DIAG-001 and DIAG-006 in
their own commit, at the top of the branch, so that they can be dropped alone. With the owner's
agreement (open question 1), it sets `approved_by: gaetan@xeberon.net` and `approved_at` to the
date and time with its UTC offset, lists the three under "Approved requirements changed" in the
PR body and requests the owner's review. Without it, that commit is dropped and those three files
keep their text (their generated fields still refresh). Moving SwRS out of an approved StRS
(`derives_from` on the SwRS) does not change the StRS text and needs no re-approval, unless its
Main paths cite the moved SwRS (they do not today: CORE-001 cites CORE-001, 034, 041, LIFE-094;
DIAG-001 cites DIAG-001, 005, 009, 015, 017; DIAG-006 cites DIAG-023, 032, 039).

### 3. SwRS merges, splits and rewrites

Rule for a split: the original ID keeps the behaviour its title names (identity preserved), the
other behaviour gets a new SwRS from `okfreq new swrs ... --derives-from <StRS> --lifecycle
proposed`, and its scenarios, markers and tests move with it. Rule for a merge: the absorbed SwRS
is superseded into the one that holds the rule; its scenarios become rows of the survivor, its
markers are renamed to the survivor, and any Main path citing it is rewritten to cite the
survivor.

| Today | Change | Result |
|---|---|---|
| CORE-001 (4 behaviours) | Split. (a) the unsaved buffer is rendered in process, the newest edit wins (nominal, cancel, late result) stays CORE-001. (b) CommonMark constructs render the same in every palette mode, complete for 6000 lines: new SwRS under StRS-CORE-001. (c) engine warm-up: to the verification notes. (d) trust refusal: removed (production always passes `allowUntrusted: true`), noted in the verification notes as a pipeline guard. | CORE-001 + 1 new |
| CORE-028 (style catalogue) | Split inline code (pill, in links, in tables, in forced themes) from body typography (body text, headings, lists, block quote tint, link colour in forced themes, end padding). | CORE-028 (typography) + 1 new (inline code) |
| CORE-070 (internals) | Rewrite as an observable outcome: the parse time does not grow with the number of directives times the document size, and the blank lines around each directive stay unchanged. Keep its tests (`test/build/mystSourcePatches.test.ts`). Fix the prose warning if any. | CORE-070 |
| GFM-029 vs CORE-071 (two raw HTML subsets) | Merge: read the real allow-list in `src/core/render/mystRawHtml.ts` and `src/core/render/mystBlockTransforms.ts`, write it once in CORE-071 (details/summary/kbd become rows), supersede GFM-029 into CORE-071; markers at `mystBlockTransforms.ts:116` and `mystRenderer.ts:544` become CORE-071 (or move to the exact branch). | CORE-071 |
| DIAG-001 SwRS (9 scenarios) | Split "figure and picture" (figure HTML, label fit, width, hidden while edited) from "renderer loading" (script and chunk loading). The loading part becomes the shared rule below. | DIAG-001 + shared |
| "renderer script loads only when the page holds one" (DIAG-001 scenario, DIAG-023 scenario, DIAG-124) | One shared SwRS, engine-agnostic (Mermaid, PlantUML, Vega). If DIAG-124 holds only this rule, it is that SwRS (retitled) and the others cite it by `depends_on`; otherwise create it new. | 1 SwRS, cited by `depends_on` |
| "drawn once per source and theme, late results dropped" (DIAG-009, DIAG-039, DIAG-123, cache part of DIAG-097) | One shared SwRS, cited by `depends_on`. The SwRS that keeps the ID is the one whose StRS Main path cites it (DIAG-009 under DIAG-001); an engine-specific SwRS that holds nothing else is superseded into it, and the Main paths of DIAG-006 (citing DIAG-039) are rewritten to cite the survivor, which then also derives from DIAG-006 (a Main path may cite only a derived SwRS). | 1 SwRS |
| DIAG-084 (one 150-word sentence; "one process per diagram") | Rewrite: one process per diagram, at most 2 at once, results in document order; the concurrency part of DIAG-097 moves here. The JAR include-containment refusal leaves the sentence and cites the shared roots rule by `depends_on`. | DIAG-084 |
| DIAG-097 (bounds + cache + concurrency) | Keep bounds, kill and settle-once. Cache goes to the "drawn once" SwRS, concurrency to DIAG-084. | DIAG-097 |
| Allowed-roots rule, written 6 times (CORE-013, DIAG-054, DIAG-084, DIAG-122, TRUST-002, TRUST-025) | Keep the rule once in TRUST-025 (the resource policy, `src/core/security/resource-policy.ts`) or in the roots part of CORE-013, whichever the code names as the single check; the others cite it by `depends_on` and keep only what is their own (the trigger and the message). DIAG-061 likewise cites CORE-013's depth rule (8 levels) instead of repeating it. | no new ID |
| TRUST-002 (title "reads no include" contradicts its text and test) | Retitle to what the text and `test/security/trustReq.requirements.test.ts:195` say (a read-only preview reads includes from the folder of its document). Split the image exception (images from the workspace folder unless broad) into a new SwRS under StRS-TRUST-004. | TRUST-002 + 1 new |
| TRUST-005, TRUST-006 | Merge TRUST-006 into TRUST-005: "every page message is handled whatever the trust; only reads are narrowed". TRUST-001 stays (affordances kept, trust-needing features off with a reason). | TRUST-005 |
| TRUST-061, 062, 063, 064 (rows of one behaviour, one test) | Merge into TRUST-059 as a table of host-message checks; supersede each; TRUST-009 Main path cites TRUST-059. | TRUST-059 |
| TRUST-074 (icon + shipped bundle) | Split: the icon stays under StRS-TRUST-012, the shipped bundle under StRS-TRUST-014. The ID keeps the behaviour its title names. | TRUST-074 + 1 new |

### 4. Reparenting (`derives_from` and `depends_on`)

| SwRS | Drop from `derives_from` | Then |
|---|---|---|
| TRUST-052 | StRS-CORE-001 | stays under TRUST-009 |
| REVIEW-017, REVIEW-038 | StRS-DIAG-001, StRS-DIAG-006 | `relates_to` the diagram SwRS only if the exclusion of diagrams from review marks is a scenario of theirs |
| DIAG-001 (SwRS) | StRS-DIAG-006 | |
| TRUST-074, TRUST-075 | StRS-DIAG-006 | stay under TRUST-014 (and TRUST-012 for the icon part) |
| TRUST-065, TRUST-090 | StRS-DIAG-009 | DIAG-046 and the other DIAG SwRS that use them cite them by `depends_on` (DIAG-046 already does) |
| LIFE-026 | StRS-TRUST-001 | |
| CORE-041 | StRS-TRUST-006 | stays under CORE-001 |
| BLOCK-238, FMEDIT-054, GFM-027, TRUST-086 (and DIAG-050) | StRS-TRUST-009 | each cites TRUST-052 by `depends_on` and keeps its feature parent |
| LIFE-062 | StRS-TRUST-004 (weak link) | only if it keeps another parent; otherwise leave it and say so in the log |
| CORE-069, CORE-073..076, CORE-078, CORE-080..086, DIAG-121..127 | as in section 1 | |

Every SwRS keeps at least one in-force parent; `just requirements-lint` (validate and
`scripts/check_main_paths.py`) proves it.

### 5. Markers on the code and on the tests

Implementation markers move next to the code they name, at most 3 IDs per marker comment
(rule of `req-marker-gate`):

- `src/core/preview/styles/contentBlockStyles.ts:6-19` (14 IDs), `contentLayoutStyles.ts:80-85`,
  `tableStyles.ts:1-3`, `commentStyles.ts:3` (CORE-008 does not belong to comment styles),
  `propertiesStyles.ts:1` (CORE-050), `editModeStyles.ts:9` (8 IDs, DIAG-001): each ID of these
  scopes moves to the CSS constant or rule block it concerns; IDs of other scopes in the same block
  are left for their CR (or moved along when the right place is obvious and the sibling CR has not
  touched the block).
- `src/core/security/html-sanitizer.ts:268-275`, `rewriteNode` with 8 IDs (CORE-008, CORE-041,
  GFM-016, GFM-034, TRUST-011, 025, 036, 042): each on its branch or helper (dir attribute, script
  removal, link rewrite, resource resolution, missing image). GFM-016 and GFM-034 move only if
  their branch is obvious; else they stay for the gfm CR.
- `src/core/render/mermaidFont.ts:1` file header (DIAG-001): onto the function it concerns.
- DIAG-024 at `import "@plantuml/core/themes.js"` (`src/page/modules/plantumlPreview.ts:15`) is the
  offline themes of DIAG-023: retarget the marker to DIAG-023 and put DIAG-024 on the engine choice.
- DIAG-032 at `askHost` (`plantumlPreview.ts:28`) is the include request of DIAG-046: retarget to
  DIAG-046. DIAG-032 stays at `findUnsupportedPlantUmlFeature` (`plantumlDiagram.ts:71`).
- DIAG-097 on `cacheKey` (`plantUmlRenderer.ts:89`): rename to the "drawn once" SwRS; add DIAG-084
  on `acquireRenderSlot`; keep DIAG-097 on `renderSource`.
- CORE-043: add `@implements_req` at the `enableFindWidget` options of the custom editor
  (`src/host-vscode/activation.ts:100`) and of the panel (`:239`), not only on `openPreview`.
- Companion files: add `scripts` to `source_dirs` of the rendering-core scope in
  `requirements/config.yml` and, if okfreq accepts a source dir inside a test dir (check with
  `okfreq trace requirements --json`), `test/site`. Then put the markers on the code:
  CORE-070 in `scripts/myst-patches.mjs`, CORE-069/080..086 in `test/site/` and
  `test/site/requirementsViewer/`, and remove `src/core/render/mystTightness.markers.ts`,
  `requirementsViewer.markers.ts` and `siteTheme.markers.ts`. Where okfreq refuses it, the
  companion stays and follows the companion rule of `req-marker-gate` (each ID names its
  scenario). `src/page/modules/plantumlBundle.markers.ts` (TRUST-074, built by the root
  `esbuild.mjs`, not in a source dir) stays and follows that rule. CORE-075/076/078 keep
  `annotation_exemption` unless their markers in `scripts/` now count; then the exemption is
  removed.
- Test markers in file headers move onto the tests: DIAG-017 in the header of
  `test/page/modules/editActions.test.ts:9`; the DIAG-001 entries in
  `test/integration/realInput/markers.ts` move onto the real-input scenario that checks them
  (when `req-marker-gate` has not already done it).

Unmarked tests named by verification notes get `@tests_req` on the test itself (re-check each
asserts the scenario before marking):

- CORE-001: `test/core/render/renderPipeline.test.ts:55, :81`,
  `renderReq.renderingCore.requirements.test.ts:63, :73`
- CORE-003: `mystFeatures.test.ts:924, :1144, :1270`
- CORE-012: `test/core/render/includeBudget.test.ts:106`,
  `renderReq.renderingCore.requirements.test.ts:145`; CORE-013: `includeBudget.test.ts:94`
- CORE-022: `mystFeatures.test.ts:171` (code-cell output), `:885` (`#tbl:`)
- CORE-028 (or its new inline-code SwRS): `previewStyles.test.ts:58, :764`, `inlineCode.test.ts:35, :65`
- CORE-050: `test/page/modules/motion.test.ts:152, :170`, `previewStyles.test.ts:1248`
- LIFE-094: `test/core/preview/updatedRanges.test.ts:44, :57, :64, :73`, `motion.test.ts:116`
  (marker only; LIFE-094's text is the lifecycle CR's)
- CORE-069: `test/site/requirementsViewer/home.test.ts:18, :46`, `write.test.ts:25`; CORE-081:
  `pages.test.ts:56, :74`; CORE-084: `search.test.ts:8`; CORE-085: `cards.test.ts:18, :38`
- DIAG-009: the verification notes are stale (draw passes, late picture, late error are tested at
  `test/page/modules/mermaidPreviewEntry.test.ts:100, :128, :149`): fix the notes.

### 6. Tests for the scenarios no test checks

Each new test checks a scenario the SwRS already states, with `@tests_req` on it. If a new test
shows the code does not do what the SwRS says, the SwRS is corrected to what the code does with a
line "Known issue: ..." and the fix goes to the backlog (constitution, section 1); the code is not
changed in this CR. When an existing assertion changes, the commit says why (constitution,
section 3).

- DIAG-084 (H): rewrite `test/core/render/diagReq.jar.requirements.test.ts:104` "starts one process
  per diagram before any of them finishes", which passes only through the 30 s timeout (30016 ms
  measured). New test: with 3 diagrams and a scripted spawner, at most 2 processes run at once, the
  third starts when one finishes, results come in document order; it must finish well under the
  timeout (no wait on the 30 s bound).
- CORE-003: the CRLF and CR rows. CORE-010: link, image, math and raw HTML refusals (today named
  by a test title only). CORE-013: the 10 Mi characters budget row. CORE-025: the first render
  fails (error page). CORE-041: the right alignment itself (an RTL paragraph is aligned to the
  right). CORE-043: the custom editor opens with the find widget enabled. CORE-050: the 3 px
  offset.
- DIAG-005: the boundary "the colours stay the same, nothing is redrawn" and the border and
  secondary colours. DIAG-024: the built-in engine needs nothing outside the extension (for
  example a contract test that the engine is in the page bundle and the page loads no outside
  resource for it). DIAG-050: the 100-character edit id and a 4097-character `from`. DIAG-053:
  the step that remembers the canonical path. DIAG-068: the too-large row. DIAG-089: the signal
  wording (the Windows process group stays a known gap in the verification notes).
- TRUST-007: Restricted Mode, subfolder and multi-root rows and the bundle-folder entry. TRUST-025:
  `srcset` and the blocked-srcset diagnostic. TRUST-036: `embed`, `object`, `form`; tighten
  `test/security/html-policy.test.ts:68`, which accepts the code `blocked-svg-content` that does not
  exist, to pin `blocked-active-element` (the assertion's intent is unchanged: it pins the real
  code). TRUST-042: the wiki case, a bad anchor, `xlink:href`, `blocked-navigation`, the stylesheet
  removal. TRUST-012: the policy of the document body. TRUST-022: the Mermaid and PlantUML scripts
  and the maths style carry the nonce. TRUST-090: the default timeouts (6 s, 10 min), a late answer
  after a timeout, no callback after cancel, the 15 s comment timeout (with fake timers).

### 7. A validation test per StRS

`strs_test_coverage_mode` is `linked-swrs-and-validation-test`: each StRS needs a direct
`@tests_req StRS-...` on a real scenario (an integration or visual scenario that walks the use
case), never on a companion list.

| StRS | Today | Change |
|---|---|---|
| CORE-001 | visual `scenarioDefinitions1.ts:59`, v25, v26 | keep |
| CORE-002 | none | `test/integration/projectFeatures.test.ts` `run()`: the expanded include (`:134`) and the unresolved one (`:142-154`) |
| CORE-003 | visual `unresolved-dark-full` | keep |
| DIAG-001 | visual `scenarioDefinitions1.ts:367`, `scenarioDefinitions2.ts:844` (+ companion) | keep the visual ones; the companion entry does not count |
| DIAG-006 | visual v10/v11 | keep |
| DIAG-007 | visual `plantuml-success-light` | keep |
| DIAG-009 | visual v15/v16 | keep |
| TRUST-001 | `untrusted-suite.ts`, `standalone-suite.ts:39` | keep |
| TRUST-004 | partial: `standalone-suite.ts:40` (standalone file only) | add a Restricted Mode scenario to `test/integration/untrusted-suite.ts`: an image inside the document folder loads, one outside does not |
| TRUST-006 | none | `test/integration/trusted-suite.ts` `run()`: open a hostile fixture (inline script, `on*` attribute, `iframe`/`object`) and assert the page is inert and carries the deny-by-default policy and nonce (the policy is asserted at `:93`) |
| TRUST-009 | none | `test/integration/blockMove.test.ts` `run()` and `commentWrite.test.ts` `run()` (a stale render answered as out of date) |
| TRUST-012 | none | `test/security/package-contract.test.ts:20` (icon) and `test/security/userFacingText.test.ts:131` |
| TRUST-014 | none | `test/security/package-contract.test.ts:368` (VSIX contents) |
| 4 new StRS | | as in section 1 |

### 8. Use-case diagrams

Each of the 17 in-force StRS of this CR (13 + 4 new) gets a `### Use case diagram` section by the
rule of `req-use-case-diagrams`, at use-case level (no SwRS IDs), consistent with its Main paths.
Kinds and steps from the audit: CORE-001 sequence (writer, VS Code editor, extension host,
preview page; render the unsaved buffer, cancel the older render, sanitize and patch, show the
blocks, another tool edits, changed blocks glow); CORE-002 sequence; CORE-003 state (good page,
rendering, stale page with diagnostics, error page on a first failure); DIAG-001, 006, 007, 009
sequence; TRUST-001 actors (trusted writer; Restricted Mode or standalone-file writer); TRUST-004,
006, 009 sequence; TRUST-012 and TRUST-014 actors. The new StRS: charts and drawings sequence,
writing skill actors (writer, coding agent, agent host), release sequence (maintainer, CI, tag),
published site actors (reviewer, site). The audit sections give the steps of each. For the three
approved StRS, the diagram is part of the re-approval commit (section 2).

### 9. Wording and records

- Fix the W002 prose warnings ("no filled EARS expression") on CORE-071, 076, 078, 080, 085.
- One dated entry in `requirements/tiers/log.md` under `## <date>` / `### Gardening of
  rendering-core, diagrams and trust-security`: new StRS, the old-to-new mapping of every
  supersession and split, the reparentings, the approval state of CORE-001/DIAG-001/DIAG-006, and
  the verification results.
- No change to `skills/writing-for-markdown-okf-schema-studio/` (no rendered syntax changes).

## Out of scope

- Any product behaviour change, including fixes of defects that new tests reveal (they become
  "Known issue" lines and backlog items).
- DIAG-128's marker and the stale LAYOUT-021 marker (`req-marker-gate`), the diagram rule and its
  site rendering (`req-use-case-diagrams`).
- Making the diagram section mandatory with a check (after the six req-garden CRs).
- Deleting retired requirements (refused by the owner).
- Moving TRUST-012 to another scope, retitling DIAG-001 to include SVG pictures, and the other
  retitle candidates of `audit-crosscutting.md` A1/A3 that the group audit does not propose.
- The body and markers of SwRS of other scopes (only their links to these scopes change).

## Evidence

Checks, in the worktree after `just dev`:

1. `just requirements-update`, then `just requirements-lint`: 0 errors;
   `scripts/check_main_paths.py` reports all citations valid; `okfreq validate requirements
   --prose`: no new warning, and the five W002 of section 9 gone.
2. `uv run --no-sync --group requirements okfreq trace requirements --json`: no missing IDs, no
   marker on a superseded or StRS ID other than validation tests; every in-force non-exempt SwRS of
   the three scopes has an implementation and a test file.
3. `just check-markers`: green, and the baseline of `req-marker-gate` holds no entry of these
   scopes that this CR fixed (diff of the baseline file in the PR).
4. `okfreq status` and `just requirements-report`: the 17 StRS of this CR are covered by a
   validation test (`linked-swrs-and-validation-test`).
5. The new DIAG-084 test runs in well under 1 s (report its time); the full unit suite time does
   not grow by the 30 s it used to wait.
6. `just check`, then `just preflight` (on Windows the static stage; CI runs the others).
7. The new and newly marked integration assertions (`projectFeatures`, `untrusted-suite`,
   `trusted-suite`, `blockMove`, `commentWrite`) only run in the real VS Code jobs: run
   `gh workflow run ci.yml --ref <branch> -f heavy=true` and link the green run in the PR.
8. Review scenario for a person: open `out/reports/requirements/` (or the site built by the
   preflight) and read the four new StRS and CORE-001, DIAG-007, TRUST-009: each reads on its own,
   shows its diagram, and lists only the behaviours of its use case.

The PR body's Tests section lists the requirement IDs added, changed, superseded and reparented
with their source and test files, and "Approved requirements changed" lists CORE-001, DIAG-001 and
DIAG-006 when the owner agreed.

## Open questions

1. Re-approval (owner): do you agree to change the text of the approved StRS CORE-001 (remove the
   trust-refusal option from Main path 1, remove the skill, plugin and release mentions, add the
   use-case diagram), DIAG-001 (charts and SVG pictures moved to a new StRS "A writer reads charts
   and drawings in the page", rationale trimmed to the need and constraints, diagram added) and
   DIAG-006 (rationale trimmed, diagram added)? With yes, the Driver records your re-approval
   (`approved_by`, `approved_at`) and requests your review on the PR; with no, those three files
   keep their text and only their SwRS move.
