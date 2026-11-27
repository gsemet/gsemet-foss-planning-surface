# CR-510: before and after

Before: `5a73b6ebcf66ef80b412afcdbfd09c4defc028d8` (base). After:
`7d35be3430689c4979a58f471d4cd588ecb93fac` (pushed head). No visual change (a CI script, its
tests, one guideline sentence), so the pairs are command outputs. `<worktree>` is the CR's
worktree, `<scratch>` a throwaway folder.

| Pair | Files | What it shows |
| --- | --- | --- |
| Head tests on both scripts | `tests-before.txt`, `tests-after.txt` | 19 pass at the head; with the base script, 4 new chain cases fail, the other 15 pass |
| Real forge chain of run 45741461955 | `real-chain.txt` (both) | base script lists the 10 chain merges and fails; head script passes, 24 commits |

## Reproduce

- After: in `<worktree>`, `uv run pytest test/build/test_no_merge_commits.py -v`.
- Before: `git worktree add --detach --no-checkout <scratch>/vbase 5a73b6e`; check out `justfile`,
  `pyproject.toml`, `scripts/check-no-merge-commits.sh`, `test/build/test_no_merge_commits.py`,
  `.github/workflows/ci.yml` and `.agents/guidelines/pull-request.guidelines.md` there; replace the
  test file by the head's; `uv run --project <worktree> pytest <that test file> --rootdir
  <scratch>/vbase -c <scratch>/vbase/pyproject.toml -p no:cacheprovider`.
- Real chain: `git clone --shared --no-checkout <worktree> <scratch>/clone`; fetch
  `refs/pull/516/merge` from the forge into it; set `refs/remotes/origin/main` to `17b779d5` and
  `HEAD` to `921754e3`; run each script from the clone with the argument `origin/main`.
