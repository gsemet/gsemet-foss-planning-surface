# CR-106 verify

Head: 668e002b9f93797daf383cd3e08b000ef5bc6073 (worktree HEAD and PR 41 headRefOid agree; worktree clean).
Method: the real CLI from that worktree, in a throwaway git repo (bare origin) outside this project.
Full transcript: `cli-run.txt` (script run with `verify.ps1` from the scratchpad). The "spent" state is set by editing
`batch.json` (`spent_usd: 2`, budget 1), as the scenario does.

| Claim | Command and output | Result |
|---|---|---|
| Spent budget refuses `order qa` with EXIT_BUDGET, no folder, no order, no event | `order qa --note ...` -> `error: budget spent: $2.00 of $1.0; only the user raises it (order budget)`, exit=5. Before and after: qa folders 0, orders=0, events lines=2 | ok |
| `order budget` lets it through | `order budget --note 10` exit 0; `order qa` -> `order O-2: qa .agents/changes/1-inbox/qa-261105-1757`, exit 0; qa folders 1, orders=2, events 4 | ok |
| Within budget (5, spent 0) behaves as before | `order qa` -> O-1 created, folder made, exit 0; events 3 | ok |
| No budget behaves as before | `order qa` -> O-1 created, folder made, exit 0; events 3 | ok |
| PR is a draft, not auto-merge | `gh pr view 41`: isDraft true, autoMergeRequest null, state OPEN | ok |
| Body first line exact | `**Eval run: do not merge.** The maintainer decides what happens to this PR.` | ok |
| Diff scope | commands.py: +1 line `check_budget(b)` in the `qa` branch, before `_new_request`; scenario check added | ok |

I did not rerun `just check` or `just scenario` (reported green by the gate and CI).

VERIFIED
