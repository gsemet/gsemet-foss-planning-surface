## Summary

On Claude Code, chantier ran its Foreman and its stack and release drivers on the most expensive model, although a cost analysis showed steering took 46 % of a batch's spend. This PR makes Sonnet 5.5 the default for every role but the Spec-writer, lets a task escalate to a stronger model when one of five named troubles hits (always said, never silent), and lowers the recommended auto-compact window from 400K to 300K.

## Deliverables

The CLI now prints the escalation model in one place, the last line of `playbook` and `playbook --batch`; the cards name no model and use this value:

```text
escalate: opus (claude-opus-5-5, Claude Opus 5.5)     # Claude Code
escalate: (none on this host)                          # Copilot
```

The five escalation triggers, each with the parent that sees it and the new agent started on the escalation model:

| Trigger | Parent | New agent |
| --- | --- | --- |
| A CR blocked twice (trouble in the work) | Foreman | the CR's next CR driver |
| Rounds used up, reviewer still FIX-REQUIRED | CR driver, then Foreman once rounds are granted | Coder of each new round |
| A red check the Debugger could not explain | Driver | a new debugger |
| A conflict the resolver could not settle | Driver | a new conflict-resolver |
| A failed restack | Foreman | the next stack driver |

Choices: escalation is a new agent, never a model swap of a running one; once per trigger and per task; recorded in a note before the start and in the batch retro; no escalation on a host that prints none (Copilot is untouched).

## Blast radius

The CLI change is one printed line; the rest is agent frontmatter, cards and docs. Rollback is a plain revert. The Foreman's start on Sonnet is unproved until a batch runs it.

Grade: 1

## Autonomous decisions

- The investigator step was skipped: the specification named the files and lines.
- The README has no compaction text, so no 300K line was added there.

<details>
<summary>Details</summary>

## Changes

- `agents/stack-driver.md`, `agents/release-driver.md`: model `claude-sonnet-5-5`.
- `playbook.py`, `commands.py`: an escalation table next to `MODELS` and the last `escalate:` line.
- Cards: new "Escalation" section in `concepts.md`; pointers in `driver.md`, `foreman.md`, `chief-of-staff.md`.
- `hosts/claude-code.md`: Foreman start row and Models row on Sonnet 5.5 (marked unproved until seen); Compacting recommendation at 300000.
- `README.md`, `docs/tutorial-claude-code.md`, `CONTRIBUTING.md`, two diagrams and their texts: same defaults, no model in host-neutral text.
- `test_structure.py`: the Opus roles are split per host; `scenario/run_scenario.py`: steps for the `escalate:` line and the drivers' models.

## Human decisions

- Sonnet 5.5 by default for the Foreman and every driver; the Spec-writer stays on Opus 5.5.
- Escalation to Opus on five named troubles, always said in a note and the retro, never silent.
- Auto-compact window recommended at 300K for the Chief of Staff and the Foreman.
- Copilot is left as it is.

## Impacts

No visual change. Users of Claude Code get cheaper steering by default and see `escalated:` notes when a task escalates.

## Test plan

- [x] New or changed tests (they fail on the previous code): structure test split per host, scenario steps
- [x] Local gates at `9332f0c`: `just check`, `just scenario` pass
- [x] Evidence: after at `9332f0c`: `playbook` and `playbook --batch` end with `escalate: opus (claude-opus-5-5, Claude Opus 5.5)`
- [x] Review: approved at `9332f0c`
- [x] Verified at `9332f0c`
- [x] CI green at `9332f0c`

## Internal references

- CR-177 foreman-sonnet-300k

</details>
