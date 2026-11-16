## Summary

Chantier runs in any kind of project, and the last batch showed proofs being skipped and workers writing outside their worktree. This change makes the two proofs that matter mandatory at hand-back, and fixes several small frictions of the CLI, without making the rest of the process stricter.

## Deliverables

- `handback <cr> ready` now refuses unless, at the PR's head, the long gate passed and the last verdict is `VERIFIED`. A project with no long gate, or one that exempts the change, hands back with `--no-gate "<the project's rule>"`; the reason is logged and shown, and the verdict stays mandatory.

```text
verdict <cr> VERIFIED | "NOT VERIFIED"      (run by the Verifier, at the head it verified)
gate <cr> "<cmd>" ["<cmd>"...]              (one command per argument, same on every OS)
handback <cr> ready <link> [--no-gate "<rule>"]
```

- Claude Code only: a hook refuses a worker's Write, Edit or NotebookEdit outside its worktree and its CR folder.
- `take`, `round` and `handoff` list the two gates as a checklist at the PR's head.
- `order add` queues a CR on a running direct batch; a CR number may be given bare (`165`); `cost` shows the steering session's own subagents on their own line; `playbook` prints the spec-writer's first prompt line.
- The README has a new "Your gates" section for any project.

## Blast radius

Grade: 2. The CLI's hand-back path and the Claude Code hook change; a revert restores the old behaviour. The hook's engine shapes are not proved on a real session.

## Autonomous decisions

- The hook records a worker only after its spawn resolves; the spawn-to-first-call race could not be checked against the engine's types (not available here).
- Fixed README and card lines that said a running direct batch refuses `order add`, since part 3 made them false.

<details>
<summary>Details</summary>

## Changes

- `hooks/register.tsx`: worker write guard; tests in `hooks/register.test.tsx`.
- CLI (`cli.py`, `commands.py`, `state.py`, `status.py`): `verdict`, the new `handback` refusals and `--no-gate`, multi-command `gate` with a run id, the CR-number normaliser, `order add` queueing, cost grouping, `agents set O-<k>`, `playbook` line.
- Cards, README, tutorial, CONTRIBUTING and the scenario follow.

## Human decisions

- The hook refuses (it does not only warn), for workers only and for their Write and Edit.
- The Verifier records its own verdict; `NOT VERIFIED` is recorded too and the last verdict at a head decides.
- A project with no long gate hands back with `--no-gate`; the steering session checks it; no setting is added to `chantier.yaml`.
- A QA driver keeps its own line in `cost`.

## Impacts

No visual change. Drivers must run the gate and have a verdict before `ready`.

## Test plan

- [x] New or changed tests (structure tests, hook tests) at `adf7d7a`; hook tests not run on the author's machine (no `claude` CLI): **UNVERIFIED by running**
- [x] Local gates at `adf7d7a`: `just check && just scenario` pass
- [x] Evidence: none visual
- [x] Review: approved at `adf7d7a`
- [x] Verified at `adf7d7a` (first pass at `1579dac` found the hook guarding Drivers, fixed in `adf7d7a`)
- [x] CI green at `adf7d7a` (three `just check`, `just scenario`)
## Internal references

CR-171 batch-09-retro-fixes.

</details>


