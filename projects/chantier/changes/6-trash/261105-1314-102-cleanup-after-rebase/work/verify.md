# verify CR-102
Head: 6c56d0fc547f81365192db9d8cfdbc0e6b286c0b (PR 25: OPEN, draft, no auto-merge, first body line exact)

1. No card tells an agent to use git branch -d: `git grep -E 'branch -d([^a-z]|$)'` at head returns nothing; foreman.md:32, chief-of-staff.md:122,155 use -D.
2. Throwaway proof rerun by the verifier (evidence/verifier_rerun.out.txt): -d refused ("not fully merged") after rebase merge; worktree remove + branch -D removed the branch. Note: the forge's "PR merged" check is stood in for by a local rebase merge pushed to a bare remote.
3. just check: 25 passed, exit 0 locally; gh pr checks 25: macos, ubuntu, windows all pass.

VERIFIED
