# Audit: rendering-core, diagrams and trust-security (okfreq gardening, phases 4, 6, 6b, read-only)

Repository: markdown-okf-schema-studio, `main` at dedbdb2a. Method: `okfreq trace requirements --json`,
`okfreq validate requirements --prose` (1124 requirements, 0 errors, 36 warnings), a frontmatter
inventory of every requirement, then each `@implements_req` / `@tests_req` site read with the code or
test around it, and each SwRS's "Verification notes" checked against the markers of the tests it names.
Paths are relative to the repository root. Nothing in the repository was changed (one existing compiled
test was run, see DIAG-007).

Scope: 13 in-force StRS (CORE-004/005, DIAG-002..005, 008, 010..014 are superseded and ignored; no
in-force StRS cites an inactive SwRS in its Main paths). 92 in-force SwRS audited: 80 of the three
scopes plus 12 of other scopes derived by these StRS (GFM-027, GFM-029, LIFE-026, LIFE-062, LIFE-094,
REVIEW-017, REVIEW-038, BLOCK-238, FMEDIT-054, and TRUST-059/061..065/086/090 counted in-scope). `okfreq
trace`: no missing IDs, no non-leaf markers, no warnings. Phase 6: the three approved StRS (CORE-001,
DIAG-001, DIAG-006) carry `approved_by` and `approved_at`; every in-force SwRS is `proposed`.

IDs drop the `MDOKFSTUDIO-` part. Severity: **H** wrong or misleading traceability / missing
behaviour, **M** split or marker placement to fix, **L** wording.

## Summary

| StRS | Title (short) | #SwRS | Relevance | Split OK? | Markers OK? | Tests OK? | Validation test? | Diagram |
|---|---|---|---|---|---|---|---|---|
| CORE-001 | Faithful rendering of any document | 22 | Real, but a catch-all: 6 SwRS unrelated (H) | No: CORE-001 mixes 4 behaviours, 070 internal, 028 a catalogue | No: CSS header blocks, sanitizer cluster, companion file | Gaps: 11 unmarked tests, CRLF/CR, first-render failure | Yes (visual handbook, v25, v26) | Sequence |
| CORE-002 | Compose from included files | 2 | Real; thin; "edit from the include" unbacked (H) | Yes; root rule repeated elsewhere | OK | Gaps: 3 unmarked, 10 Mi chars row | No; `projectFeatures.test.ts` can serve | Sequence |
| CORE-003 | See what cannot render, keep a usable preview | 6 | Real; good | Yes | OK | Gap: first render fails (on Main path) | Yes (visual `unresolved-dark-full`) | State |
| DIAG-001 | Read and insert Mermaid diagrams | 14 | Real; too verbose; holds charts and SVG (H) | No: 7 chart/SVG SwRS, 2 REVIEW misparented, repeated rules | No: CSS headers, file headers | Gaps: stale notes, boundary on Main path untested | Yes (visual, real input) | Sequence |
| DIAG-006 | PlantUML without setup | 10 | Real; too verbose | No: DIAG-001, TRUST-074/075, REVIEW-* misparented | No: DIAG-024, DIAG-032 on wrong code | Gap: "needs nothing outside" | Yes (visual v10/v11) | Sequence |
| DIAG-007 | Own JAR, safely bounded | 7 | Real; very verbose (1509 words) | No: 097 two behaviours, 084 one 150-word sentence | DIAG-097 on the cache | No: concurrency test contradicts code (H) | Yes (visual `plantuml-success-light`) | Sequence |
| DIAG-009 | Local includes and PUML files | 9 | Real; verbose | Mostly; 061/054 repeat CORE-013 rules; TRUST-065/090 misparented | OK | Gaps: 050 bounds, 053, 068 too large | Yes (visual v15/v16) | Sequence |
| TRUST-001 | Editable whatever the trust | 4 | Real; good | No: 001/005/006 overlap; LIFE-026 misparented | Spread (15 sites for 001) but placed | OK | Yes (untrusted, standalone suites) | Use case |
| TRUST-004 | Local files only from allowed folders | 4 | Real; good | Mostly; TRUST-002 title contradicts body | OK (sanitizer cluster) | Gaps: Restricted Mode rows of 007, srcset | Partial (`standalone-suite.ts`) | Sequence |
| TRUST-006 | No foreign code, unsafe HTML inert | 8 | Real; good | Mostly; CORE-041 misparented | No: `rewriteNode` carries 8 IDs | Gaps: 036, 042, 012, 022 rows | No; `trusted-suite.ts` can serve | Sequence |
| TRUST-009 | Exchanges checked, never misapplied | 12 | Real but abstract | No: 061-064 one test; feature validators misparented | OK | Gap: 090 timeouts | No; `blockMove.test.ts` can serve | Sequence |
| TRUST-012 | Visible text and icon speak of the product | 2 | Real; thin | 074 mixes icon and bundle | Companion file (074) | OK (070 exempt, valid) | No; `package-contract.test.ts` can serve | Use case |
| TRUST-014 | Pinned dependencies, ships what it loads | 10 | Real; 8 site SwRS unrelated (H) | No: CORE-069, 080-086 misparented | Companion files | Gaps: 7 unmarked tests | No; `package-contract.test.ts:368` can serve | Use case |

## CORE-001 A reader reads a faithful rendering of any document (approved, 812 words)

SwRS: CORE-001, 003, 008, 010, 028, 034, 041, 043, 050, 070..079, GFM-029, LIFE-094, TRUST-052.

1. **H** Misparented SwRS. CORE-073 (writing skill examples render), CORE-074 (skill packaged as agent
   plugin), CORE-075 (manifest versions equal package version), CORE-076 (CI tags only after a green
   heavy run), CORE-078 (release notes) have nothing to do with reading a rendering; TRUST-052 (page
   message envelope) belongs to TRUST-009 only. No StRS states their use case. Proposal: new StRS "An
   agent writes Markdown for Studio with the shipped skill" (073, 074) and "A maintainer ships a
   version" (075, 076, 078); drop CORE-001 from TRUST-052 `derives_from`.
2. **H** Main path 1 option "CORE-001 (refusal): the render is refused when trust is required" cites a
   scenario that the SwRS itself calls a pipeline guard ("production always passes `allowUntrusted:
   true`", CORE-001 Criteria); it contradicts StRS TRUST-001 (Restricted Mode renders and edits). Remove
   the option and the scenario (or move it to a verification note).
3. **M** CORE-001 (SwRS) holds four behaviours: (a) the unsaved buffer is rendered in process and the
   newest edit wins (nominal, cancel, late result); (b) CommonMark constructs, identical in every palette
   mode, complete for 6000 lines; (c) engine warm-up (internal); (d) the trust refusal (dead, see 2).
   Mapping: CORE-001 -> CORE-001 (a) + new "CommonMark constructs render the same in every mode" (b);
   (c) to verification notes; (d) removed.
4. **M** CORE-070 describes internals (line splits per parse, in-memory patching of the MyST packages,
   esbuild plugin). Restate as an observable budget (parse time of a document with many directives) or
   exempt it; its marker lives in the companion `src/core/render/mystTightness.markers.ts` (code in
   `scripts/myst-patches.mjs`).
5. **M** CORE-028 is a style catalogue (body text, headings, lists, inline code pill, block quote tint,
   link colour in forced themes, end padding; 8 scenarios, 3 parent StRS). Split inline code (pill,
   links, tables, forced themes) from body typography.
6. **H** GFM-029 (derived by CORE-001) defines the raw HTML subset as details/summary/kbd with "the rest
   dropped", while CORE-071 renders div/p with align, br, img, a, picture, sub, sup, kbd. Two SwRS state
   the same rule differently. Merge GFM-029 into CORE-071 (one "raw HTML subset" SwRS) or make GFM-029
   cite CORE-071 by `depends_on`.
7. **M** Markers in central files: `src/core/preview/styles/contentBlockStyles.ts:6-19` is a header block
   of 14 IDs (CORE-008, 022, 028, 034, DIAG-001, 023, 032, ...); `contentLayoutStyles.ts:80-85`,
   `tableStyles.ts:1-3`, `commentStyles.ts:3` (CORE-008 in the comment styles), `propertiesStyles.ts:1`
   (CORE-050) likewise. Move each next to the CSS constant or rule block it concerns.
   `src/core/security/html-sanitizer.ts:268-275` puts 8 IDs (CORE-008, CORE-041, GFM-016, GFM-034,
   TRUST-011, 025, 036, 042) on `rewriteNode`; put each on its branch or helper (dir attribute, script
   removal, link rewrite, resource resolution, missing image).
8. **M** Unmarked tests named by the notes: CORE-001 `test/core/render/renderPipeline.test.ts:55, :81`,
   `renderReq.renderingCore.requirements.test.ts:63, :73`; CORE-003 `mystFeatures.test.ts:924, :1144,
   :1270`; CORE-028 `previewStyles.test.ts:58, :764`, `inlineCode.test.ts:35, :65`; CORE-050
   `test/page/modules/motion.test.ts:152, :170`, `previewStyles.test.ts:1248`; LIFE-094
   `test/core/preview/updatedRanges.test.ts:44, :57, :64, :73`, `motion.test.ts:116`.
9. **M** Scenarios not checked (from the notes, confirmed): CORE-003 CRLF and CR rows; CORE-010 link,
   image, math, raw HTML refusals ("named by the test title only"); CORE-041 the right alignment itself;
   CORE-043 custom editor (its `enableFindWidget` at `src/host-vscode/activation.ts:100` has no marker;
   the marker sits on `openPreview`, `activation.ts:186`, the option is at `:239`); CORE-050 3 px offset.
10. **L** `okfreq validate --prose` W002 "no filled EARS expression": CORE-071, 076, 078, 080, 085.

Validation test: yes, `test/visual/scenarioDefinitions1.ts:59` (handbook-dark-top),
`scenarioDefinitions2.ts:539` (v25), `test/visual/releaseShowcaseScenarios.ts:15` (v26).

Diagram (sequence): Writer -> VS Code editor -> Extension host (render pipeline) -> Preview page. 1 the
writer types; 2 the host renders the unsaved buffer, cancelling an older render; 3 the host sanitizes and
patches the page; 4 the page shows the blocks (RTL aligned, long words wrapped); 5 another tool edits
the file; 6 the page makes the changed blocks glow.

## CORE-002 A writer composes a document from included files (273 words)

SwRS: CORE-012, CORE-013.

1. **H** The normative text promises "let the writer edit it from the include location"; no SwRS
   specifies it (CORE-012 only maps included blocks to the directive lines; BLOCK-127 forbids moving an
   included block). Add the SwRS (what a click or an edit on included content does) or reword the StRS.
2. **M** The allowed-roots rule is written six times: CORE-013, DIAG-054, DIAG-084 (JAR includes),
   DIAG-122 ("under the rules of the include directive"), TRUST-002, TRUST-025. Keep one rule (CORE-013's
   roots part or TRUST-025) and cite it by `depends_on`.
3. **M** Unmarked tests: CORE-012 `test/core/render/includeBudget.test.ts:106`,
   `renderReq.renderingCore.requirements.test.ts:145`; CORE-013 `includeBudget.test.ts:94`. Unchecked:
   CORE-013 the 10 Mi characters budget row. Markers are well placed (`mystRenderer.ts:258`
   `expandIncludes`, `resource-policy.ts:247`); `mystContextTags.ts:150` only serves the alert scenario.

Validation test: none. `test/integration/projectFeatures.test.ts` `run()` asserts an expanded include
(`:134`) and an unresolved one (`:142-154`): add `@tests_req StRS-MDOKFSTUDIO-CORE-002` there.

Diagram (sequence): Writer, Extension host, Resource policy, File system, Preview page. 1 include
directive found; 2 path checked against the roots; 3 file read (depth, budget, size); 4 content expanded
and mapped to the directive lines; 5 a refused include stays a placeholder with a warning.

## CORE-003 A reader sees what cannot be rendered and keeps a usable preview (482 words)

SwRS: CORE-001, 008, 012, 013, 022, 025. Split and parents are coherent.

1. **M** CORE-025 "first render fails" (refusal, cited as an option in Main path 1) is untested (notes
   say so). The other scenarios are checked.
2. **M** Unmarked tests of CORE-022: `mystFeatures.test.ts:171` (code-cell output), `:885` (`#tbl:`).
3. **L** Overlap with CORE-002 by CORE-012/013 is intentional (refused includes); fine.

Validation test: yes, `test/visual/scenarioDefinitions1.ts:266` (`unresolved-dark-full`).

Diagram (state): Good page -> Rendering -> Good page (success) | Stale page + diagnostics listed (failure
after a good render) | Error page (first render fails); a placeholder with a warning inside Good page for
build-only constructs; a newer edit moves Rendering back to Rendering.

## DIAG-001 A writer reads and inserts Mermaid diagrams that follow the theme (approved, 1336 words)

SwRS: DIAG-001, 005, 009, 015, 017, 121..127, REVIEW-017, REVIEW-038.

1. **H** Vega-Lite/Vega charts (DIAG-121..124) and inline SVG pictures (DIAG-125..127) derive only from
   this Mermaid StRS; no StRS states "a writer reads charts and drawings in the page". Add that StRS and
   move the seven SwRS to it.
2. **M** REVIEW-017 and REVIEW-038 derive DIAG-001 (and DIAG-006) only because diagrams are excluded from
   review marks; drop those parents (`relates_to` if wanted).
3. **M** Repeated rules across engines: "the renderer script loads only when the page holds one" (DIAG-001
   scenario, DIAG-023 scenario, DIAG-124); "drawn once per source and theme, late results dropped"
   (DIAG-009, DIAG-039, DIAG-123, cache part of DIAG-097). One SwRS each, cited by `depends_on`.
4. **M** DIAG-001 (SwRS) has 9 scenarios mixing figure HTML, label fit, width, hidden while edited, script
   loading and chunk loading: split "figure and picture" from "renderer loading".
5. **M** The StRS rationale is SwRS-level (64 drawings, exact message strings, known issues): trim to the
   need, the constraints and the Main paths.
6. **M** DIAG-009 verification notes are stale: they say draw passes, late picture and late error "have no
   test", yet `test/page/modules/mermaidPreviewEntry.test.ts:100, :128, :149` carry DIAG-009.
7. **M** Main path option DIAG-005 (boundary) "the colours stay the same, nothing is redrawn" is untested
   (notes); border and secondary colours untested. DIAG-001 relies on visual scenarios for several rows.
8. **M** Markers: DIAG-001 in `contentBlockStyles.ts:16`, `editModeStyles.ts:9` (header block of 8 IDs)
   and the file header of `src/core/render/mermaidFont.ts:1`; DIAG-017 test marker in the header of
   `test/page/modules/editActions.test.ts:9` (with 5 PALETTE IDs), not on a test. DIAG-127 is marked on
   `renderSvgNodes` (`src/core/render/svgPictures.ts:156`, render side) while the click is page-side;
   only the visual scenario v22 tests it.

Validation test: yes, `test/visual/scenarioDefinitions1.ts:367`, `scenarioDefinitions2.ts:844`,
`test/integration/realInput/markers.ts:50` (a companion file, not a test: see Counts).

Diagram (sequence): Writer, Edition palette, Extension host, Preview page, Mermaid renderer. 1 pick
Mermaid (GFM mode); 2 starter flowchart inserted; 3 host renders a figure with the source disclosure; 4
page loads the renderer and draws the picture in theme colours; 5 theme change redraws; 6 invalid source
shows one message with the parser reason.

## DIAG-006 A writer reads PlantUML diagrams without any setup (approved, 1219 words)

SwRS: DIAG-001, 023, 024, 032, 039, 053, REVIEW-017, REVIEW-038, TRUST-074, TRUST-075.

1. **M** Misparented: DIAG-001 (Mermaid), REVIEW-017/038 (see DIAG-001), TRUST-074/075 (package and
   pinned dependencies; keep them under TRUST-014).
2. **M** Marker on the wrong code: DIAG-024 (engine choice) sits on `import "@plantuml/core/themes.js"`
   (`src/page/modules/plantumlPreview.ts:15`), which is the offline themes of DIAG-023; DIAG-032 sits on
   `askHost` (`plantumlPreview.ts:28`), the include request of DIAG-046. DIAG-032 is already right at
   `plantumlDiagram.ts:71` (`findUnsupportedPlantUmlFeature`).
3. **M** DIAG-024 scenario "the built-in engine needs nothing outside the extension" untested (notes).
4. **M** StRS too verbose; SwRS-level limits and messages in the rationale.

Validation test: yes, `test/visual/scenarioDefinitions2.ts:857` (v10/v11 built-in).

Diagram (sequence): Writer, Extension host, Preview page, built-in engine (in page). 1 fence rendered as
a figure; 2 page loads the engine script; 3 engine draws the light or dark variant; 4 the picture is kept
by source; 5 a URL, library or 1 MiB source shows one message with the useJar hint.

## DIAG-007 A writer renders PlantUML with an own JAR or command, safely bounded (1509 words)

SwRS: DIAG-024, 032, 054, 084, 089, 097, 105.

1. **H** Contradiction. The StRS ("one process is started per diagram in parallel") and DIAG-084
   ("One process per diagram") against DIAG-097 and the code (`src/core/render/plantUmlRenderer.ts:75`
   `PLANTUML_MAX_CONCURRENT_RENDERS = 2`, `acquireRenderSlot` `:130`). The test
   `test/core/render/diagReq.jar.requirements.test.ts:104` "starts one process per diagram before any of
   them finishes" (3 diagrams) passes only because the 30 s timeout frees the slots: run today it took
   30016 ms. It checks the timeout, not its claim. Rewrite the StRS line, DIAG-084 and the test.
2. **M** DIAG-097 holds two behaviours: bounds, kill and settle-once; and cache plus concurrency. Mapping:
   cache -> the shared "drawn once" SwRS (DIAG-001 finding 3), concurrency -> DIAG-084, bounds stay.
3. **M** DIAG-084 normative is one 150-word sentence that also carries the JAR include-containment
   refusal (the DIAG-054 rule). Split the refusal out or cite the shared roots rule.
4. **M** DIAG-097 marker on `cacheKey` (`plantUmlRenderer.ts:89`), the cache, not a bound; add one on
   `acquireRenderSlot` and keep `renderSource` (`:303`).
5. **L** DIAG-089 signal wording untested; Windows process group untested (known).

Validation test: yes, `test/visual/scenarioDefinitions1.ts:398` (`plantuml-success-light`, needs
`plantuml` on PATH) and the built-in scenario.

Diagram (sequence): Writer, VS Code settings, Extension host, PlantUML process, Preview page. 1 useJar
true; 2 host re-renders; 3 one process per diagram (at most 2 at once) on stdin; 4 SVG or error per
diagram in document order; 5 timeout or cancel kills the process group; 6 page patched in place.

## DIAG-009 PlantUML diagrams use local include files and PUML files (1097 words)

SwRS: DIAG-039, 046, 050, 053, 054, 061, 068, TRUST-065, TRUST-090.

1. **M** TRUST-065 and TRUST-090 are generic protocol rules: cite them by `depends_on` (DIAG-046 already
   does), not as derived SwRS.
2. **M** DIAG-061 repeats CORE-013's depth rule (8 levels) and DIAG-054 the roots rule (CORE-002
   finding 2).
3. **M** Unchecked: DIAG-050 the 100-character edit id and a 4097-character `from`; DIAG-053 the step that
   remembers the canonical path; DIAG-068 the too-large row.
4. **L** The StRS says the "too large" and "budget exhausted" messages are triggered by no test, but
   `test/core/render/diagReq.pipeline.requirements.test.ts:67` tests the budget message: half stale.

Validation test: yes, `test/visual/scenarioDefinitions2.ts:900` (v15/v16 include). The PUML-file path
has only SwRS markers (v13/v14).

Diagram (sequence): Preview page (engine), Page script, Extension host, File system watcher. 1 engine
meets `!include`; 2 page asks the host (`previewPlantUmlInclude`); 3 host checks the request and the roots
and answers or refuses; 4 diagram drawn; 5 the file changes on disk; 6 host tells the page; 7 diagrams
that read files are drawn again.

## TRUST-001 A document opens editable whatever the trust, with narrow reads (491 words)

SwRS: TRUST-001, 005, 006, LIFE-026.

1. **M** TRUST-001, 005, 006 say the same rule three ways (affordances kept, writes handled, other page
   messages handled); TRUST-001 has 15 implementation sites and 5 parent StRS. Mapping: keep TRUST-001
   (affordances, trust-needing features off with a reason); merge TRUST-006 into TRUST-005 ("every page
   message is handled whatever the trust; only reads are narrowed").
2. **M** LIFE-026 (side preview follows the active editor) derives TRUST-001 for one scenario about
   another trust state: drop the parent.
3. **L** TRUST-001's test `test/core/preview/previewStyles.test.ts:485` only counts toolbar buttons.

Markers are well placed (`src/session/previewManager.ts:505, :544`, `src/core/edits/readOnlyReasons.ts:1`
is a one-purpose file). Validation test: yes (`test/integration/untrusted-suite.ts`,
`standalone-suite.ts:39`, `realWindowGaps.ts:669`, `commentWrite.test.ts:222`).

Diagram (use case): actors Writer (trusted), Writer (Restricted Mode or standalone file); use cases
edit blocks/tables/frontmatter, comment, paste images (same for both); read includes and resources (narrowed
for the second actor); use PlantUML JAR or citation list (disabled with a reason for the second).

## TRUST-004 Local files load only from the allowed folders (400 words)

SwRS: TRUST-002, 007, 025, LIFE-062.

1. **M** TRUST-002's title "reads no include" contradicts its normative text ("read includes ... from the
   folder of the document") and its test `test/security/trustReq.requirements.test.ts:195` "a read-only
   preview reads includes from the folder of its document". Its normative text is also very long: split
   the image exception (images from the workspace folder unless broad).
2. **L** LIFE-062 (missing source) is a weak parent link.
3. **M** Unchecked: TRUST-007 Restricted Mode, subfolder and multi-root rows and the bundle-folder entry;
   TRUST-025 srcset and the blocked-srcset diagnostic.

Validation test: partial, `test/integration/standalone-suite.ts:40` (standalone file only; no Restricted
Mode scenario).

Diagram (sequence): Page, Sanitizer, Resource policy, File system, Webview. 1 reference found; 2 decoded
and resolved (real path); 3 inside a root and a regular file -> webview address; 4 otherwise attribute
removed with a code; 5 webview loads only from its local resource roots.

## TRUST-006 The preview runs no foreign code and unsafe HTML is made inert (509 words)

SwRS: CORE-013, CORE-041, TRUST-007, 011, 012, 022, 036, 042.

1. **M** CORE-041 (RTL `dir="auto"`) is presentation, not security: drop this parent (it stays under
   CORE-001).
2. **M** Markers: the `rewriteNode` cluster (CORE-001 finding 7).
3. **M** Unchecked: TRUST-036 embed, object, form; its removal test accepts the code
   `blocked-svg-content`, which does not exist in the code (notes), so the real code
   `blocked-active-element` is not pinned; TRUST-042 wiki case, bad anchor, xlink:href,
   `blocked-navigation`, stylesheet removal; TRUST-012 the policy of the document body; TRUST-022 the
   Mermaid and PlantUML scripts and the maths style.

Validation test: none. `test/integration/trusted-suite.ts` `run()` (asserts the policy, `:93`) can serve;
better a real-window scenario on a hostile fixture.

Diagram (sequence): Document, Renderer, Sanitizer, Page builder, Webview. 1 raw HTML with scripts; 2
sanitizer removes scripts, active elements, on* attributes; 3 links rewritten, removals recorded; 4 page
builder adds the deny-by-default policy and a fresh nonce on its own scripts; 5 webview shows an inert
page with no network.

## TRUST-009 What the page and the host exchange is checked and never applied to another version (606 words)

SwRS: BLOCK-238, FMEDIT-054, GFM-027, TRUST-052, 059, 061, 062, 063, 064, 065, 086, 090.

1. **M** TRUST-061, 062, 063, 064 are rows of one behaviour: they share one test,
   `test/core/protocol/hostToPage.test.ts:90-93` "the payload checks refuse what the page used to
   refuse". Mapping: merge into TRUST-059 as a table of host-message checks.
2. **M** BLOCK-238, FMEDIT-054, GFM-027, TRUST-086 (and DIAG-050) are feature-owned request bounds; the
   StRS rationale itself says those live with the feature. Cite TRUST-052 by `depends_on` and drop
   TRUST-009 from their `derives_from`.
3. **L** The rationale points at "the rendering-core record for ignored messages": the rule is TRUST-052
   (trust scope); TRUST-052 wrongly also derives CORE-001.
4. **M** TRUST-090 untested: default timeouts (6 s, 10 min), late answer after a timeout, no callback after
   cancel, 15 s comment timeout. Markers are on the validator registry entries
   (`src/core/protocol/pageToHost.ts:227-366`, `hostToPage.ts:371-449`): well placed.

Validation test: none. `test/integration/blockMove.test.ts` `run()` and `commentWrite.test.ts` `run()`
(stale render answered as out of date, TRUST-065) can serve.

Diagram (sequence): Page, Host message gate, Session (current render), Feature handler. 1 page sends a
message; 2 gate checks type and envelope, else ignores; 3 session matches render and document, else
answers "out of date" or drops; 4 handler acts; 5 host answers by id; 6 page accepts only registered,
addressed, in-bounds answers.

## TRUST-012 Visible text and the icon speak of the product (149 words)

SwRS: TRUST-070, TRUST-074.

1. **M** TRUST-074 mixes the icon (this StRS) and the shipped bundle (TRUST-014); split. Its implementation
   marker is the companion `src/page/modules/plantumlBundle.markers.ts` (the bundle is built by
   `esbuild.mjs`).
2. TRUST-070 `annotation_exemption: true` with a sound reason; test `test/security/userFacingText.test.ts:131`.

Validation test: none. `test/security/package-contract.test.ts:20` (icon) and `userFacingText.test.ts:131`
can serve.

Diagram (use case): actor Reader; use cases read messages (no build-tool name), find the Studio in the
Extensions view (own icon).

## TRUST-014 The extension is built from pinned dependencies and ships what it loads (263 words)

SwRS: CORE-069, 080..086, TRUST-074, TRUST-075.

1. **H** CORE-069 and CORE-080..086 (published site: requirements home, area pages, Main-path maps,
   behaviour pages, History, search index, social cards, cream look) have nothing to do with pinned
   dependencies. Add a StRS "A reviewer reads the project's published site and its requirements" and move
   the eight SwRS there.
2. **M** Their implementation markers are companion files `src/core/render/requirementsViewer.markers.ts`
   (7 IDs) and `src/core/render/siteTheme.markers.ts`: the code lives in `test/site/` and the markers in
   the rendering core. Same pattern as CORE-070 and TRUST-074, while CORE-075/076/078 use
   `annotation_exemption` with markers written in `scripts/`. Pick one convention: add `scripts/` and
   `test/site/` to the scope `source_dirs` so markers sit on the code, and remove the companions.
3. **M** Unmarked tests: CORE-069 `test/site/requirementsViewer/home.test.ts:18, :46`, `write.test.ts:25`;
   CORE-081 `pages.test.ts:56, :74`; CORE-084 `search.test.ts:8`; CORE-085 `cards.test.ts:18, :38`.
4. TRUST-075 `annotation_exemption: true` (declarative `.nvmrc`), sound.

Validation test: none. `test/security/package-contract.test.ts:368` (VSIX contents) can serve.

Diagram (use case): actor Maintainer; use cases install on pinned Node from the official registry, build
the bundles, package the VSIX with the bundles the page loads.

## SwRS of these scopes outside these StRS (orphans)

No in-force SwRS of the three scopes lacks an in-force parent. One is derived only from another scope:

- **H** DIAG-128 "Exported diagrams are drawn images in the theme of the file" (parent StRS-TOOLBAR-014)
  has no `@implements_req`, `annotation_exemption: false`. Cause: commit abc9e650 (CR 288, export to HTML)
  added the SwRS and its tests (`test/page/modules/exportSnapshot.test.ts:166, :179, :198, :205`,
  `test/integration/exportHtml.test.ts:48`) but put `@implements_req SwRS-MDOKFSTUDIO-TOOLBAR-137` on the
  code that does the behaviour: `src/page/modules/exportSnapshot.ts:84` `whenDiagramsSettled` (with
  `DIAGRAM_SELECTOR` `:14` and `isPending` `:39`); the "diagram kept as a data image" step is
  `src/core/export/exportContent.ts:260`. No gate caught it: `okfreq validate` reports 0 errors and no
  check requires an implementation marker on a non-exempt in-force SwRS. Fix: add the marker at
  `exportSnapshot.ts:84` (and `exportContent.ts:260`); consider a check for in-force, non-exempt SwRS
  without an implementation file.

## Counts by category

| Category | H | M | L | Examples |
|---|---|---|---|---|
| Misparented SwRS / missing StRS | 3 | 7 | 0 | CORE-073..078 under CORE-001; CORE-069/080-086 under TRUST-014; DIAG-121..127 under Mermaid; REVIEW-017/038, DIAG-001, LIFE-026, CORE-041, TRUST-052, TRUST-065/090 parents |
| StRS behaviour without SwRS / contradiction | 4 | 1 | 0 | CORE-002 "edit from include"; CORE-001 trust-refusal path; GFM-029 vs CORE-071; DIAG-007 concurrency; TRUST-002 title |
| Merge (scenarios of one behaviour, repeated rule) | 0 | 6 | 0 | TRUST-061..064 -> 059; TRUST-006 -> 005; roots rule x6; "drawn once" x4; "renderer loads only when needed" x3; feature validators under TRUST-009 |
| Split (several behaviours in one SwRS) | 0 | 6 | 0 | CORE-001, CORE-028, DIAG-001, DIAG-084, DIAG-097, TRUST-002 (+ TRUST-074) |
| Internals, not observable | 0 | 1 | 0 | CORE-070 (and the warm-up scenario of CORE-001) |
| Marker misplaced / missing | 1 | 7 | 1 | DIAG-128 none; CSS header blocks; `rewriteNode` 8 IDs; DIAG-024, DIAG-032, DIAG-097 on wrong code; companion `*.markers.ts` (4 files); test-file header markers; CORE-043 custom editor |
| Test gaps / unmarked tests / stale notes | 1 | 12 | 2 | DIAG-084 test passes by timeout; 32 tests named in notes without a marker; untested refusal/boundary rows on Main paths (CORE-025, DIAG-005); DIAG-009 stale notes |
| StRS without validation test | 0 | 5 | 0 | CORE-002, TRUST-006, TRUST-009, TRUST-012, TRUST-014 (TRUST-004 partial) |
| StRS length | 0 | 4 | 2 | DIAG-001/006/007/009 over 1000 words; TRUST-012, CORE-002 thin |
| Wording / prose warnings | 0 | 0 | 3 | W002 on 5 SwRS; TRUST-009 stale cross-reference; DIAG-009 known-issue half stale |
| **Total** | **9** | **49** | **10** | |

StRS: 13 in force; 7 need re-parenting or a new StRS (3 new StRS proposed: charts and SVG pictures;
writing skill and release tooling; published site), 4 too verbose, 5 without a validation test. SwRS: 92
audited; 34 have at least one parent to change (including the 7 chart/SVG and 8 site SwRS that need a
new StRS); 9 merge candidates; 7 split candidates; 1 without an implementation marker (DIAG-128); 5 exempt
with a sound reason (CORE-075, 076, 078, TRUST-070, 075); 32 tests named in verification notes carry no
marker.
