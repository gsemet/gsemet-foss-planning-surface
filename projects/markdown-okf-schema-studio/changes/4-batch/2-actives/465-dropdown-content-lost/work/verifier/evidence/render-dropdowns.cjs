// usage: node --import <patches> render.cjs <root> <outdir>
const path = require("node:path");
const fs = require("node:fs");
const root = process.argv[2];
const outDir = process.argv[3];
const { renderMyst } = require(path.join(root, "out/src/core/render/mystRenderer.js"));
const { PREVIEW_THEME_CSS, PREVIEW_ACCESSIBILITY_CSS } = require(path.join(root, "out/src/core/preview/previewStyles.js"));
const { THEMES } = require(path.join(root, "out/test/visual/themes.js"));
const source = [
  "# Release notes", "", "Intro paragraph before the dropdowns.", "",
  ":::{dropdown} Closed colon dropdown", "Body of the closed dropdown.", "", "Second body paragraph.", ":::", "",
  "````{dropdown} Open backtick dropdown", ":open:", "", "Body of the open dropdown.", "````", "",
  ":::{dropdown}", "Untitled body.", ":::", "", "Closing paragraph.", "",
].join("\n");
(async () => {
  const { html } = await renderMyst(source, { sourcePath: path.join(root, "docs/guide.md") });
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, "source.md"), source);
  fs.writeFileSync(path.join(outDir, "fragment.html"), html);
  for (const theme of THEMES.filter((t) => ["light", "dark"].includes(t.id))) {
    const vars = Object.entries(theme.variables).map(([k, v]) => `  ${k}: ${v};`).join("\n");
    const page = `<!doctype html><html lang="en"><head><meta charset="utf-8"><style>${PREVIEW_THEME_CSS}${PREVIEW_ACCESSIBILITY_CSS}\nbody {\n${vars}\n}</style></head><body>${html}</body></html>`;
    fs.writeFileSync(path.join(outDir, `page-${theme.id}.html`), page);
  }
})();
