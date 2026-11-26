// Claim C at this head: the two Known gaps sentences about a box left with a heading or `---` first,
// and about cards and {div} blocks that start with dashes. Every box kind, erasing the first block
// through PreviewManager, rendered with the same page helpers.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");

const load = async (source) => {
  const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
  const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
  return { page, blocks };
};
const html = (page) => {
  const boxes = page.document.querySelectorAll("aside, details, [data-okf-github-alert]")
    .map((e) => `<${e.tagName.toLowerCase()} ${e.getAttribute("class")}> ${JSON.stringify(e.textContent.replace(/\s+/g, " ").trim())} hr=${e.querySelectorAll("hr").length}`).slice(0, 2).join(" | ");
  const text = JSON.stringify(page.document.querySelectorAll("p, h1, h2, li").map((e) => e.textContent.trim()).join("/").slice(0, 120));
  return `${boxes || "(no box)"} ; page text ${text}`;
};
const colon = (open, opts = []) => (b) => [`::::${open}`, ...opts, ...b, "::::"];
const BOXES = {
  note: colon("{note}"), noteBT: (b) => ["````{note}", ...b, "````"], titled: colon("{admonition} T"),
  seealso: colon("{seealso}"), version: colon("{versionadded} 1.0"), deprecated: colon("{deprecated} 1.0"),
  noteDropdownClass: colon("{note}", [":class: dropdown", ""]), titledDropdownClass: colon("{admonition} T", [":class: dropdown", ""]),
  noteOpen: colon("{note}", [":class: dropdown", ":open:", ""]),
  dropdown: colon("{dropdown}"), dropdownT: colon("{dropdown} T"),
  dropdownOpen: colon("{dropdown}", [":open:", ""]), dropdownTOpen: colon("{dropdown} T", [":open:", ""]),
  dropdownOpenYaml: colon("{dropdown} T", ["---", "open: true", "---"]),
  dropdownColor: colon("{dropdown} T", [":color: primary", ""]),
  calloutDot: colon("{.callout-note}"), calloutFence: (b) => ["::: {.callout-tip}", ...b, ":::"],
  calloutDiv: colon("{div}", [":class: callout-tip", ""]), collapse: (b) => ['::: {.callout-tip collapse="true"}', ...b, ":::"],
  alert: (b) => ["> [!NOTE]", ...b.map((l) => (l ? `> ${l}` : ">"))],
};
(async () => {
  console.log("--- erase the first block");
  for (const [name, box] of Object.entries(BOXES)) for (const [sn, sp] of [["rule", ["---"]], ["heading", ["## Headword"]]]) {
    const lines = box(["Firstword.", "", ...sp, "", "Lastword."]);
    const source = `${[...lines, "", "Endword."].join("\n")}\n`;
    const n = lines.indexOf(lines.find((l) => l.endsWith("Firstword."))) + 1;
    try {
      const { page } = await load(source);
      const run = fixture({ text: source });
      await run.send("previewEditSave", { editId: "e1", line: n, endLine: n, originalText: `${lines[n - 1]}\n`, editedText: lines[n - 1].startsWith("> ") ? ">\n" : "\n", final: true });
      const written = run.document.getText();
      let after; try { after = html((await load(written)).page); } catch (error) { after = `THROWS ${error.message}`; }
      console.log(`${name}|${sn}\n  before ${html(page)}\n  after  ${after}\n  text kept ${written.includes("Lastword.")}`);
    } catch (error) { console.log(`${name}|${sn} source THROWS ${error.message}`); }
  }
  console.log("--- cards and divs with dashes");
  for (const [name, source] of [
    ["card in note, starts ---", "::::{note}\n:::{card}\n\n---\n\nCardword.\n\nMoreword.\n:::\n::::\n"],
    ["card in note, --- after first", "::::{note}\n:::{card}\nCardword.\n\n---\n\nMoreword.\n:::\n::::\n"],
    ["titled card in note, --- after first", "::::{note}\n:::{card} T\nCardword.\n\n---\n\nMoreword.\n:::\n::::\n"],
    ["card in note, YAML-like --- start", "::::{note}\n:::{card}\n---\nCardword.\n\nMoreword.\n:::\n::::\n"],
    ["div argument callout, starts ---", ":::{div} callout-note\n\n---\n\nBetaword.\n:::\n\nEndword.\n"],
    ["div plain, starts ---", ":::{div}\n\n---\n\nBetaword.\n:::\n\nEndword.\n"],
    ["div other argument, starts ---", ":::{div} someclass\n\n---\n\nBetaword.\n:::\n\nEndword.\n"],
    ["div argument in note, starts ---", "::::{note}\n:::{div} callout-note\n\n---\n\nBetaword.\n:::\n::::\n"],
  ]) {
    try { const { page } = await load(source); console.log(`${name} ${JSON.stringify(source)}\n  ${html(page)}`); }
    catch (error) { console.log(`${name} ${JSON.stringify(source)}\n  THROWS ${error.message}`); }
  }
  console.log("--- chord moving --- first in a div that is no box (what the page offers, then the host)");
  for (const [name, source] of [
    ["div plain", ":::{div}\nAlphaword\n\n---\n\nBetaword\n:::\n"],
    ["div argument callout", ":::{div} callout-note\nAlphaword\n\n---\n\nBetaword\n:::\n"],
    ["div other argument", ":::{div} someclass\nAlphaword\n\n---\n\nBetaword\n:::\n"],
  ]) {
    const { page, blocks } = await load(source);
    console.log(`${name}: top-level ${blocks.topLevelMappedBlocks().map((e) => `<${e.tagName}>${JSON.stringify(blocks.blockRange(e))}`).join(" ")}`);
    console.log(`  mapped ${page.document.querySelectorAll(MAPPINGS_SELECTOR).map((e) => `<${e.tagName} ${blocks.blockRange(e).line}-${blocks.blockRange(e).endLine}>`).join("")}`);
  }
})();
