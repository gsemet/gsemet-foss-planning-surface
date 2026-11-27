// The three Known gaps bullets changed in the posted description, judged as written, with one build.
// A: tight list item followed by hidden content: click on the first paragraph, Enter on the item and
//    on its paragraph (reached with the real structural cursor), then the emptied editor.
// B: the first block of a box body emptied through PreviewManager, a `---` line first.
// C: card bodies with a `---` line right under the opening line, and the {div} that is no box.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot> <A|B|C>
const path = require("node:path");
const [root, part] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { structuralMove } = o("src/page/modules/structuralCursor.js");

const context = { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" };
const load = async (source) => {
  const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
  return { page, blocks: createMappedBlocks(page.document, context) };
};
const all = (e) => [e, ...e.children.flatMap(all)];
const tidy = (t) => t.replace(/\s+/gu, " ").trim();
const tree = (e, depth = 0) => {
  const own = e.children.length ? "" : ` ${JSON.stringify(tidy(e.textContent).slice(0, 70))}`;
  const cls = e.getAttribute("class");
  return `${"  ".repeat(depth)}<${e.tagName.toLowerCase()}${cls ? ` .${cls.replace(/ /g, ".")}` : ""}>${own}\n${e.children.map((c) => tree(c, depth + 1)).join("")}`;
};
const dom = (page) => page.document.children.map((c) => tree(c, 2)).join("").trimEnd();

// Every element the arrows reach, by walking the real cursor model over the real mapped blocks.
const reachable = (blocks) => {
  const describe = (element) => ({ element, get children() { return blocks.mappedChildren(element).map(describe); } });
  const tree_ = { element: null, children: blocks.selectableBlocks().map(describe) };
  const found = [];
  const visit = (position, keys) => {
    let node = tree_;
    for (const i of position.path) node = node.children[i];
    found.push({ element: node.element, keys });
    const down = structuralMove(tree_, position, "right");
    if (down.kind !== "move" || down.to.cell) return;
    let at = down.to; let walked = [...keys, "Right"];
    for (;;) {
      visit(at, walked);
      const next = structuralMove(tree_, at, "down");
      if (next.kind !== "move") break;
      at = next.to; walked = [...walked, "Down"];
    }
  };
  tree_.children.forEach((_, i) => visit({ path: [i] }, [`block ${i + 1}`]));
  return found;
};

const erase = async (source, line, endLine) => {
  const run = fixture({ text: source });
  await run.send("previewEditOpen", { editId: "e1", line, endLine });
  const [answer] = run.of("previewEditSource");
  if (!answer || answer.originalText === undefined) return { error: JSON.stringify(answer) };
  await run.send("previewEditSave", { editId: "e1", line, endLine, originalText: answer.originalText, editedText: answer.originalText.endsWith("\n") ? "\n" : "", final: true });
  return { text: answer.originalText, written: run.document.getText() };
};

async function partA() {
  const FOLLOW = {
    "HTML comment": ["  <!-- Hiddenword -->"], "HTML comment after blank": ["", "  <!-- Hiddenword -->"],
    HTML: ["  <div>Hiddenword</div>"], "HTML after blank": ["", "  <div>Hiddenword</div>"],
    "link definition": ["", "  [ref]: https://example.org/Hiddenword"],
    "footnote definition": ["", "  [^f]: Hiddenword"], target: ["  (Hiddenword)="], "percent comment": ["  % Hiddenword"],
  };
  const BOXES = {
    note: (c) => [":::{note}", ...c, ":::"], dropdown: (c) => [":::{dropdown} D", ...c, ":::"],
    alert: (c) => ["> [!NOTE]", ...c.map((l) => (l ? `> ${l}` : ">"))],
  };
  for (const [kind, follow] of Object.entries(FOLLOW)) for (const [boxName, box] of Object.entries(BOXES)) {
    const first = kind === "footnote definition" ? "- Itemword[^f]" : "- Itemword";
    const source = `${[...box([first, ...follow, "- Next"]), "", "Endword."].join("\n")}\n`;
    const { page, blocks } = await load(source);
    const walk = reachable(blocks);
    const item = walk.find((w) => w.element.tagName === "LI" && w.element.textContent.includes("Itemword"));
    const para = walk.find((w) => w.element.tagName === "P" && tidy(w.element.textContent).startsWith("Itemword"));
    const tight = !source.includes("\n\n- Next") && !source.includes("\n>\n> - Next");
    console.log(`\n=== ${kind} | ${boxName} | tight source ${tight} | ${JSON.stringify(source)}`);
    const p = para?.element ?? all(page.document).find((e) => e.tagName === "P" && tidy(e.textContent).startsWith("Itemword"));
    const gestures = [["click on first paragraph", p, false], ["Enter on the item", item?.element, true], ["Enter on the first paragraph", para?.element, true]];
    for (const [name, element, exact] of gestures) {
      if (!element) { console.log(`  ${name}: not reachable`); continue; }
      const x = blocks.editingElementFor(element, { exact });
      const r = x.sourceRange ?? blocks.blockRange(x.element);
      const result = await erase(source, r.line, r.endLine);
      const keys = exact ? ` [keys ${(element.tagName === "LI" ? item : para).keys.join(", ")}]` : "";
      console.log(`  ${name}${keys}: <${x.element.tagName.toLowerCase()}> ${r.line}-${r.endLine} editor ${JSON.stringify(result.text)} holds following content=${result.text?.includes("Hiddenword")}; after emptying, content left=${result.written?.includes("Hiddenword")}`);
    }
  }
}

async function partB() {
  const colon = (open, opts = []) => (b) => [`::::${open}`, ...opts, ...b, "::::"];
  const tick = (open, opts = []) => (b) => [`\`\`\`\`${open}`, ...opts, ...b, "````"];
  const BOXES = {
    titled: colon("{admonition} Titlewords"), "titled backtick": tick("{admonition} Titlewords"),
    "titled :class: dropdown": colon("{admonition} Titlewords", [":class: dropdown", ""]),
    "titled backtick :class: dropdown": tick("{admonition} Titlewords", [":class: dropdown", ""]),
    "titled :class: dropdown :open:": colon("{admonition} Titlewords", [":class: dropdown", ":open:", ""]),
    "titled :class: tip": colon("{admonition} Titlewords", [":class: tip", ""]),
    "titled :class: tip dropdown": colon("{admonition} Titlewords", [":class: tip dropdown", ""]),
    "titled :name:": colon("{admonition} Titlewords", [":name: somewhere", ""]),
    "titled no blank after option": colon("{admonition} Titlewords", [":class: tip"]),
    "titled with markup": colon("{admonition} The **bold** `title`"),
    note: colon("{note}"), tip: colon("{tip}"), warning: colon("{warning}"),
    "alert": (b) => ["> [!NOTE]", ...b.map((l) => (l ? `> ${l}` : ">"))],
    "callout": (b) => ["::: {.callout-tip}", ...b, ":::"],
    "callout with title attribute": (b) => ['::: {.callout-tip title="Titlewords"}', ...b, ":::"],
    dropdown: colon("{dropdown} Titlewords"), "dropdown :open:": colon("{dropdown} Titlewords", [":open:", ""]),
  };
  for (const [name, box] of Object.entries(BOXES)) {
    const lines = box(["Firstword.", "", "---", "", "Lastword."]);
    const source = `${[...lines, "", "Endword."].join("\n")}\n`;
    console.log(`\n=== ${name} ${JSON.stringify(source)}`);
    const { page, blocks } = await load(source);
    const p = all(page.document).filter((e) => e.tagName === "P" && tidy(e.textContent) === "Firstword.").pop();
    console.log(`  before\n${dom(page)}`);
    if (!p) { console.log("  no first paragraph"); continue; }
    const x = blocks.editingElementFor(p, {});
    const r = x.sourceRange ?? blocks.blockRange(x.element);
    const result = await erase(source, r.line, r.endLine);
    console.log(`  click opens <${x.element.tagName.toLowerCase()}> ${r.line}-${r.endLine} ${JSON.stringify(result.text)}; emptied writes ${JSON.stringify(result.written)} Lastword kept=${result.written.includes("Lastword.")}`);
    try { console.log(`  after\n${dom((await load(result.written)).page)}`); } catch (error) { console.log(`  after THROWS ${error.message}`); }
  }
}

async function partC() {
  const BODIES = {
    "--- Alpha blank Beta": ["---", "Alpha", "", "Beta"], "--- blank Alpha Beta": ["---", "", "Alpha", "", "Beta"],
    "--- Alpha": ["---", "Alpha"], "--- Alpha Beta (one paragraph)": ["---", "Alpha", "Beta"],
    "--- Alpha: x blank Beta": ["---", "Alpha: x", "", "Beta"], "---- Alpha blank Beta": ["----", "Alpha", "", "Beta"],
    "--- trailing space": ["--- ", "Alpha", "", "Beta"],
    "closed": ["---", "class-card: x", "---", "Alpha", "", "Beta"],
    "blank then ---": ["", "---", "", "Alpha", "", "Beta"],
  };
  const CARDS = {
    card: (b) => [":::{card}", ...b, ":::"], titled: (b) => [":::{card} Title", ...b, ":::"],
    tick: (b) => ["```{card}", ...b, "```"], grid: (b) => ["::::{grid}", ":::{grid-item-card}", ...b, ":::", "::::"],
  };
  for (const [bn, body] of Object.entries(BODIES)) for (const [cn, card] of Object.entries(CARDS)) {
    const source = `${["::::::{note}", ...card(body), "::::::"].join("\n")}\n`;
    try {
      const { page } = await load(source);
      const missing = ["Alpha", "Beta"].filter((w) => source.includes(w) && !page.document.textContent.includes(w));
      console.log(`card | ${bn} | ${cn} | missing=${missing.join(",") || "-"}`);
      if (cn === "card") console.log(dom(page));
    } catch (error) { console.log(`card | ${bn} | ${cn} | THROWS ${error.message}`); }
  }
  for (const open of [":::{div} callout-note", "```{div} callout-note", ":::{div} callout-tip extra"]) {
    for (const [bn, body] of Object.entries(BODIES)) {
      const close = open.startsWith("`") ? "```" : ":::";
      const source = `${[open, ...body, close, "", "Endword."].join("\n")}\n`;
      try {
        const { page } = await load(source);
        const missing = ["Alpha", "Beta", "Endword"].filter((w) => source.includes(w) && !page.document.textContent.includes(w));
        console.log(`div | ${open} | ${bn} | drawn, missing=${missing.join(",") || "-"} boxes=${page.document.querySelectorAll("aside").length}`);
      } catch (error) { console.log(`div | ${open} | ${bn} | THROWS ${error.message}`); }
    }
  }
}

({ A: partA, B: partB, C: partC })[part]().catch((error) => { console.error(error); process.exitCode = 1; });
