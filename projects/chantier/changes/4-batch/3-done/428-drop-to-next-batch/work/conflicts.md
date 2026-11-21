# Conflicts: rebase of CR-428 on origin/main (99fa847f, park)

Only the first commit (1e1dcf45, now 5501f1ce) conflicted; the second applied clean (now d91edcf3).

- forge_stack_gh.py `held_outside`: kept park's 5-field unpacking (`left, dropped, held, moved, waiting`) with this CR's docstring (moved to the backlog or the next batch `3-ready`, no inbox).
- orders_drop.py imports: kept park's imports (`apart`, `is_parked`, `dependents`, `BatchRecord`, `CrEntry`) and this CR's `pr_clause` in place of `close_pr_clause`; dropped the old `all_merged`/`is_held` imports; park's `_apart_line` and `apart(c)` branch kept, `pr_clause(b, c)` used.
- release.py `cancel`: park's removal of `done`/`all_merged` kept, with `pr_clause(b, c)`.
- core/records.py: kept park's `parked` field and its comment, this CR's `left_to` comment (`3-ready`, older `1-inbox`).
- tests/test_came_back.py: kept both: this CR's added assertions in the way-back test, and park's new `test_the_cards_name_the_park_and_its_way_back`.

Fast gate: `just check` run in the worktree at head d91edcf3: pass (ruff clean, 1557 passed, 20 skipped, release-notes ok).
