# A clean rebase does not cost a full verify

Parallel mode churns: in run 2 CR-101 cost $2.98 (11 Verifiers, 5 long gates, 15 ships) and the batch ran 25 Verifiers against 15 in run 1. Since CR-265 a gate pass carries over a clean rebase; the Verifier and gates after each rebase remain (batch-18 retro R6). Decide, in a grill, what a clean rebase with no new conflict needs to re-prove. It moves a safety line: grill first.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: later.
