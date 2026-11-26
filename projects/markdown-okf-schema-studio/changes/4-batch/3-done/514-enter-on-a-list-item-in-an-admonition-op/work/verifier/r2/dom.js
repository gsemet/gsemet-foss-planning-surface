// Prints the mapped DOM of one Markdown file, and what a click and Enter open on each mapped
// element. Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot> <file.md>...
const fs = require("node:fs");
const path = require("node:path");
const [root, ...files] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
(async () => {
  for (const file of files) {
    const source = fs.readFileSync(file, "utf8");
    console.log(`=== ${path.basename(file)}`);
    source.split("\n").forEach((l, i) => console.log(`${String(i + 1).padStart(3)}| ${l}`));
    const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
    const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
    const walk = (e, depth) => {
      const line = e.getAttribute("data-sphinx-source-line");
      const cls = e.getAttribute("class") ?? "";
      let info = "";
      if (line !== null) {
        const r = (exact) => { const x = blocks.editingElementFor(e, { exact }); const g = x.sourceRange ?? blocks.blockRange(x.element); return `<${x.element.tagName.toLowerCase()}> ${g.line}-${g.endLine}`; };
        info = ` [${line}-${e.getAttribute("data-sphinx-source-end-line") ?? line}] click=${r(false)} enter=${r(true)}`;
      }
      const alert = e.getAttribute("data-okf-github-alert") !== null ? " alert" : "";
      const text = e.children.length === 0 ? ` ${JSON.stringify(e.textContent.trim().slice(0, 30))}` : "";
      console.log(`${"  ".repeat(depth)}${e.tagName.toLowerCase()}${cls ? "." + cls.replace(/\s+/g, ".") : ""}${alert}${info}${text}`);
      for (const c of e.children) walk(c, depth + 1);
    };
    for (const c of page.document.querySelectorAll("body")[0]?.children ?? page.document.children ?? []) walk(c, 0);
  }
})();
