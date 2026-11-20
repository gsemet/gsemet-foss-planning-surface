# Share cards for requirement pages: one image per category

Shared on X, every page of the requirements viewer shows a card with its own share title and
text and a picture of its feature category; the `/requirements` link (no slash) shows the
index's card.

## Goal

The owner shared requirement pages of the published site on X (2026-11-20). The index and the
MyST category showed a title and text but a generic icon; a use case page (MYST-005) and a
behaviour page (CORE-022) showed no card. The live tags are valid (see `work/investigation.md`):
X most likely cached failed crawls. Three real defects remain, and this CR fixes them:

- the pictures are per level (areas, area, use case, behaviour), not per category: all MyST pages
  should share one MyST picture;
- the texts are not written for sharing: a category page should say it is a feature category of
  the extension, a use case its user need, a behaviour its rule without Markdown syntax;
- `requirements.html`, served for `/requirements` without a slash, is a redirect stub with no
  tags, and X does not follow a meta refresh.

Every picture also gets a URL X has never crawled, so no failed crawl cached by X can stand in
for it.

Done when every requirement page has its own share title and text, one picture per category
(and one for the index, under a new name), the stub has the index's card, all checked by build
tests; after deploy, the owner reshares with `?v=2` and the cards show on X.

## Decisions carried from 02-answers.md

1. share-cards-Q1: one picture per category, `requirements/og/area-<areaId>.png`, with the
   eyebrow "Feature category", the category title and the category colour. The category page
   and every use case and behaviour page of that category use it. The index has its own picture
   (renamed, see Q7).
2. share-cards-Q2: texts. Category: share title `<Category>: a feature category of Markdown
   OKF-Schema Studio`, description starting with `A feature category of Markdown OKF-Schema
   Studio`. Use case: its own title with its full ID, description = its user need. Behaviour:
   its title with its full ID, description = its rule without Markdown, cut at a word with an
   ellipsis, at most 200 characters. Full IDs: `StRS-MDOKFSTUDIO-MYST-005`, not `MYST-005`.
3. share-cards-Q3: the `/requirements` stub (`requirements.html`) carries the index's tags.
4. share-cards-Q4: no cache-busting in the site; a reshare with `?v=<n>`; a curl smoke check after
   deploy is optional and not in CI.
5. share-cards-Q5: SwRS-MDOKFSTUDIO-CORE-085 is updated in place; no published requirement is
   removed.
6. A spec critic reviewed this spec (done, 2026-11-21; its results are Q7 to Q11 and the fixes
   below).
7. share-cards-Q7: no agent posts on X (publishing is the owner's). Every picture gets a URL X has
   never seen: the category pictures are new, and the index picture is renamed
   `requirements/og/areas-card.png`. The Driver's `delivery.md` tells the owner to reshare with
   `?v=2` after deploy. If the cards still fail after that, it is a new CR.
8. share-cards-Q8: "without Markdown" means only two things are removed: the backticks of inline
   code (the code text stays as written) and the link syntax `[x](url)` (the text `x` stays).
   Nothing else in the text changes. A build test over the real requirements checks that no
   description loses a word.
9. share-cards-Q9: a separate share title in the page spec; the tab titles stay as they are
   (viewer-ids decides them). Share title: title first, full ID last, `<title> (<full ID>)`, for
   example `<title> (StRS-MDOKFSTUDIO-MYST-005)`; a category `<Category>: a feature category of
   Markdown OKF-Schema Studio`.
10. share-cards-Q10: the pages keep "Area". The glossary gets both words: "Area: a feature
    category of the extension; 'feature category' is the wording of share cards".
11. share-cards-Q11: the use case description is the whole user need, not cut; only behaviours
    are cut at 200.

## What changes

All the code is in the site build, under `test/site/` (the extension in `src/` does not change).
Read the project's `.agents/constitution.md` and `AGENTS.md` before you start.

### Share text helpers: `test/site/socialCard.ts`

Add two exported functions:

- `plainText(text: string): string`: removes the backticks of inline code (`` `x` `` becomes
  `x`, the code text kept as written) and the link syntax (`[x](url)` becomes `x`), and folds
  every run of whitespace into one space, trimmed. Nothing else changes: emphasis marks,
  underscores, HTML-looking text and MyST role names stay as they are. Mark it
  `// @implements_req SwRS-MDOKFSTUDIO-CORE-085`.
- `shareDescription(text: string, max = 200): string`: `plainText(text)`. When the result is
  longer than `max`, it is cut at the last space that leaves room for `…` (U+2026) and ends with
  `…`, so the result is at most `max` characters, ellipsis included, and never ends in the
  middle of a word. A single word longer than `max` (no space to cut at) is cut at `max - 1`
  characters, then `…`.

`socialMetaTags` (it escapes the values), `cardDocument`, `simpleCard` and `writeCardPictures`
keep their behaviour.

### Pictures: `test/site/requirementsViewer/cards.ts`

- Replace the four level cards with the index card plus one card per category:
  - `areas-card` (file `requirements/og/areas-card.png`): the current index card, unchanged in
    content (`levelCardBody("areas")`: eyebrow "Requirements", headline "Studio requirements",
    the three layers), under its new name.
  - `area-<areaId>` (file `requirements/og/area-<areaId>.png`), one per entry of
    `model.areas`, built by a new `categoryCardBody(area: Area): string`: the eyebrow
    "Feature category", the headline = the category title (`area.title`, for example "MyST
    syntax"), the line "Use cases and behaviours, linked to code and tests", and the three
    layers (Use case / Behaviour / Code and tests) all outlined in the category colour (like the
    index card's `.chain.areas`). The category colour (`area.colour`) replaces `var(--link)` in
    this card for the top band, the eyebrow and the layer outlines; the card sets it in its own
    `<style>` (the frame of `cardDocument` stays shared and cream).
- Replace `levelCards()` with `viewerCards(model: ViewerModel | undefined): { name: string;
  html: string }[]`: the `areas-card` card first, then one `area-<areaId>` card per area in
  `model.areas` order. Without a model (no report) it returns the `areas-card` card only. Move
  the `// @implements_req SwRS-MDOKFSTUDIO-CORE-085` marker to `viewerCards`.
- No `areas.png`, `area.png`, `use-case.png` or `behaviour.png` is drawn any more.
- Each headline fits: the longest category title of `test/shared/e2eGroups.ts` ("Edition
  palette and slash menu") stays inside the content area of the card, above the brand bar. Lower
  the headline size of the category card if it does not (a test below checks it).

### Which picture and which share title a page uses: `test/site/requirementsViewer/shell.ts`

- `PageSpec` gets:
  - `readonly shareTitle: string`: the og:title and twitter:title. `title` stays the tab title
    only (its doc comment says so), unchanged by this CR.
  - `readonly area?: Area`: the page's category; absent on the index. `areaPage`,
    `useCasePage` and `behaviourPage` set it.
- Replace `levelCard` with `shareCard(spec)`: `title: spec.shareTitle`, `description:
  spec.description`, `page: <spec.dir>/`; `image: requirements/og/area-<spec.area.id>.png` with
  `imageAlt: Feature category: <area title>` when the spec has an area, `image:
  requirements/og/areas-card.png` with the index's current alt text (`Requirements: Every
  feature, from use case to test`) otherwise. `viewerDocument` passes `shareCard(spec)` to
  `headTags`; the `<title>` stays `${spec.title} | Studio requirements`. Mark `shareCard` with
  `// @implements_req SwRS-MDOKFSTUDIO-CORE-085`.
- `Level` and `LEVELS` stay only as far as the index card (`levelCardBody("areas")`) and the
  page code still use them; remove what becomes unused (`just check` runs the unused-exports
  check). `test/site/siteTheme.test.ts` imports `levelCardBody`; see Tests.

### Texts of the pages: `test/site/requirementsViewer/pages.ts` and `home.ts`

- `areaPage`: `shareTitle` `${area.title}: a feature category of Markdown OKF-Schema Studio`;
  description `A feature category of Markdown OKF-Schema Studio: ${plainText(area.description)}`
  when the area has a description, `A feature category of Markdown OKF-Schema Studio.` when it
  has none. (`area.description` is the group's `scope` of `test/shared/e2eGroups.ts`.) The tab
  title (`${area.title}: use cases and behaviours`) and the visible page (eyebrow "Area",
  heading, lead) do not change.
- `useCasePage`: `shareTitle` `${useCase.title} (${useCase.id})`; description
  `plainText(useCase.userNeed)`, whole, not cut; `plainText(useCase.description)` only when the
  user need is empty (no active StRS has one today). The statistics sentence is no longer the
  description: remove the `description` field of `MapSummary` and its line in `mapSummary`
  (`test/site/requirementsViewer/layout.ts`), which nothing else uses, and the "N behaviours make
  up this use case" fallback. Tab title and visible page unchanged.
- `behaviourPage`: `shareTitle` `${behaviour.title} (${behaviour.id})`; description
  `shareDescription(behaviour.description)` (replaces the raw `.slice(0, 200)`). Tab title and
  visible page unchanged.
- `homePage` (`home.ts`): `shareTitle` = its title, "Requirements of Markdown OKF-Schema
  Studio"; description `HOME_DESCRIPTION`, unchanged.

### The `/requirements` stub: `test/site/requirementsViewer/write.ts`

- `redirectDocument(card: SocialCard)` writes, in its `<head>`, the charset, the title, the
  meta refresh and the canonical link as today, plus `socialMetaTags(card)` where `card` is the
  index's card (`shareCard` of the home page spec). So the stub's tags are the index page's tags,
  `og:url` included (`<SITE_URL>requirements/`, the same as the canonical link). Its `<title>`
  stays "Requirements | Markdown OKF-Schema Studio" (a tab title). Mark it `// @implements_req
  SwRS-MDOKFSTUDIO-CORE-085`.
- `writeViewerPages` builds the index card from the first page of `viewerPages` and passes it
  to `redirectDocument`; a missing report still writes the stub with that card.
- `writeRequirementsViewer` draws `viewerCards(model)` with the model `writeViewerPages`
  returns (instead of `levelCards()`); update its doc comment ("the index picture and one
  picture per category").

### Tests

- `test/site/requirementsViewer/fixture.ts`: add a `description?: string` option to
  `FixtureOptions`, used for the frontmatter `description` when given, so a test can give a
  behaviour a long rule with inline code and a link.
- `test/site/requirementsViewer/cards.test.ts`: replace "social tags of each level" with tests
  that each carry `// @tests_req SwRS-MDOKFSTUDIO-CORE-085`, over `viewerPages(model,
  "/nonexistent-root")` of the fixture model, rendered by `viewerDocument`:
  - every page: exactly one `og:title`, `og:description`, `og:url`, `og:image`,
    `twitter:card`, `twitter:image`; `og:title` = `twitter:title` = the spec's `shareTitle`;
    `<title>` = `${spec.title} | Studio requirements`; `og:url` = `SITE_URL + <dir>/`;
    `og:image` = `twitter:image`; width 1200, height 630; `twitter:card` =
    `summary_large_image`; every share title is distinct.
  - picture per page: the index points to `<SITE_URL>requirements/og/areas-card.png`; the `gfm`
    category page, the use case `StRS-X-001` (scope `gfm`) and the behaviour `SwRS-X-010`
    (scope `gfm`) all to `<SITE_URL>requirements/og/area-gfm.png`; the behaviour `SwRS-X-013`
    (scope `myst`) to `area-myst.png`. No page points to `og/areas.png`, `og/area.png`,
    `og/use-case.png` or `og/behaviour.png`.
  - category text: the share title of the `gfm` page ends with `: a feature category of
    Markdown OKF-Schema Studio`; its description starts with `A feature category of Markdown
    OKF-Schema Studio`; its tab title is still `GitHub Flavored Markdown: use cases and
    behaviours`.
  - use case text: the share title of `StRS-X-001` is `Title of StRS-X-001 (StRS-X-001)`; its
    description is the fixture's whole user need, `As a writer, I do <b>a</b> thing.` (escaped
    in the tag as `&lt;b&gt;`); a use case built with a user need longer than 200 characters
    keeps it whole.
  - behaviour text: the share title of `SwRS-X-010` is `Title of SwRS-X-010 (SwRS-X-010)`; a
    behaviour built with a rule of more than 200 characters holding inline code and a link has a
    description of at most 200 characters, ending with `…`, with no backtick and no `](`, whose
    text before `…` is the start of the rule's plain text and ends at a word (the next character
    of the plain text is a space).
- `test/site/requirementsViewer/shareText.test.ts` (new) or `test/site/socialCard.test.ts`, each
  test with `// @tests_req SwRS-MDOKFSTUDIO-CORE-085`:
  - unit tests of `plainText` and `shareDescription`: backticks removed and code text kept;
    `[x](url)` becomes `x`; `*x*`, `snake_case`, `<b>` and `` {role} `` names unchanged; text at
    or under 200 left whole; a long text cut at a word; a single long word.
  - the real requirements: read every `requirements/tiers/strs/**/*.md` and
    `requirements/tiers/swrs/**/*.md` of the repository as it ships, parse the frontmatter with
    the `yaml` package (already a dependency), and for each `description` and `user_need`: the
    words (runs of letters and digits) of the text with only the link targets `(url)` of
    `[x](url)` left out appear, in the same order and none missing, in `plainText(text)`; and for
    each SwRS, `shareDescription(description)` before its `…` is a word-boundary start of
    `plainText(description)`. This test reads the Markdown bundle, not the okfreq report (the
    report is built after `just check` in `ci-static`, so a test on it would be skipped there).
- Replace "the four pictures are drawn at 1200 x 630" with "the index and category pictures are
  drawn" (same Chromium skip as today): `writeCardPictures` of `viewerCards(fixture model)`
  writes exactly `areas-card.png`, `area-gfm.png` and `area-myst.png` in `og/`, each a PNG of
  1200 x 630 under 5 MB.
- A Chromium test (same skip) that the headline fits: for each of the 16 groups of `GROUPS`
  (`test/shared/e2eGroups.ts`), the category card of an `Area` with that title rendered at
  1200 x 630 has its `.headline` box inside the viewport and above the `.brand` bar.
- `test/site/requirementsViewer/pages.test.ts:70`: the line `assert.ok(page.description
  .startsWith("4 ways"))` asserts the statistics sentence; change it to assert the description
  is the fixture's user need, `As a writer, I do <b>a</b> thing.` (the body checks of the map
  summary stay).
- `test/site/siteTheme.test.ts`, "the social card documents are cream": replace
  `cardDocument(levelCardBody("use-case"))` (that level card goes) with the index card
  `cardDocument(levelCardBody("areas"))` and one category card
  `cardDocument(categoryCardBody(<an Area>))`; the same assertions (`#f5f1e8`, none of the former
  teal values) hold. Keep its `@tests_req SwRS-MDOKFSTUDIO-CORE-086`.
- `test/site/requirementsViewer/write.test.ts`, "requirements.html redirects to
  requirements/": the stub still holds the meta refresh to `requirements/` and the canonical
  link, and its social tags equal those of the index page written by `viewerDocument` (same
  `og:image` `<SITE_URL>requirements/og/areas-card.png`, `og:url` `<SITE_URL>requirements/`,
  `twitter:card` `summary_large_image`). "a missing report writes the home and the redirect only"
  also checks that the stub written by `writeViewerPages` carries `og:image` and `twitter:card`.
  Both with `@tests_req SwRS-MDOKFSTUDIO-CORE-085`.

### Requirements

`requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-085.md`, updated in place (same
ID, uuid and lifecycle; nothing removed from the bundle):

- title: `The site requirements viewer has a social card for each page`;
- statement: When a maintainer builds the Pages site, the build SHALL write one social picture
  for the index of the viewer and one for each feature category, give each page of the viewer
  the Open Graph and Twitter tags that point to the picture of its category (the index's own
  picture on the index), with its own share title and a description without inline-code
  backticks or link syntax, and give the `requirements.html` page the tags of the index;
- scenarios: (nominal) tags of each page; (nominal) one picture per category shared by its use
  cases and behaviours; (nominal) texts of a category, a use case and a behaviour (the "feature
  category" wording, the title with the full ID last, the whole user need, the rule without
  backticks or link syntax); (boundary) a rule longer than 200 characters is cut at a word with
  an ellipsis; (boundary) no description of the shipped requirements loses a word; (nominal) the
  `requirements.html` page carries the index's tags; (refusal) no browser, kept as today with
  "the unit tests of the pictures are skipped";
- verification notes: name the tests above;
- `implemented_in_files`: `test/site/requirementsViewer/cards.ts`, `shell.ts`, `pages.ts`,
  `write.ts` and `test/site/socialCard.ts` (each with an `@implements_req` at its code point:
  `viewerCards`, `shareCard`, the page texts, `redirectDocument`, `plainText`);
  `tested_in_files`: the test files above.

`requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-086.md`, scenario "A social card":
"GIVEN a social picture of a main page or of a level of the viewer" becomes "GIVEN a social
picture of a main page, or of the index or of a category of the viewer".

Then `just requirements-update` and a dated entry in `requirements/tiers/log.md` (CORE-085:
pictures per category, share titles and texts, stub tags; CORE-086: scenario wording).

### Glossary: `.agents/glossary/common.md`

- Add "Area: a feature category of the extension (one of the 16 groups of
  `test/shared/e2eGroups.ts`, an okfreq scope); 'feature category' is the wording of share
  cards."
- Extend "Social card": the requirements viewer has one picture for its index
  (`requirements/og/areas-card.png`) and one per area (`requirements/og/area-<areaId>.png`),
  shared by the area's pages; their share title is separate from the tab title.

## Out of scope

- The visible pages and their tab titles: the eyebrow "Area", headings, breadcrumb and search
  keep their text (full IDs on the page and search by full ID are the viewer-ids CR).
- Removing more Markdown than inline-code backticks and link syntax.
- Cache-busting in the site, and any change to the gallery, report or Markdown pages' cards.
- Posting on X (the owner's), a curl smoke check in CI, X's own cache.
- The site manifest's `cards` list in `test/site/buildSite.ts`.
- The extension (`src/`), the writing skill (no rendered syntax changes) and the release notes
  (no extension behaviour changes).

## Evidence

- `just check` (it runs the unit tests above: tags, share titles, texts, the real-requirements
  word check, pictures, headline fit, cream cards, stub) and `just requirements-lint`, then
  `just preflight` (constitution, section 4; on Windows it stops after the static stage). The
  picture tests need Chromium (`just dev` installs it); without it they are skipped, so the
  Driver's run must show them passing, not skipped.
- The checks read what the shipped code writes: HTML from `viewerDocument` and
  `redirectDocument` over the fixture model, PNG files from `writeCardPictures`, and the
  real-requirements check reads the shipped `requirements/tiers/` Markdown files at the head
  under test; no test prepares a copy of a page.
- Built files: from `just site-assemble` (it builds the requirements report, compiles and builds
  the gallery and the site in `out/site/`; it works locally, including on Windows where
  `preflight` does not reach the site), or else from the CI gallery job's site artifact
  (`studio-site-attempt-<n>`, `out/site/`, on a heavy run). The built site holds
  `requirements/og/areas-card.png` and 16 `requirements/og/area-<areaId>.png` files, and no
  `areas.png`, `area.png`, `use-case.png` or `behaviour.png`. The PR shows `areas-card.png`,
  `area-myst.png` and the longest title's picture (`area-palette-slash.png`) as screenshots,
  per the pull-request guideline.
- In the built `requirements/myst/StRS-MDOKFSTUDIO-MYST-005/index.html` and
  `requirements/rendering-core/SwRS-MDOKFSTUDIO-CORE-022/index.html`: `og:image` is
  `<SITE_URL>requirements/og/area-myst.png` and `.../area-rendering-core.png`; `og:title` is
  `<title> (<full ID>)`; the descriptions are the whole user need and the rule without backticks
  or link syntax; the `<title>` is unchanged. In `requirements.html`: the index's tags. The PR
  body quotes these tags.
- After merge and deploy (not the Driver's gate, and no agent posts on X): `delivery.md` tells
  the owner to reshare `/requirements/?v=2`, `/requirements/myst/?v=2`, the MYST-005 and
  CORE-022 pages with `?v=2`, and `/requirements?v=2`, and lists the optional curl check (each
  page and its `og:image`: 200, `image/png`). If the cards still fail, a new CR.

No CI job changes; no host or default matrix (the site build does not depend on a host or a
setting).

## Sibling CRs

`4-batch/2-actives/440-requirements-viewer-shows-table-scenario` (CR-440) and
`4-batch/2-actives/441-requirements-path-graph-design` (CR-441), both in batch-07 and in the
same stack, and `1-inbox/requirements-viewer-ids`, also edit
`test/site/requirementsViewer/pages.ts`, `shell.ts`, `layout.ts`, `viewer.css` and
`requirements/tiers/log.md`: whichever lands second rebases. This CR adds `shareTitle` and
`area` to the page specs, changes their `description`, and removes `MapSummary.description`;
it does not touch the tab titles or the visible IDs that viewer-ids changes.

## Decided in the spec

The answers leave these points open; each is decided here, the option most consistent with the
product and the answers:

1. The category description is `A feature category of Markdown OKF-Schema Studio:
   <category scope>`, whole (only behaviours are cut, per Q11), with the scope's backticks
   removed by `plainText`.
2. A use case whose user need is empty falls back to its description (none today); the
   statistics sentence and `MapSummary.description` are removed.
3. The category picture's content beyond the answers (eyebrow, title, colour): the line "Use
   cases and behaviours, linked to code and tests" and the three layers outlined in the category
   colour; no counts, so the picture does not change with every new requirement.
4. The index picture is named `areas-card.png` (the example of Q7).
5. The stub's `og:url` is `<SITE_URL>requirements/`, the canonical page, so X groups both URLs
   under one card; its `<title>` stays a tab title, unchanged.
6. The real-requirements word check reads the Markdown bundle with `yaml`, not the okfreq
   report, so it runs in `just check` and in `ci-static`.
