## Summary

The CLI's built-in price table had no row for `claude-fable-5-2`, so calls of that model were counted as not priced: a batch's cost read as a floor ("at least") and the shares and orchestration ratio read "not measured". The table now prices `claude-fable-5-2` (and a dated id of it, `claude-fable-5-2-YYYYMMDD`) with no `prices:` entry in `chantier.yaml`.

## Deliverables

The new row, in $/MTok (input, 5-min cache write, 1-h cache write, cache read, output), from Anthropic's pricing page (https://platform.claude.com/docs/en/about-claude/pricing, row "Claude Fable 5.2", read 2026-11-12):

| Base input | 5m cache writes | 1h cache writes | Cache hits and refreshes | Output |
| --- | --- | --- | --- | --- |
| $8 | $10 | $16 | $0.20 | $40 |

```python
"claude-fable-5-2": (8, 10, 16, 0.20, 40),
```

Choices: only the base row is priced (no long-context or fast-mode row, which the table's shape does not hold); no other row changes.

## Blast radius

Grade: **1**. One table row and one test; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The row sits between the Sonnet and Haiku rows, with no `>100k` variant: the table has no such tier for this model in scope.
- The test is added to `skills/chantier/scripts/cli/tests/test_costs.py`, the file that exists, and uses five distinct token counts so a swapped column fails.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/scripts/cli/src/chantier/costs.py`: one `PRICE` row for `claude-fable-5-2`.
- `skills/chantier/scripts/cli/tests/test_costs.py`: `test_claude_fable_5_2_is_priced_from_the_built_in_table` prices one call with all five token kinds ($0.2768).

## Human decisions

- The price comes from the provider's published page, with no figure invented.
- Only `claude-fable-5-2` is added; other rows are unchanged.

## Impacts

Cost reports now price `claude-fable-5-2` calls. No visual change.

## Test plan

- [x] New test fails on the previous code (call unpriced) and passes with the row (checked at `82e367f`)
- [x] Local gates at `82e367f`: `just check` pass, `just scenario` pass (github and gitlab, 586/586 each)
- [x] Evidence: none visual (no visible change)
- [x] Review: approved at `95d02de` (rebased unchanged to `82e367f`)
- [x] Verified at `82e367f`
- [x] CI green at `82e367f`

## Internal references

CR-192 price-claude-fable-5-2

</details>
