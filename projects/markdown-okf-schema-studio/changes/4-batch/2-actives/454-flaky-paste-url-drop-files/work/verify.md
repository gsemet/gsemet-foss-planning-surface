# Verify CR-454

Head: 845997bb757b19f14b92a269672776160dde9455

Base: origin/main e0c7836c (merge-base). PR 460, draft, head 845997bb (gh pr view).

## Claims

1. Evidence 1, static gate at 845997bb. Gate log first line: `gate CR-454 branch chantier/batch-07/cr-454-flaky-real-window-paste-url-and-drop-fil head 845997bb757b19f14b92a269672776160dde9455`, last line `result: pass at 845997bb757b19f14b92a269672776160dde9455` (work/gates/20261121-133852.log). Re-run at 845997bb: `npx tsx --test test/build/stressPlan.test.ts test/build/hangWatchdog.test.ts test/build/realWindowTrace.test.ts` gives pass 23, fail 0, skipped 4 (the existing ps-based watchdog tests, Windows); includes "CR 454: paste-url and drop-files run in the default trusted plan, alone when named, never in the untrusted window". `uv run --no-sync python -m pytest test/build/test_workflows.py -q`: 81 passed. `git grep` for `12 rounds|all 19|19 scenarios|'12'|defaultRepeat = 10` leaves only a comment saying 12 rounds would not fit. VERIFIED.
2. Evidence 2, helper unit test: test/build/realWindowTrace.test.ts has five tests (format line and JSON fields; failing body prints error, then trace once, rethrows same error; passing body; collector that never settles gives collectError after the bound; collector that throws never replaces the error); they pass in the run of claim 1. VERIFIED.
3. Evidence 3: `git grep -n -E "storedEditModeForTests|setTimeout\(resolve, (700|400)\)" -- test/integration/pasteUrl.test.ts test/integration/dropFiles.test.ts` at 845997bb printed nothing, exit 1. VERIFIED.
4. Evidence 4, default heavy dispatch: run 44903251073 (gh run view) is at 9fce8441, not 845997bb; conclusion success, integration success, stress success; log lines `stress: launch deadline 1440000 ms (11 rounds x 21 scenarios, ceiling 1440000 ms)`, `stress: 11 round(s) of ... checkbox-toggle, paste-url, drop-files`, `stress: 11 round(s) passed`; stress job 12:18:40 to 12:34:48 (16 min, setup included) against 24 min. Carried from 9fce8441: `git range-diff be10fe81..9fce8441 e0c7836c..HEAD` shows the CR patch commits identical (`3 = 2`) and the first commit's only difference the requirements/tiers/log.md context (the long-path commit bec8d0d3 is already on main). No default-plan heavy run was dispatched at exactly 845997bb; carried. Narrow run 44903254624 at 9fce8441 also success. VERIFIED (carried).
5. Evidence 5, trace in a real window: runs 44905091608 (paste-url) and 44905104654 (drop-files), branch throwaway/cr-454-trace-proof at d571951e, stress job logs contain `paste-url failed: Error: forced failure for the trace proof` + `paste-url failure trace: {...}` and the drop-files pair; the lines match evidence/trace-proof.md and the PR body. VERIFIED.
6. Evidence 6, 100-round loop: run 44904977842 at 845997bb, success; log `stress: launch deadline 1320000 ms (100 rounds x 2 scenarios, ceiling 1440000 ms)`, `stress: 100 round(s) of paste-url, drop-files`, `stress: 100 round(s) passed` (about 6.5 min). VERIFIED.
7. PR checks at 845997bb (gh pr view 460): static, static-windows, visual, viewer-graph, report, checks all SUCCESS; heavy jobs skipped as designed on a pull request. VERIFIED.
8. Body claim "before the fix the default stress failed twice at round 2 `frontmatter-title`": run 44899492187 at 7eeeb33f stress failure `stress round 2/11, scenario frontmatter-title: Edit mode did not switch to on`; second occurrence in work/ci-44899492187-b.log (same message). VERIFIED.
9. PR description (posted body equals work/pr-body.md except one blank line): renders (sections Summary, Deliverables, Changes, Impacts, Blast radius, Test plan; fenced trace block); no CR number, batch or agent role; Summary, Deliverables and Changes match `git diff --stat origin/main...HEAD` (15 files, all named; stressPlan intent change stated); unproven viewport cause stated in Impacts as unproven; the Test plan names the head the proofs ran at (pre-rebase carried, with its reason) and does not claim a default-plan run at 845997bb; no image. Review and CI green boxes are unchecked (not claims). VERIFIED.

Not proved here: Evidence 7 (after merge). Review box absent (unchecked), nothing to judge.

VERIFIED

## Description-only pass at 845997bb757b19f14b92a269672776160dde9455

Head: 845997bb757b19f14b92a269672776160dde9455

Checked `gh pr view 460 --json body`: sections present, no internal ids, SHA marks and run ids match gh run view (44903251073 and 44903254624 at 9fce844, 44905091608 and 44905104654 at d571951, 44904977842 at 845997b; all conclusions as stated), trace lines match, Known gaps match the diff (run.ts:210 literal 1400x900; dropFiles.test.ts:121 catch).
Failed claim: Test plan "Requirements: no behaviour change; `just requirements-update` reports no change" has no command or output in verify.md or the gate log (the gate runs `okfreq validate`, not `requirements-update`; the diff touches only requirements/tiers/log.md).

NOT VERIFIED
