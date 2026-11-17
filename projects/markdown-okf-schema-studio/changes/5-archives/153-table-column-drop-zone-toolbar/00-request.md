# 153 — Table column drop zone works again with the Fold toolbar button (heavy integration fix)

Type: fix · Priority: P1 · From the user, 2026-10-28 (fix forward from main, no revert)

## Intent

Heavy CI integration fails on `main` since "feat(preview): fold and unfold sections under headings"
(#151, merge f7b17518) in `test/integration/tableMoves.ts`, column drop zone scenario: "the marker
shows after the third column while the pointer is in the handle strip". Main was green before
(run 40668487526); after: #166 on f7b17518 fails only on this test (run 40675571987); the heading
folding branch failed it before merging (runs 40640639724, 40656120188). Hypothesis (unproven): the
6th toolbar button (Fold) widens the floating toolbar so it overlaps the table handle strip at the
integration window size, or shifts the geometry the test aims at.

## Decisions (user)

- One independent PR on `main`, from fresh `origin/main`; fix forward.
- Reproduce first (heavy CI on the unchanged branch); real-window geometry check.
- No retry loop and no weakened assertion. If the product is right and the test aims wrongly, fix
  the test's pointer path and say why; if the toolbar overlaps the strip, fix the product.
- Requirements traceability as usual (okfreq 0.16: `just requirements-update`, new requirements with
  `okfreq new ... --lifecycle proposed`).
- Gate: `just check` green and heavy CI integration green on the branch; stress ignored.

## Scope extension (user, 2026-10-28, via main)

Rearrange the floating toolbar into 4 rows: (1) reload / link / edit mode; (2) navigation + zoom;
(3) theme, layout, TOC; (4) NEW: fold, diff, comments. Replace the one-rule CSS workaround if the
new layout makes it unnecessary, but keep the table handle strip clear (tableMoves heavy scenario
must pass). Update unit tests, visual layout checks (incl. warning banner reserve, e.g.
myst/v32-conf-warning-banner-narrow-dark-460), StRS/SwRS toolbar requirements (ask before changing
any `approved` one), docs/user/toolbar.md and other user docs; refresh PR screenshots (light+dark,
before/after) on the -assets branch; update PR title/body; heavy + normal CI.

## Scope 2: five-row toolbar (user, 2026-10-28, via Chief of Staff)

Replaces the four-row layout of the scope extension above. Fresh scope: round budget 3 again
(round 1/3 of scope 2), per the user's instruction relayed by the Chief of Staff.

Rows, mapped to the real buttons in `src/core/preview/previewToolbar.ts`:

| Row | User's words | Buttons |
| --- | --- | --- |
| 1 (always visible) | refresh, edit, fold other lines | Refresh, Edit, toolbar collapse ("Hide view controls") |
| 2 | linked to side panel, previous / next page | Anchor, Back, Next |
| 3 | theme, zoom in / out | Theme, Zoom out, Zoom in |
| 4 | layout, table of contents | Width, TOC |
| 5 | section collapse, diff, comment | Fold all sections, Diff, Comments |

Reading (Foreman, autonomous): "fold other lines" is the toolbar collapse button, which folds rows
2–5; "section collapse" is "Fold all sections". This places all 14 buttons once, none left over.
Rows 2–5 stay in the group the collapse button hides; Tab order follows the rows.

Owner approval: the owner APPROVED on 2026-10-28 changing the approved toolbar requirements
(StRS/SwRS) for this layout change. Record it in `requirements/tiers/log.md`; set `approved_by` /
`approved_on` (2026-10-28) on any approved requirement changed; list them in the PR body under
"Approved requirements changed".

Must stay green: the tableMoves handle-strip overlap fix (heavy integration passed on 59f0c329,
run 40700884217) and the warning-banner reserve. Known red on 59f0c329 (normal run 40700890317,
visual job): `palette-slash/v04-palette-not-sticky-narrow-dark-360` and
`check_edit_palette_tall` on `05-long-chapter--dark--sticky-3--default.html` at 360 px (palette
bar bottom 354 vs frame top 362: gap 8 px > 6). The stopped round-3 coder had only added debug
prints for the latter (left uncommitted in the worktree; not part of the change).
