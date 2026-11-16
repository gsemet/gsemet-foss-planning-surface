# Conflicts: restack of CR-266 onto CR-262

Command: `git rebase --onto origin/chantier/batch-18/cr-262-... b9f20b6 <branch>`. Only commit 1 (47e2c8f) conflicted.

- scenario/run_scenario.py, "stack" case list: kept both `base_from_pr` (CR-262 side) and `stack_waiver` (this CR); wrapped over lines for the formatter.
- scenario/run_scenario.py, CASES dict: kept both `base_from_pr` and `stack_waiver` entries.
- commands/facts.py imports: kept both `stacked_read` and `gate_passed`.
- commands/orders.py imports: kept `WAIVE_USAGE` and `require_epoch` (CR-255).
- commands/driver.py, handback ready tail: kept the upstream split into `_record_ready` (with `from_blocked`, `blocked_reason` clearing) and this CR's `GateBasis` (`basis.event_keys()`, waiver words, carried head); `_record_ready` takes `(basis, reason)`; imported `GateBasis`.
- Follow-up commit: `order()` went over 50 lines; extracted `_normalise_args` in orders.py (a pure move, no new behaviour).

Epoch (CR-255): no steering call added by this CR's commits lacks --epoch (the added calls are CoS orders, handback, verdict: none are steering commands needing it).

Gate: `just check` -> passed (ruff, mypy, biome, 163 pytest, release notes). Not pushed; `just scenario` not run.
