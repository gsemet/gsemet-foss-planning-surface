# Change Specification: role configuration in layers, a model per role on each host, the board's Configuration page

Date: 2026-11-16 (second run, after the answers to the first run's open questions). Sources:
[intent](01-intent.md), [answers](02-answers.md) (Q1 to Q15 and the Chief of Staff's two
decisions; they rank above the intent), [original request](intake/request.md). No tracker issue.

## Depends on

- [copilot-role-models](../copilot-role-models/03-change-spec.md) (third run): the Copilot agent
  files' `model:` lines (Coder on Sol; Verifier, Debugger, Conflict resolver on Terra), the
  hand-written `gpt-6.1-terra` row of `MODELS["copilot"]`, its documentation rows (`docs/agents-and-models.md`,
  `hosts/copilot.md` "Models", "Models at an agent's start", "The model a role ran on") and its
  `evals/copilot/RUNBOOK.md` section "Models" with `evals/kit/copilot_models.py`. This CR edits
  what that one writes; it is built on top of it.
- [copilot-model-catalog](../copilot-model-catalog/) (its intake): chantier's Copilot model list
  built from GitHub's tables (a copy kept in the repository, a refresh command, `MODELS["copilot"]`
  built from it). This CR uses `MODELS[host]` as the catalog (the YAML's model identifiers, the
  board's model choice) and does not redo it. Where this CR changes a Copilot `Model`'s `start`
  value (section 3), the change goes where that CR builds `MODELS["copilot"]`.

Both merge before this CR; its Driver takes their files as they are on `main`.

## Goal

The user sets, per role, which agent runs it and on which model, without touching the plugin's
installed files and without losing the settings at an upgrade. The settings live in plain YAML
files in layers: the plugin's shipped defaults, the code repository's `chantier.yaml`, and, with
an external planning surface, the project's file in the surface. A model change works on both
hosts: where the host can start a named agent with a model (Claude Code), the role's agent keeps
its tools and runs the chosen model; where it cannot yet (Copilot), a generic agent runs the role
with its whole contract in its prompt and the chosen model, and chantier says plainly that its
tools are the caller's, not restricted. The Copilot agent files stop enforcing their own model
(`model-policy: required` removed), and the Copilot eval gains the probe that tells whether a named
Copilot agent runs a model given at its start; Copilot then moves to the first case by changing one
capability, in a later CR. The web board gets a Configuration page that edits each role's agent and
model in the surface's file, through the same reading and validation as the CLI.

## Decisions carried from the grill

- Q1: `chantier.yaml` and `chantier.yml` are both accepted. Both present in the same place is
  refused, with the two paths named.
- Q2: with an external planning surface, `projects/<name>/chantier.yaml` (or `.yml`) of the
  surface is read above the code repository's root file: the code repository's file is the base,
  the surface's overrides it key by key. With no surface, nothing changes.
- Q3: no generated agent file, anywhere (plugin, managed folder, workspace, user folder). What a
  host cannot apply at an agent's start is refused on that host, with the reason.
- Q4: a change applies at the next batch. A batch keeps the team frozen at its `open`, as today;
  the board says "applies at the next batch".
- Q5, Q6: a model per role, configurable, on both hosts. Claude Code: the Agent tool's `model`
  parameter wins over the agent file's `model` (proved). Copilot: documented, unproved: an explicit
  model wins over a custom agent's `model` unless the agent sets `model-policy: required`. A
  generic agent is never a fallback: it runs only as the user's configuration (Q8, Q9). Neither
  host changes a named agent's tools at its start.
- Q7: the Configuration page writes only the surface's `projects/<name>/chantier.yaml`, committed
  by the autosync (the board commits nothing), and shows the value inherited from the code
  repository's file and the effective value. With no surface the page is read-only and says to
  edit `chantier.yaml` by hand.
- Q8, narrowed by Q9: per role, nothing set: the plugin's agent with its file's model; an agent
  name: the user's own agent runs the role (its file, its tools, its model); a model different
  from the agent file's: on a host that can start a named agent with a model, the role's agent
  starts with that model and keeps its file's tools; on a host that cannot, no agent file is used
  and a generic agent starts with the role's whole contract in its prompt, rebuilt by chantier,
  and the configured model. Each host declares that one capability; Copilot flips it once proved,
  with nothing else to rewrite; a host added later declares its own.
- Q10: a role's tools change only by naming the user's own agent. No field restricts tools in
  the YAML. A generic agent has the caller's tools: the board and the playbook say "the caller's
  tools, not restricted".
- Q11: `config/chantier.defaults.yml`, shipped in the plugin, is the lowest layer, read like the
  user's files. The models the shipped agent files declare stay equal to it; a test checks it.
  The model catalog (identifiers, names, availability) stays copilot-model-catalog's copy of
  GitHub's tables (Copilot) and `MODELS["claude"]` (Claude Code).
- Q12: this CR removes `model-policy: required` from every Copilot agent file (their `model:` stays
  the default). Copilot's capability stays "no" (a model change starts the generic agent) until the
  user's Copilot run. This CR's eval preparation adds the probe: a named agent started with a
  requested model, the model it ran on read from `subagent.*`; if it matches, a one-line change
  switches Copilot's capability on, in a later CR. The test asserting `model-policy: required`
  changes accordingly.
- Q13: on Copilot, the user's own agent named for a role together with another model is refused
  with the reason, at the batch's open (and wherever the playbook is read); the board says it as it
  is entered. No generic agent in its place, nothing hidden.
- Q14: the board's Configuration page edits only each role's agent and model; the rest of the
  configuration (prices, board, CI, long gate, needs) is shown read-only.
- Q15: the existing `roles.<role>.tools` (with `skills`) stays what it is, a list of what the role
  needs, checked at preflight, restricting nothing; the docs say so.
- The Chief of Staff's decision: the `AGENTS.md` wording (section 8) is written by the Driver as
  below; the user reads and approves it in the PR's diff at the merge.
- The Chief of Staff's decision: a Spec-writer or a Spec critic started as a generic agent, or
  replaced by the user's own agent, leaves the grill line of `cost`; `cost --explain` says so.
  The AGENTS.md named exception (the cost code knows `spec-writer`, `spec-critic` by agent type)
  is not extended.
- Spec critic: yes.

## What changes

### 1. The layers and their files (`skills/chantier/scripts/cli/src/chantier/playbook/config.py`)

Read from lowest to highest, each one optional except the first:

| Layer | Path | Shown as |
| --- | --- | --- |
| defaults | `<plugin root>/config/chantier.defaults.yml` (`plugin_files.plugin_root()`) | `defaults` |
| project | `<code repository root>/chantier.yaml` or `chantier.yml` (`repo.root`; in external mode the project's clone) | `project` |
| surface | `<surface>/projects/<name>/chantier.yaml` or `chantier.yml` (`repo.project_folder`), external mode only | `surface` |

- File names: `FILE = "chantier.yaml"` becomes the pair `("chantier.yaml", "chantier.yml")` for
  the project and surface layers. When both exist in one place, reading stops with one problem:
  `<path 1> and <path 2> are both present: keep one`, both paths as the user would type them
  (relative to the repository or the surface root). The defaults file has one fixed name.
- Each problem line names its file instead of the fixed `chantier.yaml:`: `<file>:<line>:
  <message>`, where `<file>` is `chantier.yaml`/`chantier.yml` for the project layer,
  `projects/<name>/chantier.yaml` (or `.yml`) for the surface layer, and
  `config/chantier.defaults.yml` for the defaults. Every message's text stays as today.
- Each layer is parsed by the same `yaml_subset.parse` and validated by the same key checks; a
  problem in any layer makes the whole configuration invalid (exit 2 where it is today, preflight
  P12 fails), each problem listed with its file and line, never skipped to read the others alone.
- Merge, "key by key" (Q2): a mapping merges with the mapping below it, key by key, down to the
  leaves; a leaf (a scalar, or a list such as `skills`) of a higher layer replaces the lower one
  whole. One exception keeps today's rule that no price is derived from another: an entry
  `prices.<model id>` is replaced whole, never merged price by price.
- New top-level key, `hosts`, accepted in every layer (the defaults need per-host models, and
  Q11 reads the defaults "like the user's file"): `hosts: <host>: roles: <role>: <keys>`, with
  `<host>` one of `claude`, `copilot` (`plugin_files.HOSTS`). For the running host, the role keys
  under `hosts.<host>.roles` sit above the top-level `roles` of the same layer. The layers merge
  first, then each host's view: defaults < project < surface, and within each layer top-level
  `roles` < `hosts.<host>.roles`. A model named under `hosts.<other host>` is resolved against that
  host's catalog only when that host's view is asked for (the board asks for both; `playbook`,
  `preflight` and `open` ask for the running host).
- The unknown-key message lists `roles`, `hosts`, `prices`, `board`, `ci` and `long_gate`.
- Every reader reads the merged configuration, not the root file alone: `read_playbook`
  (`plugin_files.py`; `playbook`, `preflight`, `open`, the prices of `cost`), `load_board`
  (`board/address.py`, `board/command.py`) and `load_long_gate` (`commands/gate.py`). The
  `board`, `ci`, `long_gate`, `prices` and the roles' `skills`/`tools` needs keep their meaning
  (Q15: `tools` lists what the role needs, checked at preflight, and restricts nothing); they now
  merge like the rest.
- The playbook's head line names the files read, in order, e.g. `playbook: defaults,
  chantier.yaml, projects/chantier/chantier.yaml, valid, host copilot`; with no user file:
  `playbook: no chantier.yaml, the plugin's agents and models` (unchanged text). `preflight`'s P12
  line names the same files.
- The defaults file missing or unreadable (a skill installed with no plugin: no plugin root) is
  the existing "the chantier plugin is not installed" situation (`agent_problems`); otherwise a
  missing defaults file under a plugin root is a P12 failure naming its path.

### 2. The shipped defaults (`config/chantier.defaults.yml`, new)

- Holds only `hosts.claude.roles.<role>.model` and `hosts.copilot.roles.<role>.model`, one entry
  per plugin role on each host, each value the exact identifier the role's agent file declares on
  `main` after copilot-role-models (Claude Code: `claude-opus-5-5` for `spec-writer`,
  `spec-critic`, `retro-critic`, `claude-sonnet-5-5` for the others; Copilot: the identifier in
  each `com.github.copilot/agents/chantier-<role>.agent.md` `model:` line). A header comment says:
  the plugin's defaults, the lowest layer; do not edit in an install, set your values in your
  `chantier.yaml`; changed only by a release, together with the agent files (a test checks it).
- It sets no `agent` (the plugin's agent stays `default_agent(host, role)`), no `prices` (the
  built-in table stays in `costs/`), no escalation (`ESCALATION` stays in `models.py`).
- `models.py`'s comment above `MODELS` points to the defaults file for each role's model and keeps
  the catalog's own source as copilot-model-catalog wrote it.

### 3. The Copilot agent files (`com.github.copilot/agents/`), Q12

- In each of the fourteen `chantier-<role>.agent.md`, the frontmatter line `model-policy: required`
  is removed. Nothing else changes: `model:` (as copilot-role-models set it), `tools`,
  `strict-tools-list`, `user-invocable`, and the body byte for byte, so both hosts' bodies stay
  identical (AGENTS.md). The Claude Code agent files (`agents/`) do not change.
- Effect today: none at run time. Copilot's capability stays "no" (section 4), so chantier passes
  no model when it starts a named Copilot agent and the file's `model:` runs, as the Copilot CLI
  reference says for an agent without an explicit model. The removal prepares the flip: per the
  same reference, a model given at the start then wins over the file's, which the probe of
  section 8 checks.

### 4. How a role starts on each host (`playbook/models.py`, `playbook/config.py`, `playbook/lines.py`)

- `SETS_MODEL_AT_START` becomes `NAMED_AGENT_MODEL_AT_START = {"claude": True, "copilot":
  False}`, with its comment: whether this host starts a named agent with a model given at the
  start, so that model runs and the agent keeps its file's tools; only what the host's reference
  marks proved; a host added later declares its own value; Copilot's value turns `True` once the
  eval's probe (`evals/copilot/RUNBOOK.md`, "Models") shows a named agent ran the requested model.
  It is the one switch for Copilot.
- A Copilot `Model`'s `start` value becomes its identifier (`Model(id, name, id)`), where
  copilot-model-catalog builds `MODELS["copilot"]`: CR-296 round 6 proved that a `task` start with
  `model: gpt-6.1-sol` ran Sol (its host log: `modelSelectionSource: explicit_override`).
  `MODELS["claude"]` keeps its aliases.
- The default model of a role on a host is the defaults layer's value. The configured model is the
  merged value from the project and surface layers (and their `hosts.<host>` parts). Per role, the
  CLI resolves one of four starts:

  | Configured | Host can (named agent with a model) | Host cannot |
  | --- | --- | --- |
  | nothing, or a model equal to the default, no `agent` | the plugin's agent, no model passed | the same |
  | `agent` only | the user's agent, no model passed (its file's model) | the same |
  | a model other than the default, no `agent` | the plugin's agent, the model passed | a generic agent, the model passed, the role's contract in the prompt |
  | `agent` and a model | the user's agent, the model passed | refused (Q13) |

- The refusal (Q13), one problem line, with the file and line of the `model` key that makes it:
  `role "<role>": <Host> cannot start a named agent with a model (hosts/<file>.md, "Models at an
  agent's start"); remove "model" for <role>, or name the model in your agent's own file`. It is a
  problem of the configuration for that host's view only: `playbook`, `preflight` (P12) and `open`
  on that host refuse (exit 2 where they do today), so a batch never opens with it; the other
  host's view is unaffected.
- The old refusal `<Host> cannot set a model when it starts an agent ...` is gone (it replaced the
  case "a model, no agent" on Copilot); copilot-role-models' test and evidence that expected it on
  `roles: {coder: {model: gpt-6.1-terra}}` now expect a generic start.
- A model equal to the default, given with no `agent`, is the plugin's agent with no model passed,
  on every host: the agent file's model already is that model.

### 5. What the CLI prints (`playbook/lines.py`, `plugin_files.py`, `commands/rules.py`, `commands/facts.py`, `commands/opening.py`, `commands/cost/`)

- `playbook` (and `playbook --batch`), one line per role, each value followed by its layer in
  brackets when a user layer set it:
  - plugin's agent, file's model: `coder: agent=chantier:coder model=(its file's)` (unchanged);
  - named agent with a model: `coder: agent=chantier:coder model=opus (claude-opus-5-5, Claude
    Opus 5.5) [surface]` (today's form, plus the layer);
  - generic: `coder: agent=(generic) model=gpt-6.1-terra (gpt-6.1-terra, GPT-6.1 Terra) [project]
    tools=(the caller's, not restricted)`;
  - `skills`/`tools` needs and `Needs:` lines as today.
- The `team:` lines of `take`, `round` and `handoff` (`team_lines`) carry the same three forms.
- A generic start's prompt (Q8, "rebuilt by chantier"): wherever the CLI prints a role's opening
  lines or first line (`chief_prompt_lines` for `playbook`'s `<role> prompt, first line: …`;
  `worker_prompt_lines` for `take`, `round`, `handoff`), for a role that starts generic it adds,
  right after them: `<role> contract (a generic agent: copy it unchanged, without the two leading
  spaces, after the opening lines):` then the body of the plugin's agent file for that role and
  host (everything after its frontmatter, `# chantier-agent:` line included), each line indented
  by two spaces. The role keeps its card through the prompt's `Read` line, as today. No file is
  written.
- `open` records, in `batch.json`'s `playbook`, the merged result per role as today plus, per role,
  `start` (`plugin`, `named`, `generic`) and the layer of each set value, and the list of files
  read; `playbook --batch` prints it, so a running batch keeps it (Q4). A batch opened before this
  change, with a `playbook` that lacks these fields, prints as today.
- `concepts.md`'s rule "the output is ten lines at most" exemption already covers `playbook`,
  `take`, `round`, `handoff`.
- `cost --explain` (`commands/cost/command.py`, `_explain_notes`): for `spec-writer` and
  `spec-critic`, when the configuration read now, for the batch's host, starts that role other
  than the plugin's agent, one line per such role: `Grill line: <role> starts as a generic agent
  (or: as your agent <name>), so its spend is counted with the Chief of Staff's steering, not on
  the grill line`. Nothing else in `costs/` changes; the grill line's detection by agent type
  (`costs/sessions.py`, `costs/transcripts.py`) stays as it is.

### 6. The cards and host references (`skills/chantier/references/`)

- `concepts.md`, "Starting an agent":
  - the playbook is the configuration in layers (defaults, the code repository's `chantier.yaml`
    or `.yml`, the surface's `projects/<name>/chantier.yaml` or `.yml`), read, merged and resolved
    only by the CLI;
  - a new bullet: `agent=(generic)` printed: start the host's generic agent (the host reference's
    row), pass the model as printed, and put the printed contract lines after the opening lines;
    its tools are the caller's, the card bounds what it does; never chosen by the parent, only
    printed by the CLI;
  - the rest unchanged (copied as printed, never retried without the model or with another).
- `chief-of-staff.md`, "The team": the YAML example gains `hosts:`; the text says where the files
  live and that the Chief of Staff edits the code repository's or the surface's file only on the
  user's word (with a surface, the surface's, as the board does), names the board's Configuration
  page, replaces "A host that cannot set a model ... refuses a `model`" with the four starts of
  section 4 in one sentence (Copilot refuses the user's own agent with a model), and says that a
  role started generic runs with the caller's tools, not restricted, which the Chief of Staff tells
  the user when it shows the team. The table row "use my agent for <role>" names `chantier.yaml`
  or the surface's file.
- `driver.md` and `foreman.md`: where they say the agent and model are passed as printed, add "or
  the generic agent with the printed contract lines (concepts, Starting an agent)". No other
  change.
- `hosts/claude-code.md`: row "Models at an agent's start" gains "named agent with a model:
  yes (the capability `NAMED_AGENT_MODEL_AT_START`); a model changed in the configuration starts
  the role's named agent with that model, its tools unchanged". No generic row (never used on
  Claude Code).
- `hosts/copilot.md` (on top of copilot-role-models' rows):
  - row "Models": the words "with `model-policy: required`" are removed; the file's model is the
    one that runs when no model is passed.
  - row "Models at an agent's start": "named agent with a model: no, until the probe of
    `evals/copilot/RUNBOOK.md`, "Models", shows a named agent ran a requested model (the
    capability `NAMED_AGENT_MODEL_AT_START`). The plugin's agents no longer set
    `model-policy: required` (documented: a model given at the start then wins over the file's,
    [CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#command-line-options);
    unproved). Observed before the removal, CR-296 rounds 5 and 6: (copilot-role-models' text,
    kept). Start value: the identifier. A model changed in the configuration starts a generic
    agent (row below); the user's own agent with a model is refused". The old capability text
    "none; no start value" and the refusal "cannot set a model when it starts an agent" are gone.
  - new row "Start a generic agent (a role configured with a model)": "`task`, `mode: background`
    for a Driver, the generic agent (`agent_type: general-purpose`, unproved as to the exact value:
    CR-296 round 6 ran a generic agent this way), `model:` the printed start value, the prompt with
    the printed contract lines; its tools are the caller's, not restricted. Proved: a generic
    `task` start with `model: gpt-6.1-sol` ran Sol (CR-296 round 6, the host's
    `subagent.started` record)".
  - copilot-role-models' row "The model a role ran on" gains: after a start with a model, the
    parent reads, in its session's `events.jsonl`, the `model` of the `subagent.started` event of
    that start; when it differs from the printed identifier, the parent stops that agent's work,
    reports both identifiers and the host's text (rule 7), and starts nothing else for it.
    Unproved as a routine; read after the start, not a guarantee before it.
  - the "Startup core" sections of both references do not change (the startup budget test).
- `SKILL.md` of `skills/chantier`, `skills/griller`, `skills/status`: the sentence "an optional
  `chantier.yaml` at its root, are the only configuration" becomes "an optional `chantier.yaml`
  at its root (and, with a planning surface, the project's file there)". Their byte counts stay
  within `test_startup_manifest.py`'s budget; if a sentence does not fit, the shorter form "an
  optional `chantier.yaml` (the project's, and its surface's)" is used.

### 7. The board's Configuration page (`skills/chantier/scripts/cli/src/chantier/board/`)

- API, in a new module `board/config_api.py`, registered like `write_api.ROUTES`:
  - `GET /api/projects/<id>/config`: for each plugin role (`plugin_roles(host)` for each host,
    the board knows no role), for each host (`claude`, `copilot`): the value of `agent` and of
    `model` in each layer (defaults, project, surface; `null` where unset), the effective agent
    and model (identifier and name), the start (`plugin`, `named`, `generic`, or `refused` with the
    CLI's message), `tools`: `"the agent file's"` or `"the caller's, not restricted"`; per host
    the capability `NAMED_AGENT_MODEL_AT_START`; the catalog of each host (`MODELS[host]`: id and
    name) for the model choice; the other keys (`prices`, `board`, `ci`, `long_gate`, each role's
    `skills`/`tools` needs) as merged values with their layer, read-only (Q14); the files read and
    their problems with file and line; whether the page can write (`surface` mode and the project
    has a project folder); the surface file's relative path and its `sha256` (absent: `null`);
    and, when a batch is open, its id and the sentence "applies at the next batch".
  - `PUT /api/projects/<id>/config`, JSON body `{"changes": [{"host": null | "claude" |
    "copilot", "role": "<role>", "key": "agent" | "model", "value": "<text>" | null}],
    "base_sha256": "<hash or null>", "dry_run": true | false}`. `key` accepts only `agent` and
    `model` (Q14; any other: 400 naming the two). `host: null` writes under the top-level `roles`;
    a host writes under `hosts.<host>.roles`. `value: null` removes the key from the surface file
    (and a role, `hosts.<host>` or `roles` map left empty). It refuses, writing nothing:
    - with no surface: 409 `the configuration is read-only with no planning surface: edit
      chantier.yaml by hand` (Q7);
    - when the surface file's hash differs from `base_sha256`: 409, as `backlog/file` does;
    - when the surface holds both `.yaml` and `.yml`: 409 with Q1's message;
    - when the resulting text has a problem in reading or validation (a key, a value, a model no
      host's catalog resolves): 409 with the problem lines, the surface file named with the line
      numbers the new text would have.
    A start refused on one host (Q13: the user's agent with a model on Copilot) does not block the
    write: it is the user's configuration, valid for the other host; the answer's view shows it as
    `refused` with the CLI's message, and `open` on that host refuses it.
    With `dry_run: true` it writes nothing and answers the view the changes would give (as `GET`,
    with the problems), so the page shows a refusal as it is entered (Q13). Otherwise, on success
    it writes the surface's existing file (else creates `chantier.yaml`), UTF-8, LF, keeping the
    other keys and the comments of the file; answers the new view and the new `sha256`; adds one
    journal line (`config`, the role and key per change, e.g. `coder.model = gpt-6.1-terra
    (copilot)`). The board commits nothing: the surface's autosync commits it.
  - Both routes go through the existing key check and `_write`'s rules (415 for a non-JSON body,
    404 for an unknown project).
- The page (`web/js/views/config.js`, new; `registry.js` gains `{ id: 'config', icon: 'config',
  word: 'nav.config', module: config }`, no overview; an icon in `ui/icons.js`; styles in
  `web/css/views/config.css`; words in `i18n/en-board.js` and `fr-board.js`):
  - one table per host (Claude Code, Copilot), one row per role: role; agent (inherited value
    greyed with its layer, the surface's value editable as text); model (a choice among the host's
    catalog, plus "inherited"); effective agent and model; start: "named agent", "named agent,
    model given at the start", "generic agent: the caller's tools, not restricted", or the
    refusal's text in the error style; a line above each table states the host's capability
    ("starts a named agent with a model: yes / not yet");
  - a second section "All hosts" edits the top-level `roles` the same way (agent and model),
    the model typed as text (it is resolved per host; each host's result shows in its table);
  - each change of an agent or model field sends a `dry_run` `PUT`, and the rows show the result
    at once, the Copilot refusal of Q13 included;
  - "Save" sends the changes; a refusal shows its lines and keeps the edits; a 409 on the hash
    says the file changed and reloads it;
  - with an open batch: a banner "applies at the next batch" (Q4);
  - with no surface: the same tables, read-only, and the sentence "Edit `chantier.yaml` at the
    project's root by hand: the board writes only a planning surface's file";
  - the other keys (`prices`, `board`, `ci`, `long_gate`, `skills`/`tools` needs) are shown
    read-only as the merged values with their layer (Q14).
- `docs/web-board.md`: a section "### Configuration" under "The views" with a PC and a phone
  screenshot (`docs/web-board/config-pc.png`, `config-phone.png`, taken with the existing
  `docs-screenshots` recipe on the demo surface `docs/demo/`, which gains
  `projects/shop-api/chantier.yaml` setting one Copilot model so the page shows a generic start).

### 8. The Copilot eval's probe (`evals/copilot/RUNBOOK.md`, `evals/kit/copilot_models.py`), Q12

On top of copilot-role-models' section "Models" and script:

- `evals/copilot/RUNBOOK.md`, "Models", a new step after the fourteen starts and the script's
  first run (so its count of fourteen holds): the operator asks the Chief of Staff to start the
  plugin agent `chantier-coder` once more, with `task`, the prompt `model probe` and `model:
  gpt-6.1-terra` (a model other than its file's `gpt-6.1-sol`), and waits for its refusal line.
  Then the operator runs `uv run --no-project python <this checkout>/evals/kit/copilot_models.py
  --probe gpt-6.1-terra` on the same session and pastes its output into the report. The step says:
  when the probe prints `ran the requested model`, the finding goes to an inbox CR, offered by the
  Chief of Staff to the user, that sets `NAMED_AGENT_MODEL_AT_START["copilot"] = True` and updates
  `hosts/copilot.md`'s row; otherwise the report names the recorded model and the host's exact
  text, and nothing is worked around. "What it proves" gains a line: whether a named Copilot agent
  runs a model given at its start, from the host's own record.
- `evals/kit/copilot_models.py` gains `--probe <identifier>` (standard library only, writing
  nothing): it reads the same session's `events.jsonl` and takes only the last ended subagent event
  (`subagent.completed` or `subagent.failed`); it prints its type and the three fields of the
  script (`model`, `firstDispatchedModel`, `modelSelectionSource`, `absent` when missing), then
  `ran the requested model` and exits 0 when `model` equals the identifier, else `ran <model>,
  not the requested <identifier>` (or `no ended subagent event`) and exits 1. Without `--probe`
  the script behaves as copilot-role-models specified.

### 9. Project rules and docs

- `AGENTS.md` (the user's project rules; the Driver writes the sentences below and the PR's body
  says they change a project rule, for the user to read and approve in the diff at the merge):
  - "the user's `AGENTS.md`, and an optional `chantier.yaml` at the project's root, are the only
    configuration" becomes "... an optional `chantier.yaml` (or `chantier.yml`) at the project's
    root and, with an external planning surface, at the project's folder there, are the only
    configuration (the plugin's `config/chantier.defaults.yml` is the lowest layer, shipped)";
  - the board's exception: "it edits the backlog (...) only through the CLI's role-free commands"
    gains "and each role's agent and model in the project's configuration file in the planning
    surface (`projects/<name>/chantier.yaml`), through the CLI's own reading and validation of it".
- `docs/agents-and-models.md`, "Your own agents": the layers and their paths, `.yaml` or `.yml`
  (not both), the `hosts:` key, the four starts as a table (Copilot refuses the user's own agent
  with a model), "the caller's tools, not restricted" for a generic start, the board's page (agent
  and model only), "a change applies at the next batch", and Q15: `tools` and `skills` under a role
  list what the role needs, checked at preflight, and restrict nothing; to change a role's tools,
  name your own agent. "Models": the table's values come from `config/chantier.defaults.yml`; the
  sentence copilot-role-models wrote about `model-policy: required` becomes: "On Copilot the
  agent files' models run when no model is passed; a model you set starts a generic agent until
  Copilot is proved to start a named agent with a model (the eval's probe)". "A host that cannot
  set a model ... refuses a `model`" is removed. A note says a Spec-writer or Spec critic started
  generic, or as your own agent, is counted with the Chief of Staff's steering, not on the grill
  line (`cost --explain` says so).
- `docs/planning-modes.md`, "The planning surface": one sentence: the project's folder may hold a
  `chantier.yaml`, above the code repository's.
- `README.md` line "run the inspector on Opus": unchanged meaning; "a `model` for the role in
  `chantier.yaml` (or the surface's)".
- Release notes: as the project's release process asks (`just check` checks them).

### 10. Tests (`skills/chantier/scripts/cli/tests/`), few, parametrized, fast

- `test_plugin_files.py`:
  - `test_both_hosts_give_a_role_the_same_body_and_their_own_frontmatter`: the assertion
    `copilot["model-policy"] == "required"` becomes `"model-policy" not in copilot` (Q12); the
    rest of the line (`user-invocable`) stays.
  - new, parametrized over both hosts: every plugin role has exactly one default model in
    `config/chantier.defaults.yml`, equal to the identifier its agent file declares (Claude:
    `model:`; Copilot: the second item of `model: [name, id]`), and no default names a role the
    host has no agent for; the defaults file is valid.
  - copilot-role-models' parametrized test of `evals/kit/copilot_models.py` gains two cases of
    `--probe` on its fake session: the last ended event's `model` equal (exit 0, `ran the requested
    model`) and different (exit 1).
- `test_playbook_config.py`, parametrized cases on a prepared state (in-project and external):
  - layers: a key set in the project file and overridden in the surface file; a list replaced
    whole; a `prices` entry replaced whole; `hosts.<host>.roles` above `roles` in one layer;
  - Q1: both `chantier.yaml` and `chantier.yml` in one place refused with both paths, in the
    project and in the surface;
  - problems name their file (`projects/<name>/chantier.yaml:<line>:`);
  - the four starts of section 4 on each host (Claude: named with model; Copilot: generic, its
    `team:` line with `tools=(the caller's, not restricted)` and the contract lines printed by
    `take`; Copilot `agent` and model: the refusal's text, from `playbook` and `preflight`);
  - a model equal to the default: no model passed;
  - a running batch keeps its frozen playbook after a surface file changes (Q4);
  - `cost --explain` prints the grill note when `spec-writer` is configured with the user's agent;
  - the existing tests adjusted to the head line naming the files read, and copilot-role-models'
    cases that expected "cannot set a model when it starts an agent" to the generic start.
- `test_board.py`: `GET` and `PUT /config`: a valid write (the file written, comments kept,
  journal line, new hash), a `dry_run` (the view answered, nothing written), a stale hash (409,
  nothing written), an invalid model (409 with the line, nothing written), a key other than
  `agent`/`model` (400), no surface (409 read-only), both `.yaml` and `.yml` (409), and a Copilot
  agent with a model (written; the Copilot row `refused` with the CLI's message).

### 11. Scenario (`scenario/run_scenario.py`)

- §11 (`chantier.yaml`): one check that `chantier.yml` alone is read like `chantier.yaml`, one that
  both together exit 2 naming both.
- §20 (a planning surface): a code repository's `chantier.yaml` and a surface
  `projects/<name>/chantier.yaml` set the same role's model differently; `playbook` prints the
  surface's value with `[surface]`; `open` freezes it; the board's `PUT /config` changes it;
  `playbook --batch` still prints the frozen one and `playbook` the new one; the fake autosync
  commits the surface file; with `CHANTIER_HOST=copilot`, the role prints `agent=(generic)` and
  `take` prints its contract lines.

## Out of scope

- The Copilot model catalog, its refresh (copilot-model-catalog) and the Copilot agent files'
  `model:` values (copilot-role-models).
- Flipping Copilot's capability `NAMED_AGENT_MODEL_AT_START["copilot"]` to `True`: a later CR,
  after the user's Copilot run of the probe (Q12).
- Running any Copilot session.
- Any restriction of a role's tools by configuration (Q10); the existing `skills`/`tools` needs
  keys keep their meaning (Q15).
- Editing keys other than each role's `agent` and `model` from the board (Q14).
- Extending the cost code's named exception to find a generic or user-named Spec-writer or Spec
  critic for the grill line (the Chief of Staff's decision: it leaves the line, said by
  `cost --explain`).
- Prices, the cost computation and the escalation model (not moved to the defaults file).
- A user-level configuration file (in the home folder), and any layer other than the three above.
- A new `chantier` command to write the configuration; the board's page is the one writer besides
  a hand edit.
- Generated or temporary agent files of any kind (Q3).
- Changing a running batch's team (Q4).

## Evidence

- `just check` green on Linux, macOS and Windows; `just test` within its budget.
- `just scenario` green: the pipeline's `just scenario (ubuntu-latest)` job at the PR's head, and
  the local Windows run when the CR is on top of its stack (AGENTS.md). `hooks/` and `types/`
  untouched: no `just mod`.
- `git diff` of `com.github.copilot/agents/`: one line removed per file (`model-policy: required`),
  fourteen files, nothing else; `agents/` untouched.
- In the PR, the output of `chantier playbook` on chantier's own checkout with no user file (each
  role `model=(its file's)`), and with a surface file setting `coder: model: gpt-6.1-terra` under
  `hosts.copilot`, run with `CHANTIER_HOST=copilot` (generic line) and `CHANTIER_HOST=claude`
  (unchanged plugin agent); and with `coder: {agent: my-coder, model: gpt-6.1-terra}` under
  `hosts.copilot`, the refusal's line.
- Screenshots of the Configuration page (PC and phone) in the PR, from the demo surface.
- `evals/kit/copilot_models.py --probe` run on the test's fake session, its output pasted in the
  PR.
- The proofs on a real Copilot session are the user's later run; the PR's Known gaps names them:
  "a named Copilot agent started with a requested model not yet observed (the probe of
  `evals/copilot/RUNBOOK.md`, Models)", "a generic start on its configured model not yet observed
  in a real Copilot session", and the exact `agent_type` of Copilot's generic agent.
- No CI job is added or changed.

## Open questions

None.
