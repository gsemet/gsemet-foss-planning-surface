# Change Specification: optimise the startup core in size and efficiency

Short name: `startup-core-optimise`. No tracker issue (verbal, the user, 2026-11-18).

Stacks on `watcher-autostart` (`1-inbox/the-watcher-starts-on-its-own-with-a-run`), which lands
below it: that CR adds one line to `skills/chief-of-staff/SKILL.md`'s `## Startup core`, adds `, but
the watcher` to `session-start.md` "## 5. Reload", **Does**, and cuts two clauses of
`skills/chief-of-staff/SKILL.md`. This CR keeps all three as they land and rebases on them.

Folds in `portable-cli-invocation` (`2-backlog/P2/portable-cli-invocation`, settled by the Chief of
Staff on 2026-11-18): its one rule and its test land here (section 1 and Evidence 4). That CR
stays in the backlog until this one merges, then is closed as done here (its own `02-answers.md`
says so).

## Goal

Every session and agent reads the startup core whole at each boot and reload. The user, 2026-11-18:
« Je suis d'accord pour que la limite à 12K reste, il faut que ce noyau soit optimisé en taille et
en efficacité. » Wanted: the limit kept, and the core smaller and more effective: the rules that
matter at boot said once, clearly and first; what one action needs read at that action.

## Decisions carried from `02-answers.md`

1. The limit stays 12,544 in its three places (`startup-manifest.json` `limit`, `STARTUP_LIMIT` in
   `tests/test_startup_manifest.py` and in `tests/test_plugin_files.py`); none is edited. This CR
   lowers what each role reads.
2. Target: the tightest role and host, at boot and at reload, ends at most 11,290 bytes (10% under
   the limit), measured by `test_startup_manifest_measures_every_real_role_and_host`; the PR gives
   the before and after table for every role and host (Evidence 1).
3. Size: a rule said in two core files is said once, where every role that needs it reads it;
   restatements of what a deferred card holds go; wording that adds no rule goes. No rule is
   dropped.
4. Efficiency: the core holds only what a role needs before its first action or at every turn; a
   rule tied to one action moves to the card section that action reads (the manifest's action
   readings), with a one-line pointer only where the action could be missed. The rules that must
   never be missed (stop on a CLI failure, the watcher's start, the seat, no fallback) stay in the
   core, first in their file.
5. Each moved or merged rule is listed in the PR's delivery with where it now lives ("Moved and
   merged rules" below is that list); a structure test checks each is still present there.
6. Both hosts' agent files keep identical bodies (`AGENTS.md`).
7. It stacks after `watcher-autostart` and keeps its startup line.
8. `portable-cli-invocation` folded in: "Write `$CHANTIER` out in full, as given, in each shell
   call, never in a shell variable" goes into `startup-core.md`, with its test, counted in the
   budget table.

Two readings of decision 4, stated so the Chief of Staff can overrule them:

- "No fallback" is not in any core file today (it is in `concepts.md` rule 2, `chief-of-staff.md`
  and each worker card). Since the answers name it among the rules that stay in the core, this CR
  writes it once in `startup-core.md`, second after the CLI stop; the cards keep theirs.
- "The seat" in the core today is the router's two seat bullets (`skills/chantier/SKILL.md`) and
  "no seat" in the CLI stop. Those stay, the router's moved first in its file. The Chief of Staff's
  and the Griller's seat rule stays where it is (`session-start.md` "## 2. The seat and the role",
  read at their first action, and "## 5. Reload", read at a reload).

## Where the bytes are today

Measured at main (3a9afc2c), LF bytes, the test's own count (`pytest -s -k measures`):

| Piece | Read by | Bytes |
| --- | --- | --- |
| `startup-manifest.json` | every role, boot and reload | 6,905 |
| `skills/<skill>/SKILL.md` (wrapper of the four skill roles) | that role | about 2,550 to 2,850 |
| `startup-core.md` | every role | 1,623 |
| an agent file (wrapper) | that role, its host | about 1,050 to 1,500 |
| `session-start.md` "## 5. Reload" | every role, reload only | 743 |
| a host core | every role on that host | about 230 |
| `role-core.md` | every role | 170 |
| a card's `## Startup core` boilerplate | each role | about 140 |

Tightest at main: `chief-of-staff` on Copilot, reload 12,544; the router on Copilot, reload 12,502.
`watcher-autostart`'s own table puts them at about 12,481 and 12,519 after it lands. The manifest
is more than half of every role's boot reading: most of it is the path prefix
`skills/chantier/references/` written about 70 times, and a `mandatory_sections` entry per role
that repeats the role's card and the same heading.

## What changes

### 1. `skills/chantier/references/startup-core.md`: the common core

Rewritten to this text (the Driver may reword further, never dropping a rule; every phrase
`tests/test_cli_stop.py` guards stays, word for word: "in either mode, at any call", "report the
exact error and stop", "no seat", "nothing written in the planning folder", "retry once only on a
transient network error", "the launch fails", "keep their handling", "The CLI is never a tool a
role works without"):

```markdown
# Chantier startup core

`$CHANTIER` is the CLI, prepared only as your skill or prompt gives it. Write `$CHANTIER` out in
full, as given, in each shell call, never in a shell variable. If it cannot run (the launch
fails: uv or uvx cannot set it up or start it, or the CLI crashes on start), in either mode, at
any call, report the exact error and stop: no work as the role, no seat, nothing written in the
planning folder, never "without it". Do not upgrade, reinstall, repair, relaunch another way, or
choose another source or tool; retry once only on a transient network error. A steering session
tells the user; a started agent ends its turn with the error as plain text. A CLI refusal, a
command's own error exit and a host's permission denial keep their handling. The CLI is never a
tool a role works without.

No fallback: a tool, a model, an agent or a `$CHANTIER` command not available exactly as named is
a stop, reported with its error; never a look-alike, a workaround or an estimate. A skill or tool
the playbook names and the session lacks is not a stop: your card says how.

Other checks are read-only and block only the actions whose prerequisite failed. Permissions are
scoped to this session, project and effect; a started agent inherits only its role's, never merge
or publication permission. Report role, project, checked state, blocked actions and causes,
pending permissions, authorized effects and evidence limits: failed, unavailable or not
performed; available, documented, exercised, server-announced, not tested or skipped. Never
invent capacity: a host path not exercised is labelled untested.

Before an action, read every reading the manifest lists for it; one that cannot be read blocks
that action only.
```

Measured as drafted: 1,735 bytes (+112): the shell-variable rule and the no-fallback rule added,
paid by the cuts below. What left this file: its opening paragraph (the deferral rule, now said
once in `role-core.md`), "Run the official `$CHANTIER` preparation for the selected source and
version" (now "prepared only as your skill or prompt gives it"), "Reload does not repeat grants or
duplicate services" (moved to "## 5. Reload"), and the two "distinguish" lists merged into the
report sentence.

The shell-variable rule (`portable-cli-invocation`): the literal command as `cli_command()`
(`skills/chantier/scripts/cli/src/chantier/plugin_files.py`) and the `cli:` lines print it works
unchanged in bash, zsh, sh, dash and PowerShell, and is the only form the host permission rules
(`hosts/claude-code.md`: `uv run --no-sync --project * chantier *`, `uvx --from * chantier *`)
match; a variable breaks in zsh ("command not found"), PowerShell ("not recognized as the name of
a cmdlet") and, with a quoted path, bash (the quotes stay characters). It covers the whole command
and any part of it (the plugin root too). It is not repeated in the four `SKILL.md` files nor in
the `cli:` lines; the CLI does not change; `evals/kit/audit.py`'s `CLI_CALL` keeps reading a call
through a variable.

### 2. `skills/chantier/references/role-core.md`: the deferral rule, once

The deferral rule is said today in `startup-core.md`'s opening, in `role-core.md`, in every agent
file, in every card's `## Startup core` boilerplate ("Read this short role contract at boot. Load
the complete card only before an action listed in the startup manifest."), in each `SKILL.md`
("Read [concepts] ... only when their action requires them"), in `concepts.md`'s and both host
cards' `## Startup core`. It is said once, here, which every role reads:

```markdown
# Role startup core

At boot read only the cores, your wrapper and the startup sections the manifest lists for your
role; read the rest of a card only before an action whose readings name it.
```

### 3. Host cores: `host-core-claude-code.md`, `host-core-copilot.md`

Each keeps its title and its first sentence (the host provides the documented tools described by
the deferred host reference). "Availability is not proof that a path was exercised; label
untested host behavior as untested." goes: said once in `startup-core.md` ("a host path not
exercised is labelled untested"), which every role on both hosts reads.

### 4. `skills/chantier/references/startup-manifest.json`: compact, same content

`version` becomes `2`. The same lists, written without repetition; only the tests and the agents
read this file (no CLI code does: `driver_prompt.py` only names it). The format:

- Every path is relative to the manifest's own folder (`skills/chantier/references/`), said in a
  `"paths"` key. A reading is a file, or `file#heading` for that file's level-2 section `## heading`
  (every section reading today is level 2). A host-specific reading is an object
  `{"claude": <reading>, "copilot": <reading>}`.
- `mandatory_sections` becomes `startup_sections`, listing only the roles whose card has a startup
  section (after section 5 below: the four Driver roles, `driver.md#Startup core`; the Foreman,
  `concepts.md#Startup core` and the two host cards' `#Startup core`). A role absent from it has
  none: its wrapper is its boot reading.
- `roles`, `entries`, `hosts` and `actions` keep their keys and their content, with the shorter
  paths.

A draft (the Driver may lay it out otherwise; same content, the measure decides):

```json
{
  "version": 2,
  "limit": 12544,
  "paths": "relative to this file's folder; a reading is a file, or file#heading for its level-2 section",
  "manifest": "startup-manifest.json",
  "common": "startup-core.md",
  "role_core": "role-core.md",
  "hosts": {
    "claude": {"core": "host-core-claude-code.md", "wrappers": "../../../agents"},
    "copilot": {"core": "host-core-copilot.md", "wrappers": "../../../com.github.copilot/agents"}
  },
  "entries": {"foreman": {"wrapper": null, "prompt_builder": "chief-of-staff.md"}},
  "roles": {
    "cr-driver": "driver.md",
    "...": "one line per role as today, e.g. \"chief-of-staff\": \"../../chief-of-staff/SKILL.md\", \"router\": \"../SKILL.md\""
  },
  "startup_sections": {
    "cr-driver": ["driver.md#Startup core"],
    "stack-driver": ["driver.md#Startup core"],
    "qa-driver": ["driver.md#Startup core"],
    "release-driver": ["driver.md#Startup core"],
    "foreman": ["concepts.md#Startup core", {"claude": "hosts/claude-code.md#Startup core", "copilot": "hosts/copilot.md#Startup core"}]
  },
  "actions": {
    "route": ["routing.md", "../SKILL.md", "session-start.md"],
    "reload": ["startup-core.md", "role-core.md", "startup-manifest.json", "session-start.md#5. Reload"],
    "cr-driver": ["driver.md#Your means", "driver.md#CR driver"],
    "...": "every other action of today, one line each, the same readings"
  }
}
```

The full draft, every role and action written out, measured 2,808 bytes (from 6,905: about
-4,100 for every role, boot and reload).

### 5. The cards' `## Startup core` sections

- Every card that carries the boilerplate line "Read this short role contract at boot. Load the
  complete card only before an action listed in the startup manifest." loses it (it restates
  `role-core.md`): `coder.md`, `conflict-resolver.md`, `debugger.md`, `demo-explorer.md`,
  `driver.md`, `foreman.md`, `inspector.md`, `investigator.md`, `retro-critic.md`,
  `spec-critic.md`, `spec-writer.md`, `verifier.md` (under `skills/chantier/references/`).
- A section left empty loses its heading too (all of them but `driver.md`'s, which keeps "A `Note:
  resume: closing` reads only the CR's notes, as the opening reading rules list."). A worker's card
  is read whole at its action, which starts at once (its agent file: "Your card is `<role>.md`:
  read it first").
- `concepts.md` "## Startup core" keeps only "At startup, identify the role, batch, project and
  parent session." Its "Read only this core, ... defer the rest until an action names it." goes
  (restates `role-core.md`). "A prompt must name the card and section it expects the role to
  read." moves to the section on how an agent is started (beside the prompt template, ~line 455),
  the reading of whoever starts an agent. The paragraph "The steering sessions and the Drivers read
  this file: ..." moves, unchanged, above the `## Startup core` heading (the card's introduction,
  not a boot rule).
- `hosts/claude-code.md` and `hosts/copilot.md` "## Startup core": "Read only this section at
  boot; defer session, worktree and capability procedures until the action names them." goes
  (restates `role-core.md`). The paragraph "What is proper to this host: ... Read it with your card
  when you run on <host>." moves, unchanged, above the `## Startup core` heading. The marks (Claude
  Code) and the "unproved" paragraph (Copilot) stay in the section: the Foreman reports with them.

### 6. The agent files (`agents/*.md`, `com.github.copilot/agents/*.agent.md`)

In every agent file, both hosts, the sentence

> Read the startup core and the short Startup core section of your card first; defer all other card sections until the action names them, then do only your role's part and reply as your card says.

becomes

> Read the startup core first, and your card's `## Startup core` section when it has one; then do only your role's part and reply as your card says.

Nothing else in them changes (descriptions, refusal lines, "Your card is ..." lines: all tested by
`test_plugin_files.py`). Each role's two bodies stay identical.

### 7. The four `SKILL.md` files: the key rule first

Each keeps its frontmatter, title, `chantier-version:` line and its `$CHANTIER` paragraph as it
stands after `watcher-autostart` (every form `test_one_launch_two_modes_one_text` and
`test_cli_stop.py` require stays: "uv run --no-sync --project", "uv sync --locked --project",
"uvx --from", "--skill", ".git", "Any failure of the sync or of `$CHANTIER`, in either mode, at
any call, follows `startup-core.md`"). Then, in each, a `## Startup core` heading follows the
`$CHANTIER` paragraph directly, and the rest of the body sits under it, the role's key rule first.
The trailing boilerplate `## Startup core` at the end of each file goes.

- `skills/chief-of-staff/SKILL.md`: under `## Startup core`, first, `watcher-autostart`'s line
  ("A `watch: not running` line in any output, a reload's too: start the watcher now, on the
  session's yes; run the printed command as is: no flag added."), then the rest. "Read the common
  core, host core, role core and wrapper named by [startup-manifest.json](...). Read
  [concepts](...), [session-start](...) and [chief-of-staff](...) only when their action requires
  them." becomes "You are the **Chief of Staff**; your startup reading is named by
  [startup-manifest.json](../chantier/references/startup-manifest.json)." (the deferral half is
  `role-core.md`'s; the cards are the manifest's action readings). The mode word sentence and the
  `reload` sentence stay.
- `skills/chantier/SKILL.md` (the router): under `## Startup core`, first, the two seat bullets
  ("With **no live Chief of Staff in the seat** ...", "With a **live Chief of Staff in the seat**
  ..."), then the `reload` sentence, then the manifest pointer, shortened as above. The paragraph
  "Nothing to install but `uv`: ..." goes but its last sentence ("In a planning surface,
  `$CHANTIER` also carries `--project <the project's folder>`."), which joins the `$CHANTIER`
  paragraph: the router writes nothing, and the zero-configuration rule is `session-start.md`'s
  "Zero configuration" (read at the router's `route` action).
- `skills/griller/SKILL.md`: as `watcher-autostart` does for the Chief of Staff: "Nothing to
  install or set up but `uv`: the project's `AGENTS.md`, and an optional `chantier.yaml` (...),
  are the only configuration, and" goes; kept: "everything chantier writes goes to the planning
  folder (...), and, when the project asks for it, a CR's archive in its PR", and the `--project`
  sentence. Under `## Startup core`, first, "You are a **Griller**", the manifest pointer
  shortened as above, then the `reload` sentence.
- `skills/status/SKILL.md`: "Nothing to install or set up but `uv`: ... are the only
  configuration." goes (status writes nothing; "You change nothing" stays). Under `## Startup
  core`, first, "You change nothing: no order, no heartbeat, no epoch, no file." (moved up from the
  end), then the manifest pointer, the "Read [status-layout] only for the status action, and
  nothing else of chantier ..." rule (kept whole: it is a rule, not a restatement), the three steps
  and the rest. The status skill's only action starts at boot, so its steps stay here.

### 8. Where moved rules land

- `session-start.md` "## 5. Reload", **Does**: gains "It repeats no grant and starts no service
  twice." (from `startup-core.md`).
- `session-start.md` "## 4. First turn", **Zero configuration**: gains, after "in the planning
  folder ... in its planning surface)", ", and a CR's archive in its PR when the project asks" so
  the archive clause the router's and status's `SKILL.md` drop is said there (it already holds the
  rest).
- `concepts.md`, beside the prompt template: "A prompt names the card and section it expects the
  role to read."

## Moved and merged rules

The PR's delivery carries this list as it lands (the Driver updates it to the final wording):

| Rule | Was | Now |
| --- | --- | --- |
| Read at boot only the core; the rest of a card at its action (deferral) | `startup-core.md` opening, `role-core.md`, every agent file, every card's `## Startup core` boilerplate, each `SKILL.md`, `concepts.md` and both host cards' `## Startup core` | `role-core.md`, once |
| Reload repeats no grant and starts no service twice | `startup-core.md` | `session-start.md` "## 5. Reload", **Does** |
| A host path not exercised is labelled untested | both host cores | `startup-core.md` |
| Distinguish failed / unavailable / not performed; available / documented / exercised / server-announced / not tested / skipped | `startup-core.md`, two sentences | `startup-core.md`, the report sentence |
| `$CHANTIER` prepared only as the skill or prompt gives it | `startup-core.md` ("Run the official `$CHANTIER` preparation ...") | `startup-core.md`, reworded |
| No fallback | `concepts.md` rule 2, `chief-of-staff.md`, worker cards (not in the core) | also `startup-core.md`, second paragraph |
| Write `$CHANTIER` in full, never in a shell variable | nowhere (`portable-cli-invocation`) | `startup-core.md`, first paragraph |
| Zero configuration, a CR's archive in its PR when the project asks | router's, Griller's and status's `SKILL.md` | `session-start.md` "Zero configuration" (the Griller keeps its writes sentence) |
| A prompt names the card and section the role reads | `concepts.md` "## Startup core" | `concepts.md`, how an agent is started |
| concepts' introduction; the host cards' "What is proper to this host" | inside their `## Startup core` | above it, unchanged |
| The router's seat rule; the Chief of Staff's watcher line; status's "You change nothing" | in the body / at the end | first under each `SKILL.md`'s `## Startup core` |

## Expected result

Estimated after `watcher-autostart` and this CR (the Driver measures; the table it gives is the
truth): every role about 4,300 to 4,600 bytes lower at boot and reload; the Chief of Staff and the
router on Copilot, reload, about 8,100 to 8,300; no role above 9,000. The goal (at most 11,290 for
every role and host, boot and reload) holds with room. If the measure leaves any role above
11,290 without dropping a rule, the Driver stops `blocked` with the measured table.

## Host and default matrix

The startup reading depends on the host (each host has its core and its agent file); it does not
depend on a configured value. The measure covers every cell:

- Claude Code: every role, boot and reload (`test_startup_manifest_measures_every_real_role_and_host[claude]`).
- Copilot: every role, boot and reload (`...[copilot]`).

## Out of scope

- Raising or lowering the limit.
- The prompt line `driver_prompt.py` and `concepts.md`'s prompt template print ("Read
  .../startup-core.md, the host core, role core, and the short startup section named by
  .../startup-manifest.json; defer the rest until an action names it."): still true, and a CLI
  `src/` change is not needed.
- The `$CHANTIER` paragraph of the four `SKILL.md` files (beyond `watcher-autostart`'s cut and the
  `--project` sentence joining it).
- The deferred cards' content beyond the lines named above; `session-start.md`'s own opening
  ("This card is deferred action guidance ...") is not core reading and stays.
- Any CLI change; an eval check flagging a CLI call through a variable; a wrapper script or shell
  function for the CLI.
- The CR board pane and `STATUS.json`: nothing they show changes; no pane screenshot is owed.

## Evidence

Tests (`skills/chantier/scripts/cli/tests/`, in-process, few, parametrized), every one reading the
shipped files from the repository at the head under test, never a prepared text, except where
named:

1. `test_startup_manifest.py`, adapted to the version-2 manifest: paths resolved from the
   manifest's folder; `file#heading` read as the level-2 section `## heading`; a host object read
   for the host under test; `startup_sections` optional per role (a role with none measures its
   cores, manifest and wrapper); every listed section exists and holds more than its heading;
   `_check_actions` keeps its checks (each reading exists, reload's first three readings are the
   common core, the role core and the manifest, each Driver role's action reads `## Your means`
   and its own section), with the shorter paths; the Foreman still reads both host cards'
   `## Startup core`. The limit stays `STARTUP_LIMIT = 12_544` and `manifest["limit"] ==
   STARTUP_LIMIT`. `test_reload_budget_includes_additional_whole_file_readings` appends
   `"foreman.md"` (its prepared manifest is a refusal case the shipped file cannot hold).
   `test_reading_union_counts_lf_bytes_and_nested_sections_once` unchanged.
   The PR's delivery carries the table of `pytest -s -k measures`'s `startup-bytes` lines, every
   role and host, boot and reload, before (the base, `watcher-autostart` landed) and after.
2. A new parametrized test in `test_startup_manifest.py`, the moved rules: one case per row of
   "Moved and merged rules" whose text moves, `(phrase, file, heading or None)`, asserting the
   phrase is in that file's section (whitespace normalised as `test_cli_stop.py` does, sections
   read with `_section_span`), and, for each rule that left a core file, that the phrase is no
   longer there (the deferral boilerplate "Read this short role contract at boot" is in no file
   under `skills/`; "defer all other card sections" in no agent file).
3. The same test, the rules first: `startup-core.md`'s first paragraph after its title holds
   "report the exact error and stop" and "never in a shell variable", its second "No fallback";
   the first non-blank line under `## Startup core` of `skills/chief-of-staff/SKILL.md` holds
   "`watch: not running`", of `skills/chantier/SKILL.md` holds "live Chief of Staff in the seat",
   of `skills/status/SKILL.md` holds "You change nothing".
4. `test_plugin_files.py::test_one_launch_two_modes_one_text`, extended (no new function), from
   `portable-cli-invocation`: it reads the shipped `startup-core.md`, normalises whitespace and
   asserts it holds "never in a shell variable"; and for a dev root and a plugin root under
   `tmp_path / "with space"` (prepared folders: a case the shipped plugin cannot hold),
   `shlex.split(cli_command())` gives `["uv", "run", "--no-sync", "--project", <root as posix>,
   "chantier"]` and `["uvx", "--from", <root as posix>, "chantier", "--skill", <skill as posix>]`.
5. Unchanged and green: `test_cli_stop.py` (its startup-core phrases, the four `SKILL.md` pointer
   sentences), `test_plugin_files.py` (agent files: identical bodies per role, refusal lines, "Your
   card is `<role>.md`: read it first"), `watcher-autostart`'s structure test (the Chief of Staff's
   `## Startup core` holds its line).

`just test` stays within its budget (`AGENTS.md`).

Shells, for the folded rule (in the PR's delivery, one line each, the literal dev-mode command run
as `<cli> --version` from the Driver's machine, and the variable form where the shell is at hand):
PowerShell 5.1 (runs; the variable form fails, measured 2026-11-18), bash (runs; a quoted path in
a variable keeps its quotes), zsh (runs; "command not found" in a variable, or "not run" if zsh is
not at hand), sh/dash (runs).

Scenario: no step is added; the scenario's agents read the cards, and `just scenario` exercising
every role's boot from the new manifest and cores is the check that nothing an agent needs at boot
went missing.

Gates (`AGENTS.md`): the change touches the cards, the agent files, the manifest and the tests,
not the CLI's `src/` nor the eval kit: the Driver runs `just check` at the rebased head before the
first push (no `just eval-dry-run` owed); the pipeline's `just scenario (ubuntu-latest)` job is
green at the PR's head before the PR; no `hooks/` or `types/` change, no `just mod`.

## Open questions

None. (The two readings of decision 4 above are the Spec-writer's; the Chief of Staff may
overrule them.)
