# Verification, CR-160, head 7fb1a98, round 2

- Gate: work/gates/20261110-174834.log reused (just check + just scenario passed at this head; CI green on 3 OSes).
- Manual external-mode check (temporary surface, one project, own bare origins, clone outside the surface):
  preflight (after clone present) passes, P8 finds the clone's AGENTS.md, P11 reports default branch;
  init creates the 8 stage folders and changes/.gitignore; file, triage --ready, open, take work;
  take prints cli: with --project, clone:, archive: lines and absolute paths, worktree under checkout.yml's worktrees.
- Surface `git status --porcelain -uall`: only changes/.gitignore and the CR's 01-intent, 03-change-spec, intake/request
  (no batch.json, events, STATUS, lock, seat, .batch-number). Clone: clean, no extra worktree.
- Diagrams: 6 PNGs present; planning-modes, cr-folder-lifecycle, how-chantier-works viewed and legible, consistent with spec.
- Docs names (--project, checkout.yml, delivery.md, "Archive in the PR") match the CLI.
- Not run: hooks/register.test.tsx (unrunnable here). Scenario not rerun.
- Finding (minor): checkout.yml written with a UTF-8 BOM (Windows PowerShell `>`) is silently ignored: defaults used, P8 then fails naming .repo.
