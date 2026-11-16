# CR-221 Coder, round 3: done, remains

Nothing committed. `just test`: 59 pass, 1 fails on purpose (`test_code_targets`).

## Counts at the end
- `ruff check`: 49 findings (from 178): PLR1702 x21, C901 x13, PLR0913 x6, PLR0912 x5,
  PLR0917 x5, E501 x1 (`delivery.py:76`), PLR0911 x1. `ruff format`: clean.
- `mypy --strict`: 401 errors in 52 files (from about 510). Not worked on beyond what the
  refactors touched.
- Files over 400 lines: none (`orders.py` and `rails.py` are split).
- Functions over 50 lines: 17 left: `_handler` (server), `close`, `_archive_and_delete`,
  `cost_summary`, `cost`, `chief_line` (97), `ship` (53), `cr_facts` (83), `_rebuild`, `_show`,
  `restore` (75), `seat`, `copilot_session_costs` (79), `prepared_cr`, `config.load`, and one test
  (`test_preflight_warns_on_missing_allow_rules...`).

## Done
1. `rails.py` split: `rails_release.py` (grant, release merge, fix go, ask). `orders.py` split:
   `orders_apply.py` (one handler per order kind, `Word` dataclass, dispatch table).
2. ruff: E501, PLW1510, PLC0415 and PLR2004 (tests) at zero; complexity removed from `order`,
   `open_batch` (+ `opening_record.py`), `handback` (+ `driver_checks.py`), `gate` (`_Gate`),
   `preflight` (`_Report`), `usage` (`_Scan`), `_convert`, `status` and `_activity`.
3. Tests moved imports to the top and use constants.

## Remains
- The 49 ruff findings and 17 long functions above; mypy 401 errors; `Batch` attribute access
  not started (the code still reads `Batch.data`).
- Not run: `just eval-dry-run`. `just check` is red (lint) until the ruff findings are gone.
- `$CHANTIER rules` was not run.
