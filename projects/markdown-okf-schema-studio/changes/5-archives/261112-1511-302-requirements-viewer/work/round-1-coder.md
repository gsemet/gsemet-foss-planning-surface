# CR-302 requirements viewer, round 1, Coder notes

Nothing is committed. Worktree: `markdown-okf-schema-studio.worktrees/batch-01-CR-302`.

## What changed

Generator, in `test/site/requirementsViewer/`: `model.ts` (report model, lifecycle read from
`req_lifecycle` with fallback to `lifecycle`), `mainPaths.ts` (parser), `urls.ts`, `layout.ts` (port of
`gen.py` graph, metro SVG, phone list, walk count), `shell.ts` (page frame, theme, History checkbox,
search sheet), `pages.ts` (area, use case, behaviour), `home.ts`, `searchIndex.ts`, `cards.ts` (four
level cards through `cardDocument` and `writeCardPictures`), `write.ts` (`writeViewerPages` sync,
`writeRequirementsViewer` async, `redirectDocument`), `viewer.css`, `viewer.js`, `fixture.ts` (test data).
Also `test/site/siteHead.ts` (shared head tags) and `relativeFolderLink` in `siteLinks.ts`.
- Output: `requirements/index.html`, `requirements/<area>/`, `requirements/<area>/<id>/`,
  `search-index.js`, `viewer.css`, `viewer.js`, `og/{areas,area,use-case,behaviour}.png`. All links relative.
  Retired requirements have no page; they are rows hidden by CSS and shown by the History checkbox.
- `requirements.html` is now a redirect (meta refresh, link, canonical). The site nav links `requirements/`.
- Removed `test/site/requirementsPage.ts` and its test; the marker companion became
  `src/core/render/requirementsViewer.markers.ts`.
- Links updated in README.md, docs/how-we-ship.md, CONTRIBUTING.md.
- Requirements: CORE-069 amended; new CORE-080..085 (proposed, derive from TRUST-014, scope rendering-core);
  markers in the companion and `@tests_req` in each test; `just requirements-update` run; log entry
  `### The site requirements viewer replaces the Requirements page (CR 302)` under 2026-11-12.
  `### Main paths` format needs no change (CR-301 documentation is enough).
- Tests (23, 5 files + write): mainPaths, model, pages, home, search, cards, write under `test/site/requirementsViewer/`.
  The old nav assertion (`requirements.html`) changed to `requirements/` because the page moved into a folder.

## Gates

- `just check`: pass (exit 0, 3870 unit tests; run before the last CSS tweak).
  One earlier run failed once on `diagReq.settings.requirements.test` ("releaseCellEditorOnOutsideChange is
  not a function", stack naming a `worktrees/277` path); it passed alone and in two later full runs: flaky, unrelated.
- `just requirements-report && npm run compile && npm run site`: pass. 572 pages checked, 11232 relative links,
  only miss is the existing `index.html -> LICENSE`. Four og PNGs written. 375px and 1280px: no horizontal scroll
  (fixed one overflow of the home area table header on mobile). Search, History and redirect checked in Chromium.
- Not run: `just preflight`, e2e.

## Open points

- Active counts are 80 StRS / 473 SwRS (467 + 6 new), not the spec's 79/433.
- `Known issue (CR 152):` style lines are not counted (strict `- Known issue:` regex, as before).
- `docs/how-we-ship.md` links `../requirements/`: on GitHub that opens the requirements folder, on the site the viewer.
- If Chromium cannot start, `npm run site` stops after writing the pages, with the existing socialCard message.

## Hand-over

Review the rendered pages under `out/site/requirements/`; run `just site` for a full build. Dark theme and the
Play animation were not checked visually.
