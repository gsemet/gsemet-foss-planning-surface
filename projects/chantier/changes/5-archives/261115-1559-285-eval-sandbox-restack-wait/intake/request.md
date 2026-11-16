# The sandbox merge waits for the restack's checks

PR #224 (branch chantier/fix-sandbox-stack-merge) moves `evals/kit/sandbox.py merge` to GitHub's asynchronous merge so a PR of a native stack merges; the user merges it. Left: after each bottom merge GitHub restacks the PRs above and reruns their CI, so the next `merge` is refused for a pending check (run 1: #7 refused, retried once green, 10-20 s). `merge` waits for the checks at the new head (bounded) instead of refusing at once, and the README says so.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: before release.
