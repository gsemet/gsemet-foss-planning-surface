# Verify CR-318, head 2ca565e1

- Visual: capture.py on toolbar-navigation v06..v21 (15 scenarios ran, 16 ids; v21 not a separate run on base either): status passed, incl. check_toolbar_collapse (Tab order, width equal expanded/collapsed within 0.5 px, <= 134 px) and check_preview_toolbar_rows (rows main, navigation, view, review, 4 buttons each).
- Unit: node scripts/node-test.mjs unit out/test/core/preview/previewStyles.test.js: 104 pass (T08 offsets 160 px / 62 px asserted at test line 905-906).
- Screenshots: before/ vs after/ show 5x3 becoming 4x4.
- CI: PR 390 run 43480609447 at 2ca565e1: static, static-windows, visual, report pass; integration/stress skipped (PR path); "checks" pending (aggregate).
- Heavy: no heavy run at 2ca565e1. 43480001535 is at b1e8d1be and ended startup_failure (workflow file issue); 43476490855 at b9f7dc2b: integration failure, stress success.
Verdict: VERIFIED for the visual/unit claims; heavy integration and geometry y 12..146 unproved at this head.
