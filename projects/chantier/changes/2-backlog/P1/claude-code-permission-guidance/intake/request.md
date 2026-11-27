# Apply Claude Code's official permission guidance to chantier

## The owner's words (2026-11-27), verbatim

« pour les commandes je suis un peu perdu. Demande a "[Battle] 💬 Markdown-okf-schema-studio · CoS" qui m'a demandé dæen rajouter. Toi aussi tu veux en enlever. Mettez vous d accord, donne moi la commande pour tout aligner et met en P1 les recommandations officielles a mettre dans Chantier pour claude code. »

## What is asked

Put Anthropic's official Claude Code permission guidance into chantier (rules, P10, cards).

## Official guidance, read on 2026-11-27

Base: https://code.claude.com/docs/en/ . Quoted lines below were read on the page itself.

1. Wildcards (permissions.md): `*` "matches any text, including spaces". Warning: "Put the `*` after the subcommand." `Bash(git *)` allows every git command.
2. Runners (permissions.md): `npx`, `docker exec`, `devbox run` and others are not stripped; "write a specific rule that includes both the runner and the inner command", one rule per inner command. `uv` is not named; applying this to `uv run` and `uvx` is an inference.
3. Fragility (permissions.md): "Bash permission patterns that try to constrain command arguments are fragile."
4. Compound commands (permissions.md): "Every subcommand must be allowed."
5. Precedence (permissions.md): "deny, then ask, then allow"; specificity does not change the order.
6. Auto mode (permission-modes.md): on entering it, broad allow rules that grant arbitrary code execution are dropped, "including": blanket `Bash(*)`, wildcarded interpreters, a wrapper followed only by a wildcard, shell rules starting with a wildcard, some wildcarded paths, **package-manager run commands**, `Agent` and `Monitor` allow rules. "Narrow rules like `Bash(npm test)` stay in effect."
7. Narrow rules (auto-mode-config.md): "A narrow rule can still let a destructive argument through without the classifier seeing it". `autoMode.classifyAllShell: true` suspends Bash and PowerShell allow rules in auto mode.
8. Reload (settings.md): settings files are watched; "most edits" apply to the running session without a restart, `permissions` included.

Reported by a documentation research agent, not re-read on the page:

- No documented way for a plugin to ship permission rules (plugins/manifest-reference.md, plugins/components.md): "not documented", not "forbidden". User settings are the documented route.
- `autoMode` (`environment`, `allow`, `soft_deny`, `hard_deny`) is read from user or managed settings, not from project settings.
- Unattended runs: `--permission-mode dontAsk` with `--allowedTools`, or `permissions.denyInsteadOfPrompting`.
- A PreToolUse hook can allow a command, but matching deny and ask rules still apply.
- The sandbox covers macOS, Linux and WSL2, not native Windows.
- `/fewer-permission-prompts` writes to the project's settings.

## Where chantier may differ (to check, nothing proved)

- Do the pinned `uv run ... chantier *` and `uvx --from ... chantier *` rules count as "package-manager run commands"? If so, auto mode drops them and the classifier judges every chantier command. The docs do not name `uv`. `references/hosts/claude-code.md` marks these rules unproved in auto mode. Needs a real trial.
- Rules with `*` before the subcommand (`git -C * push ...`, `git -C * rebase ...`, `gh api -X PUT repos/*/pulls/*/merge-async*`) go against guidance 1.
- `help allow-rules` says it is unproved that a running session picks up an edit; the docs say settings are reloaded (guidance 8).

## Observed on 2026-11-27 (chantier, not the docs)

- The rules are global to the machine, but each project's Chief of Staff asks from its own project's P10: one asked to add the merge-async rules, another offered to remove merge rules the same morning, and P10 calls `uvx --from * chantier *` unneeded in the dev mode while other projects use `uvx`. The owner got lost. Wanted: one consistent view and one command for the whole machine.

Not grilled.
