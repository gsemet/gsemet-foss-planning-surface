Head: 1ed038919603387200db21974d264e450ef80b68

Description pass of PR 319 (gh pr view 319, headRefOid = the head above). No verdict recorded.

- t3.json quoted = file at head (cat t3.json): equal. Judged at 1ed0389.
- SVG quoted = docs/logo.svg at head (cat; wc -c = 520): equal. Judged at 1ed0389.
- Changes match diff (git diff --name-status origin/main...HEAD): A docs/logo.svg, A t3.json only. Judged at 1ed0389.
- Image link: curl -sL -> 200 image/png; bytes identical to evidence/logo-256-and-16px.png; opened: logo 256 px and 16 px, no path or username. Judged at 1ed0389.
- Test plan: just check 578 passed (work/coder/r1.md; driver note "before first push at 1ed0389: just check: pass"); Review approved: log notes "committed as 1ed0389; inspector approved"; CI green: gh pr checks 319, all 5 jobs pass; Verified at 1ed0389: previous verify.md VERIFIED at the head.
- Known gaps "None": no UNVERIFIED claim in the closing note. No STALE mark. No role name outside Internal references.

VERIFIED
