## Summary

One call on a model chantier has no price for used to hide the cost of a whole session and block a batch's `close`. Now the known calls are priced, the others are counted and named, and every figure that leaves some unpriced says it is a floor ("at least"). A project adds a new model's price under `prices:` in its own `chantier.yaml`, with no release. This also gives every Progress and Completion report one fixed skeleton (the cost as a table, with the ratio of orchestration) and removes the "Driver chief-of-staff" line that named the steering session.

## Deliverables

Before and after, one unpriced `mystery-model` call in a batch (the scenario's fixture; proof named in the Test plan):

| | Before | After |
| --- | --- | --- |
| `cost` | refuses ("no Claude price for model ...") | `at least $X over N priced model calls; 1 calls of mystery-model not priced` |
| `status`, `STATUS.md`, board | `Spent: unknown` / `spend not updated` | `spent at least $X of $B` |
| `close` | refused | prints the final cost as a floor; refuses only when nothing at all can be priced |

```yaml
# chantier.yaml (all five prices required, $/MTok; long_context optional)
prices:
  claude-example-6-0:
    input: 3
    cache_write_5m: 3.75
    cache_write_1h: 6
    cache_read: 0.30
    output: 15
```

`cost` lines now carry their share of the batch's spend, followed by one ratio line:

```text
Driver cr-driver: $0.912 (64 calls, 57%)
Orchestration (steering + Drivers): 81% of the batch's spend
```

With unpriced calls the shares read `share not measured` and the ratio `not measured (calls not priced)`; on Copilot the ratio reads `not measured (no parent link on this host)`.

**UNVERIFIED:** no model was added to the built-in price table. The provider's price pages could not be read in this run, and no price is guessed. A model not in the table is covered by the floor and by `prices:`.

## Blast radius

Grade: 2

The cost code, the status files and the report card are shared; a revert restores the old behaviour, but a batch recorded with the new `unpriced` field keeps it in `batch.json` (ignored by older code).

## Autonomous decisions

- Prices are read from `chantier.yaml` live at each pricing, not frozen at `open`, so a price added mid-batch prices the next refresh.
- A `chantier.yaml` that is not valid makes `cost` refuse, instead of pricing with the file ignored.
- The built-in price table is left unchanged (no price page could be read), rather than adding a figure from memory.

<details>
<summary>Details</summary>

## Changes

- `costs.py`: a model id is priced by the same id or the id without a `-YYYYMMDD` suffix, nothing else; an unpriced call goes to `unpriced` by model, adds no dollars, still counts for context measures.
- `playbook.py`: optional `prices:` key with per-line validation, and a `prices:` line in `playbook`.
- `commands.py`, `rails.py`, `status.py`: floor wording everywhere the spend shows, `unpriced` recorded in `batch.json` and `STATUS.json`, `close` refuses only when nothing can be priced, shares and the orchestration ratio in `cost`, the steering session's main row no longer keyed as a Driver.
- `status-layout.md`, `status/SKILL.md`: the literal report skeleton, with Notes and Cost notes as the only free places.
- README, concepts and docs: the unknown-model wording and the `prices:` example.
- Tests: `test_costs.py` (unknown model counted, dated id priced) and new scenario steps.

## Human decisions

- A model with no known price is never given a look-alike price: its calls are counted and named, and the known calls are priced.
- A figure that leaves calls unpriced is a floor and says so; it is never a plain total and never `$0.00`.
- The budget counts the priced part; taking a CR or starting a round is not refused for an unknown model.
- `close` is refused only when nothing at all can be priced, not for an unknown model alone.
- A new model's price is added without a release, in the project's own `chantier.yaml`; nothing is fetched from the network.
- Copilot is left as it is: its records carry the price.
- The ratio of orchestration counts the steering session's own subagents with the steering session, as the summary split already does.

## Impacts

Reports show the cost as a table with the ratio line. No visual change otherwise.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_costs.py` and scenario steps
- [x] Local gates at `2f04cf6`: `just check`, `just scenario` pass
- [x] Evidence: the scenario asserts the before/after pair (unpriced model refused before, floor after), at `2f04cf6`
- [x] Review: approved at `2f04cf6`
- [x] Verified at `2f04cf6` (the missing built-in price stays UNVERIFIED)
- [x] CI green at `2f04cf6`

## Internal references

CR-181 cost-unknown-model. Work files: `work/04-investigation.md`, `work/04-prices.md`.

</details>

