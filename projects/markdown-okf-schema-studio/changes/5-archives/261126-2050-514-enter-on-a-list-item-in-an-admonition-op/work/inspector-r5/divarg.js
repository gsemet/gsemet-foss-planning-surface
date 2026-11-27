// The host move of a paragraph below a --- line in a {div} that is no callout.
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
(async () => {
  const source = [":::{div} callout-note", "Before.", "", "---", "", "After.", ":::", ""].join(String.fromCharCode(10));
  const run = fixture({ text: source });
  await run.send("previewBlockMove", { line: 2, endLine: 2, neighbourLine: 4, neighbourEndLine: 4, direction: "down" });
  console.log(JSON.stringify(run.of("previewBlockMoveResult").map(({ ok, reason }) => [ok, reason])));
  const after = run.document.getText();
  console.log(JSON.stringify(after));
  try { await renderMappedPage(after, "/w/a.md", "file:///w/a.md"); console.log("renders"); } catch (e) { console.log("THROWS " + e.message); }
})();
