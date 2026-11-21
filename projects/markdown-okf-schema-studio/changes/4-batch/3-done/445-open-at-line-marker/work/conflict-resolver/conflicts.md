# Conflicts, CR-445 rebase on the CR-444 branch

Rebase finished (5/5 commits). Only one conflict, at commit fde7a6e0.

## CHANGELOG.md, section Unreleased

- Base side: the CR-439 entry (requirements map). Branch side: the CR-445 entry (open at a searched line).
- Choice: keep both. The list is in CR order, oldest first (CR-444 blank-lines entry is last), so the CR-445 entry is appended after the CR-444 entry, before `## 1.10.0`. No BOM (file starts with `# C`).

## Not a conflict, fixed after the rebase (uncommitted in the worktree)

The base brought a bundle test (`test/site/requirementsViewer/bundle.test.ts`) that requires every `### Scenario` heading to carry a `: title`. SwRS LIFE-178..185 (this CR) used bare `### Scenario (nominal)` / `(boundary)`. Added a title to each heading in `requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-178.md` to `-185.md` (8 files, 16 lines). The Driver must commit them.

## Fast gate

Command as run: `just check` (in the worktree). Result: first runs failed in `unit` on "no scenario card of the requirements bundle is empty" (LIFE-178, then 179); after the heading fix, exit 0, all checks pass. Log: `check.log` in this folder.
