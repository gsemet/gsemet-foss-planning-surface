# One short card per worker role

Cache writes are 51-77% of worker cost in both runs: each worker reads whole shared cards. Give each worker role one short card holding only what it needs (CR-274 made every worker open its card: 45/45 and 49/49). No user-facing defect: a cost refactor.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: later.
