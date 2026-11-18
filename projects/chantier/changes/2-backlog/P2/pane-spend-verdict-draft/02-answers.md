Short name: `pane-spend-verdict`

# Answers

1. The Chief of Staff, 2026-11-15, filing (`intake/request.md`): one pane change grouping three
   display points: the spend's age in the CR board pane and the web board; the `STATUS.md` now
   line of a PR in draft (`notify()`) in the ready line's wording; a "Verdict carried from
   <sha7>" step. Later, not for that release.
2. The Chief of Staff, 2026-11-18 (spec-writer's brief): the user asks no questions. A point that
   is done at `main` is scoped out. The AGENTS.md pane screenshot rule applies: the PR names "no
   screenshot of the pane from a real session" under Known gaps until the user gives one. Do not
   overlap CR-369 (`open-empty-batch`, batch-28), which also touches the pane and STATUS.json
   (`crs_total`).

## Settled by the spec-writer (2026-11-18)

Points with no user-visible behaviour of their own: they follow from the answers above and the
code at `main`.

- Done at `main`, scoped out: the age in `status`, `4-batch/STATUS.md` and STATUS.json
  (`spent_at`, CR-279); the web board's Costs page "Last computed" line; the ready line's wording
  (CR-277); `ship`'s `Carried` step (`a0918624`).
- The age's words are the ones `status` already prints (`<n> min old`, `age unknown`, nothing
  while the spend is unknown). The web board reuses its own time words (`age()`, as the Costs
  page's "Last computed: <age> ago"). No new wording is invented.
- The pane reads the age from the index's `spent_at`, which is already in STATUS.json. The web
  board reads it from the batch payload's `cost_at`, which already follows the live figure the
  board lays over the record (`model/live.js`), so the age is always the age of the figure shown.
  No new STATUS.json field and no `SCHEMA` bump.
- The now line and the ready line come from one helper, so they cannot disagree. The next line of
  a PR in draft stays as it is.
- The verdict's step is made from the ready `handback` event's `verdict_from`. That key is recorded
  whenever the verdict carried, whether `ship` proved it (a `carry` event) or the hand-back did.
  It has the form of the long gate's step: name `Verdict`, verdict column `carried from <sha7>`.
  The pane then shows the head in its Verdict column, with no change to the pane's code.
- With CR-369: when `spent_usd` is null nothing is added to the title line or the board figures,
  so CR-369's `none yet` / `no CR yet` drawing is untouched. The two CRs edit the same functions
  (`Batch` in `hooks/register.tsx`, `ChantierBatch` in `types/index.d.ts`, `figures` in
  `home-batch.js` and `batch.js`); whichever lands second rebases on the other, with no
  behaviour in common.
