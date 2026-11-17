# 060 — requirements page on the published site

From backlog `P3/requirements-report-site` (first slice). User request (2026-10-25): publish on the
GitHub Pages site a page with the diagram that explains how the requirements work and the stats
from the okfreq JSON report, like the "Deliverable showcase" of PR #62.

## Decisions

1. Scope: one page "Requirements" in the published site (built by `npm run site`,
   `test/site/buildSite.ts`, deployed by `.github/workflows/pages.yml`).
   - How it works: the chain StRS (use case) → SwRS (one behaviour with its scenarios,
     cross-cutting rules cited) → `@implements_req` in the code → `@tests_req` in a test, as a
     diagram (inline SVG or Mermaid rendered at build time; no runtime CDN), with one real SwRS
     shown as an example.
   - Stats read at build time from `okfreq generate-report` JSON (`just requirements-report`,
     `out/reports/requirements/requirements-report.json`): counts per scope (StRS, SwRS),
     implementation and test marker coverage, lifecycle counts, exemptions, Known issue count.
     Read active requirements only; superseded/archived counted separately.
   - Linked from the site navigation; light and dark themes like the rest of the site.
2. Out of scope (stays in backlog `P3/requirements-report-site`): the requirement browser
   (StRS → SwRS navigation, per-requirement pages, search) — needs a grilling session.
3. Branch stacked on PR #62 (`changes-requests/059-requirements-batch3`) so the page shows the
   real baseline; the PR targets main and is rebased once #62 lands.
4. The site build must not fail when the report is missing: the page then says the report was not
   generated. The site job generates the report first.
5. Tests: unit test of the stats extraction from a fixture JSON; the site build test covers the
   page; one visual check of the page in light and dark if the site has visual tests.
6. PR describes the deliverable (Deliverable showcase with a screenshot of the page).
7. README: add a link to the published requirements page (GitHub Pages URL, next to the existing site/gallery links) in the same PR (user, 2026-10-25).
7. (user, later) Link the published requirements page from README.md, next to the existing site/gallery links. Use the GitHub Pages URL derived from existing README links; Pages deploys only on a release tag, so state in the PR that the link goes live with the next release.
8. Page purpose and structure (user, 2026-10-25), written for a reader outside the project:
   1. What: what the requirements are (StRS = user use cases, SwRS = observable behaviour with
      scenarios) and what this project specifies.
   2. Why: keep the documented behaviour equal to the code, make bugs visible as Known issues,
      know which test checks which behaviour, review changes against a contract.
   3. How it works: the chain diagram, then the marking in the code with real examples: a
      `@implements_req <SwRS-ID>` comment in a source file and the `@tests_req <SwRS-ID>` comment
      in the test that checks it (snippets taken from the repository for the example SwRS, with
      their file paths), and the gates that keep it in sync (okfreq validate / update-coverage
      in CI).
   4. Stats from the okfreq report.
   5. A "Browse the requirements" section stating that per-requirement navigation comes later.
