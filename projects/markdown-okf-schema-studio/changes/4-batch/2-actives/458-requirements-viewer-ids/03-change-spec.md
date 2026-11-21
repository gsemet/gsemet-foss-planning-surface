# Requirements viewer: search by ID, full IDs in titles and breadcrumb

The published requirements viewer (`https://gsemet.github.io/markdown-okf-schema-studio/requirements/`)
names a requirement by its short ID (`BLOCK-003`) in several places, and its search cannot find a
requirement by its full ID. This change makes the full ID (`StRS-MDOKFSTUDIO-BLOCK-003`) the name
of a requirement everywhere on the viewer. It also makes the search find a requirement from its
full ID, its short ID, in any case, from a number written without its leading zeros, and from a
bare number.

Sources: `intake/request.md` (owner, 2026-11-20), `02-answers.md` (owner's answers viewer-ids-Q1
to Q9, 2026-11-21, and the two points settled by the Chief of Staff). No tracker issue. The code
read is `origin/main` at `be10fe81` (after v1.11.0, which shipped CR-443 requirements-share-cards).

## Goal, in the owner's words

- "je peux pas rechercher directement par ID": typing `StRS-MDOKFSTUDIO-BLOCK-014` in the search
  box says "Nothing matches". After the change it finds the page, and so do `BLOCK-014`,
  `block-014`, `strs-mdokfstudio-block-014` and `block-14`; the exact ID match comes first and
  Enter opens it (viewer-ids-Q1). When a short ID names both a use case and a behaviour, the use
  case comes first and Enter opens it, with the behaviour right under it (viewer-ids-Q6). A bare
  number (`14`) is an ID match too: every requirement whose ID ends in that number is listed first
  (viewer-ids-Q9).
- "ID complet partout": the browser tab title and the X share card title of a use case read
  `Use case StRS-MDOKFSTUDIO-BLOCK-003: …`, and the same for a behaviour (SwRS) (viewer-ids-Q2).
  The eyebrow above the `<h1>` is the type and the full ID only:
  `Use case StRS-MDOKFSTUDIO-BLOCK-003`, without repeating the title (viewer-ids-Q8).
- "utilise StRS-MDOKFSTUDIO-BLOCK-014 a la place pour les liens partout": every place where the
  viewer names a requirement (captions, graph steps, lists, links, titles, breadcrumb, the
  previous and next links) shows the full ID (viewer-ids-Q2; the pager settled by the Chief of
  Staff).
- "Tous les requirements": every requirement in the breadcrumb is in full ID:
  `Areas / Block editing / StRS-MDOKFSTUDIO-BLOCK-003`, and on a behaviour page
  `Areas / Block editing / StRS-MDOKFSTUDIO-BLOCK-003 / SwRS-MDOKFSTUDIO-BLOCK-014` (viewer-ids-Q3).

## Where the viewer stands at origin/main

The viewer is built by the TypeScript under `test/site/requirementsViewer/`: the pages are written
by `writeViewerPages` in `write.ts`, and the browser script `viewer.js` and the index
`search-index.js` are copied next to them.

Already full ID at `origin/main` (kept as is; the test "a full ID is the text of every link to a
requirement" in `pages.test.ts` guards them):
- the use case list of an area page
- the list of behaviours of a use case
- the retired rows and their "superseded by" links
- the "Step N of path M in <use case>" caption of a behaviour page
- the pills and other-outcome labels of the use case map, and its phone list (`layout.ts`, `pill`,
  `metroList`)
- the `<title>` tooltips of the map

The full-ID pills came with CR-441 (`4-batch/3-done/441-requirements-path-graph-design`, merged as
`c121375c` "feat: draw the use case path graph as a joined map"). The owner's BLOCK-003 screenshot
(`evidence/block-003-path-graph-overlap-top.jpg`) predates it: it shows the older published site,
with short IDs in the pills.

Still short ID at `origin/main`. These are all the places this change fixes, and every one uses
`shortId` of `urls.ts`:

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
| Pager links (previous, next) | `behaviourPage` `pager` | `← <title>`, `<title> →` (no ID) | `← <full ID>: <title>`, `<full ID>: <title> →` |
| Search result line | `searchIndex`, `searchIndex.ts` (`s` field) | `BLOCK-014 Block editing` | `StRS-MDOKFSTUDIO-BLOCK-014 Block editing` |
| Search hint | `viewer.js`, `draw` | `Type a word, an id such as DIAG-015, or a file name.` | names the full ID form (see "Search") |

After the change, `shortId` keeps one use: the DOM id of a use case diagram (`ucd-…` in
`useCaseDiagram.ts`), which is never shown. Its doc comment ("only a display label, never in a
URL") is rewritten to say so. No visible text of the viewer calls it any more.

## What changes

### 1. Full ID on the use case and behaviour pages (`test/site/requirementsViewer/pages.ts`)

- `useCasePage`:
  - The eyebrow is `Use case <full ID>`, the type and the full ID only (viewer-ids-Q8). The `<h1>`
    below it keeps the title, as today.
  - `title` and `shareTitle` are both `Use case <full ID>: <title>`. The tab adds
    ` | Studio requirements` in `viewerDocument` (`shell.ts`), which is unchanged.
  - The last crumb is the full ID.
- `behaviourPage`:
  - The eyebrow is `Behaviour <full ID>`.
  - `title` and `shareTitle` are both `Behaviour <full ID>: <title>`.
  - The parent use case crumb (a link) and the last crumb are full IDs.
  - The pager's `aria-label` is `Behaviours of <full ID of the use case>`.
  - The pager's previous and next links read `← <full ID>: <title>` and `<full ID>: <title> →`.
- The share description (`description`) is unchanged: the user need of a use case, or the rule of
  a behaviour (`shareDescription`).
- Area pages: unchanged (already full ID). The index and `requirements.html` are unchanged too:
  they name no requirement.
- The breadcrumb already wraps (`.crumbs{…flex-wrap:wrap…}` in `viewer.css`). The Chromium check
  below proves that the breadcrumb, the eyebrow and the pager stay inside the page at 1280, 800 and
  390 px. If one of them does not fit, the Driver fixes it in `viewer.css`, for example by letting
  a long ID break (`overflow-wrap:anywhere`).

The share title change stands. The owner's viewer-ids-Q2 answer named the X share card with the
format `Use case <full ID>: <title>`, and it supersedes share-cards-Q9's title order: CR-443
shipped `<title> (<full ID>)`. The assertions of `cards.test.ts` that pin the old format
(`"Title of StRS-X-001 (StRS-X-001)"`, `"Title of SwRS-X-010 (SwRS-X-010)"`) change their
expected value for that reason, and the commit and the PR say so. "Every share title is distinct"
still holds and stays asserted.

### 2. Search (`searchIndex.ts`, `viewer.js`)

Index (`searchIndex`, `SearchItem`):

- A use case or behaviour entry carries the requirement's full ID: its `s` text starts with the
  full ID instead of the short ID (`StRS-MDOKFSTUDIO-BLOCK-014 Block editing`,
  `SwRS-MDOKFSTUDIO-BLOCK-014 block-editing`, plus the lifecycle on a retired entry as today). The
  result line therefore shows the full ID, and a plain text search on `StRS-MDOKFSTUDIO-BLOCK-014`
  or `BLOCK-014` matches it.
- A new optional field `i` holds the full ID of a use case or behaviour entry; it is absent on Area
  and File entries. With it, the page matches IDs without parsing `s`. Its doc comment says so.

Page (`viewer.js`, `draw` and `q.onkeydown`):

- An **ID match** is a match between the trimmed query and an entry's `i`. It is decided by either
  of two rules:
  - **ID parts.** The query has at least two dash-separated parts, and they equal the last parts of
    the ID. The comparison is case-insensitive, and the last part is compared as a number. So
    `StRS-MDOKFSTUDIO-BLOCK-014`, `strs-mdokfstudio-block-014`, `MDOKFSTUDIO-BLOCK-014`,
    `BLOCK-014`, `block-014` and `block-14` all match StRS-MDOKFSTUDIO-BLOCK-014. `block-14` is no
    ID match for BLOCK-140. `StRS-MDOKFSTUDIO-BLOCK-14` matches the StRS only, never the SwRS of
    the same number.
  - **Bare number** (viewer-ids-Q9). The query is digits only, and the number of the ID's last part
    equals it. So `14` and `014` match every requirement numbered 14, in every area
    (`…-BLOCK-014`, `…-GFM-014`, …), use cases and behaviours alike. `14` is no ID match for
    `…-140` or `…-114`.
- Order of the results:
  - The ID matches come first, in index order (use cases before behaviours, then the order of the
    report).
  - The other hits follow as today: a substring of `t + " " + s`, in index order.
  - Each entry appears once.
  - For a short ID shared by a use case and a behaviour (`BLOCK-014`, `block-14`), the use case
    comes first and the behaviour right under it (viewer-ids-Q6).
- **Cap:** the list still stops at 30 entries, and the ID matches are counted first, so an ID match
  is never cut while there are 30 or fewer of them. Text hits fill what is left. A bare number
  matching many requirements may push the text hits down or out of the list (viewer-ids-Q9).
- **Enter:** the first ID match is selected (`sel = 0`, as today), so Enter opens it. For a shared
  short ID, that is the use case.
- **Headings:** the usual kind headings (`Use cases`, `Behaviours`, `Files`) are written each time
  the kind changes, as today. With the ID matches first, a kind heading can appear twice. There is
  no extra "exact match" heading (viewer-ids-Q7).
- Unchanged:
  - The History filter: a retired entry, ID match or not, shows only when History is on.
  - The minimum query length of 2 characters: a one-digit query (`7`) still shows the hint, while
    `07` is a bare-number match.
  - The "Nothing matches" message.
- The hint shown under 2 characters names the full ID form and says the short form works:
  `Type a word, an ID such as SwRS-MDOKFSTUDIO-DIAG-015 or DIAG-015, or a file name.`

### 3. Requirements (`requirements/`, okfreq)

All the touched SwRS are `proposed`, none `approved`, so no owner re-approval is needed.

- **New SwRS** (`okfreq new … --lifecycle proposed`, scope `rendering-core`, `derives_from:
  StRS-MDOKFSTUDIO-CORE-008`): "The site requirements viewer finds a requirement by its ID".
  - Normative statement: the search finds a requirement from its full ID, its short ID or its bare
    number, in any case, with the number written with or without leading zeros. The ID matches come
    first and Enter opens the first.
  - Scenarios:
    - nominal: full ID, short ID, any case.
    - boundary: `block-14` finds BLOCK-014 first, and BLOCK-140 only after it as a text hit.
    - boundary: a short ID shared by a use case and a behaviour lists the use case first, the
      behaviour right under it, and Enter opens the use case.
    - nominal: a bare number (`14`) lists every requirement numbered 14 first, before any text hit,
      and the cap of 30 counts them first.
    - refusal: a retired ID match stays hidden while History is off.
  - Markers: `@implements_req` at the ID matching code in `viewer.js`, and `@tests_req` in each
    test below that checks it.
- **New SwRS**, same scope and parent: "The site requirements viewer names every requirement by its
  full ID".
  - Normative statement: on a use case or behaviour page, the eyebrow (type and full ID), the tab
    title, the share title, every crumb, and the pager's accessible name and link texts name the
    requirement by its full ID. The tab and share titles take the form `Use case <full ID>: <title>`
    or `Behaviour <full ID>: <title>`.
  - Markers: `@implements_req` in `useCasePage` and `behaviourPage`, and `@tests_req` in the tests
    below.
  - A Driver may instead extend CORE-080 and CORE-082, when the okfreq guidelines
    (`requirements/guidelines/requirements.guidelines.md`) say a change of an existing behaviour
    belongs there. The PR names which.
- **CORE-085** (social card): the scenario "Texts of a category, a use case and a behaviour" says
  the use case share title is `Use case <full ID>: <title>` and the behaviour's is
  `Behaviour <full ID>: <title>`, no longer "its title then its full ID". The normative statement
  and the verification notes follow.
- **CORE-084** (search index): the "Index entries" scenario says a use case or behaviour entry
  carries the full ID of the requirement, shown in its result line.
- **StRS CORE-008** (`proposed`): its statement is unchanged. Only its lists of derived SwRS are
  updated (the generated `derived_by` and Links block), through `just requirements-update`.
- Markers move with the code, with at most 3 IDs per marker block (`just check-markers`).
- Run `just requirements-update` and commit its generated files. Add an entry under the
  `## YYYY-MM-DD` heading for the day of the change in `requirements/tiers/log.md`, titled
  `### Requirements viewer full IDs and ID search`.

### 4. Glossary (`.agents/glossary/common.md`)

- Add **Full ID**: `StRS-MDOKFSTUDIO-BLOCK-003`, the ID a requirement is named by everywhere on the
  requirements viewer.
- Add **Short ID**: `BLOCK-003`, never used to name a requirement on a page, but accepted in the
  search.
- Adjust the **Social card** entry: on a use case or behaviour page, the share title is the tab
  title without the site suffix.

## Out of scope

- The layout of the use case path graph: side-branch labels and test counts that overlap each other
  and the dashed lines (`evidence/block-003-path-graph-overlap-*.jpg`). That is its own item,
  CR-441 requirements-path-graph-design (viewer-ids-Q4), done in
  `4-batch/3-done/441-requirements-path-graph-design` and merged as `c121375c`. The owner's
  screenshot predates it.
- The share card pictures (`cards.ts`, one per area): unchanged; only the share title text changes.
- The PO gallery's own `shortId` (`test/site/poGallery.ts`), which is for scenario IDs, not
  requirements.
- The URLs of the pages: unchanged (`requirements/<area>/<full ID>/`).
- Splitting from requirements-share-cards: moot, since CR-443 shipped in v1.11.0 (viewer-ids-Q5).

## Evidence

Every check below reads the shipped files at the head under test. The pages are those of
`useCasePage`, `behaviourPage` and `viewerDocument` from the repository. The search tests run the
shipped `test/site/requirementsViewer/viewer.js`, read from the repository, never a copy of its
logic.

Unit tests (Node, run by `just check` and `just ci-static` on Linux and Windows):

1. `pages.test.ts`: extend "a full ID is the text of every link to a requirement", or add a new
   test. On `fullIdReport()`:
   - The use case page's eyebrow is exactly `Use case StRS-MDOKFSTUDIO-GFM-001`, with no title after
     it.
   - Its `title` and `shareTitle` are `Use case StRS-MDOKFSTUDIO-GFM-001: <title>`.
   - Its crumbs are `Areas`, the area title, `StRS-MDOKFSTUDIO-GFM-001`.
   - On the behaviour page, the eyebrow, the titles, both requirement crumbs, the pager
     `aria-label` and the previous and next link texts carry the full IDs.
   - The full `viewerDocument` HTML of each page has
     `<title>Use case StRS-MDOKFSTUDIO-GFM-001: … | Studio requirements</title>`, and the same text
     in og:title and twitter:title.
   - No short ID appears as a text anywhere in the document, head and breadcrumb included. The
     `>(?:GFM|MYST)-\d+<` guard becomes "no short ID that is not part of a full ID", over the whole
     document.
   - The area page is unchanged and still passes.

   This test fails on `origin/main`.
2. `cards.test.ts`: the two share title assertions take the new form. The reason is the owner's
   viewer-ids-Q2, which supersedes share-cards-Q9. "Every share title is distinct" is kept.
3. `search.test.ts`: a use case and a behaviour entry carry `i` equal to the full ID, and an `s`
   that starts with it. Area and File entries have no `i`.
4. A new `test/site/requirementsViewer/searchMatch.test.ts` (or a name the Driver chooses).
   - Setup:
     - It reads `viewer.js` from the repository and runs it in `node:vm`, with a small stub of what
       the script uses: `#history`, `#search`, `#q`, `#results`, `#search-open`, `#search-close`,
       `document.currentScript.src`, `localStorage`, `addEventListener` and `location`, with no
       `svg.metro`.
     - `window.SEARCH` is `searchIndex(model)` of a fixture that holds:
       - StRS and SwRS `…-GFM-014`
       - a `…-MYST-014` behaviour
       - a behaviour `…-GFM-140`
       - a behaviour whose title holds the text `14`
       - a retired ID
       - enough entries that a bare number fills most of the cap.
   - Steps: it types each query into `q` (`q.oninput`) and reads the order of the links in
     `#results`.
   - Assertions:
     - `StRS-MDOKFSTUDIO-GFM-014`, `stRs-mdokfstudio-gfm-014`, `GFM-014` and `gfm-14` each list the
       StRS first and the SwRS right under it, under the usual kind headings. A heading may repeat,
       and there is no other heading.
     - `SwRS-MDOKFSTUDIO-GFM-140`'s text hit never comes before the ID matches of `gfm-14`.
     - `StRS-MDOKFSTUDIO-GFM-14` lists the StRS only as an ID match.
     - The bare number `14` (and `014`) lists every requirement numbered 14, in every area, before
       the behaviour whose title holds `14`, and the `…-140` entry is not an ID match.
     - With more than 30 hits, the ID matches are all kept and the text hits are cut first.
     - Enter (`q.onkeydown({ key: "Enter" })`) sets `location.href` to the first ID match's page:
       the use case for `gfm-14`.
     - The retired ID is absent with History off and present with it on.

   This test fails on `origin/main`: the index has no full ID and there is no leading-zero or
   bare-number match.

Chromium check (in the style of the existing `metroMap.browser.test.ts`):
- On a written use case page and behaviour page of the real report (`writeViewerPages`), at
  1280 px, 800 px and 390 px (phone), the breadcrumb, the eyebrow and the pager stay inside the
  page width, with no horizontal page scroll and no element past the right edge of `main` or the
  header.
- It runs in `test:viewer-graph`, so `just ci-viewer-graph` runs it with Chromium required
  (`STUDIO_REQUIRE_CHROMIUM=1`). It goes either in `metroMap.browser.test.ts` or in a new file added
  to the `test:viewer-graph` script of `package.json`.
- The `viewer-graph` job of `.github/workflows/ci.yml` and the `ci-viewer-graph` justfile target
  are unchanged. Their environment (ubuntu-latest, `just dev-ci visual`, Chromium from Playwright)
  already runs the map checks.
- Without Chromium, the test is skipped with a message, unless `STUDIO_REQUIRE_CHROMIUM=1`, as the
  map checks are. Only the job's CI run proves it on Linux. Locally, `just preflight` runs it except
  on Windows, where its static stage skips the viewer-graph stage.

Scenario steps for the PR (captures per the pull-request guidelines), on pages written from the
real report:

1. Open `requirements/block-editing/StRS-MDOKFSTUDIO-BLOCK-003/`. Check:
   - the eyebrow reads `Use case StRS-MDOKFSTUDIO-BLOCK-003`
   - the tab reads `Use case StRS-MDOKFSTUDIO-BLOCK-003: … | Studio requirements`
   - the breadcrumb reads `Areas / Block editing / StRS-MDOKFSTUDIO-BLOCK-003`
   - the page source has og:title `Use case StRS-MDOKFSTUDIO-BLOCK-003: …`
2. From it, open the page of SwRS-MDOKFSTUDIO-BLOCK-014. Check the eyebrow, the tab, the four
   crumbs and the previous and next links, all in full ID.
3. Press `/` and type `StRS-MDOKFSTUDIO-BLOCK-014`: the use case is first, and Enter opens it.
4. Type `block-14` and `BLOCK-014`: the use case is first and the behaviour right under it.
5. Type `14`: every requirement numbered 14 is listed first.
6. At 390 px wide, the behaviour page's breadcrumb, eyebrow and pager wrap and stay inside the
   page.

Gates:
- `just check`
- `just requirements-lint`
- `just requirements-update`, leaving no diff
- `okfreq validate --check-links --project-root .`
- `just ci-viewer-graph` where Chromium starts
- then `just preflight` (constitution, section 4); on Windows only its static stage runs, and CI
  runs the others.
