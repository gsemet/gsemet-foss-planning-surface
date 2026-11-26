# Verify CR-504 (CR-A)

Head: 2f3c629acdec1f49ca94aa0809506dc4e0f93325

Verification after moves: previous verdict NOT VERIFIED at `afbb55c5` (copy in `work/scratch/verify-afbb55c.md`), then rounds 6 and 7 (`afbb55c..1905009`), a restack from base `4a47151e` onto `origin/main` `17b779d502b9633fd42dd275986067397db5c4aa` with rounds 8 and 9 (`1905009..2f3c629`). Claims are judged at `2f3c629a` unless marked `carried`. `<W>` is the CR worktree, `<CR>` the CR folder, `V` is `<CR>/work/verifier`. Probes ran on `git archive` copies under `<CR>/work/scratch`, removed at the end.

## Verdict: NOT VERIFIED

One claim of the PR body is false (G below). The six failures of the verdict at `afbb55c` (A to F) are fixed or disclosed.

## Gates (run by this Verifier; `chantier.yaml` has no long gate)

- `<CR>/work/gates/verify-check-2f3c629.log`, first line `CR-504 verifier: just check at 2f3c629acdec1f49ca94aa0809506dc4e0f93325 2026-11-26T01:51:02+01:00`; `just check` ends `exit=0`: `check-markers: 11 companion file(s), 459 in-force SwRS marked, 13 files on the marker baseline`; node tests `35/35 pass`, `5317 tests, 5310 pass, 0 fail, 7 skipped`, `107/107 pass`; pytest `206 passed`; `1228 requirements, 0 errors, 26 warnings`; `main paths: 96 StRS checked, 625 SwRS citations, all valid`; `use case diagrams: 94 StRS checked, all parse`.
- `<CR>/work/gates/verify-static-rest-2f3c629.log`, first line `CR-504 verifier: ci-static parts other than check at 2f3c629acdec1f49ca94aa0809506dc4e0f93325 2026-11-26T02:00:03+01:00`: `check-no-merge-commits: passed (7 commits since origin/main)`, `merge exit=0`, `fmt exit=0`, `found 0 vulnerabilities`, `audit exit=0`, sphinx `4 passed`, `sphinx exit=0`, `report exit=0`.
- Worktree clean after both (`git status --short` empty).

## Claim that fails

G. PR body, Autonomous decisions, line 54: "A migration script, run group by group, declared `scenarios:` and renamed the headings; each migration commit carries its markers' fragments." FALSE at `2f3c629a` (introduced by the restack).
- Command: for each commit of `17b779d5..2f3c629a`, `git archive <commit>` into an empty scratch project, then `node <copy>/scripts/check-marker-companions.mjs --root <copy>` (each commit's own script).
- Output: `8560a8b6` exit 0; `0796f53c`, `919fc171`, `5748d0a0`, `5a86c95f`, `8d72801e` exit 1 with 54 `fragment-required` lines each (for example `test/page/runtimePageControls.test.ts:591: fragment-required: @tests_req SwRS-MDOKFSTUDIO-LAYOUT-023 (... declares scenarios:; name the one this marker checks with #S<n>)`); `2f3c629a` exit 0.
- New-mode validation per commit (`sh V/newmode.sh <W> <scratch> <commits>`, okfreq 0.18.1, mode switched): errors `8560a8b6` 0, `0796f53c` 14, `919fc171` 14, `5748d0a0` 14, `5a86c95f` 14, `8d72801e` 14, `2f3c629a` 0; the errors are "has no scenario fragment" on the chart, gallery and Auto width tests of `main`.
- Cause: the migration commits declare the scenarios of the requirements `main` added or extended, and the fragments of their tests arrive only in the last commit. Spec "Commit order" asks `just check` and the new-mode validation to pass on each commit; the repository merges by rebase (`release-process.guidelines.md`), so the five commits would land on `main`.
- No Known gap names it.
- Narrower true wording (a Known gap would cover it, body only): "The migration commits carry the fragments of the markers that existed before the restack on `main`; the fragments of the chart, gallery and Auto width tests of `main` arrive in the last commit, so `0796f53c` to `8d72801e` fail the marker check (`just check`, 54 `fragment-required`) and the new-mode validation (14 errors)." The other fix moves those fragments into the commits that declare the scenarios (new head).

## Failures of the verdict at afbb55c, judged at 2f3c629a

A. StRS marker sort: fixed as claimed (body: "a marker stays only where the test walks the whole declared path", strict rule under Autonomous decisions, candidates under Known gaps).
- `git grep -n -E "@(tests_req|accepts_req) StRS-" 2f3c629a -- test` (via `V/table.py`): 26 lines in 16 files; 19 `@accepts_req` lines on 17 distinct paths, 7 `@tests_req` lines on 6 paths, as the body says ("26 ... 23 of 156 ... 17 accepted, 6 tested").
- All 26 tests read against their declared path (`V/paths.py <W> 2f3c629a <ids>`) and the strict rule: each meets it. Two limit cases are under Observations.
- Examples named as removed (CODE-004 S1, MYST-007 S1, TABLE-015 S1, TABLE-001 S1, LIFE-014 S1, TRUST-004 S1, BLOCK-011 S2, MYST-009 S1, DIAG-001 S2): `git grep` shows no marker on them; table rows read "partial path / marker removed". Spot checks: `check_code_copy` fakes the host answer (`answer_code_copy`), `serializer.test.ts` restores through `deserializePreviewPanelForTests`, the reload suite asserts no reading position, the Start writing scenario walks the Enter option.
- The audit's wider reading of "walks" (spec D9, Q7, Q28) is not what was delivered; the body says so (strict rule; "even where it exercises most of the path"). Disclosed.

B. Classification table: fixed. `V/table.py <W> <CR>/work/pr-body.md e5ee7ec1 2f3c629a`: `187 rows, 0 bad`; partial path 111, single-state snapshot 27, SwRS duplicate 12, other 11, walks in real VS Code 19, walks on the simulated bench 7; 185 base lines in 62 files, 26 head lines in 16 files, no marker without a row. The commit `e5ee7ec1` the body names is outside the head's history, and the body says it predates the restack; `gh api .../commits/e5ee7ec1` resolves it.

C. Uncovered list: fixed. `V/lists.py <W> <CR>`: the body's lists equal the computed ones (722 scenarios, 133 paths); the list of 66 candidate paths is correct.

D. 136 dropped marker blocks: disclosed (Known gaps, and the decision to leave it under Autonomous decisions). `V/pairs.py <W> 17b779d5 2f3c629a`: the SwRS that lost their last `test/integration` marker are exactly the 12 the body names; no SwRS lost all test markers.

E. Wrong fragments: disclosed (Known gaps: 3 of 16 sampled, three lines named; unread fragments named). The three lines read at head still carry those fragments.

F. `implements-fragment` in the marker-check SwRS: fixed. CORE-097 (the former CORE-096 of this CR) states the rule in its normative text and scenario S7; `test/build/checkMarkers.test.ts` has a test marked `CORE-097#S7`; its 8 tests cover S1 to S7 and passed in the check log.

## Claims that hold

1. Head and PR. `git rev-parse HEAD`, `git ls-remote origin <branch> main`: head `2f3c629a`, main `17b779d5` (the merge base). `gh pr view 524`: `OPEN`, `isDraft true`, same head, title `build: declare StRS paths and SwRS scenarios on okf-schema 0.18`.
2. CI. `gh pr checks 524`: `static`, `static-windows`, `viewer-graph`, `visual`, `report`, `checks` pass; `integration`, `stress`, `release-check`, `toc-loop`, `gallery`, `pages`, `release`, `tag-release` skipping.
3. "Local gates: `just check`, `just requirements-lint` and `just preflight` (static stage on Windows) pass at `2f3c629`": the two logs under Gates cover every part of `ci-static` and `check` (which includes `requirements-lint`).
4. "Review: approved at `2f3c629`". `$CHANTIER log CR-504`: `r9 approved at 8d72801eacd0e5b7217f8987b23632edc8b18837, committed as 2f3c629acdec1f49ca94aa0809506dc4e0f93325`.
5. Declarations. `V/scan.py <W> 2f3c629a`: 1228 requirements; live StRS 95, all declare; live SwRS 461, the 459 non-exempt all declare (exempt TRUST-070, TRUST-075); declaration problems 0; approved SwRS none; retired without exemption 0; marker lines tests 5599, accepts 19, implements 1531; all eight violation counts 0; 16 groups.
6. Figures. Same script: 722 of 2633 scenarios unmarked; 133 of 156 paths unmarked; 78 of 95 StRS without `@accepts_req`; LIFE-023 four paths with no marker; BLOCK-027, TRUST-012, TRUST-014 paths exist (no marker).
7. New-mode validation figures ("measured ... at `1905009`: 0 errors and 104 warnings: W004 x78, W2 x26"): `V/newmode.sh` at `19050098` gives exactly that; at `2f3c629a` the same figures.
8. Committed mode. `uvx --from okf-schema==0.18.1 okfreq validate` on copies of `8560a8b6`, `0796f53c`, `8d72801e`, `2f3c629a`: 0 errors, 26 warnings.
9. Impacts. Reports generated on copies of `17b779d5` (okf-schema 0.17.0) and the head (0.18.1), `V/figures2.py`: main 95 live, 23 covered, 24 with every linked SwRS covered; head 1 covered, 24, 6 with a direct `@tests_req`, 1 with both; every exempt linked SwRS is reported `missing`. "Only the requirements viewer reads it": `git grep -n -E "requirements-report\.json|REQUIREMENTS_REPORT_PATH|stakeholder_test_coverage" 2f3c629a -- scripts test justfile .github src` finds only the two report recipes, `test/site/requirementsViewer/` and its caller `test/site/buildSite.ts`.
10. No `src/` change: `git diff 17b779d5 2f3c629a -- src .github package.json package-lock.json` is empty.
11. Configuration and pin (`config.yml` markers and `accepted_in_files`, `okf-schema>=0.18.1`, schemas): carried from afbb55c: `git diff afbb55c 2f3c629a -- pyproject.toml uv.lock requirements/config.yml requirements/tiers/_schema` is empty.
12. Approved StRS and requirement text. `V/reqdiff.py <W> 17b779d5 2f3c629a`: only CORE-097 added; 97 retired SwRS newly exempt (92 superseded, 5 deprecated), none approved; the 15 approved StRS change only `approved_at`, `verified.at`, `scenarios:` and heading ids, `approved_by` unchanged.
13. Requirements from `main`. `V/textsame.py <W> 17b779d5 2f3c629a`: DIAG-009, DIAG-128, CORE-096 identical apart from ids; DIAG-121, DIAG-123, LAYOUT-023 hold the same lines with scenarios reordered. The 15 removed marker lines and the DIAG-123 line (`V/pairs.py`, `V/codediff2.py`) are tests that check no declared scenario of the named requirement, as the Known gap says; the DIAG-009 and LAYOUT-023 residues it names are there.
14. "New or changed tests fail on the previous code" (box unticked): carried from afbb55c: the branch's own change to the check script, `checkMarkers.test.ts`, `scripts/mutation` and `test/site` differs between the old and new base only by requirement ids and the new markers on tests of `main` (`diff` of the two `git diff` outputs); old results: check tests on the base script 6 pass, 8 fail; viewer tests on base code 21 pass, 19 fail.
15. Marker rules (owner steps 5 and 6 and others). `V/ownersteps.py <W> <copy of 2f3c629a>`: untouched copy exit 0; one broken marker at a time gives `accepts-placement`, `fragment-required`, `fragment-undeclared`, `accepts-on-swrs`, `strs-tests-in-integration`, exit 1.
16. Split test files lose no assertion; code changes beyond markers are those under Changes (`V/codediff2.py`).
17. Skills and shared guideline refresh: carried from afbb55c: `git diff afbb55c 2f3c629a -- .agents/skills requirements/guidelines` is empty. Glossary terms, CONTRIBUTING text and "Benches" section present at head (`git diff 17b779d5 2f3c629a -- .agents/glossary/common.md CONTRIBUTING.md`; `grep` of `project.guidelines.md:173 ## Benches`). Both report recipes write the trace (`just requirements-report` produced `requirements-trace.json`).
18. Viewer. Sites built from base and head (`V/transpile.cjs`, `V/buildsite.cjs`, `V/shots.cjs`; every image viewed, no user name or home path): base card "23 of 95 StRS with a stakeholder validation test"; head cards 6/156 paths tested, 17/156 accepted, 1/95 StRS covered, 1911/2633 scenarios tested; two area columns; LIFE-023 S1 to S4 "None"; 461 SwRS pages with 722 "missing" marks. Pairs: `V/evidence/before-after.md` (before `17b779d5`, after `2f3c629a`).
19. PR body form. Posted body equals `work/pr-body.md` (400 lines); GitHub `body_html` renders 12 h2, 3 tables (187 + header rows for the classification), one fold; no image, no user name or home path, no internal reference outside "Internal references", no STALE mark.

## Observations (not counted as failures)

- BLOCK-006 S2, link and Back lines (`test/integration/realInput/flushBeforeNavigate.ts:236`, `:260`): the activation is a synthetic DOM click dispatched by `clickWithoutBlur`. The strict rule excludes "an injected page message, a test hook or a faked host result" and does not name a synthetic DOM event; the tab-switch line (`:284`) walks the same path without it, so the counts hold either way.
- MYST-016 S2: the identity of the shown panel after the click is asserted only by the edit-mode step of the walk; read mode asserts the count and the selected tab.
- DIAG-121, DIAG-123 and LAYOUT-023 also have their scenarios reordered; the Test plan says "scenario ids and test markers only".
- "Tested by" block of a scenario card has no horizontal padding (named in Known gaps).
- Body lines to refresh at the next edit: "Verified" and "CI green" boxes still pending; the Evidence line says the comparison was made at `afbb55c` (made again at `2f3c629`); "Internal references" lists `r1.md` to `r8.md` while `r9.md` exists.
