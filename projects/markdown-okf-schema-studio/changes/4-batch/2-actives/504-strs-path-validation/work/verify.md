# Verify CR-504 (CR-A), round 3

Head: 77a8d0749bbc02da7adfc5fbf58dcd037a633063

Worktree `markdown-okf-schema-studio.worktrees/batch-09-CR-504`, clean tree. All claims judged at 77a8d074. Specification base `4a47151e`.

## Verdict: NOT VERIFIED

The marker, schema, fragment, heading, approved-metadata and baseline claims hold. NOT VERIFIED because of two description failures and delivered-versus-specified gaps that the PR's Known gaps never name (details at the end).

## Claims that hold (all at 77a8d074)

1. Requirements lint, old mode. `just requirements-lint` exited 0 (`lint-exit=0`). It reported `0 files would change`, `main paths: 96 StRS checked, 625 SwRS citations, all valid` and `use case diagrams: 94 StRS checked, all parse`.
2. Config and pin.
   - `requirements/config.yml` has `strs_test_coverage_mode: linked-swrs-and-validation-test`, `markers.accepts: '@accepts_req'`, and `accepted_in_files` in `generated_fields`.
   - `pyproject.toml` line 10 is `requirements = ["okf-schema>=0.18.1"]`.
   - `uv.lock` line 638-639 is `name = "okf-schema"`, `version = "0.18.1"`.
3. Scratch new-mode validation. I copied `requirements/` to a scratch folder, set `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`, and gave the scratch folder junctions to `src`, `test`, `scripts`, `sphinx`, `skills` and `docs`. Without them okfreq scans no marker.
   - Command: `okfreq validate <scratch>/requirements --project-root <scratch> --json`.
   - Output: exit 0, 0 errors, 64 warnings (W004 x38, W2 x26), no W003.
   - Check-links was left out because the junctions escape the project root.
   - The first run with `--project-root .` and no junctions gave `1227 requirements, 0 errors, 121 warnings`, W004 x95. That run scanned no marker, so it proves nothing about fragments. The PR body quotes exactly this run (see failure A).
4. Scan of the requirement files (a script of mine, read-only, over `requirements/tiers`).
   - 1227 requirements. 95 live StRS, 458 live non-exempt SwRS, 2 live exempt SwRS. 672 retired.
   - `bad 0`: every live StRS and live non-exempt SwRS declares `scenarios:` whose ids and titles match their `#### Path S<n>:` or `### Scenario S<n>[ (<kind>)]:` headings one for one, with the right shape (keys `id` and `title`, `S[1-9][0-9]*`, unique).
   - `git grep -nE '^#### Path [0-9]' requirements/tiers` finds 0 lines.
   - No `### Scenario:` or `### Scenario (` heading in a live SwRS.
   - TRUST-070 and TRUST-075 have `scenarios: None`.
   - No retired requirement has `scenarios:`, and every retired SwRS has `annotation_exemption: true` and a reason.
   - Note: 458 live non-exempt SwRS against the spec's 457, the extra one being the new SwRS-MDOKFSTUDIO-CORE-096, as D16 allows.
5. Scan of every tracked test and source file (not trace). 5531 `@tests_req` and 62 `@accepts_req` marker lines on known IDs, with these violation counts:
   - `@tests_req StRS` without a fragment: 0.
   - `@tests_req StRS` under `test/integration/`: 0.
   - `@accepts_req` outside `test/integration/` and not on a D7 StRS: 0.
   - `@accepts_req` on a SwRS: 0.
   - Fragmentless marker on a declaring target: 0.
   - Undeclared fragment: 0.
   - Fragment on a target with no `scenarios:`: 0.
6. D5 and approved StRS.
   - `git diff 4a47151e..HEAD` shows 97 added `annotation_exemption: true` lines on SwRS files. None of these SwRS is approved: `git grep -l '^approved_by:' HEAD -- requirements/tiers` returns 17 StRS and 0 SwRS.
   - The 15 listed approved StRS: the diff, once headings, `scenarios:` and `approved_at` lines are filtered out, leaves only `verified.at`, set to the same new time.
   - `approved_at` is `2026-11-25T15:37:43+01:00` on all 15. No `approved_by` line changes anywhere.
   - The other 2 approved StRS (MYST-001, TABLE-012) are superseded and untouched.
7. `scripts/marker-baseline.json`. `strsTestsInIntegration` is `{}`, and `blocks` only shrinks (diff shown above).
8. `just check`: exit 0. It includes `check-markers: 10 companion file(s), 458 in-force SwRS marked, 16 files on the marker baseline` and the 8 new rule tests of `checkMarkers.test.ts`.
9. Each new marker rule has a test that fails on the old script.
   - I ran the compiled `checkMarkers.test.js` from the head against `git show 4a47151e:scripts/check-marker-companions.mjs`, in a scratch folder.
   - Output: `ℹ pass 6`, `ℹ fail 8`. The 8 failures are the rule 4 tests (declared fragment; fragment required or absent; `@implements_req` never has a fragment; two fragments count as one ID), the rule 5 tests (`@accepts_req` placement; never on a SwRS; no StRS `@tests_req` under integration) and the companion-lines test.
10. `just release-tests`: exit 0, `206 passed`. `test_check_main_paths.py` has `#### Path S1: p` cases.
11. Viewer unit tests, `node scripts/node-test.mjs unit "out/test/site/**/*.test.js"`: exit 0, `tests 196`, `pass 195`, `fail 0` (the remaining test is skipped). Included are `a path heading carries its S<n> id, and the older heading has none` and `a scenario heading carries its S<n> id, and the older heading has none`.
12. Uncovered counts in the PR body: my own scan finds 2617 declared SwRS scenarios with 722 unmarked and 156 StRS paths with 94 unmarked. This matches the PR.
13. `requirements/tiers/log.md` has the dated entry for 2026-11-25 (agreements, D5, the marker sort). Verified by `git diff` on the file.
14. Review box: `Review: approved at 77a8d07` is checked in the PR body. I did not read `$CHANTIER log` for it in this pass. Carried as the Driver's claim, not proved here.
15. Not run here: `just preflight`. The PR body claims it. No gate log was read.

## Failures

A. The PR body's new-mode validation line is wrong.
   - It says `{'errors': 0, 'warnings': 121, 'infos': 0}: W004 x95 (a StRS with no @accepts_req yet)`.
   - That is the run that scanned no marker (claim 3). At the head, with the markers scanned, the run gives 0 errors and W004 x38, 64 warnings.
   - The Known gap "95 StRS have no acceptance test (W004)" is then 38.
   - Spec check 3 asks for the summary line of the last commit's run.

B. Delivered against specified, with no Known gap for it. `git diff 4a47151e..HEAD --stat` (excluding `requirements/tiers` and `test`) shows 8 files: CONTRIBUTING.md, pyproject.toml, config.yml, project.guidelines.md, check-marker-companions.mjs, marker-baseline.json, mutation/report-pure.mjs and uv.lock. The following parts of the specification are therefore absent, and the PR's Known gaps do not name them:
   - Section 4 and D12, the viewer: no "StRS paths tested", "paths accepted", "StRS covered" or "SwRS scenarios tested" cards, no "Paths tested" or "Paths accepted" columns, no per-path tested and accepted files on the StRS page, no "missing" mark on the SwRS page, no trace join. `stakeholderValidated` is still in `test/site/requirementsViewer/model.ts` (lines 58 and 377). `git grep "Paths accepted\|requirements-trace" HEAD -- test/site justfile` finds nothing. The PR describes only ids in the viewer.
   - Section 5, justfile: `requirements-report` and `requirements-report-json` do not write `requirements-trace.json`. The justfile is untouched.
   - D13: `.agents/skills/okfreq*` and `requirements/guidelines/requirements.guidelines.md` are not refreshed from v0.18.1.
   - Section 6: `.agents/glossary/common.md` is untouched, and CONTRIBUTING.md changes by 4 lines only (the bench convention is not shown in the diff).
   - Owner scenario steps 1 to 4 of the specification (home cards, area table columns, LIFE-023 use case page with files, SwRS page with "missing") cannot be shown.

The owner or the Foreman can accept B as a deliberate split, but then the Known gaps and the Deliverables must say it, and the spec or CR-B must take it.
