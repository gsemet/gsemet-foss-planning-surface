# Grill answers: t3-project-icon (short name `t3`)

Grilled with the user on 2026-11-18.

- **Fact found by the Chief of Staff:** step 1 of the request finds nothing (no favicon, `app/icon.*`,
  `assets/icon.*`, `assets/logo.*` or `.idea/icon.svg`; no `index.html` with an icon), and step 2
  finds no logo either: the tracked images are diagrams and screenshots only. No `t3.json` exists.
- **t3-Q1, no logo in the repository:** A. The Coder draws a simple square SVG logo on the theme of
  a building site (chantier), at `docs/logo.svg`, and `t3.json` points to it.
- **t3-Q2, "Ne commite pas":** A. The change goes through the batch as a normal PR that the user
  merges; the final `t3.json` is shown in the PR's description.

## Settled by the Chief of Staff

- `t3.json` at the repository's root holds `$schema` and `iconPath` only. The scripts T3 could run,
  from the `justfile` (for example `just check`, `just test`, `just scenario`), are proposed in the
  PR's description and not added, as the request asks.
- The logo is a plain SVG, legible at 16 px, with no text, no external font and no raster image.
