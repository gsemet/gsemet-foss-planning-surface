# Report — move-block-up-down

Status: **done** (feature session, 2026-10-21, branch `dev/gsemet`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T05 | Included blocks: line ranges clamped to the `{include}` directive, blocks marked `data-sphinx-preview-included` | `ef1dbce` |
| T36 | ↑/↓ on the "+" insert bar swap the block above with its neighbour in one undo step; the block stays under the pointer; refusals (read-only, open editor, stale, include, non-blank text between) shown next to the bar | `5293923` |
| T37 | Alt+↑/↓ moves the focused block; Cmd/Ctrl+Alt+↑/↓ in the text box saves, moves and reopens the editor at the same caret; key repeat ignored during a move | `a57ddf1` |

## Proof of completion

- `planBlockMove` unit tests (LF/CRLF, final newline, glued blocks, separators, frontmatter, round trip); host integration with one-undo checks; scroll scenario (two moves keep the block within 3 px).
- Reviews: T36 APPROVE r1, T37 APPROVE r1.
- Phase 5 e2e (2026-10-21, `5eae169`, unlocked idle machine): green in full: unit, contract,
  security, visual 162 scenarios / 157 screenshots, every integration host including the keyboard
  suites (75 real-input screenshots), checkboxToggle, labelRename and blockMove (with its undo
  checks).

## Open items

- A move can add a blank line, so move-and-back is an exact identity only for blank-separated blocks.
- Ctrl+Alt+Arrow may clash with AltGr layouts on Windows/Linux; check the focus ring on the moved block.
- No screenshot of the move buttons (light/dark/cream).
- Manual check §9.2 (Alt+Down twice; Cmd/Ctrl+Alt+Up in the text box).

- Final gate: `just preflight` green in CI on `8c55e48` (run 39753045267); merged to `main` with PR #11 on 2026-10-22.
