# Change Specification: Copilot model catalog from GitHub's own tables

Date: 2026-11-16 (third run: the spec critic's text fixes; second run: the open questions closed
by [answers](02-answers.md)). Sources:
[original request](intake/request.md); the grill is copilot-role-models'
[answers](../copilot-role-models/02-answers.md), Q3 to Q9 and Q10 (this split), and its
[specification](../copilot-role-models/03-change-spec.md), "Out of scope"; this CR's
[answers](02-answers.md) to the first run's open questions. No tracker issue.

## Goal

chantier's list of the models Copilot offers (`MODELS["copilot"]`) stops being written by hand. It
is built from GitHub's own tables (`github/docs`, `data/tables/copilot/`) and the Copilot CLI
reference's "Supported models", copied into the repository and refreshed by one command run by
hand: the CLI itself never goes to the network. Each model's identifier (the value a Copilot call
takes, `gpt-6.1-terra`) comes from its display name (`GPT-6.1 Terra`) by one rule, the rule
copilot-session-usage already uses. Where GitHub's sources disagree, the refresh says so and
refuses nothing. Each model's plans are kept and shown. Prices stay with copilot-session-usage.

## The stack

Bottom to top: [copilot-role-models](../copilot-role-models/03-change-spec.md) (the four Copilot
`model:` lines; GPT-6.1 Terra added by hand to `MODELS["copilot"]`), this CR, then
[model-defaults-board-config](../model-defaults-board-config/03-change-spec.md), which resolves
its configuration's model names against `MODELS[host]` (`models.resolve`) and keeps, in the
comment above `MODELS`, "the catalog's source as copilot-model-catalog wrote it". This CR's branch
starts from copilot-role-models' head; it removes that CR's hand-written Copilot rows, Terra
included.

## Decisions carried from the grill

- Q3, Q4: a Copilot model is named by its identifier, never by its display name, and the
  identifier comes from a source, never a guess. GitHub's tables key every model by its display
  name only; the identifiers come from the runtime (`listModels()`, `/model --list --json`), which
  the CLI cannot call, hence the rule below and its check against the CLI reference.
- Q5, with the request's reading of copilot-session-usage (`_normalize_model_name` in
  `src/copilot_session_usage/_internal/core.py`): the identifier is the display name with each
  footnote marker (`[^...]`) dropped, `(preview)` dropped, every other parenthetical kept, lower
  case, each run of spaces made one `-`, dots kept, ends trimmed. `GPT-6.1 Terra` →
  `gpt-6.1-terra`; `Claude Sonnet 5[^promo]` → `claude-sonnet-5`; `GPT-5.3-Codex` →
  `gpt-5.3-codex`; `Claude Opus 4.8 (fast mode) (preview)` → `claude-opus-4.8-(fast-mode)`. The
  display name gets the same cleaning (footnote markers and `(preview)` dropped, case and spaces
  kept): `Claude Opus 4.8 (fast mode)`. The parentheses kept in the last identifier are
  copilot-session-usage's behaviour, reported there as
  [copilot-session-usage#67](https://github.com/gsemet/copilot-session-usage/issues/67); chantier
  follows the one rule and works nothing around.
- Q6 as superseded by Q10, and Q7: a model is in the catalog when any of GitHub's sources says the
  Copilot CLI or the Copilot App has it: `model-supported-clients.yml` with `cli: true`,
  `auto-model-selection.yml` with `cli: true` or `app: true`, or the CLI reference's "Supported
  models" table. GPT-6.1 Sol, missing from `model-supported-clients.yml`, is in through
  `auto-model-selection.yml`.
- Q7: a model's plans (`model-supported-plans.yml`) are shown; no plan refuses a model.
- Q8: the Investigator stays on `gpt-5.6-luna`. The comparison with the CLI reference's list
  (which names `gpt-6-luna` and no GPT-5.6 model) reports the difference and refuses nothing.
- Q9: no prices. `models-and-pricing.yml` is not copied; `chantier cost` on Copilot keeps its
  prices from copilot-session-usage (`costs/copilot.py`, `session_usage.py` untouched). A bug met
  in copilot-session-usage is reported as an issue on that project, never worked around here.
- Q10: this CR is the copy of GitHub's tables, `just copilot-models`, `copilot-models.json`,
  `MODELS["copilot"]` built from it, and their tests.
- The project's rule (AGENTS.md): the CLI needs no network; the tables are a copy kept in the
  repository, refreshed by a command.
- Spec critic: yes (copilot-role-models' grill; this CR touches the CLI).

## Decisions carried from this CR's answers (2026-11-16)

- Short names on Copilot: a short name (`opus`, `sonnet`, `luna`, `sol`, `terra`) that matches
  several catalog models is refused as ambiguous, the message listing the matching identifiers;
  the user writes the full identifier. No short name is kept resolving to the model chantier's
  agent files use (point 4).
- A model GitHub stops listing while a Copilot agent file names it: the refresh drops it from the
  catalog and reports it, and `just check` fails
  (`test_the_model_table_names_every_model_the_agent_files_name`) until the agent file changes.
  The catalog never keeps such a model, marked or not: nothing hidden (points 2, 3, 6). The
  Driver of this CR changes no agent file for it: it stops and reports it (point 3).
- Where a model's plans show: in `just copilot-models`' output and in `copilot-models.json`, as
  point 3 and point 2 say; no user command prints them in this CR. The board's Configuration page
  (board-config-page) shows them later (point 4).

## What changes

CLI paths below are under `skills/chantier/scripts/cli/src/chantier/`.

### 1. The copy of GitHub's sources (`playbook/copilot_tables/`, new)

- The files, each copied byte for byte from `github/docs` at one commit:
  - `model-supported-clients.yml`, `auto-model-selection.yml`, `model-release-status.yml`,
    `model-supported-plans.yml` (from `data/tables/copilot/`);
  - `cli-supported-models.md`: the section "Supported models" of
    `content/copilot/reference/copilot-cli-reference/cli-command-reference.md`, from its heading to
    the next `## ` heading, verbatim.
- Not copied: `models-and-pricing.yml` (Q9), `model-comparison.yml`,
  `model-deprecation-history.yml`.
- `SOURCE.json`: the repository (`github/docs`), the full commit SHA the files were taken at, the
  date of the refresh, and each file's path in `github/docs`.
- The folder is inside the package, so it ships with the CLI (hatchling takes every file under
  `packages`); `.gitattributes` gains `skills/chantier/scripts/cli/src/chantier/playbook/copilot_tables/** text eol=lf`
  and `skills/chantier/scripts/cli/src/chantier/playbook/copilot-models.json text eol=lf`, so a
  Windows checkout with `core.autocrlf=true` keeps the bytes and the drift test (point 6) compares
  like for like (the trap commit 82d8863 fixed for the startup budget).

### 2. The catalog (`playbook/copilot_catalog.py`, new; `playbook/copilot-models.json`, new)

- `copilot_catalog.py` builds the catalog from the copy, reading local files only (no network
  module imported): YAML through `ruamel.yaml` imported inside the function (the project bans it
  at module level), the CLI reference's table by its rows `` | `<id>` | ... | ``.
  - `identifier(name)` and `display_name(name)`: the Q5 rule above.
  - The catalog: every model the Q7 rule admits, keyed by identifier; a name two tables write
    differently but that gives one identifier is one model. For each model: `id`, `name` (the
    cleaned display name: `model-release-status.yml`'s when it names the model, else that of the
    first table naming it, in the order of point 1's list; for a model only the CLI reference
    names, its identifier, see differences), `release_status` (from `model-release-status.yml`,
    else `null`), `cli` and
    `app` (from the client tables: `true`, `false`, or `null` when no table names the model),
    `plans` (`pro`, `pro_plus`, `max`, `business`, `enterprise` as the plans table gives them,
    `null` when the table does not name it), `in_cli_reference` (`true`/`false`: `false` marks an
    identifier derived by the Q5 rule that the CLI reference does not list, so unproved until the
    runtime's `listModels()` shows it; `claude-opus-4.8-(fast-mode)` is likely not what Copilot
    takes, copilot-session-usage#67), and `sources` (the files that name it). Sorted by
    identifier, for stable diffs.
  - Only what GitHub's sources admit is in the catalog: a model an agent file names but no source
    lists any more is not kept (this CR's answers).
  - The differences, one plain line each, refusing nothing, built from the copied tables alone
    (so the JSON and its drift test depend only on `copilot_tables/`):
    - a catalog model the CLI reference does not list (`gpt-5.6-luna: in the tables, not in the
      CLI reference's Supported models`, Q8);
    - a CLI reference identifier that no table's name gives (its display name is then its
      identifier);
    - a model the client tables disagree on (`gpt-6.1-sol: absent from
      model-supported-clients.yml, cli and app in auto-model-selection.yml`, Q7);
    - a catalog model with no release status or no plans row;
    - two catalog identifiers that share one `models.normalise` key (e.g.
      `claude-opus-4.8-(fast-mode)` and `claude-opus-4.8-fast-mode`), named as a pair; nothing is
      merged (point 3 says what the Driver does).
  - `agent_file_differences(catalog, agents_folder)`, a separate function, compares the catalog
    with the Copilot agent files (`com.github.copilot/agents/*.agent.md`, `model: [name, id]`),
    one plain line each: an identifier an agent file names that the catalog does not hold
    (`gpt-5.6-luna: named by com.github.copilot/agents/chantier-investigator.agent.md, not listed
    by GitHub; the agent file must change`), and an agent file's display name that differs from
    the catalog's `name` for its identifier. These lines are printed by the refresh (point 3) and
    never written to `copilot-models.json`.
- `copilot-models.json`: `{"schema": 1, "source": <SOURCE.json's content>, "models": [...],
  "differences": [...]}`, UTF-8, two-space indent, LF, written only by the refresh (point 3).
- `playbook/models.py`:
  - `MODELS["copilot"]` is built at import from `copilot-models.json` (standard `json`, read
    through `importlib.resources` or the module's folder): one `Model(id, name, "")` per catalog
    model, in the file's order. `MODELS["claude"]`, `Model`, `SETS_MODEL_AT_START`
    (`copilot: False`), `ESCALATION` (`copilot: None`), `normalise`, `resolve`, `HOST_NAMES` do not
    change.
  - The comment above `MODELS` says where each host's list comes from: Claude's, from the plugin's
    agent files, by hand; Copilot's, from `copilot-models.json`, built by `just copilot-models`
    from GitHub's tables (`github/docs`, `data/tables/copilot/`) and the Copilot CLI reference's
    "Supported models", never edited by hand. model-defaults-board-config keeps this sentence.
    It also says that an identifier with `in_cli_reference: false` is derived by the rule,
    unproved until `listModels()`.
  - One function, `copilot_catalog()`, returns the file's models with their status, clients and
    plans, for later readers (model-defaults-board-config's board list, board-config-page);
    nothing in the CLI prints it in this CR beyond what point 4 says.
- A missing or unparsable `copilot-models.json` is a bug of the release, not a user's state: the
  import fails with the file's path; no fallback list.

### 3. The refresh (`scripts/copilot_models.py`, new; `justfile`)

- `justfile` gains, next to the other maintainer recipes:
  `# Refresh the Copilot model catalog from GitHub's tables (network; by hand, not in check)` and
  `copilot-models *args:` running `{{run-cli}} scripts/copilot_models.py {{args}}` (the locked
  project, so it uses the package's `copilot_catalog.py` and `ruamel.yaml`).
- `scripts/copilot_models.py` (standard library for the network, `urllib.request`):
  - takes the commit to copy from `--ref <sha>`, else `github/docs`'s `main` head
    (`https://api.github.com/repos/github/docs/commits/main`, its `sha`); fetches each file of
    point 1 from `https://raw.githubusercontent.com/github/docs/<sha>/<path>`;
  - stops with the URL and the error, writing nothing, on any failed download, a missing "Supported
    models" section, or a table it cannot parse; it writes nothing either when the catalog built
    is empty;
  - otherwise writes the copy (point 1), `SOURCE.json`, and `copilot-models.json` built by
    `copilot_catalog.py` from the files it just wrote;
  - prints the commit, one row per model (identifier, display name, release status, CLI, App,
    plans, in the CLI reference), then the differences under `differences:` (or
    `differences: none`), then `agent_file_differences`' lines under `agent files:` (or
    `agent files: none`), and exits 0 whatever the differences, a dropped model an agent file
    names included (`just check` is what stops it, point 6).
- The commit that follows a refresh is the maintainer's (the CLI keeps no git write); the PR shows
  the diff of the copy and of the JSON.
- What the Driver of this CR does with the refresh's lines (behaviour, never a workaround):
  - a model a current agent file names that the refresh drops (e.g. Luna, should it fail Q7's
    rule): it stops and reports it to the user, and changes no agent file;
  - a pair of identifiers sharing one `normalise` key: it reports the pair to the user and never
    merges or edits the catalog by hand; `test_the_model_table_names_no_model_twice_per_host` is
    the stop.
- `CONTRIBUTING.md`, in the commands list: `just copilot-models  # refresh the Copilot model
  catalog from GitHub's tables (network), then review the diff and its differences`, and one
  sentence where the release steps list what to check before a release: run it, and carry the
  differences that touch an agent file's model into the PR; a model GitHub no longer lists that an
  agent file names makes `just check` fail until the agent file changes.

### 4. What the user sees

- `chantier playbook --host copilot` and `chantier preflight` resolve a `chantier.yaml` `model:`
  against the larger catalog (about thirty models on 2026-11-16), then refuse any model on
  Copilot with "cannot set a model when it starts an agent", as today. The unknown message lists
  the catalog's `id (name)` pairs, as today, so it gets longer.
- Short names that resolved alone on Copilot become ambiguous, since GitHub lists several models
  of a family: `opus` (Claude Opus 4.8, 4.8 (fast mode), 5, 5.5), `sonnet`, `luna` (GPT-5.6, GPT-6),
  `sol`, `terra` (GPT-5.6, GPT-6.1). Such a name is refused as ambiguous, the message listing the
  matching identifiers; the user writes the full identifier (this CR's answers). On Copilot the
  result is a refusal either way today; the message changes from "cannot set a model" to
  "ambiguous". Claude Code's resolution does not change.
- Plans (Q7) are shown in the refresh's output and kept in `copilot-models.json`; no user command
  prints them in this CR, and the board's Configuration page (board-config-page) shows them later
  (this CR's answers).

### 5. Documentation

- `skills/chantier/references/hosts/copilot.md`, row "Models": after the agent files' sentence,
  "chantier's list of Copilot models is a copy of GitHub's tables (`github/docs`,
  `data/tables/copilot/`) and of the CLI reference's "Supported models", refreshed by
  `just copilot-models`; a model's plans are shown, none refused. An identifier the CLI reference
  does not list is derived by the rule, unproved until `listModels()`." The "Startup core" section
  does not change (`test_startup_manifest.py` holds).
- `docs/agents-and-models.md`, after "the CLI ... turns a model name into an exact identifier":
  on Copilot, the names it knows are GitHub's (the tables above), the identifier being the display
  name with each footnote marker (`[^...]`) and `(preview)` dropped, every other parenthetical
  kept, in lower case, each run of spaces made one `-`, dots kept, ends trimmed (Q5, point 2); an
  identifier the CLI reference does not list is derived by that rule, unproved until
  `listModels()` (for example `claude-opus-4.8-(fast-mode)`, likely not what Copilot takes,
  copilot-session-usage#67); a short name such as `opus` can match several Copilot models and is
  then refused as ambiguous, with the matching identifiers: write the identifier.

### 6. Tests (`skills/chantier/scripts/cli/tests/`)

Few, parametrized, fast; no network:

- New `test_copilot_catalog.py`:
  - the identifier rule, parametrized on the request's and Q5's examples (`GPT-6.1 Terra`,
    `Claude Sonnet 5[^promo]`, `GPT-5.3-Codex`, `Claude Opus 4.8 (fast mode) (preview)` →
    `claude-opus-4.8-(fast-mode)`, `Claude Sonnet 5.5`), and the display name's cleaning;
  - the committed `copilot-models.json` equals what `copilot_catalog.py` builds from the committed
    `copilot_tables/` (no drift, no hand edit);
  - on small tables written in a temporary folder: a model only in `auto-model-selection.yml`
    with `app: true` is in (the Sol case); a model with `cli: false` in every client table and
    absent from the CLI reference is out; a model in the tables but not the CLI reference is in,
    with its difference line (the Luna case); a CLI reference identifier no table names is in,
    named by its identifier, with its difference line; a model with `pro: false` keeps it in
    `plans` and is in; two names giving identifiers that share one `normalise` key give a
    difference line naming the pair; a model named differently by two tables takes
    `model-release-status.yml`'s cleaned name, else the first table's;
  - `agent_file_differences` on a temporary agents folder: an identifier no table lists is out of
    the catalog, with its line naming the agent file; a display name differing from the catalog's
    gives its line; neither line is in the built JSON.
- `test_plugin_files.py`:
  - `test_the_model_table_names_every_model_the_agent_files_name`, as copilot-role-models' point 5
    extends it (on Copilot, the agent file's display name equals `MODELS`' name for that
    identifier), holds unchanged, now against the built catalog: every Copilot agent file's
    identifier, `gpt-5.6-luna` and `gpt-6.1-terra` among them, resolves to itself, and its display
    name equals the catalog's `name` (the source rule of point 2). It is the stop when GitHub
    drops a model an agent file names or names it differently;
  - `test_the_model_table_names_no_model_twice_per_host` holds unchanged; it is the stop when two
    catalog identifiers share one `normalise` key.
- `test_playbook_config.py`, `test_playbook_and_preflight_name_the_problem_and_its_line`: the
  Copilot `model: gpt` case still finds "ambiguous" with Luna and Sol; the `model: opus` case on
  Copilot becomes `model: claude-opus-5.5` for the "cannot set a model when it starts an agent"
  refusal, and `model: opus` on Copilot is checked "ambiguous" with the matching Opus identifiers
  in the message.
- The `just test` budget is unchanged (the JSON is read once at import).

## Out of scope

- Prices of any kind on Copilot, and `costs/` (Q9).
- Reading the account's models at run time (`listModels()`, `/model --list --json`), and any
  network access from the CLI.
- The Copilot agent files' `model:` lines and the role models (copilot-role-models), Claude's
  models, `ESCALATION`, `SETS_MODEL_AT_START`.
- Refusing or warning on a model for its plan, its release status, or its absence from the CLI
  reference (Q7, Q8): reported only.
- A short name kept resolving on Copilot, and a model kept in the catalog because an agent file
  names it (this CR's answers).
- Showing plans in a user command or on the board (board-config-page).
- Retired models (`model-deprecation-history.yml`) and the comparison table.
- A scheduled or CI refresh; the refresh is by hand.
- The configuration layers, the board's model list and any change to `resolve`
  (model-defaults-board-config and its stack).
- Fixing copilot-session-usage#67 (that project's).

## Evidence

- `just check` green on Linux, macOS and Windows (lint and types cover `copilot_catalog.py`; the
  new tests run with no network).
- `just scenario` green (the CLI changes): the pipeline's `just scenario (ubuntu-latest)` at the
  PR's head, and the local Windows run when the CR is on top of its stack (AGENTS.md). `just mod`
  is not needed (`hooks/`, `types/` untouched).
- `just copilot-models` run once by the Driver, its output pasted in the PR (the commit of
  `github/docs`, the model rows, the differences, among them `gpt-5.6-luna` not in the CLI
  reference and GPT-6.1 Sol absent from `model-supported-clients.yml`, and its `agent files:`
  lines); the committed copy and JSON are that run's. A dropped agent-file model or a `normalise`
  pair in that output stops the Driver, who reports it to the user (point 3).
- `git diff`: `costs/`, `session_usage.py`, `agents/`, `com.github.copilot/agents/` untouched;
  `models.py` loses its hand-written Copilot rows.
- `chantier playbook --host copilot` with no `chantier.yaml` prints the plugin's agents as before;
  with `model: claude-opus-5.5` under a role it refuses with "cannot set a model when it starts an
  agent"; with `model: opus` it refuses as ambiguous, listing the matching Opus identifiers.
- No CI job is added or changed.
