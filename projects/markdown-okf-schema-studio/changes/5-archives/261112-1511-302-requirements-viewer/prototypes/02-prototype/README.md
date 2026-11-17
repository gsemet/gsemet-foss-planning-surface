# Prototype 02: one vertical slice, real data

Second version of the viewer prototypes, after the owner's review of the journey series
(2026-11-12): keep the theme, cut the text, explain plainly what the reader sees, no hype. The
pages are meant to show people outside the project why requirements are written this way.

## What it shows

One vertical slice of the real Studio requirements (okfreq report at commit 0e79699d):

| Page | File | Content |
| --- | --- | --- |
| Areas | `site/index.html` | the three layers (use case, behaviour, code and tests) and the 16 areas; only Diagrams opens |
| Area | `site/area-diagrams.html` | the use cases of Diagrams; only DIAG-001 opens |
| Use case | `site/use-case-diag-001.html` | the metro map of DIAG-001 (two main paths), a list version on phones, the count of walks against the count of tested behaviours |
| Behaviour | `site/behaviour-*.html` (14 pages) | the rule, where it sits on the path, scenarios (Given/When/Then), implementing files, tests |

Every page has a social card: Open Graph and Twitter meta tags in its `<head>` with its own
title and description, and the picture of its level, one of four 1200 x 630 PNG in `site/og/`
(`areas`, `area`, `use-case`, `behaviour`) drawn from `site/cards/<level>.html` and shot by
`shoot.mjs` (Playwright). The image URLs use the planned Pages address
`https://gsemet.github.io/markdown-okf-schema-studio/requirements/`.

Search (`/`) covers the slice. Theme switch (cream, dark). Pages read without JavaScript.

## Differences from the journey series

- Static multi-page HTML, one file per page: the shape the GitHub Pages export would have.
- One explanatory sentence per section at most; no taglines, no animated numbers.
- Real data only for one slice instead of a full single-page app with 1.6 MB of inlined data.

## Rebuild

```bash
python3 gen.py journey-data.js site && cp style.css app.js site/
node shoot.mjs site <repository>/node_modules   # needs playwright-core and Playwright Chromium (just dev)
```

`journey-data.js` comes from `../prototypes/journey/build_journey.py` (see the folder README).
Serve `site/` with `python3 -m http.server` and open `index.html`.
