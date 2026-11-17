# Report — 044-flaky-linked-target-watcher

Status: **done** (2026-10-23, branch `fix/linked-target-watcher`,
[PR #40](https://github.com/gsemet/markdown-okf-schema-studio/pull/40), merge commit 13af918).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | The linked-target watch reports its state to the test snapshot; the integration test waits until the target is watched before saving (helper `test/integration/linkedTargetSave.ts`, diagnostic timeout messages); new `linked-target-save` stress scenario; no timeout raised, no retry, no sleep | f01a231 (13af918 on main) |

## Proof of completion

- 3/3 rounds, reviewer APPROVE on round 3.
- Root cause analysis (r1): all 5 watcher timeouts in 38 failed CI runs predate d53b756 (direct watch).
- Local gates: tsc clean, unit 1915/1915 (r1), `just check`, `just visual` 300 scenarios; local stress 20/20.
- CI: [run 39977481749](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/39977481749) `checks` pass; heavy
  [run 39978607074](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/39978607074) integration + stress 20/20 pass;
  main [run 39977727664](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/39977727664) success.

## Open items

- Full local suite failures on macOS (checkboxToggle undo, slash menu after line break) moved to CR 048 (decision 6 there).
