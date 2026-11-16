# The spend is fresh when the budget is checked

During all of run 2 `status` showed "$0.82 of $20" while the real spend passed $11; the budget rail reads that stored figure. Only `status --refresh` and `pause` write `spent_usd` (`batch_status.py`); `take` and the other commands that check the budget do not refresh it, so the budget check is blind in a short batch.

Refresh the spend where the budget is checked (or refuse on a stale figure), and show its age. Absorbs 2-backlog/P3/status-spend-age (which only shows how old the figure is): close that item with this one.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: before release.
