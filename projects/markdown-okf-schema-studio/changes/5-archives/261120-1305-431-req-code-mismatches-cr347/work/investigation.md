# Investigation CR-431: five CR-347 mismatches

Worktree: `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-06-CR-431` (paths below are relative to it).
Read only; nothing was run except `rules`, searches, `git log -S` and `gh`. No test was run.
PR 418's body only says "Their fixes go to the backlog" (no extra detail); the facts below come from the code.

## Summary of verdicts

| SwRS | Verdict | Fix | Owner question |
| --- | --- | --- | --- |
| CORE-010 | SwRS wrong | reword the SwRS, keep test | no |
| CORE-025 | Code wrong | fix pipeline and two callers, flip test, add stale test | no |
| DIAG-005 | SwRS wrong (claim too wide) | reword scenario and criteria; optional border probe | no |
| DIAG-009 | SwRS wrong (guards are dead) | reword Mermaid rows; keep guards with a comment | no |
| TRUST-042 | SwRS wrong, weakly settled | say SVG links are routed by the host like HTML ones | optional: a small behaviour choice, see below |

No verdict touches StRS-CORE-001 or StRS-DIAG-001 (their text names none of the five points).

## 1. CORE-010 wikilinks between inline HTML tags

Facts confirmed. `expandWikiLinks` (`src/core/render/mystInlineTransforms.ts:114-115`) returns early for
node types `link, image, code, inlineCode, math, inlineMath, html`. In mdast an `html` node is an HTML
block or one inline tag; `<span>[[Note]]</span>` is `html` + `text` + `html`, so the text node is converted.
`autolinkBareUrls` (same file, `AUTOLINK_SKIP_PARENTS`) has the same rule. The function's comment says
"(not in code, math, links or HTML)", i.e. the author meant the node type. Test (pinned issue):
`test/core/render/renderReq.coreRows.requirements.test.ts:40-63`, the `InRawInline` case at lines 60-62.

Evidence. Converting matches CommonMark (Markdown between inline tags is still Markdown), the
autolink transform and the in-code comment. `git log -S` shows the `html` skip came with the split
commit `85133469`; no doc, issue or commit says inline HTML content is meant to stay literal. The writing
skill (`skills/writing-for-markdown-okf-schema-studio/`) says nothing on wikilinks except `[[toc]]` (not
rendered), so no skill edit. A code fix would need a new "inside an inline HTML element" notion in an
mdast walk (open/close tag pairing) which is large and diverges from CommonMark.

Recommended verdict: SwRS is wrong; behaviour is intended. Reword "raw HTML" to "a raw HTML block or an
HTML tag itself (text between two inline tags is plain text and is converted)".

Files to edit:
- `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-010.md`: description and Normative
  sentence (frontmatter `description` is prose, hand-editable; keep both identical), refusal table row
  ("raw HTML" -> "an HTML block or tag"), add a boundary row or scenario for `<span>[[Note]]</span>`
  converted, remove the Known issue line, adjust the second Verification note and Criteria.
- `test/core/render/renderReq.coreRows.requirements.test.ts`: keep the assertion, replace the "Known
  issue" comment (lines 60-61) with a plain comment; optionally rename/split the test so the inline
  case is its own test with `@tests_req SwRS-MDOKFSTUDIO-CORE-010`.
- Consistency (not required): `SwRS-MDOKFSTUDIO-GFM-003.md` and its criteria say "raw HTML" for
  autolinks with the same node-type behaviour and no known issue; mention in the log entry or reword the
  same way if the Coder judges it in scope. I would leave GFM-003 alone (out of scope) and note it in the PR.
- `requirements/tiers/log.md`.
Markers: unchanged (`@implements_req CORE-010` stays on `expandWikiLinks`).

## 2. CORE-025 fallback message of a failed render

Facts confirmed. `src/core/render/renderPipeline.ts:325-329` throws
`new RenderError(error instanceof Error ? error.message : String(error), ...)`; `String(undefined)` is
"undefined". `src/session/features/rendering.ts:414` and `:422` (`showRenderFailure`) and
`src/session/previewManager.ts:424` use `error instanceof Error ? error.message : <fallback>`, and the
error is always a `RenderError`, so the three fallbacks are dead. An `Error` with an empty message
shows an empty message. `previewManager.ts:432` (`String(error)` for a rejected `requestDocument`
itself) is another path, not a render failure; leave it.

Evidence. The fallback strings exist in code and in SwRS scenarios; intent is plain. The guard
`instanceof Error` was clearly written for non-Error throws, which the pipeline wrap now hides.

Recommended verdict: code is wrong; fix the code.

Smallest change (three one-line edits):
1. `renderPipeline.ts` catch: message = `error instanceof Error ? error.message : error === undefined || error === null ? "" : String(error)`
   (a thrown string or object keeps its text; a value with no message becomes an empty message). Keep
   `RenderError` an `Error`.
2. `rendering.ts` lines 414 and 422, and `previewManager.ts:424`: use the fallback when the message is
   empty: `error instanceof Error && error.message ? error.message : "<fallback>"`.
   (A small helper `failureMessage(error, fallback)` in `rendering.ts` used by both files avoids three copies; check module-layer rules / `just check` markers.)

Files to edit:
- `src/core/render/renderPipeline.ts`, `src/session/features/rendering.ts`, `src/session/previewManager.ts`.
- `test/host/coreReq.requirements.test.ts`: change the test at lines 47-56 (rename to "...shows the fallback
  'The render failed.'"), assert `data-sphinx-preview-status-message>The render failed.<` and drop the
  "Known issue" comment and the `undefined` assertions. Add a second case for an `Error("")`.
- New test for the stale path "The latest render failed.": no test covers it today (grep for
  `latest render failed` in `test/` finds nothing). Use the host harness: `setRenderOverrideForTests`
  to resolve once (first render good), then reject `undefined`, trigger a second render (edit or refresh
  command as `test/host/lifeReq.requirements.test.ts:205` does for "render of B failed"), and assert the
  stale label and message. Put it in `test/host/coreReq.requirements.test.ts` with `@tests_req CORE-025`.
- `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-025.md`: remove the Known issue, update
  the Verification note for the first-render test and add the stale test; the normative text and
  scenarios already say the right thing. `previewManager.ts` is not in `implemented_in_files`: add it
  by hand only if `just requirements-update` does not (frontmatter lists are generated from markers, so
  put an `@implements_req SwRS-MDOKFSTUDIO-CORE-025` marker on the edited code in `previewManager.ts`).
- `requirements/tiers/log.md`.
Risk: other callers that print `RenderError.message` (grep `\.message` after `RenderError`, e.g.
`test/core/render/renderPipeline.test.ts:70`, `buildQueue`) may now see "" for a no-message throw;
only a value without a message is affected.

## 3. DIAG-005 border, secondary and tertiary in the picture

Facts confirmed. `themeVariables` at `src/page/modules/mermaidPreview.ts:72-82` give
`primaryBorderColor`, `secondaryColor`, `tertiaryColor`; Mermaid runs with `theme: "base"`.
`check_mermaid_theme_switch` (`test/visual/capture_final_checks.py:659-714`) injects a probe `g.node`
(rect, polygon, circle, path) into the drawn SVG and reads only its computed `fill`.

Does the fixture draw parts with those colours? `test/visual/fixtures/06-mermaid-map.md` is a flowchart
with no `subgraph` (no cluster) and all nodes carry `classDef` with their own fill and stroke, so the
drawn nodes show neither the theme border nor secondary/tertiary. Mermaid's base theme (from
`node_modules/mermaid/dist/chunks/mermaid.core/chunk-DSNLSHJZ.mjs`): `clusterBkg = tertiaryColor` (cluster
only), `edgeLabelBackground` is `darken/lighten(secondaryColor, 30)` (a derived colour, not equal to
secondary). So no part of the fixture shows tertiary at all; secondary appears only through a derived edge
label background, which the visual campaign checks only as contrast (>= 4.5:1).

Border: the same probe technique can read it for free: the diagram's own style sheet gives
`.node rect/polygon/circle/path { stroke: <nodeBorder = primaryBorderColor> }`, so a probe node's computed
`stroke` can be compared with `--sphinx-preview-border` like the fill is with
`--studio-textCodeBlock-background`. I could not run the visual job (Windows: static stage only; `just
dev` is running, not the visual harness), so this is untested here. Secondary/tertiary could be probed
only with a probe `g.cluster rect` (style sheet rule for `.cluster rect`, fill = tertiary), still
reading the style sheet, not a part the fixture draws.

Recommended verdict: the SwRS claim is too wide. Smallest safe change, no visual job: reword the
nominal scenario so the picture claim covers what is checked in the drawn picture (node fill, and the
background as transparent) and state that border, secondary and tertiary colours are checked as the
values given to Mermaid (unit test), because the base theme uses secondary and tertiary only for clusters
and the derived edge-label background, which the fixture does not draw as such. Remove only the first
Known issue; leave the other three.

Optional extension (Coder's call, more proof, needs the CI visual job): add the border probe
(`getComputedStyle(probe.firstChild).stroke` vs a span `border-color` from `--sphinx-preview-border`) to
`check_mermaid_theme_switch`, and then the SwRS may claim "node fill and border in the picture". Not
required to close the known issue and I would not take it in this CR unless the owner wants the
stronger claim (risk: the colour may be serialised differently, e.g. `rgb()` vs `#`; verify in CI only).

Files to edit (reword path):
- `requirements/tiers/swrs/diagrams/SwRS-MDOKFSTUDIO-DIAG-005.md`: scenario "Colours come from the theme
  variables" (table keeps the Source column; THEN line says the node fill and the transparent
  background are checked in the picture, the other parts as values given to Mermaid), Verification
  notes and Criteria; remove the first Known issue line.
- `requirements/tiers/log.md`. No source or test change; markers unchanged.
If the extension is taken: also `test/visual/capture_final_checks.py`, and the scenario description text
`test/visual/scenarioIds.ts:294` (the v01 description) if its wording changes.

## 4. DIAG-009 Mermaid late-result guards

Facts confirmed. `src/page/modules/mermaidPreview.ts:139` (`if (drawnKeys.get(diagram) === key) showImage`)
and `:141` (`if (drawnKeys.get(diagram) !== key) return;`).

Does any real path change a node's key during a drawing? No. `drawnKeys` is a `WeakMap` written in one
place only (line 120, when the pass plans the node). Every pass is chained on `renderQueue`: the first
pass, the `studio:content-replaced` listener and the theme `MutationObserver` all do
`renderQueue = renderQueue.then(...)`. Inside a pass, `pending` holds each element once and plans it once;
a node that a content patch replaces is a different element (new `WeakMap` key). So between the planning
at line 120 and the `await mermaid.render` result, nothing else writes that node's key. The guards are
dead for both the picture and the error. (Defence only: if a future change ran passes in parallel they
would matter.) The test `a Mermaid drawing finished for an earlier theme never replaces the picture of the
current one` (`test/page/modules/mermaidPreviewEntry.test.ts:~129`) confirms it: the second pass starts only
after `calls[0]` resolves, and the old drawing is shown only from the cache later.

Recommended verdict: the SwRS is wrong for the Mermaid rows; the behaviour is "passes are serialised".
Keep the two guards as defence, add a one-line comment each ("unreachable today: passes are serialised
and a pass plans each node once"), so no test or marker moves. (Removing them is also allowed by the
spec but adds code risk for no gain.)

Files to edit:
- `requirements/tiers/swrs/diagrams/SwRS-MDOKFSTUDIO-DIAG-009.md`: normative sentence ("drop a result that
  arrives for a key the node no longer has" -> "for PlantUML and charts, drop a result ...; Mermaid passes
  run one at a time, so a later theme is drawn only after the running pass ends"); scenario "A late
  picture for a replaced key is not shown": first row becomes "A diagram is being drawn for the dark theme
  and the theme changes to cream: the cream pass starts after the dark pass ends; the dark drawing is
  stored in the cache and shown, then replaced by the cream one" (what the test shows); scenario "A late
  error...": first row says PlantUML (and charts) only; Verification notes lines for the two Mermaid tests;
  Criteria; remove the fifth Known issue (the "cannot be reached" one) only. Leave the other four.
- `src/page/modules/mermaidPreview.ts`: two comments (optional if keeping a bare guard comment already
  at line 137-138: extend it).
- `test/page/modules/mermaidPreviewEntry.test.ts`: rename/comment the earlier-theme test so it asserts
  "later theme drawn after the pass ends", still `@tests_req DIAG-009`.
- `requirements/tiers/log.md`.
Markers: `@implements_req DIAG-009` stays at line 108 and `@tests_req` on the same tests.

## 5. TRUST-042 SVG xlink:href and the navigation attribute

Facts confirmed. `src/core/security/html-sanitizer.ts:457-482`: the branch `name === "href" ||
name === "xlink:href"`; the navigation attribute is set only when `name === "href"` (for `uri` only if also
`tagName === "a"`). parse5 names `xlink:href` as `href` (prefix `xlink`), so the `"xlink:href"` comparisons
are dead and an SVG `<a xlink:href>` is treated exactly like an HTML link (blocked: href removed, request in
`data-sphinx-preview-navigation`, `blocked-navigation` recorded; allowed `#section`: href kept and the
attribute set). Test pinned: `test/security/trustReq.pageBuild.requirements.test.ts:96-111`.

What a click does today. Page code selects `a[data-sphinx-preview-navigation]` (`src/page/modules/linkNavigation.ts:101`,
`activate` at `:165-190`, `closest(selector)`), which matches an SVG `a`; it calls `preventDefault()` and posts
`previewLink` with the request, and the host re-checks it. A blocked `javascript:` SVG link therefore
does nothing in the page and the host refuses the request; an allowed link is followed by the host. So SVG links in raw
HTML behave like HTML ones today.

Is host routing wanted anywhere? Searched `docs/`, `README.md`, the skill and tests: the only mention
is `skills/.../references/svg.md:51`, which says that `<a>` and every link to another page are removed from
fenced `svg` pictures (a different path, `svgSanitizer.ts`, not touched here); SwRS DIAG-001/003
known issue says links in svg pictures are inert. Issue 336 (inline svg) never mentions links. History: the
`xlink:href` branch exists since `e757ef06`, written to validate the address, with no document saying SVG
links should be left out of host routing. Nothing says "wanted" and nothing says "not wanted".

Recommended verdict: SwRS is wrong. Reasons: it is the safe and consistent behaviour (every link the user
can click goes through the same host check, the blocked one has no click action, the request leaks no
address into an `href`), a code fix would make allowed SVG links follow the webview's own navigation or be dead
(the opposite of the policy "a relative link never navigates by itself; the host follows it after checking"),
and it needs prefix/namespace tests in the sanitizer for no known need.
It is a small real behaviour choice (what a click on an SVG link in a raw-HTML SVG does), the evidence leans one way
but does not decide it; the Driver can decide alone per the specification, but flag it in the PR body so the
owner can overturn it. If the owner wants the other way: in the sanitizer, tell the two apart with
`attribute.prefix === "xlink"` (or `attribute.namespace`), do not set the navigation attribute for them, and flip the test;
that also changes click behaviour for allowed SVG links and needs a new test.

Files to edit (SwRS-wrong path):
- `requirements/tiers/swrs/trust-security/SwRS-MDOKFSTUDIO-TRUST-042.md`: refusal table rows 3 and 4 ->
  "an `xlink:href` the link rules block (SVG link): no href remains; the request is only in
  `data-sphinx-preview-navigation`, as for an HTML link" and "allow: the address is kept and the request is in
  `data-sphinx-preview-navigation`, the host routes the click"; remove the Known issue; adjust the
  Verification note that names the xlink cases.
- `test/security/trustReq.pageBuild.requirements.test.ts`: rename the test ("an SVG xlink:href is treated like an
  HTML link: blocked loses its address, allowed keeps it, both keep the request for the host"), drop the
  "Known issue" comment, keep the assertions.
- Optional: `src/core/security/html-sanitizer.ts:457`: drop the dead `|| name === "xlink:href"` or add a
  comment that parse5 reports the local name `href` for `xlink:href`. Do not change behaviour.
- `requirements/tiers/log.md`.

## Risks and cross-cutting

- Frontmatter lists (`implemented_in_files`, `tested_in_files`) and the `okf:links` block are generated: edit
  only prose, then `just requirements-update` and commit its output.
- "Normative sentence" and frontmatter `description` repeat the same text (CORE-010, DIAG-009): change both.
- Markers: at most 3 IDs per block; none move in the recommended verdicts except a new
  `@implements_req CORE-025` marker in `previewManager.ts` if edited.
- `docs/known-limitations.md`/skill: no edit needed (no mention of any of the five).
- Only CORE-025 changes behaviour (visible: a no-message failure now reads "The render failed." / "The latest render failed." instead of "undefined").

## Evidence plan

Kind: mostly requirements prose, one small code fix (CORE-025).
- Fails on previous code (constitution section 3; run once on the base and keep the failure in round notes):
  - `test/host/coreReq.requirements.test.ts` first-render no-message test (expects "The render failed.", got "undefined").
  - New stale-path test for "The latest render failed." (expects the fallback, got "undefined").
  - New `Error("")` case (empty message shows the fallback).
- Tests that keep passing, only reworded or relabelled: CORE-010 renderReq test, TRUST-042 pageBuild test, DIAG-009
  `mermaidPreviewEntry` tests; DIAG-005 has no code change. No test fails on previous code for these four (the SwRS
  was wrong), and the PR body says why.
- Gates: `just check` (unit, contract, security, markers, file size), `just requirements-lint`,
  `just requirements-update` with nothing left to commit, `uv run --no-sync --group requirements okfreq validate
  --check-links --project-root .` and coverage, then `just preflight`. The visual job (`just ci-visual`) is needed
  only if the optional DIAG-005 border probe is taken; then the PR's CI visual run is the proof.
- Add the dated entry to `requirements/tiers/log.md` (five SwRS, verdicts, sources, tests) and the PR body lines (verdict
  and evidence per item).
- Cannot be shown: the DIAG-005 picture check of border, secondary and tertiary (not drawn by the fixture), and a real
  late Mermaid result (no real path).
