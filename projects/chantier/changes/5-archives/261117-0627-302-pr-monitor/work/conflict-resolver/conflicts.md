# Conflicts: CR-302 rebase onto origin/main (7ae5958)

Rebased the single commit 0141856 (now edf4642, message unchanged). Both sides kept in every hunk.

- AGENTS.md hunk 1 (no-setup bullet): main's config-layers text kept; added "except the board's PRs page (below)" to the no-network clause.
- AGENTS.md hunk 2 (board exception): main's "backlog and role config in chantier.yaml" text kept; the CR's PRs-page exception appended before "it takes its dependencies".
- board/routes.py import: `autosync_api, config_api, costs, files, guard, prs, static, write_api`.
- board/web/js/i18n/en.js: both `nav.config` and `nav.prs`.
- tests/test_board.py MODULES: `config_api`, `prs`, `forge_read`.

Line endings kept (CRLF files stay CRLF, en.js LF), no BOM added. Nothing pushed.

Fast gate: `just check` (run in the worktree): passed, 349 tests passed, ruff, mypy, biome, uv lock check, release-notes ok.