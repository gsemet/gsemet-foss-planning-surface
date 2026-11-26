# Verify CR-504 (CR-A)

Head: 2c0a01a3ec265c60514533044f2405e393c9283d

Third, closing pass at the same head, on the description as posted on PR 524. Earlier passes at this head: `work/scratch/verify-2c0a01a-1.md` (full, NOT VERIFIED on two body lines) and `work/scratch/verify-2c0a01a-2.md` (VERIFIED on the fixed local file, then not posted). `<W>` is the CR worktree, `<CR>` the CR folder, `V` is `<CR>/work/verifier`, `S` is `<CR>/work/scratch`.

## Verdict: VERIFIED

## Judged in this pass, at 2c0a01a

P1. Head, tree, PR. `git -C <W> rev-parse HEAD`: `2c0a01a3ec265c60514533044f2405e393c9283d`; `git -C <W> status --porcelain=v1 -b`: only the branch line, level with upstream. `gh pr view 524 --json ...`: `OPEN`, `isDraft true`, head `2c0a01a3...`, base the CR-500 branch at `c7c6a562...`, `mergeStateStatus CLEAN`, title `build: declare StRS paths and SwRS scenarios on okf-schema 0.18`. `git ls-remote`: CR branch `2c0a01a3`, base branch `c7c6a562`, main `17b779d5`. VERIFIED.

P2. The posted description is the file. `gh api repos/gsemet/markdown-okf-schema-studio/pulls/524 > S/posted-2c0a01a-3.json`, then `python -I S/pass3_check.py`: `api head 2c0a01a3... draft True state open`; `posted chars 49504 bytes 49507 file bytes 49507`; `equal True`; `posted CR chars 0`. (`gh pr view 524 --json body -q .body > S/posted-2c0a01a-3.md` differs from `work/pr-body.md` by one empty last line only, the newline that `-q` appends.) VERIFIED.

P3. Only line 391 changed since the second pass. `git -c core.autocrlf=false diff --no-index --word-diff=plain S/pr-body-2c0a01a-2.md pr-body.md` (in `<CR>/work`): one hunk, line 391, `[-[ ]-]{+[x]+} Verified at [-the head-]{+`2c0a01a`+}`; no other line. VERIFIED.

P4. Line 391, "Verified at `2c0a01a`", ticked. `chantier log CR-504`: `2026-11-26T05:34:41Z driver verdict result=VERIFIED head=2c0a01a3ec265c60514533044f2405e393c9283d base=c7c6a562...`; the earlier verdict at this head (05:30:33Z, NOT VERIFIED) is superseded by it; no later verdict before this pass. The body was posted after it (`05:35:05Z note=closing: body posted at 2c0a01a`; PR `updatedAt 05:35:01Z`). Form as pr-template line 202, ``Verified at `<sha7>` ``. VERIFIED.

P5. Test plan boxes of the posted text (`pass3_check.py`: lines 382, 383, 387 to 392, all `[x]`; forge-rendered HTML: `rendered checkboxes 8 checked 8`).
- 382 (new or changed tests), 383 to 386 (requirements), 387 (changelog), 389 (evidence): text unchanged since the second pass; carried below (claims C, 10, 11 and the 2f3c629a list). VERIFIED.
- 388, local gates at `2c0a01a`: `work/gates/preflight-2c0a01a.log` line 1 `CR-504 ... 2c0a01a3ec265c60514533044f2405e393c9283d just preflight`, line 5579 `pass 5318`, 5580 `fail 0`, 5836 `ci-static: passed`, 5838 `preflight exit=0 head=2c0a01a3...`. VERIFIED.
- 390, review approved at `2c0a01a`: `chantier log CR-504`: `04:35:54Z driver note note=r10 approved at 94f070d798df8da00f08ceb097886631f28fa8e2, committed as 2c0a01a3ec265c60514533044f2405e393c9283d`. VERIFIED.
- 392, CI green at `2c0a01a`: `gh pr checks 524` exit 0: `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual` pass; `gallery`, `pages`, `release`, `tag-release`, `integration`, `release-check`, `stress`, `toc-loop` skipping. `gh run view 45757241066`: `headSha 2c0a01a3...`, `event pull_request`, `completed`, `success`. VERIFIED.

P6. The posted text is clean and renders. `pass3_check.py` on the posted body: SHAs `17b779d`, `2c0a01a`, `7a80c64c`, `94f070d7`, `b93e855a`, `bd910ce3`, `d083eff4` are ancestors of the head, `2f3c629` is not and stands on line 389 only, after `carried from`; no hit for the user name, a home folder path, `STALE`, `UNVERIFIED` or an image; no CR, batch, work path or role name before "Internal references"; `<details>` one opened (line 95), one closed (line 399). Forge HTML (`Accept: application/vnd.github.html+json`, `.body_html`): 12 `h2`, 2 `h3`, 1 `details` with its `summary`, 3 tables, 113 list items, 0 images, no raw heading, table or fence left in the text; Changes, Human decisions, Impacts, Test plan and Internal references inside the fold. VERIFIED.

## Carried from the second pass at this head (2c0a01a)

Reason for all: same head, same base `c7c6a562`, and the only body line changed since is 391, judged above. The text below is the second pass's own note (also in `work/scratch/verify-2c0a01a-2.md`); in it, "this pass", "not posted yet" and "Line 391 is unchecked on purpose" speak of that pass.

### Judged in the second pass

A. Head, tree, PR. `git rev-parse HEAD`: `2c0a01a3ec265c60514533044f2405e393c9283d`; `git status --short --branch`: clean, level with upstream. `gh pr view 524`: `OPEN`, `isDraft true`, head `2c0a01a3`, base CR-500 branch at `c7c6a562`, `CLEAN`, title `build: declare StRS paths and SwRS scenarios on okf-schema 0.18`. VERIFIED.

B. What differs from the posted (older) body. `gh pr view 524 --json body -q .body` into a scratch file, then `git diff --no-index --word-diff=plain` against `work/pr-body.md`: changed lines 43, 54 (added), 55, 56, 78, 86, 100, 388 to 392, 396, and one trailing line removed. Besides the four lines edited since the first pass (43, 56, 86, 389), these are the lines the first pass quoted or judged.

C. Line 389, Evidence (was F1): "... compared in a browser, before at `17b779d`, after at `2c0a01a` (carried from `2f3c629`); screenshots not posted". VERIFIED.
- Form: pr-template, `before at <sha7>, after at <sha7>`, a carried proof as `at <head7> (carried from <sha7>)`.
- `git merge-base --is-ancestor <sha> 2c0a01a3`: `17b779d` ancestor; `2f3c629` not an ancestor, and it stands only after `carried from`.
- `V/evidence/before-after.md`: before `17b779d502b9...`, after `2f3c629acdec...`; 0 images in the body.
- Carry reason: `git diff --name-status 2f3c629a 2c0a01a3 -- src test requirements scripts justfile package.json pyproject.toml uv.lock`: only `requirements/tiers/log.md`, `scripts/check-no-merge-commits.sh`, `test/build/test_no_merge_commits.py`, `test/site/siteClips.test.ts`. `git diff --stat 2f3c629a 2c0a01a3 -- src test/site/requirementsViewer justfile requirements/tiers/strs requirements/tiers/swrs scripts requirements/config.yml pyproject.toml uv.lock test/shared`: only `check-no-merge-commits.sh`. Requirement markers added or removed in the move: nine `@tests_req SwRS-MDOKFSTUDIO-CORE-095#S1`, none on a requirement of the screenshots (LIFE-023, CODE-004, CORE-082, PALETTE-001); the head's figures (1911 of 2633 scenarios tested, claim 5) equal the after capture's.
- Before against the PR base: `git diff --stat 17b779d5 c7c6a562 -- test/site/requirementsViewer requirements`: no output.
- "checked by its unit tests": `package.json` `test:unit` includes `out/test/{...,site}/**/*.test.js`; `work/gates/preflight-2c0a01a.log`: `tests 5326, pass 5318, fail 0`, `preflight exit=0 head=2c0a01a3...`.
- "no visual change in the extension": claim 11 (`src` unchanged).

D. Line 43 (was F2): "Measured at `2c0a01a`: ... 0 errors and 104 warnings: W004 x78 ... W2 x26". `2c0a01a` is the head; the first pass's claim 7 measured at `2c0a01a3`, on a scratch copy of bundle and sources in mode `linked-swrs-and-acceptance-paths` with okf-schema 0.18.1: 0 errors / 104 warnings (W004 x78, W2 x26). Same head, same figures. VERIFIED.

E. Line 86, commits (with line 55's "arrive only in `94f070d7`"). `git log c7c6a562..2c0a01a3`: eight commits, `7a80c64c`, `bd910ce3`, `b93e855a`, `3b134d7b`, `31a632d9`, `d083eff4`, `94f070d7`, `2c0a01a3`, all ancestors of the head; `bd910ce3` to `94f070d7` are six, `b93e855a` to `d083eff4` four. Against claim 7's table (below): `bd910ce3` 54 findings and 14 errors; the four 63 (54 + 9 clip page markers) and 15 errors; `94f070d7` 9 and 1 error; `7a80c64c` and the head pass the marker check with 0 errors in the new mode. Every figure of the line matches. VERIFIED.

F. Line 56: "The scenario fragment of each migrated SwRS test marker was first chosen by a keyword match ...": the wording the first pass's observation gave as exact; the nine round-10 markers are no longer covered by it. The counts on the line are carried (see "Carried from 2f3c629a"). `S/ovr.txt`, read, holds only `acc:` (StRS path) overrides. VERIFIED.

G. Test plan boxes, lines 388, 390, 392. 388: gate log first line `CR-504 ... 2c0a01a3ec265c60514533044f2405e393c9283d just preflight`, last `preflight exit=0 head=2c0a01a3...`. 390: `chantier log CR-504`: `r10 approved at 94f070d798df8da00f08ceb097886631f28fa8e2, committed as 2c0a01a3ec265c60514533044f2405e393c9283d`. 392: `gh pr checks 524` exit 0: `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual` pass, the others skipping (run 45757241066). Line 391 is unchecked on purpose. VERIFIED.

H. SHAs and cleanliness of the whole file. `rg -o "\b[0-9a-f]{7,40}\b" work/pr-body.md`: `2c0a01a`, `94f070d7`, `bd910ce3`, `b93e855a`, `d083eff4`, `7a80c64c`, `17b779d` (all ancestors of the head) and `2f3c629` (after `carried from` only). Search for the user name, home folder paths, `STALE`, `UNVERIFIED`, images, `Measured before`, `1905009`: no hit; one `<details>` opened (line 95) and closed (line 399). `file`: UTF-8, first bytes `23 23 20` (no BOM), 0 CR characters. No failed claim was accepted rather than fixed, so Known gaps needs no bullet for F1 or F2. VERIFIED.

### Carried by it from the first pass at this head (2c0a01a)

Reason for all: same head, same base `c7c6a562`, and the body lines they judge are not among the four edited since (for claim 7, the figures are what lines 43 and 86 now state). Their commands and outputs, as judged then:

1. Head, tree, PR: as A; `git ls-remote`: branch `2c0a01a3`, base branch `c7c6a562`, main `17b779d5`. VERIFIED.
2. Move. `git range-diff` of `17b779d5..2f3c629a` against `c7c6a562..2c0a01a3`: all `=` except `b93e855a` `!` (hunk context in `siteClips.test.ts` only) and the new `2c0a01a3`. `git diff --name-only` of both own diffs: the same 1293 files. `2c0a01a` changes 2 files: `requirements/tiers/log.md` (+4, under `## 2026-11-26`) and nine `#S1` in `test/site/siteClips.test.ts`. VERIFIED.
3. Local gates. Gate log `work/gates/preflight-2c0a01a.log`: `check-markers: 11 companion file(s), 459 in-force SwRS marked, 13 files on the marker baseline`; unit `5326 tests, 5318 pass, 0 fail, 8 skipped`; security `107/107`; pytest `213 passed`; `1228 requirements, 0 errors, 26 warnings`; main paths `96 StRS checked, 625 SwRS citations`; `94 StRS` diagrams parse; sphinx `4 passed`; `0 vulnerabilities`; `ci-static: passed`. It runs `just check` and `just requirements-lint`. No long gate in `chantier.yaml`. VERIFIED.
5. Figures and lists (lines 71-73, 87-89, 99-291). `V/scan.py <W> 2c0a01a3`: 1228 requirements; live StRS 95 all declare; live SwRS 461, 459 non-exempt all declare; exempt TRUST-070 and TRUST-075; declaration problems 0; markers tests 5608, accepts 19, implements 1531; all violation counts 0; scenarios 722 of 2633 unmarked; paths 133 of 156 unmarked; 78 StRS without `@accepts_req`; 17 paths accepted, 6 tested; LIFE-023 four paths unmarked. `V/lists10.py <W> <CR>`: both lists equal the computed ones; 66 candidate paths all unmarked. `V/table.py <W> work/pr-body.md e5ee7ec1 2c0a01a3`: `187 rows, 0 bad`; `S/r9_check_body.py`: 26 kept lines in 16 files, 0 bad line numbers. VERIFIED.
6. Impacts figures (lines 371-378). `V/figures10.py` on okfreq 0.18.1 reports of main, base and head: main and base `covered 23` of 95; head `covered 1`, linked all covered 24, direct `@tests_req` 6, both MYST-018; exempt linked SwRS all `missing`. VERIFIED.
7. Commits and the new-mode figures. For each commit, `git archive` into a scratch copy, that commit's own `scripts/check-marker-companions.mjs --root <copy>`, then the copy's mode set to `linked-swrs-and-acceptance-paths` and `uvx --from okf-schema==0.18.1 okfreq validate <copy>/requirements --check-links --project-root <copy> --json`:

   | Commit | Marker check | New mode errors / warnings |
   | --- | --- | --- |
   | `7a80c64c` | pass | 0 / 216 |
   | `bd910ce3` | 54 `fragment-required` (0 siteClips) | 14 / 163 |
   | `b93e855a`, `3b134d7b`, `31a632d9` | 63 (54 + 9 siteClips) | 15 / 64 |
   | `d083eff4` | 63 | 15 / 104 |
   | `94f070d7` | 9 (siteClips) | 1 / 104 |
   | `2c0a01a3` | pass | 0 / 104 (W004 x78, W2 x26) |

8. Lines 54 and 78, `test/site/siteClips.test.ts` against CORE-095 S1 to S4, read at the head. The base adds 9 tests, marked `#S1` here; each asserts the video source and the clip files. Seven other tests carry a fragment they do not check (lines 17, 27, 34, 40, 54, 71, 279); the GIF with no WebM (line 34, S2) is marked S3, S4. VERIFIED.
9. Line 78, sampled lines re-read: `mathRenderer.test.ts:52` MYST-024 `#S8`, `alertSourceLines.test.ts:150` GFM-009 `#S10`, `lineEndingSave.test.ts:40` BLOCK-234 `#S3` still check another scenario. VERIFIED.
10. Requirements current and text (lines 39, 383-385). `okfreq update-coverage requirements --check`: `0 files would change`; `okfreq lint requirements --check --prose --check-links --project-root .`: `0 indexes would change`, `0 requirement OKF projections would change`; exit 0, tree clean. `V/reqdiff.py <W> c7c6a562 2c0a01a3`: only CORE-097 added; 97 retired SwRS newly exempt, none approved; the 15 approved StRS change only `approved_at`, `verified`, `scenarios`, same approver; other body differences beyond heading ids are on `proposed` requirements. `git diff --numstat c7c6a562 2c0a01a3`: CORE-069 `48 6`, CORE-080 `38 6`, CORE-082 `29 8`, CORE-097 `108 0`. `git grep -E "@(implements|tests)_req SwRS-MDOKFSTUDIO-CORE-(069|080|082|097)" 2c0a01a3 -- scripts test src` shows markers in `model.ts`, `home.ts`, `pages.ts`, `model.test.ts`, `home.test.ts`, `pages.test.ts`, `write.test.ts` (also `bundle.test.ts`), `check-marker-companions.mjs` and `checkMarkers.test.ts`. VERIFIED.
11. Changelog and no user-facing change (lines 369, 387). `git diff c7c6a562 2c0a01a3 -- CHANGELOG.md docs/releases-notes src package.json package-lock.json skills .github`: 0 lines. VERIFIED.
12. Configuration (line 43's mode names, Changes). `requirements/config.yml`: mode `linked-swrs-and-validation-test`, `accepts: '@accepts_req'`; `pyproject.toml` `okf-schema>=0.18.1`; `uv.lock` 0.18.1; `scripts/marker-baseline.json` `strsTestsInIntegration`: `{}` (line 57). VERIFIED.
13. Internal references (lines 396-397). `work/coder/r1.md` to `r9.md`, `work/r10.md`, `evidence/` exist. The CR-505 spec covers every declared scenario, every live path's acceptance test, the 136 dropped blocks, the wrong fragments and the mode switch. VERIFIED.
14. Rendering and wording. No internal reference before "Internal references", no chantier role name as the doer; local Markdown render: 12 `h2`, 2 `h3`, 3 tables, no stray pipe paragraph. The edits since change text inside existing lines only. VERIFIED.

(Claim 4 of the first pass, the Review and CI boxes, is judged again under G.)

### Carried by it from 2f3c629a

Reason for all: the own file list is identical, the range-diff shows no patch change but the context noted in claim 2, and `git diff --stat 2f3c629a 2c0a01a3` over the marker script and baseline, mutation report, viewer, `test/shared`, `justfile`, `pyproject.toml`, `uv.lock`, `config.yml`, schemas, `.agents/skills`, `requirements/guidelines`, CONTRIBUTING and the StRS and SwRS tiers shows only one glossary line brought by the base.

- carried from 2f3c629: line 382, new or changed tests fail on the previous code (`V/oldcode.py`; the 23 changed cases are among the base-code failures). The old files are the same on `c7c6a562` as on `17b779d5`.
- carried from 2f3c629: line 386, the six requirements from `main` (ids, order and markers only), and line 80 (15 removed marker lines, DIAG-123).
- carried from 2f3c629: line 79 (12 SwRS), lines 81-82 and 92-93 (requirement and test files unchanged).
- carried from 2f3c629: marker rules (`V/ownersteps.py`), split test files lose no assertion, viewer behaviour and card figures of the before/after, skills and guideline refresh, exemption reasons, Human decisions, Summary, Deliverables and Changes against the diff (the two files of `2c0a01a` are covered by Changes).
- carried from 2f3c629: the strict marker rule on the 26 StRS lines (their test files unchanged) and the 486-fragment counts of line 56 as judged then.

## Observations (not counted as failures)

- Line 100: "`Line before` as the files stood before the sort" names no SHA; it describes a table column, not a Test plan item or a caption.
- The CR-505 spec names neither the LAYOUT-023 known-issue text nor the 15 removed lines explicitly.
- BLOCK-006 S2 activates by a synthetic DOM click; MYST-016 S2 asserts the shown panel's identity only through the edit-mode step.
- The refused removal command of the first pass is reported in `work/scratch/verify-2c0a01a-1.md`; this pass met no refusal.
