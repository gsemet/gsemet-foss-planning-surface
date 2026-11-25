# index: regenerating an index drops authored sections and the root intro

From the OKF 0.2 compliance check of `origin/main` 2f09cef (0.18.1), 2026-11-25. Filed on the
user's yes, not grilled. Spec text: `skills/okf-schema/references/okf-v0.2.md` (the upstream text).

OKF 0.2 section 8: "The body uses one or more sections, each grouping concepts under a heading".

Observed with `okf-schema index`:
- A `tables/index.md` with `# Tables`, `## Core` (one entry) and `## Other` (one entry
  `* [Sub](../sub/) - other`) becomes `# tables` with `## Core` and one entry: the second section
  and its entry are gone, and the title is replaced by the folder name.
- A root index with `# Root` and an introduction paragraph is rewritten with the folder name as
  title and no introduction (`api.py:1089` and `1114`: the introduction is kept for non-root
  directories only).

The result is still a valid section 8 index, but authored content is lost.

Related: CR `57-index-broken-root-links` (batch-01) covers subdirectory summaries only; inbox item
`index-stale-descriptions` covers entry descriptions that are never refreshed.
