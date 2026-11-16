## Summary

In a recent real run, three agents wrote "no CI" in their hand-backs and PR bodies while a `test` check ran green on every PR. The claim came from somewhere other than the forge, most likely from a look taken before the forge had registered the checks. This change makes every claim an agent makes about CI come from the forge's list of checks for the PR, read at the head it pushed, and makes "no CI" need a second empty look a minute after the push.

## Deliverables

The CI rules in the Driver card, before and after:

| | Before | After |
| --- | --- | --- |
| Source of a CI claim | unspecified | the forge's checks for the PR at the pushed head (`gh pr checks`, `glab ci list`) |
| Project says "no CI" | could be taken as the claim | the forge's list is still read; a contradiction is said in a `note` |
| Head | not checked | the PR's head on the forge must equal the pushed head before reading |
| "No CI" | after one look | only after a second empty look a minute after the push (one bounded wait at most, never a loop) |
| Note / PR box | free text | names the command and the 7-character head; `No CI: no check listed at <sha7>` for an empty list |

Choices: the rule sits in the common `CI:` bullet, so it binds every agent that pushes; the one bounded wait is a named exception to the "no sleep, no polling loop" rule; the CLI is untouched.

## Blast radius

Grade: **1**. Card text and one scorecard row only; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- Left out the optional line in the PR template's rules section: the CI item's comment already carries the form.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: the `CI:` bullet gains the only-source, rules-do-not-replace-the-look, head-first, two-looks, one-bounded-wait and note rules; nothing of the bullet's text is removed.
- `skills/chantier/references/concepts.md`: rule 8 points to that one bounded wait.
- `skills/chantier/references/pr-template.md`: the CI Test plan item gets the `No CI: no check listed at <sha7>` form.
- `evals/SCORECARD.md`: row J25, marked by hand.

## Human decisions

- The forge's list is the only source, even when the project's rules say it has no CI; the rules only say how to judge the list.
- "No CI" needs a second look about a minute after the push; if the other work ends sooner, one bounded wait, once, never a loop.
- The rule binds every agent that pushes.
- With no check listed, the PR body's CI box stays, checked, and reads `No CI: no check listed at <sha7>`.
- No CLI change, and the Verifier's card is unchanged.

## Impacts

No visual change. Agents that push will read the forge's checks at the pushed head before claiming anything about CI.

## Test plan

- [x] New or changed tests (they fail on the previous code): No behaviour change (cards and docs only)
- [x] Local gates at `99113b7`: `just check` pass; `just scenario` carried from `01e1288`: patch unchanged; the long gate runs once at the top of the stack, PR 152 (586/586 on GitHub and on GitLab at `01e1288`)
- [x] Evidence: none, a card-only change with nothing visible
- [x] Review: approved at `01e1288` (carried to `99113b7`: patch unchanged by the restack)
- [x] Verified at `99113b7`
- [x] CI green at `99113b7`: `gh pr checks 142` lists 5 checks (just check x3 OSes, eval-dry-run, scenario), all pass

## Internal references

- CR-197 driver-ci-from-pr-checks
- Source finding: `evals/results/real-direct-2026-11-12-run1.md`, finding 1

</details>
