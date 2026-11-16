# Answers

Grill with the user, 2026-11-13 (asked in French, recorded in English).

1. **Shape: option B** (the user: "B"). One file per batch in `5-archives/batches/`, never
   written by another batch, so no git conflict between users of a surface and none with an
   autosync. Rejected: A, one `5-archives/batches.json` for all (two `close` at once conflict);
   C, the CR folders grouped by batch (moves the 103 archives and breaks the links to them).
2. **Padding** (the user: "met un padding 01, 02,... sur les batch"): batch numbers on two
   digits in every id and file name: `batch-01`, `batch-02`, … (the batch ids already are; the
   file names follow them).
3. **`batch-NN.json`**, read by the UI: the number, the open and close dates, the shape (stack,
   parallel, series), who steered (Foreman or direct), the budget and the final cost; for each
   CR its archive folder, its PR, its result (merged, dropped), its rounds and its cost.
4. **`batch-NN.md`**, for a human: the Completion report and the retro. The retro leaves the
   folder of the batch's last merged CR.
5. **The number:** `open` reserves it by writing `batch-NN.json` with its state "running"; with
   an autosync it is pushed within seconds. `close` completes it. The next number is the highest
   of these records, the live batch and `.batch-number`, plus one.
6. **CLI impact:** `open`, `close`, the next number, and one line in `status` naming the last
   closed batch. The UI shows the history from these files (the board CRs).
7. **The past:** batches 1 to 16 are backfilled once, from the archived `STATUS.json` still on
   this machine; a batch with no trace left is named as such.

The questions above were proposed by the Chief of Staff and the user chose B with the padding;
the rest are the proposal's defaults, to be listed as open points in the specification.

## Decisions after the specification

Asked by the Chief of Staff, 2026-11-13 (in French, recorded in English).

- The other open points stay at the specification's defaults.
