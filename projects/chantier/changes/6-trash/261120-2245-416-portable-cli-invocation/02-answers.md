# Answers

The user was not grilled on this CR (the Chief of Staff's brief, 2026-11-18: no questions to the
user). Each point below has no user-visible behaviour.

## Settled by the spec-writer (2026-11-18)

1. **The portable form is the literal command, not a path in a variable.** The intake proposed
   keeping only the script's path in a variable (`CHANTIER_CLI=...; uv run --script
   "$CHANTIER_CLI" ...`). The launch has changed since (`uv run --no-sync --project "<root>"
   chantier`, `uvx --from "<root>" chantier --skill "<skill>"`), and the literal command as
   `cli_command()` prints it already works in bash, zsh, sh, dash and PowerShell; it is also the
   only form the host's permission rules were written for. So: an agent writes `$CHANTIER` out in
   full, as given, in each shell call, and never holds it, or a part of it, in a shell variable.
   One form, no variant per shell.
2. **Where the rule lives:** once, in `skills/chantier/references/startup-core.md`, which every
   role reads at boot (steering sessions and started agents alike). Not repeated in the four
   `SKILL.md` files nor in the `cli:` lines.
3. **Budget:** the startup budget (`STARTUP_LIMIT` = 12,544 bytes) is not raised; the Chief of
   Staff's reload total is at 12,538 today, so the rule is paid for by tightening
   `startup-core.md` itself.
4. **The CLI does not change:** `cli_command()` and the `cli:` lines of `facts.py`, `driver.py`
   and `orders.py` already print the literal, quoted command.
5. **The eval audit is left as it is:** `evals/kit/audit.py`'s `CLI_CALL` keeps reading a call
   through a variable (`$c`, `$env:CHANTIER`), so old transcripts still score; no new eval check
   flags a variable.

## Settled by the Chief of Staff (2026-11-18)
- Folded into `optimise-the-startup-core-in-size-and-ef`: both change `startup-core.md` under the same budget, so the rule lands there, with this spec's test. This CR stays in the backlog until that one merges, then is abandoned as done there.

