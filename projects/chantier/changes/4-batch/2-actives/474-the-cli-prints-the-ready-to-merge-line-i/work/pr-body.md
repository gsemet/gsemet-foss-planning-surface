## Summary

After a context compaction, a steering agent lost the batch's state, and its ready-to-merge reports were written by hand: no colour icon, named links instead of the PR's URL, gaps not quoted next to each link. `status` now prints that line itself, one per CR handed back ready, and a `batch:` line with the batch's state (shape, slots, steering, rounds limit, budget, who owes the long gate, who merges), so the agent copies facts instead of recalling them. A short new card, `reload-rules.md`, holds the rules to re-read after a compaction.

## Deliverables

`status` gains two kinds of line. The first line and the CR rows are unchanged; `batch:` is the new second line.

| Before | After |
| --- | --- |
| first line, CR rows | first line, `batch:` line, CR rows, one `handed back:` line per ready CR |
| report lines written by hand | the line is copied from `status`: icon, full PR link, gaps, owed steps, long gate clause |

Real output from this branch (neutral names):

```
batch: shape parallel; slots 4/4; steering Foreman; rounds 3; budget $80.52 of $100; long gate owed: none; merges: the user; under the grant: the release/fix PR (steering session); rules: <skill>/references/reload-rules.md (reread after a compaction)
handed back: 🟢 ready to merge <id> <slug> https://github.com/<owner>/<repo>/pull/<n> | long gate <id> at <sha7>: exempt: <rule>
```

The same code on a prepared batch, with a draft PR and a CR that has no PR yet:

```
handed back: 🟤 PR in draft CR-2 the-slug https://github.com/o/r/pull/12 | do not merge: waits for its turn out of draft | owed before the merge: its long gate passes at abc1234 (the Foreman) | long gate CR-2 at abc1234: not run
handed back: 🟣 ready locally CR-3 the-slug no PR yet | owed before the merge: its long gate passes at abc1234 (the Foreman) | long gate CR-3 at abc1234: not run
```

Choices made:
- A step still owed reads `owed before the merge: <step> (<who>)`; the user may still merge, and the merge is recorded as any other.
- The rules pointer is carried by the `batch:` line, not by the startup manifest, because the Chief of Staff's startup reading has 15 bytes of room on Claude Code and 9 on Copilot, of the 12,544-byte limit, and the manifest line alone costs 35. Counted bytes (reload) are unchanged: Chief of Staff 12,529 (Claude) and 12,535 (Copilot); Foreman 9,387 and 9,568.

## Blast radius

Grade: 1. The change adds output lines to `status` and a new card; `status`'s first line, the rows, `STATUS.md` and `STATUS.json` are untouched. A plain revert restores the previous output; the one consumer that moved is tests and scenario checks that read `status` lines by position.

## Autonomous decisions

- The fallback form of the byte limit shipped (no manifest action, no sentence in the reload section; a `rules:` pointer on the `batch:` line), because the manifest line pushes the Chief of Staff's reload over the limit on both hosts. The byte limit left no room for the manifest line.
- The opening of `foreman.md` drops two phrases ("; defer the remaining sections", ", in a reused session too") to name the pointer and stay at the previous byte figures.
- `stopped_agents` also asks a ready CR's agent, so the "its Driver" clause is true only while that Driver is live; otherwise the steering role is named.
- Helpers of `batch_status.py` moved to a module of their own, with no behaviour change, to keep the file at 400 lines.

## Known gaps

- The Copilot reading of a Driver's end is unproved on a real host: the clause names the steering role by rule.
- No `own-gate` per-shape wording exists in the cards yet, so the shape bullet of `reload-rules.md` uses the batch-start card's per-shape sentence.
- The long gate (`just scenario`) is owed at the PR's head; the stack unit passed after the position fix, the full run is pending.

<details>
<summary>Details</summary>

## Changes

- `status/ready_line.py`: the `handed back:` and `batch:` lines; hooked into `commands/batch_status.py`; moved helpers in `commands/batch_status_orders.py`; `commands/activity.py` reads a ready CR's agent.
- Cards: new `reload-rules.md`; `foreman.md` opening, `chief-of-staff-merge.md` words to the user, `status-layout.md` report rules; `CONTRIBUTING.md` list.
- Tests and scenario: `tests/test_ready_line.py`, `tests/test_reload_rules.py`; the scenario checks the new lines and reads the lines that moved down by one.

## Human decisions

- One line per ready CR, with icon, full link, gaps, owed steps and the long gate clause, copied by the agent.
- One complete `batch:` line; the user merges, plus the release/fix PR under a release grant.
- A step still owed is a clause the user may overrule, not a ban on merging; a PR in draft keeps its `do not merge`.
- If the counted reload cannot fit, the pointer moves to the `batch:` line instead of raising the limit.

## Impacts

Agents see two more kinds of `status` line; no visual change for users.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test_ready_line.py`, `test_reload_rules.py`
- [ ] Local gates at `e8d53ac`: `just check` pass (2459 passed); `just eval-dry-run` 19 of 19; stack scenario unit 256/256
- [ ] Evidence: no visual change; the `status` output above is from the code at `e8d53ac`
- [x] Review: approved at `e8d53ac` (carried from `a94085d`: the tree was committed unchanged)
- [ ] Verified at `e8d53ac`
- [ ] CI green at `e8d53ac`

## Internal references

CR-474 `ready-line`, batch-31; specification and answers (ready-line-Q1 to Q13) in the planning surface; coder report `work/r1.md`.

</details>
