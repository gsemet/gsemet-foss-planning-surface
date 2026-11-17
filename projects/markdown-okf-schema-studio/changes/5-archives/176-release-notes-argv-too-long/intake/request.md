# 176 — Release fails: release notes prompt exceeds the argv limit (HOTFIX, release 1.0.0)

Type: fix (release tooling) · Priority: P1, top · Approved by the user via the Chief of Staff,
2026-10-28 · From `origin/main`, ONE standalone PR (not in the night stack). Normal CI is enough.

## Problem

Release VSIX run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40780555553
(tag v1.0.0, b723e176) failed in `package` → "Generate user-facing release notes":
`OSError: [Errno 7] Argument list too long: 'gh'` at `scripts/release_notes.py:164`. `main()` passes
the whole prompt + `release_context(...)` (the full history for a first release) as one argv element
to `gh copilot -- --prompt`, above Linux MAX_ARG_STRLEN (~128 KiB). Nothing was published (failed
before vsce). Log: `reports/release-40780555553-failed.log`.

`release.yml` checks out the TAG and runs `scripts/release_notes.py` from it, so a fix on main alone
cannot release v1.0.0.

## Fix (Chief of Staff decision)

1. `scripts/release_notes.py`: write the Git context to a file in the workspace; keep the argv prompt
   short and tell the agent to read that file (view/read tools are already allowed). Unit test: argv
   stays under a size bound for a context of several MB.
2. `release.yml`: on `workflow_dispatch`, the release tooling (`scripts/release_notes.py`) comes from
   the workflow's own ref (`github.sha`), not from the tag (e.g. check out the workflow ref into a
   `tools/` path, or `git show "$GITHUB_SHA:scripts/release_notes.py"`). Package, verify and publish
   keep using the tag checkout. New `workflow_dispatch` input `notes`: `generated` (default) or
   `placeholder` (writes a one-line `release-notes.md`; hand-written notes replace it afterwards).
3. Test that a `workflow_dispatch` of `release.yml` from main with `tag=v1.0.0` passes the tag
   verification (HEAD == tag commit, tag in main, version matches) — workflow test in
   `test/build/test_workflows.py` / `test_release.py` style.

After merge, the Chief of Staff runs
`gh workflow run release.yml --ref main -f tag=v1.0.0 -f notes=placeholder`.

## Gate

`just check`; normal CI. PR for an external reader; tell the Foreman when green.
