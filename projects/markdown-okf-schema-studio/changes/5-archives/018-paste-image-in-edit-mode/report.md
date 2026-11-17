# Report — paste-image-in-edit-mode

Status: **done** (feature session, 2026-10-21, branch `dev/gsemet`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T38 | Pasting an image into an open block text box saves it next to the document as `image.png`, `image-1.png`, … and inserts `![image.png](image.png)` with the alt selected (one undo step); text on the clipboard wins; png/jpeg/gif/webp ≤ 10 MB with magic bytes checked; refused for read-only, unsaved and outside-workspace documents | `ae5bac0` |

## Proof of completion

- `pastedImage` unit tests (sniffing, spoofed type, free names); validator caps; webview tests; integration (file written, second paste `image-1.png`, refusals, untrusted folder unchanged, files removed in teardown). Review APPROVE r1.
- Phase 5 e2e (2026-10-21, `5eae169`, unlocked idle machine): green in full: unit, contract,
  security, visual 162 scenarios / 157 screenshots, every integration host including the keyboard
  suites (75 real-input screenshots), checkboxToggle, labelRename and blockMove (with its undo
  checks).

## Open items

- Only the page enforces "editor open" (D7); no per-preview paste cap; tiny overwrite race between `readDirectory` and `writeFile`.
- Manual check §9.5 (paste a screenshot; second paste; text wins).

- Final gate: `just preflight` green in CI on `8c55e48` (run 39753045267); merged to `main` with PR #11 on 2026-10-22.
