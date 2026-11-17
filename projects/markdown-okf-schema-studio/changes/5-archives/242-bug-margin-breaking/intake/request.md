# 242 — Tables stay in the column when they fit, and break out when they need to

Type: fix · Priority: P1 · Approved by the owner on 2026-11-03 · Worktree
`../markdown-okf-schema-studio-wt-242`, branch `change-requests/242-bug-margin-breaking`.
Part of the stacked run of 2026-11-03 (afternoon), before release 1.3.0.

## Intent

See [01-intent.md](../01-intent.md) and [related-unnecessary-table-margin-breakage/01-intent.md](../work/related-unnecessary-table-margin-breakage/intent.md) (with its owner-reviewed [prototype](../work/related-unnecessary-table-margin-breakage/prototype.html)).

## Owner decisions (2026-11-03)

- One CR for both items: apply variant D of the prototype, in Auto width mode only.
- A token column (every cell inline code, a number, a date, or at most three words) never wraps; its minimum width is its widest cell. A prose column needs about 20ch.
- The table stays in the column when the minimums (plus padding) fit; otherwise it breaks out to its natural width, capped by the page.
- A cell holding content that cannot shrink (a code block, an admonition with a code block, a long unbroken line) makes the table break out (screenshot of this item).
- Expected verdicts at 720 px: stays for prototype cases 1, 2, 3, 4, 8, 9; breaks out for 5, 6, 7, 10, 11, 12.
- 2026-11-03 (later): the minimum prose column width is 24ch (not 20ch), so prototype case 6 breaks out as decided.
- 2026-11-03 (later): rounds: 5. The owner grants 2 more rounds to fix the red visual scenarios v26 and v27 (breakout table, Auto width, 900 px): diagnose first, never weaken a test without the owner.
- 2026-11-03 (later): round 5 may rewrite the three Description cells of `test/visual/fixtures/63-breakout-table-handles.md` as multi-word prose (fixture input only; no scenario or assertion change). Before/after screenshots of v26/v27 in the PR body.
