# Report — 048-local-undo-macos

Status: **done** (2026-10-23, branch `fix/local-undo-macos`, PR #45, merged by the user, merge commit ea8759d).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Each real-window suite brings its VS Code window to the front on macOS and waits for `window.state.focused`, failing fast with diagnostics on a locked screen; slash-menu step waits for page settle and caret, with diagnostics and a stress entry; `STUDIO_VSCODE_EXECUTABLE` picks a local build | PR #45, ea8759d |

## Proof of completion

- Full local `npm run test:integration` on macOS: 123 pass, 0 fail.
- CI checks run 39999525511 pass; heavy real VS Code run 40000506165 pass.
- Reviews: T1-r1 FIX-REQUIRED, T1-r2 APPROVE.
- Root cause: the test window launched in the background on macOS, so VS Code had no focused editor (undo, cursor commands, typed keys ignored). Not a product bug, not the VS Code version (1.143.0 and 1.143.1 renderer identical but the version string).

## Open items

- One unexplained failure in 8 isolated `--reload-only` runs (candidate backlog item).
- Slash-menu timeout not reproduced in ~15 runs: guarded, cause unproven.
- Commit guideline asks for `Assisted-by`, history uses `Co-Authored-By`: to align.
