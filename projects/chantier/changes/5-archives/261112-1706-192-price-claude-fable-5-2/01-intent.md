# Price claude-fable-5-2 in the CLI's table

## The request

From the retro of batch-13 (2026-11-12): `claude-fable-5-2` has no price in the CLI's built-in
table (`skills/chantier/scripts/cli/src/chantier/costs.py`, `PRICE`), so the 17 calls of the
fable review were not priced: the batch's cost was a floor, and the shares and the orchestration
ratio read "not measured".

## The price, from the primary source

Anthropic's pricing page, https://platform.claude.com/docs/en/about-claude/pricing, read on
2026-11-12, "Model pricing" table, row "Claude Fable 5.2":

| Base input | 5m cache writes | 1h cache writes | Cache hits and refreshes | Output |
| --- | --- | --- | --- | --- |
| $8 / MTok | $10 / MTok | $16 / MTok | $0.20 / MTok (footnote 1) | $40 / MTok |

Footnote 1 of that page: cache hits and refreshes on Claude Fable 5.2 are priced at 0.025x the
base input price ($8 × 0.025 = $0.20, consistent with the row).

## What changes

- `PRICE` gets `"claude-fable-5-2": (8, 10, 16, 0.20, 40)`, in the table's order (input, 5-min
  write, 1-h write, cache read, output).
- A test of the cost module prices a `claude-fable-5-2` call with these figures (the existing
  test file `tests/test_costs.py`; the structure rule keeps tests few).
- Any doc or card that names fable as not priced is updated.

## Out of scope

- Other models of the page (Mythos, Fable 5.1, older ones): not used by chantier's team.
- Fast mode or long-context pricing of Fable 5.2: not in the table's shape.
