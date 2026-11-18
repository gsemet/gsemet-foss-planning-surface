## Summary

Three checks failed only on a loaded machine and cost reruns: the scenario's reused-pid check (local Windows gate), an autosync test with a 1 s wait (macOS), and a mypy wheel download timeout in CI's macOS `just check`. This PR gives each a margin that does not depend on how fast the machine is, and retries the CI tool download once.

## Deliverables

| Where | Before | After |
|---|---|---|
| Scenario sleeper (reused-pid block) | sleeps 120 s | sleeps 600 s |
| Lock and stale queue ticket time | `now - 10 s`, written after the sleeper started | `born - 60 s`, `born` being the sleeper's own creation time read with `psutil` |
| "runs at once" bound | `< 10` s | `< 60` s |
| `test_board.py` autosync waits | `timeout=1` / `3` | `timeout=60` (each returns as soon as its condition holds) |
| CI `check` job | `just check` only | `just tools \|\| just tools`, then `just check` |

```just
# Fetch the pinned check tools into the caches, running nothing (CI runs it before `check`, retried once)
tools:
    uv sync --locked --group dev
    uv run --locked --group dev --with {{mypy}} --with types-psutil mypy --version
    uvx {{ruff}} --version
    uvx --from {{node}} npx --yes {{biome}} --version
```

## Blast radius

Grade: **1**. Test and CI scaffolding only (scenario, one test file, a justfile recipe, one CI step); no shipped code changes. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The other short autosync waits (`observe_join(timeout=3)`, `watcher.join(timeout=3)`, `proc.wait(timeout=3)`) also go to 60 s, since each returns when its condition holds and none gets slower on an idle machine.
- The retry covers only the tool and wheel fetches of `just tools`; `just check` itself is not retried, so a failing test still fails the job.
- The failing scenario run's detail was not kept, so the sleeper-creation-time cause is the probable one; the sleeper's 120 s life, a second possible cause, is removed too.

## Known gaps

- A real download timeout and its retry cannot be provoked; the retry is proved by its shape (`||`) only.
- A network read inside `just check` itself (for example `uv lock --check`) is not retried.

<details>
<summary>Details</summary>

## Changes

- `scenario/run_scenario.py`, `rails()`: sleeper sleeps 600 s; `born` read right after it starts; the lock and the stale ticket (name prefix and mtime) are dated `born - 60`; the "runs at once" bound is 60 s. No check's text, order or count changes.
- `skills/chantier/scripts/cli/tests/test_board.py`: four autosync tests use 60 s waits; the `0.01` s waits that are the condition under test stay.
- `justfile`: new `tools` recipe using the existing tool pins.
- `.github/workflows/ci.yml`: a bash step "Fetch the check tools (retried once)" before `just check`.

## Impacts

No visual change. Fewer spurious reds under load; CI's `check` job gains one step.

## Test plan

- [x] New or changed tests (they fail on the previous code): the four changed autosync tests keep proving the same diagnostics with a larger margin; `just test -k test_join`: 4 passed, carried from `d171065` (clean rebase onto CR-349, head `c6da18b`)
- [x] Local gates: carried from `d171065` (`just check` pass (565 passed); with a new empty `UV_CACHE_DIR`, `just tools` then `just check`: both pass; local Windows `just scenario`: exit 0, the four reused-pid checks ticked; clean rebase onto CR-349, head `c6da18b`)
- [x] Evidence: the CI log of the `check` jobs at `c6da18b` shows the new step running `just tools || just tools`
- [x] Review: carried from `d171065` (clean rebase onto CR-349, head `c6da18b`)
- [x] Verified: carried from `d171065` (clean rebase onto CR-349, head `c6da18b`)
- [x] CI green at `c6da18b`: `gh pr checks 311`: `just check` on ubuntu, macOS and windows, `just eval-dry-run`, `just scenario (ubuntu-latest)` pass

## Internal references

CR-350 timing-checks-margin (batch-24).

</details>
