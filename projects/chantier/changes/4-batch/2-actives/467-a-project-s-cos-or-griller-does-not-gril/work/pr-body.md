## Summary

In a planning surface with several projects, a Chief of Staff or Griller session worked on another project's CRs: after filing two items into another project's inbox on the user's word, it offered to grill them. Their grill belongs to that project's own sessions. The cards now say a session works on its own project's CRs by default, may relay an item into another project's inbox on the user's word, then says in one line that the CR waits for that project's own Chief of Staff or Griller and writes nothing more there. Only the user's explicit word for that CR lifts the default, for its grill, specification and triage, never for a launch.

## Deliverables

Cards only, no CLI change. Where the rule now lives:

| Card | Section | Change |
| --- | --- | --- |
| `skills/chantier/references/session-start.md` | 2. The seat and the role | the default rule, for both roles |
| `skills/chantier/references/chief-of-staff.md` | Backlog and grill; Never | "Another project's CR" paragraph; one Never bullet |
| `skills/chantier/references/griller.md` | Never; the covered-file summary paragraph | one Never line (a board run's CR is the user's word); no `summary set` after a relay |

Choices: the CLI's `file` line is unchanged (it cannot tell a relay from an ordinary filing); the cards say its "grill the CR here" is not followed for another project's CR. Launches (`order add`, a batch, `open`) stay outside the user's word.

## Blast radius

Grade: 1. Wording in three cards and five test entries; a `git revert` restores the previous behaviour. The board Griller's startup reading is unchanged.

## Autonomous decisions

- No investigator was started: the change is three cards and one test list, all named by the specification.

## Known gaps

None

<details>
<summary>Details</summary>

## Changes

- `session-start.md`, `chief-of-staff.md`, `griller.md`: the rule above.
- `skills/chantier/scripts/cli/tests/test_startup_manifest.py`: five `MOVED_IN` entries that read the shipped cards for the verbatim phrases.

## Human decisions

- The check is in the cards only: no CLI refusal is added.
- After a relay, nothing more is written in the other project's CR (no intent, no summary).
- Only the user's explicit word for that CR lifts the default, for grill, specification and triage; a launch needs the other project's batch.

## Impacts

No visual change. Sessions of a multi-project surface stop offering to grill another project's CRs.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`:
- [ ] Evidence: before at `<sha7>`, after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-467 own-project-grill

</details>
