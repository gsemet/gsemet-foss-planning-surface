# CR-515 verification

Head: 2fb89df9c1d19c9e882702f7b2f8328ccc105ae8

Base: `b9a1abd074ab34ba49920448315c86452d80d832`. Pull request 541 (draft). Verdict:
**NOT VERIFIED**, on claim 16 only (the description). Every claim about the code, the tests, the
gates and the CI run holds at the head; the fix is an edit of the description.

`<worktree>` is the CR's worktree, `<work folder>` the CR's `work/` folder, `<repo>` is
`gsemet/markdown-okf-schema-studio`. Raw logs are in `<work folder>/gates/`.

## 1. The head judged is the pushed head and the pull request's head: VERIFIED

SHA: 2fb89df

- `git -C <worktree> rev-parse HEAD` -> `2fb89df9c1d19c9e882702f7b2f8328ccc105ae8`; parent
  `b9a1abd...`; `git status --porcelain` empty.
- `git ls-remote origin` -> the branch at `2fb89df...`, `main` at `b9a1abd...`.
- `gh pr view 541 --repo <repo> --json headRefOid,isDraft,state,body` ->
  `2fb89df9c1d19c9e882702f7b2f8328ccc105ae8  true  OPEN`; one commit, base `main`, title
  `ci: split the visual checks into two jobs that run in parallel`, mergeable and clean.
- `git -C <worktree> diff --stat b9a1abd 2fb89df` -> `16 files changed, 1112 insertions(+), 141
  deletions(-)`: ci.guidelines.md, ci.yml, pages.yml, AGENTS.md, CONTRIBUTING.md, justfile,
  requirements/config.yml, requirements/tiers/log.md, SwRS CORE-076, select_e2e_run.py,
  test_select_e2e_run.py, test_visual_parts.py, test_workflows.py, capture.py, capture_report.py,
  merge_parts.py. The forge lists the same 16 files.

## 2. The campaign runs in two parts (`capture.py`, `capture_report.py`): VERIFIED

SHA: 2fb89df

- `git -C <worktree> diff b9a1abd 2fb89df -- test/visual` -> `VISUAL_PARTS` lists part 1
  (rendering-core to layout-width, 8 groups) and part 2 (theme-zoom to trust-security, 8 groups);
  `parts_problem` runs at every start and exits 2 naming a group in no part or two; `--part` with
  `--scenario` or `--group` is a parser error; a part removes only its own report files and its own
  scenarios' stale captures; the full run also removes `*.part-*.md`; the part manifest carries
  `"part"`; the writing moved to `capture_report.write_reports`.
- Tests of claim 6 (`test_visual_parts.py`: shipped parts cover the groups once, group outside the
  parts, part with a selection, two part runs keep each other's files) pass at the head.

## 3. The merge (`merge_parts.py`): VERIFIED

SHA: 2fb89df

- Same diff -> with no part file and a full manifest it prints `visual parts: none, the full run's
  manifest stands` and exits 0; a missing part, no render manifest, a revision or run id
  disagreement, a scenario absent or unknown, differing results or a missing capture write nothing;
  a failed part or identical screenshots write status failed; earliest start, latest completion,
  `"parts": [1, 2]`; the campaign start is aligned only for a pinned run id whose run and start
  belong to a part.
- Each of these has a test in `test_visual_parts.py`, passing at the head (claim 6).

## 4. `just ci-visual` and `just ci-report`: VERIFIED

SHA: 2fb89df

- `grep` of `<worktree>/justfile` -> line 326 `ci-visual PART=""`; line 332 `usage: just ci-visual
  [1|2]; got '$part'` with `exit 2`; line 337 removes screenshots, first-gap and width-margins (no
  part only); line 348 merges; line 482 `ci-report` runs `merge_parts.py` (before the review step);
  line 215 adds `test_visual_parts.py` to the tests `check` depends on.
- `test_workflows.py` runs the real recipe with fake `npm` and `uv` for parts 1, 2 and none, refuses
  `3`, `0`, `1 2` and `all`, keeps every step after a red one and checks the order in `ci-report`;
  passing at the head (claim 6).

## 5. Workflows, run selection, requirement and documents: VERIFIED

SHA: 2fb89df

- `grep` of `<worktree>/.github/workflows/ci.yml` -> `visual` `timeout-minutes: 15` (line 131),
  `just ci-visual 1` (179), job `visual-2` (190) with `timeout-minutes: 15` (194), restore only
  (223), `just ci-visual 2` (229), artifact `e2e-visual-2-attempt-N` (234); `report` needs
  `visual-2` (539) and downloads it (580-583); `checks` needs it (669). The pattern `retry` matches
  nothing in the file: no retry is added, no limit raised.
- `git diff b9a1abd 2fb89df` -> `pages.yml` changes a comment only; `STAGE_ARTIFACTS` of
  `select_e2e_run.py` gains `e2e-visual-2`; CORE-076 names `visual-2` in S2, S3, S4 and S6, adds
  S12 and lists the new source and test files; `config.yml` adds `test/visual`; a dated log entry;
  no StRS file and no `CHANGELOG.md` among the 16 files; ci.guidelines.md, AGENTS.md and
  CONTRIBUTING.md describe the two parts.

## 6. New and changed tests pass at the head: VERIFIED

SHA: 2fb89df

- `uv run --directory <worktree> --no-sync --group docs --group release --group requirements python
  -B -m pytest test/build/test_visual_parts.py test/build/test_workflows.py
  test/build/test_select_e2e_run.py -q -p no:cacheprovider` -> `184 passed in 16.72s`
  (`gates/verifier-head-tests.log`).

## 7. They fail on the previous code: VERIFIED

SHA: tests of 2fb89df on the code of b9a1abd

Detached worktree of the base under the scratch folder (removed after the runs), same command.

- Control, the base's own two files -> `142 passed in 8.76s` (`gates/verifier-base-own-tests.log`).
- The head's `test_workflows.py` and `test_select_e2e_run.py` -> `18 failed, 137 passed`
  (`gates/verifier-base-new-tests.log`); the reasons are about the change: no recipe for parts, no
  job `visual-2`, no `e2e-visual-2` among the required artifacts; none is a missing file.
- The head's `test_visual_parts.py` -> `ModuleNotFoundError: No module named 'capture_report'`
  (`gates/verifier-base-visual-parts.log`).

## 8. Requirements validate and the update leaves no change: VERIFIED

SHA: 2fb89df (all run in `<worktree>` with `uv run --no-sync --group requirements`)

- `okfreq validate --check-links` -> `1228 requirements, 0 errors, 26 warnings`.
- `okfreq update-coverage requirements --check` -> `0 files would change`.
- `okfreq lint requirements --prose --check --check-links --project-root .` -> exit 0,
  `0 indexes would change`, `0 requirement OKF projections would change`.
- `git status --porcelain` -> empty. These are the two steps of `just requirements-update`, in check
  mode.

## 9. Local gate before the push: VERIFIED

SHA: 2fb89df

- First line of `gates/preflight-2fb89df.log`: `CR-515
  chantier/batch-09/cr-515-split-the-ci-visual-job-in-two-parts-tha
  2fb89df9c1d19c9e882702f7b2f8328ccc105ae8: just preflight`.
- Same log -> line 7 no merge commit; 113-116 56 of 56; 5620-5625 `tests 5366, pass 5358, fail 0,
  skipped 8`; 5763-5765 116 of 116; 5792 `296 passed`; 5796 `1228 requirements, 0 errors, 26
  warnings`; 5853 `0 files would change`; 5875 `4 passed`; 5891 `ci-static: passed`; 5892 the visual
  and later stages skipped on Windows; 5893 `just preflight exit 0`.
- `chantier.yaml` names no long gate.
- `r1.md` and `r2.md` give the Driver's earlier failing-test and requirement runs on earlier trees;
  claims 6 to 8 are judged on my own runs, not on those.

## 10. CI evidence points 1 to 4 of the specification: VERIFIED

SHA: 2fb89df. Run 45827873343, attempt 1, the only run at the head (`pull_request`).

- `gh pr checks 541 --repo <repo>` -> pass: `static`, `static-windows`, `viewer-graph`, `visual`
  6m53s, `visual-2` 7m56s, `report`, `checks`; the real VS Code, release and Pages jobs skipped.
- Point 1: `visual` 413 s (job 139936610350), `visual-2` 476 s (job 139936610303), both success,
  both under 600 s.
- Point 2: `report` (job 139941071289) success; `gates/verifier-ci-report.log` lines 386-388
  `visual part 1: passed, 269 scenarios, 343 s`, `visual part 2: passed, 254 scenarios, 393 s`,
  `visual parts: merged`; 401-405 `ok visual`, `ok review-index`, `ci-report: passed`. The merged
  manifest: status passed, `partial` false, parts [1, 2], 523 of 523 (claim 11).
- Point 3: `checks` (job 139941451671) success.
- Point 4: both job logs restore the key
  `apt-archives-visual-Linux-ubuntu26-X64-08f25b32...` (`verifier-ci-visual.log` 260,
  `verifier-ci-visual-2.log` 262) and print `dev-ci: system packages installed from
  .cache/apt-archives, no mirror contacted` (762, 764).
- Parts: `capture.py --part 1` (log 778) and `--part 2` (780), `rendered 225 pages, 523 scenarios`
  in both, `ci-visual: passed` in both; the table breakout tests run in part 1, `tests 14, pass 14`
  (lines 1256-1258).

## 11. Every scenario and check still runs: VERIFIED

SHA: 2fb89df against b9a1abd (base run 45825388443)

- `python -I -B <work folder>/verifier/compare_runs.py <base e2e-visual zip> <head studio-reports
  zip>` (`gates/verifier-compare-runs.log`; head zip sha256 `ccc17ac0...`, equal to the forge's) ->
  523 scenarios on both sides, same identifiers in the same order, 523 passed, 0 failed; 497
  captures (85 step, 412 final) on both, all referenced files present, no identical images; 2092
  machine check rows on both; 0 differences in capture files, checks, capture flag, status or keys;
  breakout 1/1, first-gap 56/56, width-margins 12/12; only six per-part report files added;
  `MACHINE-CHECKS.md` identical, `INDEX.md` differs by the revision line.
- The head manifest's revision `41bce3e...` is the pull request's merge commit: `gh api
  repos/<repo>/commits/41bce3e...` -> parents b9a1abd and 2fb89df, tree `ddf80dad...`, the head's
  tree.

## 12. Description renders, shows no user name: VERIFIED

SHA: description posted on 541, read at head 2fb89df; equal to
`<work folder>/verifier/posted-body.md` (`diff` of `gh pr view 541 --json body` against it: no
difference).

- The forge's rendered HTML (`gh api` with the `full+json` media type) -> every heading, list, the
  table, the checklist, the diagram block and the footer link; the project's template has no fold.
- The diagram rendered with the project's `mermaid` in headless Chromium -> 4 nodes, labels
  `visual: just ci-visual 1(+ table breakout tests)`, `visual-2: just ci-visual 2`, `report: just
  ci-reportmerge_parts.py first`, `checks`, and both artifact edge labels; no error.
- No image in the body; `grep` for the user name, home paths, `STALE` and `UNVERIFIED` in
  `<work folder>/verifier` -> no match.

## 13. Summary, Deliverables, Changes and Impacts match the diff and are proven: VERIFIED

SHA: 2fb89df; history figures from the runs named

- 804 to 890 s on `main`: `gh api repos/<repo>/actions/runs/<id>/jobs`, job `visual`, runs
  45412775118 882, 45429944338 804, 45459891203 882, 45476952370 842, 45580228461 863,
  45713440510 885, 45771447942 821, 45773405420 890 (all success); the base run 877.
- One pass line one second after the limit: run 45794366914 (head `e76c0843`), job 139821112935,
  started 09:41:54Z, cancelled, annotation `exceeded the maximum execution time of 15m0s`; log line
  1520 `09:56:55.783 ci-visual: passed`, the limit being 09:56:54.
- 523 -> 269 and 254, group ranges, limit and local commands: claims 2, 4, 5, 10, 11.
- Changes: each of the seven bullets is in the diff (claims 2 to 5); no delivered change is left
  out.
- Impacts has "No visual change" with its reason. Screenshots folder emptied: justfile line 337, and
  real-window captures live under that folder (`captureRegistry.ts`), read by `ci-gallery`.
  `ci-report` refusing unpinned part-by-part runs and the site deployment running the suite for an
  older run: tests of `test_visual_parts.py` and `test_select_e2e_run.py` (claim 6).
- Blast radius: one grade with its explanation; the grade is the author's judgement.

## 14. Autonomous decisions, Known gaps, internal references: VERIFIED

SHA: 2fb89df

- The three decisions match the diff and the round notes (`r1.md`, `r2.md`). The acceptance of two
  parts started apart under one local pinned id is the designed behaviour the `justfile` comment and
  S12 state.
- Known gaps lists the two accepted defects (no remedy in the failure message; the awkward
  contributor guide sentence). The first says the guide and the comment "give" the remedy: the guide
  states it, the comment implies it; accepted. No evidence pair is missing
  (`verifier/evidence/before-after.md`).
- The change request number appears under "Internal references" only, as the template asks. "new
  scenario S12" is a scenario of the requirement named on the same line, public in the repository,
  not a planning id (merged requests 524 and 532 name such scenarios); accepted.

## 15. Test plan facts: VERIFIED

SHA: 2fb89df

- New tests fail on the previous code: claim 7. Requirements: claim 8. No user-facing changelog
  line: no behaviour a user sees, `CHANGELOG.md` not among the changed files (claim 1).
- Local gates counts: claim 9; "296 Python tests" leaves out the 4 Sphinx tests, an understatement.
- Review: `chantier log CR-515 --batch batch-09` -> `driver note r2 approved at 54d1da6268...,
  committed as 0b310d45ca...`, then `rebased once onto origin/main b9a1abd ... 0b310d45 ->
  2fb89df..., range-diff =, same tree, review pass carried`. `git range-diff 54d1da62..0b310d45
  b9a1abd0..2fb89df9` -> `1: 0b310d45 = 1: 2fb89df9`; trees of 0b310d45 and 2fb89df both
  `ddf80dad...`. `approved at 2fb89df (carried from 0b310d4)` holds.

## 16. Each proof in the description names its SHA: NOT VERIFIED

SHA: description posted on 541, head 2fb89df

- `<work folder>/verifier/posted-body.md` lines 92-97 -> three checked Test plan items name no SHA:
  `New or changed tests (they fail on the previous code)`, `Requirements: ... leaves no change` and
  `Changelog: No user-facing change`. Lines 98-102 (`Local gates`, `Review`) name theirs.
- The Verifier card asks that each proof name its SHA, and chantier's pull request rules name the
  Test plan items; the project's rules and template are silent on it.
- Fix: write `at 2fb89df` on those three items (the tests and requirements are proven at that SHA by
  claims 6 to 8, the tests against base `b9a1abd`), and name it on `CI green`.

## Sentences now outdated or unproven (to update with the same edit)

- `- [ ] CI green` (line 103): outdated; CI is green at 2fb89df, run 45827873343 attempt 1.
- `The first runs after the merge show whether the time limit holds.` (lines 66-67): partly
  outdated, the pull request run already measured 413 s and 476 s; what stays unproven is the first
  push to `main`, with the heavy jobs (the specification's after-merge check).
