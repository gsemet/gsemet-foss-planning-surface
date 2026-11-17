# Decisions (user, 2026-10-25)

- Wait for okf-schema to ship the complete JSON export and the one-page viewer (okf-schema
  backlog graph-viewer, amendment of 2026-10-25), then integrate it in the site. Do not build a
  project-specific browser in the meantime.

# Decisions (owner, 2026-11-12) — supersede the 2026-10-25 wait

- Build a requirements viewer specific to Studio, for the GitHub Pages site (no longer wait for the okf-schema viewer). Data: the okfreq report JSON.
- "Layer by layer" = the traceability chain: StRS (user need) → SwRS (behaviour) → source files → tests.
- Superseded and deprecated requirements hidden by default; a toggle shows them with their "superseded by" links.
- Must be beautiful and striking. First step: three HTML prototypes, each in its own visual direction; the owner picks one.

# Owner's idea (2026-11-12): show how a use case is cut into testable behaviours

- A StRS tells a full use case: "I do A, then B, then C, and I get D". Validating it whole is a combinatorial problem; there is no StRS validation test today.
- Each step is cut into several SwRS: in state A, these are the options; one of them leads to B; in B, one option leads to C, and so on. SwRS are tested one by one.
- The viewer should show the StRS as one or two main paths through a map of states, the SwRS as the transitions (the options at each state), and how few paths the StRS covers compared with every walk the SwRS make possible.
- Prototype `prototypes/explorations/d-usecase-metro.html` (hand-written mapping on StRS DIAG-001 with the real SwRS, scenarios and test counts).
- Data gap: a StRS file holds no ordered steps, and `derives_from` says which StRS a SwRS serves, not at which step. The map needs the steps written down (see the closing proposal in the session of 2026-11-12).

# Owner's feedback on the prototypes (2026-11-12)

- Keeps the metro view, for the StRS page only. Rejects the constellation (flashy, unusable).
- Must look good on a wide screen and on a phone.
- Navigation in several views, each with limited detail: scopes (with their description) → StRS of a scope → StRS as a metro map, click a SwRS → SwRS with its sources and tests. Search everywhere.
- Scope titles and descriptions exist in `test/shared/e2eGroups.ts` (title, scope).

# Decision (owner, 2026-11-12): steps of a use case

- The steps of a use case are written in a `### Main paths` section of each StRS ("main_paths dans un premier temps suffira"). No okfreq schema change for now. Format: `main-paths/FORMAT.md`.
- Prototype of the 4 views: `prototypes/explorations/e-journey.html` (built by `prototypes/journey/build_journey.py` from the okfreq report, `test/shared/e2eGroups.ts` and `main-paths/*.md`). Metro only on the StRS page; the other pages are a line index, a vertical line of stations and a behaviour sheet. Wide screens draw the metro as SVG; phones as a vertical line in HTML.

# Owner (2026-11-12): a series of step prototypes, kept in a CR-shaped folder

- "Une série de prototypes qui capture chaque étape", professional, a little striking, no flashy effects or AI slop. Done in `prototypes/journey/` (steps 0 to 5); this folder is the CR-shaped home for a later change.

## 2026-11-12: prototype 02

- Owner: the journey prototype is good and the theme is liked, but there is too much text and slop.
  Make it simpler and more professional, explain directly what the reader sees. The pages will be
  used to show people outside the project why requirements are written this way: teach, without
  hype.
- Done: `prototype-02/`, static pages for one vertical slice of real data (area Diagrams, use case
  DIAG-001, its 14 behaviours).
- Owner: every page must have its social card (a picture shown when a link is shared on X); the
  gallery page too, one card for the page, not one per capture. Viewer: written into the spec
  (target behaviour 7) and done in `prototype-02/`. Gallery: separate backlog item
  `P3/gallery-page-social-card`.
- Owner, same day, made precise: one card picture per level, not per page; the text (title,
  description) may differ per page. Done: four level pictures, page-specific meta text.
- Owner, same day: an image per StRS (its metro map) would be nice later, but the first version
  keeps one image per level (4 in all), the StRS level included. Per-StRS images (80 today, with
  the metro map once a StRS has its Main paths) stay an idea for a later change.
- Owner, same day: generate the Main paths intelligently wherever possible, ideally on every StRS
  (not only one area).
- Owner, same day: two changes. `P4/strs-main-paths` writes the Main paths of the StRS first;
  this change (the viewer) reads them.
- Owner, same day: priorities raised. `P1/gallery-page-social-card` and `P1/strs-main-paths`,
  then this viewer in P2 (earlier entries name the old folders P3 and P4).
- Grill before the batch (owner's choices):
  - Generator in TypeScript, next to `test/site/buildSite.ts`, sharing its head and social card code.
  - Navigation, owner's words: "Replace by your viewer, just ensure the root page display the same
    information, stats etc". The menu's Requirements link opens the viewer; its home page shows
    the information and statistics of the okfreq report it replaces.
  - Main paths check: a project script (decided in `P1/strs-main-paths`).
  - Same batch, after `strs-main-paths` and `gallery-page-social-card`.
- Owner, 2026-11-12: "Oui tu peux tout lancer" (go for the specifications and the batch).
- Spec questions, owner's choices on 2026-11-12:
  - URLs: nested folders, `requirements/<area>/<id>/` ("Nested folders"), not the flat files of
    prototype-02.
  - Header: the viewer's own bar with the site links in it ("Own bar + site links").
  - Retired requirements: rows only, behind the History toggle, linking to GitHub and to their
    replacements; no page each ("Rows only").
  - The lifecycle bug of `test/site/requirementsPage.ts` (reads `lifecycle`, files carry
    `req_lifecycle`): fixed by the viewer; the published active counts drop to the true figures
    ("Yes, fix it").
  - `requirements.html` becomes a redirect to the viewer home ("Yes, redirect").
  - Home page: same information and statistics as today's page, shortened to the viewer's
    one-sentence style ("Shortened").
- Owner, 2026-11-12: "No more question. Finish the work autonomously" (go for the batch).
