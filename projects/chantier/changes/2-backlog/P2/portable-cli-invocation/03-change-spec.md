# Change Specification: one way to call the CLI that works in every shell

## Goal

The user, 2026-11-13: « Pour zsh, trouve une syntaxe générique qui marchera partout ». An agent
calls the chantier CLI in a form that works in bash, zsh, sh, dash and PowerShell alike, because
the cards say once how to write it: the command written out in full in each shell call, never
held in a shell variable.

## The problem at main (3a9afc2c, 2026-11-18)

It still exists; `01-intent.md` holds the evidence. In short: `$CHANTIER` is still a command of
several words (`cli_command()`, `skills/chantier/scripts/cli/src/chantier/plugin_files.py`), no card
says how to write it in a shell call, agents still hold it in a variable (eval of 2026-11-15:
`C="uv run --no-sync --project C:/... chantier"; $C rules`), and that form fails in zsh ("command
not found"), in PowerShell ("not recognized as the name of a cmdlet") and, now that
`cli_command()` quotes its paths, in bash too as soon as the quotes are copied (`"C:/x` and `y"`
become two arguments, quotes included). It also matches none of the host's permission rules
(`uv run --no-sync --project * chantier *`, `uvx --from * chantier *`). The literal command, as
given, works in all five shells.

## What changes

### 1. `skills/chantier/references/startup-core.md`: the rule, once

Add, next to the existing `$CHANTIER` lines (line 6, "Run the official `$CHANTIER` preparation
..."), this rule, worded so that the whitespace-normalised text holds the phrase
`never in a shell variable`:

> Write `$CHANTIER` out in full, as given, in each shell call, never in a shell variable.

(Decision 1 and 2 of `02-answers.md`: the literal command, one form for every shell, written
once in the file every role reads at boot.) It covers the whole command and any part of it: an
agent writes the paths too, not a variable holding the plugin root.

Budget (decision 3): `STARTUP_LIMIT` (12,544 bytes, `startup-manifest.json` and
`tests/test_startup_manifest.py`) is not raised. Today the Chief of Staff's reload total is 12,538
(Copilot: 12,544, exactly at the limit), and `startup-core.md` counts in every role's startup and
reload. So the Driver frees at least as many bytes as the rule adds, in `startup-core.md` itself,
by rewording, without dropping a rule and keeping every phrase `test_cli_stop.py` guards there
("in either mode, at any call", "report the exact error and stop", "no seat", "nothing written in
the planning folder", "retry once only on a transient network error", "the launch fails", "keep
their handling", "The CLI is never a tool a role works without"). A candidate: lines 3-4 ("This
is the mandatory common core. The startup manifest is the single list of mandatory reads; cards
named here are deferred references, not boot material.") can say the same in fewer words, e.g.
"The startup manifest is the single list of mandatory reads; a card named here is read only when
an action needs it."

### 2. What does not change

- The CLI (decision 4): `cli_command()`, `sync_command()`, and the `cli:` lines of
  `commands/facts.py` (line 81), `commands/driver.py` (line 87) and `commands/orders.py` (line 130)
  already print the literal, quoted command an agent copies.
- The four `SKILL.md` files (`skills/chantier`, `skills/chief-of-staff`, `skills/griller`,
  `skills/status`) keep their `$CHANTIER` paragraph unchanged (decision 2).
- The host cards' permission rules (`hosts/claude-code.md`, `hosts/copilot.md`): the literal form
  is the one they were written for.
- `evals/kit/audit.py` (decision 5): its `CLI_CALL` keeps reading a call through a variable.

## Out of scope

- An eval check or a hook that flags a CLI call through a variable.
- A wrapper script or a shell function for the CLI (a new launch form).
- Raising the startup budget.

## Evidence

Tests, in `skills/chantier/scripts/cli/tests/test_plugin_files.py`, extending
`test_one_launch_two_modes_one_text` (no new test function):

1. It reads the shipped `skills/chantier/references/startup-core.md` from the repository at the
   head under test (through `PLUGIN_ROOT`, as the test already reads the `SKILL.md` files),
   normalises its whitespace (`" ".join(text.split())`, as `test_cli_stop.py` does) and asserts it
   holds `never in a shell variable`. No prepared text.
2. It asserts the literal command survives one shell parse unchanged even when the plugin root
   holds a space: for a dev root and a plugin root under `tmp_path / "with space"`,
   `shlex.split(cli_command())` gives `["uv", "run", "--no-sync", "--project", <root as posix>,
   "chantier"]` and `["uvx", "--from", <root>, "chantier", "--skill", <skill>]`. (The prepared
   folders here are a case the shipped plugin cannot hold: a root with a space.)

Guards that already exist and must stay green:

- `test_startup_manifest.py::test_startup_manifest_measures_every_real_role_and_host` (both
  hosts): every role's startup and reload total at most 12,544 bytes. Its printed
  `startup-bytes` lines (`-s`) for `chief-of-staff` and `router`, before and after, go in the PR's
  Deliverables.
- `test_cli_stop.py`: the startup core's stop rule, phrase by phrase.

Shells: no host or default matrix applies (the rule is the same text on both hosts and depends on
no configured value). The shell matters; the PR's Deliverables carry one line per shell, the
literal dev-mode command run as `<cli> --version` from the Driver's machine, and the variable
form's failure where the shell is at hand:

| Shell | Literal command | Whole command in a variable |
| --- | --- | --- |
| PowerShell 5.1 (Windows) | runs (measured 2026-11-18: `chantier 0.13.0`) | fails (measured) |
| bash | runs | splits, but a quoted path keeps its quotes (measured, bash 5.3) |
| zsh | runs | "command not found" (intake, 2026-11-13); run it if zsh is at hand, else say "not run" |
| sh / dash | runs (intake, 2026-11-13) | splits, same quote fault as bash |

Gates (`AGENTS.md`): `just check` at the pushed head. The change touches the cards and the tests,
not the CLI's `src/` nor the eval kit, so `just eval-dry-run` is not owed; a cards change passes
the pipeline's `just scenario (ubuntu-latest)` job before its PR. No scenario step is added: the
scenario's agents follow the cards, and nothing in it reads how a call is written.

## Open questions

None.
