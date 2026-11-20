Short name: `share-cards`

From the owner's request (2026-11-20, X screenshots): the category page should say "A Feature category
for Markdown OKF Schema Studio" instead of the bare site name; a use case page "un text special mais une
image generic pour tous les MyST"; behaviour pages had no card. The rest decided by the Chief of Staff
under the owner's autonomy rule ("tu es maintenant autonome. plus de question. tu grilles tout seul avec
un fable").

1. share-cards-Q1: **One image per category.** `requirements/og/area-<areaId>.png`, with the eyebrow
   "Feature category", the category title and its colour; used by the category page and by every use
   case and behaviour page of that category. The index keeps `areas.png`.
2. share-cards-Q2: **Texts.** Category: title "<Category>: a feature category of Markdown OKF-Schema
   Studio", description starting "A feature category of Markdown OKF-Schema Studio". Use case: its own
   title with its full ID, description = the user need (its statement), plain text. Behaviour: its title
   with its full ID, description = its rule without Markdown, cut at a word with an ellipsis (max 200).
   Full IDs follow the viewer-ids CR.
3. share-cards-Q3: **The `/requirements` stub** (`requirements.html`) carries the index's tags.
4. share-cards-Q4: **X cache.** No cache-busting in the site; the release notes / announcement may
   reshare with `?v=<n>`. A post-deploy curl smoke check is optional, not in CI.
5. share-cards-Q5: **Requirements.** SwRS-MDOKFSTUDIO-CORE-085 is updated (no published requirement
   removed).
6. Spec critic: yes, on Fable (owner's rule): it changes what readers see when the site is shared.
