# Verify CR-284

VERIFIED

Head: fc55ab07d37a9275a7e0292827982c3c6c5c96d3

- just eval-dry-run: 11 of 11 as expected, incl. audit-cos-prompt (J1), audit-claim-call (J14), audit-heredoc (J26), each with planted FAILs; evidence/dry-run.log
- just check: pass (190 tests); evidence/check.log
- diff touches only evals/kit/audit.py, dry_run.py, evals/README.md (row lists the 3 cases)
- CI: 5 of 5 jobs pass; Known gaps are honest

## Description pass at fc55ab0

VERIFIED. Posted PR 232 body equals work/pr-body.md (trailing newline only); SHAs fc55ab0, 9d4136c, bb3e97e resolve; no CR name or path outside "Internal references"; title clean.
