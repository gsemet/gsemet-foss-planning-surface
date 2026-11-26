// Differential: the mapped elements outside any box must be the same on base and head.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <headRoot> <baseRoot> <dir>...
const fs = require("node:fs");
const path = require("node:path");

const [headRoot, baseRoot, ...dirs] = process.argv.slice(2);
const parse5 = require(path.join(headRoot, "node_modules/parse5"));

const load = (root) => require(path.join(root, "out/src/core/render/mystRenderer.js")).renderMyst;
const head = load(headRoot);
const base = load(baseRoot);

function* markdownFiles(dir) {
  const stat = fs.statSync(dir);
  if (stat.isFile()) { yield dir; return; }
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (["node_modules", "out", ".git", ".venv", "dist"].includes(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* markdownFiles(full);
    else if (/\.md$/u.test(entry.name)) yield full;
  }
}

const attr = (node, name) => node.attrs?.find((a) => a.name === name)?.value;
function isBox(node) {
  const cls = (attr(node, "class") ?? "").split(/\s+/u);
  if (attr(node, "data-okf-github-alert") !== undefined) return true;
  if (cls.includes("admonition") && !cls.includes("myst-context-admonition")) return true;
  if (node.tagName === "details") return true;
  return cls.some((name) => name.startsWith("callout-"));
}

function mapped(html) {
  const out = [];
  const inside = [];
  const walk = (node, boxed) => {
    for (const child of node.childNodes ?? []) {
      if (!child.tagName) continue;
      const line = attr(child, "data-line");
      if (line !== undefined) {
        const entry = `${child.tagName} ${line}-${attr(child, "data-end-line") ?? line}${attr(child, "data-single-line") !== undefined ? " single" : ""}`;
        (boxed ? inside : out).push(entry);
      }
      walk(child, boxed || isBox(child));
    }
  };
  walk(parse5.parseFragment(html), false);
  return { out, inside };
}

const stripLines = (html) => html.replace(/ data-(line|end-line|single-line|okf-marker-line|okf-marker-end-line)="[^"]*"/gu, "")
  .replace(/id="[^"]*mermaid[^"]*"/gu, "");

(async () => {
  let files = 0, outsideDiffs = 0, insideDiffs = 0, htmlDiffs = 0, errors = 0;
  for (const dir of dirs) {
    for (const file of markdownFiles(dir)) {
      files += 1;
      const source = fs.readFileSync(file, "utf8");
      let a, b;
      try { a = (await base(source)).html; b = (await head(source)).html; }
      catch (error) { errors += 1; console.log(`ERROR ${file}: ${error.message}`); continue; }
      const ma = mapped(a), mb = mapped(b);
      if (JSON.stringify(ma.out) !== JSON.stringify(mb.out)) {
        outsideDiffs += 1;
        console.log(`OUTSIDE ${file}`);
        const sa = new Set(ma.out), sb = new Set(mb.out);
        console.log("  base only:", ma.out.filter((e) => !sb.has(e)).join(" | "));
        console.log("  head only:", mb.out.filter((e) => !sa.has(e)).join(" | "));
      }
      if (JSON.stringify(ma.inside) !== JSON.stringify(mb.inside)) insideDiffs += 1;
      if (stripLines(a) !== stripLines(b)) { htmlDiffs += 1; console.log(`HTML-OTHER-THAN-LINES ${file}`); }
    }
  }
  console.log(`files=${files} errors=${errors} outsideBoxMappingDiffs=${outsideDiffs} insideBoxMappingDiffs=${insideDiffs} htmlDiffsBesidesLineAttributes=${htmlDiffs}`);
})();
