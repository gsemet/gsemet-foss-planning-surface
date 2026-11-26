# Verify CR-504 (CR-A)

Head: 2f3c629acdec1f49ca94aa0809506dc4e0f93325

Third pass at this head (earlier: `work/scratch/verify-2f3c629-1.md`, NOT VERIFIED on claim G; `work/scratch/verify-2f3c629-2.md`, NOT VERIFIED on claim H). No commit changed since; only the posted PR body. `git diff 83d88b2e -- .../work/pr-body.md` in the planning surface (83d88b2e: the body the second pass judged): 4 lines changed, 28, 85, 349 and 385. Judged now: those four lines and posted body = file. Everything else is carried with its pass. No gate rerun. `<W>` is the CR worktree, `<CR>` the CR folder, `V` is `<CR>/work/verifier`.

## Verdict: VERIFIED

No claim fails.

## Judged now (at 2f3c629a)

H. Line 85, Known gaps, reworded: "The five commits from `0796f53c` to `8d72801e` fail the marker check (`just check`, 54 `fragment-required`) and the validation in the new coverage mode (14 errors), because the fragments of the chart, gallery and Auto width tests of `main` arrive in the last commit. The first commit and the head pass both. A merge by rebase puts these commits on `main`; a squash merge does not." Holds.
- `git log --format="%h %p %s" 17b779d5..HEAD`: seven commits, `8560a8b6` first, then `0796f53c`, `919fc171`, `5748d0a0`, `5a86c95f`, `8d72801e`, `2f3c629a`.
- Marker check: `python -I V/percommit.py <W> <CR>/work/scratch/vg 17b779d5 4a47151e 8560a8b6 0796f53c 919fc171 5748d0a0 5a86c95f 8d72801e 2f3c629a`: `8560a8b6 check exit 0 failing lines 0`; each of the five `check exit 1 failing lines 54 {'fragment-required': 54}`; `2f3c629a check exit 0`; `failing commits 5 identical sets True`; `origin of the failing lines {'from main after old base': 64}`.
- New mode: `sh V/newmode.sh <W> <CR>/work/scratch/vg 8560a8b6 0796f53c 919fc171 5748d0a0 5a86c95f 8d72801e 2f3c629a` (okfreq 0.18.1, mode switched in the copy): `8560a8b6` `errors 0`; the five `validate exit 1`, `errors 14`; `2f3c629a` `errors 0`. The 14 errors of `8d72801e` all say `has no scenario fragment` (`chartCsp`, `chartError`, `chartTooltip`, `chartViewCache`, `exportSnapshot`, `findIndex`, `vegaChart`, `liveChart`, `codeBlockBreakout`, `runtimePageControls`).
- Gallery: `git grep -c -E "SwRS-MDOKFSTUDIO-CORE-096#S"`: no output at `8d72801e` (exit 1); at `2f3c629a` `test/site/gallery.test.ts:4`, `test/site/galleryLinks.browser.test.ts:3`. Its fragments arrive in the last commit, as the sentence says (see Observations).
- Merge sentence: the five are ancestors of the head and not of `main` (the log above), so a rebase merge replays them onto `main` and a squash merge does not.

Lines 28, 349, 385 (DIAG-009 and DIAG-128 added to the lists). Hold.
- `python -I V/mainreqs.py <W> 4a47151e 17b779d5 2f3c629a`. Main since the old base: description, text or both changed in SwRS DIAG-009, DIAG-121, DIAG-123, DIAG-128, LAYOUT-023, and CORE-096 added. Its other changes: DIAG-124 `implemented_in_files` only (`body changed False`), three StRS with link or path citation text. So the list names the SwRS `main` added or extended.
- Same script, `17b779d5` to `2f3c629a`, the six: front matter changed only in `scenarios` (all six) and `tested_in_files` (DIAG-009, DIAG-123, LAYOUT-023); `title` and `description` unchanged; `same non-empty lines True` for all six; scenario headings all numbered (7, 4, 6, 2, 8, 5). DIAG-009, DIAG-128, CORE-096 `body identical apart from ids True`; DIAG-121 and DIAG-123 differ in block order only (`same heading blocks True`); LAYOUT-023 differs in order and one added blank line before a table. So "numbered scenarios", "scenario and normative text is unchanged" and "scenario ids, scenario order and test markers only" hold.
- Same script: `test marker lines of the six at head: 116 without #S: 0`. DIAG-128 on `main` (`git grep ... 17b779d5`): 7 markers with no fragment.

Posted body = file, and form: `gh pr view 524 --json ...` into `V/pr524.json`, then `python -I V/bodycmp.py <CR>`: `posted lines 401 local lines 401`, no diff line; `username hits 0`; no home path; `images 0`; `stale 0 UNVERIFIED 0`; fold open 1, close 1; no internal reference printed before "Internal references". API `body_html`: `h2 12 tables 3 details 1 img 0`. PR: head `2f3c629a`, `isDraft true`, `OPEN`, base `main`. `git rev-parse HEAD` = `2f3c629a`; `git status --short --branch`: clean, level with its upstream; `git ls-remote`: branch `2f3c629a`, main `17b779d5`.

CI (line 391): `gh pr checks 524`: `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual` pass; `gallery`, `integration`, `pages`, `release`, `release-check`, `toc-loop`, `stress`, `tag-release` skipping.

Lines 389, 390: `Review: approved at 2f3c629` (log: `r9 approved at 8d72801e..., committed as 2f3c629a...`, carried from the second pass, head unchanged); `Verified: pending at 2f3c629` is expected before this verdict.

## Carried from the second pass (2f3c629a: head unchanged, lines untouched)

- G. Line 54: "The migration commits carry the fragments of the markers that existed before the restack on `main`; the fragments of the chart, gallery and Auto width tests of `main` arrive only in the last commit": holds (`V/percommit.py`, run again above with the same result; `git merge-base 19050098 17b779d5` = `4a47151e`).
- Line 388 (browser comparison at `2f3c629`): `V/evidence/before-after.md`: "After: pushed head `2f3c629a...`", all pairs captured again after the restack and rounds 6 to 9.
- Line 395: `ls <CR>/work/coder`: `r1.md` to `r9.md`.

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
2. "Local gates ... pass at `2f3c629`": the two logs above.
3. Declarations (`V/scan.py <W> 2f3c629a`): 1228 requirements; live StRS 95 all declare; live SwRS 461, the 459 non-exempt all declare; declaration problems 0; approved SwRS none; retired without exemption 0; markers tests 5599, accepts 19, implements 1531; all violation counts 0; 16 groups.
4. Figures (same script): 722 of 2633 scenarios and 133 of 156 paths unmarked; 78 of 95 StRS without `@accepts_req`; LIFE-023 four paths with no marker.
5. New-mode figures at `1905009` (`V/newmode.sh`): 0 errors, 104 warnings (W004 x78, W2 x26); same at the head.
6. Committed mode (`uvx --from okf-schema==0.18.1 okfreq validate` on copies of `8560a8b6`, `0796f53c`, `8d72801e`, `2f3c629a`): 0 errors, 26 warnings.
7. Impacts (`V/figures2.py`): main 23 of 95 covered, head 1; 24 with every linked SwRS covered; 6 with a direct `@tests_req`, 1 with both. `git grep` finds only the report recipes, the requirements viewer tests and `buildSite.ts` reading the figure.
8. No `src/` change: `git diff 17b779d5 2f3c629a -- src .github package.json package-lock.json` empty.
9. Configuration and pin: carried from `afbb55c` (`git diff afbb55c 2f3c629a -- pyproject.toml uv.lock requirements/config.yml requirements/tiers/_schema` empty).
10. Requirement text (`V/reqdiff.py <W> 17b779d5 2f3c629a`): only CORE-097 added; 97 retired SwRS newly exempt, none approved; the 15 approved StRS change only `approved_at`, `verified.at`, `scenarios:` and heading ids.
11. Requirements from `main` (`V/textsame.py`, `V/pairs.py`, `V/codediff2.py`): text unchanged apart from ids and order; the 15 removed marker lines and the DIAG-123 line check no declared scenario of the named requirement.
12. "New or changed tests fail on the previous code" (box unticked): carried from `afbb55c` (old results: check tests on the base script 6 pass, 8 fail; viewer tests on base code 21 pass, 19 fail).
13. Marker rules (`V/ownersteps.py`): untouched copy exit 0; each broken marker gives its rule, exit 1.
14. Split test files lose no assertion; code changes beyond markers are those under Changes (`V/codediff2.py`).
15. Skills and shared guideline refresh: carried from `afbb55c` (`git diff afbb55c 2f3c629a -- .agents/skills requirements/guidelines` empty); glossary, CONTRIBUTING and "Benches" present; both report recipes write the trace.
16. Viewer: sites built from base and head, every image viewed (no user name or home path): head cards 6/156 paths tested, 17/156 accepted, 1/95 StRS covered, 1911/2633 scenarios tested; pairs in `V/evidence/before-after.md`.

## Observations (not counted as failures)

- Line 85: the gallery tests are not what makes the five commits fail. None of the 14 errors or of the failing marker lines names CORE-096, which gets its scenarios and its fragments together in the last commit. The chart and Auto width fragments are the cause; every fact stated holds. "chart and Auto width tests" would be tighter at a later body edit.
- BLOCK-006 S2 (`test/integration/realInput/flushBeforeNavigate.ts:236`, `:260`): the activation is a synthetic DOM click; the strict rule does not name it; the counts hold either way.
- MYST-016 S2: the shown panel's identity after the click is asserted only by the edit-mode step.
- "Tested by" block of a scenario card has no horizontal padding (named in Known gaps).
