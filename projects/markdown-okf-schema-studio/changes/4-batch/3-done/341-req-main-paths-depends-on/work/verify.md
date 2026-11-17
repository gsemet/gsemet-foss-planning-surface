# Verify CR-341

Head: f16dbc3c8bc2fb4d928a11d8324a74f530f13027

Base: dedbdb2ac283e76ac91e718c683168f8fe67278a (origin/main).

1. Tests at f16dbc3: `uv run --no-sync pytest test/build/test_check_main_paths.py -q` -> `12 passed in 0.39s`. The three new tests (depends_on passes, neither fails with both-ways message, superseded depends_on fails) are in the file. PASS.
2. Same tests at the base (detached worktree of dedbdb2a, new test file copied in, head's python): `2 failed, 10 passed`; failed: test_depends_on_sibling_passes and test_neither_derived_nor_depended_fails_with_both_ways (message was `... does not derive from StRS-T-A-001`). The superseded test passes at the base too, as that rule already existed (a regression guard). PASS.
3. `just requirements-lint` at f16dbc3, last line: `main paths: 78 StRS checked, 536 SwRS citations, all valid`; count unchanged. PASS.
4. Manual check on a temp copy of the real bundle (StRS-MDOKFSTUDIO-BLOCK-001, SwRS-MDOKFSTUDIO-BLOCK-001 with the derives link removed): without depends_on -> `does not derive from StRS-MDOKFSTUDIO-BLOCK-001 and is not in its depends_on`; with depends_on and the SwRS active -> no problem; with the SwRS superseded -> `is superseded, not active`. PASS.
5. Diff vs spec (`git diff origin/main...HEAD`, 4 files): item 1 (check + message + docstring) done; item 2 (bullet and the shared-rule sentence) done; item 3 tests done; item 4 no requirement moved (no file under requirements/tiers other than log.md); item 5 dated `## 2026-11-17` entry in log.md, project rules (okfreq-baseline: agents append a dated entry after substantive edits) ask for it. PASS.
6. PR body (work/pr-body.md): Summary, Deliverables table, Changes match the diff (checker, guideline, tests, log; nothing unmentioned); test plan numbers (12 passed, 78/536) match items 1 and 3; Known gaps "None" is right (before-after.md records no uncaptured pair); no images; role names appear only in Internal references. PASS.
7. Review box `approved at f16dbc3`: `chantier log CR-341` has "r1 approved at dedbdb2, committed as f16dbc3". PASS.
8. Gate pass: gate log first line `gate CR-341 branch ... head f16dbc3c8bc2fb4d928a11d8324a74f530f13027`, command `just preflight`. PASS. CI "CRs green" not rerun, per brief.

VERIFIED

## Description pass (PR 409 as posted, head f16dbc3c8bc2fb4d928a11d8324a74f530f13027)

Command: `gh pr view 409 --json body,headRefOid,title`; headRefOid = f16dbc3c8bc2fb4d928a11d8324a74f530f13027 (the head); `git diff --stat origin/main...HEAD` = 4 files (check_main_paths.py, project.guidelines.md, test_check_main_paths.py, tiers/log.md).
- Sections in order (Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps, fold with Changes, Impacts, Test plan, Internal references), blank lines around the fold, nothing after it; Deliverables table matches the checker diff (message text, depends_on list or str, inactive error kept). PASS.
- Changes match the diff (checker, guideline, tests, log, no requirement moved); nothing unmentioned. PASS.
- Internal references (CR-341, batch) only in the last section; no role names; no images. PASS.
- SHAs f16dbc3 right; 12 passed and 78/536 proven by items 1 and 3 above; Review box matches log "r1 approved at dedbdb2, committed as f16dbc3"; Known gaps "None" right (before-after.md has no uncaptured pair). PASS.
- Note: the Test plan has no Evidence item (project template has none; before-after.md records the 2-failed-at-base pair, which the first item states). Not a failure.

VERIFIED

## Second pass, head 72eb59fcf875ace3320c68ddbd9bc99f5df4e35b (move f16dbc3..72eb59f, restack onto CR-340 10c9233)

Head: 72eb59fcf875ace3320c68ddbd9bc99f5df4e35b

Touched by the move: log.md (conflict), and the base (`git diff --name-only dedbdb2 10c9233` includes requirements/guidelines/project.guidelines.md, requirements/tiers/log.md, justfile, scripts/check-marker-companions.mjs). check_main_paths.py and its test are not in the base diff; carried from f16dbc3 by content (`git diff --stat 10c9233 72eb59f`: check_main_paths.py, test_check_main_paths.py, project.guidelines.md, log.md).

1. Tests at 72eb59f: `uv run --no-sync pytest test/build/test_check_main_paths.py -q` -> `12 passed in 0.63s`. PASS.
2. `just requirements-lint` at 72eb59f, last line: `main paths: 78 StRS checked, 536 SwRS citations, all valid`. PASS.
3. log.md at 72eb59f: no conflict markers (grep count 0); the CR 341 entry sits under `## 2026-11-17` after the CR-340 entry, 5 lines added vs 10c9233. PASS.
4. Before/after of claim 2 of the first pass: carried from f16dbc3 (checker and test unchanged by the move).
5. Gate pass at 72eb59f: FAIL. `work/gates/20261117-201306.log` first line names head 72eb59fc... but the run is still in progress (last line is the okfreq validate step, no pass); `chantier log` has no gate pass at this head. Not run by me, per brief.
6. PR 409 description as posted (`gh pr view 409 --json body,headRefOid`): headRefOid is 72eb59f, but the Test plan still says `12 passed at f16dbc3`, `unchanged count ... at f16dbc3`, `just preflight passed at f16dbc3`, `Review: approved at f16dbc3`, `Verified at f16dbc3`, `CI green at f16dbc3`; f16dbc3 is not in the head's history and none is a `carried from` proof. The PR is also still draft with base `main` while the branch forks from CR-340's head. FAIL.
7. Review box: `chantier log CR-341` has "inspector approved at 72eb59fc..." for the move; the box must name 72eb59f (or carry). Currently names f16dbc3. FAIL with item 6.

NOT VERIFIED

## Third pass, head 72eb59fcf875ace3320c68ddbd9bc99f5df4e35b

Head: 72eb59fcf875ace3320c68ddbd9bc99f5df4e35b

Only the failed points of the second pass are judged again; the rest is carried from the second pass at the same head.

5. Gate pass: `chantier log CR-341` has `driver gate result=pass head=72eb59fc... command=just preflight run=20261117-201306-33800`; gate log last line `result: pass at 72eb59fcf875ace3320c68ddbd9bc99f5df4e35b`. PASS.
6. PR 409 body (`gh pr view 409 --json body,headRefOid`): headRefOid 72eb59f; grep of the body shows no f16dbc3, and every Test plan SHA is 72eb59f (tests, requirements, preflight, Review, Verified, CI green). The Review line says the restack was re-reviewed, patch carried from f16dbc3, with a note in the log: "inspector approved at 72eb59fc...". `gh pr checks 409`: checks, report, static, static-windows, visual pass; others skipping. Draft and base `main` stay until the stack driver makes the stack on the forge: not a failure of the CR. PASS.
7. Review box names 72eb59f, matching the log note. PASS.

VERIFIED
