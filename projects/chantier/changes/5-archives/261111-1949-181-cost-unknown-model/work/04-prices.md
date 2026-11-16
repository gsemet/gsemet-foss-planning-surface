# Prices: CR-181 round 1

No model was added to `costs.PRICE` in round 1.

The Coder has no network tool in this run, so it could not read any provider pricing page, and a price is
never inferred from another model (spec part 1, decision 3). The built-in table is unchanged:
`claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5` (and its `>100k` tier).

Still to do by a Driver or the Chief of Staff with network access: add `claude-fable-5-2` and any other model
the Claude Code host offers that the table lacks, each at the figure on the provider's public pricing page, and
cite the page URL here and in the PR description. A model whose price is not found published stays out of the
table: its calls are then counted and named as not priced, and a project adds the price under `prices:` in its
`chantier.yaml`.

| Model | Source page | Status |
| --- | --- | --- |
| claude-fable-5-2 | not fetched | not added |
