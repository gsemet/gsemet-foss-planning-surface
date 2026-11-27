# CR-521 verification

Head: 4000024f8220ac13bbdba952af5f6a701994f216

Base for comparisons: `b9b29c5a34e6d6e24b898513f5fad44c4515b52c` (origin/main). Every claim below was judged at the head
(`4000024`) unless it names another SHA. Date: 2026-11-27. `<worktree>`: the CR worktree. `<base>`: a detached worktree
of `b9b29c5a`, removed after the run. `<CR>`: this change's folder. Logs are in `<CR>/work/scratch/` unless said.

Verdict in one line: the rule works for every render state, but a PlantUML syntax error with the default engine ends in
state `rendered`, so a figure that failed now loses its source (claim 3, and the description in claim 12).

## 0. Head under test: PASS

- `git rev-parse HEAD` in `<worktree>`: `4000024f8220ac13bbdba952af5f6a701994f216`; `git status --porcelain`: 0 lines,
  also after every probe.
- `gh pr view 553 --json headRefOid,isDraft,state,mergeStateStatus`:
  `{"headRefOid":"4000024f...","isDraft":true,"state":"OPEN","mergeStateStatus":"CLEAN"}`. The remote branch ref is the
  same SHA (`git ls-remote origin <branch>`: `4000024f8220ac13bbdba952af5f6a701994f216`).

## 1. A drawn figure shows no source panel; a failed one (state error or unavailable) shows it closed, and it opens: PASS

Command (builds the real preview page and bundles, exports through the real `HtmlExportController`, opens the file with
JavaScript off):
`fnm exec -- node --import ./scripts/register-myst-patches.mjs <CR>/work/verifier/realflow.cjs <worktree> <out> assert`,
log `v-realflow-head.log`.

Preview, engine built-in (word: state, `display` of the panel, height of its summary, open):

```text
wmermaiddrawn  rendered     none    0  closed     wmermaidfail   error        block  20  closed
wplantdrawn    rendered     none    0  closed     wplantrefused  unavailable  block  20  closed
wlitedrawn     rendered     none    0  closed     wplantmissing  error        block  20  closed
wvegadrawn     rendered     none    0  closed     wlitefail      error        block  20  closed
wnoteddrawn    rendered     none    0  closed     wvegafail      error        block  20  closed
                                                  wnotedfail     error        block  20  closed
clicks, each of the six failed: openAfterClick true, codeVisible true, openAfterSecondClick false
export: ok true, userGesture true, scripts 0; the eleven rows (JavaScript off) equal the preview rows
export clicks, each of the six failed: openAfterClick true, codeVisible true, openAfterSecondClick false
pageErrors: none
```

- JAR pipeline (made-up absent JAR path): the three PlantUML figures are `unavailable` and show the panel, closed, in
  preview and export; the other rows are the same.
- Pending (no diagram runtime): all eleven panels `display: none`.
- A real drawn PlantUML picture from a JAR was not available on this machine: see claim 7 (CI, v04 and v05) and claim 5.

Base `b9b29c5a`, same command (`v-realflow-base.log`): drawn Mermaid and PlantUML panels `block` in preview and export;
chart panels `none` in the preview, failed ones too; all panels `block` in the export; pending Mermaid and PlantUML
panels `block`.

## 2. Find bar: a hidden source is not matched, a failed figure's source is: PASS

Same run, section `find` (Ctrl+F in the page, each word is only in one figure's source and diagram text):

```text
head: wmermaiddrawn, wplantdrawn, wlitedrawn, wvegadrawn, wnoteddrawn : "No results"
      wplantrefused, wplantmissing : "1 of 1" in myst-plantuml-source
      wlitefail, wvegafail         : "1 of 1" in myst-vega-source
      wmermaidfail, wnotedfail     : "1 of 2" in myst-mermaid-diagram and myst-mermaid-source
      openPanels 0 in every row; pending: "1 of 1" in the diagram element only
base: wmermaiddrawn "1 of 1" in myst-mermaid-source, wplantdrawn "1 of 1" in myst-plantuml-source;
      wlitefail, wvegafail "No results"
```

## 3. "A figure that fails to render keeps its source panel" (specification Goal, decision 3): FAIL

PlantUML syntax error, default built-in engine. Three sources (a stray line, a bad arrow, a broken class body), each in
`@startuml`. Command: as claim 1 with mode `syntax`, logs `v-realflow-syntax.log` (head) and
`v-realflow-syntax-base.log` (base).

```text
head 4000024, preview AND export (JavaScript off):
  wplantsyntaxline   rendered  "Diagram source"  display none   summaryBox 0
  wplantsyntaxarrow  rendered  "Diagram source"  display none   summaryBox 0
  wplantsyntaxclass  rendered  "Diagram source"  display none   summaryBox 0
  picture text: "... [From textarea (line 3) ] @startuml class A {  Syntax Error? (Assumed diagram type: sequence)"
base b9b29c5, preview AND export: the same three rows with display block, summaryBox 20
```

- The engine answers a syntax error with its own error picture through the success path
  (`src/page/modules/plantumlDiagram.ts`, `showImage` sets `rendered`; its comment: "Without this check the engine draws
  its own error picture"). The picture holds the source only up to the failing line: the lines after it (`+x : int`,
  `activate ??? !!`) are in neither the picture nor a shown panel, so a reader of an export loses them.
- The owner's question in `02-answers.md` named "a syntax error" among the failures; the answer was « Garder la source ».
- Approved StRS DIAG-006: "keep the source readable when the bundled engine cannot draw it", "a failed or oversized
  source shows its cause; ... no picture, and keep the source".
- SwRS DIAG-032 (`proposed`), line 99: "the engine rejects a diagram (syntax error) with a reason | ... no picture,
  state error, and the source is kept". The real engine does not reject here (the same at base); the "source is kept"
  part is what this change breaks.
- The letter of the rule (panel only for `data-render-state` `error` or `unavailable`) is met: the state is wrong for
  this failure. Mermaid, chart and JAR failures do set `error` or `unavailable`.
- Pictures: `verifier/evidence/before-plantuml-syntax-error-light.png`, `after-plantuml-syntax-error-light.png`.

## 4. Edit mode: the click on "Diagram source" of a failed figure opens the editor: PASS

Same run as claim 1, section `editMode` (`data-sphinx-preview-edit-mode` on):

```text
wmermaidfail   visible true  previewEditOpen [[13,17]]  disclosureOpen false  editor first line ```mermaid
wplantrefused  visible true  previewEditOpen [[30,36]]  disclosureOpen false  editor first line ```plantuml
wnotedfail     visible true  previewEditOpen [[85,91]]  disclosureOpen false  editor first line ```{mermaid}
```

Base `b9b29c5a` gives the same three rows (behaviour unchanged).

## 5. New or changed tests fail on the base and pass at the head: PASS

`<base>` holds `src/` of `b9b29c5a` and `test/` of `4000024` (`git checkout 4000024f... -- test/`), compiled and bundled.

Page tests: `fnm exec -- node scripts/node-test.mjs verif out/test/page/blockReq.requirements.test.js
out/test/page/chartCsp.test.js out/test/page/modules/chartError.test.js out/test/page/modules/findIndex.test.js`

```text
base (v-tests-base.log): exit 1, tests 60, pass 55, fail 5
  only the broken chart shows its Chart source section, closed, in reading and edit mode, under its message
  the HTML export shows only the Chart source section of the broken chart, closed, and keeps the charts as inline SVG
  the preview sheet hides the three source panels and shows them for a failed figure; the export sheet adds no rule
  the source panel of a drawn or drawing figure is hidden and not searched
  the source panel of a failed figure is searched, and only that one
head (v-tests-head.log): exit 0, tests 60, pass 60, fail 0
```

The edit-mode click test of `blockReq` passes on both: it asserts unchanged behaviour (the `chartError` hunk beside the
new test is a comment).

Visual: `renderFixtures.js`, then `uv run --no-sync --group docs python test/visual/capture.py --scenario
diagrams/v04..v16 --scenario toolbar-navigation/v42-export-html-cream-900 --scenario
toolbar-navigation/v43-export-html-dark-900` (`v-capture-<worktree>.log`).

```text
base: failed v10, v11, v13, v14 ("the source disclosure is present and not shown"),
      v42, v43 ("the source of the drawn Mermaid diagram is displayed"), v04, v05, v15, v16;
      passed v06-v09, v12 (failed figures, shown at base too)
head: passed v06-v14, v42, v43; failed v04, v05 ("requires a loaded image", no PlantUML here) and v15, v16
      ("not drawn by the built-in engine", the same on base); all four pass in CI (claim 7)
```

The new v04/v05 assertion, without PlantUML: `uv run --no-sync --group docs python
<CR>/work/verifier/drawn_jar_check.py <worktree>` puts a loaded picture in the v04 and v05 pages and runs the real
`PAGE_CHECKS` (`v-drawn-jar-<worktree>.log`).

```text
base: exit 1, v04 and v05: ['PlantUML diagram 1 must not display its source disclosure']
head: exit 0, v04 and v05: PlantUML failures: []
```

## 6. Approved StRS DIAG-001 and DIAG-006 hold exactly the listed changes; requirements lint: PASS

`git diff --word-diff b9b29c5a..HEAD -- requirements/tiers/strs`

- DIAG-001: description and normative text ("keep its source available" now "... when the diagram fails to render"),
  `user_need` (", with the source one click away" removed), use case diagram reply "picture", the "Reading" bullet,
  Path S1 line; `approved_at` 2026-11-25 to `2026-11-27T11:54:00+01:00` and the generated `verified.at`.
- DIAG-006: the "Reading" bullet, `approved_at` and `verified.at`. Nothing else.
- Both: `req_lifecycle: approved`, `approved_by` equals the file's `default_owner_email` (compared, "yes"), the time
  carries its UTC offset. The description lists both under "Approved requirements changed".
- The nine other changed requirement files read `req_lifecycle: proposed` (StRS DIAG-009, DIAG-015; SwRS BLOCK-014,
  DIAG-001, 023, 068, 105, 121, 123), as the log entry says. No deprecated requirement is in the diff. SwRS diff read
  (`git diff b9b29c5a..HEAD -- requirements/tiers/swrs`): S1, S3, S4, S7 and wording as the specification lists.
- `just requirements-lint`: exit 0; "0 indexes would change", "0 requirement OKF projections would change",
  "0 files would change", "main paths: 96 StRS checked, 625 SwRS citations, all valid", "use case diagrams: 94 StRS
  checked, all parse". The W2 broken-link warnings shown are in `palette-slash` files this change does not edit.

## 7. CI at the head, and the PlantUML scenarios: PASS

- `gh pr checks 553`: exit 0; checks, report, static, static-windows, viewer-graph, visual, visual-2 pass (7); 10
  skipped.
- `gh run view 45997063361`: `workflow_dispatch`, headSha `4000024f8220...`, conclusion success. Success: static,
  static-windows, visual, visual-2, viewer-graph, integration, acceptance (trust-security), stress, report, checks,
  gallery. Skipped: release-check, perf-547, toc-loop, tag-release, release, pages.
- Job logs (`artifacts-45997063361/job-140499025312.log`, `...321.log`): `ci-visual 1` and `ci-visual 2` installed
  PlantUML 1.2020.2; 274 and 256 "passed:" lines, 0 "failed:". Both jobs ran the PlantUML scenarios:

```text
passed: diagrams/v04-plantuml-success-light-900      passed: diagrams/v05-plantuml-success-dark-900
passed: diagrams/v06..v14                            passed: diagrams/v15-plantuml-include-light-900
passed: diagrams/v16-plantuml-include-dark-900       passed: toolbar-navigation/v42, v43 (export)
```

v04 and v05 (in the `visual` job) ran with the head's check "must not display its source disclosure"
(`test/visual/capture_support.py`) and passed. None of these scenarios has a PlantUML syntax error.

## 8. Local preflight gate: PASS

`<CR>/work/gates/preflight-4000024f.log`, first line `head 4000024f8220ac13bbdba952af5f6a701994f216`; end
`ci-static: passed`, "preflight: visual, viewer-graph, integration, acceptance, report and gallery stages skipped on
Windows; CI runs them", `preflight=0`. `handoff CR-521`: "at 4000024f8220: just preflight (static stage, Windows) exit 0
(work/gates/preflight-4000024f.log)". Not rerun here (no long gate in chantier.yaml).

## 9. Screenshots before and after, light and dark: PASS

Ten images and `before-after.md` in `<CR>/work/verifier/evidence/`, from `realflow.cjs` modes `shots` and `syntax` at
`b9b29c5a` and `4000024` (`v-shots-*.log`). Each image opened: no username, no home folder.

## 10. Review box: PASS

`log CR-521`: "r2 inspector approved at 17f6bb8651245dbe894266037f2ed728bb560ef7" and "r2 approved at 17f6bb86, committed
as 4000024f8220ac13bbdba952af5f6a701994f216", which is what the description's "Review" line says. It proves a review
happened, not the code. `git diff --stat 17f6bb86..4000024f`: CHANGELOG.md, SwRS DIAG-001 and DIAG-023,
`capture_support.py`, `scenarioIds.ts`.

## 11. Changelog and user documentation: FAIL (the changelog line; the rest passes)

`git diff b9b29c5a..HEAD -- CHANGELOG.md docs/`: one `## Unreleased` line ending
"(CR-521 remove-diagram-source-disclosure, PR #553)"; `docs/user/charts.md` states the rule for charts (matches claim 1);
a note in `docs/demo-video/clips/export-html/clip.md`. The changelog words "a figure that fails to render still shows its
source" are not true for the case of claim 3: FAIL with it.

## 12. PR description, as posted: FAIL

`gh pr view 553 --json body` (saved `pr-body-posted.md`): equal to `<CR>/work/pr-body.md` but for a trailing blank line.
`body_html` renders: ten sections, two tables, one code block. No change-request number or planning path in the body.

False or incomplete, all from claim 3:

- Summary: "a figure that fails to render keeps it, closed, so a reader of an exported file does not lose the content."
- Deliverables: "Mermaid or PlantUML, failed ... unchanged": a PlantUML syntax error showed the section before and does
  not now.
- Known gaps has no bullet for it.

Pending, the one expected item: Impacts says "Before and after screenshots: provisional, to be added."; the images of
claim 9 are not in the body yet.

Proved:

- Deliverables, other rows: base and head runs of claim 1 (drawn, failed Mermaid, drawn and failed chart, not yet drawn).
  The CSS sketch matches `contentBlockStyles.ts` (shortened: one selector of three, no content-root prefix).
- Changes: `git diff --stat` shows four `src/` files (`exportStyles.ts`, `contentBlockStyles.ts` and its markers file,
  `findIndex.ts`), none in `core/render` (markup unchanged); export file holds 0 scripts; find bar as in claim 2.
- Approved requirements changed: claim 6. "Agreed before the work started": `02-answers.md`, « Oui, d'accord ».
- Requirements changed table: all seven changed SwRS and the two proposed StRS are listed; the named tests carry the
  markers (`@tests_req`, `scenarioDefinitions1.ts` holds DIAG-105#S3).
- Impacts bullets and Blast radius: claims 1, 4 and the four-file source diff.
- Autonomous decisions and first Known gap (no new search on a state change): the only caller of the find bar's
  `refresh()` is the content patch (`src/page/features/contentPatch.ts:135`); the style rule: claim 1.
- Second Known gap: the "Criteria" line of SwRS DIAG-001 is unchanged in the diff.
- Test plan: preflight claim 8, review claim 10, CI claim 7, changelog claim 11, requirements claim 6.

Not failures, for the next edit of the body: the unchecked box "New or changed tests (they fail on the previous code)" is
now proved by claim 5; the third Known gap can say that CI ran the two PlantUML success scenarios at this head and they
passed; the note in the export-html clip document is not mentioned in "Changes".

## Left to do (not judged here)

Either the built-in engine's error picture counts as a failed render (state `error`, source kept, as the approved StRS
DIAG-006 and the owner's answer say), or the owner accepts the gap and the description, changelog and SwRS DIAG-032 say
so.

NOT VERIFIED
