# Verify CR-495

Head: d2c55f0f4f7906d712e4c834684f84dbd49c106b

All claims judged at d2c55f0 unless said.

- AGENTS.md role bullet equals the spec's "After" text (re-wrapped), plus the git-folder sentence and the `brief` exception line; docs/planning-folder.md one line. Command: `git diff origin/main...HEAD -- AGENTS.md docs/planning-folder.md`. Output: the three sentences, the two exceptions word for word, `brief` line as the spec asks. Path differs from spec by the added `<project>/` folder, stated in the PR's Autonomous decisions. PASS.
- No test reads the old role sentences. `git grep -n -i "knows no role\|role's contract lives\|says what it refuses\|what the role judges" origin/main -- skills/chantier/scripts/cli/tests` printed nothing. PASS.
- No card or wrapper edited: `git diff --stat origin/main...HEAD -- skills/chantier/references/*.md agents com.github.copilot` shows only `references/floor.md` (new, 14 lines). PASS.
- `just check` at d2c55f0: exit 0, "2745 passed, 20 skipped in 114.79s", release-notes ok (log: work/verifier-check.log). PASS.
- `just eval-dry-run` at d2c55f0: "dry run: 25 of 25 cases as expected", `ok quiz-folder` positive. PASS.
- `just mod` at d2c55f0: "118 pass, 0 fail". PASS.
- `pytest tests/test_brief.py`: "26 passed in 6.04s". PASS.
- PR description as posted (`gh pr view 481`) is identical to work/pr-body.md; renders, no image, sections consistent with the diff (20 files; Changes list matches). PASS.
- Review box: the PR says `Review: approved at d2c55f0`. `chantier log CR-495` holds only `inspector approved at ac0367164ca5...` (pre-rebase, round 1) and `body re-inspection approved at ac03671...`; no note of an approved pass at d2c55f0, and no `carried from ac03671` note after the rebase (head moved from ac03671/d5769c38 to d2c55f0 with a rebase and a later commit, d2c55f0 "brief Coverage bullet ends with a semicolon"). FAIL: no approving note names the SHA the box cites.
- Test plan line "just scenario passed locally on the round's tree": no proof at d2c55f0 and the ship event says "no long gate passed at d2c55f0". UNVERIFIED claim stated as checked and not in Known gaps (not top of stack, so not owed, but the line claims a run). FAIL until narrowed or moved to Known gaps.
- Screenshots: not applicable (no UI); no images attached.

NOT VERIFIED

## Re-verification at d2c55f0 (second pass)

Head: d2c55f0f4f7906d712e4c834684f84dbd49c106b

All technical claims above carried from the first pass at the same head (d2c55f0, unchanged).
- Log note: `chantier log CR-495` now holds "r1 approved at d2c55f0 carried from ac03671 ..." PASS for a box citing ac03671 carried to d2c55f0.
- PR description as posted: `gh pr view 481 --json body` still reads "`just scenario` passed locally on the round's tree" (line 56) and "Review: approved at `d2c55f0`" (line 58); work/pr-body.md holds the fixed text but is not posted (diff shows lines 56 and 58 differ). FAIL: the posted description still has both defects. Post work/pr-body.md to the PR.

NOT VERIFIED

## Re-verification at d2c55f0 (third pass)

Head: d2c55f0f4f7906d712e4c834684f84dbd49c106b

Technical claims carried from the first pass at the same head (d2c55f0, unchanged).
- PR description as posted (`gh pr view 481 --json body`, judged at d2c55f0): renders (sections, fold, no image); Summary, Deliverables and Changes match `git diff --stat origin/main...HEAD` (20 files; cli.py and near_misses.py registrations are the `brief` command line noted). Test plan scenario line now names ac03671 and the pipeline job at this head; Review box says approved at ac03671 carried to d2c55f0, matching the log note "r1 approved at d2c55f0 carried from ac03671". Known gaps present. PASS.

VERIFIED

## Description-only pass (final posted body, judged at d2c55f0f4f7906d712e4c834684f84dbd49c106b)
- `gh pr view 481` body: renders, no image, Summary/Deliverables/Changes match the diff as judged above, Test plan boxes ticked, Review box "approved at ac03671 (carried to d2c55f0)" matches log notes "r1 inspector approved at ac03671" and "r1 approved at d2c55f0 carried from ac03671", Known gaps present, no role name outside Internal references. PASS.

VERIFIED

## Description-only pass 2 (judged at d2c55f0f4f7906d712e4c834684f84dbd49c106b)

Head: d2c55f0f4f7906d712e4c834684f84dbd49c106b

- `gh pr view 481 --json body,headRefOid` (headRefOid = d2c55f0): renders, no image; Summary, Deliverables and Changes match `git diff --stat origin/main...HEAD` (20 files); Test plan names no SHA outside d2c55f0 history (wording "before the rebase onto main"); Review box "approved on the tree before the rebase onto main (carried to d2c55f0)" matches log notes "r1 inspector approved at ac03671" and "r1 approved at d2c55f0 carried from ac03671"; Known gaps present; no role name outside Internal references. PASS.

VERIFIED
