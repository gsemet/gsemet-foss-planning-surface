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
