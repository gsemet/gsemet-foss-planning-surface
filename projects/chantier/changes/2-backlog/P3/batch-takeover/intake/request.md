# Take over a batch opened on another machine

The user's word, 2026-11-16, on batch-21's retro (French, translated): "Reopen the batch here and
take up its state as if it had been started here."

The retro point (4-batch/retro.md, 2026-11-16, batch-21): a batch opened and stopped on another
machine cannot be taken over here. batch-20's batch.json, events.jsonl and brief.md were local and
unpublished; `pause` refused it because CR-296 was unmerged though nothing ran, so its record stays
`running` in 5-archives/batches; the CR had to go back to 3-ready into a new batch-21, and the
Driver pushed one head to two branches (batch-20's PR branch and the batch-21 name the CLI
expects).

Wanted: on another machine, the same batch reopens and its state is taken up as if it had been
started there (its CRs, their PRs and branches, rounds, notes, events and costs to date), with no
second batch and no move back to 3-ready.
