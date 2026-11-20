# Conflicts: CR-341 restacked on CR-340 (head 10c9233)

Rebase of f16dbc3 onto origin/chantier/batch-06/cr-340-change-specification-gate-requirement-ma; new commit 72eb59fc.

## Hunk: requirements/tiers/log.md (section 2026-11-17)

Both sides added an entry under the same date. Choice: keep both, CR-340's "Requirement markers gated" first, then CR-341's "A Main path may cite an SwRS the StRS depends on", one blank line between, markers removed. No BOM added (file still starts with `# U`). The other auto-merged file (project.guidelines.md) needed no action.

`just requirements-update` was rerun afterwards (stacked-PR guideline): 0 indexes and 0 projections updated, tree unchanged.

## Fast gate

The project's rules name no fast gate. Run instead:
- `just requirements-lint`: passed (0 files would change; main paths: 78 StRS checked, 536 SwRS citations, all valid).
- `uv run --no-sync python -m pytest test/build/test_check_main_paths.py -q`: 12 passed.
