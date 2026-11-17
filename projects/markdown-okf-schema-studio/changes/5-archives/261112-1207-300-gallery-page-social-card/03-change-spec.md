---
title: Change spec - the gallery page shows a picture card when its link is shared
date: 2026-11-12
priority: P1
batch: with P1/strs-main-paths and P2/requirements-viewer (the viewer reuses this mechanism)
---

# Change spec: the gallery page shows a picture card when its link is shared

## Goal

A link to the published screenshot gallery
(`https://gsemet.github.io/markdown-okf-schema-studio/gallery.html`) shared on X or anywhere
that reads Open Graph shows a large picture card. Today it shows only a bare link. The picture
shows the site title, the number of captures and a mosaic of three real captures, and the site
build draws it again each time, so it stays current. There is one picture for the whole page, not
one per capture.

The other site pages written from Markdown, the home page, Contributing and How we ship, get a
simple card each in the same change.

The same mechanism draws the cards of the requirements viewer (`P2/requirements-viewer`, target
behaviour 7): one HTML template per picture, which Playwright shoots at 1200 x 630. This change
builds that mechanism and uses it for four cards: the gallery's and the three simple ones. The
viewer change adds its four level templates to it.

## Decisions carried from `02-answers.md`

| Decision (owner, 2026-11-12) | Where in this spec |
| --- | --- |
| Priority P1, same batch as `strs-main-paths` and `requirements-viewer` | Front matter |
| Picture: site title, number of captures, a mosaic of a few real captures, redrawn at each build ("Mosaic + count") | "The gallery card picture" |
| One picture for the whole gallery page, not one per capture | "The gallery card picture", "Out of scope" |
| The mechanism (HTML template shot by Playwright) is reused by the requirements viewer | Section 1 |
| The mosaic uses the three curated captures of `images/gallery.json` ("Curated 3") | "The gallery card picture" |
| The home, Contributing and How we ship pages get a simple social card each in this change ("Yes, one each") | Section 4 |
| Go for the specification and the batch | This file |

From `01-intent.md`: the tags (`og:title`, `og:description`, `og:url`, `og:image` with width,
height and alt text, `twitter:card` = `summary_large_image`), a 1200 x 630 PNG, an absolute https
image URL, the `<head>` written by `pageDocument` and the job `just ci-gallery`.

## Rules the Driver reads first

- `AGENTS.md` and `.agents/constitution.md`.
- `.agents/guidelines/ci.guidelines.md`, because this change edits `.github/workflows/ci.yml` and
  `.github/workflows/pages.yml`.
- `.agents/guidelines/git-commit-message.guidelines.md` and `git-commit-allowed-scopes.md`. None
  of the allowed scopes covers the project site, so the commit takes no scope (precedent:
  `feat: publish a requirements page on the project site`). Example:
  `feat: show a picture card when a site page link is shared`.
- `.agents/guidelines/pull-request.guidelines.md`. The PR shows the four card pictures as
  screenshots.

## What changes

### 1. The shared social card module: `test/site/socialCard.ts` (new)

This module is used by `buildSite.ts` now and by the requirements viewer generator later. It holds
everything a card needs, so that neither caller writes meta tags or launches Chromium itself.

- `SITE_URL`: the absolute https root of the published site, with a trailing slash
  (`https://gsemet.github.io/markdown-okf-schema-studio/`). It is derived from
  `package.json` `repository.url` (`https://github.com/<owner>/<repo>` becomes
  `https://<owner>.github.io/<repo>/`) and is defined in this one place. Every absolute URL of a
  card is built from it.
- `CARD_WIDTH = 1200`, `CARD_HEIGHT = 630`.
- `interface SocialCard { title: string; description: string; page: string; image: string; imageAlt: string }`.
  `page` and `image` are paths relative to the site (`gallery.html`, `og/gallery.png`).
- `socialMetaTags(card: SocialCard): string` returns the `<head>` lines, every value escaped
  like the page title (`escapeHtml`):
  - `<meta name="description" content="…">`
  - `og:type` = `website`, `og:site_name` = `Markdown OKF-Schema Studio`
  - `og:title`, `og:description`
  - `og:url` = `SITE_URL + page`
  - `og:image` = `SITE_URL + image`, plus `og:image:type` = `image/png`, `og:image:width` = `1200`,
    `og:image:height` = `630` and `og:image:alt`
  - `twitter:card` = `summary_large_image`, `twitter:title`, `twitter:description`,
    `twitter:image` (the same absolute URL) and `twitter:image:alt`
- `cardDocument(body: string): string` wraps a card's own body in the shared frame: a
  1200 x 630 page with no scrolling, the site palette (the `:root` colours of `pageDocument`:
  `--ink`, `--accent`, `--accent-strong`, `--paper`, `--line`, `--warm`), and a light theme only.
  The frame layout is the one of the viewer prototype (`prototype-02/style.css`, `body.card`): a
  coloured band at the top, the card's content, then a brand bar at the bottom with the logo
  (`images/logo.svg`) and "Markdown OKF-Schema Studio". The frame is plain and professional: no
  glow, no gradient, no effect (owner's direction for the viewer, which these cards share).
  `escapeHtml` moves to this module, or to a small shared helper, so that `buildSite.ts` and this
  module use one copy.
- `simpleCard(eyebrow: string, headline: string, line: string): string` returns the body of a
  simple card: the eyebrow, the headline in large type and one line of text under it. Section 4
  uses it.
- `async function writeCardPictures(siteRoot: string, cards: { name: string; html: string }[]): Promise<void>`
  does the following:
  - writes each template to `out/site-cards/<name>.html`. This is outside `out/site/`, so the
    templates are not published. The folder is emptied first. A template refers to local images
    by `file:` URL (`pathToFileURL`).
  - launches Chromium once (`chromium` from `playwright-core`, the dev dependency the page tests
    and `scripts/generate-logo.mjs` already use), opens a 1200 x 630 page with
    `deviceScaleFactor: 1`, and for each template navigates to it, waits for
    `document.fonts.ready` and for every `<img>` to finish loading, then shoots
    `<siteRoot>/og/<name>.png`. This follows `prototype-02/shoot.mjs`.
  - if Chromium cannot start, it throws "Cannot draw the social cards: Chromium does not start
    (run `just dev` to install it)". The site build then fails. It never publishes a page whose
    `og:image` is missing.

### 2. `pageDocument` takes an optional card (`test/site/buildSite.ts`)

- The signature becomes `pageDocument(title, currentPage, body, card?: SocialCard)`. With a card,
  the output of `socialMetaTags(card)` goes into `<head>` after `<title>`. Without a card, the
  page is byte for byte what it is today.
- The pages that pass a card are the gallery (section 3) and the three pages of section 4. The
  others pass none: the other Markdown pages of `docs/`, `requirements.html` (the requirements
  viewer replaces it) and `reports/index.html`.

### 3. The gallery card (`test/site/buildSite.ts`)

- The capture walk of `buildGallery` moves into an exported `listCaptures(screenshotRoot)`. The
  page and the card then count the same files: images (`png`, `jpg`, `jpeg`, `webp`) under
  `out/reports/e2e/screenshots/`, 542 on the published site today. `buildGallery` keeps its
  output unchanged.
- `galleryCard(captureCount, mosaic)` returns the card body for `cardDocument`, as described in
  "The gallery card picture" below.
- `main()` builds the gallery page with the card
  `{ title: "Screenshot gallery: Markdown OKF-Schema Studio", description: "<N> end-to-end screenshots of Markdown OKF-Schema Studio, a VS Code extension that previews and edits Markdown and MyST, each with the test that took it.", page: "gallery.html", image: "og/gallery.png", imageAlt: "Markdown OKF-Schema Studio screenshot gallery: <N> screenshots, with <k> of them shown" }`.
  `<N>` is the count from `listCaptures` and `<k>` the number of mosaic tiles.

### The gallery card picture

The picture is 1200 x 630 with the shared frame:

- On the left: the eyebrow "Screenshot gallery", then the count in large type ("542 screenshots")
  and one line under it: "End-to-end captures, each with the test that took it". The words
  follow the page's own text ("N E2E screenshots"). The count is the live one from
  `listCaptures`.
- On the right: a mosaic of the three curated captures listed in `images/gallery.json`
  (`01-paragraph-blur-commit.png`, `21-edit-hover.png`, `38-edit-mode-remembered.png`; owner's
  choice "Curated 3"). These are real captures, which `npm run site:gallery`
  (`test/site/curateGallery.ts`) copies again from the latest passing real-input run at each
  build, so the mosaic stays current. The mosaic takes the captures in the order of the file.
  Each tile has a thin border and a rounded corner, shows the top-left of its capture
  (`object-fit: cover; object-position: left top`), and the first capture is the largest.
- If `images/gallery.json` lists fewer captures, the mosaic shows the ones it has. If it lists
  none, the left column takes the full width and the card is still drawn.
- At the bottom: the brand bar of the shared frame.

### 4. A simple card for the home, Contributing and How we ship pages

These are the pages rendered from `README.md` (`index.html`), `CONTRIBUTING.md`
(`contributing.html`) and `docs/how-we-ship.md` (`docs/how-we-ship.html`). One table in
`buildSite.ts` (for example `SIMPLE_CARDS`, keyed by Markdown source path) holds, for each page,
the card meta text and the picture text. `renderMarkdown` looks the page up in the table and
passes the card to `pageDocument` when it finds one. The pictures use `simpleCard` in
`cardDocument`:

| Page | `image` | Picture: eyebrow / headline / line | `og:title` | `og:description` |
| --- | --- | --- | --- | --- |
| `index.html` | `og/home.png` | "VS Code extension" / "Markdown OKF-Schema Studio" / "Read the rendered page, click a block to edit its source" | "Markdown OKF-Schema Studio" | "A visual Markdown editor for VS Code: read a clean rendered page and click any block to edit its source. CommonMark, GitHub Flavored Markdown, MyST, OKF and OKF-Schema." |
| `contributing.html` | `og/contributing.png` | "Contributing" / "Build, test and change Studio" / "Setup, checks and the rules every change follows" | "Contributing: Markdown OKF-Schema Studio" | "How to set up, build, test and change Markdown OKF-Schema Studio." |
| `docs/how-we-ship.html` | `og/how-we-ship.png` | "How we ship" / "One owner, a team of AI agents" / "The workflow, followed through one real release" | "How we ship: Markdown OKF-Schema Studio" | "How one owner and a team of AI agents in Claude Code ship Markdown OKF-Schema Studio, followed through one real release." |

The descriptions are taken from the opening paragraph of each page. The Driver may shorten them,
but must keep them true to the page. `imageAlt` is "<eyebrow>: <headline>" (for example "How we
ship: One owner, a team of AI agents"). `page` is the output path of the row.

`main()` passes all four pictures (gallery, home, contributing, how-we-ship) to one
`writeCardPictures` call, so Chromium starts once. `site-manifest.json` gains
`"cards": ["og/gallery.png", "og/home.png", "og/contributing.png", "og/how-we-ship.png"]`.

### 5. Chromium wherever the site is built

The cards are drawn by `npm run site`, so every machine that runs it needs Chromium:

- Local and `just preflight`: `just dev` already installs it
  (`uv run --no-sync --group docs playwright install chromium`).
- `.github/workflows/ci.yml`, job `gallery`: `just dev-ci` becomes `just dev-ci visual`, the
  documented setup stage that adds Chromium (CI rule 4). Before it, the job restores the visual
  job's Ubuntu package archive cache with the same "Name the runner image" step and the same
  `actions/cache/restore` key. It only restores; saving stays with `visual`. Update the comment
  "Only this job installs Ubuntu packages" in the `visual` job so that it names both jobs.
- `.github/workflows/pages.yml`, job `build-site`: the path "Build Pages site from the downloaded
  reports" (`just site-assemble`) installs no browser today. Add an install step before it, under
  the same condition (`steps.usable.outputs.reports == 'true'`):
  `uv run --no-sync --group docs playwright install --with-deps chromium`. This mirrors the
  fallback path, which already installs it.

### 6. Glossary

Add to `.agents/glossary/common.md`: **Social card**: the picture and the Open Graph and Twitter
meta tags that a site page carries so that a shared link shows a large picture
(`test/site/socialCard.ts`; pictures in `og/` of the site, 1200 x 630).

### Requirements (okfreq)

There is no SwRS change. The requirements describe the extension (constitution, section 1), and
the published site is build tooling under `test/site/`: no file there carries an
`@implements_req` marker today, including the requirements page added by
`feat: publish a requirements page on the project site`. There is no `CHANGELOG.md` entry
either, because the extension does not change.

## Out of scope

- A card for each capture (owner: "pas chaque capture").
- Cards for `requirements.html` (the requirements viewer change replaces it and adds the cards of
  its own pages with this module), for `reports/index.html`, and for the other Markdown pages
  under `docs/`.
- The requirements viewer's four level templates (`P2/requirements-viewer`).
- A dark version of the pictures, and changes to the page bodies, their `<title>` or the gallery
  viewer.
- Posting on X or any other network. The owner checks the cards by sharing the links themselves.

## Evidence

### Checks (in `just check` through `npm run test:unit`)

New `test/site/socialCard.test.ts`. Each of these fails on the current code:

- `socialMetaTags` writes each tag listed in section 1 exactly once. `og:url`, `og:image` and
  `twitter:image` start with `https://` and with `SITE_URL`. The width is `1200` and the height
  `630`, and `twitter:card` is `summary_large_image`. A title holding `<"&>` comes out escaped.
- `SITE_URL` is `https://gsemet.github.io/markdown-okf-schema-studio/`, derived from
  `package.json`.
- `pageDocument` with a card has the tags inside `<head>`. Without a card, its output is
  unchanged: the test compares it with a page built without the argument and finds no `og:` in
  it.
- `galleryCard(542, [three images])` shows the count and three tiles. `galleryCard(0, [])` still
  gives a valid card with no mosaic.
- `simpleCard` puts the eyebrow, the headline and the line in the body, escaped.
- `SIMPLE_CARDS` covers exactly `README.md`, `CONTRIBUTING.md` and `docs/how-we-ship.md`, and each
  `page` equals `outputPathForMarkdown` of its key.
- `writeCardPictures` on a temporary site root writes `og/<name>.png`. The test reads the PNG IHDR
  bytes and checks a width of 1200 and a height of 630. When Chromium cannot start, the test
  skips with the same message as `test/page/svgBreakout.test.ts`.

`test/site/gallery.test.ts` keeps its assertions, and gains one: `listCaptures` and the count
shown by `buildGallery` agree on its fixture.

### Scenario steps (Driver, before the PR)

1. `just preflight` passes. Its `ci-gallery` stage builds the site with the four cards.
2. The four pages have the tags in `<head>`:
   `grep -cE 'og:|twitter:' out/site/gallery.html out/site/index.html out/site/contributing.html out/site/docs/how-we-ship.html`.
   Pages without a card, `out/site/requirements.html` for example, have none.
3. `uv run --no-sync --group docs python -c "from PIL import Image; [print(n, Image.open(f'out/site/og/{n}.png').size) for n in ('gallery','home','contributing','how-we-ship')]"`
   prints `(1200, 630)` four times.
4. Open the four pictures. In the gallery picture, the title, the live count and the mosaic of the
   three curated captures can be read. Each simple card shows its three lines. Nothing is cut
   off. Attach the four pictures to the PR body.
5. Pages dry run on the branch:
   `gh workflow run pages.yml --ref <branch> -f dry_run=true`. It passes, and its uploaded site
   artifact holds the four `og/*.png` files at 1200 x 630 and the four pages with the tags. This
   proves the downloaded-reports path now has Chromium.
6. Heavy gallery job on the branch:
   `gh workflow run ci.yml --ref <branch> -f heavy=true -f gallery=true`. The `gallery` job passes
   with `just dev-ci visual`.

### After the next release (the published check from `01-intent.md`)

Pages deploys only from a version tag, so this check runs after the release that ships the
change:

- `curl -s https://gsemet.github.io/markdown-okf-schema-studio/gallery.html | grep -E 'og:|twitter:'`
  shows the tags. The same is true of `index.html`, `contributing.html` and
  `docs/how-we-ship.html`.
- `curl -sI https://gsemet.github.io/markdown-okf-schema-studio/og/gallery.png` answers `200` with
  `content-type: image/png`, and the downloaded file measures 1200 x 630. The same is true of
  `og/home.png`, `og/contributing.png` and `og/how-we-ship.png`.

## Open questions

None. The owner answered both on 2026-11-12: "Curated 3" for the mosaic, and "Yes, one each" for
the cards of the other site pages.
