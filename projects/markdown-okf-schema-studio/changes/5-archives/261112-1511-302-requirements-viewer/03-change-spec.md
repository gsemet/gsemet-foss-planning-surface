---
title: Change spec - a requirements viewer on the published site
cr: none yet (backlog P2; take the next free number when it is opened)
date: 2026-11-12
issue: none
priority: P2
depends_on:
  - P1/strs-main-paths (the `### Main paths` sections and their check)
  - P1/gallery-page-social-card (the social card mechanism of the site build)
status: specified
---

# Change spec: a requirements viewer on the published site

## Goal

The published site (https://gsemet.github.io/markdown-okf-schema-studio/) shows the requirements of
Studio as a viewer that a reader moves through one level at a time, on a wide screen and on a phone: the areas, the
use cases (StRS) of one area, one use case drawn as a metro map of its main paths with its
behaviours (SwRS) as the transitions, and one behaviour with its rule, scenarios, source files and
tests. Search works everywhere. The pages teach people outside the project why the requirements
are written this way: plain, professional, a little striking, no hype, no glow, no particles, no
"AI slop" (owner, 2026-10-24 and 2026-11-12).

The viewer replaces today's Requirements page (`requirements.html`): the menu's Requirements link
opens the viewer, and the viewer's home page shows the information and statistics that page shows
today (owner: "Replace by your viewer, just ensure the root page display the same information,
stats etc").

## Context and dependencies

This change runs after two P1 changes of the same batch and is stacked above them (one gh stack).
It builds on them and does not redo them:

- `P1/strs-main-paths` writes a `### Main paths` section into every active StRS where the SwRS form
  a path (format: `main-paths/FORMAT.md` of this folder, documented by that change in
  `requirements/guidelines/project.guidelines.md`), and adds the project script, run by
  `just requirements-lint` and CI, that checks every SwRS id of a Main paths section exists, is
  active and derives from that StRS. This change only reads the sections. When that change
  exposes a TypeScript parser of the section, reuse it; otherwise write the parser here (see
  "Data").
- `P1/gallery-page-social-card` adds the Open Graph and Twitter meta tags to the head written by
  `pageDocument` in `test/site/buildSite.ts`, and the mechanism that draws a card from an HTML
  template and shoots it with Playwright (`playwright-core`, already a dependency) into a
  1200 x 630 PNG during the site build, with absolute https image URLs. That change gives a card
  to the gallery page and also to the home, contributing and how-we-ship pages, so the head
  builder already carries the tags on every `pageDocument` page. This change reuses that
  mechanism for its four level cards; it adds no second shooter.

Read both changes as merged (or as the branches below this one in the stack) before starting.

Reference design, owner-approved: `prototype-02/` of this folder (`README.md`, `gen.py`,
`style.css`, `app.js`, `shoot.mjs`, `site/`, `site/cards/`, `site/og/`). It renders one vertical
slice (area Diagrams, use case DIAG-001, its 14 behaviours) from real data at commit 0e79699d.
The palette and design principles are in `prototypes/journey/00-design-system.html`. These files
live in the change folder (`.agents/changes/` is not tracked by git), not in the repository.

## Code today (origin/main 0e79699d)

- `test/site/buildSite.ts`: `pageDocument(title, currentPage, body)` writes every site page (head,
  site CSS, nav Home / Contributing / How we ship / Gallery / Requirements); `main()` renders the
  Markdown pages, copies images and reports, calls `writeRequirementsPage(...)` for
  `requirements.html` and writes `gallery.html`. Run by `npm run site`
  (`node --import ./scripts/register-myst-patches.mjs out/test/site/buildSite.js`), from
  `just site-assemble` and `just ci-gallery`; the Pages workflow `.github/workflows/pages.yml`
  uploads `out/site`.
- `test/site/requirementsPage.ts` (377 lines): `parseRequirementsReport`, `loadRequirementsStats`,
  `REQUIREMENTS_REPORT_PATH` (`out/reports/requirements/requirements-report.json`, written by
  `just requirements-report`), `renderRequirementsPage`, `writeRequirementsPage`,
  `extractMarkerSnippet`, the chain diagram and the worked example `SwRS-MDOKFSTUDIO-GFM-021`.
  Tested by `test/site/requirementsPage.test.ts`; requirement `SwRS-MDOKFSTUDIO-CORE-069` (marker
  companion `src/core/render/requirementsPage.markers.ts`), derived from
  `StRS-MDOKFSTUDIO-TRUST-014`.
- `test/shared/e2eGroups.ts`: `GROUPS`, the 16 areas in display order, each with `id` (= okfreq
  scope), `title` and `scope` (the description shown to the reader).
- `test/site/siteLinks.ts`: `REPOSITORY_URL`, `relativeSitePath`.
- Links to `requirements.html`: `README.md` line 7 (absolute URL, also shown on the Marketplace),
  `docs/how-we-ship.md` line 48, `CONTRIBUTING.md` line 306.

Bug found while writing this spec: `parseRequirementsReport` reads the lifecycle from
`frontmatter.lifecycle`, but the requirement files and the report carry `req_lifecycle`. Every
requirement is counted as "unknown" and active: the published page says "1116 unknown", 133 StRS
and 983 SwRS, and "Retired requirements: None", while 79 StRS and 433 SwRS are active. The viewer
hides superseded and deprecated requirements (owner's decision), so its figures must read
`req_lifecycle` (falling back to `lifecycle`). The published active counts drop to the true
figures (owner, 2026-11-12: "Yes, fix it").

## What changes

### 1. Data (one model, built once per site build)

A module (for example `test/site/requirementsViewer/model.ts`) reads:

- the okfreq report JSON at `REQUIREMENTS_REPORT_PATH` (owner: the data is the okfreq report).
  Per requirement it uses `id`, `tier`, `scope`, `path`, `text` (the whole file, front matter
  included), `derives_from`, `superseded_by`, `supersedes`, `coverage_target`,
  `implementation.status`, `tests.status`, and from `frontmatter`: `title`, `description`,
  `user_need` (StRS), `req_lifecycle`, `annotation_exemption`, `exemption_reason`,
  `implemented_in_files`, `tested_in_files`. Report-level: `generated_at`, `totals`, `scopes`.
- the area titles and descriptions from `GROUPS` of `test/shared/e2eGroups.ts`, in its order
  (owner: they exist there).
- the `### Main paths` section of each StRS, parsed from its `text`, by the rules of
  `main-paths/FORMAT.md`: `#### Path N: <name>` headings; a numbered list of states; under a
  state, the first bullet without `Option` is the step to the next state
  (`- SwRS-<ID>: <label>`); `- Option SwRS-<ID> (<nominal|boundary|refusal>): <label>` bullets are
  other outcomes, the kind optional and picking the scenarios of that SwRS it covers; the last
  state has no bullet; a state is the same state in every path when its text is the same. A SwRS
  that derives from the StRS and appears in no path is listed as "also serves this need".
- the scenarios of each SwRS, parsed from `text`: `### Scenario (<kind>): <name>` headings and
  their `GIVEN / WHEN / THEN / AND` lines; the `- Known issue:` lines.
- the commit of the build: `git rev-parse HEAD` (the Pages build checks out the tag), used for
  every source and test file link (`<REPOSITORY_URL>/blob/<sha>/<file>`) and shown in the footer.

Active = `req_lifecycle` not in `superseded`, `deprecated`, `archived` (`draft` is active and
tagged "draft"). Retired = the others.

The figures of today's page (`RequirementsStats`: active StRS and SwRS, lifecycles, marker
targets, implemented, tested, fully traceable, exemptions, known issues, StRS with a stakeholder
validation test, per scope, retired per lifecycle) move into this module unchanged in meaning,
with the lifecycle key fixed.

A missing or unreadable report never fails the site build (as today): the viewer writes its home
page with the explanation and the text "The requirements report was not generated", no figures
and no area pages. A Main paths section that cites an id absent from the report draws that
transition without a link and prints a warning; the gate on ids is the check of
`P1/strs-main-paths`, not the site build.

### 2. Generator in TypeScript, next to `buildSite.ts` (owner's choice)

- New folder `test/site/requirementsViewer/` (each file under the 1 500-line limit of `test/`):
  the model, the page writers (home, area, use case, behaviour), the metro layout, the search
  index, the level cards, the static assets (`viewer.css` from `prototype-02/style.css`,
  `viewer.js` from `prototype-02/app.js`), and an entry `writeRequirementsViewer(siteRoot, ...)`.
- `buildSite.ts` `main()` calls `writeRequirementsViewer` instead of `writeRequirementsPage`.
  The viewer shares the site's head code (owner: "sharing its head and social card code"):
  extract from `pageDocument` a head builder (charset, viewport, favicon, title, the social card
  tags added by `P1/gallery-page-social-card`) used by both `pageDocument` and the viewer pages.
  The viewer pages keep their own stylesheet and top bar from `prototype-02`.
- `test/site/requirementsPage.ts` and its test are removed or folded into the new folder; the
  marker companion `src/core/render/requirementsPage.markers.ts` moves or is renamed with them
  (markers move with the code, constitution section 1).
- No new dependency (`parse5` and `playwright-core` are already there); no web font (system font
  stacks of `prototype-02/style.css`).

### 3. Pages and URLs

All under `out/site/requirements/`, one folder per view holding an `index.html`, so every view
has a clean URL ending in `/` (owner, 2026-11-12: "Nested folders", not the flat files of
`prototype-02`):

| View | URL (folder under `requirements/`) | Content (from `prototype-02`) |
| --- | --- | --- |
| Home (areas) | `requirements/` | see section 4 |
| Area | `requirements/<area>/` | area colour, title, description, counts (use cases, behaviours, % linked to code and tests from `scopes`), its use cases as a vertical line of stops: short id, title, user need without its "As a ..., " lead, behaviour count |
| Use case | `requirements/<area>/<StRS-id>/` | see section 5 |
| Behaviour | `requirements/<area>/<SwRS-id>/` | see section 6 |

`<area>` is the okfreq scope (the `id` of `GROUPS`) of the requirement itself; a SwRS that derives
from a StRS of another area lives under its own area. `<StRS-id>` and `<SwRS-id>` are the full ids
as written (`requirements/diagrams/StRS-MDOKFSTUDIO-DIAG-001/`,
`requirements/diagrams/SwRS-MDOKFSTUDIO-DIAG-015/`); the short id (without
`StRS-MDOKFSTUDIO-` / `SwRS-MDOKFSTUDIO-`) is only a display label. Shared assets
(`viewer.css`, `viewer.js`, `search-index.js`, `og/`) sit once at `requirements/`; every link and
asset reference is relative, computed with `relativeSitePath`, so the pages also work when
served from `out/site` locally. One page per active area, StRS and SwRS of the report (today
16 + 79 + 433). Retired requirements get no page (owner: "Rows only", section 7).

Every page:

- reads without JavaScript: lists, the metro map (SVG and its phone list) and the figures are in
  the HTML; `viewer.js` only adds search, the theme switch, the History toggle memory and Play;
- has the `prototype-02` top bar: "Studio requirements" home link, breadcrumb
  (Areas / area / use case / behaviour), Search button with the `/` shortcut, Theme button
  (cream and dark, default from `prefers-color-scheme`, kept in `localStorage` key `req-theme`),
  plus the site links (Home, Contributing, How we ship, Gallery) so a reader can leave the viewer
  (owner: "Own bar + site links"; no full site header above it);
- has a footer: "okfreq report generated <generated_at> at commit <short sha>" linking the commit;
- honours `prefers-reduced-motion` (no Play animation, no transitions);
- at most one explanatory sentence per section, as in `prototype-02` (owner: simpler, explain
  directly what the reader sees, no hype).

`out/site/requirements.html` becomes a small redirect page (meta refresh and a link to
`requirements/`, `rel="canonical"`), so the README and Marketplace links keep working (owner:
"Yes, redirect"). The `Requirements` link of `pageDocument`'s nav points to `requirements/`
(relative, `requirements/index.html` where a file path is needed). `README.md`,
`docs/how-we-ship.md` and `CONTRIBUTING.md` link the new URL
(`https://gsemet.github.io/markdown-okf-schema-studio/requirements/` in the README).

### 4. Home page: the areas, then the information and figures of today's page

Top, as `prototype-02/site/index.html`: the title "Requirements of Markdown OKF-Schema Studio",
one lead sentence, the three layers (Use case / StRS count, Behaviour / SwRS count, Code and tests
/ % linked from `totals.combined_coverage_percent`), then the 16 areas as rows (colour swatch,
title, description, use cases, behaviours), each opening its area page.

Below, the same information and statistics as today's `requirements.html`, shortened to the
viewer's one-sentence style (owner, 2026-11-12: "Shortened"): one short paragraph or sentence per
section for what the requirements are, why we keep them, how it works (with the chain diagram:
StRS -> SwRS -> `@implements_req` -> `@tests_req`, cross-cutting rules with `depends_on`), the
worked example `SwRS-MDOKFSTUDIO-GFM-021` with its marker snippets read from the repository files
(linking to its behaviour page), and what keeps it in sync (the CI checks named in one line). The
figures stay whole: the stat cards, the per-area table (now with the area titles and links to the
area pages) and the retired table. The "Browse the requirements ... planned and not available
yet" paragraph goes: the areas above replace it. Nothing of today's information is dropped; only
the wording is cut.

### 5. Use case page: the metro map (only here; owner's decision)

As `prototype-02/site/use-case-diag-001.html`:

- eyebrow with the area colour and the short id, the title, the user need as a quote;
- "How it is split": one hint sentence, Play buttons (one per path), the legend (path 1, path 2,
  other outcome, nominal / boundary / refusal scenario dots);
- wide screens: the map as an SVG drawn at build time (layout of `gen.py` `graph()` and
  `metro_svg()`): states as circles (the final state larger), each main-path transition a thick
  line in the path colour labelled with the SwRS short id, its test count and its scenario dots
  and the step text; a transition shared by two paths shows both colours; `Option` transitions
  are dashed branches to a small outcome node; every transition links to its behaviour page;
- narrow screens (760 px and below): the same map as a vertical HTML line per path
  (`metro_list()`), the SVG hidden;
- Play walks a dot along a path step by step (`app.js`), off under reduced motion;
- the combinatorics sentence (owner's idea): "This map has <W> different ways through it in 8
  steps or fewer. Instead of testing each one end to end, the <B> behaviours on the map are
  tested one by one, with <S> scenarios." W is computed as `gen.py` `walks()` does: walks from the
  first state of path 1, at most 8 transitions, each transition counted once per scenario it
  covers (filtered by the Option kind when given);
- "Behaviours of this use case": every active SwRS deriving from the StRS (id, title, scenario
  dots, test count), those absent from the map tagged "not on the map";
- a StRS without a `### Main paths` section shows one sentence saying its paths are not written
  yet, no map, no combinatorics sentence, and the behaviour list.

### 6. Behaviour page

As `prototype-02/site/behaviour-diag-015.html`:

- eyebrow with the area colour and the short id, the title, the rule (`description`, `SHALL` and
  `SHALL NOT` in bold);
- where it sits: for each use case it derives from, either "Step i of path p in <StRS>: from
  "<state>" to "<next state>"" with the small track, or "Another outcome at step i of path p", or
  "Part of <StRS>, outside the paths drawn on its map" (a SwRS deriving from several StRS, 141
  today, lists each);
- the scenarios as closed `<details>` with their kind and name, Given / When / Then columns; "Stated
  as one rule, without scenarios" when there is none;
- "Implemented in" and "Tested by" file lists linking to GitHub at the build commit; each test file
  tagged by its folder: `test/integration` integration, `test/visual` visual, `sphinx` sphinx,
  `test/build` build, otherwise unit; an exempt SwRS shows its `exemption_reason`;
- "Known limits (n)" as a `<details>` when it has Known issue lines;
- previous / next among the behaviours of the use case of the breadcrumb;
- breadcrumb Areas / its own area / the first StRS of its `derives_from` / its short id.

### 7. Retired requirements: hidden, History shows them (owner's decision)

Superseded and deprecated (and archived) requirements are hidden by default. A History toggle in
the top bar shows them, working without JavaScript (a checkbox and CSS) and remembered across
pages by `viewer.js`. Shown: on an area page its retired use cases, on a use case page its retired
behaviours, on a behaviour page the requirements it supersedes; each retired row shows its
lifecycle and "superseded by" links to the pages of its replacements, and links its own Markdown
file on GitHub at the build commit. Retired requirements are not in search unless History is on.

### 8. Search everywhere

`requirements/search-index.js` (as `prototype-02`), written at build time for the whole report:
areas, use cases, behaviours (id, title, rule) and files (each file links to the first behaviour
it carries, with the count of behaviours). The search sheet opens with the button or `/`, matches
on two characters or more, groups results by Areas, Use cases, Behaviours, Files, moves with the
arrow keys, opens with Enter, closes with Escape or a click outside.

### 9. Social cards: one picture per level, page text per page (owner's decisions)

Every viewer page carries the meta tags of `P1/gallery-page-social-card`'s head: `og:type`,
`og:site_name`, `og:title`, `og:description`, `og:url` (absolute, the folder URL ending in `/`), `og:image` (absolute https),
`og:image:width` 1200, `og:image:height` 630, `og:image:alt`, `twitter:card` =
`summary_large_image`. Title and description are the page's own (as `gen.py` `page()` calls).
The image is one of four PNG shared by every page of a level, `requirements/og/areas.png`,
`area.png`, `use-case.png`, `behaviour.png`, drawn from four card templates (as
`prototype-02/site/cards/<level>.html`: the level in one line and the chain use case -> behaviour
-> code and tests with that level marked, brand line at the bottom) and shot by the shared
mechanism. Per-StRS images (a metro map per use case) are a later change (owner, 2026-11-12).

### 10. Requirements (okfreq)

Follow `requirements/guidelines/requirements.guidelines.md` and "During a change" of
`requirements/guidelines/project.guidelines.md`.

- Update `SwRS-MDOKFSTUDIO-CORE-069` (proposed, not approved: no owner agreement needed): the
  site build writes the viewer home page `requirements/index.html` with the areas, the chain, the
  worked example and the figures of active requirements (read from `req_lifecycle`), or says the
  report was not generated, without failing; `requirements.html` redirects to it. Its scenarios
  and verification notes follow the new tests.
- New SwRS with `okfreq new ... --lifecycle proposed`, scope `rendering-core`, derived from
  `StRS-MDOKFSTUDIO-TRUST-014` like CORE-069, one per testable behaviour, for example: the area
  and use case pages and their lists; the use case map from its Main paths (SVG, phone list,
  combinatorics, no-section case); the behaviour page (where on the paths, scenarios, files at
  the commit, test kinds); retired requirements hidden behind History (rows only); the search index; the
  level social cards. Markers: `@implements_req` in a marker companion under
  `src/core/render/` (the CORE-069 pattern), `@tests_req` at each test.
- `just requirements-update`, and a dated entry in `requirements/tiers/log.md`.

## Out of scope

- Writing the Main paths sections and their check (`P1/strs-main-paths`).
- The gallery page card and the card mechanism itself (`P1/gallery-page-social-card`).
- Any okfreq or okf-schema change; the okf-schema one-page viewer (the 2026-10-25 wait is
  superseded).
- One social image per StRS with its metro map.
- StRS validation tests; editing requirements from the site; the pick panel and the design system
  page of the journey prototypes; animated numbers, taglines, glow or particles.
- The writing skill: no rendered syntax changes.

## Evidence

### Checks

- `just check` passes (TypeScript, boundaries, file sizes, unused exports, marker companions,
  unit, `just requirements-lint` with the Main paths check of `P1/strs-main-paths`).
- `just preflight` passes (completion gate); `just ci-gallery` builds `out/site/requirements/`.
- Unit tests (node:test, under `test/site/`), each failing on the previous code:
  - Main paths parser on the `main-paths/StRS-MDOKFSTUDIO-DIAG-001.md` sample: 2 paths, 6 and 2
    states, the shared state "The diagram is drawn as a picture", the Option kinds; a StRS
    without the section; an unknown id.
  - Model on a fixture report: active vs retired from `req_lifecycle`; figures equal to the
    expected counts (the CORE-069 fixture rewritten with `req_lifecycle`, saying why the
    assertion changes); scenarios and Known issue lines parsed.
  - Pages on the fixture: one `requirements/<area>/[<id>/]index.html` per active area, StRS and
    SwRS (a cross-area SwRS under its own area), none for retired ones; relative links and asset
    paths resolve from every depth; the
    lists, the SVG and the phone list are in the HTML (no JavaScript needed); breadcrumb; file
    links `<REPOSITORY_URL>/blob/<sha>/...`; test kind tags; retired rows marked hidden with their
    "superseded by" links; the no-Main-paths sentence; the walk count of a small fixture map
    computed by hand.
  - Home: the three layers, the 16 areas, the shortened sections, the worked example and every
    figure of today's page; degraded text
    without a report and the build does not throw.
  - Search index entries for each kind; retired entries flagged.
  - Social tags on one page of each level: own `og:title`, absolute `og:url`, `og:image` =
    `.../requirements/og/<level>.png`, 1200 x 630, `summary_large_image`.
  - `pageDocument` nav links `requirements/` from root and nested pages;
    `requirements.html` redirects there (the old assertion on `requirements.html` changes, say
    why).

### Scenario steps (before the PR is ready; screenshots in the PR body)

1. `just requirements-report && npm run compile && npm run site` (or `just site-assemble`), then
   serve `out/site` (`python3 -m http.server -d out/site`).
2. At 1440 px, cream then dark: open the site home, click Requirements in the menu: the viewer
   home (`/requirements/`) shows the layers, the 16 areas, then the short explanation and the
   figures (79 StRS / 433 SwRS at
   0e79699d, not 133 / 983).
3. Open Diagrams (`/requirements/diagrams/`), then DIAG-001
   (`/requirements/diagrams/StRS-MDOKFSTUDIO-DIAG-001/`): the map shows two paths; Play path 1 walks the dot; the
   combinatorics sentence is there; click DIAG-015 on the map: its page shows step 4 of path 1,
   scenarios, files with kind tags; the file links open GitHub at the build commit.
4. Open a use case without Main paths: the sentence and the behaviour list, no map.
5. Turn History on: retired rows appear with "superseded by" links; turn it off; reload: kept.
6. Press `/`, type `DIAG-015`, then a file name such as `mermaidError.ts`: grouped results, Enter
   opens them.
7. At 375 px: the same walk; the map is the vertical list; no horizontal scroll on any page.
8. With JavaScript off: every list and the map read; search and Play are absent.
9. With reduced motion on: Play does nothing, no transition.
10. Open `requirements.html`: it lands on `requirements/`.
11. View the source of one page per level: the card tags; open each `og/*.png`: 1200 x 630, the
    level marked. After deploy, the published `og:image` URLs return those PNG.
12. Accessibility: landmarks, focus visible, keyboard access to every link and button, text
    contrast in both themes (Lighthouse accessibility 95 or more on the four views when Chrome's
    Lighthouse is at hand).

## Decisions of the owner carried in (2026-11-12)

The six questions of the first version of this spec are answered (`02-answers.md`, "Spec
questions"): nested folder URLs (section 3); own bar with the site links (section 3); retired
requirements as rows only (section 7); the lifecycle fix (section "Code today"); the redirect of
`requirements.html` (section 3); the home text shortened, the figures kept (section 4). No open
question remains.
