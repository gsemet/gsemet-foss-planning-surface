# Investigation: CR-409 typed waits, a CR records what it waits for

Read in the worktree `chantier.worktrees/batch-29-CR-409` (base 40363bd7, CR-405's head). Paths below are under `skills/chantier/scripts/cli/src/chantier/` unless said otherwise. Nothing was modified.

## 1. Files and entry points

Record and lifecycle
- `core/records.py` `CrEntry`: no `waits` field. Add `waits: list = []` (dicts, not a nested model: unset nested fields drop out of the dump, so a model's fields would have to be set one by one). `Record.append` marks the field as set.
- `core/batch.py`: `Batch.__exit__` saves `batch.json` only when an event was logged, so every wait command must call `b.log(...)`. `check_epoch` / `require_epoch` gate the new `wait` command.
- `commands/joining.py` `join_cr`: has an early `if not came:` return before the `formerly.json` consume. The `waits.json` read and consume must go ahead of it (a never-batched CR has no `came`). `join_paths` (the `check_publish` list) must list `cdir/"waits.json"`.
- `commands/came_back.py` `reopen`: `waits` is not in its unset list, so the record keeps its waits across a come-back. Correct as is; say so in a test.
- `lifecycle/moveout.py` `move_out_cr` writes `formerly.json`: write `waits.json` here and add it to its `check_publish` list. `leave_batch` is reached from `commands/orders_drop.py` and from `release.py` (cancel).
- `core/repo.py` `check_publish`, `store`, `rel`: the write goes through `repo.store` (`store/base.py`, `folder.py`, `surface.py`).

Declaration and commands
- `declare/driver.py` `_register_record`: holds `handback`; add a repeatable `--wait`. Register `wait` here (`BATCH_EPOCH`, positionals `cr?`, `action?`, args). `cli.py` `FULL_OUTPUT` needs `wait`.
- `commands/driver.py` and `commands/driver_checks.py`: `handback_args` (validation, usage text) and `handback_blocked` (append the waits, add the `; waits: ...` suffix).
- `commands/batch_status.py` `_cr_row` (the ` | waits: ...` segment) and `_seen_lines`, which calls `journal.lines(entries, d.id, open_crs, d.orders)`.
- `commands/facts.py` `cr_facts`: also used by `take` and `round`, so the wait line prints there too unless limited.
- `status/words.py`: `waits`, `waits_on`, `phase_text` (stays "waits for the user").

Hub and journal
- `hub/interests.py` `PROVIDERS = (batch_prs.PROVIDER,)`; `hub/batch_prs.py` is the template for a new `hub/waits.py` (kinds `{"pr"}`, `by` = `<batch> <cr> <wait id>`, emits `wait-cleared@1`, adds no query, exposes `unseen()` for `waits_unseen` in the `server.json` hub entry). `hub/interest.py`, `hub/cycle.py` (early return and an `if mine` guard affect when `waits_unseen` is computed), `hub/state.py`.
- `hub/schemas.py` `PUBLISHED`: add `wait-cleared@1` (model, wake rule, text, duplicate key, example); run `just journal-schemas` to regenerate `schemas.json`.
- `hub/journal.py`: `lines()` handles only `merged@1` and the slots line; it needs an open-waits parameter and a `wait-cleared@1` branch. `waking`, `event_text`, `_key`, `append` are driven by `PUBLISHED`. `hub/lines.py` for the hub's status lines.
- `connectors/` (`__init__.py` `connector_for`, `read`, `UNCLAIMED`, `NOT_ONE_REPOSITORY`, `Place`; `github.py`, `gitlab.py`, `base.py`, `run.py`). GitHub `review` comes from `reviewDecision` (null -> `unknown`); GitLab `review` is `unproved`.

Board and validate
- `board/crs.py` `_row` (an existing `"waits"` key: add `open_waits` beside it); `board/state.py` calls `crs.cr_rows` and `backlog_items`; `board/backlog.py` `backlog_items` (follow the `depends_of` pattern for `waits.json`).
- Kanban shows "waits for the user" from the server's `phase` string (`status/words.py`), not from `js/i18n`. Card: `board/web/js/views/kanban-cards.js` `crCard`, `js/ui/item-card.js`, `js/i18n/en.js` + `fr.js`; `board/web/DESIGN.md` must be read and kept true.
- `commands/validate.py` `findings`: add `waits_findings`. `lifecycle/layout_check.py` `CR_FILES` is stage-agnostic. New reader module mirroring `summaries/store.py`.

Tests and scenario (repo root `skills/chantier/scripts/cli/tests/` and `scenario/`)
- `tests/forge_world.py`, `test_forge_hub.py`, `test_hub_connectors.py`, `test_connectors.py`, `test_store_command_table.py` (rows for `wait` and the changed `handback`), `test_validate.py`, `test_event_types.py`, `test_startup_manifest.py`, `test_scenario_coverage.py`.
- `scenario/run_scenario.py` (`UNITS`, `CASES`, `forge_hub` ~L1722, `SurfaceWorld` ~L8661), `scenario/fake_gh.py`, `scenario/fake_glab.py`, `scenario/README.md`.
- Docs/cards: `AGENTS.md` (exception wording: recount at the rebased head), `docs/forge-connectors.md`, `docs/web-board.md` (l.75), `docs/planning-folder.md`, `docs/boards.md` (l.25), `skills/chantier/references/{driver,concepts,chief-of-staff,foreman}.md`.

## 2. Smallest change

1. `CrEntry.waits` plus a `wait` command (`add|clear|list`) and `handback --wait`; ids `w1, w2...`; types `answer|approval|pipeline|merge`; `cleared_at/by`.
2. `waits.json` (`{"schema":1,"waits":[...]}`) beside `formerly.json`: written by `move_out_cr`, read and consumed by `join_cr`, both through `repo.store` after `check_publish`.
3. One `waits` hub provider (no new query) clearing `pr`-kind waits from the facts the batch provider already reads; `wait-cleared@1` in `PUBLISHED`; `waits_unseen` in the hub entry.
4. Display: ` | waits:` in `_cr_row`, wait line in `cr_facts`, `open_waits` in the board row and backlog item, a count on the card.
5. `validate` check, docs, one-line pointer in driver.md.

Cuts to hold: no `--lease` (Part D absent); the GitLab approval half cannot ship (no account to test): list it under Known gaps.

## 3. Risks

- **45,000-byte cap on driver.md's common path** (`test_startup_manifest`). Measured at the base: 44,947 bytes, room 53. Any pointer to `wait` in the common path needs at least ~70 bytes cut elsewhere (candidate: "Means: your end"). Search for `44947`, `44,947`, `45000` and `53` in tests/docs after editing, and recompute every value derived from it.
- AGENTS.md exception count and ordinal (git/forge reads): recompute at the rebased head, not from the spec.
- `journal.lines` has no hook for waits: signature change touches `_seen_lines` and every caller/test.
- `cycle.py` early return and `if mine`: `waits_unseen` must be computed on the path that returns early too, or it reads stale.
- `join_cr` early return: a never-batched CR would lose `waits.json`.
- Both `check_publish` lists (`join_paths`, `move_out_cr`) lack `waits.json`: an unpublished write would be refused or lost.
- Record wins on matching ids at join: a wait cleared by hand in the backlog reappears open after a drop and return (see questions).
- `Batch` saves only after `b.log`: a silent no-op write otherwise.
- Adding a command to the table needs rows in `test_store_command_table.py`.
- Fakes: `fake_gh` head is not a full sha; `fake_glab` has no graphql; `forge_world` does not enforce NOT_ONE_REPOSITORY. Waits tests that depend on these need the fakes extended.
- No pane change: no screenshot owed. A board card change follows `web/DESIGN.md`.
- A change under `hooks/` or `types/` is not planned (no `just mod`); confirm none is touched.

## 4. Spec parts that do not fit the code

1. The Kanban "waits for the user" is a server `phase` string, not an i18n string.
2. `journal.lines` has no waits hook.
3. `cr_facts` also feeds `take` and `round`.
4. The cycle's early return and `if mine` guard affect `waits_unseen`.
5. `CR_FILES` is stage-agnostic: `waits.json` is allowed in every stage, so the validate check must carry the stage rule itself.
6. `join_cr`'s early return skips `waits.json` for never-batched CRs.
7. `join_paths` and `move_out_cr` `check_publish` lists lack `waits.json`.
8. fake gh head is not a full sha; `fake_glab` has no graphql.
9. `forge_world` does not enforce NOT_ONE_REPOSITORY.
10. `wait <cr> add` has an awkward argparse shape (optional positional `cr` then `action`).
11. `Batch` saves only if events are logged.
12. `test_store_command_table.py` needs rows.
13. Part D is absent: no `--lease`.
14. GitLab approval cannot ship.

## 5. Questions only the user can answer

1. A wait cleared by hand in a backlog `waits.json`, then the CR joins again: should the record's list or the file win? (Today the record wins on matching ids, so a hand clear would reappear.)
2. Should the wait line print in `take` and `round` too, or only in `handoff`/`status`?
3. When every PR of the batch is merged, which Place does the batch provider give a `pr` wait (the last PR's)?

## 6. Evidence plan

Kind: CLI behaviour, hub journal event, record/file format, board JSON. No pane change.

- `just check` (Linux/macOS/Windows) and `just eval-dry-run` (CLI `src/` changed): output tail in `evidence/`.
- Before/after: `$CHANTIER status` and `handoff` output showing the ` | waits:` segment and the `; waits: ...` suffix, captured on a scenario batch; before = base, after = head.
- A `waits.json` generated by `order drop`, shown as a file, and the `join_cr` pick-up (batch.json excerpt).
- Hub: a `forge_world` run showing `wait-cleared@1` in `forge-journal.jsonl` and `waits_unseen` in `server.json`; regenerated `schemas.json` diff.
- Board: `GET` of the board state JSON showing `open_waits` on a CR row and a backlog item (no screenshot; Kanban card text only, with DESIGN.md read).
- `test_startup_manifest` output with the new driver.md byte count (must stay under 45,000).
- Long gate: `just scenario` on the pipeline (ubuntu-latest) green at the head; the top-of-stack CR also runs it locally on Windows via `chantier gate`.
- Cannot be shown: GitLab approval wait (no account), a real forge's `reviewDecision` flow (fakes only), the Windows hub lock timing.
