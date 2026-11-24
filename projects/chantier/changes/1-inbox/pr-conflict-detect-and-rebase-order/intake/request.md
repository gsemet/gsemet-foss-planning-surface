# Detect PRs left in conflict by a merge and order the rebase

The server detects a batch's PRs or MRs that a merge leaves in conflict and sends the order to rebase them.

Split from `pr-conflict-rebase-order` (user, 2026-11-24, pr-conflict-Q1 A): after the forge hub works again for a running batch, a merge triggers a scan of the batch's open PRs or MRs; a PR the forge shows CONFLICTING is journalled, the watcher carries it, and the Foreman starts a rebase Driver (conflict-resolver, push with force-with-lease, then check, CI and Verifier again, which a new head voids).

Seen: after PR 459 and 460 merged (20:04 UTC), PR 457 (CR-481) became CONFLICTING/DIRTY and nobody was told; the board's PR page reads the state (board/prs.py) but no order follows. Depends on `pr-conflict-rebase-order`. To grill: the order's form, which PRs, how GitHub's late "mergeable" state is polled, what the Driver owes after the rebase.
