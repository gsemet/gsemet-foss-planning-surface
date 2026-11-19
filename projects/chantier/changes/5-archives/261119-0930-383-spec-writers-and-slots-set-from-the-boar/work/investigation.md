# Investigation: CR-383 spec-writers and slots set from the board's configuration

Read only; worktree `batch-28-CR-383` at `020fd864`. Paths relative to
`skills/chantier/scripts/cli/src/chantier/` (`SRC`) unless they start at the repository root.
Project rules read: AGENTS.md (the CLI names no role; the board edits only the surface project's
file; `just check`, `just eval-dry-run`, `just scenario`; DESIGN.md of `board/web/` kept true;
tests few, parametrized, fast). The shipped defaults are `config/chantier.defaults.yml` (repo
root `config/`), not under `SRC`.

## Map: files and entry points

| Area | File (entry) | What it does today | Change |
|---|---|---|---|
| Checks | `playbook/config.py`: `check`, `_KEYED`, `_long_gate` (model for the new checks), unknown-key text in `check` | top-level keys `hosts prices board ci long_gate` | add `_specifying`, `_batch_key` to `_KEYED`; extend unknown-key text; sub-key check like `_long_gate` (slots 0 allowed, parallel >= 1) |
| Layers | `playbook/layers.py`: `read_defaults`, `read_user`, `read_key`, `merge`, `load` | each layer checked alone; `read_key(repo, key)` reads one merged user key | new reader (see below); `read_defaults` is where a missing shipped key is reported |
| Resolution model | `playbook/timing.py`: `_search`, `timing_from`, `load_timing` | user layers strongest first then defaults, `{value, layer, src}` | new `playbook/limits.py` copying that shape (flat paths, simpler than timing) |
| Plugin | `plugin_files.py`: `read_timing` (l.294), `plugin_root`, `recorded_timing` | defaults path `root/config/chantier.defaults.yml`; None without plugin | add `read_limits(repo)` beside it |
| open | `declare/opening.py` (`--slots default=4`), `commands/opening.py` (`open_batch`, `_read_configuration`, `_empty_lines`, first line), `commands/opening_record.py` (`open_settings` refuses `slots < 1` text "slots and budget must be positive", `new_record` uses `args.slots`) | `args.slots` is read in: `open_settings`, `new_record`, `_brief_text`, `_empty_lines`, the first `opened ...` line | `--slots` default None; resolve once at the top of `open_batch` (after `_read_configuration`, before `open_settings`), set `args.slots`, keep the layer for the label; refuse configured 0 before `open_settings`'s generic text |
| playbook | `commands/rules.py::playbook` (lines assembled after `timing_lines`/`timing_warnings`), `playbook/lines.py` (`timing_lines`, bracket-label style `[layer]`) | no `limits:` line | add `limits_line(limits, markers)` in `lines.py`; counting of `work/specifying` markers in `1-inbox`, `2-backlog/P1..P4`, `3-ready` (new small helper; `status/views.py:236` already tests `work/specifying`, `board/backlog.py` the same state: reuse stage paths from `lifecycle/stages.stage_layout`) |
| playbook with `--batch` | same function, `args.batch` branch reads the record | `limits:` is live config, never frozen: print it in both branches (decide: yes, from live files) |
| Board view/edit | `playbook/edit.py`: `config_view`, `_view`, `_flat` (the read-only "others" list), `_shape`/`_one` (role-change shape), `edit_surface_file`, `_candidate` | role changes only `{host, role, key, value}` | `limits` block in `_view`; second shape `{key, value:int|null}`; `_flat` must drop `specifying.*`/`batch.*` leaves (the Limits tab owns them); `_candidate` already re-reads text through `layers.read_text` so the check text comes from `config.py` |
| Text edit | `playbook/edit_text.py`: `_walk/_set/_remove` hard-code `hosts.<host>.roles.<role>` | role only | generalise to a path list; removal prunes emptied parents (keep the `specifying`/`batch` map removal) |
| Board route | `board/config_api.py::_put`, `board/journal.py::record` (board journal `config` kind, stays) | one board-journal line, `APPLIES` text | before/after effective values of the two keys (`read_limits` before the write, `config_view` after), append `config` lines through `hub/journal.append(..., by="board")`, role-free response lines |
| Forge journal | `hub/journal.py`: `_key` (falls through to the `merged` key: a `config` line would dedup wrongly, must get its own branch with `t`), `event_text` (falls to `merged_text`), `lines(entries, batch, open_crs)` | merged and checks-red only | `config` kind, `_key`, `event_text`, `lines` gets the batch's orders (signature change; one caller) |
| Watcher | `hub/watch.py::Watch.poll` reads every `seq` above the cursor, any kind; `lines()` prints `event_text` | works for `config` as is | no code change, only a test; see risk R2 |
| status | `commands/batch_status.py::_seen_lines` (l.235) | merged lines | pass `d.orders` and `d.status`; print the one `batch.slots` line |
| Orders | `commands/orders_apply.py::_slots`; `OrderRecord.sent=now()` (`commands/orders.py` l.184), `BatchRecord.orders` never pruned (grep) | `order slots` unchanged | the "acted on" test is: an order of kind `slots` with `sent` after the line's `t` |
| Web | `board/web/js/views/config.js` (tabs via `config-timing.js`: `TABS`, `HASH`, `tabOf`, `tabAddress`, `local.tab`; `judge/save/change/mount`), `api/config.js` (`changeConfig` already sends any `changes`), `i18n/en-board.js`+`fr-board.js` (`config.*` keys) | two tabs | third tab `limits` in a new `config-limits.js` (config.js is 268 lines; keep it small), `TABS`/`HASH`/`tabOf` extended, `config.tab_limits`, `config.limits.*` keys en+fr |
| DESIGN.md | `board/web/DESIGN.md` has no tab note (grep: none) | n/a | spec says add a note only if the file names the page's tabs: it does not; read it anyway, add nothing unless the new inputs need a token not in the table. `tests/test_board_design.py` checks CSS vs tokens: new styles must use tokens |

## Smallest change

1. Defaults file + `config.py` checks (+ presence guard).
2. `playbook/limits.py` (resolve a flat dotted key per layer, strongest first, defaults last, no
   plugin: user layers only, `None` when unset) and `plugin_files.read_limits`.
3. `open`: resolve slots, label, refusals.
4. `playbook`: `limits:` line, markers count.
5. Board: `edit.py` (+ `edit_text.py`, `config_api.py`), then JS tab and i18n.
6. `hub/journal.py` `config` kind, `status` line.
7. Cards and docs listed in the specification (AGENTS.md, CONTRIBUTING.md mirror,
   docs/web-board.md, scenario/README.md, chief-of-staff.md, griller.md, foreman.md,
   concepts.md, session-start.md, hosts/claude-code.md and the Copilot host file, `agents/` and
   `com.github.copilot/agents/` only if a role body changes: none expected).

## Risks and findings

- R1 Missing shipped key. `read_defaults` -> `_checked` -> `config.check` only checks present
  keys, so "defaults file without one of the two keys" is detected nowhere today. The guard
  belongs in `read_limits` (or in `read_defaults` through a defaults-only check), and `open` /
  `playbook` must put its problem in the same list `_read_configuration` raises
  (`EXIT_PRECONDITION`). Specification names it a defaults-file problem; an extra check
  function in `layers` that only the defaults layer runs is the smallest form. The config tests
  use the real plugin root: the "lacking one key" test needs `CHANTIER_PLUGIN_ROOT` pointed at
  a prepared copy.
- R2 Paused batch and the watcher. `hub/cycle.running_batch` returns None for a paused batch, so
  `chantier watch` refuses to start with none and `Watch.poll` ends `no-batch`. The decision-7
  case "slots changed while a batch is paused" therefore has no watcher: only `status` (which
  prints for running or paused, `d.status` any) wakes it. Not a code change; the cards must not
  promise a watcher wake for a paused batch. Surface to the Driver as a card sentence and a
  Known gap line. `poll` also puts the `config` events in `self.events` before it tests
  `running_batch`, so a save at the moment the batch pauses still prints.
- R3 `_key` dedup in `hub/journal.py`: today any non-`checks-red` line is keyed as `merged`
  (`batch`, `cr`, `bool(landed_with)`), so two `config` lines (cr None) would be swallowed as
  duplicates. The own-key branch is mandatory, and `t` is in it, so two saves in the same
  second with the same values collapse (the test must not save twice inside one `clock.now()`
  resolution; check `core/clock.now` granularity).
- R4 `_flat` in `playbook/edit.py` ("others" list) would list `specifying.parallel` /
  `batch.slots` read-only next to the editable tab. Drop them there.
- R5 `typed()`/`layers.load` return every `_KEYED` key into the playbook dict that `open` freezes
  in the record (`data.playbook = {k: v ... if k not in ("prices","price_layers")}`). Adding
  the two keys to `_KEYED` would freeze `specifying`/`batch` in the record, contradicting
  "a running batch keeps recorded slots until order slots" only superficially (nothing reads
  them) but it pollutes `batch.json`. Prefer a separate tuple in `config.py` of "checked but not
  typed" keys, or filter in `open`. To confirm in round 1.
- R6 `args.slots` is read in four places in `commands/opening.py`/`opening_record.py` plus
  `_empty_lines` (CR-369's no-CR form already merged at this head): set it once on `args`
  before `open_settings`. The generic "slots and budget must be positive" check then still
  covers an explicit `--slots 0` only if the refusal for a configured 0 runs before it and the
  explicit 0 is distinguished (`args.slots is None` before resolving).
- R7 Value derived from the old default 4: grep `4` for slots: `declare/opening.py` default,
  `references/chief-of-staff.md:734` ("4 unless you say"), `init.md:60` ("slots (4 by default)"),
  `concepts.md` Slots paragraph (~l.300), docs/README mentions (grep `slots` in `docs/`,
  `README.md`, `skills/chantier/references/*.md`) and `tests/` that open with no `--slots` and
  expect 4 (`batch_helpers.open_batch`, `test_open_empty_batch.py`, `test_opening_and_restore.py`,
  scenario `open` calls): all stay 4 through the shipped default, but their text must say
  "`batch.slots`, 4 shipped". The `wrote` order text `slots 4 -> 6` in board lines is new.
- R8 Unreleased dependencies in the stack: the specification says it stacks after CR-375 (end
  lines in `watch.py`), CR-370, CR-369 (CR-369 is in this head: `f0f8d4b7`). `_empty_lines`
  and `status`'s last lines may move under CR-375; merge conflicts in the cards, not code logic.
- R9 Windows: `edit_text` writes LF and keeps a BOM (existing behaviour); new text edit tests
  must keep both. Layer display paths use `layers.display` (posix) for the open label.
- R10 `config_view` `_view` signature now returns a `limits` block; `config.js` reads
  `view.limits`; the JS has no unit test harness beyond `just check` (biome lint); an unused
  or mistyped i18n key shows only in the board: en/fr parity is likely checked by a test (look
  for it in round 1: `test_board_description.py`/i18n tests) and by `just check`.

## Questions only the user can answer

None blocking. Two small notes for the Driver to decide: (a) `limits:` in `playbook --batch`
prints live values (they are not frozen with the batch): chosen, say so in the card; (b) R2's
paused-batch gap goes to Known gaps unless the user wants `watch` to run on a paused batch (out
of scope here).

## Evidence plan

Kind of change: CLI behaviour (open, playbook, status, watch), board API and web page, journal
line, docs and cards. Project rules ask for tests in-process (few, parametrized, `just test`
budget), the scenario's surface-board unit, and for a web view change the board's real page.

Tests (SRC tests live in `skills/chantier/scripts/cli/tests/`):

1. `test_playbook_config.py` (or a new `test_limits_config.py`): parametrized check cases over both
   keys (accepted, 0 for slots ok / parallel refused, negative, text, float, unknown sub-key,
   unknown-key message lists the two keys). Shows the exact refusal text.
2. `test_playbook_timing.py`-style resolution test in a new `test_limits.py`: the shipped
   `config/chantier.defaults.yml` read from the repo (never copied) has both keys and passes the
   checks; a prepared defaults file lacking a key gives the defaults-file problem on `playbook`;
   resolution per layer (shipped, surface project, repository) and with no plugin root.
3. `open` matrix, through `chantier.open` in-process (use `batch_helpers.open_batch`,
   `Surface` fixture): rows 1-6 and the factory cell of the specification's matrix: shipped
   (no label, equals the value read from the defaults file), surface project `[surface project]`,
   repository `[repository]`, `--slots 3` wins and no label, configured 0 refused exit 2 naming
   file and key, `CHANTIER_PLUGIN_ROOT=""` refused exit 2. Shows `open`'s first line, the
   output proof.
4. `playbook` `limits:` line with real `work/specifying` markers (create the files in prepared
   backlog folders), `at the limit`, `not set` with no plugin root, each source label.
5. `test_board_config.py` (existing `_board`/`_on_surface` helpers): PUT per key (file keeps
   comments, `null` removes, 409 stale, dry-run writes no file and no journal line, one `config`
   line per changed key with old/new/batch, two keys plus one role -> two lines, unchanged
   value -> none, bad value refused with `config.py`'s text, role-free response lines with a
   batch running, paused and none, no surface read-only). Reads the `forge-journal.jsonl`
   file produced by the real route.
6. `test_forge_hub.py`: `event_text` per form, `_key` dedup (two saves = two lines), watcher
   ends `events` on a `config` line with the existing `Watch.poll` test driver (no sleep), a
   paused batch ends `no-batch` with the line printed first.
7. `status` lines (in `test_forge_hub.py` or `test_surface_batches.py`): `batch.slots` line shows
   until an `order slots --note <n>` is recorded, a newer line replaces an older, no
   `specifying.parallel` line, a closed-batch / `batch: null` line is not printed.
   Each driven by the real board route + the real `order` command, never a hand-written record.
8. A `test_scenario_coverage.py` entry is checked by the README bullets (below).

Scenario (`scenario/run_scenario.py`, unit `surface-board`, 300 s budget: check the
measured 236 s before adding; the three legs are small): add to `forge_hub` (it already has
`watcher()`, the quick env `CHANTIER_HUB_TEST_TIMES`, a real board and a real surface) or to
`external_surface` next to `surface_config_page` (which already drives the real board's
`PUT /config` against a surface with a batch open):
- Leg 1: `PUT /config` `batch.slots` 6, a running watcher ends with `config changed on the
  board` line, `status` prints it, `order slots --note 6`, `status` no longer prints it.
- Leg 2: `PUT /config` `specifying.parallel` 1 with a `work/specifying` marker: watcher line,
  `playbook` `markers 1 (<slug>) ... at the limit`, `status` prints no line for it.
- Leg 3: `open` with no `--slots` after the save: configured slots with `[surface project]`.
Update `scenario/README.md` Coverage bullets with `(unit: surface-board)` and the test names so
`test_scenario_coverage.py` passes.

Host/default matrix (each cell by a real CLI flow): the cells map to tests 3-5 and legs 1-3:
- `batch.slots` shipped / surface project / repository / `--slots 3` / configured 0 / no plugin
  root: test 3 (`open`) + test 4 (`playbook`) + test 5 (board view `overridden`).
- `specifying.parallel` shipped / surface / repository / no plugin root: tests 2, 4, 5.
- either, shipped file lacks the key: test 2 (`playbook` and `open` stop), board view shows the
  problem (`problems` in `config_view`, asserted in test 5).
- either, no planning surface: test 5 read-only (also the Limits tab shows read-only).
- Host column: the two keys are host-independent; tests 3-4 run once with a Claude Code host and
  once with `CHANTIER_HOST=copilot` (parametrize, no new fixture) to prove the value is the
  same on both.

Screenshot / real page: the Limits tab is a web view change, not a CR board pane change, so no
pane screenshot is owed. Show the tab once from the scenario's real board (or `just
docs-screenshots` path) is optional; at minimum biome (`just check`) and the JS served by the
scenario board. A screenshot of the Limits tab from a real board on this head is cheap and I
propose it as evidence (`evidence/limits-tab.png`) if the Driver can open the board; the
rules do not ask for it.

Cannot be shown: that an idle Claude Code session wakes on the watcher's end after a board
save (decision 11): the scenario proves the watcher ends with the line only; Known gaps names
it. The wake on a paused batch is not even reachable (R2).

Gates: `just check`, `just eval-dry-run` (change under `src/`) in the worktree before the first
push; `just scenario` green at the PR head (CI) and locally on Windows if this CR is on top of
the stack. No `hooks/` or `types/` change: `just mod` not owed.
