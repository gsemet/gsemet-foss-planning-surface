# The CR board pane shows the spend's age, the carried verdict and the draft wording

Three display points that the specifications of batch-18's fixes left out, grouped into one pane
change. The group means one `just mod` and one screenshot from a real session (AGENTS.md):

1. **The spend's age** (from `spend-fresh-at-budget-check`, CR-279, open question 2). `status` and
   `STATUS.md` now say how old the spend figure is. The CR board pane and the web board show the
   figure with no age, so a reader cannot tell a fresh figure from one recorded hours ago.
2. **The draft wording** (from `stacked-ready-line-names-cr`, CR-277, open question 1). The ready
   line of a `PR in draft` hand-back now says the PR's own draft state on the forge and the CR (and
   PR) it waits on. The CR's now line (`STATUS.md`, its `STATUS.json`, the pane's CR page) still
   reads `PR in draft: <pr> on <base>, waits for <cr>.`, which reads like "this PR is a draft on
   main", the misreading CR-277 removed from the ready line.
3. **The carried verdict** (from `clean-rebase-light-verify`, CR-290, open question 1). A verdict
   carried over a clean rebase shows as its own step on the CR's page (`Verdict carried from
   <sha7>`), next to the long gate's `carried from` step.

Checked against `main` on 2026-11-18 (`3a9afc2c`). Some of this is already done:

- Spend's age: done in `status`, `4-batch/STATUS.md` (`as of <time>`) and both STATUS.json files
  (`spent_at`), and the web board's Costs page shows "Last computed: <age> ago". Still missing:
  the pane's batch title line, and the web board's home batch card and Batch page.
- Draft wording: the ready line is done (CR-277). Still missing: the now line (`status/words.py`
  `notify()`).
- Carried verdict: partly done. Since `a0918624`, `ship`'s `carry` event gives a `Carried` step
  whose note says `long gate and verdict from <sha7>`. `STATUS.md` shows that note; the pane drops
  every step's note. The hand-back adds a `Long gate | carried from <sha7>` step, but no step for
  the verdict. Still missing: the verdict's own step at the hand-back.

Source: filed 2026-11-15 by the Chief of Staff from those three open questions, which a Fable
advisor sorted as "later, not for this release". Specified 2026-11-18 at the Chief of Staff's
request; the user asks no questions.
Short name: `pane-spend-verdict`
