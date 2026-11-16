## Summary

Running an eval campaign needed the maintainer's sandbox repository, a hard-coded name, and knowledge that lived in people's heads: how to start the operator's session, which host automations to turn off, and which staging steps to do. This PR makes the `evals/` folder self-sufficient: a person with this repository and their own GitHub account can create a sandbox, stage `real-foreman` and start it by following `evals/README.md`.

## Deliverables

- One place names the sandbox: `evals/kit/sandbox.local.json` (git-ignored) when present, else the maintainer's repository in `evals/kit/sandbox.json`. Every command prints the repository and where it was read from on its first line.

```text
sandbox.py publish <owner>/<name> [--yes]   create a public empty sandbox, push the base, write sandbox.local.json
sandbox.py reset                            now refuses an empty repository, or a main/branch that does not hold the recorded base
setup.py <campaign> <workspace>             prints the operator's `prompt` line, ready to paste
```

- `evals/README.md` gains a "Prerequisites" list, the two ways to start the operator's session on Claude Desktop with the trust step, the host's PR automations to turn off, "Auto-fix during the run", a check for a board left running, and the rule that the report's cost is read after `close`.
- Each sandbox runbook has a "Start" section with the same prompt text that setup prints.
- Impactful choices: the sandbox is public only; `reset` stays safe because it refuses anything whose history lacks the recorded base; the mode stays a blank to fill in the prompt.

## Blast radius

Grade: **1**. The eval kit, its documentation, and two bullets of the Claude Code host card; the CLI and the product do not change. A `git revert` restores the previous behaviour.

## Autonomous decisions

- The dry run's fake `gh` reads the repository name from `$SANDBOX_FORGE_REPOSITORY` first, because it runs as a process of its own and the dry run needs a handle on it; outside the dry run it takes the name from `sandbox.py` only.

## Known gaps

- No real campaign was run: that a person who never ran one can stage and start `real-foreman` from the README alone is proved only by the next real campaign.
- The operator's `mcp__ccd_pr__set_monitor` call on a run's pull requests is proved only by the next real campaign; the global Auto-fix setting is marked unproved in the README and the host card.

- Two long lines (the README's "Auto-fix during the run" bullet and one sentence of the host card) are not wrapped like their neighbours; cosmetic, left as they are.

<details>
<summary>Details</summary>

## Changes

- `evals/kit/sandbox.py`: one reader of the repository name, `publish`, the new `reset` refusals, `build --record` keeps the committed `repository` field.
- `evals/kit/setup.py`, `judge.py`, `sandbox_forge.py`: take the name from `sandbox.py`; setup prints the `prompt` line and allows `mcp__ccd_pr__set_monitor` in the workspace settings of campaigns that open pull requests.
- `evals/kit/dry_run.py`: new cases `other-sandbox`, `reset-foreign`, `reset-empty`, `publish`, `setup-prompt`; the real `sandbox.local.json` is never read.
- `evals/README.md` and the runbooks; `.gitignore`; `skills/chantier/references/hosts/claude-code.md` (Auto-fix events and the `set_monitor` note in Configuration only).

## Human decisions

- The eval operator turns Auto-fix off itself on each pull request of a run, only on the run's own sandbox pull requests.
- A person's sandbox is named by one git-ignored file, `evals/kit/sandbox.local.json`; public sandboxes only.
- The operator's mode stays a blank to fill in the printed prompt; setup takes no `--mode`.

## Impacts

No visual change. Contributors running evals get a self-contained guide.

## Test plan

- [x] New or changed tests (they fail on the previous code): dry-run cases listed above
- [x] Local gates at `782385d`: `just check` (200 tests passed), `just eval-dry-run` (16 of 16 cases passed)
- [x] Evidence: none visual (the dry run covers the new behaviour)
- [x] Review: approved at `782385d`
- [x] Verified at `782385d`: `just check`, `just eval-dry-run` (16 of 16 cases), a read-through of the README's commands
- [x] CI green at `782385d`: `gh pr checks 243`: check on three systems, eval-dry-run and scenario pass

## Internal references

- CR-293 "The evals folder is self-sufficient: anyone can run a campaign from it" (batch-18)
</details>
