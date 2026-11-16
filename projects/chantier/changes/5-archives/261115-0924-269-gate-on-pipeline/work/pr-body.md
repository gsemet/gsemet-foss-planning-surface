## Summary

The local long gate (`just scenario`) was timed by the maintainer at 573 s on a quiet Windows machine, and the long gates run one at a time, while the same scenario job was timed at 1 min 43 s in the forge pipeline (the maintainer's figures, not re-measured here). This PR lets a project's rules name a pipeline job as its long gate ("green at the PR's head"), so a Driver waits on the forge instead of on the local lock. This project adopts it: its long gate becomes the pipeline's `just scenario (ubuntu-latest)` job, and the stack's top still runs `just scenario` locally once per batch for Windows coverage. Cards and docs only; the CLI does not change.

## Deliverables

The rule, as the cards now state it (the Driver is chantier's role that takes one change to a pull request; the Foreman, or the Chief of Staff in direct mode, is the steering session that receives its hand-back):

| Step | Before | After (rule names a pipeline job) |
| --- | --- | --- |
| Driver, after the approved round | `gate` locally, then push | no `gate`; push and open the PR |
| Wait | local lock, one gate at a time | the job green at the PR's head on the forge |
| Hand-back | `ready <link>` | `ready <link> --no-gate "<the rule>"` |
| Steering session | checks the recorded gate | reads the job at the PR's head (`gh pr checks <pr>`) and sends the CR back if it is not green |

This project's rule (`AGENTS.md`): the pipeline's `just scenario (ubuntu-latest)` job is the long gate; the CR on top of the stack also passes `just scenario` locally before the user merges.

## Blast radius

Grade: **1**. Text of cards and docs only; a plain `git revert` restores the local-gate rule.

## Autonomous decisions

- The existing sentence in the concepts card that said `--no-gate` is for a project with none or an exempted CR also names the pipeline-job case, so no card contradicts the new rule.

## Known gaps

- The pipeline-job path is unproved on GitLab and on the Copilot host; the cards carry the mark.
- The board and `STATUS.json` still show a `--no-gate` CR as `exempt: <rule>`.
- The decided carrier of the local Windows run in a batch with no stack (the last PR the user will merge) is not written in this project's rule, which names the stack's top only.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/concepts.md`: the definition of a pipeline job as the long gate.
- `skills/chantier/references/driver.md`: the Driver runs no `gate`, waits for the job, hands back with `--no-gate`; "Your end" accepts the pipeline case.
- `skills/chantier/references/foreman.md`: the steering check reads the job at the PR's head, and sends back the stack's top handed back with `--no-gate` when a local run is asked.
- `skills/chantier/references/chief-of-staff.md`: the two consistency edits (the no-long-gate check, the routed force-push judgement).
- `docs/gates.md`: the user's page, with the example line.
- `AGENTS.md`: this project's rule.

## Human decisions

- The change works the same on both hosts (Claude Code, GitHub Copilot) and both forges (GitHub, GitLab); a path not proved on Copilot or on a real GitLab carries the mark "unproved" in its card line.
- Windows coverage: one local `just scenario` per batch on the stack's top before the user merges, with no Windows leg in CI for now; with no stack, the last PR the user will merge carries it.
- The CLI does not change: the cards carry the generic rule and the project's instruction file carries the job's name.
- This change's own long gate is still the local `just scenario`, as the rule in force before it merges.

## Impacts

No visual change. Maintainers of this project wait on the pipeline job instead of the local gate.

## Test plan

- [x] New or changed tests: no behaviour change (cards and docs only)
- [x] Local gates at `dc13efe`: `just check` (pass, before the commit), `just scenario` (pass)
- [x] Evidence: none (text change); the edited card lines read and compared, at `dc13efe`
- [x] Review: approved at `dc13efe`
- [x] Verified at `dc13efe`
- [x] CI green at `dc13efe`: all five checks pass, including `just scenario (ubuntu-latest)`

## Internal references

- CR-269 gate-on-pipeline

</details>
