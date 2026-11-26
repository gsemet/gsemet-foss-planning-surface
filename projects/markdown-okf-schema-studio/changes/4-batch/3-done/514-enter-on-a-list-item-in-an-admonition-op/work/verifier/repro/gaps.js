// The remaining Known gaps and Changes claims, through the real renderer, page helpers and
// PreviewManager of one build.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { installBlockMoves } = o("src/page/features/blockMoves.js");
const L = (...l) => `${l.join("\n")}\n`;
const all = (e) => [e, ...e.children.flatMap(all)];

async function load(source) {
  const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
  const context = { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" };
  const blocks = createMappedBlocks(page.document, context);
  const moves = installBlockMoves({ document: page.document, window: {}, context, host: {}, state: {},
    tools: { blockSelection: {} }, blocks });
  const mapped = all(page.document).filter((e) => e.getAttribute("data-sphinx-source-line") !== null);
  const r = (e) => { const x = blocks.blockRange(e); return `${x.line}-${x.endLine}`; };
  const name = (e) => `<${e.tagName.toLowerCase()} ${r(e)}>`;
  const opens = (e, exact) => {
    const target = exact ? e : all(e).pop();
    const editing = blocks.editingElementFor(target.closest("[data-sphinx-source-line]"), { exact });
    const x = editing.sourceRange ?? blocks.blockRange(editing.element);
    return `<${editing.element.tagName.toLowerCase()} ${x.line}-${x.endLine}>`;
  };
  const inBox = (e) => e.parentElement?.closest(".admonition");
  async function chord(e, direction) {
    // Inside a box the page uses moveNeighbour; outside, the neighbouring top-level block.
    let neighbour;
    if (inBox(e)) { if (!moves.moveNeighbour) return "n/a on base"; neighbour = moves.moveNeighbour(e, direction); }
    else { const top = blocks.topLevelMappedBlocks(); neighbour = top[top.indexOf(e) + (direction === "up" ? -1 : 1)]; }
    if (!neighbour) return "no neighbour, nothing sent";
    const a = blocks.blockRange(e), b = blocks.blockRange(neighbour);
    const run = fixture({ text: source });
    await run.send("previewBlockMove", { line: a.line, endLine: a.endLine, neighbourLine: b.line, neighbourEndLine: b.endLine, direction });
    const [answer] = run.of("previewBlockMoveResult");
    return answer?.ok ? `MOVED past ${name(neighbour)} -> ${JSON.stringify(run.document.getText())}` : `refused past ${name(neighbour)}: ${answer?.reason}`;
  }
  return { page, blocks, moves, mapped, name, opens, chord };
}

async function report(title, source) {
  console.log(`\n=== ${title}\n${source.split("\n").slice(0, -1).map((l, i) => `${String(i + 1).padStart(3)} ${l}`).join("\n")}`);
  const p = await load(source);
  for (const e of p.mapped) {
    console.log(`  ${p.name(e)} "${e.textContent.trim().replace(/\s+/gu, " ").slice(0, 30)}" click=${p.opens(e, false)} enter=${p.opens(e, true)}`);
  }
  return p;
}

(async () => {
  let p = await report("topic in a note", L("::::{note}", "Before.", "", "```{topic} Title", "Topic one.", "", "Topic two.", "```", "", "After.", "::::"));
  for (const e of p.mapped.slice(1)) for (const d of ["up", "down"]) console.log(`  chord ${d} from ${p.name(e)}: ${await p.chord(e, d)}`);

  await report("quoted colon admonition left open, final quoted fence", L("> ::::{note}", "> Before.", ">", "> :::{tip}", "> Tip body.", "> :::"));
  await report("same, unquoted (for comparison)", L("::::{note}", "Before.", "", ":::{tip}", "Tip body.", ":::"));

  for (const [title, directive] of [
    ["top-level mermaid directive", ["```{mermaid}", "graph TD", "  A --> B", "```"]],
    ["top-level math directive", ["```{math}", "x = 1", "```"]],
    ["top-level code-block directive", ["```{code-block} python", "print(1)", "```"]],
    ["top-level table directive", ["```{table} Caption", "| a | b |", "| - | - |", "| 1 | 2 |", "```"]],
    ["top-level table directive without caption", ["```{table}", "| a | b |", "| - | - |", "| 1 | 2 |", "```"]],
  ]) {
    p = await report(title, L("Before.", "", ...directive, "", "After."));
    const first = p.mapped[0], last = p.mapped[p.mapped.length - 1];
    console.log(`  chord down from ${p.name(first)}: ${await p.chord(first, "down")}`);
    console.log(`  chord up from ${p.name(last)}: ${await p.chord(last, "up")}`);
  }

  for (const [title, source] of [
    ["alert block, no lazy line", L("> [!NOTE]", "> First.", ">", "> Second.", ">", "> Third.")],
    ["alert block with a lazy line", L("> [!NOTE]", "> First.", ">", "> Second", "lazy line.", ">", "> Third.")],
    ["MyST admonition block erased", L(":::{note}", "First.", "", "Second.", "", "Third.", ":::")],
    ["indented alert in a list item", L("- item", "", "  > [!TIP]", "  > First.", "  >", "  > Second.")],
  ]) {
    p = await report(title, source);
    for (const target of p.mapped.filter((e) => e.tagName === "P" && (e.textContent.trim() === "First." || e.textContent.includes("Second")))) {
    const x = p.blocks.blockRange(target);
    for (const autosave of [false, true]) {
      const run = fixture({ text: source });
      await run.send("previewEditOpen", { editId: "e1", line: x.line, endLine: x.endLine });
      const [answer] = run.of("previewEditSource");
      const message = { editId: "e1", line: x.line, endLine: x.endLine, originalText: answer.originalText, editedText: answer.originalText.endsWith(String.fromCharCode(10)) ? String.fromCharCode(10) : "" };
      if (autosave) await run.send("previewEditSave", { ...message, final: false });
      await run.send("previewEditSave", { ...message, final: true });
      console.log(`  erase ${x.line}-${x.endLine}${autosave ? " (autosave then commit)" : ""}: writes=${run.applyCalls.length} -> ${JSON.stringify(run.document.getText())}`);
      const rendered = await renderMappedPage(run.document.getText(), "/w/a.md", "file:///w/a.md");
      const alert = rendered.document.querySelectorAll(".admonition")[0];
      console.log("    rendered after: admonitions " + rendered.document.querySelectorAll(".admonition").length + ", plain blockquotes " + rendered.document.querySelectorAll("blockquote").length + ", text inside the first admonition: " + JSON.stringify(alert?.textContent.trim()));
    }
    }
  }

  p = await report("neighbouring rules: card, quote, grid, list item inner block", L("::::::{note}", "Before.", "", "> Quote.", "", "- item", "", "  Inner.", "", ":::{card} Card", "Body.", ":::", "", "After.", "::::::"));
  for (const e of p.mapped.slice(1)) for (const d of ["up", "down"]) console.log(`  chord ${d} from ${p.name(e)}: ${await p.chord(e, d)}`);

  p = await report("comment between two blocks of an alert", L("> [!NOTE]", "> One.", ">", "> <!-- x -->", ">", "> Two."));
  console.log(`  ${await p.chord(p.mapped.find((e) => e.textContent.trim() === "One." && e.tagName === "P"), "down")}`);
  p = await report("mixed quote prefixes", L("> [!NOTE]", ">One.", ">", "> Two."));
  console.log(`  ${await p.chord(p.mapped.find((e) => e.textContent.trim() === "One." && e.tagName === "P"), "down")}`);

  await report("callout and dropdown", L(":::::{dropdown} Title", "Drop body.", "", "::::{div} callout-note", "Callout body.", "::::", ":::::"));
  await report("version admonitions", L("```{versionadded} 1.2 Inline body.", "```", "", "```{deprecated} 1.3", "", "", "Late body.", "", "- item", "```"));
})();
