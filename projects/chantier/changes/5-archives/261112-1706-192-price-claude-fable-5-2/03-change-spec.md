# Change Specification: price claude-fable-5-2 in the CLI's table

## Goal

From the retro of batch-13 (2026-11-12): the CLI's built-in price table has no row for
`claude-fable-5-2`, so the calls of that model are counted as not priced, a batch's cost reads as
a floor (`at least`), and the shares and the orchestration ratio read "not measured". After this
CR, `chantier` prices a `claude-fable-5-2` call (and a dated id of it, `claude-fable-5-2-YYYYMMDD`)
from its built-in table, with no `prices:` entry in `chantier.yaml`.

## The price, from the primary source

Anthropic's pricing page, https://platform.claude.com/docs/en/about-claude/pricing, read on
2026-11-12, "Model pricing" table, row "Claude Fable 5.2" (cited in `01-intent.md`):

| Base input | 5m cache writes | 1h cache writes | Cache hits and refreshes | Output |
| --- | --- | --- | --- | --- |
| $8 / MTok | $10 / MTok | $16 / MTok | $0.20 / MTok | $40 / MTok |

Footnote 1 of that page: cache hits and refreshes on Claude Fable 5.2 are 0.025x the base input
price ($8 x 0.025 = $0.20). These five figures are the only ones this CR uses; none is derived
or invented.

## What changes

The code is read on `origin/main` (d6271d4); the Driver works from a branch of `origin/main`.

### 1. `skills/chantier/scripts/cli/src/chantier/costs.py`

In the `PRICE` dict ($/MTok, order: input, 5-min write, 1-h write, cache read, output), add one
row, after `"claude-sonnet-5-5"` and before the Haiku rows:

```python
    "claude-fable-5-2": (8, 10, 16, 0.20, 40),
```

No `"claude-fable-5-2>100k"` row: the CR prices the base row only (long-context and fast mode are
out of scope). `_price` needs no change: it already matches the exact id and the id without a
trailing `-YYYYMMDD`. The comment above `PRICE` stays as it is (it already says each price is the
provider's published one). The table's other rows are unchanged.

### 2. `skills/chantier/scripts/cli/tests/test_costs.py`

(The intake names `tests/test_costs.py`; the real file is this one, under the CLI's folder.)
Add one test, in the file's style, that prices a single `claude-fable-5-2` call using all five
token kinds with distinct counts, so a swapped column fails:

- usage: `input_tokens` 1_000, `cache_creation.ephemeral_5m_input_tokens` 2_000,
  `cache_creation.ephemeral_1h_input_tokens` 3_000, `cache_read_input_tokens` 4_000,
  `output_tokens` 5_000 (a total prompt of 10_000 tokens, so no long-context tier applies);
- assert: the row's `calls == 1`, `unpriced == {}`, and
  `usd == pytest.approx((1000 * 8 + 2000 * 10 + 3000 * 16 + 4000 * 0.20 + 5000 * 40) / 1e6)`
  (that is $0.2768).

Suggested name: `test_claude_fable_5_2_is_priced_from_the_built_in_table`. No other test changes;
the existing unpriced-model test keeps its `unknown-model`.

### 3. Docs and cards

`git grep -n -i fable origin/main` finds one mention only:
`evals/results/real-foreman-2026-11-12.md` item 11 ("`cost` has no price for `claude-fable-5-2`").
That file is a dated eval report, a record of what was observed: it is not edited. No README,
card (`skills/chantier/references/`), host card or agent file names fable or lists the priced
models, so none changes. `playbook.MODELS` (the models a role starts on) is not touched: fable is
not a role's model, and pricing a model does not make it one.

## Out of scope

- Other models of the pricing page (Mythos, Fable 5.1, older ones): not used by chantier's team.
- Fast mode and long-context pricing of Fable 5.2: not in the table's shape.
- Any change to `playbook.MODELS`, the agents' `model:` values, the `prices:` key of
  `chantier.yaml`, or the eval report that raised the point.
- A version bump or release notes: they belong to the release, not to this CR.

## Evidence

- `just check` passes (it runs the CLI's pytest, the new test included, and the release-notes
  check), on Linux, macOS and Windows through CI.
- The new test fails on `origin/main` before the row is added (the call is unpriced: `usd` is 0
  and `unpriced == {"claude-fable-5-2": 1}`) and passes after.
- `just scenario` passes (a CLI change runs the long gate, as AGENTS.md says and `02-answers.md`
  records). No scenario step is added: the scenario already proves the unpriced path and the
  `prices:` path with `mystery-model`, and one row of the built-in table is proved by the unit
  test.
- The PR's body cites the pricing page URL, its read date (2026-11-12) and the row's five figures.

## Decisions taken

From `02-answers.md`, carried:

- The price comes from the primary source cited above, with no figure invented.
- Only `claude-fable-5-2` is added; the table's other rows are unchanged.
- A CLI change: the CR runs `just scenario` before its PR.

Decided here (no question left for the user):

- The row goes between the Sonnet and Haiku rows; no `>100k` row.
- The test lives in `skills/chantier/scripts/cli/tests/test_costs.py` (the intake's
  `tests/test_costs.py` does not exist at the root), uses all five token kinds with distinct
  counts, and is the only test added.
- The eval report `evals/results/real-foreman-2026-11-12.md` stays as written: it is a dated
  record, not a doc of the current behaviour.
- No scenario step is added; no source comment is added in `costs.py` (the other rows carry none,
  the CR and the PR body cite the source).
