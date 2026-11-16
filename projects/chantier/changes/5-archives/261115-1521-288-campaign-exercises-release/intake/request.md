# The eval campaign exercises what a release claims

Batch-18's evals never exercised CR-268 (gate race at `order merged`), CR-269 (a pipeline job as long gate: the sandbox's rule is a local gate), CR-273's refusal path, or CR-271 with a Foreman. Give the campaign's scenarios a way to exercise each change a release claims, or have the release notes list what was not exercised.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: later.
