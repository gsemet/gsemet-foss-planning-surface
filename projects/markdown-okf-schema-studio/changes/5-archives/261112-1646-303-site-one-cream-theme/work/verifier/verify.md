# Verify CR-303 at 246e600d

Verdict: VERIFIED

Build: `just requirements-report` then `npm run site` (`just site-assemble` still fails in gallery curation on local reports; fallback as allowed). Served `out/site` on localhost:8302, Chromium 1248 headless.

1. Previous failure 1, breadcrumb clipped at 1280: fixed. nav.crumbs scrollWidth == clientWidth and the last crumb ends left of the site nav (CORE-069: 446 < 609; TRUST-014: 377; LIFE-169: 438) at 1280, 1100, 900 and 375. Full text "Areas/Rendering core/TRUST-014/CORE-069". Evidence: after-1280-req-usecase.png, after-1280-req-behaviour.png.
2. Previous failure 2, horizontal scroll at 375: fixed. scrollWidth == innerWidth on home, contributing, how-we-ship, gallery, reports, req-home, req-area, req-usecase, req-behaviour at 375 and at 1280.
3. Item 3 grep in out/site: outside reports/visual/pages only the three accepted hits (requirements/theme-zoom/SwRS-MDOKFSTUDIO-THEME-001, docs/user/editing.html, reports/requirements/requirements-report.json); reports/visual/pages are extension preview captures.
4. Item 4: page screenshots at 1280 and 375 (gallery with capture open, History on) and 8 social pictures regenerated; before shots kept; see before-after.md.
5. Item 5: five header links from home give the same header (logo, five links in order), body and header rgb(245,241,232), crumbs only on requirements, no theme button. History on LIFE-169: retired rows 0/2 -> 2/2. `/` opens Search. System dark: home, contributing, gallery, reports, req home, behaviour stay cream. JS disabled: cream, #search-open display none, no .play, History 0/2 -> 2/2.
6. Contrast: tokens unchanged since the previous run (all >= 4.5 there).
7. Not run: items 1, 2, 6 (Driver gates).
