# batch-08

Opened 2026-11-22T09:27:11Z, closed 2026-11-22T10:41:45Z, parallel, steered by direct (the Chief of Staff), budget $30, final cost $7.81. [batch-08.json](batch-08.json)

## Completion

| CR | Subject | Result | PR/MR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| [CR-466](../261122-1001-466-release-v1-12-0/) | release v1.12.0 | merged | - | 0 | $1.47 |

## Cost

- Total: $7.81 of a $30 budget
- Chief of Staff, steering the batch $6.34 (81%), Drivers $1.47 (19%), workers $0.00 (0%)
- Most: CR-466 $1.47
- Chief of Staff, steering the batch: 13 wakes, context 166,508 tokens on average, 227,957 at its peak
- Driver chantier:release-driver with its workers: $1.47 (94 calls)
- Chief of Staff, steering the batch (outside the budget): $0.39 since the batch opened (7 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $0.00 since the batch opened (0 calls, 0 spec-writers, 0 spec critics)
- Chief of Staff, whole session: $268.92 ($7.81 of it in the batch's spend), context 130,397 tokens; not counted: 1 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)

## Retro

# Retro batch-08

## 2026-11-22 - CR-466 release v1.12.0 (batch-08), with the batch-07 points re-checked on chantier main 687a4723 (critic: kept 10, dropped 4)

- [project] CHANGELOG lines written without their PR number forced follow-up docs(changelog) commits on main (95d34013, 369e8bad) and a round of CR-463: the lifecycle guideline ("Code" bullet) asks for the PR number in each CHANGELOG line, added right after `ship`.
- [project] The GitHub "Update branch" button put merge commits into PR branches twice (#458, #462; rebase merges only), each costing a rebase round: the pull-request guideline forbids the plain button, and a static CI check fails a PR whose commits include a merge commit.
- [project] A green re-run of a real-window test was accepted as a pass (CR-460's D1, then red on main, fixed by CR-464), although ci.guidelines rule 9 forbids it: the Driver hand-back and the ready ask name, for each re-run, the filed flake item or the fixing CR; a failure in a test the CR added or touched blocks ready.
- [chantier] A release-driver that opens the release PR and hands back `ready <PR link>: waits for the merge` without `chantier ship` gets the CR recorded as released and merged and the batch paused (driver.py:292-299 treats a release with no PR as released; CR-466 "PR: none", merged 90 s before the real merge); the post-merge steps were never driven: `handback ready` on a release with no recorded PR is refused unless a release-published event exists, and the Release driver card says to `ship` the release PR first.
- [chantier] One release needed three release-drivers (the first spent its context in 4 minutes reading cards, the release guideline and images; the second waited with Monitor and was cut by the host with no hand-back event): the Release driver section points to the typed `pipeline` wait for the heavy run on main, waits only with a background shell, and reads the release guideline by section.
- [chantier] A replaced Driver can still act (batch-07: CR-457's old Driver drafted the ready PR #471 again; CR-465 had two Drivers and two verdicts): on main, `verdict` has no lease check, `gate` and `ship` accept a missing or ended lease, a `ready` on a blocked CR skips it, and `agents set` stops no old agent: check the lease on every Driver write, stop the old Driver on replace, and forbid forge writes after a hand-back in the card.
- [chantier] Asks are free text (batch-07: stack-ready-to-merge asks sent one PR at a time without a native stack, A-24..A-31; per-PR asks left unread after their merge, A-25..A-34): an ask records the CRs and PRs it covers, a stack batch's ready ask must name the native stack bottom to top, and `order merged` marks the asks covering that CR read.
- [chantier] `ship` never checks that a stack batch's branch contains the previous CR's head, and the stack-driver card relies on restack notes (batch-07: stack 439..445 not a git chain, two restacks): `ship` checks the ancestry, and the stack-driver checks with `git merge-base` before saying no restack is needed.
- [chantier] Orchestration was half of batch-07's spend ($118 of $236; 336 Foreman timer wakes at about 180k tokens of context); the Driver model is now set per role, but the Foreman still wakes on a timer: wake the Foreman on events, as the Chief of Staff's watcher does in direct mode.
- [chantier] The fixes since 2026-11-20 (leases, typed waits, writer inside the server, the uv sync rule) are on chantier main, but no release was cut since v0.14.0 (4fdf6fc9), so a project in plugin mode never gets them and a retro cannot name a version: cut a chantier release.
