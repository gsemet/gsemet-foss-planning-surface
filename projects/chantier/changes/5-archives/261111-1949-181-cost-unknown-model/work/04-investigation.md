# Investigation: CR-181 cost-unknown-model

Code read in the worktree (base 1670ba5; the spec cites 24cc7eb, same cost code). CLI = `skills/chantier/scripts/cli/src/chantier/`. The project's rules (AGENTS.md, CONTRIBUTING, scenario/README) add: `just check` on 3 OSes, `just scenario` before the PR, no version edits, tests structural only and few, no fallback, English, CLI knows no role.

## Files and entry points

**costs.py**
- `PRICE` (l.28), `_family` (l.53, raises "no Claude price"), the only call site is `usage()` l.195-196 (`PRICE[_family(...)]` inside the calls list). Smallest change: `_price(model, prompt, extra)` returns the 5-tuple or None (exact id, or id minus `-YYYYMMDD`; `>100k`/`long_context` tier when prompt above it). `extra` = project prices, passed in as a parameter of `usage`/`session_costs` (not a module global; keeps tests pure).
- `usage()`: a None price makes the call go to `row["unpriced"][model] += 1` in `_add` (parts = None), no `usd`/`usd_*`, no `calls += 1`, but token fields, `peak_context`, `last_context`, `wakes`, `timed/expired` still update. `_new_row` gains `"unpriced": {}` (a dict; merge by sum in every aggregation). Careful: `row["model"]`/`models` for an unpriced call: add to `models` (needed for `--explain` "(not priced)").
- `session_costs` l.224 emptiness test and l.233 subagent filter (`if row["calls"]`) must also count `sum(unpriced.values())`, or an all-unpriced subagent is dropped silently. The `grill` sub-row has the same shape, so its unpriced count must be summed too (l.224 already sums grill calls).
- `copilot_session_costs`: untouched (rows have no `unpriced` key; use `.get`).

**playbook.py**: `load` l.304-306 refuses every key but `roles`; add `prices` branch (validate per spec; reuse `bad(line,msg)`; the parser gives `(line, node)` per key, scalars are strings: number check by `float()` with `bool`/NaN care; negative, missing, unknown key, `long_context` without `above`/five prices). Resolved dict gains `"prices": {id: {...}}`. Note `load` returns `None` when problems, and `{"file","host","roles"}` otherwise; with only `prices` and no `roles`, `roles` is `{}` (fine). `playbook_lines` gets the `prices:` line and the Copilot line; comment above `MODELS` (l.31-32) to rewrite. The playbook recorded at `open` (`d["playbook"]`) must not hold prices as the source of pricing: cost reads live through `read_playbook(repo, host)` (commands.py l.150), which also needs `plugin_roles(host)` (installed agent files): a cost call thus depends on the plugin install for validation, as `open` does; accepted by spec ("refuse as open does"). Risk: the scenario's `cost` calls run with the plugin present, fine; a missing plugin dir would make `cost` refuse where it did not before: only when `chantier.yaml` exists (read nothing when the file is absent: `load` returns `(None, [])` before roles are needed, but `plugin_roles` is evaluated as an argument first; harmless, it only lists files).

**commands.py** (cost block, l.2034-2384)
- `_cost_rows` (l.2039): the one place to load prices (once per call) and pass to `session_costs`; it raises "no priced calls in the Foreman transcripts" when no row has `calls`: keep (decision 6). Copilot rows have no `unpriced`; skip prices on Copilot. Where `_cost_rows` is called: `_refresh` l.1157, `pause` l.1905 (its `except` sets `Spent: unknown (...)`, l.1911: stays only for real failures), `_final_rows` l.2021, `cost` l.2353.
- `_final_rows` l.2017: still wraps any `_cost_rows` error (all-unpriced and no transcript still refuse, the "cannot be priced" text unchanged); docstring and `close` docstring l.1946 rewritten.
- `_record_costs` l.1169: `spent_usd` unchanged (priced part); add `b.data["unpriced"] = {model: n}` (clear to `{}`/absent when none), per-CR `cost_usd` stays priced, plus an unpriced marker per CR (e.g. `c["cost_unpriced"]` from `_cost_groups`). `_cost_groups` l.2167 returns `[calls, usd]` lists; extend with a third slot (unpriced count by model) and check all unpacking sites (`_record_costs`, `_final_pages` l.2030, `_cost_summary` l.2326/2335, `cost` l.2362).
- `_chief_line` l.2109: sums `r["usd"]`, `calls` over `session_costs` rows (including grill rows, `whole`); each of its lines needs its own unpriced remainder; this is the longest piece: `steer`, `grill`, `whole_usd` accumulate separately. A transcript of the Chief of Staff with an unknown model today raises, and `_chief_unknown(str(e))` hid it; after the change it prices as floor. Copilot returns `_chief_unknown`, unchanged.
- `_breakdown` l.2247 / `_cost_summary` l.2305 / `cost` l.2343: add `unpriced` to entries; share per line via `_apportion` (already imported, `_apportion` ignores zero totals); ratio line = steering entries ("Foreman" kind, includes `own` ones as `--summary`'s split does) + "Driver" kind shares; Copilot detection: `any("parent" not in r for r in rows if r["agent"]!="main")` (the `measured` test already in `_cost_summary` l.2325); unpriced anywhere: `share not measured`/`not measured (calls not priced)`. The shares must be printed in the same apportioned list as the mills, so compute shares from `lines` of the by-role mode only. `--by cr` keeps no share.
- `_cost_groups` l.2197 (driver key): for a direct batch the main row's type is `chief-of-staff` (set in `_cost_rows` l.2058), so `key = root["type"]` yields `chief-of-staff` and `_cost_summary` l.2335 prints `Driver chief-of-staff with its workers`. Fix: `key = "foreman" if root.get("own") or root["agent"] == "main" else root["type"]` (note the loop breaks with `root = r` itself when `r` is main). The by-"cr" branch already keys main as `foreman`. Check also that in Foreman mode main type is `foreman` (already fine).
- `_label`/`_kind` (l.2217-2239): no change needed for the Driver-line rule, they already label main/own as steering.
- `_explain` l.2275: models list + "(not priced)" marker and "of the priced calls" wording; `usd_*` shares come from priced only already.
- `cost` first line l.2371 and `Total`/`close` summary: floor wording; the "has no price: add it under prices:" line once per model.
- `status` first line l.1190-1196 via `rails.spent_text`; `rails.over_budget` unchanged. `spent_text(data)` can read `data.get("unpriced")` to return `at least $x`; callers: `status`, `check_budget` message l.159, and l.1846, all acceptable with "at least".

**status.py**: `_priced` (l.242) checks `Spent: unknown` in the summary: keep; `batch_view` add `"unpriced"`; `_budget` l.287 and `batch_markdown` l.308 "spent at least"; `dashboard_view` l.404 (spent figure for the board, also `"unpriced"`); `_row` l.253 (add flag), `_rows_markdown` l.272 ("at least $x"), `cr_markdown` l.236 ("## Cost" line). `write_final_pages` l.460: CR pages at close read `cost_usd` and `final_cost`.

**rails.py**: `spent_text` only (l.145); `over_budget` untouched.

**cards/docs**: `skills/chantier/references/status-layout.md` (sections Progress l.30, Completion l.60, Cost l.81: rewrite with the skeletons; lines 42 and 86-101 refer to Driver/steering lines), `skills/status/SKILL.md` last sentence, `chief-of-staff.md` l.288/371/425 (l.425 text "cannot be priced" check wording), README.md "Costs and budgets" and "Your own agents", `skills/chantier/references/concepts.md` (playbook part), `docs/batch-lifecycle-texts.md` l.173, `docs/tutorial-claude-code.md` l.175 and `docs/use-cases-foreman.md` l.97 (text about a close refused when the final cost cannot be priced; make it "nothing can be priced").

**Tests and scenario**
- `tests/test_costs.py`: the `"unknown-model"` param (l.27) leaves; new tests as specified (floor, dated id). Add pure unit tests of `playbook.load` prices only if cheap; scenario covers the file refusals.
- `scenario/run_scenario.py`: close step l.1473-1482 (`mystery-model` appended to the Foreman transcript, `refused(...)`), `playbook_config` l.1584+ (bad-file table at l.1665: add the five `prices` refusals there, the "unknown key" row at l.1665 text `unknown key "colour"` keeps), section 9 Cost l.718-766 (`check` at l.750 reads `\((\d+)%\)` on out[1], the summary split line: unchanged), l.759-760 `Total: $1.61`, `direct_batch` l.914-1190 (Driver-line checks, own-subagent step l.1097), `copilot_cost` l.3083+ (l.3155 "has no price" refusal stays), l.3272 `--explain` shares regexp. Existing assertions on `cost`'s lines l.719-740 must be updated for the share column (`($0.912 (64 calls, 57%)`) and for `out[0]` equality checks at l.1085.

## Smallest change

costs.py (`_price`, unpriced field, emptiness test) + playbook.py (`prices`) + commands.py (price loading in `_cost_rows`, unpriced carried through groups, breakdown, summary, cost, chief lines, `_record_costs`, `_final_rows` text, driver key fix) + status.py/rails.py (floor wording, fields) + the card/doc edits. No new CLI command, no module. The unpriced remainder is one dict `{model: calls}` carried on rows, groups, entries and `batch.json`.

## Risks

1. `_cost_groups` value shape (`[calls, usd]`) is unpacked in at least six places; changing it to three slots is the likeliest source of silent breakage: prefer a parallel dict (`unpriced_by_key`) over a longer list, or a tiny dataclass.
2. Untimed/grill/spec-writer handling: unpriced calls must follow the same split as priced ones (steering vs grill vs spec-writer rows), or `_chief_line` lines will not add up.
3. The ratio and the shares use `_apportion` on the entries of the batch's spend only; Chief of Staff outside-budget lines get none. In direct mode the steering row is both in the spend and (via `inside`) removed from the Chief's lines: keep that.
4. `chantier.yaml` validation depends on `plugin_roles(host)`; `cost` on a project with a valid `roles:` and no plugin agents refuses ("no plugin agent found") where it never did. Spec accepts "refuse as open does"; the Driver may validate `prices` without requiring roles to be resolvable, to avoid it.
5. A transcript record with `model` missing/empty still raises (unchanged); only an unknown non-empty id is unpriced. `<synthetic>` is already skipped.
6. Built-in price table: figures must come from the provider's pages (network, Driver's job, cited in the PR). A model whose price cannot be found is not added. Nothing in the repo lets me confirm `claude-fable-5-2`'s price; the Driver must fetch it.
7. Key order of output lines is asserted by the scenario (`out[0]`, `out[1]`, `out[2]`): the first line and the breakdown lines move or grow; scenario edits are part of the CR.
8. `STATUS.json`'s `priced` stays true for a floor; consumers of the board (docs, `skills/status`) must be told `unpriced`.
9. Wording asserted in docs (`close` "cannot be priced") appears in 3 docs, 1 card and the scenario; update together.

## Questions only the user can answer

None. Spec says none open and I found none.

## Evidence plan

Kind of change: CLI behaviour and output text, a card rewrite (report skeleton), docs. No UI.

- Before/after: the `cost`, `status`, `status --refresh`, `pause`, `close` outputs and `STATUS.md`/board JSON with one `mystery-model` call, captured as command output into `evidence/` (before: the refusal `cannot close ... cannot be priced` and `spend not updated`; after: the floor lines). Technique: `just scenario` fixtures (the scenario's world already builds a transcript with `mystery-model` at l.1473-1482 and a Copilot fake via `CHANTIER_SESSION_USAGE`), run from the worktree; save the relevant `cost` output blocks and the `close` output to `evidence/cost-floor-after.txt`, and the before from `git stash`-less run on base (`origin/main` in the main checkout is protected by the "main does not change during an eval" rule: run before-captures from a second worktree on base, not the main checkout).
- Shares and ratio: `cost` output of section 9 with the shares column, before/after; the scenario's assertion that shares add up to 100 and the ratio equals steering + Drivers.
- `chantier.yaml` prices: `playbook` output with the `prices:` line, five refusal outputs with their lines (scenario step 4), `cost` with priced `mystery-model` and dated id.
- Direct batch: `cost --summary`, `pause`, `close` outputs with no `Driver ... chief-of-staff` line.
- Unit: `uv run pytest` in the CLI folder (`just check`) for the two new `test_costs.py` tests.
- Card: the new `status-layout.md` skeleton read through once against a real `cost` output from the scenario (a hand-built Progress report in `evidence/report-sample.md`): there is no automated check of a report; `tests/test_structure.py` only if the Driver judges a presence test of the skeleton needed.
- Cannot be shown: a real provider price page figure (network, Driver's citation in the PR); the Copilot host for real (fake usage tool only); a real Chief of Staff or Foreman writing the report from the card (that is an eval, not this gate); Windows/macOS runs (CI shows them).
