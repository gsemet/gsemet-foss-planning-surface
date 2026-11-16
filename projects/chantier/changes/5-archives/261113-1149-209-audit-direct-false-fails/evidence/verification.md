CR-209 verification at 8821eb0
1. just check: 50 passed, release-notes ok (local); CI green (check x3, eval-dry-run, scenario). just eval-dry-run: 6 of 6.
2. run1_recheck.py before (audit_before.py): 3 J3 worktree FAIL, J3 run3.py FAIL, C9 FAIL, J14 FAIL. After (worktree audit.py): 3 J3 PASS, C9 PASS, run3.py and J14 still FAIL.
3. lawful_worktree synthetic: verifier --detach / -d pass; verifier non-detached, chained second non-detached (; and &&), coder/investigator detached all fail.
4. Direct: status --refresh no epoch passes, take no epoch fails; Foreman: status --refresh no epoch fails.
5. PR body matches diff and spec. Tracking boxes (Verified, CI at sha7) are the Driver's to tick.
