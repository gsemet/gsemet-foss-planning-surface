## Summary

To make a queued change wait for one more predecessor, the only form was `order after <cr> --note <list>`, which replaces the whole list: every existing predecessor had to be retyped, and each one had to be named by its id, a slug or a path being refused. This PR adds `--add` and `--remove`, which change one entry and keep the rest, and lets every predecessor (and the target) be named by its id, its folder slug or its path. A refusal now lists the accepted forms.

## Deliverables

```text
order after <cr> --note "<a>,<b>"   # replaces the list (refs may now be ids, slugs or paths)
order after <cr> --add <c>           # waits for a, b, c
order after <cr> --remove 3-ready/some-slug
order after some-slug --add 4-batch/1-pending/<n>-some-slug   # target and ref by slug or path
```

- A repeated or already-present ref changes nothing and the line ends `(unchanged)`.
- Refs resolve against the batch: an id (`CR-447`, `447`), else the folder slug of a path or bare slug; a slug shared by several CRs is refused with their ids named.
- The order recorded for the Foreman carries the resulting list as ids (or `-`), whichever form was typed.

## Blast radius

Grade: 1. Local to the `order after` command and two lines of cards; `git revert` restores the previous behaviour. `--note` keeps its meaning.

## Autonomous decisions

- The resolver and the three forms live in a new `commands/orders_after.py`, to keep `orders_apply.py` within the project's size limits.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `declare/orders.py`: flags `--add` and `--remove`, new help texts.
- `commands/orders.py`: argument checks (exactly one of the three on `after`; `--add`/`--remove` refused on other kinds) and one shared usage line; the `after` note is no longer rewritten at parse time.
- `commands/orders_after.py` (new): ref resolver, the three forms, `(unchanged)`; `orders_apply.py` and `orders_word.py` call it.
- Cards: the Chief of Staff's batch-start and steering cards and `concepts.md` say what `--add` and `--remove` do.
- `scenario/run_scenario.py`: two steps on the real CLI.

## Impacts

No visual change. Operators type fewer ids; the order line shows the resulting predecessors.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `tests/test_order_after.py`
- [x] Local gates at `b728c71`: `just check` (2426 passed), `just eval-dry-run` (19 of 19), `just scenario` pass
- [x] Evidence: none beyond tests and the scenario, at `b728c71`
- [x] Review: approved at `b728c71` (reviewed at a94085d, committed as b728c71)
- [x] Verified at `b728c71`
- [x] CI green at `b728c71`

## Internal references

- CR-480 order-after
- Specification: 03-change-spec.md

</details>
