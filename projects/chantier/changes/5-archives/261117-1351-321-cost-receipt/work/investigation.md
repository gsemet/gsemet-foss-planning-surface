# CR-321 investigation (Investigator)

Base check: the worktree (HEAD 9bb941f, the CR-319 branch) has in `board/web/css/tokens.css`: `--accent` #1d5c63, `--accent-dark`, `--accent-mid`, `--accent-light`, `--accent-tint`, `--accent-tint-2`, and "Inter" first in the font stack (l.118). The dependency is met.

Paths below are under `skills/chantier/scripts/cli/` (`src/chantier/...`, `tests/...`) unless from the repo root.

## Files and entry points

Data (CLI):
- `commands/cost/breakdown.py`: `cost_summary` (l.211) builds the text from `_split` (l.268), `_wakes` (l.257), `_driver_line` (l.249); `breakdown(rows)` gives entries by kind (Foreman/Driver/Worker/Agent); `apportion`; `cost_groups(repo,batch,rows,"driver")`. The new receipt function goes beside `cost_summary`; `_split`/`_wakes`/`_driver_line` are rebuilt from its data (text byte-identical).
- `commands/cost/sessions.py`: `_Chief` dataclass (steer, grill, whole, inside...), `_absorb`, `_chief_lines`, `chief_line` (l.183), `_chief_unknown(cause)`, constants `STEER_OUT`/`GRILL_OUT`. `chief_line` returns strings only: split out a structured reading used by both `chief_line` and the receipt's `outside` (grill = `c.grill`; steering = `c.steer`, null in a direct batch: `_chief_lines` already skips the steering line when `steer` has no calls and `inside_calls` is set; mirror that rule).
- Callers of `cost_summary`/`chief_line`: `commands/closing.py` (l.60, l.130), `commands/batch_status.py` (l.94), `commands/cost/command.py` (l.150-153).
- `commands/close_archive.py`: `_close_files` (l.116) calls `history.close_record(record, closed, total, unpriced, by_cr)`; `Closing.rows` holds the priced rows. Add `cost_receipt` here; the Chief reading should be done once in `closing.py` (where `chief_line` runs at l.130) and carried on `Closing` (fields l.36-48), not priced twice.
- `history.py` `close_record` (l.52): new `cost_receipt` key. `core/batch_records.py` `blank_record` (l.61): `"cost_receipt": None` (`open_record` inherits). SCHEMA stays 1.
- `board/costs.py`: `compute()` adds `"receipt"` (needs the same Chief reading from `d`); `_failed()` and `Live.snapshot()`'s default dict add `"receipt": None`.

Web (`board/web/`):
- `js/views/costs.js` (54 lines): `render`, `ageLine`, `figures`, `mount` (the `[data-recompute]` delegate). Becomes the two-column layout and picks the batch (spec section 4: `data.batch`, else the newest `state == "closed"` of `data.history`).
- `js/views/costs-tables.js`: `perCr` + `crRow` (Title is `hide-phone` today: Title returns, State goes); `lastMerged` unchanged.
- `costs-history.js`, `costs-action.js` (`recomputeCosts`) unchanged.
- `js/model/live.js` `withLive`: add `cost_receipt: live.receipt` on the batch. New files: `js/model/receipt.js` (pure), `js/views/costs-receipt.js`, `css/views/costs-receipt.css` (link in `index.html` after the `costs.css` line, l.32); paper/line tokens in `css/tokens.css`.
- `css/views/costs.css` (70 lines): two columns (`.cwrap`/`.cside`), phone form at `max-width:760px`, hide `.age .note` on phone.
- i18n: `js/i18n/en.js` l.192-210 (`costs.*`; `spent`, `avg`, `rest` change; new `costs.receipt_*`) and `fr.js`, same keys. The words test is in `tests/test_code_targets.py` (reads `js/i18n/{lang}.js`, l.118).
- Helpers to reuse: `core/format.js` (`usd`, `title`, `age`; `usd` takes no unpriced flag, so "at least $X" needs a small helper in `model/receipt.js`), `ui/parts.js` (`kpi`, `meter`, `empty`), `core/dom.js` (`html`, `vars`, `delegate`).
- To verify before coding: that the server's `data.history` records keep `cost_receipt` (check where the board builds `history`, `board/state.py` / `board/crs.py`; if it filters keys, add it) and that the Costs page loads `history` when no batch runs.

Docs and demo: `docs/web-board.md` "### Costs" (l.74-78); `docs/costs.md` (one line); `docs/web-board/costs-pc.png` and `costs-phone.png` via `just docs-screenshots` (`scripts/docs_screenshots.py` `views()` l.201, costs at l.212 uses `shop-api`); demo surface `docs/demo/projects/mobile-app/changes/5-archives/batches/batch-02.json`: add a made-up `cost_receipt` whose split sums to its `cost_usd`.

## Smallest change

1. `receipt_data(...)` in the cost package returning the JSON of spec section 1; `cost_summary` and `chief_line` render from the same structured pieces.
2. `close` writes `cost_receipt`; `blank_record` has the key; `board/costs.compute` carries `receipt`.
3. Web: one new model, one new view, one new CSS; edits to `costs.js`, `costs-tables.js`, `costs.css`, `live.js`, `index.html`, `tokens.css`, `en.js`, `fr.js`.
4. Docs and demo data.

## Risks

- Byte-identical text: `cost_summary` feeds close (`batch-NN.md`), pause, `status` and `cost --summary`. Refactoring `_split` must keep its "not measured" vs % rule when calls are unpriced and its kind filter. One pytest case with expected lines written out guards it.
- Transcript reads: `close` and `compute()` must read the Chief's sessions once. A `ChantierError` from `_chief_session` must become `outside: null` plus its cause, never abort `close`.
- Code targets: `breakdown.py` is already 306 lines (over the 300 target) and `sessions.py` is 256: check `tests/test_code_targets.py` for its allowance; put the receipt function in a new `commands/cost/receipt.py` if the test refuses more lines in `breakdown.py` (a departure from the spec's "in `breakdown.py`" to state in the PR). Functions at most 50 lines and complexity 10.
- Old values to grep when labels change ("Average cost per active CR", "Spent (", "the rest: steering"): they live in `en.js`/`fr.js`; recheck `docs/`, `scripts/docs_screenshots.py` and `scenario/run_scenario.py` before finishing.
- `apportion` must sum to `round(total*100)`; the split's `usd` are those apportioned cents.
- Every colour must come from `tokens.css` (code-targets test); the mock-up's own colours must be mapped.
- `hide-phone` is shared with Last merged; change only the Per CR table.

## Questions only the user can answer

None.

## Evidence plan

Kind of change: CLI data (the record and the live figure), web UI (a whole page, desktop and phone), docs and demo data.

- pytest, extending `tests/test_cost_reading.py` (with `tests/cost_world.py`'s `CostWorld`, and the helpers `check_the_chief_lines_add_up`, `check_each_agent_type_has_its_line`) and `tests/test_cost_copilot.py` (no parent link: no Driver line, an `agents` part). Parametrized receipt cases: split sums to the total in cents, one Driver line per type sorted by cost, wakes and average context, `outside` null with a cause, direct vs Foreman `outside.steering`; plus one case with `cost_summary` and `chief_line` lines written out. `tests/test_costs.py` for `blank_record`/`close_record` carrying `cost_receipt`. Shown by: `just test` output.
- `just check` (Biome on the new JS/CSS, ruff, mypy, `test_code_targets.py`, the words test); log in `work/gates/`.
- `just scenario` (`scenario/run_scenario.py`): extend the close block (around l.2264, and the Cost checks l.1189-1210): `batch-NN.json` has `cost_receipt`, its split adds to `cost_usd` within a cent, its Driver lines match `batch-NN.md`'s `## Cost` lines; the record from `open` has `"cost_receipt": null`; in the board block (l.1778-1790, `settled_live`), after `POST costs/recompute`, `live.receipt` is present and its split adds to `live.spent_usd`. Windows local run (`chantier gate`) at the stack's top CR. Log in `work/gates/`.
- Screenshots with Playwright (`scripts/docs_screenshots.py` against the demo surface, `just docs-screenshots`; a throwaway script in the scratchpad for the extra states): Costs page desktop and phone on a full receipt (demo `mobile-app` batch-02 with the new `cost_receipt`; the Driver says whether `views()` moves from `shop-api` to `mobile-app`), each beside the mock-up rendered at the same width (`prototypes/01-mockups/final-costs.html`, `final-costs-phone.html`), captioned with the head's 7-character SHA, no real path or user name in any image; plus a closed record without `cost_receipt` ("roles not recorded") and a running or paused batch with no live figure ("not computed yet" and the receipt's Recompute; `shop-api`'s running batch has no transcripts). Kept in the CR's `evidence/`; `docs/web-board/costs-pc.png` and `costs-phone.png` retaken.
- Cannot be shown: live receipt figures from a real session (the demo has no transcripts; only the scenario's fake transcripts prove `live.receipt`). No CR board pane change, so no pane screenshot is owed.
