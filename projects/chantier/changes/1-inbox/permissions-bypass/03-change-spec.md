# Close the allow-rule bypass through gate and lease hold

From the audit of 2026-11-21 (high, confirmed in the code). The allow rules that preflight's P10
recommends, `uv run --no-sync --project * chantier *` and `uvx --from * chantier *`, cover every
chantier subcommand, and two of them run any command: `chantier gate <cr> "<command>"` runs its
arguments through a shell, and `chantier lease <unit> hold -- <command>` runs the executable it is
given. So any agent with Bash, even a read-only role misled by the text of an issue or a PR, runs
any command with no prompt. `uvx --from *` also accepts any package source. A second gap (audit,
medium): `git push -u origin chantier/*` lets a second refspec through
(`git push -u origin chantier/x +HEAD:main`).

## Goal

In the user's terms: close that bypass without adding a prompt to a night batch. No chantier
subcommand covered by the recommended allow rules runs an arbitrary command; the plugin rule names
the plugin itself, not any source; and the push rules cannot be turned into a push to `main`
without a deny rule or `main`'s own protection stopping it.

## Decisions carried from the grill

1. perm-bypass-Q1: `gate` runs only a command the project names in its configuration
   (`chantier.yaml`, through the configuration's layers), called by its name
   (`gate CR-430 scenario`); a free command is refused.
2. perm-bypass-Q2: `lease hold` runs nothing. It keeps the lease live while a given process lives
   (`--pid`); the Driver starts its wait itself.
3. perm-bypass-Q3: P10 writes the plugin's real path in place of `--from *`.
4. perm-bypass-Q4: in this CR, P10 also recommends deny rules on `git push * +*` and
   `git push * *:main`, and `main`'s protection becomes a named prerequisite of P9.
5. perm-bypass-Q5: grilled enough; specified now.

## What changes

Paths: `CLI/` is `skills/chantier/scripts/cli/src/chantier/`, `REF/` is
`skills/chantier/references/`, `TESTS/` is `skills/chantier/scripts/cli/tests/`.

### 1. `gate` runs named commands only (Q1)

Today `CLI/commands/gate.py` takes each positional argument as a command line (`_commands`,
`:213-223`) and runs it with `subprocess.Popen(cmd, shell=True, ...)` (`_spawn`, `:113-114`).

- **Configuration.** The `long_gate` key of `chantier.yaml` gains a `commands` map, name to command
  line, beside `parallel`:

  ```yaml
  long_gate:
    parallel: 2
    commands:
      scenario: just scenario
      e2e: npm run e2e
  ```

  A name is a short slug (letters, digits, `-`, `_`). A command line is one command, never a `;`
  or `&&` chain (the rule the cards already give for a gate's commands). It is read through the
  same layers as every key (`CLI/playbook/layers.py`, `read_key`; shipped defaults, then the
  surface's root, the project's folder in the surface, the project's root), and checked by
  `CLI/playbook/config.py`'s `_long_gate` (`:298-325`), which today accepts only `parallel`: an
  unknown key, a bad name, an empty or chained command line is a configuration problem, as
  `parallel`'s are. `load_long_gate` (`layers.py:386-389`) returns the commands with `parallel`.
  `chantier validate` reports the same problems. The shipped defaults
  (`config/chantier.defaults.yml`) name no command (open question 3).
- **The command.** `gate <cr> <name> [<name>...]`: each argument is a name of `long_gate.commands`,
  run in order in the CR's worktree, stopping at the first failure, as today. A name that the
  configuration does not hold, or any argument that is not a bare name (a space, a quote, a path),
  is refused (exit 1, usage) before anything runs or is logged, with one line that lists the
  names the configuration holds, or says that it holds none and points to `docs/gates.md`. With
  no `long_gate.commands` at all, `gate` runs nothing and says so. `--stop` and `--first` are
  unchanged.
- **What is recorded.** The log's `$ ` line and each `gate` event's `command` field carry the name
  and the command line it resolved to at the run (for instance `scenario: just scenario`), so a
  later change of the configuration does not rewrite what ran. `gate_passed` and the carry over a
  clean rebase are unchanged.
- **How it runs.** The resolved command line runs as today (`_spawn`, own process group, output to
  the log). Its text is the project's, not the caller's.
- **Texts that show the old form.** The usage refusal (`gate.py:219`), the parser's help
  (`CLI/declare/gate.py:22-26`), `handoff`'s checklist line (`CLI/commands/facts.py:238-240`) and
  `handback`'s refusal (`CLI/commands/driver_checks.py:190`) say `gate <cr> <name> [<name>...]`.
- **Board.** The board's configuration writes (`config.put`, `CLI/board/config_api.py`) keep
  their present keys only: they never write `long_gate.commands`.

Cards and docs (both hosts' agent files are untouched: no role's body changes):

- `REF/concepts.md` (`:433-449`, the long gate; `:748-749`): the long gate is
  `gate <cr> <name> [<name>...]`, names from `long_gate.commands`; a free command is refused.
- `REF/driver.md` (`:209-214`, `:560`, `:621`, `:1101`, `:1315-1316`), `REF/verifier.md` (`:76`),
  `REF/foreman.md` and `REF/chief-of-staff.md` where they show `gate <cr> "<command>"`: the named
  form. The stack driver's local gate (`driver.md:1315`) no longer goes under `lease stack hold`:
  a running or queued gate already keeps a lease live (`driver.md:758`); see section 2.
- `REF/init.md` step 5.1 (`:76-90`) and `REF/chief-of-staff.md` ("our long gate is `<command>`",
  `:96-102`, and the example block `:160-172`): when a long gate is declared or proposed, propose
  its `long_gate.commands` entry in `chantier.yaml` together with the `AGENTS.md` line, written
  only on the user's yes; "not asked when `chantier.yaml` already has `long_gate`" becomes "has
  `long_gate.commands`".
- `docs/gates.md`: how to declare the long gate's commands by name, and that `chantier gate`
  refuses anything else.
- `docs/agents-and-models.md` (`:51`, `:103`): the `long_gate` key's new part.

Projects that ship with chantier:

- chantier's own repository gets a root `chantier.yaml` naming its long gate
  (`scenario: just scenario`), since `AGENTS.md` asks the CR on top of a batch to pass
  `just scenario` locally through `chantier gate` (open question 4 on where it lives).
- `evals/kit/fixture/` and `evals/kit/sandbox/` get a `chantier.yaml` naming the long gate their
  `AGENTS.md` declares (`uv run pytest -q`, `uv run --locked pytest -q`).
- `scenario/run_scenario.py`: the workspace's `chantier.yaml` names `GATE` (`:59`) and the slow
  gate (`:4799`); every `chantier("gate", cr, GATE)` call (`:427`, `:887`, `:1078`, `:1151`,
  `:4769`, `:4816`) passes the name.

### 2. `lease hold` runs nothing (Q2)

Today `CLI/commands/leases.py` `_hold` (`:84-107`) resolves `command[0]` with `shutil.which` and
runs it with `subprocess.run([exe, *command[1:]])` (`:95`); the record
`.lease-hold.<unit>.<k>.run` (`CLI/core/leases.py`, `write_hold`, `:321-338`) holds the CLI's own
PID and the command.

- **The command.** `lease <unit> hold --lease <n> --pid <pid> [--batch <b>]`. It renews the lease
  first (a stale number stops there, as today), then writes the hold record with the given PID in
  `pid` and no `command` field. The lease stays live while that process lives: `hold_records`
  (`core/leases.py:121-145`) already counts a record whose process runs and was created before the
  record was written (`procs.alive_since`), and drops it once the process is gone. Whether `hold`
  returns at once or waits for the process to end and renews once then, as today: open
  question 2.
- **Refusals** (before any renewal or record): `--` followed by a command, the old form, is
  refused (exit 1, usage) with a line that names the new form; no `--pid`, a `--pid` that is not
  a whole number, or a PID with no running process, is refused. Nothing ever runs.
- `USAGE` (`leases.py:17`) and the parser options (`_OPTIONS`, `_parse`) follow.
- The `lease <unit>` line keeps saying "held by N background task(s)".

Cards and docs:

- `REF/driver.md`, "Means: CI" (`:226`), "Means: the lease" (`:753-757`), the stack driver's lease
  (`:1315-1317`), the QA driver (`:1328`): start the wait (the forge's watch, a worker's run, a
  long test) yourself in the background, then `lease <unit> hold --lease <n> --pid <its pid>`;
  `hold` runs nothing. How the Driver gets that PID on each host: open question 1. The sentence
  "`hold` keeps no shell, runs only what you give it, exits with the child's code" goes.
- `REF/concepts.md` (`:64`, Lease): "by a `lease <unit> hold` child that runs" becomes "while the
  process a `lease <unit> hold` names runs".
- `docs/planning-folder.md` (`:54`) and `docs/server-api.md` (`:78`, `holds`): the record names a
  PID; wording only.
- `scenario/run_scenario.py` section 3a (`:914-952`): the CI watch is started by the scenario as
  its own process, then held with `--pid`; the checks keep their meaning (the lease is live past
  the shortened TTL while it runs, and the record goes when it ends).

### 3. P10 names the plugin's real path (Q3)

Today `CLI/commands/permissions.py` holds the sample
`uvx --from /plugin chantier --skill /plugin/skills/chantier status` with the rule
`uvx --from * chantier *` (`:76-81`), static.

- In plugin mode, P10's sample and recommended rule are built from the plugin's real root, as
  `CLI/plugin_files.py`'s `cli_command` writes it (`uvx --from "<plugin root>" chantier --skill
  "<skill folder>"`, `:70-83`): the rule is `uvx --from "<plugin root>" chantier *`, both `Bash(…)`
  and `PowerShell(…)`, matching the quoted form the cards' `$CHANTIER` uses. `RECOMMENDED_ALLOW`
  and P10's "add" text carry the real path.
- `REF/hosts/claude-code.md`, "Allow rules" (`:267-269`, the table; `:311-316`, the pasteable
  block) and "Capabilities and their commands" (`:381`): the rule shows `<plugin root>`, filled by
  the Chief of Staff with the path P10 printed, as the remote's name is today; the "Risk accepted"
  cell becomes "the chantier plugin at that path". The test that compares the block with the CLI's
  list compares it with the placeholder in place of the path.
- An upgrade that moves the plugin's folder makes the old rule stop matching: P10 warns and names
  the new rule, and the Chief of Staff asks again; the old rule stays (nothing is ever removed).
  The host card says so in one line.
- The dev-mode rules (`uv run --no-sync --project * chantier *`, `uv sync --locked --project *`)
  are unchanged by this CR (open question 5).

### 4. Push deny rules and `main`'s protection (Q4)

- **P10 recommends two deny rules**, each in `Bash(…)` and `PowerShell(…)` forms:
  `git push * +*` and `git push * *:main` (with the project's default branch's name in place of
  `main` when it is not `main`, open question 6). `CLI/commands/permissions.py` gains a
  `RECOMMENDED_DENY` list; P10 reads the user's `permissions.deny` (already read by
  `_settings_rules`) and, when one of them is missing, says so on its P10 line (a warn, never a
  block), naming the rule. A test proves with `rule_matches` that no sample command of `SAMPLES`
  is caught by them (the steering session's route
  `git push --force-with-lease=<branch>:<sha> <remote> <sha>:refs/heads/<branch>` included), and
  that `git push -u origin chantier/x +HEAD:main` and `git push -u origin chantier/x HEAD:main` are.
- `REF/hosts/claude-code.md`, "Allow rules": one paragraph says that `*` also matches spaces, so
  `git push -u origin chantier/*` lets a second refspec through; that the deny rules stop
  `+<ref>` and `<ref>:main`; and that `main`'s protection on the forge is what remains when a form
  slips past them. A pasteable `permissions.deny` block follows the allow block. "Allow rules to
  add" gets the same merge for `permissions.deny` if open question 7 says the Chief of Staff
  writes them.
- **P9 names `main`'s protection as a prerequisite.** `REF/chief-of-staff.md`, "Forge permissions
  (P9)" (`:659-712`): at every first turn and at step 1 of every batch (not only for a merge
  capability, as probe 5 is today), P9 reads the default branch's rules (GitHub:
  `gh api repos/<owner>/<repo>/rules/branches/<default branch>`, a `non_fast_forward` rule and a
  `pull_request` or `update` rule; GitLab: `protected_branches/<default branch>`, unproved) and
  names, in the user's block, a default branch that does not refuse a force push or a direct push
  as a missing prerequisite. The legacy protection stays readable only for an `ADMIN` account;
  for others P9 says "not readable with your rights". Whether a missing prerequisite blocks the
  batch's start or only warns: open question 8. `REF/init.md` step 5.1's list of checks
  (`:90`) says the same.

## Out of scope

- The audit's other findings (board on `0.0.0.0`, the writer's secret check, performance,
  tokens). They are other CRs.
- Running the gate's command line without a shell (`shlex`, the audit's low finding on
  `cmd.exe` versus `/bin/sh`): the command line is now the project's own text.
- Allow rules for other tools, the classifier's behaviour, and Copilot (which has no P10).
- Any change to which roles have Bash.

## Residual risks, said in the host card

- An agent that can edit a `chantier.yaml` the gate reads (the CR's worktree holds the project
  root's copy) can name a new command. The roles misled by text that the audit names (Inspector,
  spec critic) do not write the project's files; a Coder already runs the project's code.
- `lease hold --pid` cannot tell whose process it names: a Driver that names a long-lived process
  keeps its lease live as long as it runs. `lease <unit>` shows the hold.

## Host and default matrix

| Cell | Expected |
| --- | --- |
| Claude Code, plugin mode, settings with the old `uvx --from * chantier *` | P10 counts the sample as allowed (the old rule still matches) and names the missing deny rules |
| Claude Code, plugin mode, no chantier rule | P10 names `uvx --from "<real root>" chantier *` |
| Claude Code, dev mode | P10's chantier rules unchanged; the deny rules named when missing |
| Copilot | no P10; `gate` and `lease hold` refusals the same |
| `long_gate.commands` absent (shipped defaults) | `gate <cr> <anything>` runs nothing, refused with the line that points to `docs/gates.md` |
| `long_gate.commands` set in the project's root `chantier.yaml` | the named commands run |
| set in the surface's project folder only | the named commands run (same layers as `parallel`) |

## Evidence

Tests (`TESTS/`, in-process, parametrized, within the time budget of `AGENTS.md`):

- `test_gate_refusals.py`: a free command (`"echo x"`, `"just scenario"`, a name with a space, a
  name not configured, no `long_gate.commands`) is refused with exit 1, nothing logged, no slot
  taken; a configured name runs and the event's `command` carries `name: line`; two names run in
  order and stop at the first failure.
- the configuration checks: `long_gate.commands` with a bad name, an empty line, a chained line,
  an unknown key under `long_gate`, each a problem from `validate` and from `gate`.
- `test_leases.py` (`:186`, the hold cases): `hold -- <cmd>` refused; no `--pid`, a bad or dead PID
  refused, nothing written; a live PID (a child the test starts) keeps the lease live past its
  TTL, and the record is dropped once the child ends; no subprocess is started by `hold`.
- the permissions tests: in plugin mode the sample and rule carry the plugin root that
  `cli_command` writes; the deny rules catch the two second-refspec pushes and no sample; P10
  names a missing deny rule.
- the host card checks read `REF/hosts/claude-code.md` as it ships at the head under test (the
  allow block with `<plugin root>`, the new deny block) against `RECOMMENDED_ALLOW` and
  `RECOMMENDED_DENY`, not a prepared text.

Scenario (`just scenario`): the gate steps use names from the workspace's `chantier.yaml`; one
step proves a free command refused with nothing recorded; section 3a holds a CI watch with
`--pid`.

Gates owed (`AGENTS.md`): `just check`, `just eval-dry-run` (the CLI's `src/` and the eval kit
change), and the pipeline's `just scenario (ubuntu-latest)` job at the PR's head (the CLI and the
cards change). No `hooks/` or `types/` change, so no `just mod`.

Unproved until a real session: whether Claude Code matches the quoted
`uvx --from "<root>" chantier *` rule against the cards' `$CHANTIER` (trial: set the rule, run
`$CHANTIER status` in auto mode); whether the deny rules stop the two pushes in Claude Code as
they do in the CLI's matcher (trial: a `--dry-run` push of each form with the rules set).

## Open questions for the user

1. **How a Driver gets its wait's PID.** Claude Code's background Bash does not print one. Getting
   it takes a compound command (`gh pr checks 12 --watch & echo $!`) or PowerShell's
   `Start-Process -PassThru`, which no recommended allow rule covers and the auto-mode classifier
   may question: that would add the prompt the intent wants to avoid. Should P10 recommend a rule
   for that form, should the cards name another way, or is a trial needed first?
2. **Does `lease hold --pid` return at once, or wait for the process to end** (and renew the lease
   once then, as today's hold does)? Waiting means a second background task per wait.
3. **The shipped defaults and gate commands.** The brief says the commands come from
   `chantier.yaml` "and the shipped defaults". The spec ships no command in
   `config/chantier.defaults.yml`, since a project's commands are its own. Should it ship any?
4. **Where chantier's own gate is named:** the repository's root `chantier.yaml` (in this CR's
   PR), or `projects/chantier/chantier.yaml` in the planning surface?
5. **The dev-mode rules** `uv run --no-sync --project * chantier *` and
   `uv sync --locked --project *` accept any project path, as `--from *` accepted any source.
   Should P10 also write the checkout's real path there, in this CR?
6. **The deny rule's branch name.** `git push * *:main` misses `HEAD:refs/heads/main`, the `-C`
   forms (`git -C * push …`, which the recommended allow rules also cover), and a project whose
   default branch is not `main`. Exactly the two rules of the answer, or also
   `git push * *:refs/heads/main`, the `git -C * push …` forms, and the project's default branch
   in place of `main`?
7. **Who writes the deny rules.** `AGENTS.md` and `chief-of-staff.md` ("The allow rules") say the
   Chief of Staff adds the allow rules P10 named "and nothing else there", "no deny, ask or other
   key". Does the Chief of Staff now add the two deny rules on the user's yes (which changes that
   project rule and the card), or does P10 only name them for the user to add?
8. **`main`'s protection as a prerequisite:** does a default branch that does not refuse a force
   push or a direct push block a batch's start, or does P9 warn, as everything in P9 does today?
9. **The `AGENTS.md` long gate line.** It keeps the rule (when a long gate is owed, its
   exemptions, what `--no-gate` quotes) and `chantier.yaml` holds the runnable command. Should the
   `AGENTS.md` line name the gate by its name (`Long gate: scenario`) instead of repeating the
   command line, so the two cannot drift?
