# A Driver always hands back, within its context

Batch-18: Drivers ended without a recorded hand-back 4 times (CR-257, 259, 262, 263) and ran out of context twice (CR-262, CR-266); in the eval Drivers peaked at 85-97k. Detect "agent ended, no hand-back" (the transcript-ending detector of close-sees-finished-agent can serve) and keep a Driver's context bounded.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: later.
