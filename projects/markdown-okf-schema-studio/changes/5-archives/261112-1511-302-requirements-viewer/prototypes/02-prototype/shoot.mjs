// Shoot every card page of <site>/cards/ as a 1200x630 PNG into <site>/og/.
// node shoot.mjs <site_dir> <node_modules_dir holding playwright-core>
import { createRequire } from "node:module";
import { readdirSync, mkdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const [site, modules] = process.argv.slice(2).map((p) => resolve(p));
const { chromium } = createRequire(join(modules, "x.js"))("playwright-core");
mkdirSync(join(site, "og"), { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
for (const name of readdirSync(join(site, "cards")).filter((f) => f.endsWith(".html"))) {
  await page.goto(pathToFileURL(join(site, "cards", name)).href);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: join(site, "og", name.replace(/\.html$/, ".png")) });
  console.log("og/" + name.replace(/\.html$/, ".png"));
}
await browser.close();
