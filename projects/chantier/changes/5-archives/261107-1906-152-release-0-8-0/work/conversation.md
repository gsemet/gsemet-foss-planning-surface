# Conversation excerpts: batch-08

Excerpts of the user's talk with the Chief of Staff during batch-08, translated from French. Use
them as captures; anonymise as docs/release-process.md says before rendering.

## Adding work to a paused batch

> **User:** Raise the budget to 50 and launch them.
>
> **Chief of Staff:** Done: batch-08's budget is now $50 and both P1 CRs are running, each with
> its Driver. CR-150 docs-lifecycle, round 1, $0.51. CR-151 release-notes, round 1, $0.26.
> $35.90 spent of $50. Heartbeat every 30 minutes; as soon as a Driver hands back its PR, I send
> it to you for review and merge.

## A PR handed back

> **Chief of Staff:** CR-150 (docs-lifecycle) is ready: PR #87, "docs: describe the batch
> lifecycle, both steerings and one use-case document per configuration". CI green on all 4
> checks (`just check` on Linux, macOS and Windows, and `just scenario`), mergeable. One round,
> approved by the Inspector, verified on the 7 evidence items of the specification.
>
> Will you merge PR #87, or do you want changes?

## A merge, then a rebase handled by the Driver

> **User:** 87 merged
>
> **Chief of Staff:** CR-150 is done: merge recorded, CR archived, worktree and branch removed,
> `main` up to date. PR #88 (CR-151) now conflicts with `main`, as expected, on the README. I
> asked its Driver to rebase it, run its gates again and push; I send it back to you once its CI
> is green.

## The grill, in plain words

> **Chief of Staff:** The release 0.8.0: what may the Release driver do alone? The irreversible
> actions are merging the version PR, the tag and publishing the GitHub release.
>
> **User:** Approval at each step.
