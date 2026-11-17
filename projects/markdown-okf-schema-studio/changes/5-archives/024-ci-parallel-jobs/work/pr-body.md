## Summary

The CI ran every stage in one job, in sequence: 11 to 18 min per PR, about 5 min of that visual
and 4 min 40 integration. They now run as **parallel jobs**. Each job calls `just dev-ci`, then one
`just ci-<name>` target that runs the same way locally. This follows
`.agents/guidelines/ci.guidelines.md`.

```text
static ─────────────┐
visual ───┐         ├─> checks   (stable name for branch protection)
integration ┴─> report ┘
gallery (manual: workflow_dispatch, gallery=true) <- report
```

| Job | Target | Notes |
| --- | --- | --- |
| `static` | `just ci-static` | justfile format check, `check`, `sphinx-check` |
| `visual` | `just ci-visual` | headless Playwright, no xvfb |
| `integration` | `just ci-integration` | VS Code under `xvfb-run` |
| `report` | `just ci-report` | merges both e2e artifacts, writes the e2e manifest and JUnit |
| `gallery` | `just ci-gallery` | only on a manual run with `gallery: true` |
| `checks` | — | fails unless every job above succeeded |

## Changes

- `justfile`:
  - new targets `dev-ci` (CI-only setup from the lock files), `ci-static`, `ci-visual`,
    `ci-integration`, `ci-report` and `ci-gallery`;
  - `preflight` runs `clean`, `format`, then the `ci-*` targets in sequence. It keeps the same
    coverage and still reports the failed count.
- `scripts/e2e-campaign.mjs`: each e2e stage records its own campaign file with a real start time.
  - CI shares the run id (`run_id-run_attempt`). Locally, a stage reuses a sibling's id only when
    it is less than 2 h old.
  - Re-running a stage deletes its old evidence, so a report can never validate stale results.
  - `ci-report` fails clearly when a stage is missing or the two stages started more than 2 h apart.
- `validateReviewEvidence`: an optional per-stage identity. The default keeps the single-campaign
  behaviour, so `npm run test:e2e` is unchanged.
- AGENTS.md and CONTRIBUTING.md: the new targets.

No UI change, so no screenshot. The job graph above is the visible result.

## Test plan

- [x] New `test/site/e2eCampaign.test.ts` (4) and a split-identity case in `reviewEvidence.test.ts`.
  They fail on the previous code.
- [x] Local: `just ci-static`, `just ci-visual`; `just ci-report` fails clearly without the
  integration stage and passes with a faked one; justfile format check; `--dry-run` of `dev-ci`,
  `ci-integration` and `preflight`.
- [x] Sonnet review: rounds 1 and 2 asked for fixes (epoch start time, standalone stages, stale
  campaign reuse); round 3 approved.
- [ ] CI: this PR's own run exercises the new workflow (parallel jobs, artifact merge, `checks`).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
