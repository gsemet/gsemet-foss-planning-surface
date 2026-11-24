## Summary

Own CR branches: a rebase of a `chantier/*` branch and its `--force-with-lease` push are chantier's normal flow, pre-authorized by the playbook. P10 names the rebase allow rules (once per machine, on the user's yes); the Foreman and the Chief of Staff answer a refused rebase or force push of a covered branch themselves; a push of any other branch is never run; a Driver's prompt carries a `Rewrites:` line naming the action and its scope.

## Deliverables

- `allow_samples.py`, `permissions.py`: the rebase samples and rules, the remote fill of ` origin/`.
- `driver_prompt.py`, `commands/driver.py`: the `Rewrites:` line.
- Cards: `hosts/claude-code.md`, `chief-of-staff.md`, `foreman.md`, `driver.md`, `conflict-resolver.md`, `routing.md`, `concepts.md`.
- Tests: `test_rebase_rules.py` (new, holds the preflight and matching asserts), `test_driver_prompt.py`; scenario P10 step and README.

## Test plan

- [x] `just check` at e17cd34: 2288 passed
- [x] `just eval-dry-run` at e17cd34: 19 of 19
- [~] long gate `scenario`: waived by the user for this CR (order O-20, 2026-11-23); CI ubuntu scenario at the head
- [ ] Verifier

## Known gaps

- The classifier's effect on the `Rewrites:` line is unproved; the trial is recorded in `hosts/claude-code.md`, "Auto mode".
- The `--exec`/`-x` ban is not in `driver.md` (its cr-driver reading is at its byte limit); it stays in `conflict-resolver.md`, `concepts.md` rule 8 and the `Rewrites:` text.
- The preflight warn asserts are in `test_rebase_rules.py`, not `test_cli_runs.py` (size limits).
- Rebased onto main with CR-465's commits (conflicts in `concepts.md`, `conflict-resolver.md`, `driver.md` resolved keeping both intents).

