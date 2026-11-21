# Verify CR-428

Head: d91edcf356b075f0358ca914facf5c00e4376bbd

All claims judged at d91edcf356b075f0358ca914facf5c00e4376bbd.

1. Drop destinations, inbox refusal, PR clause, formerly.json pr_draft reset, way back by `order add`:
   command `uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests/test_order_drop_to.py skills/chantier/scripts/cli/tests/test_came_back.py -q -p no:cacheprovider`
   output `36 passed in 21.20s` (log: work/gates/verifier-tests.log). The tests call the CLI's real commands in-process on states it built:
   drop to trash/ready/p2 with live False/True; name in use refused for p2 and ready; inbox refused for a queued, a working and a ready CR with PR, record unchanged
   (`"order drop never sends a CR to the inbox" in err`, EXIT_USAGE, test_order_drop_to.py:196); PR clause in 6 cases (close for trash, draft outside a stack, none in a stack);
   cancel's draft clause for P2 and ready; order add of a 3-ready CR keeps its number.
2. Cards: `git grep -n "never sends a CR to the inbox"` finds the CLI text and tests; `driver.md:1222` keeps `1-inbox` only as "from an older Foreman is the backlog's case", as the spec says; the card-content tests (`test_the_cards_name_the_way_back_of_a_moved_out_cr`) pass in item 1.
3. Review box: `chantier log CR-428` has "move a6ba9d3..d91edcf (conflict) inspector approved at d91edcf356b075f0358ca914facf5c00e4376bbd".
4. Long gate: work/gates/20261121-204537.log first line `gate CR-428 branch chantier/batch-30/cr-428-a-cr-taken-out-of-a-batch-goes-to-the-ba head d91edcf356b075f0358ca914facf5c00e4376bbd`; log shows `gate result=pass head=d91edcf3... command=just scenario`. CI per Driver note: `gh pr checks 403` green at d91edcf; `gh pr view 403` headRefOid = d91edcf356b0.
5. PR description (posted on the forge, `gh pr view 403 --json body`): sections render, no images; Summary, Deliverables and Changes match `git diff --stat origin/main...HEAD` (orders.py, declare/orders.py, moveout.py, orders_drop.py, release.py, cards, docs+SVGs, SCORECARD, scenario, tests); Known gaps "None" and no UNVERIFIED claim or missing evidence pair exists. The Test plan boxes still hold `<sha7>` placeholders and are unchecked: the PR is a draft, to be filled by the Driver at ready (noted, not a failure of content). No role name outside Internal references.
6. Before/after: no visual change; the before is the base's refusal-free `inbox` destination, shown by the Deliverables table and the changed tests; no image captured (before-after.md).

VERIFIED

## Description pass (PR #403 description as posted)

Head: d91edcf356b075f0358ca914facf5c00e4376bbd

- Posted body (`gh pr view 403 --json body`, headRefOid d91edcf) equals pr-body.md (diff: one trailing blank line only). Judged at d91edcf.
- Renders: sections, table, details fold, no images (none to check for username/home).
- Consistent with `git diff origin/main...HEAD --stat` (29 files): orders/declare/moveout/orders_drop/release, cards, docs+SVGs, scorecard, scenario, tests all listed; the other touched src files (came_back, closing, forge_stack*, records, history, status/write) are docstring/comment-only edits, covered by "docstrings".
- Known gaps "None": no UNVERIFIED claim or accepted failure found.
- Review box `approved at d91edcf`: `chantier log CR-428` has "move a6ba9d3..d91edcf (conflict) inspector approved at d91edcf356b0...".
- No STALE mark; no role names outside Internal references.

DESCRIPTION: VERIFIED

## Move pass: rebase d91edcf3 -> 0f3dd8ce onto main 33d10454

Head: 0f3dd8ceaf489ae95070e3f7dc63e6e263ea01ca

Judged at 0f3dd8ceaf489ae95070e3f7dc63e6e263ea01ca.

1. The move's patch change: `git range-diff 99fa847f..d91edcf3 33d10454..0f3dd8ce` shows commit 1 changed (`!`, comment/help/doc hunks in chief-of-staff.md, foreman.md, commands/forge_stack.py docstring, declare/orders.py help, merged with the base's new `hold` and `waits with held` wording), commit 2 identical (`=`). Read each hunk: the base's new text (hold for a live CR, dependents of an apart CR) is kept and the CR's wording (`trash|ready|P1..P4`, `3-ready`, backlog/next batch keep a draft) is applied; foreman.md drop paragraph names `6-trash`, `3-ready` or `2-backlog/P<n>`, no `1-inbox`. Remaining "inbox" hits (`git grep -n "to the inbox"`) are the refusal text (orders.py:240), moveout.py:71 history docstring, and the restore/triage paths, all as the spec allows.
2. Behaviour tests (claim 1 re-judged, the base touched orders): `uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests/test_order_drop_to.py skills/chantier/scripts/cli/tests/test_came_back.py -q -p no:cacheprovider` -> `40 passed in 21.23s` (4 more than at d91edcf: the base's tests). Inbox refusal still asserted (test_order_drop_to.py:196).
3. Review box / move note: `chantier log CR-428` shows driver ship at 0f3dd8c with conflict=True, the conflict-resolver hunks in work/conflict-resolver/conflicts.md; carried from d91edcf: the claims on PR description sections, no images, Known gaps "None" (the diff set is unchanged in kind: same files plus docstring merges). The Review box in the PR must cite the new head or `carried from d91edcf`; the Driver sets it at ready (not content of this claim).
4. Long gate at the new head: `chantier log CR-428`: `driver gate result=pass head=0f3dd8ceaf489ae95070e3f7dc63e6e263ea01ca command=just scenario run=20261121-221012-12744 base=33d1045...`. CI: `gh pr checks 403`: just check x3 (macos, ubuntu, windows), eval-dry-run, scenario all pass; `gh pr view 403 --json headRefOid` = 0f3dd8ceaf48...
5. Carried from d91edcf: cards test, PR description rendering, before/after (no visual change), since the move touched only comments, help text and card prose, judged in item 1.

VERIFIED

## Re-proof at the rebased head (conflict move d91edcf..0f3dd8c)

Head: 0f3dd8ceaf489ae95070e3f7dc63e6e263ea01ca

1. Drop behaviour (judged again at 0f3dd8c): `uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests/test_order_drop_to.py skills/chantier/scripts/cli/tests/test_came_back.py -q -p no:cacheprovider` -> `40 passed in 21.05s` (was 36: base brought 4 more came_back/order tests).
2. Long gate at this head: work/gates/20261121-221012.log first line `gate CR-428 branch chantier/batch-30/cr-428-a-cr-taken-out-of-a-batch-goes-to-the-ba head 0f3dd8ceaf489ae95070e3f7dc63e6e263ea01ca`; `chantier log CR-428`: `driver gate result=pass head=0f3dd8ce... command=just scenario`.
3. CI: `gh pr view 403 --json headRefOid,statusCheckRollup` -> headRefOid 0f3dd8ce...; just check x3 OS, just scenario, just eval-dry-run all SUCCESS.
4. Review box: `chantier log CR-428`: "move d91edcf..0f3dd8c (conflict) inspector approved at 0f3dd8ceaf489ae95070e3f7dc63e6e263ea01ca".
5. Cards/docs/before-after: carried from d91edcf: no visual change, card claims re-covered by the tests of item 1.
6. PR description (posted, `gh pr view 403 --json body`) FAILS: its Test plan names `d91edcf` for "Local gates", "Evidence", "Review: approved", "Verified" and "CI green", with no `carried from` reason, while the PR head is 0f3dd8c. Each proof must name the head or be carried with its reason. Fix: update those five lines to 0f3dd8c (or `carried from d91edcf: <reason>`).

NOT VERIFIED
