# Task T1 — Motion for the floating toolbar and its tooltips

Implement `00-request.md` (decisions taken by the user; do not re-grill) in
`../markdown-okf-schema-studio-wt-162` on branch `change-requests/162-toolbar-motion` (from
`origin/main`, own `npm ci`). Runs in parallel with CR 161 (toolbar geometry hotfix): rebase on
main when that merges.

## Definition of done

- Shared tooltip slide-in (left ≈6 px + fade ≈120 ms) for main toolbar, edit palette, table menu.
- Rows 2–5 expand/collapse as one block (height + fade ≈160 ms).
- Load hint on every new preview opening when saved state is collapsed; never on patch, refresh or
  reload of the same preview; cancelled by any pointer/key press; preference unchanged.
- `prefers-reduced-motion: reduce` disables all three (SwRS-MDOKFSTUDIO-CORE-050, `motion.ts`).
- Unit tests (fail before), visual checks stay green, SwRS/StRS updated (ask before changing an
  approved requirement), docs/user/toolbar.md, CHANGELOG.
- PR evidence: before/after GIF or screenshot sequence on the `-assets` branch.

## Gates

- `just check`; `just requirements-update`; `okfreq validate --check-links --project-root .`.
- Normal CI, then heavy CI (`gh workflow run ci.yml --ref <branch> -f heavy=true`).
