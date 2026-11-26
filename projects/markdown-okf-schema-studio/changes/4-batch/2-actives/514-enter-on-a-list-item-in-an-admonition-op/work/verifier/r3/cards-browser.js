// Writes one styled preview page per card shape, for cards-browser.py to check in Chromium that the
// body words after a `---` line are on screen.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot> <outDir>
const fs = require("node:fs");
const path = require("node:path");
const [root, out] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMyst } = o("src/core/render/mystRenderer.js");
const styles = o("src/core/preview/previewStyles.js");
const SHAPES = {
  "note-card": "::::{note}\n:::{card}\nAlpha\n\n---\n\nBeta\n:::\n::::\n",
  "note-card-twice": "::::{note}\n:::{card}\nAlpha\n\n---\n\nBeta\n\n---\n\nGamma\n:::\n::::\n",
  "dropdown-card": "::::{dropdown} D\n:open:\n\n:::{card}\nAlpha\n\n---\n\nBeta\n:::\n::::\n",
  "alert-card": "> [!NOTE]\n> :::{card} Title\n> Alpha\n> ---\n> Beta\n> :::\n",
  "note-grid-card": "::::::{note}\n::::{grid}\n:::{grid-item-card}\nAlpha\n\n---\n\nBeta\n:::\n::::\n::::::\n",
  "note-card-start-tight": "::::{note}\n:::{card}\n---\nAlpha\n\nBeta\n:::\n::::\n",
};
(async () => {
  fs.mkdirSync(out, { recursive: true });
  console.log(`style exports: ${Object.keys(styles).filter((k) => typeof styles[k] === "string").join(",")}`);
  for (const [name, source] of Object.entries(SHAPES)) {
    const { html } = await renderMyst(source, { sourcePath: "/w/a.md" });
    const css = `${styles.PREVIEW_THEME_CSS}\n${styles.PREVIEW_ACCESSIBILITY_CSS}`;
    fs.writeFileSync(path.join(out, `${name}.html`), `<!doctype html><meta charset="utf-8"><style>${css}</style><body><main id="sphinx-myst-preview-content">${html}</main></body>`);
    console.log(`${name} ${JSON.stringify(source)} main=${html.includes("sphinx-myst-preview-content")} cardCss=${css.includes(".myst-grid-card-body")} htmlLength=${html.length}`);
  }
})();
