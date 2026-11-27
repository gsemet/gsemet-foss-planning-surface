// Lists the root-element attributes that appear in a style rule which hides content (preview CSS).
const path = require("node:path");
const root = process.argv[2];
const styles = require(path.join(root, "out/src/core/preview/previewStyles.js"));
const css = Object.values(styles).filter((v) => typeof v === "string").join("\n").replace(/\/\*[\s\S]*?\*\//g, "");
const found = new Map();
for (const m of css.matchAll(/([^{}]+)\{([^{}]*)\}/g)) {
  const [, selector, body] = m;
  if (!/display\s*:\s*none|visibility\s*:\s*hidden|user-select\s*:\s*none|content-visibility/.test(body)) continue;
  for (const part of selector.split(",")) {
    if (!/#sphinx-myst-preview-content|main/.test(part)) continue;
    const head = part.trim().split(/\s+/)[0];
    if (/^(html|body|:root)/.test(head)) found.set(head, (found.get(head) || 0) + 1);
  }
}
console.log(Object.keys(styles).join(","));
console.log([...found].map(([k, v]) => v + "  " + k).join("\n"));
