# Report — local-comment-mode

Status: **done** (feature session, 2026-10-21, branch `dev/gsemet`).

## Intent traceability

| Intent (01-intent.md) | Delivered by |
| --- | --- |
| Highlight text, a floating button adds a comment there (as in Confluence) | T43: Comment button on a text selection (also Cmd/Ctrl+Alt+M) |
| A question/answer thread | T42 badges + popover, T43 reply box, T44 resolve/reopen/delete |
| Username from git config, overridable in a VS Code setting | T43: `markdownOkfSchemaStudio.comments.authorName`, else Git `user.name`, else OS user |
| Saved in a sidecar `same-name.comments.json` | T42 format (version 1), T43 write queue, T45 re-anchoring and rename |

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T42 | Threads from `<name>.comments.json` shown as badges on their blocks; popover with comments | `dade957` |
| T43 | Comment on selected text, replies; per-file write queue, refusal on invalid or dirty sidecar, every save answered, typed text kept until confirmed | `89d6513` |
| T44 | Resolve/Reopen, Delete with inline confirmation; "Orphaned comments" box after the content; quote fallback only for unique quotes ≥ 12 chars | `fea8ce5` |
| T45 | Re-anchoring: lines shift with edits, saved on document save only; quote search near old line then whole document (exact, normalised, bounded fuzzy with numbers/negations agreeing); doubtful → orphaned; sidecar follows renames | `f44d970` |

## Proof of completion

- Unit tests (model, anchoring: 27 cases incl. roles, cite, footnotes, entities, duplicates, CRLF, fuzzy limits), page tests, visual scenario `orphan-box-document-end`, trusted integration suites `commentWrite` and `commentAnchors`, real-input review-comments scenario.
- Reviews: T42 APPROVE r2, T43 APPROVE r2, T44 APPROVE r2, T45 APPROVE r2 (reviewer re-ran adversarial re-anchoring inputs).
- Phase 6 e2e (2026-10-21, `44d7f79`, unlocked): green in full: unit, contract, security, visual
  169 scenarios / 164 screenshots, every integration host including the keyboard suites, checkboxToggle,
  commentWrite and commentAnchors. (A first run with the screen locked stopped at checkboxToggle undo: environmental.)

## Open items

- Decision D30 to confirm: a thread whose quote vanished is orphaned even if a block remains at its line (the real-input t2 expectation changed accordingly).
- A line holding an opaque role (`{ref}`, `{cite}`) keeps its thread whatever the rest says; fuzzy matching ignores units (5 mg vs 5 g).
- Re-anchoring runs only while a preview is open (no watcher on closed documents).
- A comment message failing validation gets no answer; the page times out after 15 s.
- The orphan-box visual scenario builds its own markup (module markup covered by unit tests).

- Final gate: `just preflight` green in CI on `8c55e48` (run 39753045267); merged to `main` with PR #11 on 2026-10-22.
