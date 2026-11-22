# Conflicts, rebase of 1add6822 onto origin/main (now b8aab46d)

- i18n/en.js, i18n/fr.js (imports): kept both `dashboard` and `inbox` imports.
- DESIGN.md: kept both sections (Dashboard, then The Inbox page).
- tests/test_board_design.py: kept both intents; the file went over the 400-line limit
  (test_code_targets), so the inbox test and its helper moved to the new
  tests/test_board_inbox_design.py (uncommitted, with that trim).

Fast gate: `just lint` passed; `just test`: 1736 passed, 1 failed (the 400-line limit above);
after the split, test_board_design, test_board_inbox_design and test_code_targets pass (42) and
`just lint` passes again. Full `just test` not re-run after the split.
