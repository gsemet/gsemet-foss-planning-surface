# 151 — Update every dependency, with minimum-version floors for security fixes

Type: chore · Priority: P1 · From the user, 2026-10-27 (overnight run)

## Intent (user)

See [01-intent.md](../01-intent.md).

## Autonomous decisions

- Decided by the main session on 2026-10-27; list these in the PR body under "Autonomous decisions".
- Top of the stack, above CR 150: lock files change last, after CRs 131 and 149 added packages.
- Installing and upgrading packages is allowed by this CR (its own `npm ci` in the worktree).
- The okf-schema repository's alerts are out of this stack (another repository); proposed to the
  user separately.
