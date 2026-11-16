# Change Specification: chantier's configuration in layers, and the shipped defaults

Date: 2026-11-16 (fifth run: Q20's spelling and Q23 carried, the open question closed; the CR was
split in three by Q18; this is (A), the first of the stack).
Sources: [intent](01-intent.md), [answers](02-answers.md) (Q1 to Q23 and the Chief of Staff's
decisions; they rank above the intent; Q19 supersedes Q2, Q16 removes any role setting shared by
all hosts, Q22 is C's), [original request](intake/request.md). No tracker issue.

## Depends on, and the stack

The stack, bottom to top: [copilot-role-models](../copilot-role-models/03-change-spec.md),
[copilot-model-catalog](../copilot-model-catalog/), this CR (A),
[role-model-per-host](../role-model-per-host/) (B, on A),
[board-config-page](../board-config-page/) (C, on A and B).

- copilot-role-models: the Copilot agent files' `model:` lines (Coder on Sol; Verifier, Debugger,
  Conflict resolver on Terra). The shipped defaults (section 2) copy them; this CR takes the agent
  files as they are on `main` (or on the branch below it in the stack).
- copilot-model-catalog: `MODELS["copilot"]` built from the copy of GitHub's tables. This CR
  resolves the configuration's model names against `MODELS[host]` and does not redo the catalog.
- B and C are written on top of this CR: B uses the per-host role view and the "default model"
  of section 3; C uses the layer view of section 1 (each value with its layer, and each reset).

## Goal

The user sets chantier's configuration without touching the plugin's installed files and without
losing it at an upgrade. It lives in plain YAML files in layers, from the plugin's shipped
defaults up to the project's own repository, merged node by node, so a layer carries only what it
changes, and a layer can take back what a weaker one set. Each role's settings are always per host
(Claude Code, Copilot), in every layer. The models each plugin role runs by default leave the code
and the agent files' memory: they are one shipped file, `config/chantier.defaults.yml`, kept equal
to the agent files by a test.

## Decisions carried from the grill

- Q1: `chantier.yaml` and `chantier.yml` are both accepted, in every place a user file is read.
  Both present in the same place is refused, with the two paths named.
- Q19 (supersedes Q2's order): the layers, weakest to strongest: the shipped
  `config/chantier.defaults.yml`; the surface root's `chantier.yaml` (all its projects);
  `projects/<name>/chantier.yaml` in the surface; the target project's (code repository's)
  `chantier.yaml`. Each layer is merged node by node: a layer carries only the nodes it changes.
  With no surface: the defaults, then the code repository's file.
- Q20: a stronger layer unsets a node by writing it null (`agent: ~`); the weaker value (here the
  plugin's) comes back (section 1, "Unsetting a node"). Its spelling (the user's answer to the
  split specification's open question): `~` and `null` unset a node; an empty value (`agent:` with
  nothing after it) stays refused, so a forgotten value never unsets in silence.
- Q23: the value `default` unsets a node too, like `~` and `null`; it is the spelling the docs,
  the examples and the board show. No model and no agent can be named `default`.
- Q16: there is no model, nor any role setting, for all hosts. Every layer sets roles per host
  only (`hosts.<host>.roles`). The configuration for all projects of a surface is its root file;
  inside it, roles are still per host.
- Q21: no backward compatibility. A top-level `roles` is refused in every layer (section 1); the
  old form is not read, and there is no warning-only path; the release notes name the breaking
  change.
- Q11: `config/chantier.defaults.yml` in the plugin is the lowest layer, read like the user's
  files. The models the shipped agent files declare stay equal to it; a test checks it. The model
  catalog (identifiers, names, availability) stays copilot-model-catalog's (Copilot) and
  `MODELS["claude"]` (Claude Code).
- Q4: a change applies at the next batch. A batch keeps the configuration frozen at its `open`,
  as today.
- Q15: the existing `skills` and `tools` under a role stay what they are, a list of what the role
  needs, checked at preflight, restricting nothing; the docs say so.
- Q3: no agent file is generated or written anywhere (nothing in this CR writes one).
- The Chief of Staff's decision: the `AGENTS.md` wording (section 7) is written by the Driver as
  below; the user reads and approves it in the PR's diff at the merge.
- Carried to B: Q3's refusals, Q5, Q6, Q8, Q9, Q10, Q12 as narrowed by Q17, Q13, the grill cost
  line. Carried to C: Q7, Q14, Q22, and the board's side of Q4 and Q13.
- Spec critic: yes.

## What changes

All CLI paths below are under `skills/chantier/scripts/cli/src/chantier/`.

### 1. The layers (`playbook/config.py`, `playbook/yaml_subset.py`, new `playbook/layers.py`)

| Layer | Path | Label | When |
| --- | --- | --- | --- |
| defaults | `<plugin root>/config/chantier.defaults.yml` (`plugin_files.plugin_root()`) | `defaults` | always |
| surface | `<surface root>/chantier.yaml` or `.yml` (`repo.surface_root`) | `surface` | external mode |
| surface project | `<surface>/projects/<name>/chantier.yaml` or `.yml` (`repo.project_folder`) | `surface project` | external mode |
| repository | `<code repository root>/chantier.yaml` or `.yml` (`repo.root`; in external mode the project's clone) | `repository` | always |

- Each user layer is optional. `FILE = "chantier.yaml"` becomes the pair
  `("chantier.yaml", "chantier.yml")`. When both exist in one place, reading stops with one problem:
  `<path 1> and <path 2> are both present: keep one` (Q1). The defaults file has one fixed name.
- Paths in every line the CLI prints are written as the user would type them from the session's
  folder (`repo.session_root`): in a project with no surface, `chantier.yaml` exactly as today
  (so today's messages and the scenario's `chantier.yaml:3: board: ` checks hold); in external
  mode `chantier.yaml` for the surface root, `projects/<name>/chantier.yaml`, and the code
  repository's file by its path from the surface (e.g. `projects/<name>/.repo/chantier.yaml`), or
  its absolute POSIX path when it lies outside the surface. The defaults file is
  `config/chantier.defaults.yml`.
- Each problem line is `<path>:<line>: <message>`; every message's own text stays as today except
  those named below.
- Each layer is parsed by `yaml_subset.parse` and checked alone by the same key checks (shapes,
  prices complete, `board`, `ci`, `long_gate` values, role names, role keys). Then the layers
  merge. A problem in any layer makes the whole configuration invalid, every problem listed with
  its path and line (exit 2 where it is today; preflight P12 fails); no layer is skipped to read
  the others alone.
- Merge, node by node (Q19): a mapping merges with the same mapping of the layers below it, key by
  key, down to the leaves; a leaf (a scalar, or a list such as `skills`) of a stronger layer
  replaces the weaker one whole. A `prices.<model id>` entry is replaced whole: each layer's entry
  already holds all five prices (today's rule, none derived from another), so nothing is merged
  price by price.
- New top-level key `hosts`: `hosts: <host>: roles: <role>: <keys>`, `<host>` one of
  `plugin_files.HOSTS` (`claude`, `copilot`), the role keys as today (`agent`, `model`, `skills`,
  `tools`). It is the only place role settings live (Q16).
- The top-level `roles` key is refused, in every layer, with one problem at its line:
  `"roles" goes under a host: hosts: claude: roles: or hosts: copilot: roles: (every role setting
  is per host)`. A file written for today's chantier stops at `playbook`, `preflight` and `open`
  with that line; the release notes say so (Q21: the old form is never read, nor only warned
  about; `roles: default` and `roles: ~` are refused the same way).
- The unknown-key message lists `hosts`, `prices`, `board`, `ci` and `long_gate`; `hosts:`'s own
  keys are checked (`unknown host "<x>": one of claude, copilot`), and a host's only key is
  `roles`.
- Every host's section is checked in every view: its role names against `plugin_roles(host)`, its
  model names against `MODELS[host]` (`models.resolve`), so a typo under `hosts.copilot` stops
  `playbook` on Claude Code too. What depends on the running host (whether its start can take the
  model, below and in B) is judged only for the host whose view is asked: the running host for
  `playbook`, `preflight` and `open`.
- `playbook/layers.py` gives one function the CLI and, later, the board (C) both use: the layers
  read (label, path, present or not, problems) and the merged tree with, for every leaf, the
  label of the layer that set it, and for every node a user layer unset, the label, path and line
  of that reset. `config.load` builds the host's resolved playbook from it.
- Every reader reads the merged configuration, not the code repository's file alone:
  `plugin_files.read_playbook` (`playbook`, `preflight`, `open`, the prices of `cost`),
  `config.load_board` (`board/address.py`, and `board/command.py`, which reads the board's home
  project), `config.load_long_gate` (`commands/gate.py`). `board`, `ci`, `long_gate`, `prices`
  keep their meaning and merge like the rest.

#### Unsetting a node (Q20)

- In a user layer (surface, surface project, repository), a key whose value is a plain, unquoted
  `default`, `~` or `null` is a reset: `hosts: copilot: roles: coder: agent: default` (Q20, Q23).
  `default` is the spelling every doc, example, card and board text shows; `~` and `null` are read
  the same way. `yaml_subset` reads the plain `~` and `null` as its `null` node (its docstring says
  so); the layer reader reads a plain `default` as a reset before any key's own check, so
  `default` never reaches `models.resolve` or the agent check. A quoted `"~"` or `"null"` stays
  text. A quoted `"default"` under `agent` or `model` is refused at its line (`"default" resets
  the value: write it plain, default; no agent or model is named "default"`), so no model or agent
  is ever named `default` (Q23). An empty value (`agent:` with nothing after it) is not a reset: it
  keeps today's refusal (`role "coder": "agent" is one string`, and the other "is empty" lines), so
  a forgotten value is never read as a reset (Q20's spelling).
- A reset removes the node, and everything under it, from every weaker user layer: the defaults
  layer's value, when it has one, comes back; with none the node is unset, as if no user layer had
  set it (for `agent`, the plugin's agent). A layer stronger than the reset may set the node
  again; the strongest layer that writes the node, with a value or a reset, wins.
- Examples: the surface root sets `hosts.claude.roles.coder.agent: my-coder` for every project,
  and one project's `projects/<name>/chantier.yaml` writes `agent: default`: that project runs the
  plugin's Coder. The surface root sets the Coder's `model: opus`, the code repository writes
  `model: default`: the defaults' model comes back, which counts as no configured model (section
  3). `prices: <id>: default` brings back the built-in price of that model; `board: default`,
  `ci: default`, `long_gate: default` bring back their weaker or built-in values;
  `hosts: copilot: roles: coder: default` resets every key of that role on that host.
- A reset is checked like a value for its place: its key, host and role names are checked as
  today (an unknown key, host or role written `default` or `~` is refused with today's line). A
  reset of a node
  no weaker layer sets is accepted and changes nothing. The defaults file holds no reset (its test,
  section 8).
- What the CLI prints for a reset: the value that came back, labelled as such (`model=(its
  file's)` for the defaults' model, no label when the node is unset), followed by `[reset in
  <label>]`, e.g. `coder: agent=chantier:coder [reset in surface project] model=(its file's)`.
  `open` records the reset with its layer like a set value (section 4).

### 2. The shipped defaults (`config/chantier.defaults.yml`, new, at the plugin root)

- Holds only `hosts.claude.roles.<role>.model` and `hosts.copilot.roles.<role>.model`: one entry
  per plugin role on each host (fourteen per host), each value the exact identifier its agent file
  declares (`agents/<role>.md` `model:`; `com.github.copilot/agents/chantier-<role>.agent.md`, the
  identifier of `model: [name, id]`), as they are after copilot-role-models.
- A header comment: the plugin's defaults, the lowest layer; do not edit it in an install, set
  your values in your `chantier.yaml` (where `default` takes a value back to this file's); changed only
  by a release, together with the agent files (a test checks it).
- It sets no `agent`, no `prices` (the built-in table stays in `costs/`), no escalation
  (`ESCALATION` stays in `playbook/models.py`), and no reset.
- `playbook/models.py`'s comment above `MODELS` says each role's default model is in
  `config/chantier.defaults.yml`, and keeps the catalog's source as copilot-model-catalog wrote it.
- A missing or unreadable defaults file under a plugin root is a P12 problem naming its path;
  with no plugin root (a skill installed alone) it is the existing "the chantier plugin is not
  installed" problem of `agent_problems`.

### 3. A role's model against its default (`playbook/config.py`, `playbook/lines.py`)

- A role's default model on a host is the defaults layer's value. Its configured model is the
  merged value from the user layers only (surface, surface project, repository); the defaults
  layer's model never counts as configured, nor does the defaults' model brought back by a reset.
- A configured model equal to the default, with no `agent` set, is the plugin's agent with no
  model passed, on every host (the agent file already runs that model): `playbook` prints
  `model=(its file's)`, and Copilot does not refuse it.
- Any other configured model is resolved and judged as today: on Claude Code it is passed at the
  start; on Copilot it is refused with today's message (`cannot set a model when it starts an
  agent ...`), now naming the file and line of the `model` key that set it. B replaces that rule.
- An `agent` set alone keeps today's meaning: the user's agent, with its file's model; the
  default model is not passed to it.

### 4. What the CLI prints (`playbook/lines.py`, `commands/rules.py`, `commands/preflight.py`, `commands/opening.py`)

- `playbook`'s head line names the user files read, in order, weakest first, e.g.
  `playbook: chantier.yaml, projects/chantier/chantier.yaml, projects/chantier/.repo/chantier.yaml,
  valid, host copilot`; with no user file it stays `playbook: no chantier.yaml, the plugin's agents
  and models`; with a frozen batch, `playbook: <files> as <batch> opened it, host <host>`.
  Preflight P12's line and `rules`'s playbook line (`playbook: the configuration is not valid (<n>
  problems)`) name the same files.
- Each value a user layer set is followed by its label in brackets: `coder: agent=chantier:coder
  model=opus (claude-opus-5-5, Claude Opus 5.5) [repository]`, `cr-driver: agent=my-driver
  [surface] model=(its file's)`; a reset by `[reset in <label>]` (section 1). The `prices:`, `ci:`
  and `needs:` lines name the layer in the place they name `chantier.yaml` today.
- `open` records in `batch.json`'s `playbook`, beside what it records today, the list of files read
  and, per set or reset value, its layer; `playbook --batch` prints them, so a running batch keeps
  its configuration (Q4). A batch opened before this change prints as today.
- `team_lines` (the `team:` lines of `take`, `round`, `handoff`) carry the same labels.

### 5. Cards and host references (`skills/chantier/references/`)

- `chief-of-staff.md`, "The team": the YAML example moves under `hosts: claude: roles:`, and one
  line says the same keys go under `hosts: copilot: roles:`; the text names the four layers and
  their order (Q19), says a layer carries only what it changes and that `default` takes a weaker
  layer's value back (Q20, Q23), that every role setting is per host (Q16), and that the Chief of
  Staff edits
  the code repository's or the surface's file only on the user's word. The table row "use my agent
  for <role>" names `hosts.<host>.roles.<role>.agent`, and "back to the plugin's agent" names
  `agent: default`.
- `concepts.md`, "Starting an agent": the playbook is the configuration in layers, read, merged
  and resolved only by the CLI; nothing else changes there (B changes the starts).
- `hosts/claude-code.md` and `hosts/copilot.md`, row "Models": "unless the project's
  `chantier.yaml` sets a model" becomes "unless the configuration (`hosts.<host>.roles`) sets one";
  the default models are `config/chantier.defaults.yml`'s. Their "Startup core" sections do not
  change.
- `session-start.md`, "Zero configuration", and the `SKILL.md` of `skills/chantier`,
  `skills/chief-of-staff`, `skills/griller`, `skills/status`: "an optional `chantier.yaml` at its
  root, are the only configuration" becomes "an optional `chantier.yaml` (the project's, and its
  planning surface's), are the only configuration". Their byte counts stay within
  `test_startup_manifest.py`'s budget.

### 6. Docs

- `docs/agents-and-models.md`, "Your own agents": the example under `hosts:`; the four layers and
  their paths, `.yaml` or `.yml` (not both); node-by-node merge with an example (the surface root
  sets the Coder's model for every project, one project's code repository changes it back); the
  reset with `default` (Q23; `~` and `null` read the same) and its example (the surface root names
  `agent: my-coder`, one project writes `agent: default` and runs the plugin's Coder), that no
  model or agent can be named `default`, and that an empty value is not a reset; every
  role setting per host (Q16); Q15: `tools` and `skills` list what the role needs, checked at
  preflight, and restrict nothing. "Models": the table's values come from
  `config/chantier.defaults.yml`.
- `docs/tutorial-claude-code.md`: its `chantier.yaml` example under `hosts: claude: roles:`.
- `docs/planning-modes.md`, "The planning surface": the surface root and each project's folder may
  hold a `chantier.yaml`; the code repository's file is the strongest.
- `README.md`: the configuration sentence as in section 7; the row "run the inspector on Opus":
  "a `model` for the role under `hosts.<host>.roles` in `chantier.yaml`".
- Release notes, as the project's release process asks: the layers, `.yml`, the reset with `default`,
  and the breaking change (Q21: a top-level `roles` is refused, move it under
  `hosts.<host>.roles`; shown with one before/after example, today's `roles: coder: {agent:
  rust-coder, model: opus}` and its `hosts: claude: roles:` form).

### 7. Project rules (`AGENTS.md`)

The Driver writes it as below; the PR's body says it changes a project rule, for the user to
read and approve in the diff at the merge:

- "the user's `AGENTS.md`, and an optional `chantier.yaml` at the project's root, are the only
  configuration (with no `chantier.yaml` chantier runs as if it were empty; ...)" becomes "the
  user's `AGENTS.md`, and optional `chantier.yaml` (or `chantier.yml`) files, at the project's
  root and, with an external planning surface, at the surface's root and in the project's folder
  there, are the only configuration, above the plugin's shipped `config/chantier.defaults.yml`
  (with none, chantier runs on the shipped defaults; ...)", the rest of the sentence unchanged.
- The "plain JSON and Markdown" clause and the board's exception do not change here (C changes
  them, when the board writes the surface's file).

### 8. Tests (`skills/chantier/scripts/cli/tests/`), few, parametrized, fast

- `test_plugin_files.py`: new, parametrized over both hosts: every plugin role has exactly one
  model in `config/chantier.defaults.yml`, equal to the identifier its agent file declares, no
  entry names a role the host has no agent for, the file holds nothing else (no reset), and it is
  valid.
- `test_playbook_config.py`, parametrized cases on a prepared state (in-project and external):
  - the order of Q19: a model set in the surface root, changed in the surface project, changed
    again in the repository; each step's winner printed with its label;
  - a list replaced whole; a `prices` entry replaced whole;
  - Q20, Q23: `agent: default` in the surface project over the surface root's agent (the plugin's
    agent, `[reset in surface project]`); `model: default` in the repository over the surface
    root's model (`model=(its file's)`, no model passed, accepted on Copilot); a reset set again by
    a stronger layer; `~` and `null` read like `default`, a quoted `"~"` read as text; a quoted
    `model: "default"` and `agent: "default"` refused with their line; an empty `agent:` refused as
    today; a reset under an unknown role refused;
  - Q1: both names in one place refused with both paths (repository, surface root, surface
    project); `chantier.yml` alone read like `chantier.yaml`;
  - Q16, Q21: a top-level `roles` refused with its line, `roles: default` too;
  - problems name their path (`projects/<name>/chantier.yaml:<line>:`);
  - a bad model under `hosts.copilot` refused on a Claude Code view;
  - a configured model equal to the default: no model passed, accepted on Copilot;
  - a running batch keeps its frozen configuration after a surface file changes (Q4);
  - the existing cases moved under `hosts.<host>.roles`.
- `test_gate_refusals.py` and the board's address tests: a `long_gate` or `board` key set in the
  surface root is read.

### 9. Scenario (`scenario/run_scenario.py`, `scenario/README.md`)

- The board's `chantier.yaml` checks (the block under the comment `# 11. chantier.yaml`): one
  check that `chantier.yml` alone is read like `chantier.yaml`, one that both together exit 2
  naming both.
- §20 (a planning surface): the surface root's `chantier.yaml` sets a role's model under
  `hosts.claude.roles`, the project folder's file sets another, the code repository's file a
  third; `playbook` prints the third with `[repository]`; `open` freezes it; the code repository's
  file then writes the model `default`: `playbook` prints `model=(its file's)` with `[reset in
  repository]`; after the code repository's file is removed, `playbook` prints the project
  folder's value with `[surface project]`; `playbook --batch` still prints the frozen one
  throughout.
- `scenario/README.md`: the `chantier.yaml` line names the layers and the reset.

## Out of scope

- A model per role on Copilot, the generic agent, `model-policy`, the probe, `cost --explain`: B
  (role-model-per-host).
- The board's Configuration page and any write of a configuration file by chantier: C
  (board-config-page). Nothing in this CR writes a `chantier.yaml`.
- The Copilot model catalog (copilot-model-catalog) and the agent files' `model:` values
  (copilot-role-models).
- Prices, the cost computation and escalation (not moved to the defaults file).
- A user-level layer (home folder) and any layer other than Q19's four.
- Reading a top-level `roles`, alone or alongside `hosts`, or warning about it instead of
  refusing it (Q16, Q21).
- Unsetting a node of the defaults layer itself: a reset brings the defaults' value back, it never
  removes it.
- A new `chantier` command to write the configuration.

## Evidence

- `just check` green on Linux, macOS and Windows; `just test` within its budget.
- `just scenario` green: the pipeline's `just scenario (ubuntu-latest)` job at the PR's head, and
  the local Windows run (`chantier gate`) when this CR is on top of its stack (AGENTS.md).
  `hooks/` and `types/` untouched: no `just mod`.
- In the PR, `chantier playbook` on chantier's own checkout with no user file (each role
  `model=(its file's)`), and in a surface with the three user files of the §20 step, then with the
  repository's reset, on both hosts (`--host claude`, `--host copilot`).
- `git diff` of `agents/` and `com.github.copilot/agents/`: empty.
- No CI job is added or changed.
