## Summary

A specification could ask for a check on a shipped file (a stylesheet, a script, a card) and still be satisfied by a test that only feeds a prepared text to the checker. Nothing in the cards told the spec-writer to say that such a check reads the shipped file, nor the spec critic or the inspector to ask for it, so a gap of this kind surfaced only rounds into a large change. This PR adds the rule to the three cards involved, so a specification says it, the critic asks for it, and the inspector checks it from round 1.

## Deliverables

Three cards change, one addition each:

| Card | Where | What it says now |
| --- | --- | --- |
| `spec-writer.md` | "Output", one bullet before the evidence bullet | When a check guards a shipped file, the evidence says the check reads that file as it ships, at the head under test. A prepared text is only for a case the shipped file cannot hold (a refusal, a broken input), named as such and paired with a check on the shipped file. |
| `spec-critic.md` | "What you look for", end of kind 1 | Evidence that guards a shipped file but reads a copy or a prepared text where the shipped file would do counts as a gap with the request's intent. There is still no fifth kind. |
| `inspector.md` | "Your part", one paragraph after the host and default matrix paragraph | From round 1, a named test that guards a shipped file must read it as it ships; a missing one, or one on a prepared text alone, is `blocking`. |

Reading check (replayed by hand, not run as a test):

- The board design-system specification's test section (section 8) reads the real sheets and scripts under the board's web folder for its "one card", "tokens only" and component-sheet checks, and pairs them with one parametrized test of small prepared texts for the refusals. That is exactly the shape the new bullet allows: it meets it.
- A check written for this PR: "a test feeds `.card { padding: 10px }` to the checker and asserts it refuses", with no check on the real stylesheets. The critic's kind 1 would give the one-line fix: "add a check that reads the shipped stylesheets from the repository at the head and asserts the same rule; keep the prepared text for the refusal only."

## Blast radius

Grade: **1**. Cards only; no CLI, hook, agent file, test or doc changes. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

None.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/spec-writer.md`: one bullet in "A rich specification holds".
- `skills/chantier/references/spec-critic.md`: one sentence at the end of kind 1.
- `skills/chantier/references/inspector.md`: one paragraph in "Your part".
- The agent files of both hosts only name the cards, so they are unchanged.

## Human decisions

- Cards only: no CLI rail, lint or new test, since a test asserting that a sentence is present would guard wording, not behaviour.
- The critic keeps its four kinds; this sorts under the first, as a fix sent back to the spec-writer.
- The inspector, not the coder or the verifier, carries the check, from round 1.

## Impacts

No visual change. Specifications written after this will name the shipped files their checks read, and reviews will enforce it.

## Test plan

- [x] No behaviour change in code; the structure tests load the cards
- [x] Local gates: carried from `b69d4b1` (`just check` pass, 565 passed, run on the round's tree before the commit; clean rebase onto CR-348, head `3eb8a04`)
- [x] Evidence: none (no visible change)
- [x] Review: carried from `b69d4b1` (approved at `ef9f979`; clean rebase onto CR-348, head `3eb8a04`)
- [x] Verified: carried from `b69d4b1` (clean rebase onto CR-348, head `3eb8a04`)
- [x] CI green at `3eb8a04`: all five jobs pass, including the scenario job

## Internal references

- CR-349, batch-24; specification `349-spec-checks-on-shipped-files/03-change-spec.md` (decisions sc-Q1 to sc-Q6).

</details>
