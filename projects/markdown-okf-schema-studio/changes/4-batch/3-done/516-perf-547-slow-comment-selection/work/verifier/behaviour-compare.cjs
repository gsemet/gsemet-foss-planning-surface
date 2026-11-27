// Verifier probe of CR-516: drives the same real mouse, wheel and keyboard steps in Chromium on the
// preview built from the base sources (out/vbase/out) and from the head sources (out/), and compares
// what a reader sees after each step has been drawn: the Comment button and its place, the composer's
// quote, the outline of edit mode, the copy button, the selected text of the scroll reports, and the
// copied or posted messages.
// Run from the worktree: node --import ./scripts/register-myst-patches.mjs <this file> <scratch dir>
const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");
const { pathToFileURL } = require("node:url");

const worktree = process.cwd();
const scratch = path.resolve(process.argv[2]);
const { chromium } = createRequire(path.join(worktree, "package.json"))("playwright-core");
const BUILDS = { old: path.join(worktree, "out", "vbase", "out"), new: path.join(worktree, "out") };

const code = (tag) => `\`\`\`python\n${Array.from({ length: 14 }, (_, i) => `${tag}_${i} = ${i}`).join("\n")}\n\`\`\`\n\n`;
const MARKDOWN = `# Title\n\nAlpha paragraph with some words.\n\nBravo paragraph with some words.\n\nCharlie paragraph with some words.\n\n`
  + `${code("first")}- one item\n- two item\n\n| a | b |\n| - | - |\n| 1 | 2 |\n\n${code("second")}`
  + "Filler paragraph with some words.\n\n".repeat(60);

async function build(side) {
  const load = (file) => require(path.join(BUILDS[side], file));
  const root = path.join(scratch, side);
  fs.mkdirSync(path.join(root, "out", "bundle"), { recursive: true });
  const real = fs.realpathSync(root);
  fs.writeFileSync(path.join(real, "out", "bundle", "preview.js"), load("test/page/runtimeHarness.js").pageRuntimeScript());
  const documentPath = path.join(real, "doc.md");
  fs.writeFileSync(documentPath, MARKDOWN);
  const files = load("src/node-services/nodeFileSystem.js").createNodeFileSystem();
  const rendered = await load("src/core/render/renderPipeline.js").renderPreviewDocument({
    files,
    document: { uri: { scheme: "file", fsPath: documentPath }, languageId: "markdown", version: 1, getText: () => MARKDOWN },
    workspaceRoot: real, requestId: 1, isWorkspaceTrusted: () => true,
  });
  const assets = load("test/shared/fakeAssets.js").fakeAssetResolver({ cspSource: "file:", url: (p) => pathToFileURL(p).href, extensionRoot: real });
  const bundle = { ...assets, bundleUri: (...s) => (s[0] === "preview.js" ? assets.bundleUri(...s) : undefined) };
  const built = await load("src/session/webview.js").buildPreviewWebviewHtml(files, rendered.html, real, bundle, {
    activeSourceFile: documentPath, documentId: pathToFileURL(documentPath).toString(), revision: 1, requestId: 1,
    previewThemeMode: "current", commentsEnabled: true,
  }, real, undefined, 800, true, [], "builtin");
  const file = path.join(real, "page.html");
  fs.writeFileSync(file, built.html);
  return file;
}

const settle = async (page) => {
  await page.waitForTimeout(400);
  await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(() => r()))));
};

const observe = (page) => page.evaluate(() => {
  const box = (selector) => Array.from(document.querySelectorAll(selector)).map((e) => {
    const r = e.getBoundingClientRect();
    return [r.x, r.y, r.width, r.height].map(Math.round).join(",");
  }).join(" ; ") || "none";
  const text = (e) => `${e.tagName.toLowerCase()}:${(e.textContent || "").replace(/\s+/g, " ").trim().slice(0, 30)}`;
  const outlined = Array.from(document.querySelectorAll("[data-sphinx-preview-edit-hover]")).map(text).join(" ; ") || "none";
  const posted = window.__posted;
  const scrolls = posted.filter((m) => m.type === "previewScroll" || m.type === "previewState");
  const last = scrolls[scrolls.length - 1];
  return {
    commentButton: box("[data-okf-comment-create]"),
    composer: Array.from(document.querySelectorAll("[data-okf-comment-quote]")).map((e) => e.textContent.replace(/\s+/g, " ")).join(" ; ") || "none",
    outlined,
    copyButton: box("[data-sphinx-preview-code-copy]"),
    scrollTop: Math.round(window.scrollY),
    reportedSelection: last && last.selectedText ? last.selectedText.replace(/\s+/g, " ").slice(0, 90) : "none",
    copied: posted.filter((m) => m.type === "previewCopyText").map((m) => m.text.slice(0, 20)).join(" ; ") || "none",
  };
});

const select = (page, from, to) => page.evaluate(([a, b]) => {
  const all = document.querySelectorAll("#sphinx-myst-preview-content p");
  window.getSelection().setBaseAndExtent(all[a].firstChild, 0, all[b].firstChild, 7);
}, [from, to]);

const installShortcut = () => { window.__shortcut = () => document.body.dispatchEvent(new KeyboardEvent("keydown", { key: "m", code: "KeyM", ctrlKey: true, altKey: true, bubbles: true, cancelable: true })); };

const pointOf = async (page, selector, index = 0, dx = 40, dy = 8) => {
  const r = await page.locator(selector).nth(index).boundingBox();
  return [r.x + dx, r.y + dy];
};

const P = "#sphinx-myst-preview-content p";
const PRE = "#sphinx-myst-preview-content pre";

const STEPS = [
  ["drag a selection across three paragraphs", async (page) => {
    const [x1, y1] = await pointOf(page, P, 0, 2);
    const [x2, y2] = await pointOf(page, P, 2, 120);
    await page.mouse.move(x1, y1); await page.mouse.down(); await page.mouse.move(x2, y2, { steps: 25 }); await page.mouse.up();
  }],
  ["wheel down 60", async (page) => { await page.mouse.wheel(0, 60); }],
  ["wheel down 40 more", async (page) => { await page.mouse.wheel(0, 40); }],
  ["wheel back up", async (page) => { await page.mouse.wheel(0, -100); }],
  ["hide the selected middle paragraph, then wheel", async (page) => {
    await page.evaluate(() => { document.querySelectorAll("#sphinx-myst-preview-content p")[1].hidden = true; });
    await settle(page); await page.mouse.wheel(0, 30);
  }],
  ["show it again, then wheel", async (page) => {
    await page.evaluate(() => { document.querySelectorAll("#sphinx-myst-preview-content p")[1].hidden = false; });
    await settle(page); await page.mouse.wheel(0, -30);
  }],
  ["remove the whole selected text, then wheel", async (page) => {
    await select(page, 2, 2); await settle(page);
    await page.evaluate(() => { document.querySelectorAll("#sphinx-myst-preview-content p")[2].hidden = true; });
    await settle(page); await page.mouse.wheel(0, 30);
  }],
  ["show it, scroll to the top", async (page) => {
    await page.evaluate(() => { document.querySelectorAll("#sphinx-myst-preview-content p")[2].hidden = false; window.scrollTo(0, 0); });
  }],
  ["click in a paragraph (selection cleared)", async (page) => { await page.mouse.click(...await pointOf(page, P, 1, 60)); }],
  ["shortcut in the same task as a new selection", async (page) => {
    await page.evaluate(() => {
      const all = document.querySelectorAll("#sphinx-myst-preview-content p");
      window.getSelection().setBaseAndExtent(all[1].firstChild, 0, all[1].firstChild, 15);
      window.__shortcut();
    });
  }],
  ["escape", async (page) => { await page.keyboard.press("Escape"); }],
  ["an earlier selection, then another one and the shortcut at once after the announcement", async (page) => {
    await select(page, 0, 0); await settle(page);
    await page.evaluate(() => new Promise((done) => {
      document.addEventListener("selectionchange", () => queueMicrotask(() => { window.__shortcut(); done(); }), { once: true });
      const all = document.querySelectorAll("#sphinx-myst-preview-content p");
      window.getSelection().setBaseAndExtent(all[2].firstChild, 0, all[2].firstChild, 17);
    }));
  }],
  ["escape again", async (page) => { await page.keyboard.press("Escape"); }],
  ["a selection removed, the shortcut at once after the announcement", async (page) => {
    await select(page, 0, 0); await settle(page);
    await page.evaluate(() => new Promise((done) => {
      document.addEventListener("selectionchange", () => queueMicrotask(() => { window.__shortcut(); done(); }), { once: true });
      window.getSelection().removeAllRanges();
    }));
  }],
  ["escape once more", async (page) => { await page.keyboard.press("Escape"); }],
  ["click on the Comment button", async (page) => {
    await select(page, 0, 1); await settle(page); await page.click("[data-okf-comment-create]");
  }],
  ["escape the composer", async (page) => { await page.keyboard.press("Escape"); await page.evaluate(() => window.getSelection().removeAllRanges()); }],
  ["pointer on the first code block", async (page) => { await page.mouse.move(...await pointOf(page, PRE, 0, 60, 20), { steps: 5 }); }],
  ["wheel down 90 over it", async (page) => { await page.mouse.wheel(0, 90); }],
  ["pointer lower in the same block", async (page) => {
    const r = await page.locator(PRE).nth(0).boundingBox();
    await page.mouse.move(r.x + 200, r.y + r.height - 6, { steps: 10 });
  }],
  ["press the copy button", async (page) => { await page.click("[data-sphinx-preview-code-copy]"); }],
  ["pointer to a paragraph, away from code", async (page) => {
    await page.evaluate(() => window.scrollTo(0, 0)); await settle(page);
    await page.mouse.move(...await pointOf(page, P, 0, 30), { steps: 5 });
  }],
  ["wheel until a code block is under the still pointer", async (page) => { await page.mouse.wheel(0, 200); }],
  ["turn edit mode on", async (page) => {
    await page.evaluate(() => window.scrollTo(0, 0)); await settle(page);
    await page.click("[data-sphinx-preview-edit-toggle]");
  }],
  ["outline: pointer on the first paragraph", async (page) => { await page.mouse.move(...await pointOf(page, P, 0, 30)); }],
  ["outline: pointer crosses to the third paragraph in many moves", async (page) => { await page.mouse.move(...await pointOf(page, P, 2, 30), { steps: 30 }); }],
  ["outline: pointer to a list item", async (page) => { await page.mouse.move(...await pointOf(page, "#sphinx-myst-preview-content li", 1, 10), { steps: 8 }); }],
  ["outline: pointer to a table cell", async (page) => { await page.mouse.move(...await pointOf(page, "#sphinx-myst-preview-content td", 0, 8), { steps: 8 }); }],
  ["outline: pointer to the page margin", async (page) => { await page.mouse.move(2, 300, { steps: 4 }); }],
  ["outline: pointer back, then out of the window", async (page) => {
    await page.mouse.move(...await pointOf(page, P, 1, 30)); await settle(page);
    await page.evaluate(() => {
      document.querySelectorAll("#sphinx-myst-preview-content p")[1].dispatchEvent(new MouseEvent("mouseout", { bubbles: true, relatedTarget: null }));
    });
  }],
  ["outline: edit mode off", async (page) => { await page.click("[data-sphinx-preview-edit-toggle]"); }],
];

async function main() {
  setTimeout(() => { console.log("watchdog: the probe did not end in time"); process.exit(3); }, 300000).unref();
  const pages = { old: await build("old"), new: await build("new") };
  const browser = await chromium.launch();
  let differing = 0;
  try {
    for (let pass = 1; pass <= 3; pass += 1) {
      console.log(`\n=== pass ${pass}`);
      const open = {};
      for (const side of ["old", "new"]) {
        const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
        page.setDefaultTimeout(10000);
        const errors = [];
        page.on("pageerror", (e) => errors.push(e.message));
        await page.addInitScript(installShortcut);
        await page.addInitScript(() => {
          const posted = [];
          Object.assign(window, { __posted: posted, acquireVsCodeApi: () => ({ getState: () => ({}), setState: () => undefined, postMessage: (m) => { posted.push(m); } }) });
        });
        await page.goto(pathToFileURL(pages[side]).href);
        await page.waitForFunction(() => window.__posted.some((m) => m.type === "previewReady"));
        await settle(page);
        open[side] = { page, errors };
      }
      for (const [label, step] of STEPS) {
        const seen = {};
        for (const side of ["old", "new"]) {
          const { page } = open[side];
          await page.bringToFront();
          try {
            await step(page);
            await settle(page);
            seen[side] = await observe(page);
          } catch (error) {
            seen[side] = { failed: String(error.message).split("\n")[0] };
          }
        }
        const same = JSON.stringify(seen.old) === JSON.stringify(seen.new);
        if (!same) differing += 1;
        console.log(`${same ? "same" : "DIFF"} ${label}`);
        console.log(`    new ${JSON.stringify(seen.new)}`);
        if (!same) console.log(`    old ${JSON.stringify(seen.old)}`);
      }
      for (const [side, { page, errors }] of Object.entries(open)) {
        console.log(`    page errors (${side}): ${errors.length ? errors.join("; ") : "none"}`);
        await page.close();
      }
    }
  } finally {
    await browser.close();
  }
  console.log(`\n${STEPS.length * 3} step comparisons, ${differing} with a difference`);
}

main().catch((error) => { console.error(error); process.exitCode = 1; });
