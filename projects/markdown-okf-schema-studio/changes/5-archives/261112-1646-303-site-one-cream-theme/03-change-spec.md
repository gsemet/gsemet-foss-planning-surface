# Change Specification: one cream look for the whole published site

## Goal

The GitHub Pages site has one look: the cream theme of the extension, on every page and every
social picture. Today the main pages (home, Contributing, How we ship, Gallery, Reports) are teal
on light paper with a dark palette from the system, and the requirements viewer is cream and
sepia with its own Theme button. After this change both use the same palette, the same typography
and the same header, with no dark mode.

> [!NOTE]
> The owner triaged this change as automatable: this specification is not reviewed by the owner.
> The decisions below come from `02-answers.md`; the open questions at the end are for the owner.

## Decisions carried from the grill

1. One homogeneous look between the extension's cream theme and the published site: every page of
   the GitHub Pages site (home, Contributing, How we ship and every other page rendered from
   `docs/`, Gallery, Reports index, every requirements viewer page) is cream.
2. The requirements viewer's theme (palette and typography) is the model for every page.
3. The single colour reference is the extension's cream palette, in
   `src/core/preview/styles/pageChromeStyles.ts`, the block
   `html[data-sphinx-preview-theme-mode="cream"]` (background `#f5f1e8`, text `#2b2a27`, link
   `#a14e32`, border `#d6cdbd`, and the rest of that block). The viewer aligns on it: its current
   cream values (`#f6f1e7`, `#2b2620`, `#e5ddce`, …) are replaced.
4. No dark mode: no dark palette, no `prefers-color-scheme: dark` rule, no Theme button.
5. One header on every page: the logo and five links (Home, Contributing, How we ship, Gallery,
   Requirements), plus the breadcrumb on the requirements pages.
6. The social cards are cream too, in this change: the cards of the main pages and the four level
   cards of the viewer.
7. No change to the extension itself: nothing in `src/` changes except a requirement marker file
   (see "Requirements").

## What changes

### 1. One set of site tokens: `test/site/siteTheme.ts`

Replace `DARK_THEME_CSS` with the shared site stylesheet source, used by every generator:

- The colour tokens, on `:root`, with `color-scheme: light`. Each token takes its value from the
  extension's cream block:

  | Site token | Use | Extension variable | Value |
  | --- | --- | --- | --- |
  | `--bg` | page background, header | `--studio-editor-background` | `#f5f1e8` |
  | `--paper` | panels, cards, buttons | `--studio-editorWidget-background` | `#fbf8f1` |
  | `--ink` | text, headings | `--studio-foreground` | `#2b2a27` |
  | `--soft` | secondary text | `--studio-descriptionForeground` | `#5e5850` |
  | `--line` | borders, rules | `--studio-widget-border` | `#d6cdbd` |
  | `--faint` | separators, faint marks | `--studio-input-border` | `#cfc5b2` |
  | `--link` | links | `--studio-textLink-foreground` | `#a14e32` |
  | `--focus` | focus ring | `--studio-focusBorder` | `#b05a3c` |
  | `--code-bg` | `pre`, `code` | `--studio-textCodeBlock-background` | `#ede6da` |
  | `--quote-bg` | `blockquote` | `--studio-textBlockQuote-background` | `#efe9dd` |
  | `--p1` | path 1, goal, `SHALL` | `--studio-textLink-foreground` | `#a14e32` |
  | `--p2` | path 2 | `--studio-charts-purple` | `#6b4a8a` |
  | `--nom` | nominal, passed | `--studio-charts-green` | `#34703f` |
  | `--bnd` | boundary | `--studio-charts-blue` | `#2f6690` |
  | `--ref` | refusal, failed | `--studio-errorForeground` | `#b3261e` |
  | `--alt` | option lines | `--sphinx-preview-scrollbar-hover` | `#a89d89` |
  | `--kt` | text on a coloured label | `--studio-button-foreground` | `#ffffff` |

- The font stacks of the viewer: `--serif`, `--sans`, `--mono` (values unchanged from
  `test/site/requirementsViewer/viewer.css`), and the viewer's rule "serif for what is read, sans
  for labels, mono for identifiers".
- The base rules (body, links, `pre`, `code`, `blockquote`, focus ring) and the header rules
  (section 3).

A test fails when a site token drifts from the extension: it reads the cream block of the exported
`PAGE_CHROME_CSS` (`src/core/preview/styles/pageChromeStyles.ts`) and asserts each value of the
table above.

Keep the per-area colour `--c` of the viewer as it is: it means the area, not the theme (see open
question 3).

### 2. The main pages: `test/site/buildSite.ts` (`pageDocument`)

- Remove the teal palette (`--accent`, `--accent-strong`, `--warm`, `--success`, `--danger` and
  their values) and the `${DARK_THEME_CSS}` interpolation; use the site tokens of section 1.
- Typography of the viewer: body in `--sans` at the viewer's size and line height; reading text of
  the rendered Markdown (paragraphs, list items, block quotes) and `h1` in `--serif`; code in
  `--mono`. Headings `h2`, `h3` follow open question 1.
- Replace every hard-coded colour of the gallery and its capture viewer with tokens: `#eef3f2`
  (`pre`, `.capture-open`, `.capture-actions li`, `.capture-image`) and `#e8efed` (`code`) become
  `--code-bg`; `#fff9ef` (`blockquote`) becomes `--quote-bg`; `#10191d` (video background) and the
  backdrop `#16242ccc` become `--ink`-based values; the passed and failed status badges use
  `--nom` and `--ref` for text and border, on a light tint of the same colour.
- `.report-link` uses `--link` for its border.

### 3. One header for every page

Write the header once (for example `siteHeader(currentPage, extras)` in a new
`test/site/siteHeader.ts`) and call it from `pageDocument` and from `viewerDocument`
(`test/site/requirementsViewer/shell.ts`).

- Content, in order: the brand link to the home (the logo `images/logo.svg`, 44 x 44, and the name
  "Markdown OKF-Schema Studio", as `class="site-brand"` today), then the five links Home,
  Contributing, How we ship, Gallery, Requirements, all resolved relative to the page (as
  `relativeSitePath` and `relativeFolderLink` do today).
- On the requirements pages only, the header also holds the breadcrumb (`nav.crumbs`,
  `aria-label="Breadcrumb"`), the History checkbox and label, and the Search button. The History
  checkbox stays inside the header landmark (test "the History checkbox sits inside the header
  landmark").
- Style: the viewer's sticky header (`.top`: background `--bg`, bottom border `--line`).
- The viewer's dot link "Studio requirements" (`.home`, with its `::before` circle) is removed:
  the logo brand replaces it; the breadcrumb's first crumb "Areas" and the Requirements link lead
  to the requirements home.
- The viewer gains the fifth link, Requirements (today it has four).
- Narrow screens (760 px and below): the header wraps as the viewer's does today; no horizontal
  scroll of the page at 375 px.

### 4. The requirements viewer: no dark mode, aligned palette

- `test/site/requirementsViewer/viewer.css`: remove the `[data-theme=cream]` and
  `[data-theme=dark]` blocks; the tokens come from section 1 (shared source, not a copy). Remove
  the `.home` rules. Keep every other rule.
- `test/site/requirementsViewer/shell.ts`: remove `THEME_SCRIPT` and its `<script>`, the Theme
  button (`id="theme"`), and `#theme` from `NOSCRIPT_STYLE` (which keeps `#search-open` and
  `.play`). No page sets `data-theme`.
- `test/site/requirementsViewer/viewer.js`: remove the theme switch and the `req-theme`
  `localStorage` key; update the head comment ("theme switch" goes).
- The shared stylesheet reaches the viewer from the single source of section 1: either
  `write.ts` writes it before the copied `viewer.css`, or a shared `site.css` at the site root is
  linked by every page. The Driver chooses; there is one source.

### 5. Social cards in cream

- `test/site/socialCard.ts` (`CARD_CSS`): the site tokens replace the teal ones. The band uses
  `--link`; the brand bar background `#ffffff` becomes `--paper`; the eyebrow uses `--link`; the
  headline uses `--ink`; the line uses `--soft`; mosaic image backgrounds `#ffffff` become
  `--paper`. Fonts follow open question 2.
- `test/site/requirementsViewer/cards.ts` (`CARD_STYLE`): `.chain li` background `#ffffff`
  becomes `--paper`; `--accent` becomes `--link`; the lit shadow `rgba(14, 105, 116, .16)` becomes
  the same shadow in `#a14e32` (`rgba(161, 78, 50, .16)`).
- All eight pictures are cream: `og/home.png`, `og/contributing.png`, `og/how-we-ship.png`,
  `og/gallery.png`, `requirements/og/areas.png`, `area.png`, `use-case.png`, `behaviour.png`.

### 6. Requirements (okfreq)

Read `requirements/guidelines/requirements.guidelines.md` and
`requirements/guidelines/project.guidelines.md` ("During a change") first.

- No `approved` requirement is touched: CORE-069 and CORE-080 to CORE-085 are `proposed`.
- Create one SwRS with `okfreq new … --lifecycle proposed`, scope `rendering-core`, deriving from
  `StRS-MDOKFSTUDIO-TRUST-014` (as CORE-069 and CORE-085). Its behaviour: when a maintainer builds
  the Pages site, every page and every social picture uses the cream palette of the extension
  (named values), every page carries the one header (logo and the five links; the breadcrumb on
  the requirements pages), and no page has a dark palette, a `prefers-color-scheme: dark` rule or
  a theme switch. Scenarios: a main page, a viewer page, a social card, the token drift test.
- `@implements_req` for it in a companion markers file under `src/core/render/`, following the
  pattern of `src/core/render/requirementsViewer.markers.ts` (the site build is outside the marked
  source directories); `@tests_req` at each new or changed test.
- SwRS-MDOKFSTUDIO-CORE-069, "Verification notes": replace "The published look in light and dark
  is not asserted." with a sentence that says the look is cream only and is asserted by the new
  SwRS's tests.
- Run `just requirements-update`, commit the generated files, and add a dated entry in
  `requirements/tiers/log.md` (heading `## 2026-11-12` or the day of the change, topic in a
  `### Topic` sub-heading).

### 7. Glossary

If the code introduces a shared name for the header or the token set (for example "Site header"),
add it to `.agents/glossary/common.md`.

## Tests to change, and why

The constitution forbids changing an assertion's intent silently; these change because the owner
removed the dark mode:

- `test/site/requirementsViewer/write.test.ts`, "the viewer writes …": asserts
  `home.includes("prefers-color-scheme: dark")`. It becomes the opposite: the home has no
  `prefers-color-scheme: dark` and no `data-theme`, and still links its stylesheet.
- `test/site/requirementsViewer/pages.test.ts`, "without JavaScript the search, Play and theme
  controls are hidden": the loop drops `#theme` and the test asserts that no page has a
  `id="theme"` button; rename it to "without JavaScript the search and Play controls are hidden".
- `test/site/siteLinks.test.ts`: the branding and How we ship tests stay; add the same checks for
  a viewer page (logo brand and the five links, resolved from `requirements/<area>/<id>/`).

## New tests (each fails on the previous code)

- Token drift: each site token equals the value of its extension variable in the cream block of
  `PAGE_CHROME_CSS`.
- No dark mode: `pageDocument(...)` and `viewerDocument(...)` contain no
  `prefers-color-scheme: dark`, no `data-theme`, no `req-theme`, no `id="theme"`; the generated
  stylesheet has none of the old teal values (`#0e6974`, `#084b55`, `#16242c`, `#f7faf9`) nor the
  old viewer cream values (`#f6f1e7`, `#2b2620`, `#e5ddce`).
- One header: a main page and a viewer page both carry the logo brand and the five links, in the
  same order; only the viewer page has `nav.crumbs`.
- Cards in cream: `cardDocument(...)` and `levelCardBody(...)` documents contain `#f5f1e8` (or the
  shared tokens) and none of the teal values.

## Evidence

At the pushed head:

1. `just check` passes (formatting, TypeScript, file size: `buildSite.ts` stays below 1 500 lines,
   unit tests including the new ones).
2. `just requirements-lint` and `just requirements-update` (no diff left after commit).
3. Build the site: `just site-assemble` (or `npm run site` after `just requirements-report`).
   Then in `out/site/`: `grep -rl "prefers-color-scheme: dark\|data-theme\|req-theme\|#0e6974" .`
   prints nothing (HTML, CSS and JS files).
4. Screenshots, before and after, at 1280 x 800 and 375 x 812, of: `index.html`,
   `contributing.html`, `docs/how-we-ship.html`, `gallery.html` with a capture opened,
   `reports/index.html`, `requirements/index.html`, one area page, one use case page with its map,
   one behaviour page with History on. And the eight social pictures. Placed in the PR as
   `.agents/guidelines/pull-request.guidelines.md` ("Screenshots in the PR") says; light only,
   since there is no dark mode.
5. Scenario steps on the built site, in a browser:
   - Open the home, follow each of the five header links: each page has the same header, cream,
     with the logo.
   - On a requirements page: the breadcrumb shows, History reveals retired rows, Search opens
     with `/`; there is no Theme button.
   - Set the system to dark mode and reload: the pages stay cream.
   - Disable JavaScript and reload a viewer page: the page is cream, Search and Play are hidden,
     History still works.
   - Text contrast of `--ink`, `--soft` and `--link` on `--bg` and `--paper` is at least 4.5:1
     (WCAG AA), and white on `--nom`, `--bnd`, `--ref`, `--p1` at least 4.5:1.
6. `just preflight` passes (the completion gate).

## Out of scope

- The extension: its preview themes (`current`, `dark`, `white`, `cream`), toolbar and styles in
  `src/` do not change. The extension's cream block is read, never edited.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/`: no rendered syntax changes.
- The content and structure of the pages: Markdown sources, viewer pages (areas, use cases, map,
  behaviours, search index), the gallery's data and script behaviour, page widths.
- The per-area colours of the viewer (`--c`).
- The text of the social cards (eyebrows, headlines, lines), their size (1200 x 630) and their
  meta tags.

## Open questions

1. Headings of the Markdown pages (README, Contributing, How we ship, `docs/`): the viewer's `h2`
   is a small uppercase sans label, made for its sections, which reads poorly as a heading of a
   long document. Working default if unanswered: on the Markdown pages, `h1`, `h2` and `h3` are in
   `--serif`, colour `--ink`; the viewer keeps its own `h2` label style.
2. Typography of the social cards: working default if unanswered: headline in `--serif` (like the
   page `h1`), eyebrow, line and brand in `--sans`.
3. Per-area colours of the viewer (`--c`, default `#1d4ed8`, and the colour of each area): they
   carry meaning and are not in the extension's palette. Working default if unanswered: unchanged.
