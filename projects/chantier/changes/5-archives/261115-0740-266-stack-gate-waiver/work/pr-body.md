Stacked on #209.

## Summary

In a stack, the user could waive the long gate for the lower PRs in a brief or from memory, and nothing in the record said so: a CR believed its gate was waived and nobody filed the follow-up gate on main. This PR makes a waiver a recorded fact on each CR it covers, and shows it, with the same words, in `chantier status`, `STATUS.md`, `STATUS.json`, the CR board pane and the web board.

## Deliverables

One long gate on the stack's top PR, recorded per CR, shown everywhere with the same words:

| Long gate column | Meaning |
| --- | --- |
| `passed abc1234` / `carried from abc1234` | a gate pass at that head, or one carried over a clean rebase |
| `queued` / `running` / `failed abc1234` | the gate's live or last state |
| `waived → CR-k (#n)` | covered by a stack waiver; CR-k's gate validates it |
| `validates CR-a, CR-b` | the stack's top, whose gate validates the waived CRs |
| `exempt: <rule>` | `--no-gate` under a project rule |

```text
order waive stack --note "<the user's words>"
order waive <cr> --note "<the user's words>" --follow-up <backlog folder>
order waive stack|<cr> --note -          # withdraw
```

- A covered CR hands back ready with no gate pass and no `--no-gate`; the top of a waived stack still needs its gate; the head, clean, pushed and `VERIFIED` checks stay.
- `take` and `handoff` print one `gate:` line so a Driver never guesses.
- Screenshots: none yet (see Known gaps).

## Blast radius

Grade: 2. A new order kind, a new record field and a new column on every status surface; it touches the hand-back check. `git revert` restores the previous behaviour; records written with a `gate_waiver` keep loading (the field is optional).

## Autonomous decisions

- `gate_queue`, `gate_slots` and the head helpers moved out of `commands/` so `status/` can read gate state without importing a higher layer.
- `commands/orders_reorder.py` split from `orders_apply.py` to stay under 400 lines.
- `order waive <cr> --note -` on a CR covered by a stack waiver is refused, and says to withdraw with `order waive stack --note -`.
- A CR handed back under a waiver that is later withdrawn keeps the waiver it was handed back under.

## Known gaps

- No screenshot of the pane from a real session.
- The docs screenshots are not retaken (`just docs-screenshots`) and there is no capture of the web board showing a waived stack.
- The `evals/kit/audit.py` C7 check was run through `event_checks` on the scenario's live record of a waived stack (not a full `audit.py <workspace>` run, since the scenario closes its batch); no real eval has run it.
- A CR handed back as the stack's top on a gate pass reads `waived` once another CR joins above it (the covered branch wins over the pass).
- The rule-2 clause (early push when the rebase needs a gate because the CR is a waived stack's top) is not named in `driver.md`; it holds because the top needs its gate.
- `queued` and `running` in `STATUS.md` and `STATUS.json` are as of the last render; the `chantier status` text reads the lock live.

<details>
<summary>Details</summary>

## Changes

- `declare/orders.py`, `commands/orders.py`, `commands/orders_waive.py`, `commands/orders_apply.py`: the `waive` order, `order add` on a waived stack.
- `core/records.py`: `GateWaiver` and `CrEntry.gate_waiver`; `stacks.py`: the validating top.
- `commands/driver_checks.py`, `commands/driver.py`, `commands/facts.py`: hand-back with a waiver, the `gate:` line.
- `status/gate.py`, `status/steps.py`, `status/views.py`, `status/markdown.py`, `commands/batch_status.py`, `board/crs.py`: the shared `gate` object and the column and step words.
- `hooks/register.tsx`, `types/index.d.ts`, `hooks/register.test.tsx`: the pane's column and line; `board/web/js/`: the card, the panel and the words in English and French.
- Cards (`chief-of-staff.md`, `foreman.md`, `driver.md`, `concepts.md`, `status-layout.md`), `evals/kit/audit.py` C7 and `evals/SCORECARD.md`.
- Tests: three new pytest files and a scenario case in the `stack` unit with its README bullets.

## Human decisions

- A stack waiver needs no follow-up: the top PR's gate is the validation; a follow-up is filed only for a waiver nothing in the batch validates.
- The waiver is recorded by the Chief of Staff on the user's word, through an order, then applied per CR by the CLI.

## Impacts

Each surface gains a "Long gate" column and a step line; no other visual change.

## Test plan

- [x] New or changed tests (they fail on the previous code): three pytest files (29 cases) and scenario section 13b
- [x] Local gates at `f86d5b4`: `just scenario`, `just check` and `just mod` (59 pass) passed; `just eval-dry-run` passed in CI at that head
- [x] Evidence carried from the head before the restack (the restack on #209 touched no code the C7 check runs through; the stack unit passes at `f86d5b4`): C7 on the waived stack's record: `(True, 'each CR handed back ready has a verdict VERIFIED and a passed long gate (or a no_gate, gate_from or gate_waiver hand-back) at its head (1 CRs)', 'C7')`; no screenshots (see Known gaps)
- [x] Review: approved at f86d5b4
- [x] Verified at `f86d5b4`
- [x] CI green at `f86d5b4`: `gh pr checks 215`, all five checks pass

## Internal references

CR-266 stack-gate-waiver; stacked on CR-262 (#209).

</details>
