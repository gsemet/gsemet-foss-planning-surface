# Verifier report r2, CR 289, head 24565af0 (restack of 8f13a022, rebase only)

| # | Result | Evidence |
| --- | --- | --- |
| A1 | PASS | compile ok; findBar*.test.js: 23 pass, 0 fail |
| A2 | PASS (carried from r1) | Rebase only; r1 showed 2 horizontal cases failing on the base. Not rerun. |
| A3 | PASS | capture.py --scenario toolbar-navigation/v41-find-hit-in-wide-table-light-393: passed |
| A4 | PASS | capture.py --group toolbar-navigation: 41 scenarios passed |
| A5 | PASS | Heavy run 43059797039: success at 24565af0 (integration and stress included). find-wide-table is registered in run.ts; CI does not print default-sequence names (as in r1). |
| A6 | PASS | okfreq validate --check-links exits 0; @tests_req TOOLBAR-010 present in 9 files |
| A7 | PASS | diff vs base 290 lists c5-reading.md (+19) and the 271-c5-1 replay json (+1) |
| A8 | PASS by CI | Not rerun locally; heavy run green at this head. |

Verdict: VERIFIED
