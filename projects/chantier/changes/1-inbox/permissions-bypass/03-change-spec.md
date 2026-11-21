# chantier's allow rules name real paths, not a wildcard

Step 1 of the audit finding of 2026-11-21 (high). The allow rules that preflight's P10 recommends
for chantier's own CLI carry a `*` where a path belongs: `uvx --from * chantier *` lets `uvx` run
any package from any source as long as the text holds ` chantier `, and
`uv run --no-sync --project * chantier *` matches, by its middle `*`, commands such as
`uv run --no-sync --project . python -c ... chantier x` (the CLI's own matcher,
`commands/permissions.py`, `rule_matches`, lines 205-220, says so; Claude Code's matching of it was
not tried). Older broad rules of this form are still in the user's settings.

## Goal

In the user's terms: the rules chantier offers let through chantier itself, at its real folder, and
nothing else that happens to say `chantier`; the broad rules already in the user's settings are
named so the user can remove them. No new prompt in a night batch.

## Decisions carried from the grill

- perm-bypass-Q3: P10 writes the plugin's real path in place of the `*` of `--from *`.
- perm-bypass-Q6: P10 names each broad chantier rule it finds in the user's settings as letting
  any command through, for the user to remove; nothing removes them for the user.
- perm-bypass-Q7: P10 writes the checkout's real path into both dev-mode rules
  (`uv run --no-sync --project <checkout> chantier *`, `uv sync --locked --project <checkout>`).
- perm-bypass-Q17: this CR is step 1 only; `gate` and `lease hold` are the CR
  `gate-hold-narrowing`; the push part is dropped.
- perm-bypass-Q18: a real test of the quoted-path rule in Claude Code comes first.
- perm-bypass-Q19: next to each broad chantier rule, P10 names the real-path rule that replaces
  it, and the Chief of Staff offers to add those at once, on the user's yes; the user still
  removes the broad ones by hand. No night batch meets a prompt in between.
- perm-bypass-Q20: when the plugin's path moves on an update, one question per update for the new
  rule is accepted, and P10 also names the stale chantier rule (pointing at an old copy) for the
  user to remove.

Q1, Q2, Q4, Q5 and Q8 to Q15 no longer apply to this CR.

## What changes

Paths: `CLI/` is `skills/chantier/scripts/cli/src/chantier/`, `REF/` is
`skills/chantier/references/`, `TESTS/` is `skills/chantier/scripts/cli/tests/`.

### 0. The trial first (before any code)

The Driver proves, in a real Claude Code session, which rule text matches the command the agents
type, before writing P10's rules. Setup: a scratch workspace outside the repository with only a
`.claude/settings.local.json` holding the trial rules; a non-interactive session
(`claude -p`) that loads no user-level settings (`--setting-sources local`, or the flag the host's
`claude --help` names for it; when the host has none, the Driver stops and reports, since the
user's own broad rules would let every case through), in a permission mode where a command no rule
allows is refused, not asked (`dontAsk` if the host has it, else `default`, where `-p` refuses
what it cannot ask). Each case asks the session to run one command exactly, and reads whether it
ran or was refused:

| Case | Rule set | Command run | Expected |
| --- | --- | --- | --- |
| a | `Bash(uvx --from "<plugin root>" chantier *)` | `uvx --from "<plugin root>" chantier --skill "<skill folder>" status` | runs |
| b | the same | `uvx --from "/elsewhere" chantier status` | refused |
| c | `Bash(uv run --no-sync --project "<checkout>" chantier *)` | `uv run --no-sync --project "<checkout>" chantier status` | runs |
| d | the same | `uv run --no-sync --project "<checkout>" python -c "print(1)"` | refused |
| e | `Bash(uv sync --locked --project "<checkout>")` | `uv sync --locked --project "<checkout>"` | runs |
| f | rule a | the same command with the path unquoted | recorded, no expectation |
| g | `Bash(uvx --from <plugin root> chantier *)` (unquoted) | case a's command (quoted path) | recorded, no expectation |
| h | rule a | `uv --version` (no rule allows it) | refused: the control of the mode |
| i | none in the workspace; `Bash(uvx --from * chantier *)` in the user's `~/.claude/settings.json` (already there or added for the case and restored after) | `uvx --from "/elsewhere" chantier status` | refused: the control that user-level settings are not loaded |

On Windows, each case also with the `PowerShell(…)` form. Paths are absolute, forward slashes, as
`CLI/plugin_files.py` writes them.

- When h or i runs: the setup is wrong (the mode asks or allows, or the user's settings load); the
  Driver fixes the setup and runs the trial again, and stops and reports when it cannot.
- When b or d runs: the Driver stops and reports to the Chief of Staff, with the host's exact
  text (a real-path rule that lets another path or another command through closes nothing).
- When a, c and e run and b and d are refused: the quoted form ships as below.
- When the quoted rule does not match but the unquoted rule matches the quoted command (case g
  runs: the host strips quotes before matching): the rule text ships unquoted; the rest is
  unchanged.
- When neither form matches: the Driver stops and reports to the Chief of Staff, with the host's
  exact text. No other rule form is tried (no fallback).

The trial proves rule matching only, in the main session, in the mode it ran in. The results
(date, host version, OS, mode, each case's outcome) go in the PR's body and in the Mark column of
the three rows of `REF/hosts/claude-code.md` (section 3), as "rule matching proved (main session,
`<mode>`)"; the host card's auto-mode and Driver (subagent) Marks stay unproved.

### 1. One source for the launch text (`CLI/plugin_files.py`)

`cli_command` (lines 70-83) and `sync_command` (lines 86-91) build the launch from the plugin root.
Two small functions give each form's text from the plugin root whatever the mode:
the plugin form `uvx --from "<root>" chantier --skill "<skill>"` and the dev form
`uv run --no-sync --project "<root>" chantier`, and the sync line. `cli_command` and `sync_command`
compose them as today (same output, same mode test); P10 calls them for its samples and rules, so
the rule and what the agents type cannot drift. The plugin-form sample is built whatever the mode
(the sample names the plugin-mode rule), which `sync-blocked-by-others`, ordered after this CR,
relies on when it changes `_forges`.

### 2. P10 (`CLI/commands/permissions.py`, `CLI/commands/preflight.py`)

- **Samples and rules with real paths.** The three chantier rows of `SAMPLES` (lines 64-81) keep
  placeholders, `<checkout>` and `<plugin root>`, in their rule and command:
  `uv run --no-sync --project "<checkout>" chantier *`, `uv sync --locked --project "<checkout>"`,
  `uvx --from "<plugin root>" chantier *` (or unquoted, per the trial). `commands_not_allowed`
  fills them at run time from section 1's functions: the sample commands become the exact launch
  plus ` status` (dev and plugin) and the exact sync line; the rules P10 names after `add` carry
  the real path. `RECOMMENDED_ALLOW` keeps the placeholders (it is the host card's block); one
  function returns it filled for this install, used by the scenario and the tests.
- **Broad rules named.** `_settings_rules` (lines 233-253) also keeps, for each allow rule, the
  file it came from. P10 tries each allow rule that counts (`_counts_as_allow`; rules auto mode
  drops are not chantier's) against six probe commands, each in Bash and, on Windows, PowerShell:
  `uvx --from "/elsewhere" chantier status`, `uv run --no-sync --project "/elsewhere" chantier status`,
  `uv run --no-sync --project . python -c x chantier y`, `uv sync --locked --project "/elsewhere"`,
  and the two older forms still found in users' settings,
  `uv run --script /elsewhere/chantier.py status` and
  `uv run --locked --project "/elsewhere" chantier status`.
  A rule that lets a probe through is a broad chantier rule (for instance `uvx --from * chantier *`,
  `uv run --no-sync --project * chantier *`, `uv sync --locked --project *`, `uv sync *`,
  `uv run --script * *`, `uv run --locked --project * chantier *`).
  P10 judges by matching, not by the rule's text, as it does for the samples.
- **The replacing rule named (Q19).** Beside each broad rule, P10 names the filled real-path
  rules of this install that replace it: those recommended chantier rules (section 1's forms)
  whose sample the broad rule lets through today (the plugin rule for the plugin sample, the dev
  rule for the dev sample, the sync rule for the sync line), whether or not they are already in
  the settings; those already there are marked `present`. This holds even when every sample is
  allowed (through the broad rule), so the Chief of Staff can add the replacing rules before the
  user removes the broad one, and no command meets a prompt in between.
- **Stale rules named (Q20).** A rule in the form of a recommended chantier rule (the plugin
  rule, a dev rule or the sync rule, with the trial's quoting) whose path is not this install's
  and that lets no probe through is a stale chantier rule: in the plugin form, any other path
  (one plugin copy per host install: another path is an old copy, left by an update); in the dev
  forms, only when its path no longer holds a folder (a user may keep several checkouts). P10
  names it with its file, for the user to remove by hand; it does not change the count of
  missing commands.
- **The P10 line.** On the "every batch" line (the report stays within ten lines,
  `MAX_OUTPUT_LINES`): when a broad rule is found, the line is a warn even when every command is
  allowed, and ends with
  `; broad rules let any command through, remove them by hand: <rule> (<file>), replaced by
  <real-path rule>[ present]; ...`, and, when a stale rule is found (a warn too),
  `; stale chantier rules, remove them by hand: <rule> (<file>); ...`. P10 stays warn-only and
  never blocks the go. A broad rule still counts as letting its sample through (it
  does), so the count of missing commands is unchanged by it.
- Nothing in the CLI writes or removes a settings rule.

### 3. Cards and docs

- `REF/hosts/claude-code.md`:
  - "Allow rules", the three rows (lines 267-269): the rule shows `"<checkout>"` or
    `"<plugin root>"`, filled with the path P10 prints; "Risk accepted" becomes "every chantier
    subcommand of the checkout at that path" / "of the plugin at that path", and says that `gate`
    and `lease hold` still run the command they are given, until `gate-hold-narrowing`; the Mark
    carries the trial of section 0.
  - The pasteable block (lines 311-316) and "Capabilities and their commands" (line 381, and the
    rule column): the same placeholders. Lines 448 and 472 name the new forms.
  - One paragraph after the table: a broad chantier rule (examples above, the older
    `uv run --script` and `uv run --locked --project` forms included) lets any command through;
    P10 names each with its file and the real-path rule that replaces it; the Chief of Staff
    offers to add the replacing rules at once; the user removes the broad rule by hand; chantier
    never removes it.
  - One line: the plugin's real path changes when the host moves the plugin's folder (an update,
    if the host's folder holds the version: unproved); the old rule then stops matching, P10 names
    the new one and the old one as stale, and the Chief of Staff asks again, one question per
    update; the user removes the stale rule by hand.
  - "Allow rules to add" (lines 834-858): the rules carry the real path, complete, no placeholder,
    as for the remote name; a path holding a `'` breaks the two command lines' quoting, and the
    Chief of Staff says so instead of giving them.
- `REF/chief-of-staff.md`, "The allow rules (P10, Claude Code)" (lines 104-142): the question
  lists the rules with their real path, as P10 printed them. A new bullet, **Broad rules**: when
  P10 names one, say it in the strong warning, once per session, with its file and that it lets
  any command through, and in the same question offer to add at once the real-path rules P10
  named beside it (not those marked `present`), on the user's yes; the user removes the broad
  rule by hand; never remove or edit it yourself (the last bullet, "nothing else is written",
  stands). A new bullet, **Stale rules**: when P10 names one (an update moved the plugin), name
  it in the same question as the new rule, with its file, for the user to remove by hand: one
  question per update. `AGENTS.md` is unchanged: the Chief of Staff still adds only the rules P10
  named.
- The four SKILL.md files that define `$CHANTIER` (`skills/chantier/SKILL.md` line 15,
  `skills/chief-of-staff/SKILL.md` line 18, `skills/griller/SKILL.md` line 16,
  `skills/status/SKILL.md` line 15) and `REF/concepts.md` (line 417, `$CHANTIER`) get the same
  added sentence, word for word: `<plugin root>` is written absolute, with forward slashes, quoted
  (or unquoted, per the trial), exactly as P10's rule holds it; `$CHANTIER` is carried verbatim
  into every brief and command, since another form of the path does not match the rule and meets
  the host's prompt.

Both hosts' agent files are untouched. Copilot has no P10.

## Out of scope

- `gate` and `lease hold`, which still run any command given: the CR `gate-hold-narrowing`.
- The push rules, their second refspec, deny rules and `main`'s protection: dropped by the user
  (Q17).
- Removing or editing any rule in the user's settings.
- Which mode's rules apply to a project (dev or plugin): `sync-blocked-by-others`. A note for
  that CR, not edited here: its section 3 still names the deny rules, dropped with the push part
  (Q17); its next spec run drops them.
- The audit's other findings; Copilot.

## Host and default matrix

| Cell | Expected |
| --- | --- |
| Claude Code, plugin mode, no chantier rule | P10 names `uvx --from "<real plugin root>" chantier *` |
| Claude Code, plugin mode, the real-path rule set | P10 ok for that row |
| Claude Code, plugin mode, `uvx --from * chantier *` set | sample allowed; P10 warns, naming the rule and its file as broad, and the real plugin rule that replaces it |
| Claude Code, plugin mode, `uv run --script * *` or `uv run --locked --project * chantier *` set | P10 warns, naming it as broad |
| Claude Code, plugin mode, the plugin rule of another plugin folder set | P10 names the new rule as missing and the old one as stale, with its file |
| Claude Code, dev mode, no chantier rule | P10 names both dev rules with the real checkout path |
| Claude Code, dev mode, `uv run --no-sync --project * chantier *` and `uv sync --locked --project *` set | P10 warns, naming both as broad, each with its real-path dev rule |
| Claude Code, dev mode, a dev rule whose path no longer exists | P10 names it as stale |
| Claude Code, dev mode, a dev rule of another existing checkout | not named |
| Claude Code on Windows | the same, each rule and probe in Bash and PowerShell forms |
| Copilot | no P10; nothing changes |

## Evidence

- Section 0's trial, results in the PR's body (the first evidence; nothing ships before it).
- Tests (`TESTS/test_cli_runs.py`, in-process, parametrized, within `AGENTS.md`'s time budget):
  - the host card test (`test_the_allow_rules_json_block_lists_exactly_what_preflight_checks`,
    line 198) keeps reading `REF/hosts/claude-code.md` as it ships at the head under test and
    compares its block and table with `RECOMMENDED_ALLOW` and `SAMPLES`, placeholders included;
    each sample, filled with one path, is matched by its rule filled with the same path.
  - in plugin mode (a skill folder whose plugin root holds no `.git`) P10 names the plugin rule
    with that root; in dev mode, the two dev rules with the checkout's root.
  - each of `uvx --from * chantier *`, `uv run --no-sync --project * chantier *`,
    `uv sync --locked --project *` and `uv run --locked --project * chantier *` (an older form) in
    a settings file makes P10 warn, naming the rule, the file and the filled real-path rule that
    replaces it (marked `present` when it is set too); the filled recommended rules alone give
    `P10 ok`; no probe matches a filled rule.
  - a plugin rule with another plugin folder's path is named stale; a dev rule whose folder is
    gone is named stale; a dev rule of another existing folder is not.
- Scenario (`scenario/run_scenario.py`, lines 975-1020): the settings it writes use the filled
  rules (P10 ok as today); one new check sets `uvx --from * chantier *`,
  `uv run --no-sync --project * chantier *` and `uv run --script * *` (an older form) in the home
  settings and sees P10 warn naming all three, with their replacing rules, preflight exiting 0.
- Gates owed (`AGENTS.md`): `just check`, `just eval-dry-run` (the CLI's `src/` changes), and the
  pipeline's `just scenario (ubuntu-latest)` job at the PR's head. No `hooks/` or `types/` change.

## Open questions for the user

1. **A stale rule in dev mode.** Q20 names a rule pointing at an old copy of the plugin. In plugin
   mode any other plugin path is taken as an old copy. In dev mode a user may keep several
   checkouts of chantier, so this spec names a dev rule as stale only when its folder no longer
   exists, and leaves alone a dev rule of another checkout that still exists. Is that the
   intended scope?
