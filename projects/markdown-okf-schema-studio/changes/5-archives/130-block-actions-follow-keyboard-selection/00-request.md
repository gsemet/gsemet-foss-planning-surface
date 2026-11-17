# 130 — Block actions (+ / up / down) follow the keyboard selection

Type: fix · Priority: P2 · From backlog: `02-backlog/P2/block-actions-follow-keyboard-selection`

## Intent (user)

See [01-intent.md](01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "lance 4 CR max en parallèle pour fixer tout ça et finaliser une nouvelle stack PR" (same autonomous mode as the previous run). List these in the PR body under "Autonomous decisions".
- Whichever moved last (keyboard selection or mouse hover) owns the block actions; the other indicator goes away.
- Stacked right above CR 129 (same focus code).
- Driver 2026-10-27: `just check` last step `requirements-lint --check-links` fails because the installed okfreq lacks `--check-links` (pre-existing, justfile untouched); not worked around. Reviewer round 1 required a docs line (done in round 2).
