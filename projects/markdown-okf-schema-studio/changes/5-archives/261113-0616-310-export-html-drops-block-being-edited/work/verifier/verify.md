# Verify CR 310, head 055efc8a

1. Page-level and unit tests at head: 30 pass, 0 fail (evidence/head-tests.txt).
2. Same page-level tests on base cb968299: cell, front matter value, front matter key fail; paragraph, card, list-table pass (evidence/base-tests.txt).
3. Visual v44 at head: passed (evidence/head-visual.txt); on base: fails with the cell text hidden and a hidden wrapper left (evidence/base-visual.txt).
Real-window manual steps not run (CI integration green).
Verdict: VERIFIED
