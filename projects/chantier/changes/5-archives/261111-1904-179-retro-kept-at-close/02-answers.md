# Answers: retro-kept-at-close

## Decisions of 2026-11-11

Decided by a Fable advisor on the user's delegation: "Grille tout avec une session fable je ne sais pas te répondre…"

1. **`close` keeps the retro: it moves `4-batch/retro.md` into the archive folder of the batch's
   last merged CR,** as `retro.md`, whole (every pause's section). Reason: the user's words; the
   file is the only record of the batch's lessons.
2. **"Last" is the CR merged last among those this `close` archives** (the latest merge time,
   the one whose archive folder sorts last). Reason: it is the newest folder in `5-archives`, so
   the retro is found where one looks first; "last taken" may be a cancelled CR with no archive.
3. **A close that archives no CR (every CR cancelled) keeps the retro in `5-archives` in a folder
   named for the batch,** holding only `retro.md`. Reason: the retro of a batch that failed whole
   is the one most worth keeping; it is never deleted.
4. **No `retro.md`, or an empty one: nothing is moved and `close` says "no retro".** Reason: no
   empty file is created.
5. **`close` prints one line with the retro's destination, without `--yes` (where it will go)
   and with it (where it went).** Reason: the user approves the close on what it shows.
6. **The move is part of the close's all-or-nothing:** a failed close leaves the retro in
   `4-batch`. Reason: same guarantee as the CRs' archives.
7. **A CR's archive in its PR never carries the batch's retro.** Reason: the PR is merged before
   the batch closes, and a retro speaks of the whole batch (costs, other CRs, the user's
   decisions), which does not belong in one CR's public PR.
8. **A release's own `work/retro.md` is out of scope.** Reason: it already lives in the release
   CR's folder; this item is about the batch's file only.
9. **The cards follow:** `status-layout.md` and `concepts.md` stop saying that `close` deletes
   the retro; the Retro is still offered before any close. Reason: the offer is how points become
   inbox items; keeping the file does not replace it.
