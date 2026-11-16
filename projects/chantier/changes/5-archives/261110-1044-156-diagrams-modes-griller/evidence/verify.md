# Verify CR-156 at 5916187

1, 2: just check and just scenario passed locally and in CI at this head (cited, not rerun).
3: e3.txt, all docs/*.svg parse (ok).
4: e4.txt. No DESC DIFF, MISSING or NOT IN COMPANION. 36 "NOT DRAWN" lines (companion line joins several drawn texts); the same 36 at base c2e6bb3 (e4-base.txt): layout, not a defect.
5: e5.txt. 32 relative links/images/anchors, 0 bad; git grep for the old image name: 0 matches.
6: seven PNGs in this folder, Chrome 156.0.8078.80 headless (renderer.txt); checked by eye, no overlap or cut-off text.
7: e7.txt, e7-session-start-sec4.txt. All greps pass.
Verdict: VERIFIED.
