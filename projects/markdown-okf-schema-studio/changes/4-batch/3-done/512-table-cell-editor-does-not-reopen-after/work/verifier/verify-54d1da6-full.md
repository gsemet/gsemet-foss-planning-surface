# CR-512 verification after the restack

Head: 54d1da6268e9a4fbe059c6cdb8b1160d94b4b558

Verdict: **VERIFIED** at `54d1da6`, base `chantier/batch-09/cr-505-strs-acceptance-tests-acceptance-job-and`
(`9d7e788a479dec70fd882d295bf0d5e78f4f6b98`). Draft pull request
https://github.com/gsemet/markdown-okf-schema-studio/pull/536. Outcome unchanged: 2c, "cannot
reproduce" (treated as 2b).

One thing is left for after this verdict: the posted description (equal to `W/pr-body.md`) still
names `e76c084` on its three SHA table rows and its Test plan lines. The rewrite is listed in
"Description" below; the edited body needs its own description pass before it counts as judged.

The earlier note (head `e76c084`, three passes) is kept whole in `W/verifier/verify-e76c084.md`.
"Carried" rows rest on it.

`WT` is the CR worktree, `W` the CR's `work/` folder, `S` = `W/scratch/artifacts-54d1da6` (CI job
logs, local only). Commands ran from `WT` or with `git -C WT`.

## State and move

| Claim | Proof at `54d1da6` |
| --- | --- |
| Head, remote and PR agree; base is the CR-505 branch; draft, open | `git rev-parse HEAD` = `54d1da62...`; `git ls-remote origin`: cr-512 `54d1da6268e9...`, cr-505 `9d7e788a479d...`; `gh pr view 536`: same head and base, `isDraft: true`, `OPEN` |
| Worktree clean, before and after the runs | `git status --porcelain --untracked-files=all`: empty both times |
| One commit on the base | `git log -1 --format=%H%n%P` : `54d1da62...`, parent `9d7e788a...`, subject "test: cover the editor reopening after a header-cell paste" |
| The patch is the same but for log context | `git range-diff 89cae5ff..e76c0843 9d7e788a..54d1da62`: one pair, `!`, the only difference is the context line under the CR-512 entry in `requirements/tiers/log.md` |
| Conflict resolution keeps both sides | `git diff 9d7e788a 54d1da62 -- requirements/tiers/log.md`: six added lines (the CR-512 entry) under `## 2026-11-26`, nothing removed, CR-505 entries follow; `git grep -n -E "^(<<<<<<<\|>>>>>>>\|=======)" HEAD -- requirements/tiers/log.md`: no match |
| What the base brought | `git log --oneline 89cae5ff..9d7e788a`: 3 commits, 120 files. Touches what some proofs run: `test/integration/run-tests.ts` (argument parsing, spawned window), `justfile`, `package.json` (one added script, `test:acceptance`), `.github/workflows/ci.yml` (acceptance job), requirements and their guideline |
| What the base did not bring | `git diff --stat e76c0843 54d1da62 -- test/integration/realInput docs/demo-video test/shared/stressPlan.ts test/build/hangWatchdog.test.ts requirements/tiers/swrs/table-editing src sphinx skills CHANGELOG.md docs/releases-notes package-lock.json .vscodeignore scripts/node-test.mjs`: empty |

## Specification claims

| # | Claim | Judgment | Proof |
| --- | --- | --- | --- |
| S1-S3 | New scenario: clip's document and clipboard, header-cell start, no Ctrl+A, its checks, name, marker `#S3`, run from both entries | proven, carried from e76c084 | `tableGridPaste.ts` and `run.ts` are identical at both heads (empty diff above). At head, `git grep` : `run.ts` 242-245 and 314-316 run `scenarioTableGridPaste` then `scenarioTableGridPasteFromHeader`; line 116 the stress name |
| S4 | The test reads the shipped clip files; a mismatch fails it | proven, carried from e76c084 | test, stage files and `scenario.mjs` identical (empty diff); the guards pass in the runs at head below; mismatch case `W/run9-r2-mismatch.log` |
| S5 | Passes locally in a real window | proven, judged at 54d1da6 (the runner changed) | `env STUDIO_REAL_INPUT_SCENARIO=table-grid-paste fnm exec -- npm run test:integration -- --trusted-only`: exit 0, "Validated version: 1.148.0", `STEP done: real-input (6572 ms)` (`W/verifier/run-54d1da6-single.log`); `out/reports/e2e/integration-manifest.json` of that run: `passed`, revision `54d1da62...`, `dirty: false`. Process check before the runs: no VS Code test window running (one `npm run test:clip-kit` node process, which opens none) |
| S6 | Passes in CI's real-window jobs | proven, judged at 54d1da6 | `gh run view` 45811051488 and 45811056179: `workflow_dispatch`, headSha `54d1da62...`, conclusion success; integration, acceptance (trust-security), stress, visual, report, checks success. Integration job logs: checkout `54d1da6268e9...`, `STEP done: real-input` (424559 ms; 420828 ms), `ci-integration: passed` (`S/run-45811051488-integration.log`, `S/run-45811056179-integration.log`). Skipped in both: release-check, toc-loop, tag-release, release, pages |
| N1 | Narrowing runs, one difference at a time then together | proven, carried from 8df99ce through e76c084 | observations made with temporary variants; the product code they exercised is unchanged (P1), as are the clip stage and the real-input harness. The base's runner change parses arguments and spawns the other windows; it changes nothing in the window these runs observed |
| N2 | Clip run both ways, `cellEditorOpenAfterPaste` recorded | proven, carried from 8df99ce and e76c084 | `W/take1..5/verify.json`; clip kit, scenario and product code unchanged |
| N3 | Record in `W/`, summarized in the PR body | proven, carried from e76c084 | `W/runs.md`; posted body unchanged, its table read at head |
| C1 | 2c: scenario committed; guideline sentence names the commit | proven, carried from e76c084 | guideline identical (empty diff over `docs/demo-video`); `git merge-base --is-ancestor 3478f099 origin/main`: exit 0 |
| C2 | "may or may not" gone; the take waits; Done click kept | proven, judged at 54d1da6 | `git grep -n -i "may or may" HEAD -- docs requirements test`: no match; clip files identical |
| R1 | TABLE-120 verification notes name the scenario; `proposed` | proven, carried from e76c084 | empty diff over `requirements/tiers/swrs/table-editing` |
| R2 | Requirements update and lint; dated log entry | proven, judged at 54d1da6 | `fnm exec -- just requirements-lint`: exit 0, "1228 requirements, 0 errors, 26 warnings", "0 indexes would change", "0 requirement OKF projections would change", "0 files would change" (`W/verifier/run-54d1da6-requirements-lint.log`); the log entry: see the conflict row |
| R3, O2 | No writing skill, product, changelog or package change by the CR | proven, judged at 54d1da6 | `git diff --name-only 9d7e788a 54d1da62 -- src sphinx skills CHANGELOG.md docs/releases-notes package.json`: empty |
| O1, O3 | Clip outputs not re-rendered; no OS keystroke tool | proven, judged at 54d1da6 | `git diff --stat 9d7e788a 54d1da62`: the same 8 text files, 122 insertions, 11 deletions; none is media, `package.json` not among them |
| E1 | `just check` and `just preflight` pass (Windows: static stage) | proven, judged at 54d1da6 | Logs made by others, not rerun here: `W/conflict-resolver/restack-54d1da62-just-check.log` (5366 unit, 5359 pass, 0 fail, 7 skipped; security 116; clip kit 56; release 254; 0 requirement errors; ends on the last check passing; `conflicts.md`: exit 0) and `W/gates/preflight-54d1da62.log` (ends "ci-static: passed", other stages skipped on Windows; "7 commits since origin/main", the count `git log origin/main..54d1da62` gives; Driver note 11:38:12Z: exit 0, tree clean). These two logs carry no SHA line. Same stage bound to the SHA: static-windows job of run 45811051488, checkout `54d1da6268e9...`, "254 passed", "1228 requirements, 0 errors", "ci-static: passed" (`S/run-45811051488-static-windows.log`) |
| P1 | Product code of every run is the head's | proven, judged at 54d1da6 | empty: `git diff --name-only 3478f099 54d1da62 -- src sphinx`, `git diff --name-only 3478f099 origin/main -- src sphinx` |

## Host and default matrix

| Cell | Judgment | Proof |
| --- | --- | --- |
| (a) auto-save off, header-row start | proven, judged at 54d1da6 | single run (S5); `env STUDIO_REAL_INPUT_SCENARIO=stress STUDIO_STRESS_SCENARIOS=table-grid-paste-header STUDIO_STRESS_REPEAT=20 fnm exec -- npm run test:integration -- --trusted-only`: exit 0, PASS 1/20 to 20/20, "stress: 20 round(s) passed" (`W/verifier/run-54d1da6-stress20.log`). CI run 45811056179 stress job 139878757934: `STUDIO_STRESS_SCENARIOS: table-grid-paste-header`, PASS 1/11 to 11/11, "ci-stress: passed (11 rounds)" (`S/run-45811056179-stress.log`). `git grep -n autoSave HEAD -- test package.json`: one unit test line only (`diagReq.settings`), so the real windows run with auto-save off |
| (b) auto-save `afterDelay` 200 ms, header-row start | proven, carried from e76c084 | the clip take (`W/verifier/head-clip-take-verify.json`, image in `W/verifier/evidence/`) runs the packaged product, the clip kit, the scenario and its stage: all unchanged (empty diff above). The `justfile` hunks of the base do not touch `package` or `clip` (they change `release-tests`, `ci-acceptance`, `ci-report`, `preflight`), `package.json` gains only `test:acceptance`, the lock file is unchanged, and the clip kit imports nothing from `test/` or `scripts/`. No committed check guards this cell (Known gaps) |
| (c) auto-save off, body-cell start | proven, judged at 54d1da6 | single run at head runs `scenarioTableGridPaste` first (S5); both CI integration jobs (S6) |

## Description (posted body at 54d1da6)

Read with `gh pr view 536 --json body` and `gh api .../pulls/536` (`full+json`, `body_html`), PR
updated 11:28:12Z.

| Check | Result | Proof at `54d1da6` |
| --- | --- | --- |
| Posted body is the source file | proven | `diff --strip-trailing-cr -B <posted> W/pr-body.md`: no output |
| Renders | proven | `body_html`: nine `<h2>` Summary to Internal references, the table (header and 11 rows), the mermaid section with its source, seven checked task boxes |
| No image, so none shows a username or home folder; internal references only last | proven | search of the posted body for the username, drive and home paths, `CR-<n>`, `UNVERIFIED`, `STALE`, image syntax: only the two lines of "Internal references" |
| Matches the delivery | proven | R3, O1, range-diff: the Changes bullets describe the same patch |

### Every proof of the body: judged again or carried

| Body part | Judgment | Reason | How the line should read |
| --- | --- | --- | --- |
| Summary, history (3 of 3 closed) | carried from e76c084 | a past observation | unchanged |
| Summary, reopened in every run, no product change | judged at 54d1da6 | S5, matrix, R3 | unchanged |
| Deliverables intro (product code identical to `3478f09`) | judged at 54d1da6 | P1 | unchanged |
| Rows "plain text", "copy", "auto-save", "timing", "together" | carried from 8df99ce through e76c084 | N1 | unchanged (no SHA in the row) |
| Row "committed test (after the body-cell test)", 2 runs | judged at 54d1da6 | passes again at head (S5); the 2 runs counted are the earlier ones, still true | unchanged |
| Row "repeated in one window", 20 of 20 in 2 runs | judged at 54d1da6 | 20 of 20 again at head; the 2 runs counted are the earlier ones | unchanged |
| Row "clip itself, both ways", 5 of 5 | carried from 8df99ce through e76c084 | N2 | unchanged |
| Row "clip filmed again", 1 take | carried from e76c084 | matrix (b) | "The clip filmed again at `54d1da6` (carried from `e76c084`), on VS Code 1.148.0 (the clip pins 1.147.0)", yes (1 take) |
| Row "CI real-window suite", 2 runs | judged at 54d1da6 | S6 | "at `54d1da6`", pass (2 runs) |
| Row "repeated alone in CI", 11 of 11 | judged at 54d1da6 | matrix (a) | "at `54d1da6`", pass, 11 of 11 |
| Diagram | carried from e76c084 | test and product unchanged | unchanged |
| Changes (six bullets) | judged at 54d1da6 | range-diff and diff stat | unchanged |
| Impacts, "No visual change" | judged at 54d1da6 | R3, O1 | unchanged |
| Blast radius, grade 1 | carried from e76c084 | same patch | unchanged |
| Test plan: new test also passes on the previous code | judged at 54d1da6 | product code equal on `9d7e788` and head, the shipped files the test reads unchanged, passes at head | "at `54d1da6`" |
| Test plan: requirements | judged at 54d1da6 | R2 (`--check` modes show an update would change nothing) | "at `54d1da6`" |
| Test plan: changelog | judged at 54d1da6 | R3 | unchanged |
| Test plan: local gates | judged at 54d1da6 | E1 | "at `54d1da6`" |
| Test plan: review | judged at 54d1da6 | `$CHANTIER log CR-512`, 11:31:02Z: "move e76c084..54d1da6 (restack) inspector approved at 54d1da6268e9..." | "Review: approved at `54d1da6`" |
| Test plan: verified | this verdict | | "Verified at `54d1da6`" |
| Test plan: CI green | judged at 54d1da6 | `gh run view 45810700393`: attempt 1, headSha `54d1da62...`, static, static-windows, visual (14m16s), viewer-graph, report, checks success; real VS Code jobs skipped there (not counted green), run by hand in 45811051488 and 45811056179, both success | "at `54d1da6`: the pull request checks, and two manually started runs that include the real VS Code jobs". The sentence on the visual job's second run belongs to `e76c084` only: drop it |
| Autonomous: stress step on demand | judged at 54d1da6 | `CONTRIBUTING.md` line 528 still asks for it; `stressPlan.ts` and `hangWatchdog.test.ts` unchanged (line 326: 21 scenarios 944760 ms, 22 would be 988320 ms, limit 960000 ms); CI at head runs 21 default scenarios | unchanged |
| Autonomous: take waits up to 4.4 s | carried from e76c084 | clip script unchanged | unchanged |
| Known gap: cause not established | carried from e76c084 | no new trace of the first attempts | unchanged |
| Known gap: late Done click, outputs not re-rendered | carried from e76c084 | `scenario.mjs` unchanged; O1 | unchanged |
| Known gap: no committed check for 200 ms auto-save | judged at 54d1da6 | the base's new tests add no auto-save setting (matrix (a)) | unchanged |
| Known gap: clip notes still mention HTML | judged at 54d1da6 | `clip.md` line 80 at head | unchanged |
| Known gaps complete | judged at 54d1da6 | no `UNVERIFIED` mark, no failed claim, no uncaptured pair owed; the move adds none | unchanged |

## Notes (none changes the verdict)

- The notes of `W/verifier/verify-e76c084.md` ("Notes") still apply, except the one on the forge
  image, removed since.
- The visual job took 14m16s (PR run) and about 14m38s (run 45811051488) against the 15-minute limit
  recorded in the earlier body.

## Runs and cleanup

New logs in `W/verifier/`: `run-54d1da6-single.log`, `run-54d1da6-stress20.log`,
`run-54d1da6-requirements-lint.log`. The local runs downloaded VS Code 1.148.0 into the worktree's
`.vscode-test` (ignored). No VS Code process of this worktree left. CI job logs read with
`gh api .../actions/jobs/<id>/logs` are in `S`; the temporary copy of the posted body is removed.
No CI run dispatched or re-run. No code, commit or push.
