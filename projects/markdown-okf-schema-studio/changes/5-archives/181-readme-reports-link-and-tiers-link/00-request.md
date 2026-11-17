# 181 — README: drop the Reports index link; requirements page: link `requirements/tiers/`

Type: docs/site · Priority: P1 (quick) · User request via the Chief of Staff, 2026-10-29 ·
Standalone PR from origin/main, not stacked. Normal CI only.

1. README.md line 7: remove "| [Reports index](https://gsemet.github.io/markdown-okf-schema-studio/reports/)"
   from the top link bar (user: useless). Keep the Marketplace, gallery and Requirements links.
2. test/site/requirementsPage.ts ~line 365, section "Browse the requirements": make
   `requirements/tiers/` a link to
   https://github.com/gsemet/markdown-okf-schema-studio/tree/main/requirements/tiers, keeping the
   `<code>` styling inside the link if the page style allows. Assert the link in
   requirementsPage.test.ts.
3. Find other links to the reports index (site nav, docs, README badges): do NOT remove them; list
   them in the PR body.

Note: the main checkout holds uncommitted user edits to README.md on release/1.0.0; this PR changes
one line of README on main; mention the line in the PR so the user can reconcile.
