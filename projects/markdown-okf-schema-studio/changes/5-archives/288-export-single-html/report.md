# Report — 288-export-single-html

Status: **done** (2026-11-11, branch `change-requests/288-export-single-html`, PR #365, merge commit `abc9e650`; no GitHub issue). Merged by the owner.

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Export a page as one self-contained HTML file, with an Export button in the toolbar main row (no sixth row) | `abc9e650` |

## Proof of completion

- Three rounds. Opus Inspector approved each round; a fresh Verifier returned VERIFIED at the final head 601e0bf1; `just check` passed; heavy run 43079731969 green after one rerun of failed jobs (known `alert-dropdown` stress flake and a `checkbox-toggle` integration timeout).
- Round 2 fixed the toolbar width assumptions (four buttons, 134 px): warning-banner reserve 124 to 156 px, SwRS MYST-081 and StRS TOOLBAR-001 updated. Round 3 made the v16 inline-code fixture robust (87 px margin at 460 px).

## Open items

- Backlog items filed by the Chief of Staff: export-html-drops-block-being-edited, static-export-mermaid-as-source, reload-campaign-watchdog-misses-hang, integration-checkbox-toggle-render-timeout.
- The real-input scenario `exportHtml` rests on a green real-input and integration step: CI logs print no scenario names.
- The remote branch `change-requests/288-export-single-html` is left for the owner to delete; its `-assets` branch is kept.
