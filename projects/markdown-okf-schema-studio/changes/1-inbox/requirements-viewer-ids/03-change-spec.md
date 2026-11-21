# Requirements viewer: search by ID, full IDs in titles and breadcrumb

The published requirements viewer (`https://gsemet.github.io/markdown-okf-schema-studio/requirements/`)
names a requirement by its short ID (`BLOCK-003`) in several places and its search cannot find a
requirement by its full ID. This change makes the full ID (`StRS-MDOKFSTUDIO-BLOCK-003`) the name
of a requirement everywhere on the viewer, and makes the search find a requirement from its full
ID, its short ID, in any case, and from a number written without its leading zeros.

Sources: `intake/request.md` (owner, 2026-11-20), `02-answers.md` (owner's answers viewer-ids-Q1
to Q5, 2026-11-21). No tracker issue. The code read is `origin/main` at `be10fe81` (after v1.11.0,
which shipped CR-443 requirements-share-cards).

## Goal, in the owner's words

- "je peux pas rechercher directement par ID": typing `StRS-MDOKFSTUDIO-BLOCK-014` in the search
  box says "Nothing matches". After the change it finds the page, and so do `BLOCK-014`,
  `block-014`, `strs-mdokfstudio-block-014` and `block-14`; the exact ID match comes first and
  Enter opens it (viewer-ids-Q1).
- "ID complet partout": the eyebrow, the browser tab title and the X share card title of a use
  case read `Use case StRS-MDOKFSTUDIO-BLOCK-003: …`, and the same for a behaviour (SwRS)
  (viewer-ids-Q2).
- "utilise StRS-MDOKFSTUDIO-BLOCK-014 a la place pour les liens partout": every place where the
  viewer names a requirement (captions, graph steps, lists, links, titles, breadcrumb) shows the
  full ID (viewer-ids-Q2).
- "Tous les requirements": every requirement in the breadcrumb is in full ID:
  `Areas / Block editing / StRS-MDOKFSTUDIO-BLOCK-003`, and on a behaviour page
  `Areas / Block editing / StRS-MDOKFSTUDIO-BLOCK-003 / SwRS-MDOKFSTUDIO-BLOCK-014` (viewer-ids-Q3).

## Where the viewer stands at origin/main

The viewer is built by the TypeScript under `test/site/requirementsViewer/` (pages written by
`writeViewerPages` in `write.ts`, the browser script `viewer.js` and the index `search-index.js`
copied next to the pages).

Already full ID at `origin/main` (keep as is; the test "a full ID is the text of every link to a
requirement" in `pages.test.ts` guards them): the use case list of an area page, the list of
behaviours of a use case, the retired rows and their "superseded by" links, the "Step N of path M
in <use case>" caption of a behaviour page, the pills and the other-outcome labels of the use case
map and its phone list (`layout.ts`, `pill`, `metroList`), and the `<title>` tooltips of the map.
The owner's screenshot of BLOCK-003 (`evidence/block-003-path-graph-overlap-top.jpg`) shows short
IDs in the pills because the published site predates that change.

Still short ID at `origin/main`, every place this change fixes (all use `shortId` of `urls.ts`):

| Place | Code | Today | After |
|---|---|---|---|
| Use case eyebrow | `useCasePage`, `pages.ts` | `Use case BLOCK-003` | `Use case StRS-MDOKFSTUDIO-BLOCK-003` |
| Use case tab title | `useCasePage` `title` | `Use case BLOCK-003: <title> \| Studio requirements` | `Use case StRS-MDOKFSTUDIO-BLOCK-003: <title> \| Studio requirements` |
| Use case share title (og:title, twitter:title) | `useCasePage` `shareTitle` | `<title> (StRS-MDOKFSTUDIO-BLOCK-003)` | `Use case StRS-MDOKFSTUDIO-BLOCK-003: <title>` |
| Use case breadcrumb | `useCasePage` `crumbs` | `Areas / Block editing / BLOCK-003` | `Areas / Block editing / StRS-MDOKFSTUDIO-BLOCK-003` |
| Behaviour eyebrow | `behaviourPage` | `Behaviour BLOCK-014` | `Behaviour SwRS-MDOKFSTUDIO-BLOCK-014` |
| Behaviour tab title | `behaviourPage` `title` | `Behaviour BLOCK-014: <title> \| …` | `Behaviour SwRS-MDOKFSTUDIO-BLOCK-014: <title> \| …` |
| Behaviour share title | `behaviourPage` `shareTitle` | `<title> (SwRS-MDOKFSTUDIO-BLOCK-014)` | `Behaviour SwRS-MDOKFSTUDIO-BLOCK-014: <title>` |
| Behaviour breadcrumb | `behaviourPage` `crumbs` | `… / BLOCK-003 / BLOCK-014` | `… / StRS-MDOKFSTUDIO-BLOCK-003 / SwRS-MDOKFSTUDIO-BLOCK-014` |
| Pager accessible name | `behaviourPage` `pager` | `aria-label="Behaviours of BLOCK-003"` | `aria-label="Behaviours of StRS-MDOKFSTUDIO-BLOCK-003"` |
| Search result line | `searchIndex`, `searchIndex.ts` (`s` field) | `BLOCK-014 Block editing` | `StRS-MDOKFSTUDIO-BLOCK-014 Block editing` |
| Search hint | `viewer.js`, `draw` | `Type a word, an id such as DIAG-015, or a file name.` | names the full ID form (see "Search") |

`shortId` keeps one use after the change: the DOM id of a use case diagram (`ucd-…` in
`useCaseDiagram.ts`), which is never shown. Its doc comment ("only a display label, never in a
URL") is rewritten to say so. No visible text of the viewer calls it any more.

## What changes

### 1. Full ID on the use case and behaviour pages (`test/site/requirementsViewer/pages.ts`)

- `useCasePage`: the eyebrow is `Use case <full ID>`; the `<h1>` below it keeps the title, as
  today. `title` and `shareTitle` are both `Use case <full ID>: <title>` (the tab adds
  ` | Studio requirements` in `viewerDocument`, `shell.ts`, unchanged). The last crumb is the full
  ID.
- `behaviourPage`: the eyebrow is `Behaviour <full ID>`; `title` and `shareTitle` are both
  `Behaviour <full ID>: <title>`; the parent use case crumb (a link) and the last crumb are full
  IDs; the pager's `aria-label` is `Behaviours of <full ID of the use case>`.
- The share description (`description`) is unchanged: the user need of a use case, the rule of a
  behaviour (`shareDescription`).
- Area pages, the index and `requirements.html` are unchanged: they name no requirement.
- The breadcrumb wraps already (`.crumbs{…flex-wrap:wrap…}` in `viewer.css`), so the longer crumbs
  need no style change; the Chromium check below proves the breadcrumb stays inside the page at
  800 px.

This changes the share title format CR-443 shipped (`<title> (<full ID>)`): the owner's
viewer-ids-Q2 answer puts the same `Use case <full ID>: …` text in the eyebrow, the tab and the
share card. The assertions of `cards.test.ts` that pin the old format (`"Title of StRS-X-001
(StRS-X-001)"`, `"Title of SwRS-X-010 (SwRS-X-010)"`) change their expected value for that reason,
which the commit and the PR say. "Every share title is distinct" still holds and stays asserted.

### 2. Search (`searchIndex.ts`, `viewer.js`)

Index (`searchIndex`, `SearchItem`):

- A use case or behaviour entry carries the requirement's full ID: its `s` text starts with the
  full ID instead of the short ID (`StRS-MDOKFSTUDIO-BLOCK-014 Block editing`,
  `SwRS-MDOKFSTUDIO-BLOCK-014 block-editing`, plus the lifecycle on a retired entry as today), so
  the result line shows the full ID and a plain text search on `StRS-MDOKFSTUDIO-BLOCK-014` or
  `BLOCK-014` matches it.
- A new optional field `i` holds the full ID of a use case or behaviour entry (absent on Area and
  File entries), so the page matches IDs without parsing `s`. Its doc comment says so.

Page (`viewer.js`, `draw` and `q.onkeydown`):

- An **ID match**: the query, trimmed, matches an entry's `i` when its dash-separated parts equal
  the last parts of the ID, case-insensitive, the last part compared as a number. So
  `StRS-MDOKFSTUDIO-BLOCK-014`, `strs-mdokfstudio-block-014`, `MDOKFSTUDIO-BLOCK-014`,
  `BLOCK-014`, `block-014` and `block-14` all match StRS-MDOKFSTUDIO-BLOCK-014; `block-14` does not
  match BLOCK-140 as an ID match. `StRS-MDOKFSTUDIO-BLOCK-14` matches the StRS only, never the SwRS
  of the same number.
- The results list the ID matches first, then the other hits as today (substring of `t + " " + s`,
  in index order), each entry once; the cap of 30 counts the ID matches first, so an ID match is
  never cut. The first ID match is selected (`sel = 0`, as today), so Enter opens it.
- The History filter is unchanged: a retired entry, ID match or not, shows only when History is
  on.
- The minimum query length (2 characters) and the "Nothing matches" message are unchanged.
- The hint shown under 2 characters names the full ID form and says the short form works:
  `Type a word, an ID such as SwRS-MDOKFSTUDIO-DIAG-015 or DIAG-015, or a file name.`
- Headings in the results: today a kind heading (`Use cases`, `Behaviours`, `Files`) is written
  each time the kind changes. With the ID matches first, the order of headings is open question 2;
  until it is answered the spec keeps today's rule (a heading at each change of kind), which can
  write a kind heading twice.
- A short ID shared by a use case and a behaviour (`BLOCK-014` names both StRS-MDOKFSTUDIO-BLOCK-014
  and SwRS-MDOKFSTUDIO-BLOCK-014) gives two ID matches. Until open question 1 is answered, they
  come in index order (use case, then behaviour), so Enter opens the use case.

### 3. Requirements (`requirements/`, okfreq)

All the touched SwRS are `proposed` (none `approved`), so no owner re-approval is needed; StRS
CORE-008 (`proposed`) is not changed.

- **New SwRS** (`okfreq new … --lifecycle proposed`, scope `rendering-core`, `derives_from:
  StRS-MDOKFSTUDIO-CORE-008`): "The site requirements viewer finds a requirement by its ID". Normative
  statement: the search finds a requirement from its full ID, its short ID, in any case and with
  the number written without leading zeros; the ID matches come first and Enter opens the first.
  Scenarios: nominal (full ID, short ID, any case), boundary (`block-14` finds BLOCK-014 first and
  BLOCK-140 only after it as a text hit; a short ID shared by a use case and a behaviour, as open
  question 1 settles), refusal (a retired ID match stays hidden while History is off).
  `@implements_req` at the ID matching code in `viewer.js`; `@tests_req` in each test below that
  checks it.
- **New SwRS**, same scope and parent: "The site requirements viewer names every requirement by its
  full ID". Normative statement: the eyebrow, the tab title, the share title, every crumb and the
  pager's accessible name of a use case or behaviour page name the requirement by its full ID, in
  the form `Use case <full ID>: <title>` / `Behaviour <full ID>: <title>` for the tab and share
  titles. `@implements_req` in `useCasePage` and `behaviourPage`; `@tests_req` in the tests below.
  A Driver may instead extend CORE-080 and CORE-082 when the okfreq guidelines
  (`requirements/guidelines/requirements.guidelines.md`) say a change of an existing behaviour
  belongs there; the PR names which.
- **CORE-085** (social card): the scenario "Texts of a category, a use case and a behaviour" says
  the use case share title is `Use case <full ID>: <title>` and the behaviour's
  `Behaviour <full ID>: <title>` (no longer "its title then its full ID"); the normative statement
  and verification notes follow.
- **CORE-084** (search index): the "Index entries" scenario says a use case or behaviour entry
  carries the full ID of the requirement, shown in its result line.
- Markers move with the code; at most 3 IDs per marker block (`just check-markers`).
- `just requirements-update`, its generated files committed, and an entry under the `## YYYY-MM-DD` heading of the day of the change
  in `requirements/tiers/log.md` (`### Requirements viewer full IDs and ID search`).

### 4. Glossary (`.agents/glossary/common.md`)

Add **Full ID** (`StRS-MDOKFSTUDIO-BLOCK-003`: the ID a requirement is named by everywhere on the
requirements viewer) and **Short ID** (`BLOCK-003`: a search query form only, never shown). Adjust
the **Social card** entry: on a use case or behaviour page the share title is the tab title
without the site suffix.

## Out of scope

- The layout of the use case path graph (side-branch labels and test counts overlapping each other
  and the dashed lines, `evidence/block-003-path-graph-overlap-*.jpg`): its own item
  `requirements-path-graph-design` (viewer-ids-Q4).
- The share card pictures (`cards.ts`, one per area): unchanged; only the share title text changes.
- The PO gallery's own `shortId` (`test/site/poGallery.ts`, scenario IDs, not requirements).
- The URLs of the pages: unchanged (`requirements/<area>/<full ID>/`).
- Splitting from requirements-share-cards: moot, CR-443 shipped in v1.11.0 (viewer-ids-Q5).

## Evidence

Every check below reads the shipped files at the head under test: the pages are those of
`useCasePage` / `behaviourPage` / `viewerDocument` from the repository, and the search tests run
the shipped `test/site/requirementsViewer/viewer.js` read from the repository, never a copy of its
logic.

Unit tests (Node, run by `just check` and `just ci-static` on Linux and Windows):

1. `pages.test.ts`, extended "a full ID is the text of every link to a requirement" or a new test:
   on `fullIdReport()`, the use case page's eyebrow is `Use case StRS-MDOKFSTUDIO-GFM-001`, its
   `title` and `shareTitle` are `Use case StRS-MDOKFSTUDIO-GFM-001: <title>`, its crumbs are
   `Areas`, the area title, `StRS-MDOKFSTUDIO-GFM-001`; the behaviour page's eyebrow, titles, both
   requirement crumbs and pager `aria-label` carry the full IDs; the full `viewerDocument` HTML of
   each page has `<title>Use case StRS-MDOKFSTUDIO-GFM-001: … | Studio requirements</title>`, the
   same og:title and twitter:title, and no short ID as a text anywhere in the document (the
   `>(?:GFM|MYST)-\d+<` guard extended to "no short ID preceded by a space or `>` that is not part
   of a full ID", over the whole document including head and breadcrumb). This test fails on
   `origin/main`.
2. `cards.test.ts`: the two share title assertions take the new form (reason: owner's
   viewer-ids-Q2); "every share title is distinct" kept.
3. `search.test.ts`: a use case and a behaviour entry carry `i` equal to the full ID and an `s`
   that starts with it; Area and File entries have no `i`.
4. A new `test/site/requirementsViewer/searchMatch.test.ts` (or the Driver's name): it reads
   `viewer.js` from the repository and runs it in `node:vm` with a small stub of the elements it
   uses (`#history`, `#search`, `#q`, `#results`, `#search-open`, `#search-close`,
   `document.currentScript.src`, `localStorage`, `addEventListener`, `location`, no `svg.metro`),
   with `window.SEARCH = searchIndex(model)` of a fixture that holds StRS and SwRS `…-GFM-014`, a
   behaviour `…-GFM-140` and a retired ID. It types each query into `q` (`q.oninput`) and reads the
   order of the links in `#results`: `SwRS-MDOKFSTUDIO-GFM-140`'s text hit never comes before the
   ID matches of `gfm-14`; `StRS-MDOKFSTUDIO-GFM-014`, `stRs-mdokfstudio-gfm-014`, `GFM-014`,
   `gfm-14` each list the matching entries first; `StRS-MDOKFSTUDIO-GFM-14` lists the StRS only as
   an ID match; Enter (`q.onkeydown({ key: "Enter" })`) sets `location.href` to the first ID
   match's page; the retired ID is absent with History off and present with it on. This test fails
   on `origin/main` (no full ID in the index, no leading-zero match).

Chromium check (the existing `metroMap.browser.test.ts` style, skipped without Chromium unless
`STUDIO_REQUIRE_CHROMIUM=1`; run locally where Chromium starts): on a written use case page and
behaviour page of the real report (`writeViewerPages`), at 1280 px and 800 px, the breadcrumb stays
inside the page width (no horizontal page scroll). It may live in `metroMap.browser.test.ts` (so
`just ci-viewer-graph` runs it with Chromium required) or in its own file; adding it to the
`test:viewer-graph` script changes no CI job definition (`.github/workflows/ci.yml` and
`ci-viewer-graph` unchanged).

Scenario steps for the PR (captures per the pull-request guidelines), on pages written from the
real report:

1. Open `requirements/block-editing/StRS-MDOKFSTUDIO-BLOCK-003/`: the eyebrow reads
   `Use case StRS-MDOKFSTUDIO-BLOCK-003`, the tab `Use case StRS-MDOKFSTUDIO-BLOCK-003: … | Studio
   requirements`, the breadcrumb `Areas / Block editing / StRS-MDOKFSTUDIO-BLOCK-003`; the page
   source has og:title `Use case StRS-MDOKFSTUDIO-BLOCK-003: …`.
2. Open the page of SwRS-MDOKFSTUDIO-BLOCK-014 from it: eyebrow, tab and the four crumbs in full
   ID.
3. Press `/`, type `StRS-MDOKFSTUDIO-BLOCK-014`: the use case is first; Enter opens it. Repeat
   with `block-14` and `BLOCK-014`.
4. At 800 px wide, the behaviour page breadcrumb wraps and stays inside the page.

Gates: `just check`, `just requirements-lint`, `just requirements-update` (no diff left),
`okfreq validate --check-links --project-root .`, then `just preflight` (constitution, section 4;
on Windows its static stage, CI runs the others).

## Open questions for the owner

1. A short ID names both a use case and a behaviour (`BLOCK-014` is StRS-MDOKFSTUDIO-BLOCK-014 and
   SwRS-MDOKFSTUDIO-BLOCK-014; `block-14` too). Which one comes first, so that Enter opens it: the
   use case (the spec's placeholder, index order), the behaviour, or neither selected until the
   reader picks?
2. With the ID matches listed first, how are the result headings written: today's kind headings
   (`Use cases`, `Behaviours`), possibly twice (the spec's placeholder), or a heading of their own
   for the ID matches (for example `Exact match`) above the usual groups?
3. The eyebrow: `Use case StRS-MDOKFSTUDIO-BLOCK-003` above the `<h1>` title (the spec's reading:
   the title is already the heading under it), or the whole `Use case StRS-MDOKFSTUDIO-BLOCK-003:
   <title>` in the eyebrow too, repeating the heading?
