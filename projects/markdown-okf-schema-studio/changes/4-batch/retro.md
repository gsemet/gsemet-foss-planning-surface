## 2026-11-17 · CR-336, CR-338, CR-339 (batch-05)

- [project] tableBreakout.test.ts:398 asserted a layout that depends on the page font's natural table width (705 px with Segoe UI vs the 727 px a 760 px pane allows), so it was red on Windows on main and made `just preflight` fail for every change until CR-339: long-term fix: tests do not assert font-dependent layout, or pin the font.
- [chantier] `take` and `ship` expect the CR's archive in the PR (`archive missing from the PR` on every CR) although the project gitignores .agents/changes, so each Driver was told by hand not to add one: long-term fix: set `Repo.archive_in_pr` from the project's settings so take and ship skip the archive.

(critic: kept 2, dropped 1)
