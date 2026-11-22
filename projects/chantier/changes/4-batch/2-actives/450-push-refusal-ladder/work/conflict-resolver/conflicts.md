# Conflicts, CR-450 rebase on origin/main (906e5fd1)

Old head 6ac8498f, new head 12763fa3d4e674d7e6be372b98c154bc45074128 (not pushed).

Only one file conflicted: skills/chantier/references/hosts/claude-code.md (two hunks).
docs/tutorial-claude-code.md, docs/hosts.md and the other cards merged cleanly.

- Hunk 1 (allow-rule table): kept CR-450's two force-push rows (the plain and the `git -C *`
  rule, with the Foreman-then-Chief-of-Staff wording) and main's three rows for the dev-mode
  `uv run`, `uv sync` and plugin-mode `uvx` rules, which carry CR-433/436's wording ("when the
  session's project is chantier", "another project run from chantier's checkout").
- Hunk 2 ("Every batch" row): took CR-450's row (the `git [-C <checkout>]` route, the added
  `git -C * push --force-with-lease=...` rule, the ladder reference) and re-applied main's
  "(dev, chantier's own checkout, when the session's project is chantier: ...)" wording.

No BOM added (file starts with `# C`).

Fast gate: `just check` in the worktree: 1630 passed, 20 skipped, release-notes ok.
