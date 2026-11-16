# The eval judge follows a PR whose head was replaced

In run 1 (stack) the judge returned "not run" for 4 of 6 checks: it reads the head SHA recorded in the batch, and GitHub's restack after each bottom merge replaced those heads. The campaign's verdict rests on this. The judge resolves the CR's PR and judges its merged (or current) head, and says which head it judged.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: before release.
