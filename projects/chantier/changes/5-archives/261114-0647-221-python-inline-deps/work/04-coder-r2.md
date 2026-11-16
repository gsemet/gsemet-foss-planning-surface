# CR-221 Coder, round 2: done, remains

Nothing committed (the Driver commits). `just test`: 59 pass, 1 fails on purpose
(`test_code_targets.py::test_files_and_functions_are_small...`, red until the targets are met).
`just scenario` (justfile recipe, both forges) after step 1: github 677/677, gitlab 658/658.

## Done
1. Libraries.
   - `core/records.py`: pydantic models `BatchRecord` (+ `BatchSettings`, `CrEntry`), `EventRecord`,
     `SeatRecord`, `RunRecord`, `RestoredRecord`, all `extra="allow"`, written with `to_data()`
     (`exclude_unset`). Old words `landed`/`open` in a `model_validator(mode="before")`; "invalid
     batch settings; refusing to run" kept (raised in `read_batch_json` on a bad `settings`);
     `chief_sessions`, `round_limit`, `read/write_restored_number`. Used by `core/batch.py` (write of
     `batch.json`, events lines), `core/seat.py` + `commands/seat.py` + `board/server.py` (attributes),
     `commands/gate.py` (`RunRecord`), `commands/intake.py` (restored).
   - `playbook/yaml_subset.py` on ruamel.yaml events (pure parser, lazy import): tab and several
     documents stay a line check before the parse; anchors/aliases/tags, block scalars, flow
     mappings, list in a list, duplicate key keep words and lines (checked by hand, scenario S4 passes).
     "an empty value" was unreachable in the old parser, so it is not reproduced. Lexical errors now
     use ruamel's text with `line + 1`.
   - `procs.py` on psutil (lazy import; `os.killpg` kept on POSIX; Windows tree kill by psutil;
     POSIX rule "cwd or command line", Windows "command line only" kept; a zombie is gone).
   - pyproject: `TID253` added to `extend-select` so ruff's banned-module-level-imports (ruamel,
     psutil) exempts their lazy imports from `PLC0415`. `allowed-confusables` now written as
     `→`, `…`, `–` escapes.
2. Tests: `test_structure.py` split into `test_plugin_files.py`, `test_cli_runs.py`,
   `test_cli_units.py` (all under 400 lines); `test_code_targets.py` has the two tests (the
   dependency one passes).
3. Docs: AGENTS.md (two edits, plus `tests/test_structure.py` -> `tests/` in the tests line, since
   the file is gone), CONTRIBUTING.md (item 2, board line, layout line, "Set up", `just check`
   line, new "Code standards" before "Versions"), README.md, docstrings (`playbook/`, `board/`,
   `session_usage.py`, `yaml_subset.py`, `procs.py`).
4. Partial: `justfile` has the `lint` recipe (ruff format --check, ruff check, mypy with
   `--with-requirements chantier.py --with pytest`, `uv lock --script --check`); `check: lint test
   release-notes`. mypy `files` no longer lists `chantier.py` (module name clashes with the package;
   it is a 20-line launcher). Tests are annotated and ruff-fixed in part. `ruff --fix` and `ruff
   format` applied everywhere.

## Remains (the last round)
- `ruff check`: 178 findings: E501 x38, PLR1702 x32, PLR2004 x23 (tests: use EXIT_* constants),
  C901 x22, PLR0912 x13, PLC0415 x6 (tests: move the in-function imports up), PLW1510 x6 (add
  `check=False`: delivery, driver, forge_stack, core/git, costs/copilot, a test), PLR0915 x6,
  PLR0913/0917 x5 each, PLW2901 x4, SIM x4, PLR0911 x2.
- `mypy --strict`: about 480 errors left in `src` (tests about 30). Biggest: orders 44, rails 29,
  cost/sessions 22, playbook/config 21, forge_stack 16, facts 16, status/words 15, transcripts 14.
- Files over 400 lines: `commands/orders.py` (446), `rails.py` (436).
- Functions over 50 lines (about 35; `test_code_targets` lists them): `_apply_order` 221, `usage`
  132, `_convert` 128, `open_batch` 127, `preflight` 147, `order` 116, `copilot_session_costs` 73,
  `restore` 75, `_handler` 64, `cost_summary` 66, `_archive_and_delete` 67, `_activity` 66, ...
- Records: the code still reads `Batch.data` as `dict[str, Any]`; the models validate and write it
  but attribute access through the models everywhere is not done.
- Not run after the last ruff/format pass: `just scenario` (tests pass; the ruff changes were
  format and import-sorting only, rerun once at the end).
- `just eval-dry-run` not run this round. `just check` not run (lint is red).
- A stray empty `chantier.py` at the worktree root (and the main checkout) is untracked and not
  mine; the Driver should not add it.
