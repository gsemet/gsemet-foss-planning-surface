// Compares the site built at the head with the site built at the base, from one reports artifact.
// Usage: node compare-sites.mjs <head worktree> <base worktree>
import fs from "node:fs";
import path from "node:path";

const [head, base] = process.argv.slice(2);
const read = (root) => fs.readFileSync(path.join(root, "out/site/gallery.html"), "utf8");
const walk = (dir, prefix = "") => fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
  e.isDirectory() ? walk(path.join(dir, e.name), `${prefix}${e.name}/`) : [`${prefix}${e.name}`]);

const headHtml = read(head);
const baseHtml = read(base);

const openers = [...headHtml.matchAll(/<a class="capture-open" href="([^"]*)" data-capture-id="([^"]*)"/g)];
const ids = openers.map((m) => m[2]);
const figures = [...headHtml.matchAll(/<figure data-capture-id="([^"]*)">/g)].map((m) => m[1]);
const shotRoot = path.join(head, "out/reports/e2e/screenshots");
const shots = walk(shotRoot).filter((f) => /\.(png|jpe?g|webp)$/i.test(f));
console.log("screenshot files:", shots.length);
console.log("openers:", openers.length, "data-capture-id on openers:", ids.length, "unique:", new Set(ids).size);
console.log("figures with an id:", figures.length, "same ids and order as openers:", JSON.stringify(figures) === JSON.stringify(ids));
console.log("all data-capture-id attributes:", (headHtml.match(/ data-capture-id="/g) ?? []).length);
console.log("ids by shape: real-window registry", ids.filter((i) => /^[^/]+\/r\d+-/.test(i)).length,
  "visual", ids.filter((i) => /^[^/]+\/v\d+-/.test(i)).length,
  "other", ids.filter((i) => !/^[^/]+\/[rv]\d+-/.test(i)).length);
console.log("ids with a run folder prefix or a ~:", ids.filter((i) => /-e2e-|real-input-|~/.test(i)));
console.log("ids of other shapes:", ids.filter((i) => !/^[^/]+\/[rv]\d+-/.test(i)).slice(0, 12));

const parts = (html, re) => [...html.matchAll(re)].map((m) => m[1]);
for (const [label, re] of [
  ["image src, in order", /<img loading="lazy" src="([^"]*)"/g],
  ["captions", /<figcaption>([\s\S]*?)<\/figcaption>/g],
  ["sidecar templates", /<template class="capture-sidecar">([\s\S]*?)<\/template>/g],
  ["viewer dialog", /(<dialog class="capture-viewer"[\s\S]*?<\/dialog>)/g],
  ["social card meta", /(<meta (?:property|name)="(?:og|twitter):[^>]*>)/g],
  ["title", /(<title>[^<]*<\/title>)/g],
  ["site header", /(<header class="site[\s\S]*?<\/header>|<nav[^>]*class="site[\s\S]*?<\/nav>)/g],
]) {
  const a = parts(headHtml, re);
  const b = parts(baseHtml, re);
  console.log(`${label}: base ${b.length}, head ${a.length}, identical: ${JSON.stringify(a) === JSON.stringify(b)}`);
}
console.log("head title:", parts(headHtml, /<title>([^<]*)<\/title>/g)[0]);
console.log("base has data-capture-id:", baseHtml.includes("data-capture-id"), "base has pushState:", baseHtml.includes("pushState"));

const headFiles = new Set(walk(path.join(head, "out/site")));
const baseFiles = new Set(walk(path.join(base, "out/site")));
const onlyBase = [...baseFiles].filter((f) => !headFiles.has(f));
const onlyHead = [...headFiles].filter((f) => !baseFiles.has(f));
console.log("site files: base", baseFiles.size, "head", headFiles.size);
console.log("only in base:", onlyBase.length, onlyBase.slice(0, 15));
console.log("only in head:", onlyHead.length, onlyHead.slice(0, 15));
for (const prefix of ["reports/e2e/screenshots/", "reports/e2e/gallery/"]) {
  const a = [...headFiles].filter((f) => f.startsWith(prefix));
  const b = [...baseFiles].filter((f) => f.startsWith(prefix));
  const same = a.length === b.length && b.every((f) => headFiles.has(f) &&
    fs.readFileSync(path.join(head, "out/site", f)).equals(fs.readFileSync(path.join(base, "out/site", f))));
  console.log(`${prefix}: base ${b.length}, head ${a.length}, same paths and bytes: ${same}`);
}
