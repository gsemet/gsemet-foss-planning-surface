## Summary

The cards fixed one merge path per batch shape: a stack batch could only end in one merge of the whole stack from its top PR. In practice the user merges a PR at a time, as each one is ready, and the cards had no rule for it, nor for a Driver whose PR was merged while it was still finishing.

This change makes a merge possible at any moment, one PR at a time, in every batch shape (parallel, series, stack). A PR whose CR was handed back `ready` on the default branch is mergeable now. A stack made on the forge may still be merged in one action from its top PR, or one PR at a time from the bottom, merge by merge. "You can merge" is said only after the `ready` line, and a Driver whose PR merged under it ends cleanly. The README, the use-case docs, `CONTRIBUTING.md` and the diagrams say the same.

## Deliverables

What the cards now say, by role:

| Card | Change |
| --- | --- |
| `concepts.md` | "Ready to merge" holds in every mode; a verified stack is a second way, not the only one. The Stack paragraph offers the one-PR-at-a-time merge beside the one-action merge. |
| `chief-of-staff.md` | A `ready` ask on the default branch is offered as mergeable now; "you can merge" only after the `ready` (or `stack-ready`) line; a merge before that line is recorded as any merge, with no reproach; the stack and series paragraphs and the plan at the go no longer fix the merge path. |
| `foreman.md` | After a merge in a stack batch the Foreman chooses per merge between a restack and rebase notes; a Driver's "merged: no Driver to hand it back" line is neither an anomaly nor an ask. |
| `driver.md` | A hand-back refused with `<cr> is merged: no Driver to hand it back` ends cleanly: stop touching the PR, note what is left undone, pass the line up, end. The stack driver's opening names both merge ways. |

The docs: `README.md`, `CONTRIBUTING.md`, `docs/use-cases-foreman.md`, `docs/use-cases-direct.md` and the diagrams `docs/batch-modes.svg`, `docs/batch-pace.svg`, `docs/release-driver.svg` (with their `-texts.md`) now say that a ready PR is mergeable on its own and that a stack is merged in one action from its top PR or one PR at a time from the bottom, the release last. The v0.9.0 release notes are history and are left as they are.

The scenario pins the behaviour the Driver card relies on:

```python
w.chantier("order", "merged", cr)
w.chantier("handback", cr, "ready", link, expect=2)   # "is merged: no Driver to hand it back"
w.chantier("note", cr, "merged before the hand-back; left undone: none")  # accepted
```

## Blast radius

Grade: 1. Cards, docs and one scenario check only; no CLI behaviour or text changes. A plain `git revert` restores the previous wording.

## Autonomous decisions

- The Chief of Staff card does not quote the refused text of `handback`: it only covers the user's early merge, recorded with `order merged`. The Driver and Foreman cards, which meet the refusal, name the same text.
- The CLI's refusal moved to `driver_checks.py` in an earlier change; the scenario check reads the text from the CLI's output, not from its source.

## Known gaps

- The refusal text of `handback` is unchanged; the cards explain it.
- A few edited card lines are long or unevenly wrapped; left as cosmetic.
- The edited SVGs were checked as valid XML and by line length, not rendered.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/concepts.md`, `chief-of-staff.md`, `foreman.md`, `driver.md`: the wording above.
- `README.md`, `CONTRIBUTING.md`, `docs/use-cases-foreman.md`, `docs/use-cases-direct.md`, `docs/batch-modes.svg`, `docs/batch-pace.svg`, `docs/release-driver.svg` and the two `-texts.md`: the same wording.
- `scenario/run_scenario.py`: one check at the end of `handback_proofs`.

## Human decisions

- No merge path is fixed when a batch is started, in any shape: the user may merge each ready PR on its own, or a made stack in one action, as they choose, merge by merge.

## Impacts

The diagrams' wording changes (three SVGs); no layout change. Batches run with these cards follow a user who merges PR by PR without improvised notes.

## Test plan

- [x] New or changed tests: the scenario check in `handback_proofs`, passing at the pre-restack head (it pins existing CLI behaviour, so it does not fail on the previous code)
- [x] Local gates at the pre-restack head: `just check` and `just scenario` (github 696/696, gitlab 677/677 checks passed); the docs change touches no code, so it is gated by `just check` alone at the pre-restack head, as the project's rules say for docs
- [x] Evidence at the pre-restack head: reading pass of the cards; every remaining "one action" mention offers the one-PR-at-a-time merge beside it or refers to the merge action recorded afterwards, and `is merged: no Driver` is found in the Driver and Foreman cards
- [x] Review: docs review approved at the pre-restack head, committed as the pre-restack head
- [ ] Verified at `e894eb3` (restack onto main; pending)
- [ ] CI green at `e894eb3` (restack onto main; pending)

## Internal references

- CR-233 merge-any-time

</details>
