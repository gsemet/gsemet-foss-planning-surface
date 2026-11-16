## Summary

Three gaps in chantier's reports. A batch that ends without a release got no retro, so its problems were never offered back to the user. The cost reports showed one "Chief of Staff (steering)" line that read as if steering alone cost half a batch, when much of it was grilling and specifying with the user. And `status` and `STATUS.md` said "steering foreman" on a batch steered in direct mode, and nothing said whether PRs were stacked or independent.

## Deliverables

A retro now comes at every pause (every CR merged or cancelled) and at every release, written in `4-batch/retro.md`, one line per problem with its long-term fix; the Chief of Staff numbers the points in the Completion report and offers each as an inbox item before `close`.

The Chief of Staff's cost splits in two, measured call by call from its transcript (nothing estimated):

```text
Chief of Staff, steering the batch: $x (n calls)                       <- in the spend and budget (direct mode)
Chief of Staff, grill and specifications with the user (outside the budget): $b since the batch opened (n calls, k spec-writers)
Chief of Staff, whole session: $d, context n tokens; not counted: k compactions since the batch opened ...
```

A turn that names a CR's `01-intent.md`, `02-answers.md`, `03-change-spec.md` or `work/specifying`, or starts a spec-writer, is grill and specifications, as are the spec-writers' own calls. A part that cannot be measured prints `unknown` with its cause (Copilot, no transcript, calls with no time).

`status` and the batch `STATUS.md` header now say who steers and the shape (parallel, series or stack), for example `steered by the Chief of Staff (direct mode) - independent PRs (parallel)`; a `batch.json` with no `steering` shows `unknown`, and `STATUS.json` holds `null`.

## Blast radius

Grade: 2. The CLI's cost arithmetic and the `status` output change, and a direct batch's spend drops by the grill turns (they leave the budget, as the spec-writer already did). Revert restores the old figures and wording; no stored data format changes beyond `null` for an unknown steering.

## Autonomous decisions

- A turn is attributed whole to grill and specifications when any of its tool uses matches; a steering turn that merely reads a specification counts there too (the specification's rule).
- In direct mode the "steering outside the budget" line is printed only when the Chief of Staff spent something outside its claim window.
- Calls with no timestamp are in neither share and are reported as "not placed".

<details>
<summary>Details</summary>

## Changes

- `costs.py`: `usage` reads tool uses per turn (before the message-id dedup), returns the grill share, the compaction count and the untimed calls; `is_spec_writer`.
- `commands.py`: `_cost_rows`, `_chief_line`, `_label`/`STEERING`, `_cost_summary`, `status` line.
- `status.py`: steering and shape words (parallel, series, stack), no `foreman` default.
- Cards: `foreman.md`, `chief-of-staff.md`, `status-layout.md`, `concepts.md`; docs and the two lifecycle diagrams (retro at each pause).
- Tests: a unit test of the turn rule; scenario checks for the split, compactions across a batch edge, Copilot unknown, steering and shape.

## Human decisions

- A retro at each release and at each pause when every CR is merged; each point offered as an inbox item.
- The Chief of Staff's cost is split in two lines; a part that cannot be measured is shown as unknown, never estimated, including compactions, with their count.
- The grill turns leave the batch's budget in direct mode; the retro lives in the batch folder only and is deleted at close once offered.

## Impacts

Cost reports and `status` wording change; the retro is a new step of the steering session's cards.

## Test plan

- [x] New or changed tests (they fail on the previous code) - judged at a5a4e48
- [x] Local gates: `just check` (42 passed), `just scenario` (github 459/459, gitlab 459/459) - at a5a4e48
- [x] Evidence: verifier VERIFIED at a5a4e48 (`evidence/pytest-a5a4e48.txt`, `evidence/scenario-gate-a5a4e48.log`); the retro's card behaviour is read, not executed (no test, by the specification)
- [x] Review: inspector approved rounds 2 and 3; the rebase onto b3b2da4 changed only context
- [x] CI green at a5a4e48 (ubuntu, macos, windows, scenario)

## Internal references

CR-165 systematic-retro.

</details>

