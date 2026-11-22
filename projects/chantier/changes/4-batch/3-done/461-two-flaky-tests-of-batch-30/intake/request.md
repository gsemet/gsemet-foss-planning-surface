# Two flaky tests of batch-30

Priority P1, next batch (the user, 2026-11-22). Flaky in batch-30: `test_w2_a_shell_inside_the_folder_refuses_then_lets_go` and `tests/test_live_link.py::test_the_refusals_of_several_boards[only-two]` (and its `[only-one]` variant, seen later in batch-30) failed once and passed on re-run, on Windows and in CI. Intent: find why (timing, port reuse, file locks) and make them deterministic.
