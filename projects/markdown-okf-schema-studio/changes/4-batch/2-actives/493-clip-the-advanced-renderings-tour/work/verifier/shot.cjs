// Verifier throwaway: renders the editing page (base and head sources) with the head's compiled renderer
// and the site's clip-to-video step, then screenshots the "MyST rendering" bullet.
// Usage: node shot.cjs <head worktree> <base worktree> <output folder>
const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");
const { pathToFileURL } = require("node:url");

const [head, base, outDir] = process.argv.slice(2);
const req = createRequire(path.join(head, "package.json"));
const { renderMyst } = req("./out/src/core/render/mystRenderer");
const { clipVideos } = req("./out/test/site/siteClips");
const { chromium } = req("playwright-core");

(async () => {
  const browser = await chromium.launch();
  for (const [name, root] of [["before", base], ["after", head]]) {
    const source = fs.readFileSync(path.join(root, "docs", "user", "editing.md"), "utf8");
    const rendered = await renderMyst(source);
    const html = clipVideos(rendered.html, "docs/user/editing.md", (p) => fs.existsSync(path.join(root, p)));
    const videos = (html.match(/<video [^>]*advanced-renderings-tour\.webm/g) || []).length;
    console.log(`${name}: renderings tour video elements = ${videos}`);
    const baseHref = pathToFileURL(path.join(root, "docs", "user") + path.sep).href;
    const file = path.join(outDir, "..", "..", "scratch", `verifier-page-${name}.html`);
    fs.writeFileSync(file, `<!doctype html><meta charset="utf-8"><base href="${baseHref}"><style>body{font:15px sans-serif;margin:16px;max-width:860px;background:#fff;color:#222}img,video{max-width:100%;display:block;margin:8px 0;border:1px solid #ccc}</style>${html}`);
    const page = await browser.newPage({ viewport: { width: 900, height: 900 } });
    await page.goto(pathToFileURL(file).href);
    const item = page.locator("li", { hasText: "MyST rendering" }).first();
    await item.scrollIntoViewIfNeeded();
    const state = await page.evaluate(async () => {
      const video = document.querySelector('video[src*="advanced-renderings-tour"]');
      if (!video) return null;
      if (video.readyState < 2) await new Promise((done) => video.addEventListener("loadeddata", done, { once: true }));
      video.pause();
      await new Promise((done) => { video.addEventListener("seeked", done, { once: true }); video.currentTime = 1.5; });
      video.removeAttribute("controls");
      await new Promise((done) => requestAnimationFrame(() => requestAnimationFrame(done)));
      return { width: video.videoWidth, height: video.videoHeight, duration: video.duration };
    });
    console.log(`${name}: video = ${JSON.stringify(state)}`);
    await item.screenshot({ path: path.join(outDir, `editing-page-${name}.png`) });
    await page.close();
  }
  await browser.close();
})().catch((error) => { console.error(error); process.exit(1); });
