## Summary

The steering session words, by hand, the question it puts to the user when a change request comes back ready: it reads the readiness word, the gaps, the gate, the waits and the owed items, then writes the sentence. The wording drifts and drops items. This adds `chantier judge`, which composes that ask from the record, so the same facts are always worded the same way, and which can record it as `asks` does. 

The same PR adds `chantier conflicts`: in a parallel batch the early conflict check (a `git merge-tree` run on each pair of ready changes, the notes to record and the one ask to send) was typed by hand from a 3.8 KB card. The command runs the pairs, records the notes and prints the ask.

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
- `conflicts <cr> --epoch N` first checks the local git version, then runs one `git merge-tree --write-tree` for each pair of this ready change and another ready change that has a PR on the default branch (a PR base not recorded counts as the default branch). It skips chained pairs and pairs already noted, records a note for each conflict or run that could not be made, and prints the ask for the user without recording it. A batch that is not parallel gets one line saying so; a git too old for that form is refused.

```text
chantier conflicts <cr> --epoch N
  conflicts: ... N conflict, N clean, N skipped (already noted or chained), N not run
  <cr> x <other>: conflict in <paths>; noted
  <cr> x <other>: clean
  <cr> x <other>: not run: <git's first line>; noted
  next: asks "<the ask>"
```

- Choice: `--record` prints only the lines `asks` prints (see Autonomous decisions).

## Blast radius

Grade: **1**. Two new commands (`judge` writes only with `--record`, through the existing recording path; `conflicts` records notes) and a few helpers (`core/git.py` version helpers, two status helpers made public); a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- A CR that the batch does not hold exits 2 with a message naming the batch; the existing `unknown CR` form exits 1. Every refusal of `judge` thus has the one precondition code the specification lists.
- `--record` prints only the lines `asks` prints (`[foreman→chief-of-staff] ask A-n: …`, then the supersede lines), not the `ask:` and facts lines first. The specification's output section lists `ask:` first, but its scenario step says the `--record` run's first line starts with `[foreman→`; the scenario was followed. Open question for the specification's owner.
- `near_misses.EPOCH_COMMANDS` gained `judge`, because a test keeps that list equal to the parsers that declare `--epoch`.
- `conflicts` checks the git version first on every call, before any other work, so an old git is refused at once.
- A pair whose PR base is not recorded counts as on the default branch.
- `conflicts` only prints the ask (`next: asks "..."`) and records none; the steering session sends it.
- `conflicts` counts a pair as a conflict only when `git merge-tree` exits 1 with a tree id on its first stdout line; git also exits 1 for a missing ref, so that case is "not run" with git's first line. This widens the specification's "any other exit is not run" rule.
- The `conflicts` handler is split in two functions to keep within the 50-line function limit enforced by a test.
- The scenario step for `conflicts` lives in the series-deps unit, where chained batches run.
- The two private status helpers `_gaps` and `_owed` became public (`gaps`, `owed`); the ready line keeps its bytes.

## Known gaps

- The ubuntu scenario job owns the long gate; the local Windows run is owed only by the change on top of the stack, which this one is not.
- The `git merge-tree --write-tree` form is unproved on the CI runners' git; the CI scenario job is the first run of it there.
- Both commands only add: no card text changes, and the old card keeps working (the scripted Foreman is unchanged).

<details>
<summary>Details</summary>

## Changes

- `declare/judge.py`: the parser; `commands/judge.py`: the handler (epoch required, stale epoch refused, the CR must be in the batch, ready or blocked, anything else refused); `status/judge_words.py`: `ask_text`, nine parts in the specification's order, plus `stack_open`, `stack_pairs`, `local_gate_clause`.
- `status/ready_line.py`: `gaps` and `owed` made public.
- `cli.py`: registration; `near_misses.py`: `judge` in `EPOCH_COMMANDS`.
- `scenario/run_scenario.py` and `scenario/README.md`: a step in the parallel unit and its Coverage bullet; `AGENTS.md`: the named-exception line for `judge`.
- `tests/test_judge.py`: 26 parametrized tests.
- `declare/conflicts.py`, `commands/conflicts.py`, `core/git.py` (`version`, `parse_version`, a `run` wrapper returning code, stdout, stderr, and the `merge-tree` form); `cli.py` and `near_misses.py` register `conflicts`; a series-deps scenario step and README bullet; the AGENTS.md git-exceptions clause and a `conflicts` paragraph.
- `tests/test_conflicts.py`: 21 cases.

## Impacts

No visual change. The steering session gets one command to word the ready ask and one to run the early conflict check; the wording no longer depends on who writes it.

## Test plan

- [ ] New tests (they fail on the previous code): `tests/test_judge.py`, 26 tests, 0.94 s; `tests/test_conflicts.py`, 21 cases (about 19 s alone: git setup per test); the tests ran on git 2.56.0 (Windows)
- [ ] Local gates at `<sha7>`: `just check`, `just eval-dry-run`, `just scenario --unit parallel` (parallel unit 294/294 at round 1), `just scenario --unit series-deps` (85/85 at round 2)
- [ ] Evidence: none (no visual change)
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

`just test` seconds: base 154.6 s (2745 passed, run alone on origin/main eb1f4d05), head about 172 s (2872 passed; noise on this machine is 166-185 s).

## Internal references

CR-500 (regrouped CR: `chantier judge`, then the early conflict check), batch-31, based on CR-497's branch.

</details>
