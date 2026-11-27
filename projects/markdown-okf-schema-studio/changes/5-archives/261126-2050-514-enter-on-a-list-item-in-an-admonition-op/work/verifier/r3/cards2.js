// Known gaps sentence "A card of a box whose body starts with `---`, or holds it after its first block,
// shows only part of its body": many card bodies in boxes, and which body words the page shows.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const WORDS = ["Alpha", "Beta", "Gamma"];
const BODIES = {
  "start, blank first": ["", "---", "", "Alpha", "", "Beta"],
  "start, tight": ["---", "Alpha", "", "Beta"],
  "start, tight, blank after": ["---", "", "Alpha", "", "Beta"],
  "start, closed block": ["---", "Alpha", "---", "Beta"],
  "after first, blanks": ["Alpha", "", "---", "", "Beta"],
  "after first, no blank before": ["Alpha", "---", "Beta"],
  "after first, no blank after": ["Alpha", "", "---", "Beta"],
  "after first, twice": ["Alpha", "", "---", "", "Beta", "", "---", "", "Gamma"],
  "after first, tight twice": ["Alpha", "", "---", "Beta", "---", "Gamma"],
  "after first, last": ["Alpha", "", "Beta", "", "---"],
  "after options": [":class-card: x", "", "Alpha", "", "---", "", "Beta"],
  "after options, start": [":class-card: x", "", "---", "", "Alpha", "", "Beta"],
  "after options, start tight": [":class-card: x", "---", "Alpha", "", "Beta"],
  "after header": ["Alpha", "^^^", "Beta", "", "---", "", "Gamma"],
  "after list": ["- Alpha", "", "---", "", "Beta"],
  "after fence": ["```", "Alpha", "```", "", "---", "", "Beta"],
};
const BOXES = {
  top: (c) => c,
  note: (c) => ["::::::{note}", ...c, "::::::"],
  titled: (c) => ["::::::{admonition} T", ...c, "::::::"],
  dropdown: (c) => ["::::::{dropdown} T", ...c, "::::::"],
  alert: (c) => ["> [!NOTE]", ...c.map((l) => (l ? `> ${l}` : ">"))],
};
const CARDS = {
  card: (b) => [":::{card}", ...b, ":::"], titled: (b) => [":::{card} Title", ...b, ":::"],
  tick: (b) => ["```{card}", ...b.map((l) => l), "```"],
  grid: (b) => ["::::{grid}", ":::{grid-item-card}", ...b, ":::", "::::"],
};
(async () => {
  for (const [bn, body] of Object.entries(BODIES)) for (const [on, box] of Object.entries(BOXES)) for (const [cn, card] of Object.entries(CARDS)) {
    if (cn === "tick" && bn === "after fence") continue;
    const source = `${box(card(body)).join("\n")}\n`;
    const expected = WORDS.filter((w) => source.includes(w));
    try {
      const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
      const text = page.document.textContent;
      const missing = expected.filter((w) => !text.includes(w));
      console.log(`${bn} | ${on} | ${cn} | missing=${missing.join(",") || "-"} code=${page.document.querySelectorAll("pre").length} hr=${page.document.querySelectorAll("hr").length}`);
    } catch (error) { console.log(`${bn} | ${on} | ${cn} | THROWS ${error.message}`); }
  }
})();
