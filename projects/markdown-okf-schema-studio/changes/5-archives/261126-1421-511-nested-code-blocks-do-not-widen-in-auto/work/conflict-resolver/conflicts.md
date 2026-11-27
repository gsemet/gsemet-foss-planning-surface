# CR-511: stack restack conflicts

- Branch: `chantier/batch-09/cr-511-requirements-only-top-level-blocks-widen`
- Old head `5f7658a` (old base `89cae5f`), new base `54d1da62`, new head `928ebd7e`
- One commit replayed, message unchanged. Worktree clean. Nothing pushed.

## Conflicted hunks

1. `requirements/tiers/log.md`, under `## 2026-11-26` (one hunk).
   - Base side: the CR-512 entry, the CR-505 round 3 entry and the CR-505 first round entry.
   - Branch side: the CR-511 entry "Auto width: only top-level blocks widen".
   - Choice: both kept, text unchanged. CR-511 is on top, then CR-512, CR-505 round 3,
     CR-505 first round, then the CR-504 entries as before. One date heading. No byte-order
     mark added. Against `54d1da62`, the file differs only by the CR-511 entry.

The four other files of the commit applied without conflict (SwRS-MDOKFSTUDIO-LAYOUT-023.md, the
layout-width `index.md`, `test/page/codeBlockBreakout.test.ts`,
`test/page/runtimePageControls.test.ts`).

## Fast gate

`just --justfile C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-511/justfile check`
at `928ebd7e`: passed (exit 0). Node tests: 56/56; 5360 pass, 0 fail, 7 skipped of 5367;
116/116. Python: 254 passed. Requirements checks: 0 indexes, 0 projections and 0 coverage files
would change; the lint printed broken cross-link warnings (W2) without failing.
Raw log: `just-check.log` in this folder.
