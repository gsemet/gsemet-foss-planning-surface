# Change Specification: the web board's Configuration page

Date: 2026-11-16 (fourth run: each Copilot model's plans shown, read from `copilot_catalog()`;
third run: A's reset spelled `default` (Q23); second run: Q22 carried, and A's reset (Q20)
shown). Split from
model-defaults-board-config by its Q18 (the user's choice): (C), the third of a stack of three.
Sources: [request](intake/request.md); the grill is model-defaults-board-config's
[answers](../261116-2138-299-model-defaults-board-config/02-answers.md) (Q4, Q7, Q13, Q14, Q16, Q19, Q20, Q22,
Q23, the critic's text fixes, the Chief of Staff's AGENTS.md decision and reading of Q20) and its
[intent](../261116-2138-299-model-defaults-board-config/01-intent.md); copilot-model-catalog's
[answers](../261116-2119-298-copilot-model-catalog/02-answers.md), "The spec critic's question" (this page shows
each Copilot model's plans, read from `copilot_catalog()`), and its
[specification](../261116-2119-298-copilot-model-catalog/03-change-spec.md) (point 2, `copilot_catalog()` and
`plans`); this CR's [answers](02-answers.md). No tracker issue.

## Depends on, and the stack

The stack, bottom to top: [copilot-role-models](../261116-2017-297-copilot-role-models/03-change-spec.md),
[copilot-model-catalog](../261116-2119-298-copilot-model-catalog/03-change-spec.md),
[model-defaults-board-config](../261116-2138-299-model-defaults-board-config/03-change-spec.md) (A),
[role-model-per-host](../261116-2239-300-role-model-per-host/03-change-spec.md) (B), this CR (C).

- copilot-model-catalog: `MODELS[host]`, the page's model choice; `copilot_catalog()`
  (`playbook/models.py`), each Copilot model's `plans` (`pro`, `pro_plus`, `max`, `business`,
  `enterprise` as GitHub's plans table gives them, or `null` when that table does not name the
  model).
- A: the layers and their reading (`playbook/layers.py`: each layer's path, presence and
  problems, the merged tree with each leaf's layer and each reset's layer), the paths as printed,
  Q1's refusal, every role setting under `hosts.<host>.roles`, the reset with `default` (or `~`,
  `null`) (Q20, Q23).
- B: each role's start per host (`plugin`, `named`, `generic`, or Q13's refusal) and
  `NAMED_AGENT_MODEL_AT_START`.

## Goal

From the web board, the user sees for each host and each role which agent runs it, on which
model, from which layer, and how it starts, sees on which plans GitHub offers each Copilot model,
and changes a role's agent or model for one project
without opening a YAML file. The page writes only the project's file in the planning surface,
through the CLI's own reading, checking and writing of it; the surface's autosync commits it. A
change applies at the next batch. When the code repository's file overrides what the page writes,
the page says so and shows the value that applies: nothing hidden.

## Decisions carried from the grill

- Q7: the page writes only the surface's `projects/<name>/chantier.yaml`, committed by the
  autosync (the board commits nothing), and shows the inherited values and the effective one.
  With no surface the page is read-only and says to edit `chantier.yaml` by hand.
- Q19 (supersedes Q2's order): the layers, weakest to strongest: the shipped defaults, the
  surface root's `chantier.yaml`, `projects/<name>/chantier.yaml`, the code repository's
  `chantier.yaml`, merged node by node. So the file the page writes sits under the code
  repository's.
- Q22: when the code repository's `chantier.yaml` already sets the role's agent or model, the page
  still writes the surface project's file, and shows the row "overridden by <path>" with the
  effective value (the repository's); the edit is not refused, and takes effect if the
  repository's value goes.
- Q20, Q23 (A's): a layer's `default` (or `~`, `null`) unsets a node and the weaker value comes
  back; the page shows a reset where a layer holds one, spelled `default` (Q23). The Chief of
  Staff's reading of Q20: the page's own "inherited" removes the key from the surface project's
  file, a reset included, and never writes one (Q14 keeps the page to setting or removing `agent`
  and `model`). The page offers no agent or model named `default` (Q23).
- Q16: there is no role setting for all hosts: the page edits each host's roles only; it has no
  "all hosts" section.
- Q14: the page edits only each role's `agent` and `model`; the rest of the configuration
  (`prices`, `board`, `ci`, `long_gate`, each role's `skills`/`tools` needs) is shown read-only.
- Q13: on Copilot, the user's own agent with a model is refused; the board says it as it is
  entered.
- Q4: a change applies at the next batch; with a batch open the page says "applies at the next
  batch".
- Q1: a surface folder holding both `chantier.yaml` and `chantier.yml` is refused, both paths
  named.
- The critic's text fixes: the surface file's read, check and write are CLI code that the board
  only routes to (section 1); AGENTS.md's "plain JSON and Markdown" clause and the other places
  that say what chantier writes name this file (section 4).
- The Chief of Staff's decision: the AGENTS.md wording (section 4) is written by the Driver as
  below; the user reads and approves it in the PR's diff at the merge.
- copilot-model-catalog's answer to the spec critic's question (2026-11-16): the Configuration
  page shows each Copilot model's plans, read from `copilot_catalog()`. As that CR's Q7 says, a
  plan is shown and refuses nothing: no model is hidden, disabled or refused for its plans.
- Spec critic: yes (on the CR before the split).

## What changes

All CLI paths below are under `skills/chantier/scripts/cli/src/chantier/`.

### 1. The CLI's code for the surface file (`playbook/edit.py`, new; role-free)

The board knows no role and holds no configuration logic: it calls these two functions, as
`board/write_api.py` calls `lifecycle.backlog`.

- `config_view(repo)`: for each host of `plugin_files.HOSTS` and each role of
  `plugin_roles(host)`: the value of `agent` and `model` in each layer (A's labels: `defaults`,
  `surface`, `surface project`, `repository`; `null` where unset, `"reset"` where the layer writes
  `default`, `~` or `null`), the effective agent and model (identifier and name), the layer it
  comes from, and
  `overridden_by`: when the `repository` layer sets (or resets) the key the page writes for that
  row and host, the repository file's path as A prints it, else `null` (Q22); the start from B (`plugin`, `named`, `generic`, or `refused` with the CLI's
  line); `tools`: `"the agent file's"` or `"the caller's, not restricted"`. Per host:
  `NAMED_AGENT_MODEL_AT_START[host]` and the catalog (`MODELS[host]`: id and name; on Copilot
  each entry also carries `plans`, copied unchanged from the `copilot_catalog()` entry of the same
  identifier: the plans object as `copilot-models.json` holds it, or `null` when GitHub's plans
  table does not name the model; Claude Code's entries carry no `plans`). Also: the
  other keys (`prices`, `board`, `ci`, `long_gate`, the roles' `skills`/`tools`) as merged values
  with their layer; the files read and their problems (A's paths and lines); `writable` (external
  mode, the project has its folder); the surface project file's path from the surface root and its
  `sha256` (`null` when absent); and, when a batch is open, its id.
- `edit_surface_file(repo, changes, base_sha256, dry_run)`, `changes` a list of `{host, role, key,
  value}`, `host` one of `HOSTS` (Q16: no `null`), `key` `agent` or `model` (Q14), `value` a text
  or `null` (remove the key, and any `roles`, host or `hosts` map left empty; a reset the file
  held for that key, `default`, `~` or `null`, is removed the same way). It refuses, writing
  nothing, with a reason the board
  passes on:
  - no surface: `the configuration is read-only with no planning surface: edit chantier.yaml by
    hand` (Q7);
  - the file's `sha256` differs from `base_sha256`: the file changed since it was read;
  - both `chantier.yaml` and `chantier.yml` in the project's folder: Q1's line;
  - a key other than `agent` or `model`: the two keys named;
  - a `value` of `default`: A's line (no agent or model is named `default`; "inherited" is
    `null`);
  - the resulting text, read with A's checks and merged with the other layers, has a problem (a
    key, a value, a model the host's catalog does not resolve): the problem lines, the surface
    file named with the line numbers the new text would have.
  Two things do not block the write, and the view shows them:
  - a start refused on one host (Q13): it is the user's configuration; the view shows it
    `refused` with the CLI's line, and `open` on that host refuses it (B);
  - the code repository's file setting the same key (Q22): the surface project's value is
    written, and the view's row carries `overridden_by` and the repository's effective value.
  With `dry_run` it writes nothing and returns the view the changes would give. Otherwise it
  writes the project folder's existing file (else creates `chantier.yaml`), UTF-8, LF, keeping the
  file's other keys and its comments (ruamel.yaml's round trip, imported inside the function: the
  project bans it at module level), and returns the new view and `sha256`.
- It writes no other file, never the surface root's `chantier.yaml`, never the code repository's
  file, and commits nothing.

### 2. The board's routes (`board/config_api.py`, new, registered like `write_api.ROUTES`)

- `GET /api/projects/<id>/config`: `config_view` as JSON.
- `PUT /api/projects/<id>/config`, body `{"changes": [{"host": "claude" | "copilot", "role":
  "<role>", "key": "agent" | "model", "value": "<text>" | null}], "base_sha256": "<hash or
  null>", "dry_run": true | false}`: `edit_surface_file`; a refusal answers 400 (a key other than
  `agent`/`model`, a missing or unknown `host`) or 409 (the others), with the reason or the
  problem lines; a success answers the view and the new `sha256` (an overridden row answers 200
  like any other, its `overridden_by` set), and adds one journal line (`config`, per change e.g.
  `coder.model = gpt-6.1-terra (copilot)`, and `, overridden by <path>` when the view says so).
- Both go through the existing key check and `_write`'s rules (415 for a non-JSON body, 404 for an
  unknown project). Nothing else in `board/` changes.

### 3. The page (`board/web/js/views/config.js`, new)

- `registry.js` gains `{ id: 'config', icon: 'config', word: 'nav.config', module: config }`, no
  overview; an icon in `ui/icons.js`; styles in `web/css/views/config.css`; words in
  `i18n/en-board.js` and `fr-board.js`.
- One table per host (Claude Code, Copilot), one row per role: the role; the agent (the inherited
  value greyed with its layer, the `surface project` value editable as text); the model (a choice
  among the host's catalog, plus "inherited"); the effective agent and model with its layer; the
  start: "named agent", "named agent, model given at the start", "generic agent: the caller's
  tools, not restricted", or the refusal's text in the error style. A layer's reset is shown where
  its value would be, as "reset (default) in <layer>", whether the file writes `default`, `~` or
  `null`.
- Copilot's plans (copilot-model-catalog's answer): in the Copilot table's model choice, each
  option reads `<id> (<name>)` followed by its plans; under the Copilot table, a read-only list
  "Copilot models" gives each catalog model's identifier, name and plans, in the view's order. A
  plan the object marks `true` is named (`Pro`, `Pro+`, `Max`, `Business`, `Enterprise`), one marked
  `false` is not; any other value is shown next to the plan's name as the table gives it; `plans:
  null` reads "not in GitHub's plans table". No option is disabled, hidden or marked as refused for
  its plans. The plan names and the sentence are words in `i18n/en-board.js` and `fr-board.js`.
- Q22: when the row's `overridden_by` is set, the row keeps the `surface project` value as written
  (editable, saved like any other) and says next to it "overridden by <path>", with the effective
  value (the repository's) in the effective column; the edit is never disabled for it. A line
  above each table states the host's capability ("starts a named agent with a model: yes / not
  yet").
- Each change of an agent or model field sends a `dry_run` `PUT`; the rows show its result at
  once, Q13's refusal and Q22's "overridden by <path>" included.
- "Save" sends the changes; a refusal shows its lines and keeps the edits; a 409 on the hash says
  the file changed and reloads it.
- With an open batch: a banner "applies at the next batch" (Q4).
- With no surface: the same tables, read-only, and the sentence "Edit `chantier.yaml` at the
  project's root by hand: the board writes only a planning surface's file".
- The other keys (`prices`, `board`, `ci`, `long_gate`, `skills`/`tools` needs): read-only, the
  merged values with their layer (Q14). The files read and their problems are listed at the top.

### 4. Project rules and what chantier writes

The Driver writes them as below; the PR's body says they change a project rule, for the user to
read and approve in the diff at the merge.

- `AGENTS.md`, the "plugin must work with no setup" rule: "chantier writes only in the planning
  folder (...), as plain JSON and Markdown, and a CR's cleaned archive ..." becomes "... as plain
  JSON and Markdown, and the project's `chantier.yaml` in an external planning surface's project
  folder, from the board's Configuration page, and a CR's cleaned archive ...".
- `AGENTS.md`, the board's exception: "it edits the backlog (...) only through the CLI's role-free
  commands" gains "and each role's agent and model, per host, in the project's configuration file
  in the planning surface (`projects/<name>/chantier.yaml`), through the CLI's own reading,
  checking and writing of it".
- The same fact where the other texts say what chantier writes: `CONTRIBUTING.md` (the frame's
  sentence "as plain JSON and Markdown"), `README.md` ("Everything chantier writes is Markdown and
  JSON in the planning folder"), `skills/chantier/references/session-start.md` ("Zero
  configuration"), and `skills/chantier/SKILL.md` ("as plain JSON and Markdown"), each gaining
  "(and, from the board, a project's `chantier.yaml` in its planning surface)", or in a `SKILL.md`
  the shorter "(and the board's `chantier.yaml` edits)" if the startup budget
  (`test_startup_manifest.py`) needs it.
- `docs/web-board.md`: a section "### Configuration" under "The views" with a PC and a phone
  screenshot (`docs/web-board/config-pc.png`, `config-phone.png`, taken with `just
  docs-screenshots` on the demo surface `docs/demo/`, which gains
  `projects/shop-api/chantier.yaml` setting one Copilot model under `hosts.copilot.roles`, so the
  page shows a generic start); the section says that a value the code repository's file overrides
  is still written and shown "overridden by <path>" (Q22), and that the Copilot table shows each
  model's plans, from GitHub's tables, which refuse no model.
- Release notes, as the project's release process asks.

### 5. Tests (`skills/chantier/scripts/cli/tests/`), few, parametrized, fast

- `test_board.py`, parametrized over `GET` and `PUT /config`: a valid write (the file written,
  comments kept, journal line, new hash, autosync not called); a `dry_run` (the view answered,
  nothing written); a stale hash (409, nothing written); an invalid model (409 with the line,
  nothing written); a key other than `agent`/`model` and a `null` host (400); no surface (409
  read-only); both `.yaml` and `.yml` (409); a Copilot agent with a model (written, the Copilot
  row `refused` with the CLI's line); Q22: a repository file setting the same model (200, the
  surface file written, the row's `overridden_by` the repository file's path and the effective
  model the repository's, the journal line naming it); a `default` and a `~` in the repository
  shown `"reset"`; a `value` of `default` refused (409, nothing written); the `GET` with
  `copilot_catalog()` patched to a small catalog holding one model with plans and one with `plans:
  null`: each Copilot catalog entry's `plans` equals that catalog's for its identifier (`null`
  kept), and no Claude Code entry carries `plans`.
- `test_playbook_config.py`: `edit_surface_file` keeps a comment and an unrelated key, removes an
  emptied map, and removes a `default` or `~` the file held when the key is set back to
  "inherited".

### 6. Scenario (`scenario/run_scenario.py`)

- §20 (a planning surface): with a batch open, the board's `PUT /config` changes a role's model
  in the project folder's file; its answer says "applies at the next batch"; `playbook --batch`
  still prints the frozen value and `playbook` the new one; the fake autosync commits the surface
  file; the board commits nothing.

## Out of scope

- Editing any key other than each role's `agent` and `model` (Q14), the surface root's file, or
  the code repository's file from the board (Q7); writing a reset (`default`, `~`) from the page.
- Refusing or disabling an edit the code repository's file overrides (Q22).
- A setting for all hosts (Q16).
- A new `chantier` command to write the configuration: the page and a hand edit are the writers.
- The board committing or pushing anything; changing a running batch's team (Q4).
- The layers, the reset, the starts and the catalog themselves (A, B, copilot-model-catalog).
- The CR board pane (`hooks/register.tsx`): untouched, so no pane screenshot is needed.
- Refusing, warning on or filtering a model for its plans (copilot-model-catalog's Q7); plans on
  Claude Code (no catalog there); any other field of `copilot_catalog()` (release status, clients)
  on the page; editing the catalog from the board.

## Evidence

- `just check` green on Linux, macOS and Windows; `just test` within its budget.
- `just scenario` green: the pipeline's `just scenario (ubuntu-latest)` job at the PR's head, and
  the local Windows run when this CR is on top of its stack (AGENTS.md). `hooks/` and `types/`
  untouched: no `just mod`.
- The Configuration page's screenshots (PC and phone) in the PR and in `docs/web-board/`, from the
  demo surface, the PC one showing the "Copilot models" list with its plans.
- In the PR: one `PUT /config` and its answer on the demo surface, and the written file's diff;
  one `GET /config` answer with a row `overridden_by` a repository file, and its Copilot catalog
  entries with their `plans`.
- No CI job is added or changed.

## Open questions

None.
