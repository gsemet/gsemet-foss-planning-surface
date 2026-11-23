# Conflicts: CR-470 rebase on origin/main (d9b3cd6b)

Rebased head (single CR commit): b6c4e8573940169b6a9e304620804cdec200ad2d

## Conflicted hunks

- `requirements/tiers/log.md`, `## 2026-11-23`: main added the CR-468 entry (async file-system port),
  the CR added the CR-470 entry (PlantUML jar through ProcessRunner). Kept both, CR-468 first, CR-470 after,
  separated by a blank line; markers removed, no BOM.

## Semantic (non-textual) fix, uncommitted

- `test/visual/renderFixtures.ts`: both sides added `import { createNodeFileSystem }` (TS2300 duplicate
  identifier, found by the gate). Deleted the second import line (line 28). This change is in the
  worktree but NOT committed (the resolver never commits): the Driver must commit it (amend or fixup).

## Fast gate

Command: `just check` in the worktree (after the import fix). Result: pass (exit 0; only existing
W2 broken cross-link warnings in requirements). Before the import fix it failed at `tsc` with the
TS2300 above.
