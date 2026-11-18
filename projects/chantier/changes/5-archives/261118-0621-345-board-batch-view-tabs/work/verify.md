Head: 15359cc8b32b39b099134947565bf3834aca52a4

Verdict: VERIFIED

Move judged: 7f075653..15359cc8, a restack onto CR-344 (03ee16df, brings CR-343's PRs page) with a conflict resolved in skills/chantier/scripts/cli/src/chantier/board/web/js/core/router.js (work/conflicts.md; fast gate `just check` passed there). Previous judgment: VERIFIED at 7f075653 (kept as work/verifier/verify-7f07565.md).
Method: real Chromium (Playwright), board served from the worktree at 15359cc8 on a scratch surface (scripts/docs_screenshots.py make_surface/start_board, fixed clock, UTC; no real planning surface). Script work/verifier/tabs-15359cc.py.txt, raw output work/verifier/tabs-15359cc.log. No screenshots taken, so no path or username on any image. `git rev-parse HEAD` in the worktree: 15359cc8b32b39b099134947565bf3834aca52a4.

1. Batch tabs and URL (15359cc8). Output: opening `p=shop-api&v=batch` gives URL `p=shop-api&v=batch` (default tab omitted), tabs [Graph, Gantt, Time cards]. Click Gantt -> `p=shop-api&v=batch&t=gantt`, aria-selected gantt; click Time cards -> `...&t=cards`; click Graph -> `p=shop-api&v=batch` (t dropped). PASS.
2. Reload and copied link (15359cc8). On `&t=cards`: reload keeps `p=shop-api&v=batch&t=cards`, tab cards selected, `.tcards` rendered (1); the same URL opened in a fresh page selects cards. PASS.
3. "All projects" clears it (15359cc8). From `&t=cards`, picking the surface row gives `p=*&v=home` (no t); a fresh batch open afterwards is `p=shop-api&v=batch`. PASS.
4. PRs page state filter and sort (15359cc8), project mobile-app (closed batch, rows from the record). `v=prs` -> `p=mobile-app&v=prs`; click state `open` -> `...&v=prs&st=open`; click sort `activity` -> `...&st=open&sort=activity`; reload keeps that URL with chips data-pvf-open and data-pvs-activity pressed (restored from the URL); state `all` -> `...&v=prs&sort=activity` (st dropped); picker "All projects" from PRs -> `p=*&v=home` (st and sort cleared). Chips: states all/open/draft/merged, sorts batch/opened/activity/cr. PASS.
5. Carried from 7f07565: the Gantt layout (grid minimum, now line and crosses inside the box at 1400 and 390 px), the lazy modules, Gantt/time-card data, stamps, chips, FR, closed batch. Reason: the move touched only router.js's conflict (proved by claims 1 to 4); batch-gantt.css and the Gantt's own files are unchanged by the conflict resolution (only router.js conflicted per work/conflicts.md). The base brought CR-343/344 (PRs page, design rules, Kanban card, Gantt fit), not re-run beyond the tab checks above.
6. Not re-checked at this head: the PR description and the Review box (not requested by the brief); `just check` passed per work/conflict-resolver/check.log.

VERIFIED
