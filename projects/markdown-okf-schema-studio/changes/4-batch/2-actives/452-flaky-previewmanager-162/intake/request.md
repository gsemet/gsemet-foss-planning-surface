# Flaky previewManager test (2 !== 1)

Flaky unit test: test/session/previewManager.test.ts:162 failed once locally (2 !== 1) and passed on rerun, seen during CR-432 (batch-06), which does not touch it. Find the race and make it deterministic.