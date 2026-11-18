## Summary

Today `chantier open` refuses to run with no CR, so a batch and its Foreman cannot start until the first specification is ready. With this change `chantier open` with no CR opens the batch directly paused, with no CR; CRs join it with `order add` as their specifications become ready, and the first `take` sets it running, exactly as for any paused batch. Status, the web board and the CR board pane show such a batch as "paused, no CR yet", and `close` accepts a batch that never held a CR.

## Deliverables

A batch born paused, as the CLI now behaves:

```text
chantier open                      -> opened batch-NN: no CR, paused, <slots> slots, <mode>, steering <who>
chantier order add --note <folder> -> batch-NN stays paused: the first `take` sets it running again
chantier take <cr>                 -> batch-NN was paused: running again
```

- The record is born `paused` (`open` event with no CR, then a `pause` event with trigger `open, no CR`), `spent_usd` stays unset and is shown as `none yet`, never `$0.00` or "unknown".
- `--release` with no CR is refused (it names an item and there is none); `--grant-fixes` and `--autonomous-releases` keep their existing refusal.
- `close` of a batch that never held a CR archives no CR; one that no session ever steered reads `none: no session steered it` for its cost instead of a false `$0.00`.
- `crs_total` is a new optional field of the `STATUS.json` batch entries (no schema bump); the pane, the web board's Batch page and its home card use it to tell "no CR yet" from "every CR ended". Defaults matrix: Claude Code and Copilot, Foreman and direct mode; only the heartbeat and the moment of the claim differ (see Changes).

## Blast radius

The change is additive: a path that was refused now works, and the batches with CRs print as before. `spent_text` and `status` change only for a batch with no CR.

Grade: 1

## Autonomous decisions

- A small module `core/steering.py` holds the "never steered" cause and its test, because `rails.py` is at its size cap.
- The never-steered close records its cause beside `cost_usd: null` in the batch's JSON record as a new `cost_cause` field.

## Known gaps

- No screenshot of the pane from a real session.
- The scenario's new empty-batch leg was run in no local gate yet; it is proven by the pipeline's scenario job.

<details>
<summary>Details</summary>

## Changes

- `declare/opening.py`, `commands/opening.py`, `commands/opening_record.py`: `items` optional; refusal of `--release` with no CR; the empty path writes the record, `brief.md` and the two output lines, and sets it paused through `record_born_paused` (`commands/closing.py`) without pricing.
- `rails.py` (`spent_text`), `status/markdown.py`, `status/views.py`, `commands/batch_status.py`: `none yet`, `No CR yet.`, the `order add` hint line, `crs_total`.
- `commands/closing.py`, `commands/close_archive.py`, `commands/cost/`, `history.py`: `close` of a batch with no CR, including one never steered.
- `hooks/register.tsx`, `types/index.d.ts`, `hooks/register.test.tsx`: the pane's title line and body for a paused batch with no CR.
- Web board (`board/state.py`, `js/model/semantics.js`, `js/views/batch.js`, `js/views/home-batch.js`, en/fr keys, `DESIGN.md`): empty state on the Batch page, home card line.
- Cards (`concepts.md`, `chief-of-staff.md`, `foreman.md`, `hosts/claude-code.md`, `hosts/copilot.md`) and `docs/batch-lifecycle-texts.md` / `.svg`: the empty batch, the claim just before the first `take` in direct mode, no heartbeat while the batch holds no CR.
- Tests: `tests/test_open_empty_batch.py`; scenario leg `empty_batch`.

## Human decisions

- No new flag: opening with no CR is the empty batch; one batch per project still holds.
- Direct mode claims the batch just before its first `take`; a Foreman claims at its start and its wait counts in the spend.
- `close` accepts a never-steered empty batch, with its cost shown as "none: no session steered it".
- Pane and board display ship in the same PR; the pane screenshot stays a known gap until one is provided.

## Impacts

A batch can be opened before its first CR exists; the pane, status and the board show it as paused with no CR yet.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`:
- [ ] Evidence: none, no visual capture of the pane yet (see Known gaps)
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-369 open-empty-batch (batch-28); the `ready-joins-waiting-batch` CR is stacked on it.

</details>
