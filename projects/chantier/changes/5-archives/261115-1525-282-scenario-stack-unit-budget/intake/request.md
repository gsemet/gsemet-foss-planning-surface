# The scenario's stack unit fits its budget

The scenario's stack (github) unit ran over its budget twice in batch-18 (344.8 s and 375.6 s against 320 s; `run_scenario.py`, `scenario/README.md` still shows a measured max of 313.9 s). With the budget unchanged the long gate can flake on every CR of the next batch. Measure it again and either bring the unit under its budget or set the budget from fresh measures, with the README's measured columns refreshed.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: before release.
