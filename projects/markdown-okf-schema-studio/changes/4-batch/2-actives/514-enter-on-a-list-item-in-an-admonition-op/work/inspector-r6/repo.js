// Renders every tracked Markdown file with two builds; reports HTML differences outside line attributes
// and line-attribute differences outside boxes.
const path = require("node:path");
const fs = require("node:fs");
const { execFileSync } = require("node:child_process");
const [root, base] = process.argv.slice(2);
const a = require(path.join(root, "out/src/core/render/mystRenderer.js"));
const b = require(path.join(base, "out/src/core/render/mystRenderer.js"));
const { parseFragment, serialize } = require(path.join(root, "node_modules/parse5"));
const files = execFileSync("git", ["-C", root, "ls-files", "*.md"], { encoding: "utf8" }).split("\n").filter(Boolean);
const BOX = /(^| )(admonition|markdown-alert)( |$)/u;
const outside = (html) => { const rows = []; const walk = (n, inBox) => { const attrs = n.attrs ?? []; const cls = attrs.find((x) => x.name === "class")?.value ?? ""; const box = inBox || BOX.test(cls); if (!box && n.tagName) rows.push(`${n.tagName} ${attrs.filter((x) => x.name.startsWith("data-")).map((x) => `${x.name}=${x.value}`).join(" ")}`); (n.childNodes ?? []).forEach((c) => walk(c, box)); }; walk(parseFragment(html), false); return rows.join("\n"); };
const strip = (html) => html.replace(/ data-(end-)?line="\d+"/gu, "");
(async () => {
  let h = 0, o = 0, e = 0, n = 0;
  for (const f of files) {
    const s = fs.readFileSync(path.join(root, f), "utf8");
    let x, y;
    try { x = (await a.renderMyst(s)).html; y = (await b.renderMyst(s)).html; } catch (err) { e++; console.log("ERR", f, err.message); continue; }
    n++;
    if (strip(x) !== strip(y)) { h++; console.log("HTML", f); }
    if (outside(x) !== outside(y)) { o++; console.log("OUTSIDE", f); }
  }
  console.log(`${n} files, html diffs ${h}, outside-box attribute diffs ${o}, errors ${e}`);
})();
