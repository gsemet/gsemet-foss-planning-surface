# index: concept description changes never reach index entries

Split from CR `57-index-broken-root-links` (its answer index-links-Q6, 2026-11-25).

`okf-schema index` keeps an existing index entry's description over the concept's frontmatter
description. Verified on `origin/main` 2f09cef (0.18.1): index a bundle whose `a.md` has
`description: first`, change it to `description: second`, run `index` again: the entry still says
"first". OKF 0.2 section 8 says entries SHOULD include the description from the linked concept's
frontmatter.

To decide when this item is grilled: what `index` keeps of hand-written entry text, and what the
frontmatter replaces. The same "preserved once written" rule applies to a subdirectory's
introduction copied into the parent index.
