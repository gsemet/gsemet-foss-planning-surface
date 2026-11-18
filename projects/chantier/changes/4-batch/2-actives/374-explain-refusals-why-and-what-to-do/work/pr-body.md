## Summary

When the user asks for something a rule or the CLI will refuse, the Chief of Staff used to let them find out by trying, or after the refusal. It now says so at once, before any try: what is refused, why the rule exists, and what the user can do now. The user docs also wrongly said a running direct batch refuses `order add`; they now match the CLI.

## Deliverables

A new hard rule and a table of eight known refusals in the Chief of Staff's card (before, the card gave one line for a grill request):

| Row | What the user asks | Refused? |
| --- | --- | --- |
| A | a new idea, grill or QA while a direct batch runs | no grill in that session, `order qa` refused; a specified CR is queued by `order add` |
| B | a new CR with a release CR in the batch | refused only once the release has started |
| C | a subagent's file named `report...`, `summary...`, `findings...`, `analysis...` (Claude Code) | refused by the host on the name: use a number prefix |
| D | close the batch while something runs | `close` refused until it ends |
| E | the release procedure word with other CRs open | `order confirm` refused |
| F | a CR with no specification | `open` and `order add` refused |
| G | more work past the round limit | `round` refused |
| H | a model with no price | nothing refused; cost is a floor |

The direct-mode docs and the life-of-a-batch diagram now say a specified CR joins a running direct batch (`order add` queues it) and only `order qa` and the grill are limited. The rule for files written by subagents is stated as a rule (number prefix), not advice.

**UNVERIFIED:** the rendered look of the diagram's direct box (see Known gaps).

## Blast radius

Grade: 1. Cards and docs only; a `git revert` restores the previous text.

## Autonomous decisions

- Rows A to H were checked against the code; none needed correction.

## Known gaps

- No rendered screenshot of the diagram's direct box: line widths were checked by estimate only.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/chief-of-staff.md`: the hard rule "A refusal is said before it is met", the subsection "Refusals to say before they are met" (rows A to H), and the grill-request line of the direct-steering list.
- `docs/use-cases-direct.md`, `docs/tutorial-claude-code.md`, `docs/batch-lifecycle-texts.md`, `docs/batch-lifecycle.svg`: the running direct batch queues a specified CR; `order qa` and the grill stay limited.
- `skills/chantier/references/concepts.md`, `skills/chantier/references/hosts/claude-code.md`: the number-prefix rule for subagent files.

## Human decisions

- The code is the target for a running direct batch: the docs are corrected, the refusal is not brought back.
- The host's refusal of some subagent file names is not the auto-mode classifier; the fix is a number prefix.
- Eight refusals are covered (A to H); two audit cases stay in the host references.

## Impacts

No visual change besides the diagram's direct box text; no CLI change.

## Test plan

- [ ] New or changed tests (they fail on the previous code) No behaviour change
- [x] Local gates at `4e0de99`: `just check` (635 passed)
- [ ] Evidence: the git greps of the specification, at `4e0de99`
- [x] Review: approved at `4e0de99` (reviewed at c0bb193 plus this commit)
- [ ] Verified at `4e0de99`
- [ ] CI green at `4e0de99`

## Internal references

CR-374 explain-refusals-why-and-what-to-do (batch-28).

</details>
