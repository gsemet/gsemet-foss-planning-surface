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

Spec critic (Fable), 2026-11-21 ~00:15: 9 points, 4 fixes, 5 questions decided by the Chief of Staff
under the owner's autonomy rule:
7. share-cards-Q7: **X cache.** No post on X by an agent (publishing is the owner's). The spec stays; every
   picture gets a URL X has never seen (the index picture is renamed too, e.g. `areas-card.png`), and the
   delivery note tells the owner to reshare with `?v=2` after deploy. If cards still fail, a new CR.
8. share-cards-Q8: **"Without Markdown".** Only the backticks of inline code and the link syntax
   `[x](url)` are removed; inline code content stays as written; text outside code is not changed. A build
   test over the real report checks that no description loses a word.
9. share-cards-Q9: **Titles.** A separate share title in the page spec; tab titles stay as they are
   (viewer-ids decides them). Share title: title first, full ID last, e.g.
   "<title> (StRS-MDOKFSTUDIO-MYST-005)"; categories "<Category>: a feature category of Markdown
   OKF-Schema Studio".
10. share-cards-Q10: **Area vs feature category.** Pages keep "Area"; the glossary gets both words ("Area:
    a feature category of the extension; 'feature category' is the wording of share cards").
11. share-cards-Q11: **Use case description** is the whole user need, not cut; only behaviours are cut
    at 200.
