## Summary

Chantier plans inside the project, in a planning folder of its own. This adds a second, fully supported mode: an external planning surface, a separate git repository with one folder per project (`projects/<name>/` holding `project.md`, `checkout.yml` and `changes/`). The project's repository then gets only the code and, when its maintainer wants it, each change's cleaned archive in the change's PR. A project that declares nothing behaves exactly as before.

## Deliverables

- New CLI mode: `--project <folder or name>` selects a project of a surface; without it, a surface root with several projects exits 2 naming them, and the project's own planning folder is used as today. `take` and `handoff` carry `--project` in their `cli:` line and print `clone:` and `archive:` lines.
- The planning folder gets its own `.gitignore`, so a running batch's own files and detailed logs never reach the surface's git.
- Archive: in the surface's `5-archives` with a `delivery.md` (PR link, merge time, whether the archive is also in the PR); in the PR, by a `project.md` setting (`- Archive in the PR: yes|no`, `yes` when absent); `ship` reports `archive missing from the PR`.
- The CR board shows one section per project of a surface.
- Docs: new page `docs/planning-modes.md`, a "Planning modes" README section, and diagrams for both modes (renders below).
- Hosts: the user's finding on remote sessions (start the main session locally, then Remote Control) is recorded as a finding, and the extra-folder access a surface needs as unproved.

Diagram renders (new `planning-modes`; changed `how-chantier-works`, `how-chantier-works-simple-direct`, `how-chantier-works-simple-foreman`, `cr-folder-lifecycle`, `cr-lifecycle-simple`):

![planning-modes](https://github.com/user-attachments/assets/f5f2a48b-e7b4-4c6f-8506-f1422dcf47c9)

![how-chantier-works](https://github.com/user-attachments/assets/bd6b10a9-a4f2-4b7a-b94f-8c161c5fdfeb)

![how-chantier-works-simple-direct](https://github.com/user-attachments/assets/fb8e6c8f-2347-44eb-aed5-0b63fa54db69)

![how-chantier-works-simple-foreman](https://github.com/user-attachments/assets/3958ec9d-f26e-4b36-8bd9-8542544b5cf9)

![cr-folder-lifecycle](https://github.com/user-attachments/assets/d6be365c-48c2-4295-b317-74b8d58e61e2)

![cr-lifecycle-simple](https://github.com/user-attachments/assets/e83d4ced-1020-481c-b9ec-81a6a202a450)

## Blast radius

Grade: 2

The CLI's path handling changes everywhere (the planning folder is no longer derived from the project root), and recorded CR paths become relative to the planning folder; the old form still reads. Revert restores the previous behaviour, but a batch opened with the new form would need the old one reopened.

## Autonomous decisions

- The archive setting is a line in `project.md`, `yes` when absent.
- A grill session in a surface worktree does not join the surface's autosync; its files are handed to the main session.
- This repository's own rule on where chantier writes now says: only in the planning folder (the project's, or the project's folder of an external planning surface), as plain JSON and Markdown, and a change's cleaned archive in its PR when the project asks for it. This is a project rule change, made on purpose.

<details>
<summary>Details</summary>

## Changes

- `state.py`: the project root and the planning folder are separate; `checkout.yml` parser; surface detection.
- `commands.py`, `lifecycle.py`, `status.py`, `rails.py`, `cli.py`: work from the planning folder; `preflight`, `init`, `rules`, `take`, `ship`, `order merged`, `close`.
- `hooks/register.tsx`: board sections per project.
- Cards, hosts, README and docs as above.

## Human decisions

- The surface is always worked on its default branch; only the project's code gets worktrees.
- The running batch's own files stay local; reports and evidence are pushed while a change runs.
- No migration command; no archive in the PR in in-project mode.

## Impacts

No change for a project that declares nothing. The diagrams now show both modes.

## Test plan

- [x] New or changed tests (structure test with an external variant, links test over docs)
- [x] Local gates: `just check`, `just scenario` (both forges, with the new external run)
- [x] Evidence: diagram renders in Deliverables; a manual external-mode check on a temporary surface (only the project's planning files listed by git, clone clean); the board test (`hooks/register.test.tsx`) could not be run here (no runner) and needs one run by a maintainer. Known limit: a `checkout.yml` saved with a UTF-8 BOM is ignored (defaults apply)
- [ ] Review
- [x] CI green

## Internal references

CR-160 planning-repo. Work files in `.agents/changes/4-batch/2-actives/160-planning-repo/work/`.

</details>

