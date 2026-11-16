# A running batch switches between any two modes

Filed 2026-11-14 by the Chief of Staff, on the user's word: "rajoute dans le batch la capacité de
passer de n'importe quel format en un autre: série vers parallèle, parallèle vers stack, stack vers
parallèle ou série, ... ce qui est déjà livré est évidemment pas changé."

Today `order mode` switches only a series batch to a stack (`order mode --note stack`); batch-18,
opened in parallel, was refused when the user asked for a GitHub stack ready to merge by morning.

The ask: `order mode` takes every pair (parallel, series, stack, both ways). What is already
delivered (merged CRs) is never changed. To grill: what happens to open PRs, the order of a stack
or series, and when it applies.
