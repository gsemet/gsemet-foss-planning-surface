## Summary

The loops' timing was hard-coded in the cards: the steering session woke every 30 minutes (Claude Code) or 4 minutes (Copilot), and a CI job failed on the infrastructure was re-run once. This PR moves three settings into `chantier.yaml`, next to the models: `steering_wake`, `cache_ttl` and `ci_reruns`, per host and, inside a host, per column (Claude Code: `session` or `subagent`; Copilot: `claude` or `gpt` models), with a general value per host that each column may override. The shipped defaults keep today's behaviour. The board's Configuration page gets a read-only Timing tab, and the board's "late" heartbeat mark now follows the batch's steering wake.

## Deliverables

Before, the wake and the re-run count lived in prose. Now each is a configured value, resolved layer by layer (strongest layer first; inside a layer the column beats the general value) and printed as `timing:` lines:

```text
timing: Claude Code session: steering wake 30 min, cache TTL 60 min
timing: Claude Code subagent: cache TTL 5 min, CI re-runs 1
```

| Host | Setting | Shipped default |
| --- | --- | --- |
| Claude Code | steering wake / cache TTL / CI re-runs | 30m / 5m (`session`: 1h) / 1 |
| Copilot | steering wake / cache TTL / CI re-runs | 4m / 5m (unproved) / 1 |

- A setting a column never reads is refused under that column in `chantier.yaml` and shown "not used" on the Timing tab.
- A wake longer than its column's cache TTL prints a warning, never a refusal.
- A running batch keeps the timing it opened with.
- The Timing tab: one card per host, one value pill per column; a value set in `chantier.yaml` is teal with a dot, a shipped default grey.

Timing tab at 1680 px, after (captured at 17b1c6b, carried: no board file changed by the restack) and its design reference beside it (the reference's values are illustrative and its Driver wake row is not drawn):

![Timing tab after, captured at 17b1c6b](https://github.com/user-attachments/assets/12f74c83-5c8a-48da-a8e1-90604588edcd)
![Design reference](https://github.com/user-attachments/assets/301f9ff1-578f-437e-881c-3fd1f375a823)

## Blast radius

Grade: 2. Shared configuration reading, the batch record and the cards change; the defaults equal today's behaviour, so a project with no `timing:` block sees no change. Revert restores the previous behaviour; a record opened with a `timing` field simply ignores it afterwards.

## Autonomous decisions

- The reading and resolution live in new `playbook/timing.py` and `playbook/timing_check.py`, not in `layers.py` and `config.py`, to keep files under the 400-line limit.
- The Timing view is in a new `config-timing.js` and `config-timing.css`, to limit conflicts with the board's restyle of the Configuration page.
- `take stack` prints the `timing:` lines after the CR rows; `stack` prints none.

## Known gaps

- A Foreman on Claude Code scheduling its wake at a configured value, Copilot's `/every` at a configured value, and the idle stop with a wake shorter than 30 minutes are unproved until a real batch.

<details>
<summary>Details</summary>

## Changes

- `config/chantier.defaults.yml`: the shipped `timing` block.
- `playbook/timing.py`, `playbook/timing_check.py`, `playbook/config.py`: checks (units, bounds, columns, "not used" refusals with file and line) and per-layer resolution.
- `playbook/lines.py`, `commands/rules.py`, `commands/facts.py`, `commands/driver.py`, `commands/opening.py`, `core/records.py`: `timing:` lines and warnings in `playbook`, `take`, `round`, `handoff` and `take stack`; recorded in the batch record and its brief.
- `playbook/edit.py`, `board/state.py`, the board web files: `timing` in the configuration view, `steering_wake_min`, the Timing tab, the late mark (steering wake plus 5 minutes).
- Cards (`driver.md`, `foreman.md`, `concepts.md`, `chief-of-staff.md`, `hosts/claude-code.md`, `hosts/copilot.md`) and docs (`agents-and-models.md`, `hosts.md`, `use-cases-foreman.md`): the wake and re-runs follow the `timing:` lines; the idle stop is 30 minutes with no Driver, whatever the wake.
- Tests: `test_playbook_timing.py`; the scenario checks timing in the surface-board unit and the stack take.

## Human decisions

- Three settings only: steering wake, cache TTL and CI re-runs; every other wait or maximum stays where it is.
- Read-only Timing tab; values are set in `chantier.yaml`.
- On Copilot the steering wake reads the column of the Foreman's model family, else the general value.
- The Driver wake is a separate change.

## Impacts

The Timing tab is new; the late mark moves from 15 to 35 minutes by default on Claude Code (9 on Copilot).

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_playbook_timing.py`
- [x] Local gates: `just check` at 8ab3114 (422 passed); `just scenario` run locally on the commit before its rebase (carried from b888fc6); the pipeline job runs it at the pushed head (restacked; conflict resolved, inspector approved at `8ab3114`)
- [x] Evidence: before at b89e096 (no Timing tab), after captured at 17b1c6b, carried (screenshot above) (restacked; conflict resolved, inspector approved at `8ab3114`)
- [x] Review: approved at 8ab3114 (restacked; conflict resolved, inspector approved at `8ab3114`)
- [x] Verified at `8ab3114` (restacked; conflict resolved)
- [x] CI green at 8ab3114: `gh pr checks 276`, all five jobs pass, `just scenario (ubuntu-latest)` included (restacked; conflict resolved, inspector approved at `8ab3114`)

## Internal references

CR-320 timing-settings. Work files: `work/investigation.md`, `work/r1.md`, `work/r2.md`.

</details>
