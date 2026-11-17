# Verifier report, CR 289, head 8f13a022

| # | Result | Evidence |
| --- | --- | --- |
| A1 | PASS | compile ok; findBar*.test.js: 23 pass, 0 fail |
| A2 | PASS | detached worktree of base ce6d8554 + new findBar.test.ts: 2 fail (left-of-box, right-of-box), 21 pass. The "already in view, no write" case is a guard that passes on base (as the coder reported). |
| A3 | PASS | capture.py --scenario toolbar-navigation/v41-find-hit-in-wide-table-light-393: passed |
| A4 | PASS | capture.py --group toolbar-navigation: 41 scenarios passed |
| A5 | PASS with a caveat | Heavy run 43052114268: conclusion success at head 8f13a022; jobs integration, stress, static, static-windows, visual, report, checks all success. find-wide-table is registered in the default real-input sequence (run.ts) and in the named map. The CI log does not print per-scenario names for the default sequence (find-after-click is silent too), so the name cannot be grepped; the passing integration job covers it. |
| A6 | PASS | okfreq validate --check-links exits 0 (only pre-existing W2 warnings in PALETTE-264); 22 @tests_req TOOLBAR-010 lines |
| A7 | PASS | diff vs base lists c5-reading.md and the 271-c5-1 replay json (+20 lines) |
| A8 | PASS by CI | Not rerun locally; static and static-windows green in the heavy run at this head. |

Scope: 20 files, matches the spec's list. The inspector's non-blocking notes stand (no unit test for the "wider than box" and nested cases; null-root guard theoretical).

Verdict: VERIFIED
