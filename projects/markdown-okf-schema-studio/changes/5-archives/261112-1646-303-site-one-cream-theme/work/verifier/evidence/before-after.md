# Before / after (light only)

Before: detached worktree of origin/main (6b803967), `npm run site` with the same out/reports copied in.
After: pushed head 246e600d, `just requirements-report` then `npm run site` (`just site-assemble` fails in gallery curation: "final review report is not passed", local reports).
Reproduce: serve both `out/site` folders with `python3 -m http.server`, then headless Chromium at 1280x800 and 375x812, colorScheme light.

Pairs: `before-<w>-<page>.png` / `after-<w>-<page>.png` for w in 1280, 375 and page in home, contributing, how-we-ship,
gallery (first capture opened), reports, req-home, req-area, req-usecase, req-behaviour (History checked, CORE-069).
Social: `before-social-*.png` / `after-social-*.png` for og-home, og-contributing, og-how-we-ship, og-gallery, requirements-og-areas, -area, -use-case, -behaviour (1200x630).
Round 2 re-run at 246e600d: all after-* files regenerated (before-* kept). History-on shots use SwRS-MDOKFSTUDIO-LIFE-169 (has retired rows; CORE-069 has none).
Extra after-only: `after-1280-darksystem-*.png` (system dark: stays cream), `after-1280-nojs-req-history-on.png` (JS disabled, History on),
`after-1280-req-history-on.png`, `after-1280-req-search-open.png` (`/` opens Search).
Note: the before requirements pages use the same requirements report as the after (generated at head), so CORE-086 content may appear in both.
