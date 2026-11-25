# Conflicts: CR-103 rebased on CR-102

- Rebase: `6572527608200cb688c0ae0224427e8b8bb44539` replayed on
  `125952dc04a949cc78810e2340ef57d9ffa6ba5e`
  (`origin/chantier/batch-01/cr-102-index-no-broken-links-in-subdirectory-su`).
- New head: `a2723b7a0cdea34d9fe3601f3081b21ea424d07d`, branch
  `chantier/batch-01/cr-103-show-print-the-stored-file-new-trust-com`, one commit, same message
  and author. Tree clean. Nothing pushed (the branch now diverges from its remote).
- `CHANGELOG.md` is not changed by the commit.

## Hunks

### `requirements/tiers/log.md`, under `## 2026-11-25` (one hunk)

- Base side (CR-102): entry `### Index summaries and broken links`.
- Commit side (CR-103): entry `### Show prints the stored file, and a trust command`.
- Choice: both entries kept, text unchanged. CR-103's entry is first (newest on top), then
  CR-102's, then the older entries. A line count against the ancestor and both sides shows no
  line missing and none extra.

### `skills/okf-schema/SKILL.md`, CLI Reference table (one hunk)

| Row | Taken from | Reason |
|-----|-----------|--------|
| `show` | CR-103 | Base side left this row as in the ancestor; CR-103 rewrote it |
| `trust` | CR-103 | New row |
| `index` | CR-102 | CR-102 extended it; CR-103 left it as in the ancestor |
| `stats` | CR-102 | Same |

The other CR-103 change in this file (`trust` in the bundle management list) merged on its own.

Neither resolved file gained a byte-order mark; both start as before and use LF.

## Checks

Fast gate: the project's rules define none. `just preflight` was not run, as the Driver asked.

Run in the worktree on the resolved tree, before `git rebase --continue`:

| Command | Result |
|---------|--------|
| `uv run -- okfreq update-coverage requirements --check` | `0 files would change` |
| `uv run -- okfreq validate requirements --prose --check-links --project-root .` | `36 requirements, 0 errors, 0 warnings` |
| `uv run -- okfreq lint requirements --check --check-links --project-root .` | `0 indexes would change`, `0 requirement OKF projections would change` |
| `uv run -- pytest tests/test_acceptance_core.py tests/test_api.py tests/test_cli_remaining.py -q` | 278 passed, 7 skipped; exit 1 only because the project-wide coverage threshold (95%) applies to this partial run (35%) |
| `uv run -- pytest tests/test_acceptance_core.py tests/test_api.py tests/test_cli_remaining.py tests/test_cli_core.py --no-cov -q` | 325 passed, 7 skipped, exit 0 |

The 7 skipped tests are all in `tests/test_acceptance_core.py`. `tests/test_cli_core.py` is not
touched by this commit; it was added because CR-102 changed it.

## Note

The CR-103 log entry's verification line (`1185 tests pass and 12 are skipped`, Python 3.12)
records the run made before the rebase. It was left as written; `just preflight` has not been run
on the rebased head.
