# 232-visual-capture-drops-networkidle-wait

Priority: P1 (stack -v5 blocker, approved by the owner via the CoS on 2026-10-31).

## Why

Test-only. The visual scenario v20 hangs intermittently: page.wait_for_load_state('networkidle') in test/visual/capture.py:294 never resolves on the 2.3 MB page when preview.js is requested more than 0.5 s after the document finished (Playwright 1.64.1 idle-tracking race; evidence /private/tmp/claude-502/v20-debug/NOTES.txt). Also, a retry drops attempt-1 non-timeout failures (capture.py:284) and the HUNG line does not say which call hung.

## Done when

The networkidle wait is gone; goto's load wait and the render-state waits remain. A retry keeps attempt-1 failures that are not timeouts; the HUNG line logs the timed-out call. The retry stays as a safety net (max once).

No behaviour gate: test-only, nothing a user sees changes.
