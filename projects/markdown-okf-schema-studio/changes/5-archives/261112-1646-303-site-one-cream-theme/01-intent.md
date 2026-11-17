# Intent: one cream look for the whole published site

## Request

The GitHub Pages site has two looks. The owner wants one: the requirements viewer's cream theme,
everywhere.

## Today

- Main pages (home, Contributing, How we ship, Gallery, Reports): `test/site/buildSite.ts`
  (`pageDocument` inline style) and `test/site/siteTheme.ts`. Teal palette on a light paper,
  sans-serif everywhere, header with the 44 px logo and five links (Home, Contributing, How we
  ship, Gallery, Requirements), dark palette from `prefers-color-scheme` only, no switch.
- Requirements viewer (CR-302 requirements-viewer, PR #373): `test/site/requirementsViewer/viewer.css`,
  `viewer.js`, `shell.ts`. Cream and sepia palette (`data-theme=cream|dark`), serif text, sans labels,
  sticky header with a dot instead of the logo, a breadcrumb, four site links (no Requirements),
  a Theme button kept in `localStorage` (`req-theme`), first choice from the system; the button is
  hidden without JavaScript.
- Shared today: only `test/site/siteHead.ts` (head tags, favicon, social card).

## Analysis

- Likely one shared stylesheet or token set (palette, fonts, header) used by both generators,
  with the cream palette and its dark variant as the reference.
- Touches the gallery capture viewer colours hard-coded in `buildSite.ts` and `siteTheme.ts`,
  the visual site tests, and possibly the social card colours (`socialCard.ts`).
- Open questions for the grill are in `02-answers.md` once asked.
