# Verify CR-200 at 484b8a6: PASS
- Head 484b8a6, worktree clean. Diff: costs.py, commands.py, 2 cards, test_costs.py, scenario, scenario/README.md; hooks/types untouched.
- Rule 1/2/3 implemented as specified (strict = spec-writer start or Write/Edit/MultiEdit/NotebookEdit target ending in a GRILL_NAMES entry, `\` normalised; loose elsewhere; each call classed by its own record timestamp, so since and steered calls agree inside the window).
- Run 1 re-priced (price-run1.py rerun by me): old row $0.987/18, grill $2.573/41; strict row $3.560/59, grill $0/0; sum equal ($3.560), none lost. Since open: row $3.560, grill $0.090 (2 calls) = gap to $3.61 explained in PR.
- Tests: test_costs.py 17 pass here; gate log: 58 pass, scenario 586/586 github and gitlab, result pass at 484b8a6.
- Cards chief-of-staff.md and status-layout.md match the CLI; no other card states the old rule.
- PR body matches the diff (files, rules, figures, release line, grade 1). 
- Nits: chief-of-staff.md edit leaves a very long line (wrapping only); PR "Verified at <sha7>" box to tick. CI scenario rerun pending.
