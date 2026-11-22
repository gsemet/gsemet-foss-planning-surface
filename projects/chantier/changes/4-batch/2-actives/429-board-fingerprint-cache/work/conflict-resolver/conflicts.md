# Conflicts

- scenario/run_scenario.py, one hunk (cli_form): main uses plugin mode (`uvx --from <plugin root> chantier --skill ... --project ...`); the CR added `cli_of(project)` (a per-project form) using `uv run --no-sync`. Kept both intents: `cli_of(project)` now builds the plugin-mode `uvx` form; `cli_form = cli_of("demo")`.

Fast gate: `just check` in the worktree, passed (1687 passed, 20 skipped; release-notes ok). New head 030a7f1a.
