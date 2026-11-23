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

- The long gate `just scenario` run locally on Windows at 0ec62a9 fails twice on one check, "`webui` on a running server prints `board already running at <link>`" (surface-board). This PR changes cards and a test list only; the same job passes on ubuntu-latest in CI at this head. Not investigated here.

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

- [x] New or changed tests: five startup-manifest entries that read the shipped cards (they fail on the previous cards)
- [x] Local gates at `0ec62a9`: `just check` pass; `just scenario` on Windows FAIL (see Known gaps)
- [x] Evidence: cards only, no visual change; phrases proved by the Verifier at `0ec62a9`
- [x] Review: approved at `0ec62a9` (carried from `6aa63f2` for round 1)
- [ ] Verified at `0ec62a9`
- [x] CI green at `0ec62a9`: `gh pr checks 444`, every check pass

## Internal references

CR-467 own-project-grill

</details>
