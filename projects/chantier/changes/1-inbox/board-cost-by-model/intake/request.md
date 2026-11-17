# The board's Costs page shows where the money went, by model

The user (2026-11-17) wants a card like a reference picture: a title "Where the money went", a
switch "by model", one line "$<n> of the budget left unspent", one stacked horizontal bar from $0 to
the budget (one coloured segment per model, the unspent rest hatched), then one row per model:
colour swatch, provider mark, model name and version, the number of runs (model calls), and the
cost. For a past batch as well as the current one (the Costs page's batch navigator).

Today `cost` breaks the spend down by role (Foreman, Drivers, workers, Chief of Staff), not by
model; the closed batch's record (`5-archives/batches/batch-<n>.json`, `cost_receipt`) holds the
receipt's figures.

Grill: placement, breakdown (model, role, or both), what the bar spans, columns, and what an older
batch with no per-model figures shows.
