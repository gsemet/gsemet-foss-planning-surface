## Summary

Raw CI artifacts that an agent downloads into a change's `work/` folder (hundreds of files, paths over 350 characters) made the surface server's writer fail on Windows with "Filename too long", and the blocked line named neither a file nor what to do. They are now kept out of git by a managed ignore rule, the cards tell agents where to download them, and a too-long path blocks the writer with a line that names the file and the way out.

## Deliverables

| Path | Published |
|---|---|
| `<CR>/work/artifacts-1/a.txt`, `work/debugger/artifacts-99/deep/a.bin` | no |
| `<CR>/work/artifacts-1` (a file), `work/artifacts.md`, `evidence/artifacts-1/a.txt` | yes |

- The managed `.gitignore` gains `**/work/**/artifacts-*/`; existing planning folders get it at the next write, with no migration. The CLI's own pattern reader now treats a middle `**` as git does.
- Downloads go to `<CR folder>/work/scratch/artifacts-<run id>/` (cards for the Driver, debugger, verifier, and the concepts card).
- New blocked reason `path-too-long`: `<n> characters: <path>` with the way out "move it under `work/scratch/`, or shorten it".

## Blast radius

Grade: 1. A reader of ignore patterns and one new blocked reason; `git revert` restores the previous behaviour.

## Autonomous decisions

- The startup-size limit for the Driver card's common path in `tests/test_startup_manifest.py` goes from 45,000 to 45,400 bytes: the specified sentence adds about 380 bytes and the card was within 15 bytes of the limit.
- `Writer._late` moved to a new `writer/late.py` so `cycle.py` stays within its line target.

## Known gaps

- Git for Windows only warns (and skips) when a folder itself is too long to open; the new blocked line arises when the folder opens and the file path is too long (the reported case).

<details>
<summary>Details</summary>

## Changes

- `core/files.py`, `store/base.py`: ignore line and `**` matching.
- `writer/git_ops.py`, `writer/cycle.py`, `writer/late.py`, `hub/schemas.py`: recognition, state and way out of `path-too-long`.
- Cards `driver.md`, `debugger.md`, `verifier.md`, `concepts.md`; docs `planning-folder.md`, `planning-modes.md`.

## Impacts

No visual change. Planning folders ignore downloaded artifacts; a too-long path shows a precise blocked line.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`: 
- [ ] Evidence: before at `<sha7>`, after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-421 ci-artifacts-out-of-plan.

</details>
