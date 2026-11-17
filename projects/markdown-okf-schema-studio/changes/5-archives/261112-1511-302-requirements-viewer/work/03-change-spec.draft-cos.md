---
title: Change spec (draft) - a requirements viewer on the published site
cr: none yet (backlog P4; take the next free number when it is opened)
date: 2026-11-12
issue: none
priority: P4
status: draft, not grilled for implementation
---

# Change spec (draft): a requirements viewer on the published site

> [!NOTE]
> Draft written from the owner's decisions of 2026-11-12 (`02-answers.md`). Open the CR, then
> grill the "Open questions" below before any code. Reference design: `prototype-02/`.

## Target behaviour

1. `just` builds a static viewer from the okfreq report JSON (`okfreq generate-report`), the area
   titles and descriptions of `test/shared/e2eGroups.ts`, and the `### Main paths` sections of
   the StRS files; the Pages workflow publishes it next to the gallery.
2. One HTML page per view, each with its own URL: `requirements/` (areas),
   `requirements/<area>/` (use cases), `requirements/<area>/<StRS-id>/` (metro map),
   `requirements/<area>/<SwRS-id>/` (behaviour). Lists render without JavaScript; JavaScript adds
   search, the Play animation and the pick panel.
3. Design: `prototype-02/` (owner's choice of 2026-11-12: plain and professional, one sentence of
   explanation per section at most, no hype), on the palette of
   `prototypes/journey/00-design-system.html`.
4. Metro map only on the use case page; horizontal SVG on wide screens, vertical HTML line on
   phones. Without a `### Main paths` section the page says so and lists the behaviours.
5. File links point to GitHub at the published commit; each test file is tagged unit, integration,
   visual, sphinx or build from its folder.
6. `### Main paths` format: `main-paths/FORMAT.md`, documented in
   `requirements/guidelines/project.guidelines.md`. Owner's decision of 2026-11-12: write the Main
   paths of every StRS where it is possible, not one area. An agent drafts them from each StRS and
   its SwRS (states, the SwRS that moves between them, the SwRS of other outcomes), and keeps only
   steps backed by an existing SwRS. A StRS whose SwRS do not form a path gets no section and is
   listed in the change's report. Sample: `main-paths/StRS-MDOKFSTUDIO-DIAG-001.md`.
   Owner's decision of 2026-11-12: two changes. The Main paths are written first, by their own
   change (`P1/strs-main-paths`); this change reads them.
7. Every page has its social card (owner's decisions of 2026-11-12): Open Graph and Twitter meta
   tags (`og:title`, `og:description`, `og:url`, `og:image` with its size and alt text,
   `twitter:card` = `summary_large_image`). The title and description are the page's own; the
   image is shared by every page of a level: four 1200 x 630 PNG under `og/` (`areas`, `area`,
   `use-case`, `behaviour`), absolute https URLs. Each image names the level in one line and shows
   the chain use case -> behaviour -> code and tests with that level marked. The build draws them
   from HTML templates and shoots them with Playwright. Prototype: `prototype-02/shoot.mjs`. Later, not in the first change:
   one image per StRS showing its metro map (owner, 2026-11-12).

## Open questions for the grill


- Does okfreq validate the SwRS ids of a Main paths section (lint), or the viewer build only?
- Place in the site navigation (next to the gallery, or a top-level entry).
- Static generator language: Python (as the gallery scripts) or TypeScript.

## Acceptance checks (draft)

- The four views and search work on a 1440 px screen and on a 375 px phone, in the three themes.
- Each view loads without JavaScript and shows its list.
- Every SwRS and StRS of the report has a page; every file link resolves at the published commit.
- Every page carries the card meta tags with its own title; its `og:image` is the PNG of its level,
  which resolves on the published site at 1200 x 630.
- Lighthouse accessibility 95 or more on the four views; `prefers-reduced-motion` honoured.
