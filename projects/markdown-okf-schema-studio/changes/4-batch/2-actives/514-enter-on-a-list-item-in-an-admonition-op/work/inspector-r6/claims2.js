const path = require("node:path");
const root = process.argv[2];
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");
const t = (...l) => `${l.join("\n")}\n`;
const CASES = [
  ["tab in dropdown", t("::::::{dropdown} T", "Lead", "", "::::{tab-set}", ":::{tab-item} One", "First", "", "Second", ":::", "::::", "::::::")],
  ["tab outside", t("::::{tab-set}", ":::{tab-item} One", "First", "", "Second", ":::", "::::")],
  ["card in note", t("::::{note}", "Lead", "", ":::{card} Head", "One", "", "Two", ":::", "::::")],
  ["tab panel in note", t("::::::{note}", "Lead", "", "::::{tab-set}", ":::{tab-item} One", "First", "", "Second", ":::", "::::", "::::::")],
  ["table caption in note", t("::::{note}", "Alpha", "", ":::{table} Cap", "| a |", "| - |", "| cell |", ":::", "::::")],
  ["dd rest", t(":::{dropdown} Title", "", "", "---", "", "Beta", ":::")],
  ["dd open rest", t(":::{dropdown} Title", ":open:", "", "", "", "---", "", "Beta", ":::")],
  ["note rest", t(":::{note}", "", "", "---", "", "Beta", ":::")],
  ["alert rest", t("> [!NOTE]", ">", ">", "> ---", ">", "> Beta")],
  ["callout rest", t(":::{div}", ":class: callout-note", "", "", "---", "", "Beta", ":::")],
  ["version", t("```{versionadded} 1.0", "Alpha", "", "- one", "- two", "```")],
  ["version colon", t(":::{versionadded} 1.0 inline text", "", "Alpha", ":::")],
  ["callout title", t(":::{div}", ":class: callout-note", "", "## Head", "", "Body", ":::")],
  ["details", t("<details>", "<summary>Sum</summary>", "", "Body", "", "</details>")],
  ["details note", t(":::{note}", "<details>", "<summary>Sum</summary>", "", "Body", "", "</details>", ":::")],
];
(async () => {
  for (const [name, source] of CASES) {
    console.log(`\n=== ${name} ${JSON.stringify(source)}`);
    try {
      const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
      const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
      const all = (e) => [e, ...e.children.flatMap(all)];
      for (const e of page.document.children.flatMap(all)) {
        const hit = e.closest(MAPPINGS_SELECTOR);
        const own = e.children.length ? "" : e.textContent.trim();
        if (!hit) { if (own) console.log(`  <${e.tagName}> ${own} unmapped`); continue; }
        if (!own && !/aside|details|DETAILS|ASIDE/u.test(e.tagName)) continue;
        const f = (exact) => { const x = blocks.editingElementFor(hit, { exact }); const r = x.sourceRange ?? blocks.blockRange(x.element); return `${r.line}-${r.endLine}`; };
        console.log(`  <${e.tagName} ${e.getAttribute("class") ?? ""}> ${own.slice(0, 30)} click ${f(false)} enter ${f(true)}`);
      }
    } catch (error) { console.log(`  THROWS ${error.message}`); }
  }
})();
