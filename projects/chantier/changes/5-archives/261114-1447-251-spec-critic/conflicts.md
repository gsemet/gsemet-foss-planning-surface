# Conflicts: CR-251 rebased onto cr-249 (6cfb797)

1. docs/use-cases.md (Griller paragraph): kept base's title form (`[Battle] 💬 Chantier · CoS`, icons) and this CR's "the spec critic" in the list of what a Griller does.
2. skills/chantier/references/chief-of-staff.md (shared understanding): kept this CR's restatement-with-critic-line block and the full "spec critic" section; added CR-250's sentence "The question itself follows 'Asking the user: a series'". Step 5 of the critic steps now cites that section (text first, `<short name>-Q<n>` references continuing the item's numbering, at most 5 per call) instead of a generic "grill's question format".
3. skills/chantier/references/hosts/copilot.md (preamble): one sentence names both exceptions (CR-250 question-tool row, and the Spec critic row), each unproved.

Also: deleted the stray empty untracked run_scenario.py at the worktree root.

Gate: `just check` with HOME, USERPROFILE, CLAUDE_CONFIG_DIR on scratch folders: ruff, mypy (ran, no CLI file conflicted), uv lock, biome, pytest 71 passed, release-notes ok. Rebase completed with `git rebase --continue`, commit message kept.
