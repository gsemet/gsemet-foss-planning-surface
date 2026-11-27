// Verifier probe of CR-517: the PR's "Known gaps" case (two text nodes of a block side by side).
// Claim to check: the page code before this change does the same.
// Run from the worktree: node <this file> <base.js> <head.js>
const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");
const { chromium } = createRequire(path.join(process.cwd(), "package.json"))("playwright-core");
const modules = process.argv.slice(2).map((file) => fs.readFileSync(file, "utf8"));
const thread = (id, quote) => ({ id, anchor: { line: 1, endLine: 1, quote, prefix: "", suffix: "" }, resolved: false, orphaned: false,
  createdAt: "", comments: [{ id: "c" + id, author: "Ada", createdAt: "", body: "Body" }] });
const A = thread("a", "alpha "), AEND = thread("a", "bravo cha"), CROSS = thread("b", "charlie");
// Text nodes "alpha bravo cha" + "rlie delta" side by side.
const cases = {
  "highlight ends at the boundary, then a quote crosses it": [[AEND], [AEND, CROSS], [CROSS]],
  "highlight elsewhere, then a quote crosses": [[A], [A, CROSS], [CROSS], [CROSS]],
};
(async () => {
  const browser = await chromium.launch();
  try {
    console.log("chromium", browser.version());
    for (const [name, lists] of Object.entries(cases)) {
      for (const [side, source] of [["base", modules[0]], ["head", modules[1]]]) {
        const run = async (sequence) => {
          const page = await browser.newPage();
          await page.setContent('<main><p data-line="1"></p></main>');
          await page.evaluate(source + ";window.CT = CT;");
          const state = await page.evaluate((sequence) => {
            const p = document.querySelector("p");
            p.append(document.createTextNode("alpha bravo cha"), document.createTextNode("rlie delta"));
            const comments = CT.installCommentThreads(document, window, { reply() {}, resolve() {}, remove() {} });
            for (const list of sequence) comments.setThreads(list);
            return JSON.stringify([...p.childNodes].map((n) => n.nodeType === 3 ? n.nodeValue
              : n.tagName + "(" + (n.getAttribute("data-okf-comment-thread") ?? "badge " + n.getAttribute("data-okf-comment-badge")) + ")" + n.textContent));
          }, sequence);
          await page.close();
          return state;
        };
        for (let n = 1; n <= lists.length; n += 1) {
          const inPlace = await run(lists.slice(0, n));
          const fresh = await run([lists[n - 1]]);
          console.log(name, "|", side, "list", n, inPlace === fresh ? "same as fresh" : "DIFFERS from fresh", inPlace, inPlace === fresh ? "" : "fresh " + fresh);
        }
      }
    }
  } finally {
    await browser.close();
  }
})().catch((error) => { console.error(error); process.exit(1); });
