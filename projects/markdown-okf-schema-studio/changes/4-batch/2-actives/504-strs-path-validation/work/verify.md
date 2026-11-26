# Verify CR-504 (CR-A)

Head: 2c0a01a3ec265c60514533044f2405e393c9283d

Pass after the restack on CR-500 and round 10 (last verdict: VERIFIED at `2f3c629`, base `main`; copy in `work/scratch/verify-2f3c629-final.md`). Judged: the local file `work/pr-body.md` (402 lines, modified 2026-11-26 06:01:09 +0100). The description on the forge is the old one and is not judged here. `<W>` is the CR worktree, `<CR>` the CR folder, `V` is `<CR>/work/verifier`, `S` is `<CR>/work/scratch`.

## Verdict: NOT VERIFIED

Two claims fail. Both are defects of the body text alone; no code or project file defect found.

### F1. Test plan, Evidence: a proof that names no SHA (body line 389), at 2c0a01a: NOT VERIFIED

Exact line:

> - [x] Evidence: no visual change in the extension; the requirements site is checked by its unit tests, and the verification compared it before and after in a browser before the restack on the changes below (screenshots not posted)

- Rule: verifier card, "Each proof in the description names its SHA, which is the head or carried with its reason"; pr-template, Test plan form "Evidence: before at `<sha7>`, after at `<sha7>`".
- `gh pr view 524 --json body` into `S/v/posted.md`, `git diff --no-index` against the file: the posted line read "... before and after in a browser at `2f3c629` ...". The SHA was removed after the move and none replaced it.
- The comparison did take place (`V/evidence/before-after.md`: before `17b779d5`, after `2f3c629a`); only the form fails.
- Wording this pass can prove: "... and was compared in a browser, `main` (`17b779d`) against `2c0a01a` (carried from `2f3c629`) (screenshots not posted)". Reason for the carry: `git diff --stat 2f3c629a 2c0a01a3 -- src test/site/requirementsViewer justfile requirements/tiers/strs requirements/tiers/swrs`: empty; the head's card figures are unchanged (claim 5); the move's only inputs to the site are `requirements/tiers/log.md` and the markers of `test/site/siteClips.test.ts` (the CORE-095 tested-by list).

### F2. Deliverables: a SHA outside the head's history, not marked as carried (body line 43), at 2c0a01a: NOT VERIFIED

Exact line:

> Measured before the restack on `main`, at `1905009`: a scratch copy of the bundle and of the sources, with the mode set to `linked-swrs-and-acceptance-paths`, validated with 0 errors and 104 warnings: W004 x78 (a StRS with no `@accepts_req` yet) and W2 x26 (placeholder cross-links that existed before). The mode switch and the W004 are for the follow-up change.

- `git merge-base --is-ancestor 1905009 2c0a01a3`: not an ancestor (the commit exists locally).
- Rule: pr-template, "only the SHA after `carried from` may lie outside the head's history". `ship`'s stale-SHA check does not flag it only because its pattern needs a letter a-f and this hash is all digits.
- This line passed at `2f3c629`; it is judged again because the brief puts the body's commit hashes under judgment after the move.
- The figures hold at the head (claim 7: 0 errors, 104 warnings, W004 x78, W2 x26). Wording this pass can prove: "Measured at `2c0a01a`: a scratch copy ...".

## Judged at 2c0a01a, holding

1. Head, tree, PR. `git rev-parse HEAD`: `2c0a01a3ec26...`; `git status --short --branch`: clean, level with upstream; `git ls-remote`: branch `2c0a01a3`, base branch `c7c6a562`, main `17b779d5`. `gh pr view 524`: `OPEN`, `isDraft true`, head `2c0a01a`, base CR-500 branch `c7c6a56`, `CLEAN`, title `build: declare StRS paths and SwRS scenarios on okf-schema 0.18`. VERIFIED.
2. Move. `git range-diff` of `17b779d5..2f3c629a` against `c7c6a562..2c0a01a3`: all `=` except `b93e855a` `!` (hunk context in `siteClips.test.ts` only) and the new `2c0a01a3`. `git diff --name-only` of both own diffs: the same 1293 files. `2c0a01a` changes 2 files: `requirements/tiers/log.md` (+4, under `## 2026-11-26`) and nine `#S1` in `test/site/siteClips.test.ts`. `git diff --name-status 2f3c629a 2c0a01a3 -- src test requirements scripts justfile package.json package-lock.json sphinx pyproject.toml uv.lock`: only `log.md`, `check-no-merge-commits.sh`, `test_no_merge_commits.py`, `siteClips.test.ts` (the last three brought by the base). VERIFIED.
3. Test plan line 388, local gates. Gate log `work/gates/preflight-2c0a01a.log`, first line `CR-504 chantier/batch-09/cr-504-strs-paths-and-swrs-scenarios-declared-o 2c0a01a3ec265c60514533044f2405e393c9283d just preflight`, last `preflight exit=0 head=2c0a01a3...`: `check-markers: 11 companion file(s), 459 in-force SwRS marked, 13 files on the marker baseline`; unit `5326 tests, 5318 pass, 0 fail, 8 skipped`; security `107/107`; pytest `213 passed`; `1228 requirements, 0 errors, 26 warnings`; main paths `96 StRS checked, 625 SwRS citations`; `94 StRS` diagrams parse; sphinx `4 passed`; `0 vulnerabilities`; `ci-static: passed`. It runs `just check` and `just requirements-lint`. No long gate in `chantier.yaml`. VERIFIED.
4. Test plan lines 390 and 392. `chantier log`: `r10 approved at 94f070d798df8da00f08ceb097886631f28fa8e2, committed as 2c0a01a3ec265c60514533044f2405e393c9283d`. `gh pr checks 524` exit 0: `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual` pass, the others skipping; `gh run view 45757241066`: headSha `2c0a01a3`, success. Line 391 is unchecked on purpose. VERIFIED.
5. Figures and lists (lines 71-73, 87-89, 99-291). `V/scan.py <W> 2c0a01a3`: 1228 requirements; live StRS 95 all declare; live SwRS 461, 459 non-exempt all declare; exempt TRUST-070 and TRUST-075; declaration problems 0; markers tests 5608, accepts 19, implements 1531; all violation counts 0; scenarios 722 of 2633 unmarked; paths 133 of 156 unmarked; 78 StRS without `@accepts_req`; 17 paths accepted, 6 tested; LIFE-023 four paths unmarked. `V/lists10.py <W> <CR>`: both lists equal the computed ones; 66 candidate paths all unmarked. `V/table.py <W> work/pr-body.md e5ee7ec1 2c0a01a3`: `187 rows, 0 bad`; `S/r9_check_body.py`: 26 kept lines in 16 files, 0 bad line numbers. VERIFIED.
6. Impacts figures (lines 371-378). `V/figures10.py` on okfreq 0.18.1 reports of main, base and head: main and base `covered 23` of 95; head `covered 1`, linked all covered 24, direct `@tests_req` 6, both MYST-018; exempt linked SwRS all `missing`. VERIFIED.
7. Line 86, commits, and line 43's figures. For each commit, `git archive` into a scratch copy, that commit's own `scripts/check-marker-companions.mjs --root <copy>`, then the copy's mode set to `linked-swrs-and-acceptance-paths` and `uvx --from okf-schema==0.18.1 okfreq validate <copy>/requirements --check-links --project-root <copy> --json`:

   | Commit | Marker check | New mode errors / warnings |
   | --- | --- | --- |
   | `7a80c64c` | pass | 0 / 216 |
   | `bd910ce3` | 54 `fragment-required` (0 siteClips) | 14 / 163 |
   | `b93e855a`, `3b134d7b`, `31a632d9` | 63 (54 + 9 siteClips) | 15 / 64 |
   | `d083eff4` | 63 | 15 / 104 |
   | `94f070d7` | 9 (siteClips) | 1 / 104 |
   | `2c0a01a3` | pass | 0 / 104 (W004 x78, W2 x26) |

   Line 86 VERIFIED.
8. Lines 54 and 78, `test/site/siteClips.test.ts` against CORE-095 S1 to S4, read at the head. The base adds 9 tests, marked `#S1` here; each asserts the video source and the clip files. Seven other tests carry a fragment they do not check (lines 17, 27, 34, 40, 54, 71, 279); the GIF with no WebM (line 34, S2) is marked S3, S4. VERIFIED.
9. Line 78, sampled lines re-read: `mathRenderer.test.ts:52` MYST-024 `#S8`, `alertSourceLines.test.ts:150` GFM-009 `#S10`, `lineEndingSave.test.ts:40` BLOCK-234 `#S3` still check another scenario. VERIFIED.
10. Requirements current and text (line 39, line 383). `okfreq update-coverage requirements --check`: `0 files would change`; `okfreq lint requirements --check --prose --check-links --project-root .`: `0 indexes would change`, `0 requirement OKF projections would change`; exit 0, tree clean. `V/reqdiff.py <W> c7c6a562 2c0a01a3`: only CORE-097 added; 97 retired SwRS newly exempt, none approved; the 15 approved StRS change only `approved_at`, `verified`, `scenarios`, same approver; other body differences beyond heading ids are on `proposed` requirements. `git diff --numstat c7c6a562 2c0a01a3`: CORE-069 `48 6`, CORE-080 `38 6`, CORE-082 `29 8`, CORE-097 `108 0`. Lines 384-385: `git grep -E "@(implements|tests)_req SwRS-MDOKFSTUDIO-CORE-(069|080|082|097)" 2c0a01a3 -- scripts test src` shows markers in `model.ts`, `home.ts`, `pages.ts`, `model.test.ts`, `home.test.ts`, `pages.test.ts`, `write.test.ts` (also `bundle.test.ts`), `check-marker-companions.mjs` and `checkMarkers.test.ts`. VERIFIED.
11. Changelog and no user-facing change (lines 369, 387). `git diff c7c6a562 2c0a01a3 -- CHANGELOG.md docs/releases-notes src package.json package-lock.json skills .github`: 0 lines. VERIFIED.
12. Configuration (line 43's mode names, Changes). `requirements/config.yml`: mode `linked-swrs-and-validation-test`, `accepts: '@accepts_req'`; `pyproject.toml` `okf-schema>=0.18.1`; `uv.lock` 0.18.1; `scripts/marker-baseline.json` `strsTestsInIntegration`: `{}` (line 57). VERIFIED.
13. Internal references (lines 396-397). `work/coder/r1.md` to `r9.md`, `work/r10.md`, `evidence/` exist. The CR-505 spec covers every declared scenario, every live path's acceptance test, the 136 dropped blocks, the wrong fragments and the mode switch. VERIFIED.
14. Cleanliness. 0 user name or home path hits, 0 images, no STALE or UNVERIFIED mark, one `details` opened and closed, no internal reference before "Internal references", no chantier role name as the doer; local Markdown render: 12 `h2`, 2 `h3`, 3 tables, no stray pipe paragraph; UTF-8 without BOM, LF. VERIFIED.

## Carried from 2f3c629a

Reason for all: the own file list is identical, the range-diff shows no patch change but the context noted in claim 2, and `git diff --stat 2f3c629a 2c0a01a3` over the marker script and baseline, mutation report, viewer, `test/shared`, `justfile`, `pyproject.toml`, `uv.lock`, `config.yml`, schemas, `.agents/skills`, `requirements/guidelines`, CONTRIBUTING and the StRS and SwRS tiers shows only one glossary line brought by the base.

- carried from 2f3c629: line 382, new or changed tests fail on the previous code (`V/oldcode.py`; the 23 changed cases are among the base-code failures). The old files are the same on `c7c6a562` as on `17b779d5`.
- carried from 2f3c629: line 386, the six requirements from `main` (ids, order and markers only), and line 80 (15 removed marker lines, DIAG-123).
- carried from 2f3c629: line 79 (12 SwRS), lines 81-82 and 92-93 (requirement and test files unchanged).
- carried from 2f3c629: marker rules (`V/ownersteps.py`), split test files lose no assertion, viewer behaviour and card figures of the before/after, skills and guideline refresh, exemption reasons, Human decisions, Summary, Deliverables and Changes against the diff (the two files of `2c0a01a` are covered by Changes).
- carried from 2f3c629: the strict marker rule on the 26 StRS lines (their test files unchanged) and the 486-fragment counts of line 56 as judged then.

## Observations (not counted as failures)

- Line 100: "`Line before` as the files stood before the sort" is checked against `e5ee7ec1`, which is not in the head's history; the line names no SHA. It describes a table column, not a Test plan item or a caption.
- Line 56: "The scenario fragment of each SwRS test marker was first chosen by a keyword match" is broader than true (the nine round-10 markers, the hand-read ones and the CORE-097 markers were not); "each migrated" would be exact.
- Line 86: after the restack `b93e855a` to `d083eff4` have 15 new-mode errors (the body's 14 is dated before the restack) and `94f070d7` has 1, not mentioned. The body says the first commit was not re-measured; this pass measured it: `7a80c64c` passes the marker check, 0 new-mode errors.
- The CR-505 spec names neither the LAYOUT-023 known-issue text nor the 15 removed lines explicitly.
- BLOCK-006 S2 activates by a synthetic DOM click; MYST-016 S2 asserts the shown panel's identity only through the edit-mode step.
- If F1 or F2 is accepted rather than fixed, Known gaps needs its bullet.

## Refusal met in this pass

A Bash command of mine holding `rm -rf "$D"` was refused. It would have cleared `S/v/{main,base,head}` before re-creating them; they did not exist. Not retried and not worked around: new empty folders were used instead. Exact text:

> Permission for this command was denied by a built-in Claude Code safety check, not by the user. The check stops removals that can delete far more than intended: a system, home or workspace directory, or a target it cannot resolve, such as a shell variable that, if unset or empty, turns this into `rm -rf /` or `rm -rf /*`. Only a person may approve such a removal, and no person did (the permission prompt timed out, or none was shown). The command was NOT run; do not claim it succeeded. Do not work around the check by splitting, scripting, or re-issuing the removal through another tool or shell: the check exists because a removal like this can destroy the user's data, and getting past it would not make it safe. If the text below suggests a safe rewrite, run that instead; it goes through the same check. Otherwise finish the rest of the task without this removal, tell the user what you wanted to delete and why, and leave the removal to them. What was flagged: Dangerous rm operation detected in `rm -rf "$D"`. This command sets $D from `"$S/$n"`, which is the filesystem root when the variable in it is empty, so this rm can remove that directory. A `${D:?}` guard does not help, because $D is not empty. This requires explicit approval and cannot be auto-allowed by permission rules. Use a literal absolute path instead.

Also, before that refusal, the per-commit script of claim 7 (`S/v/percommit.sh`) held `rm -rf "$D"` and `rm -f "$S/cm.mjs"` and ran; both targets are the script's own scratch copy (`S/v/c`) and script copy.
