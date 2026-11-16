## Summary

In a parallel batch, every rebase onto a moved `main` started a full Verifier, even when git could prove the CR's own patch had not changed. One real run paid 25 Verifiers for its CRs against 15 in a calmer run. The long gate's pass already carries over such a clean rebase; the Verifier's `VERIFIED` verdict did not.

This PR makes the verdict carry the same way. A rebase with no conflict that leaves the CR's patch unchanged, proved by git, carries the `VERIFIED` verdict to the new head, and `handback ready` accepts it with no new Verifier. A rebase that resolved a conflict, or that changed the patch (a commit added, edited, dropped or folded), is refused with `does not carry: <why>` and still gets a Verifier given the move. CI must still be green at the new head; the CLI reads no CI.

Known risk, accepted: a clean rebase can bring base changes that interact with the CR without a textual conflict. Only CI at the new head catches that now.

## Deliverables

The hand-back now has two independent carries, both proved by the same git check (`carry_check`):

```text
handback ready, head H recorded by ship
  long gate   passed at H?  -> yes | carried (carry_check) -> gate_from
  verdict     VERIFIED at H? -> yes | carried (carry_check) -> verdict_from
  neither: refused, "does not carry: <why>"
```

The ready line and the `handoff` checklist name it:

```text
before: handoff  [ ] verdict VERIFIED (...)            after a clean rebase, any rebase
after:  handoff  [x] verdict VERIFIED carried from <sha7> (clean rebase onto <base>)
        ready    ..., long gate and verdict carried from <sha7> (clean rebase onto <base>)
```

Choices: same rule in parallel, stack and series modes; the conservative side on any doubt (a rebase that drops or splits commits never carries); no second proof method.

## Blast radius

Grade: **2**. The change moves a safety line of the hand-back: a wrong carry would let a head reach "ready" without a Verifier. The proof is git's replay of the verified commits onto the new base (clean and giving exactly the head's tree), and a later `NOT VERIFIED` blocks any carry. Rollback is a plain revert of the PR.

## Autonomous decisions

- The scenario's commit-after-verdict case is rebased by `ship` too; its refusal reason is `the rebase changed the patch`, as the specification says, not a separate message.
- Some lines in `pr-template.md` and `status-layout.md` are longer after the one-line edit and were not re-wrapped, since those cards are rewritten by the next change.

## Known gaps

- Linux and macOS are covered by the pipeline alone; the local run was on Windows.

<details>
<summary>Details</summary>

## Changes

- `commands/crs.py`: `last_verdict_head(events)`, the head of the latest verdict, returned only when it is `VERIFIED`.
- `commands/driver_checks.py`: `_verdict_missing` (carry through `carry_check`, refusal text with the `does not carry` clause); `GateBasis.verdict_carried` and a `verdict_from` key on the `handback` event, next to `gate_from`.
- `commands/driver.py`: the ready line names the carried verdict, in one clause with the gate when both carry from the same head.
- `commands/facts.py`: the `handoff` gate and verdict boxes read `carried from <sha7>` when the carry holds (read-only git).
- Cards: `driver.md` (every place that started a Verifier after a rebase, the stack driver's restack, the description edit that only changes SHA marks to `carried from`), `worker.md` (delta assessment, carried proofs), `concepts.md`, `status-layout.md`, `pr-template.md`.
- `docs/gates.md`, `scenario/README.md`, scenario unit 12f (clean rebase carries, conflict refuses, commit after the verdict refuses), `evals/kit/audit.py` check C7 accepts a `verdict_from` hand-back.
- Tests: `last_verdict_head` assertions in `test_cli_units.py`.

## Human decisions

- A rebase with no conflict that leaves the CR's own patch unchanged carries the verdict; CI must still be green at the new head, and no new Verifier runs.
- The same rule holds in parallel and stack modes; series shares the code path and follows.
- The user accepts the known risk that a clean rebase can bring base changes that interact with the CR without a textual conflict; CI at the new head is the only catch.

## Impacts

Fewer Verifier runs after a clean rebase. No visual change; no change to `hooks/`, `types/` or the board pane.

## Test plan

- [x] New or changed tests (they fail on the previous code): `last_verdict_head` asserts and scenario 12f
- [x] Local gates carried from dc0f563 (clean rebase to `23a8307`): `just check` pass, `just scenario` pass (all units, 86/86 checks in `gates`)
- [x] Evidence: scenario 12f output, carried from dc0f563
- [x] Review: approved, carried from dc0f563
- [x] Verified at `23a8307` (scenario `gates` unit run at that head, 86/86 checks)
- [x] CI green at `23a8307`

## Internal references

- CR-290 `rebase-verify`; specification `.agents/changes/4-batch/2-actives/290-clean-rebase-light-verify/03-change-spec.md`
- Round 1 report and scenario 12f output: `work/r1.md`, `work/r1-12f.txt`

</details>
