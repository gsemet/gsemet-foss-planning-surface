## Summary

Two short guidelines for agent sessions, linked from `AGENTS.md`:

- `.agents/guidelines/prd-workflow.guidelines.md`: how a backlog item becomes a change request
  (PRD folder), then one green PR with docs, e2e and screenshots, then an archive with a report.
  It covers sub-agent roles (Sonnet implementer and reviewer), PR screenshots through a
  `pr-assets/<n>` branch (raw blobs, LFS-safe) and parallel CRs in git worktrees.
- `.agents/guidelines/ci.guidelines.md`: the CI only calls `just dev-ci` and one `just ci-<name>`
  target per job, every target is reproducible locally, and there are no retries to hide flaky
  tests.

Both are written to apply to similar projects. Project specifics stay in `AGENTS.md`.

No code change, so no screenshot.

## Test plan

- [ ] CI `just preflight` green (docs only).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
