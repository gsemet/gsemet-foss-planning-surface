# Verify CR-318 (restack)

Head: e0e60c8719efc3db283d0256c3e3a885c7d60ba1

Previous verdict at b9daeff (VERIFIED). Move: restack onto CR-317 head 0bd9d9c, one conflict in chief-of-staff.md. The base changed activity-adjacent files (batch_status.py, scenario/run_scenario.py, foreman.md, concepts.md, claude-code.md, copilot.md), so the behaviour and card claims are judged again, not carried.

Claims
- Resolved file, judged at e0e60c8: `git diff 0bd9d9c HEAD -- chief-of-staff.md hosts/copilot.md` shows the Resume bullet keeps CR-317's sentence (cleared-id Driver and replaced Foreman are never a close blocker) and appends the CR-318 direct-batch sentences; the dropped `close --stopped` sentence was obsolete. Coherent, no conflict marker. PASS.
- CI at the head: `gh pr checks 273`: just check (ubuntu, macos, windows) pass, eval-dry-run pass, `just scenario (ubuntu-latest)` PENDING (not finished). FAIL as proof: the qa-driver behaviour (flag, restart, no round counted) is not proved at e0e60c8. I tried `just scenario --unit qa-driver` locally; the permission system denied the command, so it was not run and no workaround was used. The 68/68 result in work/verifier/qa-driver.log is from b9daeff, and the base moved scenario/run_scenario.py and batch_status.py, so it is not carried.
- PR description Review box (`gh pr view 273 --json body`, line 62): `Review: approved at 8f2b9cf, committed as edd01d7, carried from edd01d7 over a clean rebase to b9daeff`. The head is now e0e60c8 after a restack whose patch changed (range-diff b9daeff..e0e60c8 shows hunk changes in run_scenario.py, chief-of-staff.md, batch_status.py). No note of an approved pass at e0e60c8; the box is stale. FAIL.
- Not re-run (carried from b9daeff: reader code stopped.py, activity.py untouched by the conflict, timing is reader-only): reader timing.

Failed: scenario at e0e60c8 not proved (CI pending, local run denied); Review box does not cover e0e60c8.

NOT VERIFIED

## Second pass at e0e60c8719efc3db283d0256c3e3a885c7d60ba1

Head: e0e60c8719efc3db283d0256c3e3a885c7d60ba1

- CI at e0e60c8 (`gh pr checks 273`): just check macos/ubuntu/windows pass, just eval-dry-run pass, just scenario (ubuntu-latest) pass (3m29s); this runs the qa-driver unit at the head. `gh pr view 273 --json headRefOid` = e0e60c8719efc3db283d0256c3e3a885c7d60ba1. PASS (fixes the earlier pending failure).
- Review box: `$CHANTIER log CR-318` holds "move b9daeff..e0e60c8 (restack) inspector approved at e0e60c8"; the posted box cites e0e60c8. PASS.
- PR description (`gh pr view 273 --json body`): renders, Summary/Changes match the earlier-judged diff, no STALE mark, Known gaps lists the unproved items, no image. PASS. Note: the "68/68 local" line is the CI scenario's coverage at the head, not a local run.
- Claims carried from the first pass (resolved chief-of-staff.md merge, reader timing): unchanged since that judgment, no new move.

VERIFIED
