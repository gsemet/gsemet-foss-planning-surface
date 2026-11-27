// The round 4 Known gaps, through the real renderer, page helpers and PreviewManager of one build.
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
const html = (page) => page.document.querySelectorAll("aside, details, [data-okf-github-alert]")
  .map((e) => `<${e.tagName.toLowerCase()} ${e.getAttribute("class")}> ${JSON.stringify(e.textContent.replace(/\s+/g, " ").trim())} hr=${e.querySelectorAll("hr").length}`).slice(0, 2).join(" | ");
const leaves = (page, blocks, source) => {
  const lines = source.split("\n");
  for (const e of page.document.querySelectorAll(MAPPINGS_SELECTOR)) {
    const x = blocks.editingElementFor(e, { exact: true });
    const r = x.sourceRange ?? blocks.blockRange(x.element);
    console.log(`  enter <${e.tagName.toLowerCase()}> ${JSON.stringify(e.textContent.trim().slice(0, 24))} -> ${r.line}-${r.endLine} ${JSON.stringify(lines.slice(r.line - 1, r.endLine).join("\n"))}`);
  }
};
const erase = async (source, line, endLine) => {
  const lines = source.split("\n");
  const run = fixture({ text: source });
  await run.send("previewEditSave", { editId: "e1", line, endLine, originalText: `${lines.slice(line - 1, endLine).join("\n")}\n`, editedText: "", final: true, deleteWhenEmpty: true });
  return run.document.getText();
};
const show = async (name, source) => {
  const { page, blocks } = await load(source);
  console.log(`\n=== ${name}\nsource ${JSON.stringify(source)}\nrender ${html(page)}`);
  return { page, blocks };
};

(async () => {
  for (const [name, source, a, b] of [
    ["erase first before --- , note", ":::{note}\nBefore.\n\n---\n\nAfter.\n:::\n", 2, 2],
    ["erase first before --- , dropdown", ":::{dropdown} T\nBefore.\n\n---\n\nAfter.\n:::\n", 2, 2],
    ["erase first before --- , alert", "> [!NOTE]\n> Before.\n>\n> ---\n>\n> After.\n", 2, 2],
    ["erase first before heading, note", ":::{note}\nBefore.\n\n## Head\n\nAfter.\n:::\n", 2, 2],
    ["erase first before heading, callout", "::: {.callout-note}\nBefore.\n\n## Head\n\nAfter.\n:::\n", 2, 2],
  ]) {
    await show(name, source);
    const written = await erase(source, a, b);
    console.log(`erase ${a}-${b} written ${JSON.stringify(written)}\nafter  ${html((await load(written)).page)}`);
  }
  for (const [name, source] of [
    ["card in a note, body starting with dashes", "::::{note}\n:::{card}\n---\nCard text.\n\nMore.\n:::\n::::\n"],
    ["bold paragraph first", ":::{note}\n**Bold**\n\nAfter.\n:::\n"],
  ]) await show(name, source);
  for (const [name, source] of [
    ["spaced name, heading", ":::{ note }\nBefore.\n\n## Head\n:::\n"],
    ["spaced name, rule", ":::{ note }\nBefore.\n\n---\n:::\n"],
    ["callout-like class, heading", "::::{div}\n:class: callout-zzz\n\nBefore.\n\n## Head\n::::\n"],
    ["fence div .callout-zzz, heading", "::: {.callout-zzz}\nBefore.\n\n## Head\n:::\n"],
  ]) {
    await show(name, source);
    const run = fixture({ text: source });
    const lines = source.split("\n");
    const upper = lines.indexOf("Before.") + 1;
    await run.send("previewBlockMove", { line: upper, endLine: upper, neighbourLine: upper + 2, neighbourEndLine: upper + 2, direction: "down" });
    const [r] = run.of("previewBlockMoveResult");
    console.log(`move ok=${r.ok} reason=${r.reason} written ${JSON.stringify(run.document.getText())}\nafter  ${html((await load(run.document.getText())).page)}`);
  }
  for (const [name, source] of [
    ["options block + rule, paragraph last", ":::{note}\n---\nclass: x\n---\nBefore.\n\n---\n\nAfter.\n:::\n"],
    ["options block, no rule", ":::{note}\n---\nclass: x\n---\nBefore.\n\nAfter.\n:::\n"],
    ["options block + rule, code last", ":::{note}\n---\nclass: x\n---\nBefore.\n\n---\n\n```py\nx\n```\n:::\n"],
    ["options block + rule, nested note last", "::::{note}\n---\nclass: x\n---\nBefore.\n\n---\n\n:::{tip}\nTip.\n:::\n::::\n"],
    ["options block + rule, list last", ":::{note}\n---\nclass: x\n---\nBefore.\n\n---\n\n- one\n- two\n:::\n"],
    ["later paragraph after code in a tight item", ":::{note}\n- item\n  ```py\n  x\n  ```\n  after code\n:::\n"],
  ]) {
    const { page, blocks } = await show(name, source);
    leaves(page, blocks, source);
  }
  const item = ":::{note}\n- Step one\n\n  ```{table} Caption\n  | a |\n  | - |\n  ```\n:::\n";
  await show("erase first line of an item holding a directive", item);
  const written = await erase(item, 2, 3);
  console.log(`erase 2-3 written ${JSON.stringify(written)}\nafter  ${html((await load(written)).page)}`);
})();
