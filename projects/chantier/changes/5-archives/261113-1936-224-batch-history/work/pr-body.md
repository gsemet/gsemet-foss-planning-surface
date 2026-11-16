## Summary

Each batch now leaves a record of its own in `5-archives/batches/`: `batch-NN.json` (for the UI) and `batch-NN.md` (for a person, with the Completion table, the cost and the retro). `open` reserves the number by writing the JSON as `running`; `close` completes it and writes the Markdown; the next batch number is read from these records, the live batch and `.batch-number`. Batches 1 to 16 are backfilled once, automatically, from the archived `STATUS.json` still on the machine. `status` names the last closed batch.

## Deliverables

The planning folder before and after:

```text
before                                  after
5-archives/                             5-archives/
  <stamp>-<n>-<slug>/  (a CR)             <stamp>-<n>-<slug>/  (a CR; no retro.md)
    retro.md  (last CR of a batch)        batches/
                                            batch-01.json  batch-01.md
.batch-number (ignored, the only            ...
 counter, lost on a new clone)            batch-NN.json  batch-NN.md   (published)
                                        .batch-number (ignored, still written)
```

Choices: two files per batch, never written by another batch; two-digit ids; the next number is the highest of the records, the live batch and `.batch-number`, plus one; the retro goes into `batch-NN.md`; past retros are linked, not moved; the backfill runs once per planning folder, all or nothing.

## Blast radius

Grade: 2. It changes the formats `open`, `close` and `status` write and print, and the first command of an existing planning folder runs the backfill. What could break: a reader that looked for `retro.md` in a CR's archive, a `close` that fails halfway (it rolls back its renames, the Markdown and the JSON), a folder with no archives (no backfill, nothing written). Rollback: revert the PR; the records are plain files in `5-archives/batches/` that older code ignores, and nothing in an existing archive was moved or changed.

## Autonomous decisions

The specification's defaults, not yet confirmed with the user: the backfill is automatic in the CLI, once per planning folder; past retros are linked into `batch-NN.md`, not moved; the Completion part of `batch-NN.md` is built by the CLI from the record, not copied from a report written by hand; `pause` does not touch the record; `title` is kept in each CR entry; `.batch-number` is still written; two machines that open before a sync take the same number and meet in a git conflict, which is named as a limit and not prevented. Every writer now writes `\n` line endings.

## Known gaps

None

<details><summary>Details</summary>

## Changes

- `history.py` (new): the record's read and write, the reservation at `open`, `last_closed`, the close record and the Markdown, and the undo of a close.
- `backfill.py` (new): writes `5-archives/batches/` once, from the archived `STATUS.json`, the live batch and `.batch-number`, in `.batches.tmp` then one rename.
- `Repo.next_batch_number` and `Batch.__exit__` (`state.py`): the next number, and the record reserved at `open` (removed if `open` fails).
- `close` (`commands.py`): the retro goes into `batch-NN.md`; the JSON is completed; a rollback restores everything on failure.
- `status`: a `last closed:` second line; the no-batch refusal names the last closed batch.
- `_past` and `archived_merged` skip `batches`.
- Cards and docs: concepts, chief-of-staff, status-layout, planning-folder, the lifecycle texts and SVGs, scenario README; scenario steps 1 to 10.

## Human decisions

- One file per batch, so users of a surface never edit the same file.
- The JSON is read by the UI and the Markdown is for a person.
- Ids and file names are padded to two digits.
- The retro moves into the batch's Markdown.
- `open` reserves the number; `close` completes the record.
- Batches 1 to 16 are backfilled from the existing archives.

## Impacts

A planning folder gets `5-archives/batches/` on its first command after the update. The board's counts do not change. No `STATUS.json` field and no board code changes.

## Test plan

- [x] New or changed tests (they fail on the previous code): scenario steps for the record at `open`, the next number, `close` with and without `--yes`, the rollback, the retro cases, the `status` line, the backfill, the index and the external mode
- [x] Local gates at `4891c44`: `just check` and `just scenario` pass
- [x] Evidence: after at `4891c44`: the Verifier ran `open`, `close` with and without `--yes`, `status` and the backfill on a scratch planning folder; outputs are text files kept in the CR folder, not images, so none is attached (no visual to show; before is the previous CLI, which has no record)
- [x] Review: approved at `4891c44`
- [x] Verified at `4891c44`
- [x] CI green at `4891c44`: `gh pr checks 165`, 5 checks pass

## Internal references

CR-224 `224-batch-history`: `.agents/changes/4-batch/2-actives/224-batch-history/03-change-spec.md`

</details>
