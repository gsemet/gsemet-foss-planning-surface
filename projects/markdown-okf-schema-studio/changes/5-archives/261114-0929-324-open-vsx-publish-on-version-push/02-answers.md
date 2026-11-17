# Answers

## 2026-11-14: picked, fix everything and release again

Owner, 2026-11-14: « oui je pense qu'il faut tout corriger et retenter une release ». The three
fixes from the v1.9.0 release go into batch-04, followed by a release CR for v1.9.1. Priority P1.

Decided by the Chief of Staff (no user impact):

- Keep the open-vsx.org registration as it is (`release.yml`, environment `release`): only one
  trusted publisher is allowed per extension, and the recovery dispatch must keep working.
- Change how the version push runs the publish so the OIDC token names `release.yml`. The
  preferred direction is that `tag-release` (or the job after it) dispatches `release.yml` with the
  tag instead of calling it with `workflow_call`; the spec-writer checks what else hangs on the
  called job (Pages, the GitHub release, run reporting, permissions such as `actions: write`) and
  may pick another path that meets the same goal.
- The recovery path (a manual dispatch of `release.yml` with the tag) keeps working unchanged.
- A test in `test/build/test_workflows.py` pins the chosen wiring.
- The real proof is the v1.9.1 version push: the release CR checks that its Open VSX step is
  green without any recovery dispatch.
