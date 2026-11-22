# Two flaky tests of batch-30

Make two tests deterministic: `tests/test_live_link.py::test_the_refusals_of_several_boards`
(`[only-two]`, `[only-one]`) and `test_w2_a_shell_inside_the_folder_refuses_then_lets_go`. The
first fails on ubuntu in 3 of `main`'s last 6 runs, so `main` is red and the v0.15.0 release
waits for this fix (the user, 2026-11-22).
Short name: `flaky-tests-30`
