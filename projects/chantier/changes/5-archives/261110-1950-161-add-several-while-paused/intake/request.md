# Add several CRs to a paused batch before it resumes

## The user's words (2026-11-10, batch-09)

"Oui dépose une nouvelle modification du CLI: on peut rajouter n CR quand le batch est en pause
avant de le relancer."

## What happened

- batch-09 was paused in direct mode, with every CR merged.
- The user said "Oui fait les 2": add `status-command` and `planning-repo`.
- The first `order add` (status-command, CR-159) printed "batch-09 was paused: running again".
- The second `order add` (planning-repo) was refused: "a running direct batch is strict: add the
  CR once the batch is paused (`pause`), or switch to Foreman mode".
- `pause` was then refused too, because CR-159 was queued and order O-11 was pending.
- So planning-repo waits for CR-159 to merge and for the next pause. Only one CR can join a
  direct batch per pause.

## The request

While a batch is paused, `order add` can be run n times, and each adds a CR. The batch runs again
only after the last one, not at the first `order add`.

How it starts again is the specification's call. One way: an explicit resume step. Another: the
first `take` resumes the batch.

## Notes

- Foreman mode is not the way out here. The user steers over Remote Control and cannot steer a
  Foreman session from there (see the inbox item `options-by-environment`).
- The CLI's error text names Foreman mode as the alternative. It should not offer it as the only
  other way.
