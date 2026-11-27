// CR-514 inspector round 6. For each case: what click and Enter open on every element of the page, and
// the document after that editor is erased and committed. Usage (from the worktree):
// node --import ./scripts/register-myst-patches.mjs <this> <buildRoot> <cases.js> [name filter]
const path = require("node:path");
const [root, casesFile, filter] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");
const CASES = require(path.resolve(casesFile));
(async () => {
  for (const [name, source, erase] of CASES) {
    if (filter && !name.includes(filter)) continue;
    console.log(`\n=== ${name} ${JSON.stringify(source)}`);
    try {
      const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
      const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
      const lines = source.split("\n");
      const seen = new Set();
      const visit = (e, depth) => {
        const hit = e.closest(MAPPINGS_SELECTOR);
        let out = `${"  ".repeat(depth)}${e.tagName}${e.getAttribute("class") ? "." + e.getAttribute("class").split(" ")[0] : ""}`;
        if (hit) {
          for (const exact of [false, true]) {
            const x = blocks.editingElementFor(hit, { exact });
            const r = x.sourceRange ?? blocks.blockRange(x.element);
            if (!r) { out += " (none)"; continue; }
            out += ` ${exact ? "E" : "C"}${r.line}-${r.endLine}`;
            seen.add(`${r.line}-${r.endLine}`);
          }
        }
        if (!e.children.length) out += ` "${e.textContent.trim().slice(0, 30)}"`;
        console.log("  " + out);
        if (!/katex|math/u.test(e.getAttribute("class") || "")) e.children.forEach((c) => visit(c, depth + 1));
      };
      page.document.children.forEach((c) => visit(c, 0));
      if (erase !== false) for (const key of seen) {
        const [line, endLine] = key.split("-").map(Number);
        const run = fixture({ text: source });
        await run.send("previewEditOpen", { editId: "e1", line, endLine });
        const [answer] = run.of("previewEditSource");
        if (!answer) { console.log(`  ${key} no editor`); continue; }
        console.log(`  ${key} opens ${JSON.stringify(lines.slice(line - 1, endLine).join("\n"))}`);
      }
    } catch (error) { console.log(`  THROWS ${error.stack.split("\n").slice(0, 3).join(" | ")}`); }
  }
})();
