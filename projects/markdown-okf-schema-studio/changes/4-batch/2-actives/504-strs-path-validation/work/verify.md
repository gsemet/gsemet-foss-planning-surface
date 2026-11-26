# Verify CR-504 (CR-A)

Head: 2f3c629acdec1f49ca94aa0809506dc4e0f93325

Closing description pass at this head (earlier: `work/scratch/verify-2f3c629-1.md` and `-2.md`, NOT VERIFIED on claims G and H; `work/scratch/verify-2f3c629-3.md`, VERIFIED, the note this one replaces). Judged: the posted description of PR 524. No commit changed; no gate rerun. `<W>` is the CR worktree, `<CR>` the CR folder, `V` is `<CR>/work/verifier`.

## Verdict: VERIFIED

No claim fails.

## Judged now (at 2f3c629a)

Posted body and file. `gh pr view 524 --json ...` into `V/pr524-final.json`, then `python -I V/finalcmp.py <CR> 522725ef` (`V/pr524.json`: the posted body the third pass judged):
- `posted-now == file-now: True`, 401 lines each; `verified-posted == file at 522725ef : True`; title unchanged.
- The diff from the verified body is five lines, all in Test plan: 381, 382, 386, 388 change `[ ]` to `[x]` only; 390 `- [ ] Verified: pending at 2f3c629` to `- [x] Verified at 2f3c629`. Nothing else differs.
- `username hits 0`, `home path hits 0`, `images 0`, `stale 0 UNVERIFIED 0`, fold open 1 close 1, no BOM, no internal reference before "Internal references".
- `gh api repos/gsemet/markdown-okf-schema-studio/pulls/524` (`body_html`): `h2 12 tables 3 details 1 img 0 checkboxes 8 checked 8`.
- PR: `OPEN`, `isDraft True`, head `2f3c629a`, base `main` `17b779d5`, `MERGEABLE`, `CLEAN`. `git ls-remote`: branch `2f3c629a`, main `17b779d5`. `git rev-parse HEAD` = `2f3c629a`; `git status --short --branch`: clean, level with its upstream.

Test plan, item by item:

1. Line 381, new or changed tests fail on the previous code: holds, proved now. `python -I V/oldcode.py <W> <CR>/work/scratch/vf 17b779d5 2f3c629a` (head's compiled tests in a scratch copy, then the same with the base's `scripts/check-marker-companions.mjs`, `marker-baseline.json`, `mutation/report-pure.mjs` and viewer `home.ts`, `layout.ts`, `mainPaths.ts`, `model.ts`, `pages.ts`, `viewer.css`):
   - HEAD-CODE: `checkMarkers 14/14`, `mutationReport 7/7`, `model 8/8`, `home 7/7`, `pages 16/16`, `write 6/6`, `mainPaths 3/3` pass, `fail 0`.
   - BASE-CODE, pass/fail: `checkMarkers 6/8`, `mutationReport 6/1`, `model 1/7`, `home 4/3`, `pages 9/7`, `write 5/1`, `mainPaths 2/1`.
   - `python -I V/changedtests.py <W> 17b779d5 2f3c629a` lists the test cases with changed code lines: 8 in checkMarkers, 1 in mutationReport, 5 in model, 3 in home, 4 in pages, 1 in write, 1 in mainPaths. Each of the 23 is among the BASE-CODE `not ok` names. (An earlier run without the `yaml` package in the scratch copy failed all of checkMarkers on both sides; the copy was removed and the run repeated.)
2. Line 382, requirements updated or added, markers, `just requirements-update`: holds.
   - `git diff --numstat 17b779d5 2f3c629a` on the files: CORE-069 `48 6`, CORE-080 `38 6`, CORE-082 `29 8`, CORE-097 `108 0`; CORE-097 is the one added SwRS file (`--diff-filter=A`).
   - `git grep -n -E "@(implements|tests)_req ..." 2f3c629a -- scripts test src`: each of the four has markers in the files named (`model.ts`, `home.ts`, `pages.ts`, `check-marker-companions.mjs`) and in their tests.
   - Generated output current: `okfreq update-coverage requirements --check`: `0 files would change`, exit 0; `okfreq lint requirements --check --prose --check-links --project-root .`: `0 indexes would change`, `0 requirement OKF projections would change`, exit 0 (broken cross-link W2 warnings only); tree clean after.
   - Sub-item for the six from `main`: lines unchanged; carried from the third pass.
3. Line 386, no changelog, no user-facing change: `git diff 17b779d5 2f3c629a -- CHANGELOG.md docs/releases-notes src package.json skills`: 0 lines.
4. Line 387, local gates (ticked before, unchanged): carried from the first pass (head unchanged): `<CR>/work/gates/verify-check-2f3c629.log` and `verify-static-rest-2f3c629.log`, below.
5. Line 388, evidence: viewer unit tests pass (item 1, HEAD-CODE); `V/evidence/before-after.md` line 5: "After: pushed head `2f3c629a...`", with its before and after images present; the item says the screenshots are not posted, and `images 0`. No `src/` change (item 3). Impacts line 368 gives "No visual change in the extension" with the reason.
6. Line 389, `Review: approved at 2f3c629`: `chantier log CR-504`: `r9 approved at 8d72801e..., committed as 2f3c629a...`.
7. Line 390, `Verified at 2f3c629`: `chantier log CR-504`: `2026-11-26T01:37:06Z driver verdict result=VERIFIED head=2f3c629a...`, and this pass.
8. Line 391, CI green: `gh pr checks 524` (exit 0): `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual` pass; `gallery`, `integration`, `pages`, `release`, `release-check`, `toc-loop`, `stress`, `tag-release` skipping.

## Carried from the third pass (2f3c629a: head unchanged, lines untouched)

- G (line 54, which fragments arrive in which commit) and H (line 85, the five commits that fail the marker check and the new coverage mode): hold.
- Lines 28, 349, 385 (the SwRS `main` added or extended, with DIAG-009 and DIAG-128; scenario ids, order and markers only): hold.
- `ls <CR>/work/coder`: `r1.md` to `r9.md` (line 395).

## Carried from the first pass (2f3c629a: head unchanged)

Gates (run by the first pass; `chantier.yaml` has no long gate):
- `<CR>/work/gates/verify-check-2f3c629.log`, first line `CR-504 verifier: just check at 2f3c629acdec1f49ca94aa0809506dc4e0f93325 2026-11-26T01:51:02+01:00`; `just check` ends `exit=0`: `check-markers: 11 companion file(s), 459 in-force SwRS marked, 13 files on the marker baseline`; node tests `35/35 pass`, `5317 tests, 5310 pass, 0 fail, 7 skipped`, `107/107 pass`; pytest `206 passed`; `1228 requirements, 0 errors, 26 warnings`; `main paths: 96 StRS checked, 625 SwRS citations, all valid`; `use case diagrams: 94 StRS checked, all parse`.
- `<CR>/work/gates/verify-static-rest-2f3c629.log`, first line `CR-504 verifier: ci-static parts other than check at 2f3c629acdec1f49ca94aa0809506dc4e0f93325 2026-11-26T02:00:03+01:00`: `check-no-merge-commits: passed (7 commits since origin/main)`, `merge exit=0`, `fmt exit=0`, `found 0 vulnerabilities`, `audit exit=0`, sphinx `4 passed`, `sphinx exit=0`, `report exit=0`.

Failures of the verdict at `afbb55c`:
- A. StRS marker sort fixed as claimed: `git grep -n -E "@(tests_req|accepts_req) StRS-" 2f3c629a -- test` (via `V/table.py`): 26 lines in 16 files, 19 `@accepts_req` on 17 paths, 7 `@tests_req` on 6 paths; all 26 tests read against their path (`V/paths.py`) meet the strict rule; the examples named as removed carry no marker; the audit's wider reading is disclosed as not delivered.
- B. `V/table.py <W> <CR>/work/pr-body.md e5ee7ec1 2f3c629a`: `187 rows, 0 bad`; partial path 111, single-state snapshot 27, SwRS duplicate 12, other 11, real VS Code 19, simulated 7.
- C. `V/lists.py <W> <CR>`: the body's lists equal the computed ones (722 scenarios, 133 paths); the 66 candidate paths are correct.
- D. Disclosed: `V/pairs.py <W> 17b779d5 2f3c629a`: the SwRS that lost their last `test/integration` marker are the 12 named; none lost all test markers.
- E. Disclosed (3 of 16 sampled, three lines named, still carrying those fragments).
- F. Fixed: CORE-097 states the `implements-fragment` rule (S7); `test/build/checkMarkers.test.ts` marks `CORE-097#S7`; 8 tests cover S1 to S7 and pass in the check log.

Claims that hold:
1. Head and PR: title `build: declare StRS paths and SwRS scenarios on okf-schema 0.18`.
2. Declarations (`V/scan.py <W> 2f3c629a`): 1228 requirements; live StRS 95 all declare; live SwRS 461, the 459 non-exempt all declare; declaration problems 0; approved SwRS none; retired without exemption 0; markers tests 5599, accepts 19, implements 1531; all violation counts 0; 16 groups.
3. Figures (same script): 722 of 2633 scenarios and 133 of 156 paths unmarked; 78 of 95 StRS without `@accepts_req`; LIFE-023 four paths with no marker.
4. New-mode figures at `1905009` (`V/newmode.sh`): 0 errors, 104 warnings (W004 x78, W2 x26); same at the head.
5. Committed mode (`uvx --from okf-schema==0.18.1 okfreq validate` on copies of `8560a8b6`, `0796f53c`, `8d72801e`, `2f3c629a`): 0 errors, 26 warnings.
6. Impacts (`V/figures2.py`): main 23 of 95 covered, head 1; 24 with every linked SwRS covered; 6 with a direct `@tests_req`, 1 with both. `git grep` finds only the report recipes, the requirements viewer tests and `buildSite.ts` reading the figure.
7. No `src/` change: `git diff 17b779d5 2f3c629a -- src .github package.json package-lock.json` empty.
8. Configuration and pin: carried from `afbb55c` (`git diff afbb55c 2f3c629a -- pyproject.toml uv.lock requirements/config.yml requirements/tiers/_schema` empty).
9. Requirement text (`V/reqdiff.py <W> 17b779d5 2f3c629a`): only CORE-097 added; 97 retired SwRS newly exempt, none approved; the 15 approved StRS change only `approved_at`, `verified.at`, `scenarios:` and heading ids.
10. Requirements from `main` (`V/textsame.py`, `V/pairs.py`, `V/codediff2.py`): text unchanged apart from ids and order; the 15 removed marker lines and the DIAG-123 line check no declared scenario of the named requirement.
11. Marker rules (`V/ownersteps.py`): untouched copy exit 0; each broken marker gives its rule, exit 1.
12. Split test files lose no assertion; code changes beyond markers are those under Changes (`V/codediff2.py`).
13. Skills and shared guideline refresh: carried from `afbb55c` (`git diff afbb55c 2f3c629a -- .agents/skills requirements/guidelines` empty); glossary, CONTRIBUTING and "Benches" present; both report recipes write the trace.
14. Viewer: sites built from base and head, every image viewed (no user name or home path): head cards 6/156 paths tested, 17/156 accepted, 1/95 StRS covered, 1911/2633 scenarios tested; pairs in `V/evidence/before-after.md`.

## Observations (not counted as failures)

- Line 85: the gallery tests are not what makes the five commits fail. None of the 14 errors or of the failing marker lines names CORE-096, which gets its scenarios and its fragments together in the last commit. The chart and Auto width fragments are the cause; every fact stated holds.
- BLOCK-006 S2 (`test/integration/realInput/flushBeforeNavigate.ts:236`, `:260`): the activation is a synthetic DOM click; the strict rule does not name it; the counts hold either way.
- MYST-016 S2: the shown panel's identity after the click is asserted only by the edit-mode step.
- "Tested by" block of a scenario card has no horizontal padding (named in Known gaps).
