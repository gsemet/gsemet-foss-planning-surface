# Verify CR-449 (description-only pass)

Head: 292ae731965dc529fe414a7be02c27cdf4f5de8f

VERIFIED

Earlier code and browser claims were judged at fb80d194 and eeca3f87 (VERIFIED at eeca3f87); they are carried
from eeca3f87 because the only move, 292ae731, touches the scenario only (claim 1).

1. Delta eeca3f87..292ae731 (292ae731): `git diff --stat eeca3f87 292ae731` gives `scenario/README.md | 2 +-` and
   `scenario/run_scenario.py | 6 +++---` (4 insertions, 4 deletions): the welcome check 22 ops/7 topics -> 26/8, text only.
2. The counts are true (292ae731): `python -c "from chantier.board.api.protocol import OPS,TOPICS;print(len(OPS),len(TOPICS))"` prints `26 8`.
3. Description at 292ae731 (`gh pr view 428 --json body`): SHA marks are the head `292ae73` or carry their reason
   (`fb80d19` for the screenshots, `3d5f28d` for the review, `eeca3f8` for eval-dry-run, whose later commit is scenario-only).
   Summary, Deliverables and Changes match the diff; Known gaps lists the unproved and cosmetic items, not "None".
   The two placeholder boxes (Verified, CI green) are intentional.
4. Images: the five PNGs exist in the planning folder's evidence and in commit aaf12b78 of the planning surface
   (`git ls-tree aaf12b78 ...evidence/` lists all five); they were looked at in the earlier pass (made-up paths).
5. Review box: `chantier log 449` holds `r4 inspector approved at 3d5f28d4`, the SHA the box cites as carried from.

## Final description pass at 292ae731965dc529fe414a7be02c27cdf4f5de8f

Head: 292ae731965dc529fe414a7be02c27cdf4f5de8f

- `gh pr view 428 -R gsemet/chantier --json headRefOid,body`: head is 292ae73; body equals work/pr-body.md except a trailing newline (diff output: `100a101`). Test plan boxes "Verified at 292ae73" and "CI green at 292ae73" are ticked.
- `gh pr checks 428`: check macos/ubuntu/windows, eval-dry-run, scenario ubuntu all pass.

VERIFIED
