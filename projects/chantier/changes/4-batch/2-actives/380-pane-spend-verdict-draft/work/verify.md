# Verify CR-380 (first verification)

Head: 924d0d713866bdc5122e1ef381d4a77645040276

All claims judged at 924d0d7 (worktree clean, `git rev-parse HEAD` = the head above).

## 1. pytest: steps and now/next lines, board words and design - VERIFIED (924d0d7)
Command: `python -m pytest skills/chantier/scripts/cli/tests/test_cli_units.py .../test_code_targets.py .../test_board_design.py -q`
Output: `59 passed, 1 skipped in 4.20s` (skip = the "none + out of draft" case, which reads ready to merge by design).
Read the diff of the new tests: `step_entries` over (both, verdict only, neither) gives Long gate/Verdict/Handed back as specified; `notify` over pr_draft True/False/None x 4 waits asserts now == "PR in draft: " + `_ready_lines` clause + ".", no `on <base>,`, next line without "the PR is out of draft" iff pr_draft is False.

## 2. Pane (hooks/register.tsx, types) - VERIFIED (924d0d7)
Command: `just mod` (log: work/mod.log). Output: `Validation passed with warnings`; `84 pass / 0 fail`, including `(pass) a batch title line shows the spend age, says it is unknown, or shows none without a spend` (12 min old / age unknown / neither for spent_usd null). The 11 TS warnings from the plugin validator concern `ChantierFeed.views` and RenderChildren, none concerns spent_at or spent_usd (a null spent_usd type-checks).
Code: `spentOld` = '' when spent_usd null, ` · age unknown` when age null, else ` · <n> min old`, right after the gauge, from `minutesSince(b.spent_at ?? null, now)`; `types/index.d.ts` adds `spent_at?: string | null`; `docs/boards.md` wording matches the spec.

## 3. Web board - VERIFIED by reading (924d0d7), no render test exists
`test_code_targets.py` and `test_board_design.py` pass (claim 1). Read: `js/model/spend-age.js` (nothing when spent_usd null; `batch.spent_age` if `age(cost_at, now)` known else `batch.spent_age_unknown`); `home-batch.js` muted `<small class="mut">` line under the meter; `batch.js` `figures(batch, now)`, render passes `state.now`, kpi sub = `of $X` + ` · ` + text; en and fr keys `batch.spent_age`, `batch.spent_age_unknown` with the spec's words. Scripts 204 and 64 lines (< 300). No server change.
Not captured by me: screenshots of the web board and of the pane from a real session (I cannot run a real Claude Code session or a browser capture); they stay in the PR's Known gaps, which names both.

## 4. Scenario - VERIFIED (924d0d7) by CI, plus diff read
`gh pr view 343`: head 924d0d713866bdc5122e1ef381d4a77645040276; `just scenario (ubuntu-latest)` SUCCESS, `just check` ubuntu/macos/windows SUCCESS, `just eval-dry-run` SUCCESS. Diff of `scenario/run_scenario.py` carries the three checks the spec names (12f Verdict step in STATUS.json and STATUS.md, the stacked-by-hand now/next lines, the index `spent_at`). I ran no local scenario and no hand CLI run in a scratch project: the in-process pytest (claim 1) and the CI scenario cover the same CLI paths.

## 5. Ready line unchanged - VERIFIED (924d0d7)
Diff of `commands/driver.py`: the clause moved verbatim to `stacks.draft_clause`; `_ready_lines` calls it; the pytest compares `_ready_lines` to `notify` for 11 cases.

## 6. PR description - VERIFIED (924d0d7)
Read as posted: clean sections and fold, no images; Summary, Deliverables and Changes match the diff (15 files vs the base); Known gaps names the missing pane screenshot and web board screenshots; no role names beyond internal references. Review box `approved at 924d0d7`: `$CHANTIER log CR-380` has "r1 approved at 8a88c556, committed as 924d0d71". The `Verified at` and `CI green` boxes are the Driver's to tick.

## Gate pass
No gate log in work/gates: none run by me. The pipeline's `just scenario (ubuntu-latest)` is green at the head (claim 4); the hand-back checklist at this head is the Driver's.

VERIFIED
