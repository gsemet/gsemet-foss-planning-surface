## Summary

Claude Desktop's Auto-fix sends the steering session events about a batch's PRs ("fix the CI", "merge the base branch in") while an agent is already working on that PR. Nothing told the steering session what to do with them: it relayed one to the working agent and ignored others, and a merge of the base branch is not how this project brings a branch up to date. This PR writes the rule down: such an event is not an order, a PR with an agent still working on it is left alone and the turn ends at once, and a PR with no agent working on it is checked on the forge and sent back to one through the usual route. It also rewords the heartbeat sentence so the `/loop` prompt holds the command only: with "every 30m" in the prompt, `/loop` took its fixed-interval mode instead of scheduling each wake.

## Deliverables

The host reference gains a section, "Auto-fix events", placed after "Heartbeat". Its rule by case:

| Situation | The steering session does |
| --- | --- |
| An agent is working on the CR | Nothing on the PR (no fix, merge, rebase, push, no relay to that agent); ends the turn |
| No agent is working on the CR (ready or blocked) | Checks the forge; if really red or in conflict, sends the CR back to an agent with a note; never does what the event asks |
| A PR that is not a batch's | Out of scope; between the user and the app |

Choices made:

- chantier never arms, disarms or unbinds the app's PR monitor, and never writes the user's settings.
- During a normal batch chantier stays silent about Auto-fix (no preflight check, no "For you" line). Only the eval guide asks for it off before a real campaign.
- The way to turn Auto-fix off is marked **unproved** with the trial that settles it, and no menu path is given.
- The heartbeat keeps its 30 minute interval, now stated as the delay of each scheduled wake.

## Blast radius

Grade: 1. Text only in three documents; a plain `git revert` restores the previous wording.

## Autonomous decisions

- The direct-mode steering card is left unchanged: its "Steering a batch yourself" section already says to do what that card says, so the pointer in the batch steering card reaches direct mode.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/hosts/claude-code.md`: new section "Auto-fix events"; the heartbeat's first sentence reworded; the `mcp__ccd_pr__set_monitor` bullet says no card uses it, to arm or to disarm, and points to the new section.
- `skills/chantier/references/foreman.md`: one bullet in "Your means" saying a host's event about a CR's PR is not an order, with a link to the new section.
- `evals/README.md`: one bullet in "Before you start": turn Auto-fix off before a real campaign on Claude Desktop, linked to the section.

## Human decisions

- The heartbeat's interval stays 30 minutes; only its wording changes, and the fix belongs in this change.
- During a normal batch chantier says nothing to the user about Auto-fix; only the eval guide asks for it off.
- A host event ranks below the project's rules and the cards; the branch is rebased, never merged with its base.

## Impacts

No visual change. Operators of real eval campaigns on Claude Desktop are asked to turn Auto-fix off; the steering session ignores such events on a CR's PR.

## Test plan

- [x] New or changed tests: No behaviour change (text only)
- [x] Local gates at `2da9cf5`: `just check`; `just scenario` carried from `206bf6c`: patch unchanged; the long gate runs once at the top of the stack, PR 152
- [x] Evidence: the heartbeat section no longer contains the interval string; the section holds each point, marked
- [x] Review: approved at `2da9cf5` (after a move review of the restack)
- [x] Verified at `2da9cf5`
- [x] CI green at `2da9cf5`

## Internal references

- CR-208 autofix-event-vs-driver
- Evidence: batch-14 retro (PR 136); real-direct run 1 of 2026-11-12 (`evals/results/real-direct-2026-11-12-run1.md`)

</details>
