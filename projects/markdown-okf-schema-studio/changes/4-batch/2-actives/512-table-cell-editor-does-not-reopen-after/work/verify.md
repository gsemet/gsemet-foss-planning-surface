# CR-512 verification

Head: e76c084313d826eeab7148418658c4394c5a33f2

Verdict: **VERIFIED**. First verification. Draft pull request
https://github.com/gsemet/markdown-okf-schema-studio/pull/536, base
`chantier/batch-09/cr-509-reliable-heavy-ci-split-the-trusted-laun`
(`89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4`). Outcome reached: 2c, "cannot reproduce" (treated as 2b).

`WT` is the CR worktree, `W` the CR's `work/` folder. All claims are judged at `e76c084` unless a
line says `carried from <sha7>`. Commands ran from `WT` (Git Bash).

## State

- `git rev-parse HEAD` = `e76c084313d826eeab7148418658c4394c5a33f2`; `git status --porcelain
  --untracked-files=all` empty (checked again after my runs and cleanup).
- `git ls-remote origin`: cr-512 branch = `e76c084...`, cr-509 branch = `89cae5ff...`.
- `gh pr view 536`: head `e76c084...`, base the cr-509 branch, draft, OPEN, updated 10:16:48Z.
- `git diff --stat 89cae5ff HEAD`: 8 files, +122/-11 (clip.md, scenario.mjs, feature clip
  guideline, requirements log, SwRS TABLE-120, realInput/run.ts, realInput/tableGridPaste.ts,
  test/shared/stressPlan.ts). One commit, `e76c0843`.

## Specification claims

| # | Claim | Result | Proof at `e76c084` |
| --- | --- | --- | --- |
| S1 | Second real-window scenario with the clip's stage document inlined, `stage/tasks.tsv` on the clipboard, click on header cell "Task", Ctrl/Cmd+V through `press()`, no Ctrl+A | proven | `test/integration/realInput/tableGridPaste.ts` lines 81-147: `CHECKLIST_DOCUMENT`, `TASKS_TSV`, `clipboard.writeText(TASKS_TSV)`, `th` /^Task$/ click, `waitForEditor`, `press(page, modifier+v)` |
| S2 | Checks: source equals the clip's `EXPECTED`; `waitFor("the editor open in the header cell Task")`; the open editor is in the header cell of column 0 and shows "Task" | proven | lines 136-157: `assert.equal(clip.EXPECTED, PASTED_CHECKLIST)`, buffer === `PASTED_CHECKLIST`, open editors == `[{rows:5,tag:"TH",row:0,column:0,text:"Task"}]`, asserted again after `waitForPageSettled` |
| S3 | Name `scenarioTableGridPasteFromHeader`, `@tests_req ...TABLE-120#S3`, run from the "table-grid-paste" entry and the full trusted run next to `scenarioTableGridPaste` | proven | tableGridPaste.ts lines 131-133; `run.ts` lines 242-245 and 312-316. SwRS S3 is "Start in the header row" |
| S4 | Guards read the shipped files (stage document, stage clipboard text, `EXPECTED`); a mismatch fails the test | proven | lines 134-137 read `stage/release-checklist.md`, `stage/tasks.tsv`, import `scenario.mjs`; my runs pass at head; mismatch case: `W/run9-r2-mismatch.log` `AssertionError` ("Dev, Fri" against "Dev, Thu"), carried from b5aaf68 plus the then uncommitted test, whose file was last edited before that run and is the committed one |
| S5 | Passes locally in a real window with `STUDIO_REAL_INPUT_SCENARIO=table-grid-paste` | proven (own run) | `env STUDIO_REAL_INPUT_SCENARIO=table-grid-paste fnm exec -- npm run test:integration -- --trusted-only`: exit 0, VS Code 1.148.0, `STEP done: real-input (6442 ms)` (`W/verifier/run-head-single.log`). Process list before: no other test or clip VS Code instance |
| S6 | Passes in CI's real-window jobs | proven | `gh run view`: 45794447911 and 45794466293, `workflow_dispatch`, headSha `e76c084`, success. Both integration logs: `STEP done: real-input` (408016 ms; 450553 ms) and `ci-integration: passed` (`W/ci-45794447911-integration.log`, `W/verifier/ci-45794466293-integration.log`) |
| N1 | Narrowing runs, one difference at a time (copy in VS Code, auto-save 200 ms, clip timing), then all together; each recorded | proven | `W/runs.md` runs 2-6 and logs `W/run2..6-*.log`: each `STEP done: real-input`; paste types `["text/plain"]` (runs 2, 4, 5) and with `copymetadata`, `vscode-editor-data` (runs 3, 6). Carried from 8df99ce: temporary variants, product code identical (P1) |
| N2 | Clip run twice (current keys and `CLIP_KEY_COMMANDS=1`), `cellEditorOpenAfterPaste` recorded per take | proven | `W/take1..take5/verify.json`: all `passed: true`, `cellEditorOpenAfterPaste: true`, `cellEditorOpen: false`. Carried from 8df99ce: takes 1-4 with a temporary trace record, take 5 on the round 1 script; `git diff da61cefe e76c084 -- .../scenario.mjs` changes comment lines only. Own take at head: see matrix (b) |
| N3 | Record in `work/`, summarized in the pull request body | proven | `W/runs.md`; the body's Deliverables table |
| C1 | 2c: scenario committed; guideline sentence in "1. The kit and a take" says the miss did not reproduce and names the commit | proven | diff of `feature-clip-process.guidelines.md`: sentence next to the drive functions, "did not reproduce in runs on a branch whose product code (`src/`, `sphinx/`) is identical to that of commit `3478f09`" |
| C2 | Clip comment and `clip.md` note drop "may or may not"; the take waits for the state it films; Done click kept when the editor is open | proven | `git grep -n -i "may or may" HEAD -- docs requirements test`: exit 1; diff of `scenario.mjs`: bounded wait until 4.4 s, record `cellEditorOpenAfterPaste`, Done click only if open; `clip.md` Shot row and note updated |
| R1 | TABLE-120 verification notes name the new scenario; behaviour unchanged; `req_lifecycle: proposed` (no re-approval) | proven | SwRS diff: one line, under "Verification notes"; frontmatter line 13 `req_lifecycle: proposed` |
| R2 | `requirements-update` done and dated `log.md` entry naming the outcome | proven | `log.md` 2026-11-26 entry "... did not reproduce (CR-512)", "Outcome: cannot reproduce". `fnm exec -- just requirements-lint`: exit 0, "1228 requirements, 0 errors, 26 warnings", "0 indexes would change", "0 requirement OKF projections would change", "0 files would change" (`W/verifier/run-head-requirements-lint.log`) |
| R3 | Writing skill not touched | proven | `git diff --name-only 89cae5ff HEAD -- src sphinx skills CHANGELOG.md docs/releases-notes package.json`: empty |
| O1 | No re-filming or re-rendering of the clip outputs | proven | `git diff --stat 89cae5ff HEAD -- .../paste-spreadsheet-cells/frames .../stage`: empty; the 8 changed files hold no media |
| O2 | Grid paste and other reopen paths unchanged | proven | same empty diff over `src` and `sphinx` |
| O3 | No OS-level keystroke tool | proven | `package.json` unchanged (empty diff); the scenario imports `press` from `./harness` |
| E1 | `just check` and `just preflight` pass (Windows: static stage) | cited | `W/gate-push-check.log`, `W/gate-push-preflight.log`: first line `head e76c084313d826eeab7148418658c4394c5a33f2`, last `exit 0 head e76c...`; preflight: "ci-static: passed", the other stages skipped on Windows. No gate is named in chantier.yaml, none run by me |
| P1 | The product code of all earlier runs is the head's | proven | empty: `git diff --name-only 8df99ce1 3478f099 -- src sphinx`, `git diff --name-only 3478f099 HEAD -- src sphinx`; `git merge-base --is-ancestor 3478f099 origin/main`: true |

## Host and default matrix

| Cell | Result | Rests on |
| --- | --- | --- |
| (a) auto-save off, header-row start: editor reopens on "Task" | proven | Own runs at head: single (S5) and `env STUDIO_REAL_INPUT_SCENARIO=stress STUDIO_STRESS_SCENARIOS=table-grid-paste-header STUDIO_STRESS_REPEAT=20 fnm exec -- npm run test:integration -- --trusted-only`: exit 0, PASS 1/20 to 20/20, "stress: 20 round(s) passed" (`W/verifier/run-head-stress20.log`). CI: two integration jobs (S6) and run 45794466293 stress, 11/11, "ci-stress: passed (11 rounds)" (`W/ci-45794466293-stress.log`). Auto-save off: no `files.autoSave` setting in `test/integration` or `package.json` (VS Code's shipped default) |
| (b) auto-save `afterDelay` 200 ms, header-row start: same | proven | Own clip take at head (VSIX from `just package` at head; `just clip paste-spreadsheet-cells setup`, `take`, both exit 0; VS Code 1.148.0, not the pinned 1.147.0): profile `files.autoSave: afterDelay`, delay 200; `verify.json` passed, file on disk equals the expected table, `cellEditorOpenAfterPaste: true`; frame at 4.26 s shows the editor in header cell "Task" (`W/verifier/evidence/after-autosave200-header-editor-open-4.26s.jpg`, `W/verifier/head-clip-take-verify.json`). Plus runs 4 and 6 and takes 1-5, carried from 8df99ce (P1). No committed test guards this cell; the body says so in "Known gaps" |
| (c) auto-save off, body-cell start: `scenarioTableGridPaste` stays green | proven | Body unchanged in the diff. Own single run at head runs it first (`run.ts` 242-245), exit 0; CI integration jobs (S6) |

## Pull request body (re-read with `gh pr view 536`, copy in `W/pr-body.md`)

| Claim | Result | Proof |
| --- | --- | --- |
| Summary: editor stayed closed in 3 of 3 first attempts | proven | CR-489 `work/r1.md` lines 7-16 ("Reproduced 3 times") |
| Summary: reopened in every run; no product code change | proven | rows above; run 9's failure is the intended text mismatch, before any paste; R3 |
| Table rows 1-5 (narrowing runs, counts) | proven | runs 1-6, carried from 8df99ce (N1, P1) |
| "committed test ... pass (2 runs)" | proven | `W/run10-r2-single.log` (6351 ms, committed test file) and my S5 run at head |
| "repeated in one window, 20 of 20, in each of 2 runs" | proven | `W/run11-r2-stress20-header.log` and my stress run at head, both "20 round(s) passed" |
| Clip, both key ways, 5 of 5 takes | proven | N2 |
| CI Linux: pass (2 runs); alone 11 of 11 | proven | S6, matrix (a); both jobs `runs-on: ubuntu-latest` |
| Diagram (paste, fill, one save, editor open; the new scenario checks fill and reopen) | proven | S2; one save is the requirement's behaviour, product code unchanged, and the diagram claims no new check of it |
| Changes: six bullets match the diff; nothing delivered is left out | consistent | the 8 files; `log.md` is covered by the requirement update |
| Impacts: "No visual change" with reason | proven | R3, O1; `W/verifier/evidence/before-after.md` |
| Blast radius, Grade 1 | consistent | tests, docs and one clip script only |
| New test also passes on the previous code | proven | product code equal on base and head (R3), shipped files it reads (`stage/`, `EXPECTED`) unchanged, passes at head |
| Requirements: notes, marker, update and lint, 0 errors | proven | R1, R2, S3 |
| Changelog: no user-facing change | proven | R3 |
| Local gates at `e76c084` | proven | E1 |
| Review: approved at `e76c084` | proven | `$CHANTIER log CR-512`, 09:34:25Z: "r2 approved at b5aaf684..., committed as e76c084313d8..."; the 8 files were last edited before the 09:32Z approval note; runs 10, 11 followed the last edit |
| "Verified" box | open, as it must be before this verdict | |
| CI green at `e76c084`; visual passed on its second run, first cut at 15 min after its checks passed | proven | `gh pr checks 536` all pass or skipped; run 45794366914 attempt 2 success; attempt 1 `visual` cancelled 09:41:54Z-09:57:04Z, `timeout-minutes: 15`, `W/ci-45794366914-visual.log` lines 1520-1521 "ci-visual: passed" then "The operation was canceled."; the two heavy runs (S6) |
| Autonomous: stress step on demand, one more default step leaves too little margin | proven | `STRESS_ON_DEMAND_SCENARIOS`; 21 default scenarios x 11 rounds: expected 944760 ms, with 22: 988320 ms, above the 960000 ms two-thirds limit of `test/build/hangWatchdog.test.ts` |
| Autonomous: take waits up to 4.4 s | proven | C2 |
| Gap: cause not established | consistent | `W/runs.md`, "The earlier miss" |
| Gap: late Done click about 0.3 s after 4.4 s; outputs not re-rendered | proven | `scenario.mjs`: wait to 4.4 s, then a 0.3 s pointer move; O1 |
| Gap: takes made before the last edits, none repeated | true when the body was written | file times and take logs; my take at head came after the body's last update |
| Gap: no committed check for the 200 ms auto-save case | proven | no `files.autoSave` in `test/integration`; the clip only records the state (no throw on it) |
| Gap: page received no HTML after the `.tsv` copy | proven | runs 3 and 6 paste types hold no `text/html` |
| Format: no images; internal references only in their last section before the Claude Code line; template sections present | consistent | `.agents/guidelines/pull-request.guidelines.md`, `.github/PULL_REQUEST_TEMPLATE.md` |

## Notes (none changes the verdict)

- The body's "pass (2 runs)" and "20 of 20, in each of 2 runs": the coder's runs 7 and 8 (round 1)
  ran the test before the `EXPECTED` comparison and a marker fragment were added (same page actions
  and assertions). The counts hold for the committed test through runs 10 and 11 plus my two runs.
- The Driver may now say that one clip take was made at `e76c084` (mine, editor open after the
  paste), which updates the gap "no take was repeated after them". "That case was run once" counts
  the isolated auto-save run (4); run 6 and the takes also ran under that setting.
- `scenarioTableGridPaste` carries `#S2` already on the base, while its case adds a row and a
  column (reads like S1). Pre-existing, outside this CR.
- CONTRIBUTING.md asks a new real-window scenario into `STRESS_SCENARIOS_BY_HOST`; this one is in
  the on-demand list of the same file (as two earlier scenarios), disclosed under "Autonomous
  decisions", and passed the `stress` job by name (run 45794466293).

## Own runs and cleanup

Logs in `W/verifier/`: `run-head-single.log`, `run-head-stress20.log`, `run-head-package.log`,
`run-head-clip-setup.log`, `run-head-clip-take.log`, `run-head-requirements-lint.log`,
`run-head-clip-kit-test.log` (`just clip-kit-test`: 56 pass, 0 fail). My clip profile
(`WT/out/verify-clip`) is removed; no process of my runs remains. No code, commit or push.
