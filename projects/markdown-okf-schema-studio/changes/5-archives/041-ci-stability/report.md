# Report — 041-ci-stability

Status: **done** (2026-10-23, PR #35, merge commit fdc88cf). Ready after one green CI run instead
of three (user decision 10, speed).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | 041 — ci-stability (coder reports in `reports/`) | PR #35, fdc88cf |

## Proof of completion

- CI run 39955908306: all jobs green on 9d2e885.
- Reviews: T1-r1..T1-r4: Verdict: APPROVE.
- Details of tests, gate counts and screenshots: `reports/` and `reviews/`.
- Note: one green run was accepted instead of three consecutive runs (user decision 10, speed).

## Open items

Follow-ups, non-blocking:

- Stale comment in `ci.yml` near "Require every check job to pass": `stress` is no longer required.
- The apt cache is saved even when no .deb was downloaded, and `ImageOS` is missing from the cache
  key.
- `pages.yml` still installs from the live Ubuntu mirror.
- IME composition checks on cell Enter and on frontmatter Escape/Enter.
- Root cause of the visual `firstClearance` flake is still unknown.
- Verify and close `backlog/P1/flaky-linked-target-watcher`.
