## Summary

`ship` recorded a PR's base only for a CR of a recorded stack, and took its draft state from the Driver's `--draft` flag. A PR stacked by hand on another branch was therefore recorded on `main`, and a PR turned ready on the forge could still read "PR in draft ... waits on <other CR>". The record drifted from the forge.

Now `ship` reads, for every PR or MR it records, in every batch mode, the base and the draft state from the forge in one read (GitHub `gh`, GitLab `glab`), and records both. The `ready to merge` word and what a PR in draft waits for read the recorded forge base.

## Deliverables

- `ship <cr> <link>` prints `recorded <link> (base <branch>, head <sha7>, draft|out of draft)`, both read from the forge. A failed read prints `base ? (not read from <link>: <why>)` and `draft not read`, records nothing stale, and the CR reads `PR in draft`.
- `ship --draft` is removed (argparse refuses it): the forge is the only source of the draft state.

```text
before: ship (base read only for a stacked CR; draft from --draft)
after:  ship -> one forge read -> pr_base, pr_draft recorded on the CR
        ready_word / draft_waits / notify / hand-back line read pr_base
```

- A PR stacked by hand on another CR's branch reads `PR in draft` and names that CR as what it waits for, even once out of draft, until its forge base is the default branch.

## Blast radius

Grade: 2

Shared CLI code (`ship`, the derived readiness words) and a new record field with a default, so old records load unchanged. Revert restores the previous behaviour.

## Autonomous decisions

- The scenario's fake forge resets its drafts and bases when the new cases finish, because PR links repeat across batches.

## Known gaps

- GitLab's `draft` field is unproved on a real instance (the fake serves the documented name).
- The card line for a Driver on GitHub Copilot turning its PR ready and running `ship` is unproved there.

<details>
<summary>Details</summary>

## Changes

- `core/records.py`: new `pr_base` on the CR record; `rails_release.py` clears it with `pr_draft` when a release is merged.
- `commands/forge_base.py`: one read returns base and draft; a missing or non-boolean draft is a failed read.
- `commands/delivery.py`, `declare/delivery.py`: `ship` always reads the forge; `--draft` removed.
- `stacks.py`, `status/words.py`, `commands/driver.py`: derived words read the recorded forge base.
- Scenario fakes and steps, `driver.md`, `concepts.md`, `scenario/README.md`.

## Human decisions

- `ship --draft` goes: the forge is the only source of the draft state.
- The change works on both forges (GitHub and GitLab) and both hosts; a path not proved on a real GitLab or on Copilot is marked "unproved" in the card.
- A forge read that fails keeps the `base ? (not read from <link>: <why>)` line, with `draft not read`: no retry, no fallback.
- `ship` records the forge's base on the CR, and the derived words read it.

## Impacts

No visual change.

## Test plan

- [x] New or changed tests (they fail on the previous code): scenario steps for the forge read, the refused read, a hand-stacked PR, and `ship --draft` refused
- [x] Local gates at `b319f0f`: `just check` (173 passed, at `6d07c1b`, carried from `6d07c1b`); scenario units stack, release, gitlab, parallel pass (at `6d07c1b`, carried from `6d07c1b`); full `just scenario` locally on Windows passed at `b319f0f`
- [ ] Evidence: none, no visible change
- [x] Review: approved at `dc1fe52` (carried from `dc1fe52` over clean rebases to `b319f0f`)
- [x] Verified at `b319f0f` (carried from `6d07c1b` over a clean rebase)
- [x] CI green at `b319f0f`: all five checks pass, including `just scenario (ubuntu-latest)`

## Internal references

CR-270 ship-reads-forge

</details>



