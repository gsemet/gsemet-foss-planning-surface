# CR-221 Coder, round 1: done, remains, open decisions

## Done (in the worktree, nothing committed)
- PEP 723 block in `chantier.py` (pydantic, ruamel.yaml, psutil; `[tool.uv] no-build = true`); `chantier.py.lock` (untracked: the Driver must `git add` it).
- `pyproject.toml`: same three dependencies, ruff (rules, caps, banned module-level imports) and mypy strict config.
- Package split per "The package layout": `core/`, `lifecycle/`, `playbook/`, `costs/`, `status/`, `commands/` (+ `cost/`), `board/`, `plugin_files.py`, `rails.py`, `procs.py`, `cli.py`; `register(sub)` in every command module; `just` import-cycle check (`work/tools/cycles.py`): no cycle.
- `Batch.after_save()` hook + `lifecycle/session.py::RenderedBatch`, and `lifecycle/convert.py::open_repo`, break the repo/batch/status cycles with no in-function import.
- Tests updated to the new paths; `just test`: 58 passed.
- `scenario/run_scenario.py`: only import paths of moved names changed.
- `just scenario --forge github` through `uv run --no-project --with-requirements ...chantier.py python`: 677/677 checks. Not run: gitlab.
- justfile: `lint` recipe (ruff format --check, ruff check, mypy, `uv lock --script --check`), `check: lint test release-notes`, scenario and eval-dry-run on the PEP 723 environment.
- `commands/__init__.py` docstring.
- ruff autofixes applied and `ruff format` run.

## Remains
1. `ruff check .`: 182 findings left: E501 x35, PLR1702 x33, PLR2004 x26, C901 x21, PLR0912 x13, PLW1510 x10 (`check=False`), PLC0415 x7, E731 x6, PLR0915 x6, PLR0913/0917 x5, PLW2901 x4, others small. Known long functions to split: `_apply_order` (~170 lines), `usage`, `_convert`, `gate`.
2. Files over 400 lines: `commands/orders.py` (429), `tests/test_structure.py` (586): split the tests into `test_plugin_files.py`, `test_cli_runs.py`, `test_cli_units.py`.
3. `mypy --strict` not yet run or fixed (annotations are partial; tests included).
4. Not started: pydantic record models (batch.json, an events line, seat.json, `.long-gate.run`, restored.json); `Batch.data` is still `dict[str, Any]`.
5. Not started: `playbook/yaml_subset.py` on ruamel.yaml (lazy import, keep structural refusals and lines); `procs.py` on psutil (lazy import, `os.killpg` kept on POSIX).
6. Not started: `tests/test_code_targets.py` (sizes and imports with no cycle; dependency lists agree and `no-build = true`).
7. Docs: the two AGENTS.md edits, CONTRIBUTING.md (item 2, board line, "Set up", "Code standards", layout line), README.md ~line 208, docstrings of `playbook`, the board and `session_usage.py`.
8. Targets for `session_usage.py`, `chantier.py`, `scenario/` and `evals/` Python under `skills/` if any; refresh `uv.lock`; run `just check` and the gitlab scenario.

## Deviations from the specified layout (all to avoid a cycle)
- `normalize_batch`/`normalize_cr` live in `core/records.py`.
- `release`/`cancel` are in `commands/release.py`, apart from `delivery.py` (keeps the help order).
- `commands/registry.py` holds `add_command` and the scope constants.
- `cost_rows` is in `commands/cost/sessions.py`; `OWN_CHIEF` too.
- `playbook/models.py` holds `HOST_NAMES`; `board/collect.py` holds `EVENTS_HIDDEN`.
- Cross-module underscore names lost their underscore (`read_seat`, `chain`, `price_table`, `cost_kind`, ...).

## Open decisions
- `ruff` pin 0.17.5 and `mypy==1.20.0` are in justfile variables.
- uv warns "Ignoring `--no-binary` setting from requirements file" when the lock-exported requirements are used with `--with-requirements`; harmless, `no-build` is set in the script.
- No STATUS byte changed (scenario passes).
