# Release v1.12.1: progress

2026-11-23, Chief of Staff.

- State: queued on top of batch-09's stack, after CR-479 (`heavy-preview-smoke-red`, the heavy
  CI regression on `main` since d762a732, bottom of the stack), CR-477 (`raw-text-opens-studio`, the urgent
  revert, Driver running, bottom of the stack on `main`), CR-475 (`save-guard-never-hangs`, round
  3/3, PR #492) and CR-476 (`blank-line-block-per-line`, waits for CR-475).
- Ships: the three CRs above and what is on `main` since v1.12.0 (CR-474, PR #491).
- Approvals: the owner merges the stack with the version PR. Tag, GitHub release and Marketplace /
  Open VSX publications are approved in advance (release-Q4), recorded with `order approve` at the
  merge. Issue comments (step 8) keep one owner approval; the announcement is the owner's.
