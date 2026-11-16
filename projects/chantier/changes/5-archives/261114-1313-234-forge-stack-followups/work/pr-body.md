## Summary

Five gaps were left by the work that checks forge permissions at the start of a batch and by the work that lets a stack change after it is ready. This PR closes them so that the code does what those changes promised:

- `preflight` finds the `gh stack` extension by asking `gh extension list`, not by looking for a folder, so an install anywhere is found.
- The card says what P10's `<k> of <n>` counts (commands, not rules), which explains why a count of 14 of 16 is not comparable with the earlier 19 of 19.
- `forge-stack rebuild` exits 4 and prints what it already did when a stack is still open after its five unstack tries, as it does for any other forge refusal (it exited 2 and dropped that list).
- `ship`'s scan of `work/pr-body.md` for stale commits no longer reads an all-digit token (a PR number, a date) as a commit.
- The scenario step for a stacked CR whose `after` keeps its old base after an insertion is shown to fail on the code before the stack work.

## Deliverables

Before and after, for the one visible line and the exit code (the scenario's new steps run against a fake `gh`):

| | Before | After |
| --- | --- | --- |
| `gh stack` detection | a `gh-stack` folder under `$XDG_DATA_HOME` or `%LOCALAPPDATA%` | `gh extension list` names `github/gh-stack` (or `gh stack`) |
| `rebuild`, stack stays open after 5 tries | exit 2, the list of done steps lost | exit 4, `stack #<n> is still open after 5 unstack tries (the forge reads it back with #<a> #<b>)` after the done steps |
| stale-SHA scan | `20261113` tried as a commit | only a token with a letter `a` to `f` is tried |

The scenario with the old `_stack_base` body (from before the stack work) put in place of the current one, run on this PR's code otherwise, fails two checks; the current code passes them (the full gate passed at 756a387, carried for this comparison, which touches `_stack_base` only; the scenario at 9bd0412 rests on GitHub CI):

```text
FAIL a stacked CR with an `after` sits on the CR under it in the stack (`stack` with no CR and `take stack` print the same base), and the CR above it sits on it
FAIL `ship` records the stack place as base for a stacked CR that has an `after`
github: 698/700 checks passed        (old _stack_base)
github: 700/700 checks passed        (current code, `just scenario` at 756a387, carried; CI runs it at 9bd0412)
```

`$CHANTIER preflight` on the user's real settings, on Windows, now finds the extension through `gh extension list` (`gh stack  github/gh-stack  v0.3.0` here) and reads `P10 warn every batch: 1 of 14 commands` at 9bd0412, and with `preflight --mode stack` also `P10 ok   a stack` (main made P10 per capability and dropped the release groups; the first run at 756a387 read 2 of 16).

## Blast radius

Grade: 1

The changes are a detection in `preflight`, an exit code and a message in `forge-stack rebuild`, a narrower regular expression in `ship`, and a card paragraph. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The all-digit rule is a lookahead in the pattern, so a 7-character abbreviation made only of digits (about 1 in 27) is not checked; the specification's default.
- The scenario's old-head commit is re-amended until its SHA holds a letter, since the new rule would otherwise skip it in about 1 run in 27.
- `_rebuild` got a docstring carrying the specification's sentence (it had none).
- The stuck `rebuild` scenario step uses the stuck stack alone; a second stack that unstacks normally first was too costly to set up.

## Known gaps

- The stuck `rebuild` step proves `is still open after 5 unstack tries` and the idempotent second run, but its first stderr has no `unstacked #<n>` line, since no earlier stack is unstacked in that step.
- No local long gate at 9bd0412 (user waiver 2026-11-14); GitHub CI runs `just scenario` there.
- `scenario/run_scenario.py` is far over 400 lines already; this PR does not split it.
- The new `scenario/README.md` bullets are single long lines, and a constant's comment in `permissions.py` sits one line above where it reads best: both cosmetic.

<details>
<summary>Details</summary>

## Changes

- `commands/permissions.py`: `_gh_names_stack` runs `gh extension list` once (10 s timeout, `check=False`); the gh-stack forge (the stack capability) applies when it exits 0 and names `gh stack` or a repository ending in `/gh-stack`. The folder test is gone. A comment above `SAMPLES` says P10 counts commands.
- `commands/forge_stack.py`: `UNSTACK_TRIES`, and the stuck-stack error is raised with exit 4 and a text naming the tries and what the forge still holds.
- `commands/delivery.py`: a token is read as a commit only when it holds a letter `a` to `f`.
- `skills/chantier/references/hosts/claude-code.md`: what P10's count counts; the `gh stack*` row says `gh extension list`.
- `scenario/`: `fake_gh.py` answers `extension list` and has an `unstack_ignored` flag; `run_scenario.py` gains the P10, stuck rebuild and all-digit SHA steps; `README.md` lists them.

## Impacts

No visual change. `preflight` asks `gh` once more; a missing or failing `gh` reads as no extension (the forge check reports `gh` itself).

## Test plan

- [x] New or changed tests: the scenario steps above fail on the previous code
- [x] Local gates: `just check` and mypy strict on windows, linux, darwin pass at 9bd0412; `just scenario` pass on both forges at 756a387, carried for `forge_stack.py`, `delivery.py`, `fake_gh.py` and the `_stack_base` comparison (unchanged since); the rebase changed `permissions.py` and the P10 scenario step, which rest on GitHub CI at 9bd0412; no local long gate at 9bd0412 (user waiver 2026-11-14), the scenario at 9bd0412 rests on GitHub CI
- [x] Evidence: before at e54e299, after at 756a387, carried to 9bd0412 (the old `_stack_base` run and the current run above)
- [x] Review: approved at e54e299 plus the diff committed as 756a387; carried to 9bd0412, whose second rebase adapted `_forges` in `permissions.py`, the P10 scenario step (`--mode stack`), the card paragraph and the README to main's per-capability P10: that adaptation has no separate review, the Verifier read it at 9bd0412
- [x] Verified at `9bd0412`
- [x] CI green at `9bd0412`: `gh pr checks 175` lists check (macos, ubuntu, windows), eval-dry-run and scenario, all pass

## Internal references

- CR-234 forge-stack-followups; evidence under `work/coder/` (`area5-old-stack-base.log`, `area5-current.log`, `gitlab-current.log`) and `work/preflight-real-settings.log` (the 756a387 run, `2 of 16`; the 9bd0412 reading is in Deliverables).

</details>
