# Conflicts: CR-471 rebased on CR-469

Rebase of `chantier/batch-09/cr-471-...` (one commit, now 792ae892) onto `chantier/batch-09/cr-469-...` (2d7152e3). Nothing pushed.

Hunks (intent kept on both sides: CR-469 async `FileSystem` lookups, CR-471 routing through `src/core/path/hostPath.ts`):

- `src/core/frontmatter/fileLinks.ts`: imports. Dropped `node:fs` (CR-469 removed every use) and kept `import * as path from "../path/hostPath"`.
- `src/core/frontmatter/stemIndex.ts`: same, and kept CR-469's `import type { LinkFiles }`.
- `src/core/myst/confLocator.ts`: same; CR-469's `readTextFile, FileSystem` import kept (outside the hunk).
- `src/core/render/documentGlob.ts`: same; CR-469's `FileKind, FileSystem` import and `GlobFiles` type kept.
- `src/core/security/resource-policy.ts`: same; CR-469's `FileSystem` import and `PolicyFiles` type kept.
- `.dependency-cruiser.cjs` NODE_DEBT: two hunks. Result is the `hostPath.ts` entry (`path`, `PATH_SHIM`) plus the unchanged `plantUmlRenderer.ts` entry (`child_process`, `fs`). Dropped CR-471's `fs` entries for the five files above (async now) and its `crypto` entries (`commentStore.ts`, `csp.ts`) with `WEB_CRYPTO`, because the base no longer imports `node:crypto` in core. Dropped CR-469's per-file `path` entries (the `hostPath.ts` entry replaces them). `PORT_FOLLOW_UP` stays declared and documented as before (it was already unused in the base).

Non-conflicting files auto-merged. No byte-order mark was added.

Fast gate: `just check` in the worktree: passed (exit 0). Log: `work/gates/conflict-resolver-check.log`; only the usual W2 broken-cross-link warnings of the requirements lint appear.
