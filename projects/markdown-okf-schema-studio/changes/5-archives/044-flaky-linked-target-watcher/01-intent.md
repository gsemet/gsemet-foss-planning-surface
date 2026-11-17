# Flaky integration test: linked-target watcher timeout

Seen 2026-10-22 21:05 on PR #21 (docs only, run 39848594435, job 120068405234): "Preview editing
integration failed: Error: Timed out waiting for the linked-target watcher to deliver the event of
the save." Docs-only change, so the test is flaky. The user wants rocket-solid tests: find the root
cause (watcher event ordering/latency under xvfb), do not just raise the timeout.
