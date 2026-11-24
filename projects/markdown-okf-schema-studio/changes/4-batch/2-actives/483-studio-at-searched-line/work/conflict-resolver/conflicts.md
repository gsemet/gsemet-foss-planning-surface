# Conflicts: rebase of 2d64c818 on origin/main (60daaefc)

- requirements/tiers/log.md: both sides added a dated entry under `## 2026-11-24`. Kept both, CR-481 (HEAD, newest) first, then CR-483, separated by a blank line.
- New head: eb25d834260c77b16525237b7a5caeedfc9abed1. No BOM added.

Fast gate: `just requirements-update` then `just requirements-lint` (no fast gate named in rules; these were asked). Result: 0 indexes, 0 projections updated; lint passes (only existing W2 broken cross-link warnings); `git status` clean, no diff.
