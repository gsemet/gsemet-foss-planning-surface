# Flaky real-input test: Quick Open lands in the locked editor group

A flaky real-window test turned `main` CI red. Filed on 2026-11-26 from the Chief of Staff session of
batch-09, as the project's rule asks for a failure the change does not touch.

Facts:

- Run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45853781390, commit 5f0746d
  on `main` (the merge of https://github.com/gsemet/markdown-okf-schema-studio/pull/535), job
  `integration`, step `real-input` (380458 ms):
  `AssertionError [ERR_ASSERTION]: the user's lock survived: Quick Open from the locked group opened
  elsewhere`, `2 !== 1`, in `scenarioPreviewGroupLock`
  (`test/integration/realInput/previewWindow.ts`, line 609 at 5f0746d). `report` and `checks` failed
  after it.
- The assertion expects the file opened by Quick Open in view column 1; it was in column 2. In the
  scenario, column 2 is by then the user's locked group (the preview's group between them closed).
- The same tree passed the heavy run of the pull request's head 223a8c4
  (https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45840378393).
- The previous `main` run passed (45838037906, e2b2235). `git diff --stat e2b2235 5f0746d` shows 19
  files: preview styles, unit and visual tests and fixtures, no extension-host or editor-group code.
- The failed jobs were not re-run.
- The two earlier failed `main` runs looked at (45580228461, 45243684146) do not show this
  assertion.

Not examined: whether the race is in the product (the lock lost or set late) or in the test (it does
not wait for the lock before Quick Open). Rule 12 of `.agents/guidelines/ci.guidelines.md` applies: a
flake is a bug, fixed at its cause and proved by repetition, never by a retry or a longer timeout.
