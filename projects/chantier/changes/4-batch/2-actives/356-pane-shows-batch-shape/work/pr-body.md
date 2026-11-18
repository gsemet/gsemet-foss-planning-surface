## Summary

In the CR board pane, nothing told the user whether a batch runs its CRs in series, in parallel or as a stack. The pane now ends the batch's slots line with that shape as one word, for example `Slots 2/3, 1 free · parallel`. The slot count itself is unchanged.

## Deliverables

The batch's line in the pane, before and after:

| Before | After |
| --- | --- |
| `Slots 2/3, 1 free` | `Slots 2/3, 1 free · parallel` |

The word is `stack`, `series` or `parallel` as the batch's record holds it, and `unknown` when the record has none (as `chantier status` prints `shape unknown`). An index written by an older CLI, with no `mode` field, shows the line as before.

```text
STATUS.json (index)  batches[].mode   <- the batch's record, raw (new)
hooks/register.tsx   Batch            -> "Slots t/n, f free · <word>"
```

**UNVERIFIED:** no screenshot of the pane from a real session yet.

## Blast radius

Grade: 1. The index gains an optional field and the pane appends a word to one line; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

None.

## Known gaps

- No screenshot of the pane from a real session: it is owed from a real Claude Code session running this head.

<details>
<summary>Details</summary>

## Changes

- `status/views.py`: each batch entry of the index carries `mode`, beside `slots`; the schema number stays 3.
- `types/index.d.ts`: `ChantierBatch.mode` is optional.
- `hooks/register.tsx`: the slots line ends with ` · <word>`; with `mode` and no `slots`, the word shows alone.
- `docs/boards.md`: the batch's line example includes the shape.
- Tests: the pane test covers each word, `unknown` and an index with no `mode`; the scenario checks the index `mode` against the batch's own `STATUS.json` and after `order mode`.

## Human decisions

- The shape is shown as a word next to the slots on the batch's line.
- The slot count and its free figure do not change.

## Impacts

The batch's line shows its shape; nothing else is visible.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates: `just check`, `just mod`
- [ ] Evidence: no screenshot yet (see Known gaps)
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-356 pane-shows-batch-shape

</details>
