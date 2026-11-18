Head: 7f075653e3d22075b3b7a284cc1f4593c82a83df

Verdict: VERIFIED

Move judged: 94f0924..7f07565 (one commit: batch-gantt.css grid minimum 480px to 400px, two lines, and a retaken docs/web-board/batch-gantt-pc.png; `git show --stat HEAD`).
Method: real Chromium (Playwright, scripts/docs_screenshots.py setup, board served from the worktree with fixed clock, UTC). Script `work/verifier/gantt-7f07565.py.txt`, raw output `work/verifier/gantt-7f07565.log`. Screenshots (made-up /home/demo paths, no username) in evidence/7f07565-gantt-{1400x860,1400x1300,390,390-scrolled}.png.

1. Gantt at 1400 px (7f07565), the claim that failed at 94f0924. Output: 1400x860 and 1400x1300: `.gscroll` box 280..968, scrollWidth 686 = clientWidth 686 (no clip, before it was 720 > 686), now line x 967, label right 967, both crosses (CR-147, CR-148) right 965: all inside the box. Image evidence/7f07565-gantt-1400x1300.png opened: now line and its "now" label at the right edge, crosses on CR-147 and CR-148 rows, the hatched open bars end at the line. The docs image's fold: the 860 px shot shows the now line, the crosses lie below its fold (accepted, named in the PR's Known gaps per the brief). PASS.
2. Narrow screen (7f07565), 390x844: scrollWidth 620 > clientWidth 364, so the panel scrolls horizontally; after scrollLeft=256 (max) the label column stays at x 21..224 and the now line/crosses come into the box (now x 377 <= 378). PASS.
3. Carried from 94f0924: the move touches only batch-gantt.css and one png (claims 1-6 and 8-12 of the earlier verify: tabs and URL, lazy module, burst, Gantt data and arrows, stamps, chips, FR, closed batch, costs files). Claim 7 (visual) is judged again as 1 above.
4. Not re-run, as before: the Review box and PR description were not re-checked at this head beyond the brief (CI green at head per the brief); the receipt's image copy and a live batch stay unproven, as in 94f0924.

VERIFIED
