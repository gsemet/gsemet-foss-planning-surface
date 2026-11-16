# Change Specification: verifier-checks-pr-description

## Problem

PR #93 (CR-156) was handed back with a posted description that had lost every line break: one
line of about 5,400 characters, unreadable on GitHub. The Inspector had checked `pr-body.md` during
the rounds, and that file was right. The Driver then put the Verifier's evidence into the
description (`driver.md`, "The evidence"), and that edit broke the posted body. Nobody checks the
description as it is posted on the forge.

## The change

The Verifier also checks the PR's description as posted on the forge. It must be:

1. **Clean:** it renders properly on the forge. That means line breaks, sections, the
   `<details>` fold, and images that resolve.
2. **Consistent with what the PR delivers:** what the Summary, Deliverables and Changes say
   matches the diff at the pushed head. No claimed change is missing, and no delivered change
   goes unmentioned.

A description that fails either point is `NOT VERIFIED`, like any other failed claim.

## Where

- `skills/chantier/references/worker.md`, section Verifier: the rule above.
- `skills/chantier/references/driver.md`: the order of the end of a CR Driver's run, so that the
  check sees the final description.
  - Today the evidence goes into the description after the Verifier, so a Verifier that checks
    the description must see it after that edit.
  - **Recommendation:** after the Driver's last description edit, a short Verifier pass that
    checks only the posted description.
  - **Alternative:** the Verifier puts the evidence in the description itself.
  - The Driver judges; record the choice in the PR's Autonomous decisions.
- The Verifier's agent files (`agents/` and `com.github.copilot/agents/`) only if their bodies
  must change; they stay identical (AGENTS.md).

Out of scope: how the Verifier reads the description (which CLI call, which comparison); the
Inspector's check of `pr-body.md`; `pr-template.md`'s content.

## Acceptance

- `worker.md`'s Verifier section states the check of the posted description, on both points.
- `driver.md`'s end-of-run order makes the Verifier's check see the final posted description.
- `just check` and `just scenario` pass (the change touches cards).
