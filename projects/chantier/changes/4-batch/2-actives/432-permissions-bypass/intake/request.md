# Allow rules cover gate and lease hold, which run any command

From the Fable audit of 2026-11-21 (high, confirmed in the code): the allow rules preflight P10 recommends, `uv run --no-sync --project * chantier *` and `uvx --from * chantier *` (`commands/permissions.py:68`, `:80`), cover `chantier gate <cr> "<command>"`, run with `shell=True` (`commands/gate.py:113-114`), and `chantier lease <unit> hold -- <command>` (`commands/leases.py:95`). Any agent with Bash, even a read-only role misled by the text of an issue or a PR, runs any command with no prompt. `--from *` also accepts any package source.

Wanted: no chantier subcommand covered by the recommended allow rules runs an arbitrary command.
