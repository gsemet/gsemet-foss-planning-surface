# CR-512 verification

Head: e76c084313d826eeab7148418658c4394c5a33f2

Verdict: **VERIFIED**. Pass 1: the pushed head. Pass 2: the description alone, on the body as posted
after pass 1. Pass 3: the description alone, on the body posted again at 10:44:47Z with one caption
and its image removed (head unchanged in all passes; pass 3 is the judgment of the posted body now).
Draft pull request
https://github.com/gsemet/markdown-okf-schema-studio/pull/536, base
`chantier/batch-09/cr-509-reliable-heavy-ci-split-the-trusted-laun`
(`89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4`). Outcome reached: 2c, "cannot reproduce" (treated as 2b).

`WT` is the CR worktree, `W` the CR's `work/` folder. All claims are judged at `e76c084` unless a
line says `carried from <sha7>`. Commands ran from `WT` (Git Bash).

## State (pass 1)

- `git rev-parse HEAD` = `e76c084313d826eeab7148418658c4394c5a33f2`; `git status --porcelain
  --untracked-files=all` empty (checked again after the runs and cleanup).
- `git ls-remote origin`: cr-512 branch = `e76c084...`, cr-509 branch = `89cae5ff...`.
- `gh pr view 536`: head `e76c084...`, base the cr-509 branch, draft, OPEN.
- `git diff --stat 89cae5ff HEAD`: 8 files, +122/-11 (clip.md, scenario.mjs, feature clip
  guideline, requirements log, SwRS TABLE-120, realInput/run.ts, realInput/tableGridPaste.ts,
  test/shared/stressPlan.ts). One commit, `e76c0843`.

## Specification claims (pass 1; head unchanged since)

| # | Claim | Result | Proof at `e76c084` |
| --- | --- | --- | --- |
| S1 | Second real-window scenario with the clip's stage document inlined, `stage/tasks.tsv` on the clipboard, click on header cell "Task", Ctrl/Cmd+V through `press()`, no Ctrl+A | proven | `test/integration/realInput/tableGridPaste.ts` lines 81-147: `CHECKLIST_DOCUMENT`, `TASKS_TSV`, `clipboard.writeText(TASKS_TSV)`, `th` /^Task$/ click, `waitForEditor`, `press(page, modifier+v)` |
| S2 | Checks: source equals the clip's `EXPECTED`; `waitFor("the editor open in the header cell Task")`; the open editor is in the header cell of column 0 and shows "Task" | proven | lines 136-157: `assert.equal(clip.EXPECTED, PASTED_CHECKLIST)`, buffer === `PASTED_CHECKLIST`, open editors == `[{rows:5,tag:"TH",row:0,column:0,text:"Task"}]`, asserted again after `waitForPageSettled` |
| S3 | Name `scenarioTableGridPasteFromHeader`, `@tests_req ...TABLE-120#S3`, run from the "table-grid-paste" entry and the full trusted run next to `scenarioTableGridPaste` | proven | tableGridPaste.ts lines 131-133; `run.ts` lines 242-245 and 312-316. SwRS S3 is "Start in the header row" |
| S4 | Guards read the shipped files (stage document, stage clipboard text, `EXPECTED`); a mismatch fails the test | proven | lines 134-137 read `stage/release-checklist.md`, `stage/tasks.tsv`, import `scenario.mjs`; the runs of pass 1 pass at head; mismatch case: `W/run9-r2-mismatch.log` `AssertionError` ("Dev, Fri" against "Dev, Thu"), carried from b5aaf68 plus the then uncommitted test, whose file was last edited before that run and is the committed one |
| S5 | Passes locally in a real window with `STUDIO_REAL_INPUT_SCENARIO=table-grid-paste` | proven (Verifier run) | `env STUDIO_REAL_INPUT_SCENARIO=table-grid-paste fnm exec -- npm run test:integration -- --trusted-only`: exit 0, VS Code 1.148.0, `STEP done: real-input (6442 ms)` (`W/verifier/run-head-single.log`). Process list before: no other test or clip VS Code instance |
| S6 | Passes in CI's real-window jobs | proven | `gh run view`: 45794447911 and 45794466293, `workflow_dispatch`, headSha `e76c084`, success. Both integration logs: `STEP done: real-input` (408016 ms; 450553 ms) and `ci-integration: passed` (`W/ci-45794447911-integration.log`, `W/verifier/ci-45794466293-integration.log`) |
| N1 | Narrowing runs, one difference at a time (copy in VS Code, auto-save 200 ms, clip timing), then all together; each recorded | proven | `W/runs.md` runs 2-6 and logs `W/run2..6-*.log`: each `STEP done: real-input`; paste types `["text/plain"]` (runs 2, 4, 5) and with `copymetadata`, `vscode-editor-data` (runs 3, 6). Carried from 8df99ce: temporary variants, product code identical (P1) |
| N2 | Clip run twice (current keys and `CLIP_KEY_COMMANDS=1`), `cellEditorOpenAfterPaste` recorded per take | proven | `W/take1..take5/verify.json`: all `passed: true`, `cellEditorOpenAfterPaste: true`, `cellEditorOpen: false`. Carried from 8df99ce: takes 1-4 with a temporary trace record, take 5 on the round 1 script; `git diff da61cefe e76c084 -- .../scenario.mjs` changes comment lines only. Take at head: see matrix (b) |
| N3 | Record in `work/`, summarized in the pull request body | proven | `W/runs.md`; the body's Deliverables table |
| C1 | 2c: scenario committed; guideline sentence in "1. The kit and a take" says the miss did not reproduce and names the commit | proven | diff of `feature-clip-process.guidelines.md`: sentence next to the drive functions, "did not reproduce in runs on a branch whose product code (`src/`, `sphinx/`) is identical to that of commit `3478f09`" |
| C2 | Clip comment and `clip.md` note drop "may or may not"; the take waits for the state it films; Done click kept when the editor is open | proven | `git grep -n -i "may or may" HEAD -- docs requirements test`: exit 1; diff of `scenario.mjs`: bounded wait until 4.4 s, record `cellEditorOpenAfterPaste`, Done click only if open; `clip.md` Shot row and note updated |
| R1 | TABLE-120 verification notes name the new scenario; behaviour unchanged; `req_lifecycle: proposed` (no re-approval) | proven | SwRS diff: one line, under "Verification notes"; frontmatter line 13 `req_lifecycle: proposed` |
| R2 | `requirements-update` done and dated `log.md` entry naming the outcome | proven | `log.md` 2026-11-26 entry "... did not reproduce (CR-512)", "Outcome: cannot reproduce". `fnm exec -- just requirements-lint`: exit 0, "1228 requirements, 0 errors, 26 warnings", "0 indexes would change", "0 requirement OKF projections would change", "0 files would change" (`W/verifier/run-head-requirements-lint.log`) |
| R3 | Writing skill not touched | proven | `git diff --name-only 89cae5ff HEAD -- src sphinx skills CHANGELOG.md docs/releases-notes package.json`: empty |
| O1 | No re-filming or re-rendering of the clip outputs | proven | `git diff --stat 89cae5ff HEAD -- .../paste-spreadsheet-cells/frames .../stage`: empty; the 8 changed files hold no media |
| O2 | Grid paste and other reopen paths unchanged | proven | same empty diff over `src` and `sphinx` |
| O3 | No OS-level keystroke tool | proven | `package.json` unchanged (empty diff); the scenario imports `press` from `./harness` |
| E1 | `just check` and `just preflight` pass (Windows: static stage) | cited | `W/gate-push-check.log`, `W/gate-push-preflight.log`: first line `head e76c084313d826eeab7148418658c4394c5a33f2`, last `exit 0 head e76c...`; preflight: "ci-static: passed", the other stages skipped on Windows. No gate is named in chantier.yaml, none run by the Verifier |
| P1 | The product code of all earlier runs is the head's | proven | empty: `git diff --name-only 8df99ce1 3478f099 -- src sphinx`, `git diff --name-only 3478f099 HEAD -- src sphinx`; `git merge-base --is-ancestor 3478f099 origin/main`: true |

## Host and default matrix (pass 1)

| Cell | Result | Rests on |
| --- | --- | --- |
| (a) auto-save off, header-row start: editor reopens on "Task" | proven | Verifier runs at head: single (S5) and `env STUDIO_REAL_INPUT_SCENARIO=stress STUDIO_STRESS_SCENARIOS=table-grid-paste-header STUDIO_STRESS_REPEAT=20 fnm exec -- npm run test:integration -- --trusted-only`: exit 0, PASS 1/20 to 20/20, "stress: 20 round(s) passed" (`W/verifier/run-head-stress20.log`). CI: two integration jobs (S6) and run 45794466293 stress, 11/11, "ci-stress: passed (11 rounds)" (`W/ci-45794466293-stress.log`). Auto-save off: no `files.autoSave` setting in `test/integration` or `package.json` (VS Code's shipped default) |
| (b) auto-save `afterDelay` 200 ms, header-row start: same | proven | Verifier clip take at head (VSIX from `just package` at head; `just clip paste-spreadsheet-cells setup`, `take`, both exit 0; VS Code 1.148.0, not the pinned 1.147.0): profile `files.autoSave: afterDelay`, delay 200; `verify.json` passed, file on disk equals the expected table, `cellEditorOpenAfterPaste: true`; frame at 4.26 s shows the editor in header cell "Task" (`W/verifier/evidence/after-autosave200-header-editor-open-4.26s.jpg`, `W/verifier/head-clip-take-verify.json`). Plus runs 4 and 6 and takes 1-5, carried from 8df99ce (P1). No committed test guards this cell; the body says so in "Known gaps" |
| (c) auto-save off, body-cell start: `scenarioTableGridPaste` stays green | proven | Body unchanged in the diff. The single run at head runs it first (`run.ts` 242-245), exit 0; CI integration jobs (S6) |

## Description pass 3: the body posted at 10:44:47Z

All rows judged at `e76c084`. Script: `W/verifier/pr536-pass3-check.py` (GraphQL
`pullRequest(number:536){body userContentEdits}` and `gh api .../pulls/536` with the
`application/vnd.github.full+json` accept header), run as `python -I <script>`; output in
`W/verifier/pr536-pass3.log`.

| Claim | Result | Proof at `e76c084` |
| --- | --- | --- |
| Head and base unmoved, still a draft | proven | `git ls-remote origin`: cr-512 `e76c084313d826eeab7148418658c4394c5a33f2`, cr-509 `89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4`; `gh pr view 536`: same head, base the cr-509 branch, `isDraft: true`, OPEN, updated 10:44:47Z |
| Posted body is the source file | proven | log: `posted == work/pr-body.md: True`, `posted == newest edit (10:44:47Z): True`, no BOM |
| The edit removes the caption and its image, nothing else | proven | log: unified diff of the 10:40:22Z body (pass 2) against the posted one: one hunk, `-26,11 +26,6`, five lines removed (blank, the two caption lines, blank, the `![...](.../d260cc30-...)` line), none added |
| Renders: sections, table, diagram, task list, no break left by the removal | proven | log, `body_html`: nine `<h2>` Summary to Internal references, 1 table of 12 rows (header and 11), `</table>` followed by the mermaid section holding the flowchart source (client-side drawing not observed), 7 of 7 task boxes checked |
| No image attached, so none can show the username or home folder | proven | log: 0 matches for `![`, `<img`, `user-attachments`, `raw.githubusercontent`, image or video file names; `body_html` `img: 0` |
| No text left pointing at the removed image | proven | log: no line matches image, screenshot, picture, capture, photo, frame, shown, below, above, following |
| Internal references only in their last section; no mark | proven | log: the only lines matching the username, home paths, planning words, role names, `UNVERIFIED`, `STALE`, `CR-<n>` are 107-108, under "Internal references" |
| Deliverables still shows the delivery; Impacts still holds its evidence | consistent | the table and the flowchart stay; Impacts reads "No visual change: no product code changes", the form `pull-request.guidelines.md` ("PR body for an external reader") asks for when nothing visible changes; the specification's "Evidence" section asks for no screenshot |
| No new Known gaps bullet owed | proven | `W/verifier/evidence/before-after.md`: "No visible change, so no before/after pair"; its image is proof of matrix cell (b), still cited here, and the body's table row "filmed again at `e76c084`" keeps its proof (`W/verifier/head-clip-take-verify.json`) |
| Review: approved at `e76c084` | proven | `$CHANTIER log CR-512`, 09:34:25Z: "r2 approved at b5aaf684..., committed as e76c084313d8..." |
| Verified at `e76c084` | proven | same log: `verdict result=VERIFIED head=e76c084...` at 10:37:39Z and 10:44:09Z |
| CI green at `e76c084` | proven | `gh pr checks 536`, run again: checks, report, static, static-windows, viewer-graph, visual pass; the others skipping |
| Every other claim | carried from e76c084 | pass 1 and pass 2 below: same head and base, and the diff above leaves their text unchanged |

The removed image stays in the body's edit history on the forge and its upload may stay reachable
(the Driver's note, 10:44:43Z); it is no longer attached to the description, and pass 2 had found no
username or home folder in it.

## Description pass (pass 2): the body posted at 10:40:22Z

The rows on the image (its resolving, its hash, the two looks) and "Edited: image caption" cover
content that pass 3 found removed; they no longer describe the posted body.

Read with `gh pr view 536 --json title,body,isDraft,headRefOid,baseRefName,files,commits` and
`gh api repos/gsemet/markdown-okf-schema-studio/pulls/536 -H "Accept:
application/vnd.github.full+json" --jq .body_html`. Head `e76c084...`, draft, OPEN, last update
10:40:22Z.

### Clean

| Claim | Result | Proof at `e76c084` |
| --- | --- | --- |
| Posted body is the source file | proven | `diff --strip-trailing-cr -B <posted body> W/pr-body.md`: no output |
| Sections, table, task list, diagram render | proven | `body_html`: nine `<h2>` (Summary to Internal references), the 11-row `<table>`, seven checked task items, a `mermaid` render section holding the flowchart source (standard syntax; the client-side drawing itself is not observed), the Claude Code line last. No fold: the project's template has none |
| Line breaks | consistent | no literal escape or broken block; the source's hard wraps show as `<br>` inside paragraphs and bullets (cosmetic) |
| The image resolves | proven | anonymous `curl -sL -w "%{http_code} %{content_type} %{size_download}" https://github.com/user-attachments/assets/d260cc30-bb2e-4d43-9213-42ad867f918c`: `200 image/jpeg 145958`; `body_html` has the `<img>` with its alt text; `gh repo view --json visibility`: PUBLIC |
| The image is the capture taken at the SHA it names | proven | `sha256sum` of the downloaded file and of `W/verifier/evidence/after-autosave200-header-editor-open-4.26s.jpg`: both `fc9e124b4c2d260cca46b156db9799375fde3b9e3b42132747f28d6eb4357748`; `before-after.md`: after at head `e76c084` |
| The look: what it claims | proven | opened: "Release 2.4 checklist" in Studio, cell editor open in the header cell "Task" (Done, Cancel), "Header, column 1 of 3", four body rows filled, `tasks.tsv` beside it. "Due" is out of view behind the widened first column, which "column 1 of 3" and the source pane agree with. Legible, nothing contradicts the caption |
| The look: no username, no home folder | proven | opened: title bar "release-checklist.md - workspace - Visual Studio Code", no path anywhere. Byte search of the file for the login name (`$USERNAME` = `gaeta`, home `C:\Users\gaeta`), `Users\`, `Exif`: no match |
| Internal references only in their last section; no role name | proven | search of the posted body for the username, drive or home paths, planning paths, batch, role names, `UNVERIFIED`, `STALE`, `CR-<n>`: only the two lines of "Internal references" (and the `s:/` of the two web addresses) |

### Claims

"Edited" marks what changed after pass 1 and was judged in this pass; the others carry pass 1's
proof at the same head.

| Claim | Result | Proof at `e76c084` |
| --- | --- | --- |
| Summary: editor stayed closed in 3 of 3 first attempts | proven | CR-489 `work/r1.md` lines 7-16 ("Reproduced 3 times"), as read in pass 1; `W/runs.md` "The earlier miss" |
| Summary: reopened in every run; no product code change | proven | S5, N1, N2, matrix; run 9's failure is the intended text mismatch, before any paste; R3 |
| Deliverables intro: real window, product code identical to `3478f09` (main branch) | proven | P1; `git diff --name-only 3478f099 origin/main -- src sphinx` and `... 3478f099 e76c084 -- src sphinx`: empty |
| Table rows 1-5 (narrowing runs, counts) | proven | runs 1-6 (`W/runs.md`), carried from 8df99ce (N1, P1) |
| "committed test ... pass (2 runs)" | proven | `W/run10-r2-single.log` (committed test file) and the S5 run at head |
| "repeated in one window, 20 of 20, in each of 2 runs" | proven | `W/run11-r2-stress20-header.log` and the stress run at head, both "20 round(s) passed" |
| Clip, both key ways, 5 of 5 takes | proven | N2 |
| Edited: clip filmed again at `e76c084`, VS Code 1.148.0, pinned 1.147.0, yes (1 take) | proven | `W/verifier/head-clip-take-verify.json`: `passed: true`, `cellEditorOpenAfterPaste: true`; `ls WT/.vscode-test`: only `vscode-win32-x64-archive-1.148.0`; `clip-kit/lib/platform.mjs` line 15 `DEFAULT_CODE_VERSION = "1.147.0"` |
| Edited: CI real-window suite (Linux) pass (2 runs) | proven | S6; `gh run view 45794447911` and `45794466293`: headSha `e76c084`, success |
| Edited: repeated alone in CI (Linux), 11 of 11 | proven | `W/ci-45794466293-stress.log`: `STUDIO_STRESS_SCENARIOS: table-grid-paste-header`, PASS 1/11 to 11/11, "stress: 11 round(s) passed" |
| Edited: image caption (take at `e76c084`, auto-save 200 ms, VS Code 1.148.0) | proven | matrix (b); `clip-kit/lib/profile.mjs` lines 54-55; the two image rows above |
| Diagram (paste, fill, one save, editor open; the new scenario checks fill and reopen) | proven | S2; one save is the requirement's behaviour, product code unchanged, and the diagram claims no new check of it |
| Changes: six bullets match the diff; nothing delivered is left out | consistent | `git diff 89cae5ff e76c084` (read again): the 8 files; `log.md` belongs to the requirement update |
| Impacts: "No visual change" with reason | proven | R3, O1; `W/verifier/evidence/before-after.md` |
| Blast radius, Grade 1 | consistent | tests, docs and one clip script only |
| Edited: test plan, new test also passes on the previous code | proven | product code equal on base and head (R3), the shipped files it reads unchanged, passes at head |
| Edited: requirements notes, marker, update and lint, 0 errors | proven | R1, R2, S3 |
| Changelog: no user-facing change | proven | R3 |
| Local gates at `e76c084` | proven | E1 (the template also asks for counts, which the line does not give; form only) |
| Review: approved at `e76c084` | proven | `$CHANTIER log CR-512`, 09:34:25Z: "r2 approved at b5aaf684..., committed as e76c084313d8..." |
| Edited: Verified at `e76c084` | proven | same log, 10:37:39Z: `verdict result=VERIFIED head=e76c084...` |
| CI green at `e76c084`; visual passed on its second run | proven | `gh pr checks 536` (run again): all pass or skipping; attempt 1 `visual` cut at 15 min after "ci-visual: passed" (pass 1, `W/ci-45794366914-visual.log` lines 1520-1521); the two heavy runs (S6) |
| Autonomous: stress step on demand | proven | `test/shared/stressPlan.ts` `STRESS_ON_DEMAND_SCENARIOS`; 21 default scenarios x 11 rounds 944760 ms, 22 would be 988320 ms, above the 960000 ms limit of `test/build/hangWatchdog.test.ts` (pass 1) |
| Autonomous: take waits up to 4.4 s; nothing else left out | proven | C2; `W/r1.md` "Decisions I took": the others are how runs were made, not choices the change ships |

### Known gaps

| Claim | Result | Proof at `e76c084` |
| --- | --- | --- |
| Cause not established | consistent | `W/runs.md`, "The earlier miss": no page trace |
| Late Done click about 0.3 s after 4.4 s, zoom after 4.8 s; outputs not re-rendered | proven | `scenario.mjs`: wait to 4.4 s, then a 0.3 s pointer move; `W/runs.md` take 5 timings; O1 |
| Edited: no committed check for the 200 ms auto-save case | proven | no `files.autoSave` in `test/integration`; the clip only records the state |
| Clip notes still say the copy puts HTML on the clipboard; none received | proven | `clip.md` line 80 at head; runs 3 and 6 paste types hold no `text/html` |
| Edited: the gap "takes made before the last edits, none repeated" removed | right | one take was made at head (matrix (b)) and is in the table |
| Complete: no gap missing | proven | no `UNVERIFIED` mark; no claim of this note failed; `before-after.md` says no pair exists because nothing visible changes, which Impacts states (the specification plans no screenshot pair); reviewer minors in the log (09:32:09Z): auto-save case listed, heavy runs since made, the `#S2` marker is the base's, not this change's |

## Notes (none changes the verdict)

- The body's "pass (2 runs)" and "20 of 20, in each of 2 runs": runs 7 and 8 (round 1) ran the test
  before the `EXPECTED` comparison and a marker fragment were added (same page actions and
  assertions). The counts hold for the committed test through runs 10 and 11 plus the two Verifier
  runs.
- "Real keyboard events" is the project's "real input": key events sent by `page.keyboard.press()`
  into a real window, not an OS-level keystroke tool.
- The image is a forge upload. The project's pull request guideline ("Screenshots in the PR") asks
  for blobs on an `-assets` side branch linked by raw URL. It renders and is the captured file; only
  the hosting differs.
- `scenarioTableGridPaste` carries `#S2` already on the base, while its case adds a row and a
  column (reads like S1). Pre-existing, outside this CR.
- CONTRIBUTING.md asks a new real-window scenario into `STRESS_SCENARIOS_BY_HOST`; this one is in
  the on-demand list of the same file (as two earlier scenarios), disclosed under "Autonomous
  decisions", and passed the `stress` job by name (run 45794466293).

## Runs and cleanup

Logs of pass 1 in `W/verifier/`: `run-head-single.log`, `run-head-stress20.log`,
`run-head-package.log`, `run-head-clip-setup.log`, `run-head-clip-take.log`,
`run-head-requirements-lint.log`, `run-head-clip-kit-test.log` (`just clip-kit-test`: 56 pass,
0 fail). The pass 1 clip profile (`WT/out/verify-clip`) was removed. Pass 2 ran no product test;
its downloaded copy of the image and body (`W/scratch/pr536-asset`) is removed. Pass 3 ran no
product test; its empty scratch folder (`W/scratch/pr536-pass3`) is removed. `git status
--porcelain --untracked-files=all`: empty. No code, commit or push.
