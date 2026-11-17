# 169 — Heavy CI regression: find-in-preview stalls (match count / replace blocked by an open edit) (HOTFIX)

Type: fix · Priority: P1 · Release 1.0.0 blocker · Approved by the user via the Chief of Staff,
2026-10-28 (same basis as CR 168: release blocker, no new scope) · From `origin/main` eca17c42,
one small PR, not stacked.

## Problem

`test/integration/findInPreview.test.ts` (trusted suite) fails twice on main `eca17c42`, at the
same step (compiled lines 227–228), after passing on `b71fac7c`:

1. https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40743462032 —
   "Timed out waiting for the match count" (`waitFor` for `/^1 of \d+$/`, test source ~145/203).
   Log: `reports/heavy-eca17c42-run1-integration.log` (lines ~1293–1313).
2. https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40744401718 —
   `[data-find-toggle-replace]` stays `aria-disabled` with the title "Save or cancel the open edit
   before replacing.": a block edit is still open when the replace step starts.
   Log: `reports/heavy-eca17c42-run2-integration.log`.

The trusted suite stops there, so the real-input suite does not run (blocks the README
real-window pictures and the 1.0.0 heavy gate).

Changes since green `b71fac7c`: #179 (requirement schemas, no product code), #180 (headless visual
harness + README picture), #181 (`78a625a9` + `eca17c42`: table menu `position: relative;
z-index: 3`, the only product change).

## Lead to check first (Chief of Staff)

A positioned, raised table menu can now sit over a neighbouring element and take its click. If an
earlier find step, or a prior test in the trusted suite, clicks near a table to close an edit, the
click may land on the menu and leave the edit open. Both symptoms fit a click going astray. Prove or
exclude it with the page state at the failure (open edit? which element received the click? menu
rect vs the click target).

## Decisions

- Diagnosis first; fix product or test race (CR 159 was a test race in this same file); no
  weakened assertion, no retry loop, no `force: true`.
- Local reproduction: headless or unit only. Real-window tests stay forbidden locally (standing
  constraint), so "run the spec locally against b71fac7c vs eca17c42" is done, if needed, as heavy
  CI on the CR branch (and at most one comparison heavy on a branch at b71fac7c), never in a local
  VS Code window.
- If the cause is #181's menu, keep #181's fix (menu above the handles) and its tightened r06
  assertion green; fix the stacking scope instead (e.g. the menu only raised where it overlaps the
  handles, or not covering the click target).
- Keep green: tableMoves, TABLE-064, Edit figure clearance, the five rows, motion.
- Gate: `just check`, normal CI, heavy CI with integration green (stress verdict reported, not
  fixed here).
