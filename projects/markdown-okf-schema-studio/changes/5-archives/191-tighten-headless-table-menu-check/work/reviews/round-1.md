# CR 191 — Inspector review, round 1

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-191` (branch HEAD `cb1f2adc` + uncommitted diff).

## Scope of the diff

Only intended files changed:

- `test/visual/capture_support.py`: adds `TABLE_BAR_STYLE_JS` and `table_bar_flow_failure()` (with `@tests_req SwRS-MDOKFSTUDIO-TABLE-064`).
- `test/visual/capture_edit_checks.py`: import + the `elif` at ~1115 now calls the helper; still 1500 lines.
- `test/build/test_table_bar_flow.py` (new, untracked): 4 unit tests.
- `justfile`: `release-tests` runs the new test file.
- `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-064.md`: two `tested_in_files` entries added
  (sorted). `lifecycle: proposed` (was already proposed at HEAD). No StRS touched.

## Checks

| Check | Result |
| --- | --- |
| JS returns the keys the helper reads (`position`, `top`, `left`, `bottom`, `right`, `zIndex`) | OK, identical object to r06 |
| Call site wiring | OK: walrus in the `elif` chain, failure message appended via `Failure(page_name, bar_failure)`; the following "directly precedes its table" `elif` is unchanged |
| Parity with r06 (`editorWidgets.ts` 753-765) | OK: position exactly `relative`, each side `auto`/`0px`, z-index exactly `"3"` |
| Weakened assertions | None; the old check accepted `static`, the new one rejects it (strictly tighter) |
| Shipped CSS consistent | `editModeStyles.ts` has `z-index: 3` on the bar rules |
| `py_compile` of both visual modules | OK |
| `release-tests` command (incl. new file) | 84 passed (warnings are pre-existing pytest tmp cleanup noise) |
| `okfreq validate --check-links --project-root .` | 1067 requirements, 0 errors, 0 warnings |
| `just check-limits` / `just check-markers` | passed |

## Mutation testing (scratch copy in `/private/tmp/claude-502/cr191-driver/inspect-r1/`)

Baseline: 4 passed. Each mutation of `table_bar_flow_failure` made at least one test fail:

| Mutation | Result |
| --- | --- |
| accept `static` as well as `relative` | 1 failed |
| ignore offsets entirely | 1 failed |
| check only `top`/`left` | 1 failed |
| ignore z-index | 1 failed |
| accept z-index `auto` | 1 failed |
| reject `0px` (only `auto`) | 1 failed |

The tests are meaningful for every rule of the intent.

## Notes (non-blocking)

- The unit test imports `capture_support`, which imports Playwright and reads `test/shared/geometry-checks.js` at import
  time; it therefore needs the `docs` group. `release-tests` already uses `--group docs`, so this is fine as wired.
- The headless campaign itself was not run in this review (no browser run requested); the change at the call site is a
  pure refactor of the predicate into the unit-tested helper.

## Verdict

APPROVE
