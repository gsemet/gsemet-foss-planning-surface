# Conflicts: CR-473 rebased on CR-472

- justfile, `release-tests` pytest line: CR-472 added test/build/test_no_merge_commits.py, CR-473 added test/build/test_changelog_refs.py. Kept both (no_merge_commits then changelog_refs).
- All other files merged cleanly (requirements generated blocks included; `okfreq` checks report 0 changes).
- Rebase continued, message kept; new head c9712e21. Nothing pushed.

Fast gate: `just check` -> exit 0 (only existing W2 cross-link warnings from okfreq).
