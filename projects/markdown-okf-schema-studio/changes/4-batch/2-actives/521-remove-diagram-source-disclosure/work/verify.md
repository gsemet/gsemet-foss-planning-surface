# CR-521 verification

Head: 0afb09dc2f9712dbbcfd393563e9376e282375c4

Base for comparisons: `6b1dd90d176a9ed4a2139e2cf71e11eb02e9fc03` (origin/main). Every claim below was judged at the head
(`0afb09d`) unless it says `carried from`. Date: 2026-11-27. `<worktree>`: the CR worktree. `<base>`: a detached
worktree of `6b1dd90d`, removed after the run. `<CR>`: this change's folder. Logs are in `<CR>/work/scratch/v2/` unless
said. Probes: `<CR>/work/verifier/`, each run from its worktree as
`fnm exec -- node --import ./scripts/register-myst-patches.mjs <CR>/work/verifier/<script> <worktree> <out> <mode|set>`.
They build the real preview page and bundles in headless Chromium, export through the real `HtmlExportController`, and
open that file with JavaScript off.

Verdict in one line: the three `@startuml` syntax errors now keep their source, but an EBNF syntax error that the
built-in engine draws as "Syntax error!" still ends in state `rendered`, so that failed figure loses the source it
showed at base (claim 3, and with it claims 11 and 12).

## 0. Head under test: PASS

- Judged at `0afb09d`. `git rev-parse HEAD`: `0afb09dc2f9712dbbcfd393563e9376e282375c4`; `git status --porcelain`:
  0 lines after every probe; `git rev-parse origin/main`: `6b1dd90d176a...`.
- `git ls-remote origin refs/heads/<branch>`: `0afb09dc2f9712dbbcfd393563e9376e282375c4`. `gh pr view 553`:
  `{"headRefOid":"0afb09dc...","isDraft":true,"mergeStateStatus":"CLEAN","state":"OPEN"}` (read again at 14:52Z).
- Move since `4000024f`: `git range-diff` shows `17f6bb86`=`36cd7948` and `4000024f`=`e78c1b2c` unchanged, `0afb09dc`
  new; `b9b29c5a..6b1dd90d` touches only `.agents/guidelines/release-process.guidelines.md`.
  `git diff 4000024f 0afb09dc`: that file, `requirements/tiers/log.md`, SwRS DIAG-001 and DIAG-032,
  `diagrams/index.md`, `src/page/modules/plantumlDiagram.ts`, `test/page/chartPage.ts`,
  `test/page/modules/plantumlDiagram.test.ts`, `test/page/plantumlErrorPicture.test.ts`. Nothing under
  `requirements/tiers/strs`, `test/visual` or `src/core`.

## 1. A drawn figure shows no source panel; one in state error or unavailable shows it closed, and it opens: PASS

Judged at `0afb09d`. `realflow.cjs ... assert`, `v-assert-head.log` (state, `display`, summary height):

```text
preview, engine built-in
wmermaiddrawn rendered none 0     wmermaidfail  error       block 20 closed
wplantdrawn   rendered none 0     wplantrefused unavailable block 20 closed
wlitedrawn    rendered none 0     wplantmissing error       block 20 closed
wvegadrawn    rendered none 0     wlitefail     error       block 20 closed
wnoteddrawn   rendered none 0     wvegafail     error       block 20 closed
                                  wnotedfail    error       block 20 closed
clicks, six failed: openAfterClick true, codeVisible true, openAfterSecondClick false
export: {"ok":true,"userGesture":true,"scripts":0}; the eleven rows and the six clicks equal the preview
jar pipeline (absent JAR): the three PlantUML figures unavailable, block 20, closed, preview and export
pending (no runtime): all eleven display none
pageErrors: none
```

Base (`v-assert-base.log`): drawn and pending Mermaid and PlantUML panels shown; chart panels hidden in the preview,
failed ones too, and shown in the export.

Drawn PlantUML is not taken for an error (`kinds.cjs ... drawn`, `v-drawn-head.log`, 43 sources, light and dark,
preview and export): 35 end `rendered`, panel `none` (sequence, class, activity old and new, state, use case, component,
deployment, object, timing, ER, ArchiMate, mindmap, WBS, Gantt, JSON, YAML, salt, regex, EBNF, themes, and sources that
write the error words in notes, legend, header, caption or names). The other 8 are kinds the engine does not support
(`@startuml salt`, nwdiag, ditaa, board, files, chronology, wire, packet): `error`, panel shown.

Salt-like pictures (`kinds.cjs ... salt`, `v-salt-head.log`, 28 sources): light `@startsalt` whose first text is the
JSON, YAML or "Diagram not supported" message (also `msg | [OK]`, a `{+` grid, an imitated banner) ends `error`, the
same in dark `rendered`; a boxless mindmap or WBS whose root is one of the messages ends `error` in both themes. The
message as a button label, title, second line or part of longer text stays `rendered`. Each of these still draws; the
effect is a source shown under a drawn figure (see claim 12).

## 2. Find bar: a hidden source is not matched, a shown one is: PASS

Judged at `0afb09d`. Same run as claim 1, section `find`.

```text
head: wmermaiddrawn, wplantdrawn, wlitedrawn, wvegadrawn, wnoteddrawn : "No results"
      wplantrefused, wplantmissing : "1 of 1" in myst-plantuml-source
      wlitefail, wvegafail         : "1 of 1" in myst-vega-source
      wmermaidfail, wnotedfail     : "1 of 2" in myst-mermaid-diagram and myst-mermaid-source
      openPanels 0 in every row; pending: "1 of 1" in the diagram element only
base: wmermaiddrawn and wplantdrawn matched in their source; wvegadrawn "No results"
```

## 3. "A figure that fails to render keeps its source panel" (specification Goal, decision 3): FAIL

Judged at `0afb09d`.

Fixed since `4000024`: the three `@startuml` syntax errors (`realflow.cjs ... syntax`, `v-syntax-head.log`), light and
dark, preview and export: `error`, "Diagram source" `block` 20 closed, opens on click, found by Ctrl+F; base: `rendered`,
shown. In the sets `errors` and `errors2` (`v-errors-head.log`, `v-errors2-head.log`), 38 of 42 and 36 of 47 end `error`
with the panel shown; those ending `rendered` draw a diagram, except the EBNF ones below.

Still failing: EBNF syntax errors that the engine draws as "Syntax error!" (`realflow.cjs ... ebnf`,
`v-ebnf-head.log`, `v-ebnf-base.log`). Sources inside `@startebnf`: a valid `wplantebnfgood = "x", { "y" } ;`, then
`wplantebnfbad = [ "x" ;`, then `wplantebnfbar = digit, { digit } ;` with `digit = "0" | "1" | ;;`.

```text
head 0afb09d, light and dark, preview AND export (JavaScript off):
  wplantebnfbad  rendered  "Diagram source"  display none  summaryBox 0   picture says "Syntax error!"
  wplantebnfbar  rendered  "Diagram source"  display none  summaryBox 0   picture says "... digit digit Syntax error!"
  Ctrl+F for either word: "No results"; pageErrors none
base 6b1dd90, same sources: rendered, display block, summaryBox 20, opens on click, Ctrl+F "1 of 1" in the source
```

`kinds.cjs ... errors3` (`v-errors3-head.log`, `v-errors3-base.log`) gives the same for `a = ((( ;`, `a = [ "x" ;`,
`a = "x" | ;`, `a = b c ;` and a titled two-rule grammar ending `;;`: head `rendered`, `none`; base shown. `errors` and
`errors2` add `ebnfbad`, `ebnf_unclosed` and `ebnf_second` (a good rule then a bad one), the same at head. Other EBNF
errors (no `=`, unterminated string or comment, missing semicolon, `@startuml ebnf`) end `error`.

- `src/page/modules/plantumlDiagram.ts:154`, `ENGINE_ERROR_PICTURE`, matches the "[From ... (line N)]" banner, "Your
  data does not sound like JSON/YAML data" and "Diagram not supported ..."; not "Syntax error!".
- With the picture of `a = [ "x" ;` the reader sees only "Syntax error!": no line of the source is visible in the page
  or the export.
- The owner's answer in `02-answers.md` keeps the source on a syntax error (« Garder la source »). Approved StRS
  DIAG-006, line 91: "a failed or oversized source shows its cause; ... and keep the source". SwRS DIAG-032
  (`proposed`), statement: when "the built-in engine fails, the page SHALL say why, with the render state unavailable or
  error".
- Not counted as failures: unclosed `!if`, `!endfunction`, missing `@enduml`, creole, regex `a[b` and `a{2,1}`, EBNF
  `a = ;`, YAML `a: [` draw something and end `rendered`.
- Pictures: `verifier/evidence/before-plantuml-ebnf-error-*.png`, `after-plantuml-ebnf-error-*.png`.

## 4. Edit mode: the click on "Diagram source" of a failed figure opens the editor: PASS

Judged at `0afb09d`. Claim 1 run, section `editMode`; claim 3 `syntax` run.

```text
wmermaidfail      visible true  previewEditOpen [[13,17]]  disclosureOpen false  editor first line ```mermaid
wplantrefused     visible true  previewEditOpen [[30,36]]  disclosureOpen false  editor first line ```plantuml
wnotedfail        visible true  previewEditOpen [[85,91]]  disclosureOpen false  editor first line ```{mermaid}
wplantsyntaxline  visible true  previewEditOpen [[5,11]]   disclosureOpen false  editor first line ```plantuml
wplantsyntaxarrow visible true  previewEditOpen [[15,21]]  disclosureOpen false  (the same at base)
```

## 5. New or changed tests fail on the base and pass at the head: PASS

Judged at `0afb09d`. `<base>` held `src/` of `6b1dd90d` with `test/` of `0afb09d`, compiled and bundled.

`fnm exec -- node scripts/node-test.mjs verif out/test/page/blockReq.requirements.test.js
out/test/page/chartCsp.test.js out/test/page/modules/chartError.test.js out/test/page/modules/findIndex.test.js
out/test/page/modules/plantumlDiagram.test.js out/test/page/plantumlErrorPicture.test.js`

```text
base src (v-base-tests.log): exit 1, tests 83, pass 76, fail 7, skipped 0
  only the broken chart shows its Chart source section, closed, in reading and edit mode, under its message
  the HTML export shows only the Chart source section of the broken chart, closed, and keeps the charts as inline SVG
  the preview sheet hides the three source panels and shows them for a failed figure; the export sheet adds no rule
  the source panel of a drawn or drawing figure is hidden and not searched
  the source panel of a failed figure is searched, and only that one
  an error picture keeps the error state from memory too, until a changed include draws the diagram
  the built-in engine's error picture is a failed render that keeps its source, in the preview and the export
head (v-head-tests.log): exit 0, tests 83, pass 83, fail 0, skipped 0
round-3 tests on the previous src e78c1b2c with head test/ (v-r3prev-tests.log): exit 1, tests 23, pass 21, fail 2
  (the last two above; actual rendered/none, expected error/block)
```

Visual at head: `renderFixtures.js`, then `uv run --no-sync --group docs python test/visual/capture.py --scenario
diagrams/v04..v18 --scenario toolbar-navigation/v42-... --scenario toolbar-navigation/v43-...` (`v-capture-head.log`):
passed v06-v14, v17, v18, v42, v43; failed v04, v05 ("requires a loaded image", no PlantUML here) and v15, v16 ("not
drawn by the built-in engine"); all four pass in CI (claim 7). `drawn_jar_check.py <worktree>`
(`v-drawn-jar-head.log`): exit 0, v04 and v05 `PlantUML failures: []`.

Base visual results, carried from 4000024: base moved by one guideline file, and round 3 changed no visual file or CSS.
Base failed v10, v11, v13, v14, v42, v43 (source shown under a drawn diagram), v04, v05, v15, v16; the picture check
failed on v04 and v05 with "PlantUML diagram 1 must not display its source disclosure".

## 6. Approved StRS DIAG-001 and DIAG-006 hold exactly the listed changes; requirements lint: PASS

Judged at `0afb09d`. `git diff --word-diff 6b1dd90d..HEAD -- requirements/tiers/strs`:

- DIAG-001: description and normative text ("keep its source available when the diagram fails to render"), `user_need`
  (", with the source one click away" removed), use case reply "picture", the "Reading" bullet, Path S1 line,
  `approved_at` 2026-11-25T15:37:43+01:00 to 2026-11-27T11:54:00+01:00, `verified.at`.
- DIAG-006: the "Reading" bullet, `approved_at`, `verified.at`. Both `req_lifecycle: approved`.
- `approved_by` equals the owner's address: carried from 4000024: no StRS file changed in round 3.
- The other changed requirement files read `proposed`: StRS DIAG-009, 015; SwRS BLOCK-014, DIAG-001, 023, 032, 068,
  105, 121, 123.
- `just requirements-lint` (`v-reqlint.log`): exit 0; "0 indexes would change", "0 requirement OKF projections would
  change", "0 files would change", "96 StRS checked, 625 SwRS citations, all valid", "94 StRS checked, all parse
  (Mermaid 12.2.0)".

## 7. CI at the head, and the PlantUML scenarios: PASS

Judged at `0afb09d`.

- `gh pr checks 553`: exit 0; checks, report, static, static-windows, viewer-graph, visual, visual-2 pass; 10 skipping.
- `gh run view 46012817304 --json headSha,event,conclusion`:
  `{"conclusion":"success","event":"workflow_dispatch","headSha":"0afb09dc..."}`; viewer-graph, acceptance
  (trust-security), stress, visual-2, visual, static-windows, static, integration, report, gallery, checks succeeded;
  toc-loop, perf-547, release-check, tag-release, pages, release skipped.
- Job logs in `<CR>/work/scratch/artifacts-46012817304/`: `job-140552342371.log` (visual) 274 "passed:", 0 failed;
  `job-140552342354.log` (visual-2) 256, 0 failed. v04-v18, v42 and v43 are among the passed lines.
- `job-140552342507.log` (static) and `job-140552342399.log` (static-windows): "the built-in engine's error picture is a
  failed render ..." and "only the broken chart shows ..." are skipped, "no Chromium can start here"; the fake-engine
  test "an error picture keeps the error state ..." passes in both.

## 8. Local preflight gate: PASS

Judged at `0afb09d`. `<CR>/work/gates/preflight-0afb09dc.log`, first line
`0afb09dc2f9712dbbcfd393563e9376e282375c4`; check-no-merge-commits passed (3 commits); unit tests 5571, pass 5563, fail
0, skipped 8; security 116; clip-kit 56; Python 298 and 4 passed; requirements lint clean; `ci-static: passed`;
"preflight: visual, viewer-graph, integration, acceptance, report and gallery stages skipped on Windows; CI runs them".
`handoff CR-521` note: "at 0afb09dc...: just preflight (static stage, Windows) exit 0
(work/gates/preflight-0afb09dc.log)". Not rerun here.

## 9. Screenshots before and after, light and dark: PASS

Judged at `0afb09d` (before at `6b1dd90`). Eighteen images and `before-after.md` in `<CR>/work/verifier/evidence/`,
from `realflow.cjs` modes `shots`, `syntax`, `ebnf` (`v-shots-*.log`, `v-syntax-*.log`, `v-ebnf-*.log`). Each image
opened: no username, no home folder. `cmp` of the before and after syntax-error pairs: identical; the other seven pairs
differ.

## 10. Review box: PASS

Judged at `0afb09d`. The body's "Review" box is unticked (the Driver fills it). `log CR-521`: "r3 inspector
FIX-REQUIRED on pr-body only ... fixed", "r3 body re-inspection approved at 4000024f8220...", "r3 approved at 4000024f,
committed as 757c4d4b...", then a clean rebase 757c4d4b to 0afb09dc onto 6b1dd90d. It proves a review happened, not the
code.

## 11. Changelog and user documentation: FAIL (the changelog line; the rest passes)

Judged at `0afb09d`. `git diff 6b1dd90d..HEAD -- CHANGELOG.md`: one `## Unreleased` entry: "A Mermaid or PlantUML
diagram or a chart that draws no longer has a source section under it, in the preview and in the HTML export; a figure
that fails to render still shows its source, closed, under its message (CR-521 remove-diagram-source-disclosure, PR
#553)". The second half is untrue for the EBNF errors of claim 3.

`docs/user/charts.md` and `docs/demo-video/clips/export-html/clip.md`: carried from 4000024: unchanged by round 3.

## 12. PR description, as posted: FAIL

Judged at `0afb09d`. `gh pr view 553 --json body` (saved `pr-body-now.md`): equal to `<CR>/work/pr-body.md`; no
change-request number or planning path.

False or incomplete:

- Summary: "a figure that fails to render keeps it, closed" (claim 3).
- Deliverables: "Mermaid or PlantUML, failed ... unchanged": an EBNF syntax error showed the section at base, not now.
- Changes: "Built-in PlantUML engine: its syntax-error picture now marks the figure as failed." and Autonomous
  decisions "A PlantUML syntax error that the built-in engine draws as its own error picture counts as a failed render":
  not for "Syntax error!".
- Known gaps has no bullet for the EBNF case.
- Known gaps, salt bullet, is narrower than the product: it names a light `@startsalt` with the JSON message; the YAML
  and "Diagram not supported" messages do the same, and a boxless mindmap or WBS does it in both themes (claim 1).
- Known gaps omits two limits that SwRS DIAG-032 "Known issues" states (a crash picture is not recognised; a source
  drawn in part counts as drawn).

Pending, not failures: "Before and after screenshots: provisional, to be added." and the unticked Test plan boxes (New
or changed tests, now proved by claim 5; Local gates; Review; CI green).

Proved:

- Deliverables, other rows: claim 1 at base and head. The export needs no JavaScript.
- Changes: find bar as in claim 2; the `@startuml` syntax errors as in claim 3.
- Requirements changed table: lists the eight changed SwRS and the proposed StRS DIAG-009 and 015 (`git diff --stat
  6b1dd90d..HEAD`); DIAG-105#S3 is marked at `test/visual/scenarioDefinitions1.ts:400`, its check in
  `capture_support.py:234-238`.
- Known gaps: the real-engine test is skipped by the static CI jobs (claim 7); its file names no dark theme.
- Approved requirements changed: claim 6. "Agreed before the work started" (`02-answers.md`, « Oui, d'accord ») and
  the find-bar bullets: carried from 4000024: `findIndex.ts` and the answers unchanged.

## Left to do (not judged here)

Either the "Syntax error!" picture of an EBNF source counts as a failed render (state `error`, source shown), or the
owner accepts the gap and the description, changelog and SwRS DIAG-032 say so.

NOT VERIFIED
