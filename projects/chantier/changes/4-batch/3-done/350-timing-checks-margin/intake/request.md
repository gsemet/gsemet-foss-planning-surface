# Timing-bound checks hold on a loaded machine

From the retro of batch-24 (2026-11-18), kept by the retro critic; the user asked to file all six and run them in batch-24.

Timing-bound checks failed under load and cost reruns: the local Windows gate at CR-336 (`order merged does not signal a reused pid`, a scenario check), `test_board.py::test_join_observe_reports_early_failure_exactly` (`timeout=1`, macOS, CR-345), and a mypy wheel download timeout on macOS (CR-343). The scenario's reused-pid check and the autosync test wait on a condition with a margin that holds on a loaded machine, not on a fixed short timeout; a download timeout in CI is retried once.

