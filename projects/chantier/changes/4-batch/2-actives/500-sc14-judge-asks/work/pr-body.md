## Summary

The steering session words, by hand, the question it puts to the user when a change request comes back ready: it reads the readiness word, the gaps, the gate, the waits and the owed items, then writes the sentence. The wording drifts and drops items. This adds `chantier judge`, which composes that ask from the record, so the same facts are always worded the same way, and which can record it as `asks` does. (PART 2 of this PR, the early conflict check, is listed in its own section when it lands.)

## Deliverables

`judge <cr> --epoch N [--local-gate] [--record ["sentence"]]` reads the batch record and prints the ask, the facts behind it and the decision the user owes. It decides no merge and no take-back.

```text
chantier judge <cr> --epoch N [--local-gate] [--record ["one sentence"]]
  ask: <nine parts, in a fixed order: word, gaps, gate, waits, owed items, ...>
  handed back: <line>        (or the blocked lines)
  <wait line>
  decide: <what the user answers>
```

- Without `--record` nothing is written. With it, the ask is recomputed under the lock and recorded as `asks` does.
- A blocked hand-back, or a stack CR that is not alone, gets no ask and `--record` is refused.
- Choice: `--record` prints only the lines `asks` prints (see Autonomous decisions).

## Blast radius

Grade: **1**. A new read-only command (its one write is the `--record` option, through the existing recording path) and two helpers made public in the status code; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- A CR that the batch does not hold exits 2 with a message naming the batch; the existing `unknown CR` form exits 1. Every refusal of `judge` thus has the one precondition code the specification lists.
- `--record` prints only the lines `asks` prints (`[foreman→chief-of-staff] ask A-n: …`, then the supersede lines), not the `ask:` and facts lines first. The specification's output section lists `ask:` first, but its scenario step says the `--record` run's first line starts with `[foreman→`; the scenario was followed. Open question for the specification's owner.
- `near_misses.EPOCH_COMMANDS` gained `judge`, because a test keeps that list equal to the parsers that declare `--epoch`.
- The two private status helpers `_gaps` and `_owed` became public (`gaps`, `owed`); the ready line keeps its bytes.

## Known gaps

- The ubuntu scenario job owns the long gate; the local Windows run is owed only by the change on top of the stack, which this one is not.
- Part 2 of the PR is not described here yet.

<details>
<summary>Details</summary>

## Changes

- `declare/judge.py`: the parser; `commands/judge.py`: the handler (epoch required, stale epoch refused, the CR must be in the batch, ready or blocked, anything else refused); `status/judge_words.py`: `ask_text`, nine parts in the specification's order, plus `stack_open`, `stack_pairs`, `local_gate_clause`.
- `status/ready_line.py`: `gaps` and `owed` made public.
- `cli.py`: registration; `near_misses.py`: `judge` in `EPOCH_COMMANDS`.
- `scenario/run_scenario.py` and `scenario/README.md`: a step in the parallel unit and its Coverage bullet; `AGENTS.md`: the named-exception line for `judge`.
- `tests/test_judge.py`: 26 parametrized tests.

## Impacts

No visual change. The steering session gets one command to word the ready ask; the wording no longer depends on who writes it.

## Test plan

- [ ] New tests (they fail on the previous code): `tests/test_judge.py`, 26 tests, 0.94 s
- [ ] Local gates at `<sha7>`: `just check`, `just eval-dry-run`, `just scenario --unit parallel` (294/294 at round 1)
- [ ] Evidence: none (no visual change)
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

`just test` seconds: base BASESEC, head HEADSEC.

## Internal references

CR-500 (regrouped CR: `chantier judge`, then the early conflict check), batch-31, based on CR-497's branch.

</details>
