# Before / after

No user-visible change, so no screenshots. Base (before) origin/main 116f39d8; after acc957944b82a2c4404a6a27bf00870d7c64d4df.

- Static boundaries: before, `.dependency-cruiser.cjs` NODE_DEBT lists `fs` for fileLinks.ts and stemIndex.ts; after, `path` only. Reproduce: `git diff origin/main...HEAD -- .dependency-cruiser.cjs`; `just check-boundaries` passes.
- Not captured: cold stem-index build timing (old sync vs new async) and visual/e2e before-after; the visual job passed in CI, integration runs in the heavy workflow.
