## Summary

A change request that keeps failing used to escalate to a stronger model only when its last review was still "fix required"; a red CI job, a gate broken after a rebase or a failed verification never escalated, and the escalation model was a fixed name in the CLI. Now every `blocked rounds:` hand-back escalates the next rounds' Coder, a CR that still fails once escalated stops and goes to the user, and the escalation model is a per-host, per-role setting of the configuration, shown and edited like a role's model.

## Deliverables

Escalation model per role and host, in `config/chantier.defaults.yml`, overridable in a project's `chantier.yaml` and on the board's Configuration page:

```yaml
hosts:
  claude:
    roles:
      coder: { escalation: claude-opus-5-5 }   # also debugger, conflict-resolver
```

| Before | After |
| --- | --- |
| `ESCALATION = {"claude": "claude-opus-5-5", "copilot": None}` fixed in the CLI | `escalation` role key, accepted only on a role whose shipped defaults carry one |
| One `escalate:` line, read live | `escalate:` line and `escalation=` on role lines, read from the batch's recorded map with `--batch` |
| Five triggers, "once per trigger" | Four triggers, "once per CR, then the user" |

Choices: only the roles that write code escalate (`coder`, `debugger`, `conflict-resolver`); judging agents and Drivers never do. On Copilot an escalated role starts as a generic agent with the configured model; a role carrying the user's own agent does not escalate there.

## Blast radius

Grade: 2. Configuration validation, the batch record and the printed playbook lines change, and so do several cards; revert is possible but a batch opened with the new record keeps its map.

## Autonomous decisions

- The escalation map entries carry both the model's value on the host and its start mode (`named` or `generic`), to print the start as the specification asks.
- The size gate forced splitting the new code into `playbook/escalation.py` and its tests into `test_playbook_escalation.py`.

## Known gaps

- **UNVERIFIED:** the board's Escalation column is not proven in a browser at the head (carried from an earlier head); the Copilot generic start was proven by a probe of `take`, `round` and `handoff`, not in a real Copilot session.

<details>
<summary>Details</summary>

## Changes

- `playbook/config.py`, `layers.py`, `escalation.py`: the `escalation` key, its validation, its resolution from the shipped defaults then the user layers.
- `commands/opening.py`: `open` records the effective map in the batch record; `playbook --batch` reads it.
- `plugin_files.py`, `driver_prompt.py`, `commands/facts.py`: a role's contract lines print also when its escalation starts as a generic agent (Copilot), including the shipped-default escalation of the batch's recorded map, with no user `chantier.yaml`; on Copilot `take` then also prints the conflict-resolver's and the debugger's contracts, once per role.
- `playbook/lines.py`, `commands/rules.py`: `escalation=` on role and `team:` lines, one `escalate:` line.
- `playbook/edit.py`, `board/web/js/views/config.js`, i18n files: an Escalation column on the Configuration page.
- Cards and docs: the "Escalation" section rewritten; the Driver, Foreman, Chief of Staff and host cards, user docs and the eval scorecard follow; `AGENTS.md` names the board's editing of escalation.

## Human decisions

- A `blocked rounds:` hand-back, whatever its cause (red CI job, gate broken after a rebase, failed verification, review asking for fixes), escalates the next rounds' Coder once the user grants rounds.
- Only the roles that write code escalate (`coder`, `debugger`, `conflict-resolver`); judging agents and Drivers keep their model.
- The escalation model is a per-host, per-role configuration setting, shown and edited on the board like a role's model; on Copilot the escalated role starts as a generic agent with that model.
- A CR already escalated that fails again stops and goes to the user (one more round, drop it, another approach); no further round without the user's answer.

## Impacts

No visual change outside the Configuration page's new column.

## Test plan

- [x] New or changed tests (`test_playbook_escalation.py` and updates)
- [x] Local gates at `2b95cfe`: `just check` passes (460 tests); `just eval-dry-run` passes
- [ ] Evidence: none; the Configuration page column is checked in a browser by the verification pass
- [x] Review: approved at `9c9e99d`, committed as `2b95cfe`
- [x] Verified at `2b95cfe`
- [x] CI green at `2b95cfe` (all 5 checks, `just scenario (ubuntu-latest)` included)

## Internal references

CR-331 escalation-gaps.

</details>
