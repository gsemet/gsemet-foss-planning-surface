## Summary

In a parallel batch, two ready PRs that conflict with each other were only found at a trial merge, hours later. In one batch ten such PRs surfaced at once; rebuilding them into a stack cost about 2.5 hours, 11 conflict resolutions and about 9 extra long gates.

The Foreman card (the role that steers a batch) now checks each newly ready branch against the other ready PRs of a parallel batch with plain `git merge-tree`, when the second one is handed back. On a conflict it sends the Chief of Staff one ask to switch the batch to a stack, so the later change is rebased once onto the earlier one. The user decides; nothing switches by itself. Cards and scenario only: no CLI command, hook or type changes.

## Deliverables

The new check, as the Foreman card describes it:

```mermaid
sequenceDiagram
    participant D as Driver (CR B)
    participant F as Foreman
    participant C as Chief of Staff
    D->>F: hand-back ready to merge (B)
    F->>F: git merge-tree --write-tree B A (A already ready)
    F->>C: asks "conflict B with A: paths; switch to a stack?"
    C->>C: tells the user, switches on a yes
```

- One `git merge-tree --write-tree --name-only --no-messages` per pair, read-only for the checkouts. Any exit other than 0 or 1 is noted and never falls back to a trial merge.
- A pair is noted once and never asked again; no check in a series or stack batch; each PR stays mergeable on its own.
- The scripted Foreman of the scenario does the same, and a new scenario section proves it (no ask without a conflict, one ask and one note for a conflicting pair, none in a stack batch, the switch ordering the earlier CR at the bottom).

## Blast radius

Grade: 1. Card text, one scenario section and one docs row; a `git revert` restores the previous behaviour.

## Autonomous decisions

- The new scenario section lives in the existing `series-deps` unit rather than a new unit, to keep the scenario's unit count and its time budget.

## Known gaps

- The check run by a Copilot Foreman is unproved; the stack it may lead to on a real GitLab project is unproved.
- No `merge-tree` allow rule is added to the host capability table or the preflight sample: the host's classifier judges it, and a refusal is a `refused` ask.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/foreman.md`: the early conflict check bullet, the git duty wording, the new line in the asks list.
- `skills/chantier/references/chief-of-staff.md`: the "An early conflict" bullet (what to tell the user, the switch on a yes, nothing on a no).
- `scenario/run_scenario.py`, `scenario/README.md`: `Foreman.early_conflicts`, the allowed `merge-tree --write-tree` verb, a no-conflict check in section 4, and a new early conflict section.
- `docs/use-cases-foreman.md`: one row for what the user sees on such a conflict.

## Human decisions

- The same behaviour on both hosts and both forges, with paths not proved on Copilot or a real GitLab marked "unproved".
- On a conflict the Foreman only asks; the user decides the switch to a stack, nothing switches automatically.
- A later conflicting pair still brings a new ask after a "no"; no allow rule is added for `git merge-tree`.

## Impacts

No visual change. A user running a parallel batch gets one early question instead of a late trial-merge surprise.

## Test plan

- [x] New or changed tests (they fail on the previous code): scenario `series-deps` section, 73/73 checks
- [x] Local gates at `97f8bf1`: `just check` and `just scenario` pass
- [x] Evidence: no visual change
- [x] Review: approved at `97f8bf1` (reviewed as `afd42be` plus the uncommitted round, committed as `97f8bf1`)
- [x] Verified at `97f8bf1`
- [x] CI green at `97f8bf1`: all five checks pass

## Internal references

- CR-271 early-conflicts
- Archive: `.agents/changes/4-batch/2-actives/271-early-conflicts`
- `evals/kit/audit.py` `GIT_WRITES` does not match `merge-tree` (regex read and run).

</details>
