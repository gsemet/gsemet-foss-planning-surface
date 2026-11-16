# Change Specification: an optional `chantier.yaml` playbook, parsed and resolved by the CLI

## Goal

The user's words (`intake/request.md`): a finer configuration of chantier than what is detected
from `AGENTS.md` today, so that:

- the Chief of Staff finds, with no ambiguity, which agent runs each role, the user's own Drivers
  included;
- a project picks the model a role runs without declaring a custom agent (today the model is
  fixed in each plugin agent's frontmatter);
- a project declares the skills or tools a role needs (for example a skill to reach Jira).

The answer of the grill (`02-answers.md`): an optional `chantier.yaml` at the project's root,
parsed, validated and resolved by the CLI, never by an agent. With no `chantier.yaml`, chantier
works exactly as today.

## Decisions carried from `02-answers.md`

| Decision (02-answers.md) | Where this spec carries it |
| --- | --- |
| The fine configuration lives in a dedicated file, not in `AGENTS.md` (2026-11-10, Q1) | "The file" |
| This amends the rule "the user's `AGENTS.md` is the only configuration" | "The rule, amended" |
| `chantier.yaml` at the project's root, YAML, structured, validated by the CLI (Q2) | "The file", "The CLI" |
| Optional: with no `chantier.yaml`, chantier works as today (Q2) | "The file", evidence S1 |
| Per role: the agent (the user's own Drivers included), the model, the required skills or tools (restatement) | "The file", schema |
| A model is passed by the parent at the agent's start; nothing set means the agent file's model (2026-11-07) | "Starting an agent" |
| A host that cannot set a model at start refuses clearly, no workaround (2026-11-07, restatement) | "The CLI", host capability |
| A missing required skill or tool: the Chief of Staff warns the user, naming it, and the role works without it (Q3) | "Required skills and tools" |
| Kept apart from "no fallback": the role works without the missing skill, never with a look-alike or a workaround (Q3) | "Required skills and tools", concepts rule 2 |
| The CLI parses and validates `chantier.yaml`, never an agent (the user's warning) | "The CLI" |
| The CLI resolves each role's model to its exact identifier and refuses an unknown or ambiguous name (same) | "Model resolution" |
| The parent passes the model exactly as the CLI printed it, never reading or interpreting the name itself (same) | "Starting an agent" |

## The file

- Path: `chantier.yaml` at the project's root, the folder `Repo.root` names
  (`skills/chantier/scripts/cli/src/chantier/state.py`). With a planning surface: see open
  question 1.
- Optional. Absent: every role runs the plugin's agent with the model of its file, exactly as
  today; no command prints an error or a warning about its absence.
- chantier never writes it. The user writes it, or the Chief of Staff on the user's word, like the
  `chantier` section of `AGENTS.md` today. It is the user's file, committed in the project like
  `AGENTS.md`; chantier still writes only in the planning folder.
- Encoding UTF-8; a leading BOM is ignored (Windows editors write one).

### Schema

```yaml
# chantier.yaml: optional; every key below is optional
roles:
  coder:
    agent: rust-coder          # the agent id the host knows; absent: the plugin's agent
    model: opus                # a model name, resolved by the CLI; absent: the agent file's model
    skills: [jira]             # skills the role needs
    tools:                     # tools the role needs
      - mcp__atlassian__getJiraIssue
  cr-driver:
    agent: my-driver           # a user's own Driver; it keeps driver.md as its card
  inspector:
    model: claude-opus-5-5
```

- One top-level key, `roles`. Any other top-level key is refused.
- A key under `roles` is a role: the name of one of the plugin's agents for the host, read from the
  files the plugin installs (`agents/<role>.md` on Claude Code,
  `com.github.copilot/agents/chantier-<role>.agent.md` on Copilot), the same files preflight's P4
  reads in `_agent_problems` (`commands.py`). The CLI keeps knowing no role: the list comes from
  the installed files, not from code. An unknown key is refused with the known names.
- Under a role, four keys, each optional, any other refused: `agent` (one string), `model` (one
  string), `skills` (a list of strings), `tools` (a list of strings). A role with none of them is
  refused (an empty entry is a typo).
- `agent` names the agent id the host knows (its reference, row "Agent ids of the project"). The
  CLI checks its form only (non-empty, no whitespace); see open question 4 for its existence. A
  built-in role run by another agent keeps its card, as today (`chief-of-staff.md`, "The project").
  A user's agent for a Driver role needs the tools a Driver uses (`Agent`, `SendMessage`, ...):
  the user's to provide; a start the host refuses is a stop (concepts rule 7).

### The YAML the CLI reads

The CLI has no dependency (`AGENTS.md`), so it reads a strict subset of YAML with the standard
library, next to `read_keyed` in `state.py`, and refuses anything outside it with the file, the
line number and what was found:

- block mappings indented with spaces (a tab is refused); keys `[a-z0-9-]+` or the tool names
  above (`[A-Za-z0-9_.:-]+`);
- scalars: plain, `'single'` or `"double"` quoted (in double quotes only `\"` and `\\`);
- lists: block (`- item`) or flow (`[a, b]`) of scalars;
- comments: `#` at a line's start or after whitespace; blank lines;
- refused: anchors (`&`), aliases (`*`), tags (`!`), block scalars (`|`, `>`), flow mappings
  (`{}`), a duplicate key, several documents (`---`).

## The CLI

All under `skills/chantier/scripts/cli/src/chantier/`. A new module, e.g. `playbook.py`, holds the
reader, the validation, the model table and the resolution; `commands.py` and `cli.py` call it.

### `$CHANTIER playbook [--host claude|copilot] [--batch <batch>]`

A new command (`cli.py`, `_parser`), in `FULL_OUTPUT` (it prints one line per role, more than
ten). No `--batch`: reads `chantier.yaml` now, for the host `detect_host` gives (or `--host`).
With `--batch`: prints the playbook the batch recorded at `open` (below), and reads no file.

Output, one line per role of the plugin, in the order of the installed files, then one line per
need:

```text
playbook: chantier.yaml, valid, host claude
coder: agent=rust-coder model=<start value> (Claude Opus 5.5) skills=jira tools=mcp__atlassian__getJiraIssue
cr-driver: agent=my-driver model=(its file's)
inspector: agent=chantier:inspector model=<start value> (Claude Opus 5.5)
investigator: agent=chantier:investigator model=(its file's)
...
```

- `agent=` is the exact id to pass: the configured one, else the plugin's (`chantier:<role>` on
  Claude Code, `chantier-<role>` on Copilot, the names the hosts' references give).
- `model=` is the exact value to pass at the start (below), with the model's display name in
  parentheses for the reader; `(its file's)` when none is configured: then no model is passed.
- No `chantier.yaml`: the first line says `playbook: no chantier.yaml, the plugin's agents and
  models`, and every role shows its plugin agent and `(its file's)`. Exit 0.
- Invalid: exit 2 (precondition), every problem found listed, each with its line, e.g.
  `chantier.yaml:4: role "codr" is not one of the plugin's agents: coder, cr-driver, ...`.

### Model resolution

The user's warning: agents mix up close model names ("Opus 5.6" and "5.6"), so the CLI alone turns
a name into an identifier.

- A table in the CLI, per host, lists each model it knows: its exact identifier, its display name,
  and its start value on that host. Seeded from what the plugin's agent files already name:
  - Claude Code: `claude-opus-5-5` (Claude Opus 5.5), `claude-sonnet-5-5` (Claude Sonnet 5.5),
    `claude-haiku-5-5` (Claude Haiku 5.5), the models `costs.PRICE` prices.
  - Copilot: the `[display name, id]` pairs of `com.github.copilot/agents/*.agent.md`:
    `claude-opus-5.5`, `claude-sonnet-5.5`, `gpt-5.6-luna`, `gpt-6.1-sol`.
- Normalising a name: lower case, every run of characters other than letters and digits becomes
  one `-` (`Opus 5.5` → `opus-5-5`; `claude-opus-5.5` → `claude-opus-5-5`).
- A name resolves to the table's entries whose normalised identifier or display name equals it;
  failing that, to those whose normalised identifier contains it as whole dash-separated parts
  (`opus` and `opus-5-5` match `claude-opus-5-5`; `opus-5-6` matches nothing).
- One entry: resolved, printed with its exact identifier's start value. None: refused as unknown,
  listing the host's models. Several: refused as ambiguous, listing them (`5.5` on Claude Code:
  Opus, Sonnet and Haiku; `gpt` on Copilot: Luna and Sol). A name with no letter (`5.6`) is
  refused: "name the model, not only its version".
- A new model reaches the table by a chantier release, like a new price in `costs.PRICE`: the
  table is the only source (see open question 3).

### Host capability: a model at start

- The table records, per host, whether a start of an agent takes a model and the value it takes
  (the "start value"). It follows the host's reference: a host whose reference does not mark
  that capability **proved** has none.
- A model configured on a host with no such capability is refused by `playbook`, `open` and
  preflight, clearly: `chantier.yaml:<line>: <host> cannot set a model when it starts an agent
  (hosts/<host>.md, "Models"): remove "model" for <role>, or run the role with your own agent
  that names it`. No other way is offered or tried.
- Claude Code: whether `Agent` takes a model, and which value (the full identifier, or only an
  alias such as `opus`), is not recorded (its reference says "no model, no effort" today). The
  Driver of this CR runs the trial first: start a plugin agent with a model passed, read the model
  its transcript shows, and record the row with its mark and date in `hosts/claude-code.md`. The
  start value is what the trial proved. If the tool takes only an alias, see open question 2
  before going on.
- Copilot: no trial is in this CR's reach (no Copilot host in the batch); the capability stays
  "none" and `hosts/copilot.md` says so, with the trial that would settle it.

### `open`, `take`, `round`, `handoff`

- `open` (`commands.open_batch`) reads and resolves `chantier.yaml` for the detected host before
  it moves any folder; invalid: exit 2 with the problems, nothing moved (the `failed_opening`
  path of the scenario). Valid: the resolved playbook (host, and per configured role its agent,
  model start value and display name, skills, tools) goes into `batch.json`, next to the batch's
  settings. A running batch keeps the playbook it opened with, whatever changes in the file since
  (as `apply_batch_settings` does for the settings, and as the team today). No `chantier.yaml`:
  nothing recorded, and the batch runs as today.
- `take`, `round` and `handoff` print, after their other lines, one line per configured role:
  `team: <role> agent=<id> model=<start value> (<display name>) skills=<...> tools=<...>`
  (only the keys set). No configured role: no `team:` line, as today.
- Preflight (`commands.preflight`): a new check P12, `chantier.yaml`: `ok` when absent (`no
  chantier.yaml: the plugin's agents and models`) or valid (`chantier.yaml valid: <n> roles
  configured`); `FAIL` when invalid, with the first problem and "run `$CHANTIER playbook`".
  Preflight being all or nothing, an invalid file starts no batch.
- `init` and `file` are unchanged; no command writes `chantier.yaml`.

## Starting an agent

`concepts.md`, "Starting an agent" today says the parent "passes no model and no effort". New
text, in substance:

- The parent passes the agent and, when one is printed, the model, exactly as `$CHANTIER`
  printed them (`playbook`, `playbook --batch`, or the `team:` lines of `take`, `round`,
  `handoff`): copied as printed, never typed from memory, completed, shortened or "corrected".
  No model printed: no model passed, the agent file's model runs. Never an effort.
- Who reads what:
  - the Chief of Staff, for its own subagents (the Spec-writer, the Demo explorer), reads
    `$CHANTIER playbook`;
  - the Foreman (or the Chief of Staff in direct mode), for a Driver, reads `$CHANTIER playbook
    --batch <batch>`;
  - a Driver, for a worker, reads the `team:` lines of `take`, `round` or `handoff`.
- The prompt's `Team:` line (concepts, the Driver's prompt; `chief-of-staff.md`, the Foreman's
  prompt) carries those lines as printed, plus the review steps of the `AGENTS.md` section (open
  question 5).
- A start the host refuses with a model (an unknown value, a capability the trial did not cover)
  is reported with its exact text (rule 7): `handback blocked refused <text>` for a Driver, an ask
  for the Foreman, said to the user by the Chief of Staff. Never retried without the model, never
  with another model.
- When the agent needs skills or tools, its prompt gets one more line, as printed:
  `Needs: skills <...>; tools <...>`.

## Required skills and tools

- What the playbook gives: the names of the skills and tools a role needs, so the agent knows to
  use them (the `Needs:` line), and the Chief of Staff can check them.
- The check: the Chief of Staff, at its first turn's preflight and at step 1 of "Starting a batch"
  (and before it starts its own subagent), compares each need with the skills and tools its own
  session has. Each one it cannot find, it tells the user in one line: `<role> needs the skill
  <name>: not found in this session; <role> works without it.` A warning, never a preflight fail:
  nothing blocks.
- How a session sees its skills and tools is the host's: each host's reference gets a row,
  marked **unproved** until a trial records it (trial: a `chantier.yaml` naming one skill that is
  installed and one that is not; the Chief of Staff names only the second). Whether a subagent
  sees what the Chief of Staff's session sees is part of open question 6.
- At work: an agent whose `Needs:` names something it does not have says so in a note (a Driver:
  `$CHANTIER note`) and does its part without it.
- Kept apart from "no fallback" (concepts rule 2, `chief-of-staff.md` "Hard rules"): a missing
  need is a capability the role goes without, warned and noted; it never makes the role reach the
  same thing by another means. With the Jira skill missing, the role does not call Jira's API with
  `curl`, a browser or another skill: it works from what the CR already holds. Rule 2 gets one
  sentence saying this.

## The rule, amended

On the user's word (`02-answers.md`, Q1), the configuration is `AGENTS.md` plus, optional,
`chantier.yaml`. The same sentence changes in each place it is written:

- `AGENTS.md` (this repository), the line "The plugin must work with no setup: the user's
  `AGENTS.md` is the only configuration, ..." becomes: "The plugin must work with no setup: the
  user's `AGENTS.md`, and an optional `chantier.yaml` at the project's root, are the only
  configuration; with no `chantier.yaml` chantier runs as if it were empty; ..." (the rest of the
  line unchanged: chantier writes only in the planning folder).
- `README.md` line 14 ("Zero configuration"), `skills/chantier/SKILL.md`,
  `skills/chief-of-staff/SKILL.md`, `skills/griller/SKILL.md`, `skills/status/SKILL.md` (the
  "only configuration" sentence each), `skills/chantier/references/session-start.md` ("Zero
  configuration" in the introduction): the same amendment, in their own words.
- `chief-of-staff.md`, "The project": "Nothing is configured anywhere else" becomes "nothing
  else is configured except `chantier.yaml`"; the paragraph "The team" says the agent and model
  of a role come from `chantier.yaml` through `$CHANTIER playbook`, and the entry row "use my agent
  for <role>", "which models?" points to `chantier.yaml`, edited only on the user's word, then
  `$CHANTIER playbook` to show the result. "The host's reference says which model each role runs"
  becomes "its file's model, unless `$CHANTIER playbook` prints another".

## Cards and references touched

- `skills/chantier/references/concepts.md`: "Starting an agent" (above); rule 2, the one sentence
  on needs; the `Team:` and `Needs:` lines of the prompt template.
- `skills/chantier/references/chief-of-staff.md`: entry row, "The project", "Starting a batch"
  (step 1: the needs warning; step 2: the plan shows the playbook; the Foreman's prompt `Team:`
  line), the Spec-writer's and Demo explorer's start with the model printed.
- `skills/chantier/references/foreman.md`: a Driver's start reads `playbook --batch`.
- `skills/chantier/references/driver.md`, "Your means": the worker's agent and model from the
  `team:` lines, passed as printed; a missing need noted.
- `skills/chantier/references/hosts/claude-code.md`: rows "Start a Driver or a worker", "Start
  the Spec-writer", "Models" (the trial's result, mark and date), and a row for how a session sees
  its skills and tools (unproved).
- `skills/chantier/references/hosts/copilot.md`: the same rows; the model capability "none,
  unproved", with its trial.
- The agent files (`agents/`, `com.github.copilot/agents/`): unchanged, unless open question 6
  is answered otherwise (then both hosts together, bodies identical).

## Docs

- `docs/tutorial-claude-code.md`, section 8 "Make the team yours": `chantier.yaml` for agents,
  models and needs, an example, `$CHANTIER playbook` (or "which agents and models?") to see it;
  the default models paragraph kept.
- `docs/use-cases.md` (lines ~152 to 165, the team): the same.
- `README.md`: the "Zero configuration" bullet (above), and one line naming `chantier.yaml`.

## Out of scope

- The Foreman's and the Chief of Staff's own models (sessions, not plugin agents): see open
  question 7.
- An effort per role.
- Checking that a configured agent exists (open question 4) or that a subagent can load a skill
  (open question 6) beyond what is written above.
- A `chantier.yaml` written by chantier, or a migration of the `AGENTS.md` section into it.
- Any change to the planning folder's layout, the batch lifecycle, the limits or the cost
  (`costs.PRICE` keeps its own table).
- Refreshing a running batch's playbook.

## Evidence

Checks, on Linux, macOS and Windows: `just check` passes. Structure tests
(`tests/test_structure.py`), few:

- every model named in an agent file's frontmatter, on each host, resolves in the CLI's table to
  itself (the table and the files cannot drift);
- the CLI's model table names no display name or identifier twice per host.

`just scenario` passes, with these steps added (`scenario/run_scenario.py`), each a `check`:

1. S1, no `chantier.yaml`: `playbook` exits 0 and prints the plugin's agents and `(its file's)`;
   preflight P12 ok; `open`, `take` and `handoff` print no `team:` line; the rest of the scenario
   unchanged.
2. S2, a valid file (`coder` with `model: opus`, `skills: [jira]`; `cr-driver` with `agent:
   my-driver`): `playbook` prints the resolved start value and display name (under the host
   capability the trial recorded; if Claude Code has none, the step instead checks the refusal of
   S5 and a file with no `model` key); `open` records it; `take` prints the `team:` lines;
   `playbook --batch` prints the same.
3. S3, the batch keeps its playbook: after `open`, `chantier.yaml` changes; `take` of another CR
   and `playbook --batch` still print the opening's.
4. S4, refusals, each exit 2 with its line number and nothing moved by `open`: an unknown role,
   an unknown key, an empty role, a tab, an anchor, a duplicate key, a model `opus 5.6` (unknown,
   listing the models), `5.5` (no letter), `gpt` with `--host copilot` (ambiguous, listing Luna and
   Sol); preflight P12 FAIL on the first.
5. S5, the host capability: a `model` with `--host copilot` is refused with the "cannot set a
   model when it starts an agent" message.
6. S6, with no `chantier.yaml` again, `open` of the next batch records nothing.

By hand, once, recorded in the hosts' references with date and mark: the Claude Code trial of a
model passed at an agent's start (above), and the needs check (a skill present and one missing:
only the missing one is warned).

## Open questions

1. **With a planning surface**, where is `chantier.yaml`: at the code repository's root (its
   clone, `Repo.root`), or in the project's folder of the surface (`<surface>/projects/<name>/`,
   next to `checkout.yml` and `project.md`)? Recommended: the code repository's root, so the
   project's team and its colleagues share it with `AGENTS.md`, in both modes.
2. **If Claude Code's `Agent` tool takes only an alias** (`opus`, `sonnet`, `haiku`) and not an
   exact identifier: the CLI would still resolve and print the exact model, but the start value
   would be the alias, whose meaning is the host's. Accept the alias as the start value (the CLI
   prints both), or count Claude Code as a host that cannot set an exact model, and refuse?
   Recommended: accept, printing both, only when the trial shows the alias runs the model the
   table names.
3. **A model the CLI's table does not know** (a newer one, before a chantier release): refused,
   as the answers say for an unknown name, even when written as an exact identifier? Recommended:
   refused; a new model comes with a release, like its price.
4. **A configured agent that does not exist**: the CLI cannot see every place a host loads agents
   from (other plugins among them), so this spec leaves it to the host, whose refused start is a
   stop. Should the CLI also warn when the id is not found in the project's and the user's agent
   folders the host's reference names? Recommended: no, the refusal is enough.
5. **The `chantier` section of `AGENTS.md`**, which today names an agent per role, extra review
   steps and the release procedure: once `chantier.yaml` exists, does an agent per role still
   come from `AGENTS.md`, and do the extra review steps move into `chantier.yaml`? Recommended:
   agents per role only in `chantier.yaml` (one place, no ambiguity); the review steps, the
   release pointer and the `planning:` line stay in `AGENTS.md`; the Chief of Staff tells the user
   when the section still names an agent for a role, and offers to move it.
6. **Skills and tools in the plugin's agents**: the plugin's agent files list their tools
   (`tools:` in each frontmatter, with no Skill tool and no MCP tool), so a plugin agent may be
   unable to use a required skill or an MCP tool at all, whatever the session has. Add them to
   every plugin agent (both hosts), leave the files as they are (a need is then met only by the
   user's own agent for the role, and the warning says so), or another way?
7. **The Foreman's model**: the Foreman is a session (started with `model: claude-opus-5-5`),
   not a plugin agent, so it has no role key in this schema. Should `chantier.yaml` set it too?
   Recommended: not in this CR.
