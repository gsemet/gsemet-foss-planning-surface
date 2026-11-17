# Report — 058-image-paste-empty-file

Status: **done** (2026-10-24, [PR #53](https://github.com/gsemet/markdown-okf-schema-studio/pull/53),
rebase-merged; main at abc2f21).

- Cause: `workspace.fs.writeFile` creates the file empty then fills it; the stress test read the gap.
- Fix: write a hidden `.partial` file, rename without overwrite, delete on failure; `delete` added
  to the file-system port; the test waits for the image link; failure diagnostics added.
- 1/3 rounds, APPROVE; heavy [run 40067865564](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40067865564)
  stress image paste 20/20.
- Internal id removed from a test comment at landing.
- Follow-ups filed in backlog P2: paste-diagnostics-race, paste-partial-leftover, paste-name-race-message.
