# Task T1 — make the replace-all check wait for the final status

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-159
(branch change-requests/159-find-in-preview-heavy-regression). Read 00-request.md (diagnosis) and
rules.md first. Constitution: .agents/constitution.md.

## Change

`test/integration/findInPreview.test.ts`, "Replace all" step:
- After `waitFor("the document to change", ...)`, wait until the page's `[data-find-note]` is the
  final answer of the host, i.e. it is no longer the transient "Replacing..." status (the page sets
  it when the request leaves and replaces it when `previewFindReplaceResult` arrives, after the
  edit is applied). Use the existing `waitFor` helper on the note text (readiness signal the page
  reports, not a sleep); on timeout the error must say what the note and the document held.
- Then keep the existing assertion `/cannot be replaced from the preview/` (do not weaken it). It is
  fine to also assert the note starts with "Replaced 2 matches" if that is what the product says
  (check `runReplace` in src/page/modules/findBar.ts and the SOURCE fixture; only add it if sure).
- Look for the same race elsewhere in this file (any note/status read right after a document
  change) and fix it the same way. Do not touch other test files.

## Requirements

No behaviour change. Keep the `@tests_req SwRS-MDOKFSTUDIO-TOOLBAR-012` marker. Add a dated
entry (2026-10-28) in `requirements/tiers/log.md` (follow the file's existing format) saying the
real-window replace-all check of SwRS-MDOKFSTUDIO-TOOLBAR-012 now waits for the host's answer
before reading the status. Run `just requirements-update` and
`uv run --no-sync --group requirements okfreq validate --check-links --project-root .`.

## Gates (foreground; NEVER run real-window tests: no `npm run test:integration`, no ci-integration)

- `fnm exec -- npm run compile` (or `just compile`) — the test must type-check.
- `just check`
- requirements commands above.

## Report

Write reports/T1-r<n>.md in the PRD folder
(/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/03-requests/159-find-in-preview-heavy-regression/).
