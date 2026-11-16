# The ready line of a stacked CR names the CR it waits on

Since CR-270 the ready line reads the PR's base from the forge: `driver.py` `_ready_lines()` prints "PR in draft: it waits on <forge base>". In run 1 (stack) it printed "PR in draft: it waits on main" for PRs that were out of draft and stacked on another CR; four Drivers stopped on that false line, and in batch-18 one Driver put its PR back to draft because of it (retro point R12).

The line says the draft state as the forge has it, and for a stacked PR names the CR (and PR) below it that it waits on, not the forge's base branch.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: before release.
