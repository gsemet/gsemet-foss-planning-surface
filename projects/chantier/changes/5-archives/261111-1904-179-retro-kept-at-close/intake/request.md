# A batch's retro survives `close`: it is kept in the batch's last CR

The user (2026-11-11, after batch-09's close): "les rétro peuvent être perdu ce serait bien
qu'ils soient stocké dans la dernière CR du batch".

## What happened

- `close` deletes `4-batch/retro.md` with the batch's other files.
- The Chief of Staff's card says to offer the Retro before any `close`, but the file itself is
  lost.
- After batch-09's close, the Chief of Staff rebuilt it by hand from its own context, into
  `5-archives/261111-1247-171-batch-09-retro-fixes/retro.md`.

## What the user wants

- At `close`, the CLI moves `4-batch/retro.md` into the folder of the batch's last CR, as that
  CR goes to `5-archives`; it does not delete it.
- Open for the grill:
  - What "last" means: the last merged, or the last taken.
  - A batch with no merged CR (every CR cancelled).
  - Whether `close` prints where the retro went.
  - Whether a CR's archive in its PR (`archive: in the PR`) carries it too.
