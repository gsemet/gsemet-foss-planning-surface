## Summary

The long gate's proof was loose: the gate recorded a short commit id after its run, the log named no commit, and handing a change back as ready never checked that the work was still at that commit, clean and pushed. Short ids could also differ between commands in large repositories, which would refuse a hand-back forever. The batch budget was only checked when a worker started, not when a new work cycle began. A dropped change request could only leave the trash by a manual move.

This PR binds the gate's proof to one exact, readable commit, makes the budget a real bound on new work cycles, and adds a `restore` command.

## Deliverables

Gate proof, before and after:

| | Before | After |
| --- | --- | --- |
| Commit recorded | short id read after the run | full 40-character SHA read before the first command, first line of the gate log |
| Dirty worktree at `gate` | accepted | refused (exit 2), nothing run |
| HEAD moves during the run | recorded at the new head | no pass at either head, exit 4 |
| `handback ready` | gate and verdict only | also: head is the shipped one, tree clean, branch pushed |
| `--no-gate` | skipped the gate check | still the same, and only that check |

Budget and restore:

```text
round     : refused (exit 5, budget message) once the recorded spend reaches the budget; checked before the round limit
restore   : restore <6-trash/item> [--slug <name>]  ->  1-inbox/<name>, content kept, date stamp (and a batch number) removed
```

Choices: heads are full SHAs everywhere, short only for display; a head recorded short before the upgrade still matches its full SHA by prefix; CR numbers are never reused after a restore.

## Blast radius

Grade: 2. Shared CLI code (gate, ship, handback, round) and the cards change; a revert is possible, an open batch survives through the prefix rule.

## Autonomous decisions

- Number reuse after `restore` is prevented by a small file in the planning folder (`restored.json`, plain JSON, written after the move succeeds) holding the highest restored number, read by the numbering: simplest durable mechanism.
- `gate` skips its final result line when a cancel already moved the log's folder, as the existing cancel-during-gate path does.

<details>
<summary>Details</summary>

## Changes

- `commands.py`: full-SHA heads, `same_head` prefix tolerance, gate header and dirty/moved-head handling, `handback ready` checks, `restore`.
- `rails.py`: the budget is checked before the round limit.
- `state.py`, `status.py`, `cli.py`: number reservation (`restored.json`), short display, command registration and help.
- Cards (driver, worker, foreman, concepts, chief-of-staff, griller) say the same about the gate, hand-back, budget and `restore`.
- `scenario/run_scenario.py`: steps `gate_proof` and `restore_cr`.

## Human decisions

- A gate binds to a commit: a dirty tree is refused rather than gated.
- Past the budget, new work cycles are refused; proofs (gate, verdict, ship, hand-back) never are.
- `restore` goes only from the trash to the inbox; a merged change is delivered and new work is a new item.

## Impacts

Whoever hands a change back sees new refusals on `handback ready`; users get `restore`. No visual change.

## Test plan

- [x] New scenario steps `gate_proof` and `restore_cr` at `1f269b2` (fail on the previous code)
- [x] Local gates at `1f269b2`: `just check`, `just scenario` (github and gitlab, 558/558 each)
- [x] Evidence: scenario output and hand proofs at `1f269b2`
- [x] Review: approved at `1f269b2` (patch carried through a clean rebase)
- [x] CI green at `1f269b2`
- [x] Verified at `1f269b2`

## Internal references

CR-184 gate-proof-cli-fixes (batch-11); `.agents/changes/4-batch/2-actives/184-gate-proof-cli-fixes/03-change-spec.md`.

</details>

