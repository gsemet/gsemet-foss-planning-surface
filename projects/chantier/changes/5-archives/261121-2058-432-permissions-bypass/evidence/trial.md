# Trial of rule matching (section 0)

Date 2026-11-21. Host: Claude Code 2.1.326, Windows 11. Mode: `claude -p --setting-sources local
--permission-mode dontAsk --model haiku` (main session; user-level settings not loaded), one scratch
workspace per case holding only `.claude/settings.local.json`. Each case in the Bash and the
PowerShell tool. Paths absolute, forward slashes; `<checkout>` is a scratch uv project (a stand-in
checkout, outside the repository), `<plugin root>` is `C:/Users/gaeta/Projets/chantier`.

| Case | Rule | Command | Bash | PowerShell |
| --- | --- | --- | --- | --- |
| a | `uvx --from "<plugin root>" chantier *` | `uvx --from "<plugin root>" chantier --skill "<skill>" status` | ran | ran |
| b | same | `uvx --from "/elsewhere" chantier status` | refused | refused |
| c | `uv run --no-sync --project "<checkout>" chantier *` | `uv run --no-sync --project "<checkout>" chantier status` | ran | ran |
| d | same | `uv run --no-sync --project "<checkout>" python -c "print(1)"` | refused | refused |
| e | `uv sync --locked --project "<checkout>"` | same | ran | ran |
| f | rule a | case a's command, path unquoted | refused | refused |
| g | `uvx --from <plugin root> chantier *` (unquoted) | case a's command (quoted) | refused | refused |
| h | rule a | `uv --version` | refused | refused |
| i | none (the user's broad rules `uvx --from * chantier *` etc. exist in `~/.claude/settings.json`) | `uvx --from "/elsewhere" chantier status` | refused | refused |

Controls h and i refused: the mode refuses what no rule allows and the user's settings did not
load. a, c, e ran and b, d refused: the quoted form ships (the rule text matches the quoted
command; an unquoted rule does not match it, case g). The trial proves rule matching only, in the
main session, in `dontAsk`. Raw output: `work/trial-quoted-raw.txt`.
