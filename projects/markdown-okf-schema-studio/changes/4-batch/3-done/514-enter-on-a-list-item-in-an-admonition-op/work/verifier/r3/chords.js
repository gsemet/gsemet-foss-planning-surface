// The move-chord and outside-box Known gaps bullets and the chord rows of Changes, with one build.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { installBlockMoves } = o("src/page/features/blockMoves.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");
const L = (...l) => `${l.join("\n")}\n`;
const tidy = (t) => t.replace(/\s+/gu, " ").trim();

async function load(source) {
  const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
  const context = { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" };
  const blocks = createMappedBlocks(page.document, context);
  const moves = installBlockMoves({ document: page.document, window: {}, context, host: {}, state: {}, tools: { blockSelection: {} }, blocks });
  const mapped = page.document.querySelectorAll(MAPPINGS_SELECTOR);
  const name = (e) => { const r = blocks.blockRange(e); return `<${e.tagName.toLowerCase()} ${r.line}-${r.endLine}>`; };
  return { page, blocks, moves, mapped, name };
}
const inBox = (e) => e.parentElement?.closest(".admonition");
async function chord(p, source, e, direction) {
  let neighbour;
  if (inBox(e) && p.moves.moveNeighbour) neighbour = p.moves.moveNeighbour(e, direction);
  else { const top = p.blocks.topLevelMappedBlocks(); neighbour = top[top.indexOf(e) + (direction === "up" ? -1 : 1)]; }
  if (!neighbour) return "no neighbour, nothing sent";
  const a = p.blocks.blockRange(e), b = p.blocks.blockRange(neighbour);
  const run = fixture({ text: source });
  await run.send("previewBlockMove", { line: a.line, endLine: a.endLine, neighbourLine: b.line, neighbourEndLine: b.endLine, direction });
  const [answer] = run.of("previewBlockMoveResult");
  if (!answer?.ok) return `refused past ${p.name(neighbour)}: ${answer?.reason}`;
  const written = run.document.getText();
  let after; try { const q = await load(written); after = JSON.stringify(q.page.document.querySelectorAll("aside, details").map((x) => `title=${tidy(x.querySelectorAll(".admonition-title, summary")[0]?.textContent ?? "")} text=${tidy(x.textContent).slice(0, 80)}`)); } catch (error) { after = `THROWS ${error.message}`; }
  return `MOVED past ${p.name(neighbour)} -> ${JSON.stringify(written)}\n      page ${after}`;
}
async function report(title, source, pick) {
  console.log(`\n=== ${title} ${JSON.stringify(source)}`);
  let p; try { p = await load(source); } catch (error) { console.log(`  THROWS ${error.message}`); return; }
  console.log(`  mapped ${p.mapped.map(p.name).join("")}`);
  for (const e of pick ? p.mapped.filter(pick) : p.mapped.slice(1)) for (const d of ["up", "down"]) console.log(`  chord ${d} from ${p.name(e)} "${tidy(e.textContent).slice(0, 20)}": ${await chord(p, source, e, d)}`);
  return p;
}
(async () => {
  await report("B4 image paragraph", L("::::{note}", "Alpha", "", "![a](x.png)", "", "Beta", "::::"));
  await report("B4 image directive", L("::::{note}", "Alpha", "", ":::{image} x.png", ":::", "", "Beta", "::::"));
  await report("table directive with caption", L("::::{note}", "Alpha", "", ":::{table} Cap", "| a |", "| - |", "| cell |", ":::", "", "Beta", "::::"));
  await report("table directive without caption", L("::::{note}", "Alpha", "", ":::{table}", "| a |", "| - |", "| cell |", ":::", "", "Beta", "::::"));
  await report("topic", L("::::{note}", "Alpha", "", ":::{topic} T", "One", "", "Two", ":::", "", "Beta", "::::"));
  const t = await load(L("::::{note}", "Alpha", "", ":::{topic} T", "One", "", "Two", ":::", "", "Beta", "::::"));
  for (const e of t.mapped.filter((x) => x.tagName === "P")) {
    const leaf = e; const x = t.blocks.editingElementFor(leaf, { exact: false }); const r = x.sourceRange ?? t.blocks.blockRange(x.element);
    console.log(`  topic click ${t.name(e)} -> <${x.element.tagName.toLowerCase()} ${r.line}-${r.endLine}>`);
  }
  await report("bold-only paragraph", L("::::{note}", "Alpha", "", "**Bold**", "::::"));
  await report("bold-only in callout", L("::::{.callout-note}", "Alpha", "", "**Bold**", "::::"));
  for (const [n, opts] of [["class zzz", [":class: callout-zzz"]], ["name callout-x", [":name: callout-x"]], ["braces .callout-zzz", []]]) {
    const open = n.startsWith("braces") ? "::::{div .callout-zzz}" : "::::{div}";
    await report(`div mentioning callout (${n})`, L("::::::{note}", open, ...opts, "", "Alpha", "", "## Head", "::::", "::::::"));
    await report(`div mentioning callout, top (${n})`, L(open, ...opts, "", "Alpha", "", "## Head", "::::"));
  }
  await report("empty line added: note", L(":::{note}", "One", "", "Two", ":::"), (e) => e.tagName === "P" && e.textContent === "One");
  await report("empty line added: alert", L("> [!NOTE]", "> One", ">", "> Two"), (e) => e.tagName === "P" && e.textContent.trim() === "One");
  await report("item list moves", L("::::{note}", "Alpha", "", "- one", "- two", "", "Beta", "::::"));
  await report("heading titled/dropdown/alert and *** allowed", L("::::{admonition} T", "Alpha", "", "## Head", "::::"));
  await report("heading in dropdown", L("::::{dropdown} T", "Alpha", "", "## Head", "::::"));
  await report("heading in alert", L("> [!NOTE]", "> Alpha", ">", "> ## Head"));
  await report("*** in note", L("::::{note}", "Alpha", "", "***", "::::"));
  await report("heading tilde untitled", L("~~~{note}", "Alpha", "", "## Head", "~~~"));
  await report("heading backtick untitled", L("````{warning}", "Alpha", "", "## Head", "````"));

  console.log("\n######## outside a box");
  for (const [title, directive] of [
    ["mermaid", ["```{mermaid}", "graph TD", "  A --> B", "```"]],
    ["math", ["```{math}", "x = 1", "```"]],
    ["code-block", ["```{code-block} python", "print(1)", "```"]],
    ["captioned table", ["```{table} Caption", "| a | b |", "| - | - |", "| 1 | 2 |", "```"]],
  ]) {
    const source = L("Before.", "", ...directive, "", "After.");
    const p = await report(`outside ${title}`, source, (e) => /Before|After/u.test(e.textContent));
    const dir = p.mapped[1];
    const x = p.blocks.editingElementFor(dir, { exact: false }); const r = x.sourceRange ?? p.blocks.blockRange(x.element);
    console.log(`  click on ${p.name(dir)} -> <${x.element.tagName.toLowerCase()} ${r.line}-${r.endLine}> ${JSON.stringify(source.split("\n").slice(r.line - 1, r.endLine).join("\n"))}`);
  }
  const source = L("- Item", "", "  ```{figure} x.png", "  Capword", "  ```", "", "Tail");
  const p = await load(source);
  console.log(`\n=== outside figure caption in list ${JSON.stringify(source)}\n  mapped ${p.mapped.map(p.name).join("")}`);
  for (const e of p.mapped.filter((x) => tidy(x.textContent) === "Capword")) for (const exact of [false, true]) {
    const x = p.blocks.editingElementFor(e, { exact }); const r = x.sourceRange ?? p.blocks.blockRange(x.element);
    console.log(`  ${exact ? "enter" : "click"} ${p.name(e)} -> <${x.element.tagName.toLowerCase()} ${r.line}-${r.endLine}> ${JSON.stringify(source.split("\n").slice(r.line - 1, r.endLine).join("\n"))}`);
  }
})();
