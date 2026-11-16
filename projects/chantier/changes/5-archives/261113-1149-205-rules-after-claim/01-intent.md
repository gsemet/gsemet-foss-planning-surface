# The steering session reads the rules after its claim

## The request

From real-direct run 1 (2026-11-12, PR 137, audit J14, finding 6): the direct-mode Chief of Staff
ran `chantier rules` at the start of its session, before `open`, and not again after it claimed
the batch. The steering card should say that the steering session reads the rules right after
its claim, every batch, in direct mode too.

## The problem

- A Foreman reads the project's rules at the start of every batch (`foreman.md`: the brief, the
  cards and the rule files `$CHANTIER rules` lists, read again and not from memory).
- `chief-of-staff.md`, "Steering a batch yourself", says to do what the Foreman's card says, but
  its own list of steps ("Your epoch") goes from the claim straight to the Drivers. A Chief of
  Staff that read the rules at its session's start sees no reason to read them again, and its
  session may be hours old, compacted, or on its second batch by then.
- The audit reads the steering transcript from the claim on, so it found no `rules` and failed
  J14. The audit is right: the rail is "the steering session reads the rules", per batch.
- The real-foreman run of the same day showed the weaker form of the same gap (its finding 5): a
  Foreman ran `rules`, which prints the list of rule files, and read none of them.

## What would fix it

One line in `chief-of-staff.md`, "Steering a batch yourself": right after the claim, every batch,
run `$CHANTIER rules` and read the rule files it lists, as a Foreman does at its start. The
command is the anchor the audit reads; the files are the substance.

Done when: the card says it, and a direct batch's audit passes J14 with the rules read after the
claim.

## Out of scope

- The audit: J14 stays as it is (item `audit-direct-false-fails` does not touch it).
- The Foreman's card, unless its wording on the same step disagrees with the new line.
- The agent files (`agents/`, `com.github.copilot/agents/`): the contract is in the card.
- A CLI refusal (for instance `take` refused until `rules` ran): the CLI knows no role, and
  nothing measured asks for it.
