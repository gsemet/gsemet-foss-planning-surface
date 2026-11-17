# Investigation: CR-320 timing and retry settings (before round 1)

Read only. Worktree `C:\Users\gaeta\Projets\chantier.worktrees\batch-23-CR-320`. Paths below are
under `skills/chantier/scripts/cli/src/chantier/` (`cli/`) unless stated. Project rules read
(`rules`): AGENTS.md (tests few/parametrized, `just check`, long gate = `just scenario`, no
screenshot rule applies only to the CR pane, which this CR does not touch), CONTRIBUTING.md,
scenario/README.md.

## Files and entry points, per area

### Area 1: `playbook/config.py`, `playbook/layers.py`
- `config._host` (l.139) rejects any key but `roles`: becomes `roles, timing`. `_hosts` (l.121)
  also says "holds its keys: `roles:`" (message only). `check` runs per layer on the raw `Node`
  tree (no merge): the right place for `_timing(host, node, kline, bad)`. `Node` has `.kind`,
  `.value` (map: key -> (line, Node)), `.plain`, `is_reset`; scalars are strings, so a duration
  is parsed with a regex `^([0-9]+)(s|m|h)$`, `ci_reruns` with `^[0-9]+$` (rejects negative and
  fractional). `HOST_FILES` (l.29) is where `TIMING_COLUMNS`/`TIMING_READS` go.
- `typed()` (l.87) only handles `roles` under `hosts`; timing needs no change there (it must
  NOT go through `merge`, see below).
- `layers.read_defaults` -> `_checked` -> `config.check`: the defaults already go through
  `check`, so extending `_host` covers "the defaults go through the same check" for free. Note the
  shipped Claude `steering_wake: 30m` is a general value; `session: cache_ttl: 1h` is a column
  override.
- `layers.merge` merges node by node, weaker to stronger, and a column key present in a stronger
  layer would beat a general value of a weaker one: that is the OPPOSITE of timing-Q13. So
  `load_timing` must read `Layer.tree` per layer (strongest first), not `Merged`. A reset
  (`is_reset`) in a layer at a column key or general key = skip that layer's value and go on to
  weaker layers (and the defaults). Layer order: `read_user` returns weakest first; labels
  `surface`, `surface project`, `repository`; defaults label `defaults` (`LABELS` in edit.py).
- Existing `load` returns `(None, [])` with no user file; `load_timing(repo, roles_by_host,
  defaults)` must instead always answer (defaults alone) and carry `(timing, problems)`.
  `roles_by_host` is only passed through to `config.check`.

### Area 2: record and prints
- `core/records.py` l.190: `BatchRecord.playbook: dict | None`; add `timing: dict | None = None`
  (pydantic-style model: check how unknown/extra fields are handled so old records still load).
- `commands/opening.py` `open_batch` (l.266): `read_playbook` is called before folders move; add
  `load_timing` there too, raise on problems (same as the playbook problems), set `data.timing`.
  `_brief_text` (l.225) gets the `- Timing:` line. Careful: `team` is None with no user file, but
  timing must be recorded anyway.
- `playbook/lines.py`: add `timing_lines(timing, host)` and the warning builder; model it on
  `team_lines`/`ci_lines`/`_labelled`. Column display names: "Claude Code session/subagent",
  "Copilot claude/gpt/other models" (the `other models` row = general values, Copilot only).
  `plugin_files.read_playbook` (l.247) is the existing wrapper for defaults path + roles_by_host;
  add a sibling `read_timing(repo, host)` there.
- Print sites: `commands/rules.py` `playbook` (both branches; note the no-batch branch returns
  early on problems, and with no user file prints "no chantier.yaml..." head: timing lines must
  still print, warnings included; the `--batch` branch reads `d.timing`, falling back to shipped
  defaults of the running plugin when None); `commands/facts.py` `cr_facts` (l.109, after
  `ci_lines`) covers `take`/`round`/`handoff`; `commands/driver.py` l.84 and l.140 use
  `team_lines(d.playbook)` (the `take stack`/`take` prompt blocks via `driver_prompt.py`): add
  `timing_lines` there. HEAD commit 5c36b06 ("take, take stack and order qa print the Driver's
  whole prompt skeleton") reshaped these: check `driver_prompt.py` for where lines are placed and
  whether it needs a `timing` field next to `team`.
- Resolver reading a record with no timing: one helper `recorded_timing(d)` (defaults of the
  running plugin) used by playbook, state.py and facts.

### Area 3: cards (all in `skills/chantier/references/`)
Grep (old wording still present, line numbers current, spec numbers have drifted):
- `hosts/claude-code.md` l.62 ("30 minutes (1800 seconds)"), l.66 ("has run since the last wake");
  Tools table: two new rows.
- `hosts/copilot.md` l.54-62 (`/every 4m` at l.55-56, idle stop "every Driver has ended for 30
  minutes" l.58); tools table: two new rows.
- `foreman.md` l.615 ("every 30 minutes") and l.620 (idle stop wording).
- `chief-of-staff.md`: l.1248 ("because every Driver has ended for 30 minutes", the Copilot
  arming text), routing table row near the `hosts.<host>.roles`/`ci: beside_gate` rows, plan "Team"
  line quoting `timing:` lines.
- `driver.md` l.265 (remote command paragraph), l.384 (CI bullet), l.922 (heavy CI), l.1034
  (Release driver; stays); the beside-the-gate "one re-run, or a note" outcome was not found by
  my grep: search "one re-run" again when editing (grep found only the four hits).
- `concepts.md` l.555 (the spec says l.530: moved; "`infra:` after its one re-run"), and the
  "Starting an agent" list of what the CLI prints.
- Agent files untouched. Card tests (`tests/test_startup_manifest.py`, structure tests) may check
  card line counts or a startup manifest: run `just test` after editing.

### Area 4: `playbook/edit.py`, `board/config_api.py`, `board/state.py`
- `edit._view` (l.215) builds `hosts`, `others`, `files`...: add `"timing"`, built from
  `layers.load_timing`. `_flat` (l.195) drops role `agent`/`model` leaves with
  `path[:1] == ("hosts",) and path[-1] in KEYS`; add `path[2:3] == ("timing",)` to leave timing
  out. `config_view` (l.248) reads defaults and user layers already; reuse them (no re-read).
  `_defaults_path`/`_roles_by_host` helpers exist.
- `board/config_api.py` only routes to `edit`: probably no code change (GET returns the view as
  is); check it forwards the whole dict.
- `board/state.py` `_batch` (l.85): add `"steering_wake_min"`. Claude: `session` column's
  `steering_wake`; Copilot: the max over columns and the general value (the settled open
  question). It is not in `VIEW_KEYS`/`status/views.py` (the pane is untouched, so no pane
  screenshot is owed).
- No write route change (`_one` keys stay `agent`/`model`).

### Area 5: board web (`board/web/`)
- `js/views/config.js` (237 lines; `mount(root, state)` l.218, `render(state)`, `load(root,
  state.project)`), `css/views/config.css` (68 lines), `js/model/semantics.js`
  (`HEARTBEAT_LATE_MIN = 15` l.18, `heartbeat(batch, nowIso)` l.217-224, used by
  `views/home-batch.js` l.30), `js/i18n/en.js`, `fr.js` (+ `en-board.js`/`fr-board.js`: choose
  where the Timing strings go; the existing config strings tell).
- Tab state: how the router keeps view state (fragment) must be read in `main.js`/`ui/` when
  coding (not read yet).
- Reference look: `...319-board-visual-refresh/prototypes/01-mockups/final-config.html` (exists).
  There is no JS unit test harness found for the board JS (no `*.test.js` seen); `just lint` runs
  Biome on the web frame.

### Area 6: docs
`docs/agents-and-models.md` ("The file's keys", "The layers"), `docs/hosts.md` l.9-10 (heartbeat
table: "30 minutes", "4 minutes (`/every`)"), `docs/use-cases-foreman.md` l.178, also
`docs/use-cases-direct.md` l.121 mentions `/every` (no number, fine). `config/chantier.defaults.yml`
header comment and the new `timing:` blocks.

## Smallest change that meets the spec
1. `config.py`: constants `TIMING_SETTINGS`, `TIMING_COLUMNS`, `TIMING_READS`, a duration parser,
   `_timing`; `_host` accepts `timing`.
2. `layers.load_timing` (per-layer, strongest first; column > general inside a layer; reset =
   skip) returning `{host: {column: {setting: {value_seconds|text, layer, src} | None}}}` plus the
   general value; defaults file gets the `timing:` blocks.
3. `lines.timing_lines` + `timing_warnings`; one `plugin_files.read_timing`; hook into
   `rules.playbook`, `facts.cr_facts`, `driver.py` team blocks, `open` (record + brief).
4. `BatchRecord.timing`; `edit.config_view` `timing`; `_flat` filter; `state._batch`
   `steering_wake_min`.
5. `config.js`/`config.css`/`semantics.js`/i18n; cards; docs; tests; scenario step.

## Risks
- Merge semantics trap (above): do not reuse `layers.merge` for timing; Q13 differs.
- `playbook`/`open` with no user file: `read_playbook` returns `(None, [])`; timing must still be
  recorded and printed (new code path, unlike every other key).
- Concurrent CR-319 (board visual refresh) restyles `config.js`/`config.css`: same files, no
  `depends.json`; whichever lands second rebases. Keep Timing in new functions/new CSS block to
  lower conflict.
- Value change `HEARTBEAT_LATE_MIN` 15 -> steering wake + 5: Claude default late mark goes from
  15 to 35 min. Search for the old value `15` found only `semantics.js` l.18 and its single use;
  `evals/results/claims-v0.10.0.md` mentions heartbeat (historic, leave). The card text
  "heartbeat late" in docs/cards: grep when coding (`late` in docs/boards.md).
- Spec drift: line numbers in the spec (concepts l.530, chief-of-staff l.1239, driver "one
  re-run, or a note") are stale; the card edits are located by text, not number. HEAD
  `5c36b06` changed the take/Driver prompt: re-read `driver_prompt.py` and `driver.py` before
  placing `timing_lines`.
- `tests` budget: `just test` at most +30 s; the new tests are parametrized and in-process.
- `BatchRecord` strictness: a record with `timing` read by an older plugin; and an old record
  without it must read as defaults (nothing migrated). Check the model's `extra` setting.
- Copilot family from a model id: "first word of the identifier" (`claude-sonnet-5.5` ->
  `claude`; `gpt-6.1-sol` -> `gpt`); state.py takes the max, so the CLI side needs no family
  logic except the Driver card wording.
- Defaults-vs-agent-files test reads roles only (spec says leave it): confirm
  `test_playbook_layers.py::test_the_shipped_defaults...` ignores `timing` (it uses `config.check`
  over the tree: it will now also check timing, which is fine).

## Questions only the user can answer
None. (Spec's Open questions are settled.)

## Evidence plan
Kind: CLI behaviour + board UI + cards/docs text + tests.
- Tests: `just test` and `just check` output (log in `work/gates/`); new parametrized tests in
  `tests/test_playbook_config.py`, `tests/test_playbook_layers.py` (and `test_board_config.py`
  for `config_view`/`GET /config`, state `steering_wake_min`), calling the CLI in-process.
- CLI before/after: `$CHANTIER playbook` printed with no file (before: no `timing:` lines; after:
  the shipped lines), and with a project file setting `session: steering_wake: 20m` (`[surface
  project]` labels), plus a refused file (`driver_wake`, `steering_wake` under `subagent`)
  showing the file:line text. Captured as command output in `evidence/`.
- Scenario (`just scenario`): the new step spec'd in 03-change-spec (set, open, brief.md line,
  `playbook --batch`, `take`, change file, running batch keeps old values). Add to
  `scenario/run_scenario.py` near `surface_config_page` (l.7344) / the layered-config block
  (l.7433); `tests/test_scenario_coverage.py` may require the claim to be listed. Windows
  coverage: the stack-top CR passes `just scenario` locally.
- Board: start `chantier board` on the scenario/demo state (`docs/demo/` and
  `scripts/docs_screenshots.py` exist: the project's capture tooling, `just docs-screenshots`
  uses it, by hand), screenshot the Timing tab at 1680 px beside `final-config.html` rendered at
  the same width, with a "not used" cell and a teal set value; heartbeat mark at 20 min (not
  late) and 36 min (late) on a Claude Code batch with the default wake (state fixtures or two
  `now` values). Screenshot via the project's docs-screenshots/Playwright path, by browser.
- Cards: the grep list of Evidence (no "1800 seconds", "every 30 minutes" in heartbeat,
  `/every 4m`, "one re-run" for CI, "after its one re-run", "has run since the last wake",
  `driver_wake`) run before/after as a log.
- Cannot be shown: a real Foreman scheduling a non-30 minute `ScheduleWakeup`, a real `/every` at
  a configured value, the idle stop with a short wake, and the cache TTL values (all "unproved
  until a real batch" in the spec; shown only as card rows with trials). No pane screenshot is
  owed (the pane and `STATUS.json` are untouched).
