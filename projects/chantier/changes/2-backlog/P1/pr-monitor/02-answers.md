---
type: cr-answers
description: The user's answers to the grill of the live view of a batch's pull requests.
---

# Answers

## pr-monitor-Q1: where it shows

2026-11-16, the user chose: the web board. A page of the board (`chantier board`) shows each
pull request of the running batch with its CR, its state on the forge (open, draft, merged,
conflicting, checks running or green) and whether it is ready to merge now, refreshing by itself
(about every 10 s; one forge request for all the batch's PRs per refresh, about 360 an hour, far
under GitHub's 5,000 an hour).

## pr-monitor-Q2: reading the forge

2026-11-16, the user chose the recommended answer: a named exception. Today the CLI never reads
the forge (the agents do, with `gh` and `glab`) and needs no network. AGENTS.md names one more
exception: this view reads the forge, read-only, with `gh` or `glab`, and needs the network; the
rest of the CLI does not change.

## pr-monitor-Q3: once every PR is merged

2026-11-16, the user chose the recommended answer: the view shows its final table with "all
merged" and stops refreshing by itself.

## pr-monitor-Q4: a merge the view sees

2026-11-16, the user chose: it signals it. The view changes nothing in the batch, but leaves a
line the Chief of Staff reads at its next heartbeat to record the merge (the Chief of Staff still
records it). Today the board never edits a batch and never messages an agent (AGENTS.md): this
signal is a second named exception for the board, to be said in AGENTS.md with the first.

## The specification's open questions (first run), 2026-11-16

The spec-writer noted that the CLI already calls `gh`/`glab` in `forge-stack` and `ship`'s draft
read: Q2's exception is worded as the board's own (it reads the forge on a timer, no agent
asking).

- Q5, the user chose the recommended answer: in Foreman mode too, the Chief of Staff sees the
  line and records the merge at its own next `status`; the Foreman does nothing more, no extra
  message.
- Q6, the user chose the recommended answer: "ready to merge now" needs both the record (the CR
  ready to merge) and the forge (open, not a draft, not conflicting, checks green), the Chief of
  Staff's own rule for "you can merge it".
- Q7, the user chose the recommended answer: a PR closed without a merge counts as done; the
  final table says "all done", with each PR's end.
- Q8, the user chose the recommended answer: after the final table the page keeps reading the
  local record (no forge); a new PR in the batch starts the forge refresh again by itself.
- A picture of the page in docs/web-board.md: the Chief of Staff's decision, none for now (the
  demo has no forge; a fake forge read is not worth it).

## The spec critic's questions, 2026-11-16

- Q9, the user chose the recommended answer: while the forge has not computed a PR's
  mergeability (GitHub's UNKNOWN after a push or a neighbour's merge), or its checks have not
  started, the row says "being checked by the forge" and the PR is not ready; "no checks" counts
  as ready only when the forge says the repository has none.
- Q10, the user chose the recommended answer: Q5 stays; when nothing runs (no heartbeat, the
  batch-18 case), the row says "merged on the forge, not recorded yet: tell the Chief of Staff",
  and the docs say so.
- Q11, the user chose the recommended answer: two CRs. This CR (pr-monitor) is the read-only PRs
  page (route, view, the forge-read exception in AGENTS.md, docs). The merge signal
  (`board-seen.jsonl`, the `status` line, the two cards, the second AGENTS.md exception, Q4, Q5,
  Q10) is its own CR, `pr-merge-signal`, after this one.
- Q12, the user chose the recommended answer: the page shows the batch the Batch view shows,
  running or paused; after the close it says "no batch running" and names the last batch.
- Q13 (pr-merge-signal's open question), the user chose the recommended answer: in a stacked
  batch, a PR merged into the PR under it (another CR's branch) is signalled, with its branch in
  the line; the Chief of Staff does not record it as merged, tells the user where it went, and
  waits until the PR under it lands.
- The critic's text fixes (the sidebar count from the record, the merged-into branch and the
  unproved native-stack and GitLab reads, the AGENTS.md wording matching the read rule) are the
  spec-writer's.
