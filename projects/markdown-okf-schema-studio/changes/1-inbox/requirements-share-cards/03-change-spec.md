# Share cards for requirement pages: one image per category

Shared on X, every page of the requirements viewer shows a card with its own title and text and
a picture of its feature category; the `/requirements` link (no slash) shows the index's card.

## Goal

The owner shared requirement pages of the published site on X (2026-11-20). The index and the
MyST category showed a title and text but a generic icon; a use case page (MYST-005) and a
behaviour page (CORE-022) showed no card. The live tags are valid (see `work/investigation.md`):
X most likely cached failed crawls. Three real defects remain, and this CR fixes them:

- the pictures are per level (areas, area, use case, behaviour), not per category: all MyST pages
  should share one MyST picture;
- the texts are not written for sharing: a category page should say it is a feature category of
  the extension, a use case its user need, a behaviour its rule in plain text;
- `requirements.html`, served for `/requirements` without a slash, is a redirect stub with no
  tags, and X does not follow a meta refresh.

Done when every requirement page has its own title and text, one picture per category (and one
for the index), the stub has the index's card, all checked by build tests, and a reshare with a
`?v=` query shows the cards on X.

## Decisions carried from 02-answers.md

1. share-cards-Q1: one picture per category, `requirements/og/area-<areaId>.png`, with the
   eyebrow "Feature category", the category title and the category colour. The category page
   and every use case and behaviour page of that category use it. The index keeps
   `requirements/og/areas.png`.
2. share-cards-Q2: texts.
   - Category: title `<Category title>: a feature category of Markdown OKF-Schema Studio`;
     description starts with `A feature category of Markdown OKF-Schema Studio`.
   - Use case: its own title with its full ID; description = its user need, plain text.
   - Behaviour: its title with its full ID; description = its rule without Markdown, cut at a
     word with an ellipsis, at most 200 characters.
   - Full IDs, as the viewer-ids CR asks (`StRS-MDOKFSTUDIO-MYST-005`, not `MYST-005`).
3. share-cards-Q3: the `/requirements` stub (`requirements.html`) carries the index's tags.
4. share-cards-Q4: no cache-busting in the site. The release notes or the announcement may
   reshare with `?v=<n>`. A curl smoke check after deploy is optional and not in CI.
5. share-cards-Q5: SwRS-MDOKFSTUDIO-CORE-085 is updated in place; no published requirement is
   removed.
6. A spec critic reviews this spec (the Chief of Staff runs it; it is not part of the Driver's
   work).

## What changes

All the code is in the site build, under `test/site/` (the extension in `src/` does not change).
Read the project's `.agents/constitution.md` and `AGENTS.md` before you start.

### Shared text helpers: `test/site/socialCard.ts`

Add two exported functions:

- `plainText(text: string): string`: removes Markdown and HTML from a requirement text so it
  reads as plain text. It keeps the text of inline code (`` `x` `` becomes `x`), of a MyST role
  (`` {role}`x` `` becomes `x`), of emphasis and strong (`*x*`, `_x_`, `**x**`, `__x__` become
  `x`) and of a link (`[x](url)` becomes `x`). It drops HTML tags (`<b>a</b>` becomes `a`) and
  folds every run of whitespace into one space, trimmed. Underscores inside a word
  (`snake_case`) are kept.
- `shareDescription(text: string, max = 200): string`: `plainText(text)`. When the result is
  longer than `max`, it is cut at the last space that leaves room for `…` (U+2026) and ends with
  `…`, so the result is at most `max` characters, ellipsis included, and never ends in the
  middle of a word. A single word longer than `max` (no space to cut at) is cut at `max - 1`
  characters, then `…`.

`socialMetaTags`, `cardDocument`, `simpleCard` and `writeCardPictures` keep their behaviour.

### Category pictures: `test/site/requirementsViewer/cards.ts`

- Replace the four level cards with the index card plus one card per category:
  - `areas` (file `requirements/og/areas.png`): the current index card, unchanged
    (`levelCardBody("areas")`: eyebrow "Requirements", headline "Studio requirements", the
    three layers).
  - `area-<areaId>` (file `requirements/og/area-<areaId>.png`), one per entry of
    `model.areas`, built by a new `categoryCardBody(area: Area): string`: the eyebrow
    "Feature category", the headline = the category title (`area.title`, for example "MyST
    syntax"), the line "Use cases and behaviours, linked to code and tests", and the three
    layers (Use case / Behaviour / Code and tests) with all three outlined in the category
    colour (like the index card's `.chain.areas`). The category colour (`area.colour`)
    replaces `var(--link)` in this card for the top band, the eyebrow and the layer outlines;
    the card sets it in its own `<style>` (the frame of `cardDocument` stays shared).
- Replace `levelCards()` with `viewerCards(model: ViewerModel | undefined): { name: string;
  html: string }[]`: the `areas` card first, then one `area-<areaId>` card per area in
  `model.areas` order. Without a model (no report) it returns the `areas` card only. Move the
  `// @implements_req SwRS-MDOKFSTUDIO-CORE-085` marker to `viewerCards`.
- The cards `area`, `use-case` and `behaviour` (files `og/area.png`, `og/use-case.png`,
  `og/behaviour.png`) are no longer drawn: no page points to them.
- Each headline fits: the longest category title of `test/shared/e2eGroups.ts` ("Edition
  palette and slash menu") stays inside the content area of the card, above the brand bar. Lower
  the headline size of the category card if it does not (the test below checks it).

### Which picture a page uses: `test/site/requirementsViewer/shell.ts`

- `PageSpec` gets `readonly area?: Area` (the page's category; absent on the index).
  `areaPage`, `useCasePage` and `behaviourPage` set it.
- Replace `levelCard` with `shareCard(spec)`: title and description from the spec, `page:
  <spec.dir>/`, `image: requirements/og/area-<spec.area.id>.png` with `imageAlt: Feature
  category: <area title>` when the spec has an area; `image: requirements/og/areas.png` with the
  index's current alt text (`Requirements: Every feature, from use case to test`) otherwise.
  `viewerDocument` passes `shareCard(spec)` to `headTags`. Mark `shareCard` with
  `// @implements_req SwRS-MDOKFSTUDIO-CORE-085`.
- `Level` and `LEVELS` stay only as far as the index card (`levelCardBody("areas")`) and the
  page code still use them; remove what becomes unused (`just check` runs the unused-exports
  check).

### Texts of the pages: `test/site/requirementsViewer/pages.ts`

The title stays one field of `PageSpec`: it is both the tab title (`<title> | Studio
requirements`) and the social title, as today.

- `areaPage`: title `${area.title}: a feature category of Markdown OKF-Schema Studio`;
  description `shareDescription("A feature category of Markdown OKF-Schema Studio: " +
  area.description)` when the area has a description, and `A feature category of Markdown
  OKF-Schema Studio.` when it has none. (`area.description` is the group's `scope` of
  `test/shared/e2eGroups.ts`, which holds backticks, hence `shareDescription`.) The visible
  page (eyebrow "Area", heading, lead) does not change.
- `useCasePage`: title `Use case ${useCase.id}: ${useCase.title}` (full ID instead of
  `shortId`); description `shareDescription(useCase.userNeed)`, or
  `shareDescription(useCase.description)` when the user need is empty, or the current
  statistics sentence when both are empty. The visible page does not change.
- `behaviourPage`: title `Behaviour ${behaviour.id}: ${behaviour.title}` (full ID); description
  `shareDescription(behaviour.description)` (replaces the raw `.slice(0, 200)`). The visible
  page does not change.
- The index (`test/site/requirementsViewer/home.ts`) keeps its title "Requirements of Markdown
  OKF-Schema Studio" and its description `HOME_DESCRIPTION`.

### The `/requirements` stub: `test/site/requirementsViewer/write.ts`

- `redirectDocument(card: SocialCard)` writes, in its `<head>`, the charset, the title, the
  meta refresh and the canonical link as today, plus `socialMetaTags(card)` where `card` is the
  index's card (`shareCard` of the home page spec). So the stub's tags are the index page's tags,
  `og:url` included (`<SITE_URL>requirements/`, the same as the canonical link). `<title>`
  becomes the index's title text ("Requirements of Markdown OKF-Schema Studio").
- `writeViewerPages` builds the index card from the first page of `viewerPages` and passes it
  to `redirectDocument`; a missing report still writes the stub with that card.
- `writeRequirementsViewer` draws `viewerCards(model)` with the model `writeViewerPages`
  returns (instead of `levelCards()`); update its doc comment ("the index picture and one
  picture per category").

### Tests: `test/site/requirementsViewer/cards.test.ts` and `write.test.ts`

- `test/site/requirementsViewer/fixture.ts`: add a `description?: string` option to
  `FixtureOptions`, used for the frontmatter `description` when given, so a test can give a
  behaviour a long rule with Markdown.
- Replace "social tags of each level" with tests that each carry `// @tests_req
  SwRS-MDOKFSTUDIO-CORE-085`, over `viewerPages(model, "/nonexistent-root")` of the fixture
  model, rendered by `viewerDocument`:
  - every page: exactly one `og:title`, `og:description`, `og:url`, `og:image`,
    `twitter:card`, `twitter:image`; `og:url` = `SITE_URL + <dir>/`; `og:image` equals
    `twitter:image`; width 1200, height 630; `twitter:card` = `summary_large_image`; every
    title is distinct.
  - picture per page: the index points to `<SITE_URL>requirements/og/areas.png`; the `gfm`
    category page, the use case `StRS-X-001` (scope `gfm`) and the behaviour `SwRS-X-010`
    (scope `gfm`) all point to `<SITE_URL>requirements/og/area-gfm.png`; the behaviour
    `SwRS-X-013` (scope `myst`) to `area-myst.png`. No page points to `og/area.png`,
    `og/use-case.png` or `og/behaviour.png`.
  - category text: the title of the `gfm` page ends with `: a feature category of Markdown
    OKF-Schema Studio`; its description starts with `A feature category of Markdown OKF-Schema
    Studio`.
  - use case text: the title of `StRS-X-001` contains `StRS-X-001` (the full ID); its
    description is `As a writer, I do a thing.` (the fixture's user need with its `<b>` tags
    dropped).
  - behaviour text: the title of `SwRS-X-010` contains `SwRS-X-010`; a behaviour built with a
    rule of more than 200 characters holding inline code, emphasis and a link has a description
    of at most 200 characters, ending with `…`, with no backtick, `*` or `](`, and whose text
    before `…` ends at a word of the rule (the rule's plain text starts with it and the next
    character of the rule is a space).
- Unit tests of `plainText` and `shareDescription` (in `test/site/socialCard.test.ts`, with
  the `@tests_req SwRS-MDOKFSTUDIO-CORE-085` marker in each test that checks the cut): each
  Markdown form above; `snake_case` kept; text at or under 200 left whole; a long text cut at a
  word; a single long word.
- Replace "the four pictures are drawn at 1200 x 630" with "the index and category pictures are
  drawn": `writeCardPictures` of `viewerCards(fixture model)` writes exactly `areas.png`,
  `area-gfm.png` and `area-myst.png` in `og/`, each a PNG of 1200 x 630 under 5 MB. Skipped,
  as today, when Chromium does not start.
- A Chromium test (same skip) that the headline fits: for each of the 16 groups of `GROUPS`
  (`test/shared/e2eGroups.ts`), the category card of an `Area` with that title rendered at
  1200 x 630 has its `.headline` box inside the viewport and above the `.brand` bar.
- `test/site/requirementsViewer/write.test.ts`, "requirements.html redirects to
  requirements/": the stub still holds the meta refresh to `requirements/` and the canonical
  link, and now its social tags equal those of the index page written by `viewerDocument`
  (same `og:image` `<SITE_URL>requirements/og/areas.png`, `og:url`
  `<SITE_URL>requirements/`, `twitter:card` `summary_large_image`). The test "a missing report
  writes the home and the redirect only" also checks that the stub written from
  `writeViewerPages` carries `og:image` and `twitter:card`.

### Requirement: `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-085.md`

Update in place (same ID, uuid and lifecycle; nothing removed from the bundle):

- title: `The site requirements viewer has a social card for each page`;
- statement: When a maintainer builds the Pages site, the build SHALL write one social picture
  for the index of the viewer and one for each feature category, give each page of the viewer
  the Open Graph and Twitter tags that point to the picture of its category (the index's own
  picture on the index), with its own title and a plain-text description, and give the
  `requirements.html` page the tags of the index;
- scenarios: (nominal) tags of each page; (nominal) one picture per category shared by its use
  cases and behaviours; (nominal) texts of a category, a use case and a behaviour (full IDs,
  the "feature category" wording, the user need, the rule without Markdown); (boundary) a rule
  longer than 200 characters is cut at a word with an ellipsis; (nominal) the
  `requirements.html` page carries the index's tags; (refusal) no browser, kept as today with
  "the unit tests of the pictures are skipped";
- verification notes: name the new tests in `cards.test.ts`, `socialCard.test.ts` and
  `write.test.ts`;
- `implemented_in_files`: `test/site/requirementsViewer/cards.ts`,
  `test/site/requirementsViewer/shell.ts`, `test/site/requirementsViewer/pages.ts`,
  `test/site/requirementsViewer/write.ts`, `test/site/socialCard.ts` (each with an
  `@implements_req` at the code point: `viewerCards`, `shareCard`, the page texts,
  `redirectDocument`, `shareDescription`); `tested_in_files`: `cards.test.ts`,
  `socialCard.test.ts`, `write.test.ts`.

Then `just requirements-update` and a dated entry in `requirements/tiers/log.md` (CORE-085:
social cards per category, share texts, stub tags).

### Glossary: `.agents/glossary/common.md`

Extend the "Social card" entry: the requirements viewer has one picture for its index and one
per feature category (`requirements/og/area-<areaId>.png`), shared by the category's pages.

## Out of scope

- The visible pages: the eyebrow "Area", the headings, the breadcrumb and the search keep their
  text (full IDs on the page and in the breadcrumb, and search by full ID, are the viewer-ids
  CR).
- Cache-busting in the site, and any change to the gallery, report or Markdown pages' cards.
- A curl smoke check in CI; X's own cache.
- The site manifest's `cards` list in `test/site/buildSite.ts`.
- The extension (`src/`), the writing skill (no rendered syntax changes) and the release
  notes (no extension behaviour changes).

## Evidence

- `just check` (it runs the unit tests above: tags, texts, pictures, headline fit, stub) and
  `just requirements-lint`, then `just preflight` (constitution, section 4). The picture tests
  need Chromium (`just dev` installs it); on a machine without it they are skipped, so the
  Driver's run must show them passing, not skipped.
- The checks read what the site build writes: the HTML from `viewerDocument` and
  `redirectDocument` of the shipped code over the fixture model, and the PNG files from
  `writeCardPictures`; no test prepares a copy of a page.
- A local site build (`just preflight` builds it, or the site build target it uses) writes
  `requirements/og/areas.png` and 16 `requirements/og/area-<areaId>.png` files, and no
  `area.png`, `use-case.png` or `behaviour.png`. The PR shows `area-myst.png`, the longest
  title's picture (`area-palette-slash.png`) and `areas.png` as screenshots, per the
  pull-request guideline.
- In the built `requirements/myst/StRS-MDOKFSTUDIO-MYST-005/index.html` and
  `requirements/rendering-core/SwRS-MDOKFSTUDIO-CORE-022/index.html`, `og:image` is
  `<SITE_URL>requirements/og/area-myst.png` and `.../area-rendering-core.png`, and the
  descriptions are the user need and the plain rule; the PR body quotes these tags.
- After merge and deploy (not the Driver's gate): reshare `/requirements/?v=2`,
  `/requirements/myst/?v=2`, the MYST-005 and CORE-022 pages with `?v=2`, and `/requirements?v=2`
  on X; optionally curl each page and its `og:image` (200, `image/png`). The Driver lists these
  URLs in `delivery.md` for the owner.

No CI job changes; no host or default matrix (the site build does not depend on a host or a
setting).

## Sibling CRs

`3-ready/requirements-viewer-shows-table-scenario`, `1-inbox/requirements-path-graph-design` and
`1-inbox/requirements-viewer-ids` also edit `test/site/requirementsViewer/pages.ts`,
`shell.ts`, `viewer.css` and `requirements/tiers/log.md`: whichever lands second rebases.
viewer-ids changes the visible IDs and may move `shortId` uses; this CR changes only the
`title` and `description` fields of the page specs and the head tags, so the overlap is the
`title:` lines of `useCasePage` and `behaviourPage` (both put the full ID there).

## Decided in the spec

The answers leave these points open; each is decided here, the option most consistent with the
product and the answers:

1. The full-ID title format: `Use case <full ID>: <title>` and `Behaviour <full ID>: <title>`
   (the current format with the full ID in place of the short one), so the kind of page stays
   readable in the card.
2. One title field for the tab and the card, as today: the category page's tab title becomes
   `<Category>: a feature category of Markdown OKF-Schema Studio | Studio requirements`.
3. The category description is `A feature category of Markdown OKF-Schema Studio: <category
   scope>`, cut by the same 200-character rule, since the scope text is technical and holds
   backticks.
4. The use case description uses the same plain-text and 200-character rule as the behaviour
   (the answers say "plain text"; X shows little of it anyway), and falls back to the use case's
   description, then to the current sentence, when the user need is empty.
5. `plainText` also drops HTML tags (the fixture's user need holds `<b>`).
6. The category picture's content beyond the answers (eyebrow, title, colour): the line "Use
   cases and behaviours, linked to code and tests" and the three layers outlined in the
   category colour; no counts, so the picture does not change with every new requirement.
7. The level pictures `area.png`, `use-case.png` and `behaviour.png` are no longer written.
8. The stub's `og:url` is `<SITE_URL>requirements/`, the canonical page, so X groups both URLs
   under one card; its `<title>` becomes the index's title.
9. The page eyebrow "Area" is not renamed "Feature category": the owner asked about the shared
   cards only.
