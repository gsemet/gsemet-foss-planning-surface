# CR-299 (A): investigation, round 0

Read only. Paths under `S/` are `skills/chantier/scripts/cli/src/chantier/`, `T/` is
`skills/chantier/scripts/cli/tests/`. Worktree base: the copilot-model-catalog branch. The project's rules
(`rules`) were read: AGENTS.md (no fallback, tests few/fast, `agents/` untouched, version never by hand,
the Driver writes the section-7 wording), CONTRIBUTING.md, docs/release-process.md (release notes folder
`docs/release-notes/YYYY-MM-DD-vX.Y.Z/`, scanned by `just check`).

## 1. State today (what the code does now)

- `S/playbook/config.py` (298 lines): `FILE = "chantier.yaml"`; `load(path, host, roles)` parses one file,
  keys `roles|prices|board|ci|long_gate`, returns `{file, host, roles, prices[, ci]}` or `None` when the
  file is absent; `load_board(path)` and `load_long_gate(path)` re-parse the file and check only their own
  key (the roles are "playbook's to judge"). Every problem line is `f"{FILE}:{line}: {msg}"`.
  Model check `_role_model` does resolve + the Copilot refusal (`SETS_MODEL_AT_START`) in one place.
- `S/playbook/yaml_subset.py`: `Node(kind, line, value)`; kinds scalar/list/map/null. `null` is produced
  only for an EMPTY plain value; a plain `~` or `null` is today a scalar "~"/"null" (the docstring the
  spec cites does not say it yet). Node keeps no quoting information.
- `S/plugin_files.py`: `read_playbook(repo, host)` = `load(repo.root / FILE, host, plugin_roles(host))`;
  it imports `config.load`, so a new module that needs `plugin_files` cannot be imported from `config`
  (cycle).
- `S/playbook/lines.py`: `playbook_lines(resolved, host, roles, recorded)` (head line, one line per role,
  `prices:`, `ci:`, `needs:`), `team_lines(resolved)`, `ci_lines`, `escalate_line`. `FILE` is printed in
  four places (head x2, prices line, ci line).
- Callers of the readers: `commands/rules.py` (`playbook`, line 52-75, the "not valid (n problems)" line),
  `commands/preflight.py` `_check_playbook` (P12, line 160), `commands/opening.py` (`open_batch` line
  263-287 reads and freezes `data.playbook = team minus prices`; `_brief_text` line 243 prints `FILE`),
  `commands/cost/pricing.py` `price_table` (reads `prices`, message names `chantier.yaml`),
  `commands/facts.py` line 107-108 (`team_lines(d.playbook)`, `ci_lines`), `board/address.py` `settings`
  (`load_board(repo.root / FILE)`), `board/command.py` line 131 (`from_config`, `projects.home.root / FILE`),
  `commands/gate.py` `_parallel` line 70 (`load_long_gate(repo.root / FILE)`).
  `core/records.py:190` `playbook: dict | None` is untyped: a new shape needs no schema change.
  Nothing in `hooks/` or `types/` reads the playbook (no `just mod`).
- `S/core/repo.py`: `Repo.root` (code repo, in external mode the clone), `surface` / `surface_root`,
  `project_dir` / `project_folder`, `session_root` (= surface or root), `external`.
- Agent files: `agents/<role>.md` `model:` = bare id; `com.github.copilot/agents/chantier-<role>.agent.md`
  `model: [Name, id]`. 14 roles on each host, all of them already on the base branch (Coder/Inspector Sol,
  Verifier/Debugger/Conflict resolver Terra, Investigator/Demo explorer Luna, Opus 5.5 for stack-driver,
  release-driver, spec-writer, spec-critic, retro-critic, Sonnet 5.5 for cr-driver, qa-driver on Copilot).
  Claude: retro-critic, spec-critic, spec-writer Opus, the rest Sonnet.
- Sources of "default model" that already exist and must not diverge: `T/test_plugin_files.py` constants
  `CLAUDE_OPUS_ROLES`, `COPILOT_OPUS_ROLES`, `test_both_hosts_give...` (line 208-210), and
  `evals/kit/copilot_models.py::expected(role)` (reads the agent file with a regex; unchanged, it still
  matches the agent files, so no change needed there).
- `T/test_plugin_files.py` EXISTS (spec section 8 says "new"): extend it, do not create it.

## 2. Map: spec section -> file / function

| Spec | Where | Change |
| --- | --- | --- |
| 1 layers, `.yml`, paths | new `S/playbook/layers.py`; `config.FILE` -> `FILES = ("chantier.yaml", "chantier.yml")` | `layer_files(repo)` -> list of `Layer(label, path, display, present)` weakest first, using `repo.surface_root`, `repo.project_folder`, `repo.root`, display path computed from `repo.session_root` (`Path.relative_to` else absolute `as_posix`); both-names problem per place |
| 1 per-layer check | `config.load` split in two: `parse_layer(path, display, roles_by_host)` (shapes, prices complete, board, ci, long_gate, role names/keys, hosts keys, top-level `roles` refused, resets) and a merge | per-layer check must be host-independent: `resolve(host, m)` for the section's own host; the Copilot "cannot set a model" test moves OUT of `_role_model` into the post-merge step |
| 1 merge, provenance | `layers.merge(layers)` | node-by-node dict merge; list/scalar replaced; `prices.<id>` replaced whole; keeps for each leaf `(label, display path, line)` and for each reset `(label, path, line)` |
| 1 `hosts` key | `config.load` top-level dispatcher (the `keyed` dict + `roles` branch) | new `_hosts` validator, host in `plugin_files.HOSTS` (config cannot import plugin_files: pass `HOSTS` and `plugin_roles` in as parameters or use `models.HOST_NAMES`' keys) |
| 1 unset node (Q20/Q23) | `yaml_subset.Node` + `layers.py` | see risk R1 |
| 1 readers | `plugin_files.read_playbook` (becomes a thin call into layers), `config.load_board`, `config.load_long_gate` (+ callers `address.py`, `command.py:131`, `gate.py:70`) | board/gate readers stay light: parse the user layers, check only their key, no plugin needed, no defaults file needed (R3) |
| 2 defaults file | new `config/chantier.defaults.yml` at the plugin root; read by `layers.py` through `plugin_files.plugin_root()` | 14 `hosts.claude.roles.<r>.model` + 14 `hosts.copilot...` ids, header comment. `models.py` comment above `MODELS` edited. `.gitattributes`: add `config/chantier.defaults.yml text eol=lf` (the catalog json has the same rule) |
| 2 missing file | `plugin_files.agent_problems` / `layers` | with plugin root: P12 problem naming the path; without: already "plugin is not installed" |
| 3 model vs default | post-merge step in `layers.py`/`config.py`; `lines._fields` | compare `resolve(host, configured).id == resolve(host, default).id`; equal and no `agent` -> record nothing for model (prints `model=(its file's)`), Copilot accepts; otherwise today's rule, message gains `<display path>:<line>` of the winning `model` key |
| 4 prints | `lines.playbook_lines`, `team_lines`, `ci_lines`; `commands/rules.py` lines 66-70; `commands/preflight.py` 160-171; `commands/opening.py` 243, 266-287; `commands/cost/pricing.py` 26, 64 | head names the user files read; per-value `[label]`; `[reset in <label>]`; record gets `files` and per-value layer labels; old records (key `file`, no `files`) print as today |
| 5 cards | `chief-of-staff.md` lines 33, 132-160 (+ lines 34, 42 mention `chantier.yaml`), `concepts.md` ~396 ("Starting an agent"), `hosts/claude-code.md`, `hosts/copilot.md` row "Models", `session-start.md:185`, 4 `SKILL.md` (chantier:19, chief-of-staff:27, griller:21, status:21) | wording; keep `test_startup_manifest.py` budget (STARTUP_LIMIT 12288 bytes, LF bytes) |
| 6 docs | `docs/agents-and-models.md` (lines 8-12 and its "Models" table), `docs/tutorial-claude-code.md` 205-210, `docs/planning-modes.md`, `README.md` 23 and 291, new `docs/release-notes/<date>-vX.Y.Z/release-notes.md` | release-notes folder is the version PR's; see Q2 |
| 7 AGENTS.md | `AGENTS.md` (the "plugin must work with no setup" bullet) | wording given in the spec |
| 8 tests | see section 5 | |
| 9 scenario | `scenario/run_scenario.py` `# 11. chantier.yaml` block (line 1737-1759, in the board unit), `external_surface` (line 7059, `SurfaceWorld` with `w.root/"code"`, `w.surface`, `w.project`) and `scenario/README.md:98` | new checks; the existing `chantier.yaml:3: board: ` must still hold |

## 3. Risks and traps

- R1 `yaml_subset` does not give the three distinctions the reset needs: plain `~`/`null` (today a scalar
  text), plain `default` vs quoted `"default"`, empty value (today `null`). Needed: a quoting flag on
  `Node` (e.g. `plain: bool`) and distinct empty vs `~` (e.g. `Node("null", value="~")` for `~`/`null`,
  `Node("null", value=None)` for empty, or a new kind `"reset"`). Every existing validator test
  `value.kind != "scalar"` then sees `~` as a non-scalar (today's `"agent" is one string` message), so the
  layer reader must intercept resets BEFORE the key checks (spec says so) and the empty `agent:` case must
  still reach today's refusal. `parse()` has one consumer (config.py); check `T/test_cli_units.py` and
  grep `yaml_subset` before changing the kind names.
- R2 Import cycle: `plugin_files` imports `config.load`; `layers` needs `plugin_root`, `plugin_roles`,
  `HOSTS`. Put the assembler (`read_playbook`) in `plugin_files` or in `layers` and import `plugin_files`
  from there, never the reverse; `config` stays pure (receives roles and the host list).
- R3 Board and gate readers: the board must start with no plugin installed and today ignores bad roles.
  Do not make `load_board` / `load_long_gate` read the defaults file or fail on role problems. But they must
  see resets (`board: default` in the repository over the surface root) and the both-names refusal
  (the scenario check "both together exit 2 naming both" is in the board unit). Suggest one internal
  `layers.read_key(repo, key)`.
- R4 The Copilot "cannot set a model" refusal is host-dependent and depends on the merged value; if kept in
  the per-layer check a surface layer's `model: opus` that the repository resets would still be refused.
  It moves after the merge (spec section 1 last bullets and section 3). A model name in `hosts.copilot`
  must still be `resolve`d in every view (typo stops Claude Code too); in `hosts.claude` on a Copilot view
  likewise.
- R5 What counts as "configured": `resolved["roles"]` today is only what the user wrote; `playbook_lines`
  prints `model=(its file's)` when the role has no model. The defaults layer must NOT enter
  `resolved["roles"]` (otherwise every role would print a model and `open` would freeze 14 roles, breaking
  `"playbook" not in record(repo)` for a project with no file). `read_playbook` must keep returning `None`
  when no user file is present (head line `playbook: no chantier.yaml, ...`, P12 `no chantier.yaml`,
  `open` records nothing). Keep the defaults in a separate attribute (host's default model per role) used
  only for the equality test.
- R6 Path display. In-project: today's strings verbatim (`chantier.yaml:3: board: ` in the scenario and
  in `T/test_gate_refusals.py:46`, `T/test_playbook_config.py:202`). With `.yml` the display is
  `chantier.yml`. External: relative to `repo.session_root` (the surface) with `/`; the code repo's file
  `projects/<name>/.repo/chantier.yaml` when the clone sits under the project folder, absolute POSIX when
  outside (the scenario's clone is `w.root/"code"`, outside the surface: absolute path; Windows drive
  letters `C:/...`). Tests must not hard-code a tmp path.
- R7 Line numbers of existing refusal tests shift when the form moves under `hosts: <h>: roles:` (+2 lines,
  +4 columns of indentation); `HEAD`, the 19 `REFUSALS` rows and `test_gate_refusals`' `LINE` need re-counting.
  The unknown-key message must keep the tail `"ci" and "long_gate"` (a test asserts it) and name `hosts`.
- R8 Reset semantics are subtle and need one rule written once: a reset at node N (a role, a key, `prices`,
  `prices.<id>`, `board`, `ci`, `long_gate`, `hosts.<h>`?) deletes N and its subtree from the accumulator
  of the WEAKER USER layers, records `(label, path, line)`, and a later (stronger) layer's write re-creates
  it (and clears the displayed reset? Q1). The defaults layer is held apart, so "the defaults' model comes
  back" is just "no configured model" (section 3). A reset of a node nobody set: accepted, nothing printed
  (spec) - decide whether it is printed (`[reset in X]` on a node with nothing under it): the spec says
  "changes nothing", so print nothing.
- R9 Frozen configuration (Q4): `open` freezes `team` minus `prices`; `files`, per-value labels and resets
  must be frozen with it, and `playbook --batch` / `take` `team:` lines read only the frozen record
  (T: "a surface file changes after open"). Keep `roles` values plain (`{"agent": "my-driver"}`), because
  `T/test_playbook_config.py:88` asserts that exact dict; put labels in a sibling key (`layers`).
  Old records (`file` key, no `files`) must print as today.
- R10 Packaging: the wheel is `packages = [".../chantier"]` only; `config/` is read through `plugin_root()`
  (needs `CHANTIER_PLUGIN_ROOT` or the `--skill` argument in `uvx --from` mode), as the agent files are. No
  manifest lists folders (`.claude-plugin/plugin.json`, `.github/plugin/plugin.json` list agents/skills
  only), so `config/` ships with the plugin folder. Add the file to CONTRIBUTING.md's tree (line ~135).
  In the tests, `repo` sets `CHANTIER_PLUGIN_ROOT`, so defaults are found; any test that blanks it hits the
  "not installed" problem.
- R11 Existing text that names `chantier.yaml` and is asserted: `prices: mystery-model (chantier.yaml,
  above the built-in table)` (`T/test_cost_reading.py:322`, scenario line 2416), `mystery-model has no
  price: add it under prices: in chantier.yaml (exact id: ...)` (`costs/pricing.py:64`, tests, scenario 2375 and
  2666, `references/status-layout.md:83`), `P12 ok ... no chantier.yaml`. Spec section 4 says the `prices:`
  line names the layer "in the place it names `chantier.yaml` today": see Q1. Keep the hint text
  (`add it under prices: in chantier.yaml`) unchanged: the spec lists it nowhere.
- R12 `test_startup_manifest.py` measures LF bytes of SKILL.md / hosts references: the wording changes in
  4 SKILL.md + session-start.md are +~60 bytes each, the budget is 12288 per role: measure before and after
  (`just test -k startup`).
- R13 Windows: UTF-8 without BOM for the new file (test "no tracked file starts with a BOM"); the loader
  reads `utf-8-sig`, so a user BOM is fine (test with BOM exists, line 75-80, keep it).
- R14 Sort/ordering of problems: today sorted by line inside one file; with layers, list per layer in
  layer order (weakest first), then by line. Pick one and test it.
- R15 CR-286-style "just scenario" runtime: only two or three added checks; the SurfaceWorld already exists.

## 4. Smallest change

1. `yaml_subset`: quoting flag + `~`/`null` as null (empty stays distinguishable). 
2. `config.py`: top-level dispatcher gets `hosts` and refuses `roles`; `_roles` becomes the per-host role
   validator (host-independent), the host-dependent model judgement moves out; pass `display` instead of
   `FILE`; `FILES` pair; drop `load`'s file reading into `layers.py`; keep `load_board` / `load_long_gate`
   signatures but take a list of layer files (or call `layers.read_key`).
3. `layers.py`: `Layer`, `read_layers(repo)`, `merge`, `resolve_host(merged, host, roles, defaults)` ->
   the same dict shape as today plus `files`, `layers` (labels), `resets`.
4. `plugin_files.read_playbook` delegates; `config/chantier.defaults.yml`.
5. `lines.py` + the four commands: labels, head, resets, frozen record.
6. Cards, docs, AGENTS.md, README, release notes; tests; scenario.

## 5. Tests

Existing tests to move under `hosts.<host>.roles` (`roles:` -> `hosts:\n  claude:\n    roles:`; line numbers +2):
- `T/test_playbook_config.py`: `HEAD` (line 19), `test_a_valid_file_is_resolved...` (line 77, 95, and
  `record(repo)["playbook"]["roles"]`), `test_ci_beside_the_gate_...` (107, 117), `test_ci_is_off_by_default`
  (126-127), `REFUSALS` rows: unknown role, an unknown key, empty role, tab, anchor, duplicate key, flow
  mapping, second document, unknown model, model with no letter (10 rows with line numbers to re-count;
  the ci / price / top-level key rows do not move except `"ci" and "long_gate"`), 
  `test_playbook_and_preflight_name...` (REFUSALS[0], HEAD+gpt, HEAD+opus, HEAD+claude-opus-5.5 on copilot:
  `hosts: copilot: roles:` for the Copilot ones, and the "cannot set a model" assertion gains the file:line),
  `test_with_no_chantier_yaml_again...` (244). The `team:` assertions (lines 89-90) gain `[repository]`.
- `T/test_gate_refusals.py`: `long_gate` only, no roles; add a surface-root case (spec section 8). It needs an
  external fixture: none exists in `T/` today (grep `external|surface|--project` in conftest/batch_helpers:
  nothing). Build one small `surface` fixture in `conftest.py` or `batch_helpers.py`: a git repo with
  `projects/<name>/` + `checkout.yml` (`repo: <clone>`), the clone being `repo` (see `core/repo.py:129-168`).
  This fixture is the main new cost of the test work (also for the board address test, `T/test_board.py`).
- `T/test_cost_reading.py:282-328` prices only: no roles move; only line 322 changes if Q1 says the label
  replaces `chantier.yaml`.
- `T/test_plugin_files.py`: extend (parametrize `host`): defaults file == agent files, one model per role,
  nothing else, no reset, valid (through `layers`).
- Scenario: `run_scenario.py` lines 3377 (long_gate), 2361 (prices), 1738 (board) do not use roles; only the
  two additions and §20.

New parametrized cases of spec section 8 map to `T/test_playbook_config.py`; keep them to ~6 parametrized
functions (layers order x host, reset spellings, both-names, top-level roles, path in problems, frozen)
to stay inside the 30 s `just test` budget; each uses the `repo` or the new `surface` fixture.

## 6. Questions only the user can answer

- Q1 Section 4 says the `prices:`, `ci:` and `needs:` lines name the LAYER where they name `chantier.yaml`
  today; for an in-project user that means `prices: mystery-model (repository, above the built-in table)`,
  which breaks `T/test_cost_reading.py:322`, scenario 2416 and reads less well than the file name. Is the
  layer label wanted there, or the file's display name, with the label only in brackets after values?
  (My default: use the display name of the file(s) that set the entries, e.g. `chantier.yaml`, so in-project
  output is unchanged; the label goes only in the `[...]` after role values.)
- Q2 Release notes: the version PR owns `docs/release-notes/<date>-vX.Y.Z/`. Does this CR (A) add a new
  folder for the unreleased version or wait for the release CR? (Spec section 6 says "as the project's
  release process asks".) 
- Q3 `agent` set AND `model` equal to the default: the spec gives only "no agent set". I assume the model is
  passed on Claude (user's agent, explicit model, as today) and refused on Copilot like any other.
- Q4 A reset written in a layer where nothing weaker sets the node: printed as `[reset in X]` or silent?
  Spec says "changes nothing"; I assume silent.

## 7. Suggested split into coder rounds

One round is too big (about 12 source files, 8 test files, 15 docs). Three rounds:

1. Round 1, engine: `yaml_subset` flags, `config.py` rework, `layers.py`, `config/chantier.defaults.yml`,
   `plugin_files.read_playbook`, the three light readers (board, gate, cost) and `lines.py` / `rules` /
   `preflight` / `opening` prints and frozen record; tests: move the existing ones under `hosts`, extend
   `test_plugin_files.py`, new `test_playbook_config.py` cases, the `surface` fixture. Exit: `just test`
   green, `chantier playbook` outputs in the PR.
2. Round 2, scenario and the readers' cross-layer tests: `run_scenario.py` (section 11 and section 20),
   `scenario/README.md`, `test_gate_refusals` / board address surface cases, `just scenario` locally.
3. Round 3, text: cards (section 5), docs (section 6), README, AGENTS.md wording, release notes,
   CONTRIBUTING tree, `.gitattributes`, startup budget check, `just check`.
(Rounds 2 and 3 are independent of each other and can run in parallel after 1.)

## 8. Evidence plan

Kind: CLI behaviour (text output, validation) plus docs; no UI, no `hooks/` or `types/` change (no `just
mod`, no pane screenshot).

- Before/after command output, captured in `evidence/` as `.txt` (UTF-8, no BOM), by running
  `$CHANTIER playbook --host claude` and `--host copilot`:
  1. chantier's own checkout with no user file: every role `model=(its file's)`, head `playbook: no
     chantier.yaml, ...` (before = base branch, after = head).
  2. a scratch surface (reuse `scenario/run_scenario.py`'s `SurfaceWorld` through `just scenario`'s §20
     steps, or a temp dir with a throwaway git surface and clone made in the scratchpad) with the three user
     files of the §20 step, then with the repository's `model: default`, then with the repository file
     removed; also `playbook --batch` after `open`. The scenario's own log already carries these checks;
     keep the raw run log in `work/gates/*.log` and put the excerpt in `evidence/`.
  3. one invalid file per layer (problem line with its `projects/<name>/chantier.yaml:<line>:` path), both
     names present, and a top-level `roles:` (the breaking-change line).
- `git diff main -- agents/ com.github.copilot/agents/` empty: output pasted.
- `just check` and `just test` output (time vs the 18.5 s + 30 s budget) and the local `just scenario`
  (`chantier gate`) run: log in `work/gates/`, pass/fail line in evidence.
- Cannot be shown: CI on ubuntu/macOS (the pipeline's job at the PR head), and the layer's behaviour on a
  real Copilot session (no Copilot runtime here; the Copilot view is shown with `--host copilot` only).
- Project rules on evidence: AGENTS.md asks a screenshot only for the CR board pane (not touched here), so
  none.
