# chantier's merge route works for a PR of a native GitHub stack

In run 1 GitHub refused `gh pr merge` for every PR of a native stack ("This pull request is part of a stack and must be merged using the asynchronous merge REST API"). The cards and `permissions.py` name only `gh pr merge` for the merges chantier does for the user (a release's PR or fix, on their word): this batch's own release PR could hit it. The eval kit's fix (PR #224) uses `PUT repos/<o>/<r>/pulls/<n>/merge-async` with merge_method, merge_action and the head SHA, then polls `GET .../merge-async/<uuid>` until it is no longer pending; merging a stacked PR merges every open PR below it.

Give the cards (and the allow rules) the route for a PR in a native stack, and prove it on a real stacked PR or say what stays unproved.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: before release.
