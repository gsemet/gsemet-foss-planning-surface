## Summary

A Driver spent a large part of its context on opening reads (the cards, the project's rules, the specification) before it started its first worker, about 50k to 58k tokens measured on earlier batches. The Driver card now says what a Driver reads whole, what it reads by section and when, and what it leaves to its workers, and the prompt template and the host reference say the same. The aim is an opening about a third cheaper, with the Driver still judging what it needs.

## Deliverables

Where a Driver's opening read goes, before and after (cards only, no code):

| Read | Before | After |
| --- | --- | --- |
| `driver.md` | whole | top, "Your means" and its own section |
| `concepts.md` | whole | "Starting an agent" before the first worker; "Escalation" and "Words" entries only when named |
| `hosts/claude-code.md` | whole | "Tools", "Auto mode", "Compacting", "The write guard", when the step comes |
| `pr-template.md` | at the opening | when `pr-body.md` is written |
| Project's rules | every listed file | the instruction file whole, the others only what touches a Driver's work |

The new paragraph in `driver.md` ("Opening reads") is the card's defaults, not a gate: a rule not read still binds, and a step not covered by what was read is read before it is acted on.

Before measure, on the five first Drivers of the batch that started before this change (opening cost: the prompt of the first call that starts a worker, minus the prompt of the first call): 64.3k, 87.5k, 52.9k, 41.9k and 42.0k tokens, mean 57.7k and median 52.9k (mean 61.6k without the Driver that wrote this change and already read by section). The target is an after mean of about two thirds of it, about 38.5k to 41k. The after figures come from the batch's transcripts after the merge (see Known gaps).

## Blast radius

Grade: **1**. Only reference cards change. `git revert` restores the previous reading rules.

## Autonomous decisions

- The "Opening reads" text is a paragraph with bullets placed under the card's top paragraph (the specification allowed either), so the card's first lines stay as they were.
- The worker's read line in the prompt template is written with `worker.md` instead of the `<driver|worker>` placeholder, so the two lines sit one under the other; a worker's reading is unchanged.

## Known gaps

- The after measure of the opening cost and the check that no rule went unread come only at the batch's close, after the merge.
<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: the "Opening reads" paragraph at the top; the "ready to merge" link now names the section "Words".
- `skills/chantier/references/concepts.md`, "Starting an agent": the prompt template shows a Driver's read line and a worker's read line.
- `skills/chantier/references/hosts/claude-code.md`, "Who reads it, when": the Foreman reads the file with its card; a Driver reads the sections its card names, when the step comes.

## Human decisions

- The target is about a third less than the roughly 58k tokens of opening reads, measured before and after on a batch's transcripts. The Driver reads whole only what it judges it needs and leaves the rest to its workers.

## Impacts

No visual change. Drivers started after the merge read less at their opening.

## Test plan

- [x] New or changed tests: No behaviour change (cards only)
- [x] Local gates at `d43abe1`: `just check` (in the worktree) pass; `just scenario` pass (github 895/895, gitlab 873/873)
- [x] Evidence: before measure at `ce00ec3` in Deliverables; the after measure comes after the merge
- [x] Review: approved at `d43abe1` (the pass was recorded on the reviewed state, committed as `d43abe1`)
- [x] Verified at `d43abe1`
- [x] CI green at `d43abe1`: `gh pr checks 201`: just check (3 systems), eval-dry-run, scenario pass

## Internal references

CR-260 driver-opening-reads. Specification: `.agents/changes/4-batch/2-actives/260-driver-opening-reads/03-change-spec.md`.

</details>
