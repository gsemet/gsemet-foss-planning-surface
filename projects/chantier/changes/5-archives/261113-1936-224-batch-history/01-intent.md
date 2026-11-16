# Intent: each batch leaves a record of its own in the archive

Today the batch counter lives in `.batch-number`, ignored by git: a new clone, another machine
or another user of a surface starts again at `batch-01`. The archive keeps no tracked link from
a CR to its batch (it is only in the archived `STATUS.json`, ignored by git), and the retro is
kept in the folder of the batch's last merged CR.

Option B, the user's choice: one file per batch in `5-archives/batches/`, `batch-NN.json` and
`batch-NN.md`, numbers padded on two digits (`batch-01`, `batch-02`, …). The JSON is what the
UI reads to show the history; the Markdown is for a human. `open` reserves the number by writing
the batch's record; `close` completes it; the next number is read from these records.
