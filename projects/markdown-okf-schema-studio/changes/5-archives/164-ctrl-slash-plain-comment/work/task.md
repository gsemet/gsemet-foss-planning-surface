# Task T1 — Ctrl+/ toggles a plain HTML comment

Implement `00-request.md` (user decision taken; do not re-grill) in
`../markdown-okf-schema-studio-wt-164` on branch `change-requests/164-ctrl-slash-plain-comment`
(from `origin/main` d48739d7, own `npm ci`). Part of release 1.0.0 (CR 163).

## Definition of done

- Ctrl+/ (Cmd+/) in the block editor (and the table cell editor if it shares the binding) toggles
  `<!-- … -->` around the current line or the selected lines, one undo step; toggling off removes
  what Ctrl+/ adds (decide the TODO-wrapper case autonomously, list it).
- The palette TODO button still inserts `<!-- TODO: … -->`; its tooltip no longer shows Ctrl+/.
- Tests that fail before the change; the existing SwRS amended (ask before changing an `approved`
  one); user docs; the Unreleased CHANGELOG entry rewritten; every tooltip/help showing the shortcut.

## Gates

- `just check`; `just requirements-update`; `uv run --group requirements okfreq validate
  --check-links --project-root .`.
- Normal CI, then heavy CI (`gh workflow run ci.yml --ref <branch> -f heavy=true`); heavy
  integration on main is currently red in editToolbarCover (fixed by CR 161): report it as "also
  red on main" if it is the only red.
