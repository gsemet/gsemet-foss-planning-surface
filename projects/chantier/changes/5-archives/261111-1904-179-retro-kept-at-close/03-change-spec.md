# Change Specification: retro-kept-at-close

## Goal

The user, after batch-09's close: "les rétro peuvent être perdu ce serait bien qu'ils soient
stocké dans la dernière CR du batch" (retros can be lost; keep them in the batch's last CR).

Today `close` deletes `4-batch/retro.md` with the batch's other files, so the only record of a
batch's lessons is gone once the batch is closed. After this change, `close` keeps it: the file
moves into the archive of the batch's last merged CR, and never disappears. This works the same in
any project, in-repo (`.agents/changes/`) or on an external planning surface: every path comes
from the planning folder's layout (`stage_layout`), never from a hardcoded root.

## Behaviour

### Where the retro goes (decisions 1, 2, 3)

At `close --yes`, the CLI handles `4-batch/retro.md` as follows:

1. **The batch archives at least one CR.** The retro moves, whole (every pause's section, as
   written), to `retro.md` at the top of the archive folder of the CR merged last among those
   this `close` archives. "Last" is the one whose archive folder name sorts last
   (`archive_name()`: `<YYMMDD-HHMM>-<number>-<slug>`, the merge time first, so the latest merge
   wins and a tie on the minute goes to the name that sorts last). It is the newest folder in
   `5-archives`, where one looks first.
2. **The batch archives no CR** (every CR cancelled, or none merged): the retro moves to a new
   folder of `5-archives` named for the batch, `<YYMMDD-HHMM>-<batch id>` (the time of the close,
   UTC, as `stamp()` gives it, e.g. `261111-1530-batch-09`), holding only `retro.md`. It is never
   deleted.
3. **No retro** (`4-batch/retro.md` missing, or empty: no bytes, or whitespace only): nothing is
   moved and no file or folder is created. An empty file goes with the batch's other files, as
   today.

The retro is a move (a rename), never a copy, and never an overwrite: if the target `retro.md`
already exists in the last CR's archive (or the batch's retro folder already exists), the close
is refused whole, like an archive collision today (README: "collisions are errors rather than
overwrites"), and everything is put back.

### What `close` prints (decision 5)

One line about the retro, in both forms of the command, with the path shown as the CLI shows the
others (`_shown`, relative to the project or the surface):

- Without `--yes` (where it will go), one of:
  - `retro: 4-batch/retro.md moves to 5-archives/<last CR's archive name>/retro.md`
  - `retro: 4-batch/retro.md moves to 5-archives/<stamp>-<batch id>/retro.md (no CR archived)`
  - `retro: no retro`
- With `--yes` (where it went), the same line in the past: `retro: kept in
  5-archives/<...>/retro.md`, or `retro: no retro`.

The wording above is indicative; what is required is one line, starting `retro:`, that names the
destination path or says "no retro". The first line of `close` ("deletes its files in ...")
no longer lists `retro.md` when it is kept; it still lists an empty one, which is deleted.

### All or nothing (decision 6)

The retro's move is part of `_archive_and_delete`'s all-or-nothing: it is recorded in `done` with
the CR moves and is put back on any failure (archive collision, a file in use on Windows, a
retro collision). A failed close leaves `4-batch/retro.md` where it was, and a created
batch-retro folder is removed.

### Not in a CR's PR (decision 7)

A CR's archive in its PR (`archive: in the PR`, the project's `- Archive in the PR:` setting) never
carries the batch's retro. Nothing changes in that code path: the PR is merged before the batch
closes, and `delivery.md` is written at the merge. The Driver's card and the PR-archive cleaning
must not start copying `4-batch/retro.md`.

### The board

The planning folder's `STATUS.md`/`STATUS.json` (`status.py`, `_past` on `5-archives`) lists and
counts merged CRs. A batch's retro-only folder (case 2) holds no CR: it is neither listed nor
counted as a merged CR. A `retro.md` inside a CR's archive changes nothing on the board.
`next_cr_number` and `archived_merged` must stay unaffected by a `<stamp>-batch-<n>` folder (they
already ignore a name with no CR number; keep it so).

### Out of scope: the release's retro (decision 8)

A release CR's own `work/retro.md` is untouched: it already lives in the release CR's folder and
moves with it. Only the batch's `4-batch/retro.md` is concerned.

## What changes, area by area

### CLI (`skills/chantier/scripts/cli/src/chantier/commands.py`)

- `close()`: work out the retro's fate before printing (present and non-empty or not; target
  path: last of `archived` by `archive_name(c, source)`, or the batch's own folder name), add the
  `retro:` line to `lines`, and leave a kept `retro.md` out of the "deletes its files" list.
  The `--yes` return line says where it went.
- `_batch_files()` / the `own` list: excludes `retro.md` when it is kept; an empty one stays in it.
- `_archive_and_delete()`: after the CR moves, move the retro to its target (create the batch's
  retro folder in case 2), recording each rename in `done` so the existing rollback restores it.
  Refuse, without overwriting, when the target exists.
- Docstrings of `close`, `_batch_files` and `_archive_and_delete` say the retro is kept.

### CLI (`skills/chantier/scripts/cli/src/chantier/status.py`)

- `_past()` on the archives stage: a folder named `<stamp>-<batch id>` (a batch's retro, no CR)
  is neither listed nor counted.

### Cards (`skills/chantier/references/`) (decision 9)

The Retro is still offered before any close (it is how the points become inbox items); only the
claim that `close` deletes the file changes, to say it keeps it in the last merged CR's archive
(or a folder named for the batch when none merged).

- `status-layout.md`, the Completion's **For you** line: "the Retro is offered before the close,
  which deletes `4-batch/retro.md`" becomes "... before the close, which keeps `4-batch/retro.md`
  in the archive of the batch's last merged CR".
- `concepts.md`, Batch lifecycle, Paused: "(`close` deletes it with the batch's files)" becomes
  "(`close` keeps it, in the archive of the batch's last merged CR, or in `5-archives/<date>-<batch>/`
  when none merged)".
- `chief-of-staff.md`, the pause paragraph: "Offer the Retro before any `close`, which deletes
  `4-batch/retro.md`" becomes the same "keeps ..." wording. (The same false claim as the two
  cards decision 9 names; it is carried for consistency.)

`agents/` and `com.github.copilot/agents/` need no change (contracts live in the cards).

### Docs

- `README.md`, the layout tree and the close paragraph ("On your yes, `chantier close --yes` moves
  each merged CR to `5-archives`, deletes the batch's own files ..."): add that the batch's retro
  is kept in the last merged CR's archive (or a folder named for the batch).
- `docs/cr-lifecycle-texts.md`, the close step ("each CR of 3-done/ → 5-archives/, the batch's own
  files are deleted"): add "the retro kept in the last CR's archive". `docs/cr-folder-lifecycle-texts.md`
  already shows `retro.md` in a `5-archives` CR folder: it is the target, unchanged.
- `scenario/README.md`: the closing steps list the retro's checks below.

## Evidence

`just check` passes on Linux, macOS and Windows. `just scenario` passes with these checks added
in `scenario/run_scenario.py`:

- In `close_batch` (several merged CRs, a dropped one): write a `4-batch/retro.md` with two
  pause sections before closing.
  - `close` without `--yes` prints one `retro:` line naming the archive of the CR merged last,
    and touches nothing (the retro is still in `4-batch`).
  - The existing archive-collision refusal also leaves `4-batch/retro.md` in place, byte for byte.
  - `close --yes` puts `retro.md` in the archive of the CR with the latest merge time (the one
    sorting last in `5-archives`), its content identical (both sections); it is in no other
    archive; `4-batch` keeps only the three empty state folders; the output names where it went.
- A retro collision: a `retro.md` already in the last CR's `3-done` folder makes `close --yes`
  refuse, with everything put back and both files unchanged.
- A batch whose every CR is cancelled, with a retro: `close --yes` creates
  `5-archives/<YYMMDD-HHMM>-<batch id>/retro.md` and nothing else in that folder; the board's
  merged count does not grow and the folder is not listed as a CR; the next `file` gets the next
  CR number as before.
- A batch with no `retro.md`, and one with a whitespace-only `retro.md`: `close` prints
  `retro: no retro`, creates nothing in `5-archives` beyond the CRs' archives, and the empty file
  is gone with the batch's files.
- External mode (the scenario's surface run, near "`close` puts the merged CR in 5-archives with
  its delivery.md"): the retro lands in the surface's `5-archives` CR folder, and the CR's
  archive in its PR holds no `retro.md`.

## Out of scope

- A release CR's `work/retro.md` (decision 8).
- Carrying the retro in any CR's PR (decision 7).
- Any change to how the retro is written (the Foreman's or the Chief of Staff's sections) or
  offered (the Completion report's Retro, `$CHANTIER file`).
- Linking the retro from a STATUS page.
- Recovering retros of batches already closed.

## Open questions

None: every point of the request is decided in `02-answers.md`; the retro collision follows the
project's existing rule that collisions are errors, not overwrites.
