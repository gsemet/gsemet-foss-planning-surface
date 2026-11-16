## Summary

When the Chief of Staff steers a batch itself (direct mode), it now runs `$CHANTIER rules` and reads the rule files that command lists right after it claims the batch, every batch, a resumed or taken-over session included. Before, a steering session could run `rules` only at its start, before the claim, so the eval audit (which reads the transcript from the claim on) failed its rules check.

## Deliverables

The new sentence in the "Your epoch." bullet of "Steering a batch yourself" (`skills/chantier/references/chief-of-staff.md`):

> Right after each claim, every batch you steer, a resumed or taken-over one too: run `$CHANTIER rules` and read the rule files it lists, as a Foreman does at its start. A reading before this batch's `open` is not this batch's; skip only the re-read of a file this session has read since this batch's `open` and since its last compaction. The command runs every time, after the claim, whatever ran before it.

Choices: the command always runs; only the re-read of a file already read for this batch and since the last compaction is skipped; `rules` stays out of the `--epoch` list; no CLI refusal and no audit change.

## Blast radius

One paragraph of one card. The Foreman card, the agent files, the CLI and the eval kit are unchanged. A steering session spends one more command and a few file reads per batch.

## Autonomous decisions

None.

<details><summary>Details</summary>

### Changes

- `skills/chantier/references/chief-of-staff.md`: the rules step added to the claim bullet.

### Impacts

No visual change. The next real-direct eval should pass its rules audit with `rules` run after the claim.

### Test plan

- [x] `just check` passes (checked at 1fbe16f).
- [x] `just scenario` passes (carried from 1989d60: patch unchanged; the long gate runs once at the top of the stack, PR 152).

### Internal references

- CR-205 "The steering session reads the rules after its claim"
- Source: real-direct run 1 of 2026-11-12, finding 6; real-foreman run, finding 5.

</details>
