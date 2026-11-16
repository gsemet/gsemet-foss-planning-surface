# verify CR-103 at 2353e61e9eaf83ab0e66a5f9c65baa6cf123b8cc

Throwaway repo, Windows PowerShell 5.1, worktree CLI (lifecycle.py, commands.py, cli.py changed).

- PR 27: draft=True, open, head matches, body line 1 is exactly the required text. CI: just check passes on macOS, Ubuntu, Windows.
- `open b1 .agents\changes\1-inbox\fix-login` (unquoted): "opened b1 ... 1 CRs", exit 0.
- `open b1 .agents/changes/1-inbox/nope`: "error: prepared CR not found: <abs path>\.agents\changes\1-inbox\nope", exit 1 (names the path).
- `open b1 "@.agents/changes/1-inbox/fix-login"`: "prepared CR not found: ...\@.agents\..." exit 1 (@ is just a path).
- `order add - --note .agents\changes\1-inbox\raw-request`: "added CR-102, queued", exit 0.
- `order add - --note "@.agents/..."`: prepared CR not found, exit 1. Wrong plain path: names the path, exit 1.
- `file "@req.txt"`: "filed .agents/changes/1-inbox/raw-request", exit 0 (@file kept; quoted since PowerShell treats bare @name as splatting).
- Diff review: no remaining "@<folder>" wording in README, CONTRIBUTING, cards, runbooks (git grep); chief-of-staff.md keeps only `file ... @<file>`. evals/results untouched. Tests and scenario updated.
- Not rerun locally: `just check`/`just scenario` (CI green on 3 OSes at this head).

VERIFIED
