# The gallery page shows a picture when its link is shared

Asked by the owner on 2026-11-12: a link to the published screenshot gallery (`gallery.html`),
shared on X or elsewhere, shows only a bare link. It must show a large picture card.

Expected: `gallery.html` carries Open Graph and Twitter meta tags (`og:title`, `og:description`,
`og:url`, `og:image` with width, height and alt text, `twitter:card` = `summary_large_image`).
The image is one 1200 x 630 PNG for the whole page, not one per capture: for example the site
title, the number of captures and a mosaic of a few of them, drawn by the site build so it stays
current. The image URL is absolute (https).

Where: the page `<head>` is written by `pageDocument` in `test/site/buildSite.ts` (shared by every
site page), the gallery body by `buildGallery`; the job is `just ci-gallery`. The same card
template and Playwright shot are planned for the requirements viewer (P2
`requirements-viewer`, spec target behaviour 7, prototype `prototype-02/shoot.mjs`): reuse one
mechanism for both.

Check: the published `gallery.html` has the tags and its `og:image` URL returns a 1200 x 630 PNG.
