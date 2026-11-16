# The README says what a batch costs, Foreman or direct

The user's word, 2026-11-15: put a few facts on costs in the README, e.g. whether steering directly from Opus costs more than a Foreman on Sonnet, which does the job well, or not.

Figures from the two runs (one run each, different batch modes, so orders of magnitude, not averages):
| | run 1: Foreman (Sonnet 5.5), stack | run 2: direct (Opus 5.5), parallel |
|---|---|---|
| batch | $10.28 | $11.52 ($11.91 at close) |
| steering in the budget | $2.10 (20%) | $3.39 (30%) |
| operator (Chief of Staff) outside the budget | about $4.67 (woken at each Foreman turn, ~200k context) | $0.05 |
| all in | about $14.6-15.0 | about $11.5-11.9 |
Steering plus Drivers is over 60% in both; coding 7-8%; a steering session starts at about 70k tokens. The Sonnet Foreman cost less in the budget, but the second session (the Chief of Staff) cost more than that saving: no general "Foreman vs direct" conclusion. The README states the limits and how to measure one's own (`chantier cost`, `--by cr`, `--explain`).

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: before release.
