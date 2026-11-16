## Summary

In a Foreman batch on Claude Code, Claude Desktop tells the session that started the Foreman each time the Foreman ends a turn. In a real run, ten such notices made the Chief of Staff (a large-context model) restate the quoted text and re-read its whole context several times: about $2.55 of steering, more than the Foreman's own $2.10. None of the notices carried an ask; every ask and the final report came as separate lines. This PR writes the rule into the cards: the Chief of Staff ends such a turn at once, with no tool call, no message and no report, except when the notice shows the Foreman stopped on an error. **UNVERIFIED:** that the Chief of Staff follows the rule (it needs a real Foreman batch).

## Deliverables

| Notice that alone started the turn | Chief of Staff |
| --- | --- |
| Foreman ended a turn | ends the turn at once: no tool call, no message, no report |
| Foreman stopped on an error (usage limit, API error), no line from it | one line to the user with the error as quoted, still no tool call |
| Notice together with a Foreman line or the user's message | handles that line or message as its card says |

- New section "The Foreman's turn-end notice" in `skills/chantier/references/hosts/claude-code.md`, after "Auto-fix events": what the notice is, the rule, the one exception, the cost.
- One bullet in `skills/chantier/references/chief-of-staff.md` ("While it runs") and one sentence in `skills/chantier/references/routing.md` pointing to it.
- New scorecard row J29 in `evals/SCORECARD.md`, read by hand in the next real Foreman campaign.

## Blast radius

Grade: **1** (cards, host reference and scorecard only; a `git revert` restores the previous behaviour).

## Autonomous decisions

None.

## Known gaps

- **UNVERIFIED:** the Chief of Staff follows the rule, and the steering cost saving. Unproved until a real Foreman batch shows it (no transcript of a turn started by a notice alone yet).
- The error exception is unproved: no such notice has been seen; it is tried when a Foreman stops on an error in a real batch.

<details>
<summary>Details</summary>

## Changes

- `hosts/claude-code.md`: the new section (what it is, a notice is not a line, the rule, the error exception, a notice that arrives with a line, the cost, the mark).
- `chief-of-staff.md`: the "Foreman's turn end" bullet after "Status".
- `routing.md`: a sentence under the table.
- `evals/SCORECARD.md`: row J29.

## Human decisions

- Only notes that need the user (a question, a ready PR, the final report) make the Chief of Staff act; a Foreman's turn end does not.
- One narrow exception: a notice showing the Foreman stopped on an error gets one line to the user, with no tool call, marked unproved.
- Starting the Foreman's session not linked is out of scope and left for later.

## Impacts

No visual change. In a Foreman batch on Claude Code, the cards now ask the Chief of Staff for no call on each notice. **UNVERIFIED:** the saving itself.

## Test plan

- [x] New or changed tests: No behaviour change in the CLI; cards and docs only
- [x] Local gates at `190b208`: `just check` (223 passed at the conflict resolution; clean rebase since)
- [x] Evidence: none; the behaviour needs a real Foreman batch
- [x] Review: approved at `32df20b`, carried from `32df20b` to `190b208` by a clean rebase
- [x] Verified at `190b208`
- [x] CI green at `190b208`: `gh pr checks 237`, all checks pass

## Internal references

- CR-292 cos-quiet-on-foreman-turns
- Evidence: real-foreman run 2 of 2026-11-15 (Chief of Staff transcript and audit)

</details>
