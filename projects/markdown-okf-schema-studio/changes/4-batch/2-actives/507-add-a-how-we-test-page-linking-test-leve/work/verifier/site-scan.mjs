// Usage: node site-scan.mjs <out/site folder>
// Scan of the built site for the spec's evidence item 3. Reads only; exit 1 on any problem.
import fs from "node:fs";
import path from "node:path";

const site = path.resolve(process.argv[2]);
const problems = [];
const read = (file) => fs.readFileSync(path.join(site, file), "utf8");
const page = "docs/how-we-test.html";

if (!fs.existsSync(path.join(site, page))) {
  console.log(`${page}: missing`);
  process.exit(1);
}
const html = read(page);
const main = /<main>([\s\S]*?)<\/main>/u.exec(html)?.[1] ?? "";
const headings = [...main.matchAll(/<h([1-6])\b[^>]*>([\s\S]*?)<\/h\1>/gu)].map((m) => `h${m[1]} ${m[2].replace(/<[^>]+>/gu, "")}`);
console.log(`title: ${/<title>([^<]*)<\/title>/u.exec(html)?.[1]}`);
console.log(`headings: ${headings.length}`);
for (const heading of headings) console.log(`  ${heading}`);
const tables = [...main.matchAll(/<table\b[\s\S]*?<\/table>/gu)].map((m) => m[0]);
console.log(`tables: ${tables.length}`);
for (const table of tables) {
  const rows = [...table.matchAll(/<tr\b[\s\S]*?<\/tr>/gu)].map((m) =>
    [...m[0].matchAll(/<t[hd]\b[^>]*>([\s\S]*?)<\/t[hd]>/gu)].map((c) => c[1].replace(/<[^>]+>/gu, "").trim()),
  );
  console.log(`  rows (header included): ${rows.length}`);
  for (const row of rows) console.log(`    ${row[0]} | cells ${row.length}`);
}
const images = [...main.matchAll(/<img\b[^>]*>/gu)].map((m) => m[0]);
for (const image of images) {
  const src = /\ssrc="([^"]*)"/u.exec(image)?.[1];
  const alt = /\salt="([^"]*)"/u.exec(image)?.[1];
  console.log(`image: src=${src} alt length=${alt?.length}`);
}
const diagram = images.map((image) => /\ssrc="([^"]*)"/u.exec(image)?.[1]).filter((src) => src === "../images/how-we-test/test-levels.svg");
if (diagram.length !== 1) problems.push(`diagram image shown ${diagram.length} times`);
if (!fs.existsSync(path.join(site, "images/how-we-test/test-levels.svg"))) problems.push("diagram file missing in the site");
else console.log("diagram file in the site: yes");

// every relative href and src of the whole page resolves inside the site
const targets = [...html.matchAll(/<[a-zA-Z][^>]*?\s(href|src)="([^"]*)"/gu)].map((m) => ({ attr: m[1], target: m[2] }));
let relative = 0;
const unique = new Set();
let mainRelative = 0;
const mainTargets = [...main.matchAll(/<[a-zA-Z][^>]*?\s(href|src)="([^"]*)"/gu)].map((m) => m[2]);
const isRelative = (t) => !/^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/iu.test(t);
for (const { attr, target } of targets) {
  if (!isRelative(target)) continue;
  relative += 1;
  unique.add(target);
  if (target.startsWith("/")) {
    problems.push(`${attr} ${target}: root-absolute`);
    continue;
  }
  const file = decodeURIComponent(target.replace(/[?#].*$/u, ""));
  let resolved = path.resolve(site, path.dirname(page), file);
  if (resolved !== site && !resolved.startsWith(site + path.sep)) problems.push(`${attr} ${target}: leaves the site`);
  else if (!fs.existsSync(resolved)) problems.push(`${attr} ${target}: does not exist`);
  else if (fs.statSync(resolved).isDirectory() && !fs.existsSync(path.join(resolved, "index.html"))) problems.push(`${attr} ${target}: folder without index.html`);
}
for (const target of mainTargets) if (isRelative(target)) mainRelative += 1;
console.log(`relative href and src: ${relative} in the whole page (${unique.size} unique), ${mainRelative} inside <main>`);
for (const target of mainTargets.filter(isRelative)) console.log(`  main: ${target}`);
const absolute = mainTargets.filter((t) => /^https?:/iu.test(t));
console.log(`absolute URLs inside <main>: ${absolute.length}`);
for (const target of absolute) console.log(`  ${target}`);

// anchors inside the page
const ids = new Set([...html.matchAll(/\sid="([^"]*)"/gu)].map((m) => m[1]));
for (const target of mainTargets.filter((t) => t.startsWith("#"))) {
  if (!ids.has(target.slice(1))) problems.push(`anchor ${target}: no such id`);
}

const expected = "Home, Contributing, How we ship, How we test, Gallery, Requirements";
const viewerPage = (() => {
  const walk = (folder) => {
    for (const entry of fs.readdirSync(path.join(site, folder), { withFileTypes: true })) {
      const child = `${folder}/${entry.name}`;
      if (entry.isDirectory()) {
        const found = walk(child);
        if (found) return found;
      } else if (/SwRS-MDOKFSTUDIO-CORE-086\.html$/iu.test(entry.name)) return child;
    }
    return undefined;
  };
  return walk("requirements");
})();
const headerPages = ["index.html", "docs/how-we-ship.html", page, "requirements/index.html", viewerPage].filter(Boolean);
for (const file of headerPages) {
  const nav = /<nav class="site"[^>]*>([\s\S]*?)<\/nav>/u.exec(read(file))?.[1] ?? "";
  const links = [...nav.matchAll(/<a\b[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gu)].map((m) => ({ href: m[1], text: m[2].replace(/<[^>]+>/gu, "") }));
  const names = links.map((l) => l.text).join(", ");
  console.log(`header of ${file}: ${names}`);
  console.log(`  hrefs: ${links.map((l) => l.href).join(" ")}`);
  if (names !== expected) problems.push(`header of ${file}: ${names}`);
  for (const { href } of links) {
    let resolved = path.resolve(site, path.dirname(file), href);
    if (!fs.existsSync(resolved)) problems.push(`header of ${file}: ${href} does not exist`);
  }
}
if (!viewerPage) console.log("no requirements page of CORE-086 found by file name");

// every page of the site that has a site header carries the six links
let withHeader = 0;
const wrong = [];
const walkAll = (folder) => {
  for (const entry of fs.readdirSync(path.join(site, folder), { withFileTypes: true })) {
    const child = folder === "." ? entry.name : `${folder}/${entry.name}`;
    if (entry.isDirectory()) walkAll(child);
    else if (entry.name.endsWith(".html")) {
      const nav = /<nav class="site"[^>]*>([\s\S]*?)<\/nav>/u.exec(read(child))?.[1];
      if (nav === undefined) continue;
      withHeader += 1;
      const names = [...nav.matchAll(/<a\b[^>]*>([\s\S]*?)<\/a>/gu)].map((m) => m[1].replace(/<[^>]+>/gu, "")).join(", ");
      if (names !== expected) wrong.push(`${child}: ${names}`);
    }
  }
};
walkAll(".");
console.log(`pages with a site header: ${withHeader}, without the six links in order: ${wrong.length}`);
for (const line of wrong.slice(0, 10)) problems.push(line);

const manifest = JSON.parse(read("site-manifest.json"));
const inPages = JSON.stringify(manifest.pages).includes("docs/how-we-test.html");
const inCards = JSON.stringify(manifest.cards).includes("og/how-we-test.png");
console.log(`manifest pages lists docs/how-we-test.html: ${inPages}; cards lists og/how-we-test.png: ${inCards}`);
if (!inPages) problems.push("manifest pages lacks the page");
if (!inCards) problems.push("manifest cards lacks the picture");
const picture = path.join(site, "og/how-we-test.png");
if (!fs.existsSync(picture)) problems.push("og/how-we-test.png missing");
else {
  const bytes = fs.readFileSync(picture);
  console.log(`og/how-we-test.png: ${bytes.length} bytes, ${bytes.readUInt32BE(16)}x${bytes.readUInt32BE(20)}`);
}

console.log(`problems: ${problems.length}`);
for (const problem of problems) console.log(`  ${problem}`);
process.exit(problems.length === 0 ? 0 : 1);
