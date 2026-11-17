# Report — find-in-preview-heavy-regression

Status: **done** (2026-10-28, branch `change-requests/159-find-in-preview-heavy-regression`,
PR [#172](https://github.com/gsemet/markdown-okf-schema-studio/pull/172), merge commit
`a4338277`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | `findInPreview` "Replace all" step waits for the host's final answer in the find note before asserting; assertion unchanged; log entry for SwRS-MDOKFSTUDIO-TOOLBAR-012 | `001c1636` |

## Proof of completion

- Cause: test race (the wait on the document change ended before the host's answer reached the
  page, so the read saw "Replacing..."); product correct.
- Local: `npm run compile` OK; `just check` exit 0; `just requirements-update` 0 changes;
  `okfreq validate --check-links` exit 0.
- CI: normal [40700506976](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40700506976)
  pass; heavy [40700773622](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40700773622)
  passed `findInPreview` and stopped at the known `tableMoves` regression (fixed by
  [#167](https://github.com/gsemet/markdown-okf-schema-studio/pull/167)). Screenshots: none.

## Open items

- None. Worktree `../markdown-okf-schema-studio-wt-159` and its branch are not removed yet
  (deletion needs the user's permission, like the other landed CRs' worktrees).
