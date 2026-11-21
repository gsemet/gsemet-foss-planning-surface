# Investigation, 2026-11-20 (live site, no change)

## Live pages are correct
All four pages (`/requirements/`, `/requirements/myst/`, `.../myst/StRS-MDOKFSTUDIO-MYST-005/`,
`.../rendering-core/SwRS-MDOKFSTUDIO-CORE-022/`) return 200, static HTML, full og/twitter tags at
the top of <head>: og:title, og:description, og:url (absolute), og:image (absolute https,
1200x630 PNG, 47-53 KB, 200 image/png), twitter:card=summary_large_image, twitter:image.
robots.txt is a 404 (Twitterbot allowed). Most likely cause of what the owner saw: X's card cache
(about 7 days per exact URL) holding a failed crawl. Test: share with `?v=2`.

Real defect: `/requirements` (no slash) serves the old `requirements.html` redirect stub (meta
refresh, no tags; X follows no meta refresh): `test/site/requirementsViewer/write.ts:36-50`.

## What X shows
summary_large_image: image, title over it, "From gsemet.github.io" (from the URL, cannot be
changed; og:site_name ignored, description mostly hidden). The "feature category" wording must go
in the title and on the image.

## Where cards come from
- `test/site/socialCard.ts:42-61` socialMetaTags; `:115` writeCardPictures (Chromium).
- `test/site/requirementsViewer/shell.ts:8-15, 40-49`: four shared images only (areas, area,
  use-case, behaviour): no image per category.
- `test/site/requirementsViewer/cards.ts:23-41`: generic headlines.
- `test/site/requirementsViewer/pages.ts:55` category description = blurb; `:106-108` use case
  description = statistics sentence; `:218` behaviour description = raw rule cut at 200 chars
  mid-word with backticks.
- Tests: `cards.test.ts` (SwRS-MDOKFSTUDIO-CORE-085), `socialCard.test.ts`.

## Proposed fix (changes CORE-085: SwRS update)
1. One image per category (`requirements/og/area-<areaId>.png`, eyebrow "Feature category",
   category title, colour), used by the category page and all its use-case and behaviour pages;
   `areas.png` for the index.
2. Text: category title "MyST syntax: a feature category of Markdown OKF-Schema Studio",
   description starting "A feature category of Markdown OKF-Schema Studio"; use case description
   = the user need; behaviour description without Markdown, cut at a word with an ellipsis.
3. The `/requirements` stub gets the index's tags.
4. After deploy, reshare with `?v=<n>`.

## Tests
Per page: one of each tag, og:image == twitter:image == SITE_URL + area image, og:url matches;
category/use case/behaviour description rules; every image exists, PNG, 1200x630, < 5 MB, one per
area; the stub carries og:image and twitter:card. Optional post-deploy curl smoke check.
