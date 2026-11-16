# Intent: chantier plans in its external surface

chantier's planning moves from `.agents/changes/` in its own repository to
`projects/chantier/changes/` of the surface `gsemet/gsemet-foss-planning-surface`. This is the
external mode of `docs/planning-modes.md`.

This work had no CR number and no batch: the Chief of Staff did it directly, on the user's word.

What was done, 2026-11-16:

1. **Backup.** All of `.agents/changes/` (3022 files, ignored ones included) was zipped to the
   user's Downloads folder, as `chantier-agents-changes-2026-11-16.zip`.
2. **Copy.** The 2269 files git does not ignore were copied to the surface. Their hashes were
   checked against the originals.
3. **Push.** The autosync committed the copy. Gitleaks then blocked its push on three false
   positives in board prototypes, the localStorage key `KEY = "chantier-proto-triage-3"`. On the
   user's order, the autosync was stopped and the Chief of Staff pushed by hand.
4. **project.md.** The surface's `project.md` now says `- Archive in the PR: no`.
5. **PR 246.** chantier's `AGENTS.md` gained a `chantier` section with the line
   `- planning: https://github.com/gsemet/gsemet-foss-planning-surface, projects/chantier`.
6. **Independent check.** A read-only subagent compared the local folder, the zip and the surface
   (working tree and `origin/main`) file by file, by hash. No file had its only copy in the local
   folder. The 752 ignored files (STATUS files, gate logs, locks, two `.pyc` files) are in the
   zip only.
7. **Local folder.** On the user's word, the local folder was renamed
   `.agents/changes.disabled-use-surface/`. It was not deleted.

Left as is: the surface's autosync stays stopped until the user says `start autosync`.
