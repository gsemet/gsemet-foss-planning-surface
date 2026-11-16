# Conflicts: rebase onto origin/main 857506d

- `commands/driver.py`, import from `chantier.stacks`: main added `draft_waited`, the CR added `pr_base_of` and `start_on_for` (multi-line import). Kept both sets. `pr_base_of` is unused in driver.py, so it is dropped (ruff F401).
- Follow-up, not a conflict: the merged `take` reached 51 lines (limit 50). The stack branch moved into `_take_stack`, with no change of behaviour.
- Other files merged automatically (driver.md, concepts.md, facts.py and others): the carry-verdict wording is intact.

Gate: `just check` passes (223 tests passed, release-notes ok). Amended into the one rebased commit. Not pushed.
