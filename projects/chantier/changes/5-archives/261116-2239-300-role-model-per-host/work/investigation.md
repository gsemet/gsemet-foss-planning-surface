# CR-300 investigation: a model per role on each host

Read only, in the worktree `C:\Users\gaeta\Projets\chantier.worktrees\batch-22-CR-300`, head
`6f132fe` (CR-297/298/299 in the base). CLI paths are under
`skills/chantier/scripts/cli/src/chantier/` unless a path starts with another folder. Project rules
read: `AGENTS.md` (the CLI knows no role, agent files hand-written and identical in body on both
hosts, tests few and fast, `just check`, `just scenario`, no `hooks/` or `types/` change so no
`just mod`).

## The smallest change, in one paragraph

Four places carry it. (1) `playbook/models.py`: rename the capability, give a Copilot `Model` its
identifier as `start`. (2) `playbook/layers.py::_model_problems` (not `config.py`, see
"Disagreements"): replace the "host cannot set a model" refusal with the four starts, record `start`
in each resolved role, refuse `agent` plus a model on a host that cannot. (3) `playbook/lines.py`
and `plugin_files.py`: print `agent=(generic) ... tools=(the caller's, not restricted)` and the
contract lines. (4) `commands/cost/command.py`: the grill note. Everything else is one line removed
from `chantier-coder.agent.md`, reference and doc text, the probe, tests and one scenario block.

## 1. The host capability

- File: `playbook/models.py:53`, `SETS_MODEL_AT_START = {"claude": True, "copilot": False}`, with the
  comment lines 51-52. Only one user: `playbook/config.py:12` (import) and `:107`
  (`start_refusal`). Nothing in tests, scenario, board or docs names the constant (grep done), so the
  rename `NAMED_AGENT_MODEL_AT_START` touches two files plus comments. `ESCALATION` unchanged.
- The spec's comment text for the constant goes in `models.py`; keep it under the CLI's line length
  (ruff, `just lint`).
- Trap: `hosts/*.md` rows and the spec name the constant; the references must say the same name.

## 2. The Copilot start value

- `playbook/models.py:47`: `"copilot": tuple(Model(m["id"], m["name"], "") for m in copilot_catalog())`.
  Change `""` to `m["id"]`. The catalog build already lives in this module (the spec says "where
  copilot-model-catalog builds it": it is here, `copilot_catalog()` reads `copilot-models.json`).
- Today a Copilot model prints as `model= (id, Name)` (empty start), so nothing that printed a
  Copilot model before was usable: no legacy Copilot batch record can hold one (A refused it).
- `escalate_line` (`lines.py:112`) uses `found.start`; Copilot's `ESCALATION` is `None`, unaffected.
- Existing tests: `test_copilot_catalog.py` has no assertion on `start` (grep): add one inside an
  existing parametrized case (`start == id` for every Copilot model, `MODELS["claude"]` starts still
  aliases).

## 3. The four starts

Where the code is now:

- `playbook/layers.py::load` (l.229-267) merges the user layers, `config.typed` gives `roles` for the
  host, then `_model_problems(roles, nodes, host, defaults_tree)` (l.270-287). That function already
  has everything: `rec` (`agent`, `model` as `{"id","name","start"}`), the defaults tree via
  `default_model(defaults, host, role)`, and the model node (`nodes[role].value["model"][1]`, with
  `.src` and `.line`) used for the problem line `"{src}:{line}: {why}"`.
- Today: model equal to the default and no `agent` is deleted from `rec` (and the role from `roles`
  when `rec` empties); otherwise `config.start_refusal(host, role)` (config.py:105-113) refuses on a
  host whose flag is False, with "cannot set a model when it starts an agent ...".
- The four starts, in that function (suggest renaming it, it now also sets `start`):
  - no model left (none, or equal to default, no agent) and no `agent`: `plugin`;
  - `agent` only: `named`;
  - model not default, no `agent`: `named` if the host flag is True, else `generic`;
  - `agent` and a model: `named` if True, else the refusal at the model node's `src:line`
    (Q13, the spec's text with `HOST_NAMES[host]`, `HOST_FILES[host]` for `hosts/<file>.md`,
    section name "Models at an agent's start").
  `start_refusal` becomes the Q13 text only (or is replaced by it).
- Record `start` on every `rec` that stays in `roles`. A role kept for `skills`/`tools` only has
  no agent and no model: `start` is `plugin` for it too. Roles absent from `roles` are `plugin`
  by absence (the `playbook` line prints the plugin default for them).

Traps:

- `layers._labels` (l.299-316) builds `{k: nodes[r].value[k][1].layer for k in rec}`: a `start` key
  in `rec` raises `KeyError` there (and `lines.rec_labels` / `_fields` iterate `rec` keys). Either
  add `start` to `rec` after `_labels` ran, or have `_labels` skip it. Check `lines._fields`: it
  only reads `agent`, `model`, `skills`, `tools`, so an extra `start` is safe in the printing.
- `config.typed` returns `roles` from `_roles`; `_role_model` builds the dict
  `{"id","name","start"}`, so `rec["model"]["start"]` already exists (empty on Copilot today, the
  identifier after section 2). Do not confuse it with the role-level `start` word.
- Each host's section is validated in every view (`config._hosts` checks models of both hosts),
  the start decision only for the asked host (`typed(... host=host)`), which is what Q16 and "the
  other host's view is unaffected" need. A refusal in the Copilot view leaves `playbook --host
  claude` valid: test it.
- `playbook`, `preflight` P12 and `open` all go through `plugin_files.read_playbook` ->
  `layers.load`, so they refuse together with no extra code (`rules.py:63`, `preflight.py:160`,
  `opening.py:269`). Exit code 2 (`EXIT_PRECONDITION`) already for `playbook` and `open`; P12 FAIL
  line `P12 FAIL <src>:<line>: ...`.
- `cost/pricing.py::price_table` also calls `read_playbook` for Claude only and raises on problems.
- `playbook --batch` reads `d.playbook` and never validates again: a frozen record cannot be
  refused. Records made before the change have no `start`: treat a missing `start` as before.

Existing tests to extend (move, do not add many):

- `tests/test_playbook_config.py::test_playbook_and_preflight_name_the_problem_and_its_line`,
  lines 255-262: the "claude-opus-5.5 on Copilot, no agent" case currently expects the refusal; it
  becomes the `generic` case (exit 0, `agent=(generic)` line). Add there the `agent` + model case
  on Copilot (exit 2, the Q13 text, `chantier.yaml:5:`, plus the Claude view of the same file
  valid, plus `preflight` P12 FAIL).
- `tests/test_playbook_layers.py::test_a_model_equal_to_its_agents_is_not_passed_unless_the_agent_is_set_too`,
  lines 146-165: its "with an agent: passed, refused" step (l.154-159) keeps meaning but asserts
  "cannot set a model": change to the Q13 wording ("cannot start a named agent with a model").
- `test_playbook_layers.py:205-231` (a reset model accepted on Copilot): unaffected, but its name
  mentions Copilot models; keep.
- `tests/test_cli_runs.py::test_the_plugin_runs_with_no_setup...` is parametrized on both hosts and
  needs no change (no configuration).
- `scenario/README.md` l.98-103: the coverage bullet says "a model on a host that cannot set one at
  a start" as refused; `tests/test_scenario_coverage.py` only checks that each bullet names an
  existing unit/test, so a stale bullet will not fail, but fix the text.

## 4. What the CLI prints

Current code:

- `playbook/lines.py::playbook_lines` (l.62-103): per role `"{role}: " + _fields(rec, agent, True,
  labels, resets)`; the agent is `rec.get("agent") or default_agent(host, role)`;
  `_fields` prints `agent=`, `model=` (via `_model_text`: `start (id, name)`) or `model=(its
  file's)`, then skills/tools. `_labelled` appends `[layer]`.
- `lines.team_lines(resolved)` (l.138-146): only configured roles; `agent` is `rec.get("agent")`
  (none printed when the plugin's agent runs). Callers: `commands/facts.py:107` (`take`, `round`,
  `handoff` through `cr_facts`).
- Prompt first lines: `plugin_files.chief_prompt_lines(host, root, started_by)` (l.166) from the
  agent file descriptions ("Prompt starts with: `chantier <role> for the Chief of Staff, ...`"),
  called by `commands/rules.py:74`; `worker_prompt_lines(host, root, cr, title, batch)` (l.186)
  from files whose description says "Started by a Driver." and whose body has "Your card is `x.md`",
  called by `facts.py:109`.

Change needed:

- `generic`: `_fields` prints `agent=(generic)` (not the plugin name, not `rec["agent"]`),
  `model=...` with its label, and ends with ` tools=(the caller's, not restricted)`. The
  `tools=` key already means the user's `tools:` need list in `_fields` (l.40-44): the new text must
  not be mistaken for it (the spec's literal `tools=(the caller's, not restricted)`, placed before
  or after a `tools=a,b` need? decide, see Questions). The `needs:` lines (l.93-102) stay.
- `named` with the plugin's agent and a model: nothing new in the print (the line is the same as
  today's Claude case).
- Both functions need the role's `start`: `rec["start"]`, and for `playbook_lines` a role absent
  from `configured` is `plugin`. A missing `start` (a batch opened before) prints as today.
- Contract lines: `chief_prompt_lines` and `worker_prompt_lines` need `resolved` (the playbook) as a
  new argument and a helper in `plugin_files.py` that returns an agent file's body: split at the
  closing `---` of the frontmatter, `read_text(encoding="utf-8")` (Python text mode folds CRLF, so
  `splitlines()` never leaves a `\r`), indent each line by two spaces, and put it right after
  the opening lines (workers: after the third line; Chief roles: after the first-line row).
  Heading text from the spec: `<role> contract (a generic agent: copy it unchanged, without the
  two leading spaces, after the opening lines):`.
- `open`: nothing to write: `opening.py:288-290` stores `team` minus prices as `data.playbook`, so
  the roles dicts carry `start` once `layers.load` sets it. Test `record(repo)["playbook"]["roles"]
  [...]["start"]` (existing helper `batch_helpers.record`, see
  `test_a_valid_file_is_resolved_recorded_and_kept_by_the_running_batch`, l.93).
  Note the existing assertion at `test_playbook_config.py:93`
  (`roles["cr-driver"] == {"agent": "my-driver"}`) and `test_playbook_layers.py:180`
  (`frozen["roles"] == {"cr-driver": {"agent": "my-driver"}}`) will gain `"start": "named"`: update
  both.
- `playbook --batch` takes the host from `d.host` and prints the recorded `start`; `take` uses
  `d.host` for `worker_prompt_lines`.

Traps:

- Ten-line cap: `concepts.md:389-390` exempts `take`, `round`, `handoff`, `playbook`, `cost`,
  `preflight`, `status`... so a longer output is fine. `open` is not exempt and prints nothing
  new. The test constant `MAX_OUTPUT_LINES = 10` in `tests/test_cli_runs.py:24` is only a
  documentation constant there; check its users before adding lines to non-exempt commands (none
  planned).
- The agent bodies are short (about 12 lines after the frontmatter, 23 file lines for workers, 18
  for Chief roles) and are mostly a pointer to the card. The "whole contract in its prompt" is
  therefore the body plus the card the `Read` line names: say it in the card text.
- `tests/test_cli_runs.py::_worker_opening_lines` (l.63-76) pins the position of the opening lines
  and the three lines after the Verifier's heading: a generic contract must come only when
  configured, so these tests stay unchanged with no configuration.
- Windows/CRLF: the working tree is CRLF (`git ls-files --eol`: `i/lf w/crlf` for agent files and
  references). Reading through text mode is safe; any `read_bytes`/regex on `\n` is not. The agent
  files' `# chantier-agent:` line is matched by `AGENT_VERSION` with `re.M` on text, fine.
- The Chief roles' `chief_prompt_lines(started_by)` filter keeps only the roles a given parent
  starts; the generic block must follow the same filter.

## 5. `cost --explain`

- `commands/cost/command.py::_explain_notes(rows)` (l.95-105) takes only the rows; `cost()` (l.108)
  has `repo`, `batch`, `d` (so `d.host`). New: call `read_playbook(repo, d.host)` live (it is what
  "read now" means), keep `spec-writer` and `spec-critic` whose `start` is not `plugin` and which are
  not (`named` with no `agent`), print the two note forms. Add the lines inside `if args.explain:`
  (l.149-150); `list(dict.fromkeys(out))` keeps them unique.
- The cost code's named exception (AGENTS.md) already covers these two role names; the CR does not
  extend it.
- No grill-line change: `costs/sessions.py:70-83` (`without_specification_agents`, agent type ends
  with `spec-writer` or `spec-critic`) and `costs/transcripts.py::_grill_use` stay.
- Existing tests: the explain tests are in `tests/test_costs.py` / `test_cost_reading.py` with
  `cost_world.py`; the new case goes in `test_playbook_config.py` as the spec says (it needs a
  batch plus a cost world: see `cost_world.py`'s helpers; keep it to one parametrized case).
- Question: what a configuration that is invalid now should do in `--explain` (see Questions).

## 6. The Copilot Coder agent file

- `com.github.copilot/agents/chantier-coder.agent.md`, frontmatter line 5 `model-policy: required`.
  Delete that line only. The working copy is CRLF: use an exact one-line edit so the other
  lines keep their endings; `git diff` must show one removed line (the evidence line).
- Test: `tests/test_plugin_files.py:211`
  `assert copilot["model-policy"] == "required" and copilot["user-invocable"] == "false"` becomes
  `copilot.get("model-policy") == (None if role == "coder" else "required")` plus the unchanged
  `user-invocable` check. `_front` parser at the top of that file reads the frontmatter; a
  missing key is fine with `.get`.
- Bodies stay identical (the test just above compares `claude_body == copilot_body`): no body edit.
- Startup budget (limit 12288 bytes, `startup-manifest.json`): this file is a counted wrapper for
  `coder`/Copilot; the edit shrinks it. Measured here (run through the main checkout's venv, the
  worktree's has no pytest): coder copilot 9983, max role 10092 (conflict-resolver);
  **chief-of-staff copilot reload 12286 and claude 12280, router 12062-12068**: the chief of staff
  and router sit 2 to 8 bytes under the limit on reload. They count `skills/*/SKILL.md`, the core
  files and `session-start.md` "5. Reload": this CR must edit none of those (it does not).

## 7. Cards and host references

All in `skills/chantier/references/`; none is a counted startup section (concepts.md "Startup
core" is lines 3-11, hosts' "Startup core" lines 3-17; "Starting an agent" begins at
`concepts.md:392`; the host rows are under `## Tools`, copilot.md l.18+). Edits there do not change
`just test`'s startup measure. Reload counts only `session-start.md` and driver sections.

- `concepts.md` "Starting an agent" (l.392-417): add the `agent=(generic)` bullet after the model bullet
  (l.401-406); the existing bullet at l.412-414 ("a model the host cannot take at a start ... never
  retried") stays.
- `chief-of-staff.md` l.162-163: the sentence "A host that cannot set a model when it starts an
  agent refuses a `model` (its reference, row "Models"): say so and offer the user's own agent
  that names the model." is the one to replace (spec gives the four starts). The file is 1619 lines,
  not in the startup measure (not in `mandatory_sections`; `foreman` entry
  `prompt_builder` lists it but the test measures wrappers and sections only).
- `driver.md` l.62-68 and `foreman.md` l.166-169: "passed as printed (no model printed: none
  passed)" (driver) and "its agent and model are passed as printed, with no model when none is
  printed" (foreman): add the generic clause. Driver.md also has `## Startup core` at l.15 and
  `## Your means`, `## CR driver` readings counted in the reload: l.62-68 is in the driver text
  after l.15, check which heading holds it (it is under "Your means" if so: counted in reload ->
  byte budget; drivers' reload is 10347-10475, headroom about 1800, a one-line add is safe).
- `hosts/claude-code.md` row l.41 "Models at an agent's start": add the sentence.
- `hosts/copilot.md` (one table row per line, very long lines, CRLF): rows at l.25-28 (start rows),
  l.29 (Models), l.30 (capability row), l.31 (the model a role ran on); new row after l.30. The
  row names in the spec match the file ("Models at an agent's start (capability, start value)").
  Edit with exact-string replacements, not a rewrite.
- Eval kit names to keep consistent: `evals/copilot/RUNBOOK.md` "Models" is l.53-75; the
  `hosts/copilot.md` text points to it.

## 8. The Copilot eval's probe

- `evals/copilot/RUNBOOK.md` "Models" (l.53-75): add a step after step 2 (renumber 3 and 4 or add
  as 2b). `evals/README.md` and `evals/SCORECARD.md` are listed as project rules; check whether
  they mention the Copilot models run before editing (not read in full here).
- `evals/kit/copilot_models.py`: `main(argv)` parses `--session`; reads all `EVENTS`; prints each
  event; matches `ended` by order against `ROLES` (14). Add `--probe <identifier>`: after the same
  file read, take `ended[-1]` only, print `type` and the three `FIELDS` (`absent` when missing:
  the `data.get(f, 'absent')` idiom is already there), then the verdict line and return 0/1; with
  no ended event print `no ended subagent event` and return 1. Keep it standard library only, write
  nothing. The current `main` returns before any branch on `--probe`, so the probe must go before
  the `count_ok` block.
- Test: `tests/test_plugin_files.py::test_copilot_models_script_checks_each_role_on_a_fake_session`
  (l.247-287): the fake session builds one start+completed pair per role. Add two cases (parametrize
  with a mode) running `script.main(["--session", "s1", "--probe", <id>])` on the same fake file:
  last role's `model` equal -> exit 0, "ran the requested model"; different -> exit 1,
  "ran <model>, not the requested <identifier>". The existing assertion that every `subagent.`
  line carries "no agent field in the event" is for the non-probe path: keep it for that path only.
  The probe prints the same event lines? The spec says "prints its type and the three fields":
  one line of the form `subagent.completed: model=... firstDispatchedModel=...
  modelSelectionSource=...` (reuse `shown`), without the "no agent field" tail if the test's final
  `event_lines` assertion is to hold only for the non-probe mode.

## 9. Docs

- `docs/agents-and-models.md`: "Your own agents" (l.5-30 and "The file's keys" l.60-78): the
  sentence "A host that cannot set a model when it starts an agent refuses a `model`." is at
  l.74-75; add the four-starts table and the "caller's tools, not restricted" sentence; l.108-115
  "Models": the sentence about `model-policy: required` (l.110-115) is replaced; add the grill-line
  note. The page's links are checked by `test_skill_and_references_links_resolve`.
- Release notes: `docs/release-notes/<date>-v<ver>/` exist per version; the process
  (`docs/release-process.md`) makes them at a release, not per CR. Say in the PR it is the release
  CR's.
- No screenshot (no `hooks/register.tsx` or `STATUS.json` change): AGENTS.md's pane rule does not apply.

## 10. Tests, in one list (few, parametrized)

1. `test_plugin_files.py` l.211 (model-policy per role), l.247-287 (`--probe` cases).
2. `test_playbook_config.py`: l.246-262 (move the old refusal to generic; add agent+model refusal,
   Claude view valid, P12), l.93 (`start`), new parametrized "four starts on each host" test using
   `COPILOT_HEAD`/`HEAD` constants and `open_batch`, `take`, `record` helpers, plus the contract
   lines from `take`, plus `cost --explain` note case (needs the cost world).
3. `test_playbook_layers.py` l.154-159 (refusal wording), l.180 (`start` in the frozen record).
4. `test_copilot_catalog.py`: `start == id`.
Watch `just test` time: the suite must stay under 18.5 s + 30 s; these add a few CLI calls, no new
batches except the open for `take`/record cases (reuse one `open_batch` call).

## 11. Scenario

- `scenario/run_scenario.py` "## 20. A planning surface" starts at l.7073 (the next unit "## 21"
  at l.7480). The layered check is l.7109-7142 (claude only). `World.env` fixes
  `CHANTIER_HOST=claude` and removes `COPILOT_AGENT_SESSION_ID`
  (l.194-201); `w.chantier(..., env=...)` takes per-call env overrides (used at l.737, l.2709).
- Trap: the unit's first batch is opened on Claude (`w.start(item, "--direct", ...)` at l.7115),
  so its `take` prints Claude-host lines and `d.host` is `claude`: the Copilot `take` contract
  lines need a batch opened under `CHANTIER_HOST=copilot`. `--direct` on Copilot needs
  `COPILOT_AGENT_SESSION_ID` (`opening.py:277`, `own_transcript(host)`): pass
  `env={"CHANTIER_HOST": "copilot", "COPILOT_AGENT_SESSION_ID": "sess-c"}`. The natural place is
  the "other" project block (l.7143-7158), which opens its own batch: write a surface-project file
  with `hosts.copilot.roles.coder.model` set to another model (`gpt-6.1-terra`; the Coder's default
  is `gpt-6.1-sol`), `playbook` under copilot env prints `agent=(generic)`; add `agent: my-coder`,
  `open` exits 2 with the Q13 line and moves nothing (batch.json absent; the CR still in place);
  then remove `agent:` and open, `take` prints the Coder's contract lines. The first batch of the
  unit stays open, so the refusal check must use the "other" project, not the first.
- `playbook` and `open` refusals on Copilot must not need a Copilot session for `playbook`.
- Unit placement: the surface unit list is `UNITS` (l.~108, `"surface-board"`: needs `external_surface`
  tag); no new unit needed.
- `scenario/README.md` l.98-103 text update (see 3).

## Disagreements between the spec and the code as it is

1. Spec section 3's heading says `playbook/config.py`; the decision lives in
   `playbook/layers.py::_model_problems` (config.py only has the refusal text, `start_refusal`, and
   the per-role value parsing). `config.py` still gets the refusal text and the import rename.
2. Spec section 2 says the Copilot start value is built "where copilot-model-catalog builds it":
   it is `playbook/models.py:47`, an inline tuple comprehension with the empty start (no separate
   catalog module builds `Model`s; `copilot_catalog.py` only builds the JSON).
3. Spec section 4 says the contract goes "wherever the CLI prints a role's opening lines or first
   line". The code prints a first line only for roles whose description says "for the Chief of
   Staff" (spec-writer, spec-critic, retro-critic) and opening lines for the six workers
   (coder, conflict-resolver, debugger, inspector, investigator, verifier). The four Drivers, the
   Foreman's Driver starts, and the demo-explorer print neither (the Foreman builds a Driver's
   prompt from `concepts.md`'s template; `test_with_no_chantier_yaml_...` confirms the Demo
   explorer has no first line). A Driver or Demo explorer configured with a model on Copilot is
   `agent=(generic)` with no contract printed: see Questions.
4. `team_lines` has no host and no role list; it prints only configured roles. The spec's `team:`
   forms for `generic` need `start`; the contract lines need the host (agent file folder): `facts.py`
   passes `d.host` to `worker_prompt_lines` already, but `team_lines(d.playbook)` has no host
   argument (its text does not need one).
5. Spec section 5 says `_explain_notes` gets the configuration "for the batch's host"; today
   `_explain_notes(rows)` has neither a repo nor the batch: its signature and its one caller change.
6. Spec section 10 says tests are in `test_playbook_config.py`; the "model equal / with agent"
   Copilot tests are in `test_playbook_layers.py` (l.146-165) and the old refusal in
   `test_playbook_config.py` (l.255-262): both need the move. `test_playbook_layers.py:180` and
   `test_playbook_config.py:93` pin the frozen role record, which gains `start`.
7. The spec's section 11 says "§20 ... `take` prints the Coder's contract lines" under
   `CHANTIER_HOST=copilot`: the first batch in that unit is a Claude batch (see 11, trap).
8. `AGENTS.md` says the plugin's text "ten-line cap": the exempt list includes `take`, `round`,
   `handoff`, `playbook`, `cost`, `preflight`, so the new lines do not break it; no `concepts.md`
   edit is needed for that (the spec says the same).
9. Release notes: the spec says "as the project's release process asks"; release notes are made at
   release time (`docs/release-notes/` per version), nothing for this CR to write.

## Questions only the user can answer

1. A Driver, a stack/release/QA driver, the Foreman or the Demo explorer configured with another
   model on Copilot becomes `generic`, but no CLI line prints a contract for them. Options: accept
   (the parent builds the prompt from the concepts template as for any Driver, and the "contract"
   is the card the `Read` line names; the agent file's body adds only the refusal), or print the
   body for them too through another command. Smallest change: print it only where the CLI already
   prints opening/first lines, and say in `concepts.md` that a generic Driver's prompt is the
   template as today. Needs a yes.
2. `cost --explain` when the configuration read now is invalid: the spec says nothing. Options: no
   grill note and no failure (smallest), a refusal like `price_table`, or one line "not read".
   Recommended: no note, no failure (the explain is a read-only aside; P12 and `playbook` already
   report an invalid file), unless the user prefers a refusal.
3. The exact form of the `tools=(the caller's, not restricted)` word when the same role also has a
   `tools:` need: print both (`tools=jira tools=(...)` would be confusing). Proposal: put the
   generic marker right after `agent=(generic)` and before `skills=`/`tools=`; no other change.
   This is wording only; the Driver may decide.

## Risks

- Startup budget: no edited file is a counted section except Copilot's coder agent file (shrinks) and
  possibly a `driver.md` line under "Your means" (a reload section: about 1800 bytes of headroom for
  drivers). Chief of staff and router reloads are 2 to 8 bytes below 12288: touch none of
  `skills/*/SKILL.md`, `session-start.md`, `startup-core.md`, `role-core.md`, `host-core-*.md`.
  Run `test_startup_manifest.py` after every reference edit.
- Identical bodies: only frontmatter of the one Copilot file changes; `agents/` untouched.
- `KeyError` in `layers._labels` if `start` is put in `rec` before it runs (see 3).
- CRLF: the working tree is CRLF, the index LF. Use exact one-line edits; do not rewrite long
  Markdown tables with a whole-file write. Every file UTF-8 without a BOM
  (`test_no_tracked_file_starts_with_a_utf8_byte_order_mark`).
- Windows: paths printed in the refusal come from `Node.src` (`display()` makes posix paths), so
  tests can assert `chantier.yaml:5:` as today.
- A legacy batch record has roles with `model` but no `start`: printing must not require it.
- `just test` budget (18.5 s + 30 s): reuse one `open_batch` per test.
- The rename leaves no alias: no fallback rule in AGENTS.md; do not keep the old name.

## Evidence plan

Kind of change: CLI behaviour (printed lines, refusals, a recorded field), one agent-file line,
Markdown references and docs, an eval script flag, tests and a scenario block. No UI: no screenshot.

Before and after (commands in the worktree, run with the `uv run --no-sync --project` CLI line from
the prompt, `--host` flags, a throwaway `chantier.yaml` in a temp project or the project's surface
file as the spec's Evidence section says; each output pasted in `evidence/`):

1. `playbook --host copilot` with `hosts.copilot.roles.coder.model: gpt-6.1-terra`: before the change
   exit 2 with "cannot set a model when it starts an agent"; after, the `agent=(generic) ...
   tools=(the caller's, not restricted)` line. Same file with `--host claude`: the plugin's line
   unchanged. With `agent: my-coder` added, `--host copilot`: the Q13 refusal at the model's
   line, exit 2; `--host claude` valid. Technique: command output captured to
   `evidence/playbook-<case>.txt`.
2. `take` on a batch opened under `CHANTIER_HOST=copilot` with the generic Coder: `team:` line and
   the contract lines (scenario block; a pytest run for the same). Technique: the scenario log
   `work/gates/*.log` and the test's output.
3. `open` records `start`: `batch.json`'s `playbook.roles.coder.start`, a `jq`-free Python one-liner
   on the file.
4. `git diff -- com.github.copilot/agents/` shows one removed line; `git diff --stat -- agents/`
   empty.
5. `evals/kit/copilot_models.py --probe gpt-6.1-terra` on the test's fake session (equal: exit 0;
   different: exit 1), outputs pasted. Technique: a short script outside the repo (scratchpad) that
   writes the same fake `events.jsonl` as the test and runs the script with `COPILOT_HOME` set.
6. `cost --explain` grill note: output of a batch with `spec-writer` set to `agent: mine` and with
   the plugin's agent plus another model (no note), from the test's cost world.
7. `just check` (Linux/macOS/Windows by the pipeline; Windows locally), `just test` time against the
   18.5 s + 30 s budget, `test_startup_manifest.py` bytes before (above) and after, and `just
   scenario` (local Windows run when on top of the stack, the pipeline's job otherwise). `just mod`
   not needed (no `hooks/` or `types/` change).

Cannot be shown: a real Copilot session (the probe and the generic start are the user's later run);
the PR's Known gaps name the three the spec lists ("a named Copilot agent started with a requested
model not yet observed ...", "a generic start on its configured model not yet observed in a real
Copilot session", "the exact `agent_type` of Copilot's generic agent"). The host's row text
about `agent_type: general-purpose` is unproved.
