# Intent: one way to call the CLI that works in every shell

The user, 2026-11-13 (markdown-okf-schema-studio batch-03): « Pour zsh, trouve une syntaxe
générique qui marchera partout ». Agents put the whole `$CHANTIER` command in one shell variable
(`C="uv run ... chantier"; $C status`); zsh does not split it into words, so the call fails with
"command not found".

## Does the problem still exist at main (3a9afc2c, 2026-11-18)?

Yes. The launch changed (`uv run --script <chantier.py>` became `uv run --no-sync --project
"<plugin root>" chantier` in the dev mode and `uvx --from "<plugin root>" chantier --skill
"<skill>"` in the plugin mode, both printed by `cli_command()` in
`skills/chantier/scripts/cli/src/chantier/plugin_files.py`), but it is still several words, and
no card tells an agent how to write it in a shell call:

- The habit survived the new launch: the steering session of the eval of 2026-11-15 ran
  `C="uv run --no-sync --project C:/Users/gaeta/Projets/chantier chantier"; $C foreman set ...;
  $C rules ...` (quoted in the archived CR 284-eval-audit-no-false-fails, `03-change-spec.md`
  line 81). It worked only because that shell was bash and the path has no space.
- The new launch is worse in a variable: `cli_command()` now quotes its paths. Held in a variable,
  bash splits it but keeps the quotes as characters. Measured 2026-11-18 with bash 5.3:
  `C='printf [%s] --project "C:/x y" chantier'; $C` gives `[--project]["C:/x][y"][chantier]`,
  while the literal call gives `[--project][C:/x y][chantier]`.
- In zsh (no word splitting of a parameter by default) the variable is one word: "command not
  found". In PowerShell, `$C = 'uv --version'; & $C` fails with "not recognized as the name of a
  cmdlet" (measured 2026-11-18).
- The host's permission rules (`hosts/claude-code.md`: `uv run --no-sync --project * chantier *`,
  `uvx --from * chantier *`) match the literal command, not `$C status`.

The literal command, as `cli_command()` and the `cli:` line give it, works unchanged in bash, zsh,
sh, dash and PowerShell (its paths are double-quoted, which all of them read the same way).

## What the user wants

One form of CLI call that works in every shell an agent may get, written once in the cards, so no
agent invents a variable that one shell breaks.
