# 171 — GFM alert shifts block source lines (data-loss HOTFIX) — report

Landed 2026-10-28. PR https://github.com/gsemet/markdown-okf-schema-studio/pull/185 merged as
`a8267570` (before the heavy run; user decision: in 1.0.0, merged before the version PR).

## Outcome

- Cause: `expandGithubAlerts` rewrote each alert into a longer MyST admonition before parsing and no
  pass mapped lines back: blocks inside an alert were +1, blocks after it +1 per alert above. Lead 1
  (on-disk edit) not needed. Data-loss: the host trusts page line numbers; open/Done, cut, copy,
  move acted on the wrong lines.
- Fix: the rewrite records the source line of each output line; a tree pass maps start/end lines
  back (also unclosed-fence diagnostics and context-tag bodies). SwRS GFM-009 (proposed) gains the
  "every block keeps the document's lines" scenario; CORE-003, MYST-096 verification notes.
- 17 new tests fail on the old sources, pass on the fix (`alertSourceLines.test.ts`,
  `alertBlockEditOpen.test.ts`). Fixture is synthetic (round 1 FIX-REQUIRED: it copied the user's
  unpublished README; round 2 APPROVE).

## CI

- Normal: run 40772741465 green.
- Heavy on branch: run 40774494253 — stress, visual, static green; integration cancelled (30 min
  timeout) by the hang right after the coexistence check (same as #183 heavy #1). Proof re-run as
  heavy on main b723e176: run 40778738577.

## Follow-ups (backlog)

- P1 `ci-integration-hang-after-coexistence` (2 of 5 recent heavy runs).
- P2 `host-guard-block-range` (defense in depth).
- P2 `alert-inside-colon-container-closes-it`.
- P3 `sphinx-build-alert-line-shift`.
- Question: BLOCK-014 (admonition body opens whole directive) vs GitHub alert opening only the
  paragraph.
