# 233-demo-capture-taller-viewport

Priority: P1 (stack -v5 blocker, approved by the owner via the CoS on 2026-10-31).

## Why

Test-only. Since the narrow-toolbar fix (d5c3de33) the demo boxes start 85 px lower when the toolbar is expanded, so the fleet-loop SVG ends below the 900 px window and scenarioToolbarState fails (test/integration/realInput/previewWindow.ts:402; evidence /private/tmp/claude-502/demo-capture-debug/).

## Done when

The demo check and capture run at 1400x1040, with 900 restored in finally; the visibility assert becomes a waitFor that logs top, bottom and innerHeight. The toolbar is not collapsed.

No behaviour gate: test-only, nothing a user sees changes.
