## Summary

A pull request's proofs (tests, review, verification, CI) were never tied to a commit, so after a rebase or a new round nobody could tell which proof still held. And the tool showed `$0.00` for a cost it had never measured. This change binds each proof to the commit it judged, marks claims with no proof, and shows an unmeasured cost as unknown.

## Deliverables

- Each proof in the PR names the commit it covers (seven characters). After the head moves, only what the move touched is judged again; the rest is carried over and says so. A proof the head has moved past is marked `STALE`; a claim with no proof is marked `**UNVERIFIED:**` or narrowed.

  | Test plan item | Before | After |
  | --- | --- | --- |
  | Local gates | "Local gates: ..." | "Local gates at `2651645`: ..." |
  | Review | "Review" | "Review: approved at `1540c75`; rebase onto `7d58b96` (conflict resolutions) re-inspected at `2651645`" |
  | Verified | (none) | "Verified at `2651645`" |
  | CI | "CI green" | "CI green at `2651645`" |

- A brand-new batch shows `spent unknown` (status line, the batch's status file, the dashboard) until its first priced refresh, then a dollar figure. A measured zero stays a number.
- While CI runs, the Driver does its other work first, then makes one long wait.
- For a project with a UI, the Verifier opens each screenshot and checks it shows what the PR claims.

## Blast radius

Grade: **1**. Card text plus three small display changes in the CLI; the budget rail behaves as before on an unpriced spend. A `git revert` restores the previous behaviour.

## Autonomous decisions

- The budget rail still lets a Driver start while the spend is unpriced (reads it as 0), as the specification's default says.
- No note records what ended the CI wait (specification default).
- The scenario's "priced" check runs after the `cost` check, because a refresh right after the batch opens has no pricing data yet.

<details>
<summary>Details</summary>

## Changes

- Cards: the Inspector's reply gains a `head` field; the Verifier's report carries `Head:` and a SHA per claim, with a delta assessment after a move; the CR driver records the approved head, feeds the previous report and the move to each later Verifier, and re-inspects a changed patch after a rebase; the stack driver judges again what a restack touched; the PR template gets the SHA, `STALE` and `UNVERIFIED` rules; one sentence in the evidence rule; one bullet in the report rules.
- CLI: `spent_usd` starts empty on a new batch; `status`, the batch's status file and the dashboard print `unknown` while it is empty; a live CR with no recorded time is left out of the "longest silent Driver" line instead of counting 0 minutes; the budget messages name an unknown spend as `unknown`.
- Scenario: two new checks, before and after the first priced refresh.

## Human decisions

- Only what a move touched is judged again; the PR names the SHA of each proof and marks a stale one.
- The visual check is the Verifier's: no new role.
- CI wait: other work first, then one long wait; no measure, no CLI tool.
- An unproven claim is marked `UNVERIFIED` or narrowed; an unobserved cost or time is unknown, never 0.

## Impacts

No visual change. Reports and PRs name the commit of each proof; a fresh batch shows `spent unknown`.

## Test plan

- [ ] New or changed tests (they fail on the previous code): two scenario checks on `spent unknown` and the priced figure
- [ ] Local gates at `2651645`: `just check`, `just scenario`
- [ ] Evidence: before at `7d58b96`, after at `2651645`: before/after of `chantier status` on a fresh batch (`spent $0.00` then `spent unknown`)
- [ ] Review: approved at `1540c75`; rebase onto `7d58b96` (conflict resolutions) re-inspected at `2651645`
- [ ] Verified at `2651645`
- [ ] CI green at `2651645`

## Internal references

CR-168 proof-bound-to-head.

</details>


