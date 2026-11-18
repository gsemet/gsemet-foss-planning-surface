# Answers: board-prs-filter-sort

## prs-Q1: filters and sorts
**Answer (A):** filter by batch and by state (open, merged, draft); sort by opening date, last
activity or CR number; the choice is kept in the URL.

## Settled by the Chief of Staff
- The page's title, labels and tags say "MR" when the project's forge is GitLab, "PR" otherwise,
  in every language.
## prs-Q2: the forge read when the batch shown changes
**Answer (C):** read the forge at once on each change of batch, and widen AGENTS.md's PRs-page
rule accordingly ("the batch shown"; a change of batch reads at once, the 10 s limit applies to
the polling of the batch shown).

## Settled by the Chief of Staff
- The spec's other open questions take its working choices: "closed" PRs show under "all"; today's
  order is the default sort, dates newest first, CR numbers ascending; a row shows the date it is
  sorted by; GitLab is also recognised from the `origin` remote's host; "MR" applies wherever the
  board says PR (Home, Batch, overview, events); one batch at a time.
- The critic's one-line fixes 2 to 13 apply, with `mr.open` as the shared key scheme and `!n`
  for an MR number, as in board-forge-links.
- With no batch running, the page shows the last closed batch's PRs, with the navigator, read once
  on the forge. `pv.none` stays only when there is no history at all. This is a change from
  today, not "as today".
- It stays one CR: the user asked for "MR" on GitLab in the same request as the PRs page. The
  spec names the risk in its Limits.
