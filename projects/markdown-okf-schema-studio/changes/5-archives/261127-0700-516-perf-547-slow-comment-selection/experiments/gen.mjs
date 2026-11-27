// Deterministic generator of an OKF bundle equivalent in shape to issue 547 (own content; no download).
// usage: node gen.mjs <outDir>
import fs from "node:fs";
import path from "node:path";

const out = path.resolve(process.argv[2] ?? "bundle");

function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const WORDS = ("lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore "
  + "magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis "
  + "aute irure in reprehenderit voluptate velit esse cillum eu fugiat nulla pariatur excepteur sint occaecat cupidatat non "
  + "proident sunt culpa qui officia deserunt mollit anim id est laborum").split(" ");

function chartSvg(n, random) {
  const W = 1100, H = 560;
  const parts = [`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">`,
    `<rect x="0" y="0" width="${W}" height="${H}" fill="#ffffff"/>`,
    `<text x="40" y="36" font-family="sans-serif" font-size="22" fill="#222222">Chart ${n} lorem ipsum dolor</text>`];
  for (let g = 0; g <= 10; g += 1) {
    const y = 60 + g * 45;
    parts.push(`<line x1="70" y1="${y}" x2="1070" y2="${y}" stroke="#dddddd" stroke-width="1"/>`);
    parts.push(`<text x="30" y="${y + 4}" font-family="sans-serif" font-size="12" fill="#555555">${(10 - g) * 10}</text>`);
  }
  const points = [];
  for (let i = 0; Buffer.byteLength(parts.join("\n")) + points.length * 14 < 16100; i += 1) {
    const x = 80 + (i % 40) * 24.5;
    const h = Math.round(random() * 400 * 100) / 100;
    parts.push(`<rect x="${(x + Math.floor(i / 40) * 6).toFixed(2)}" y="${(510 - h).toFixed(2)}" width="6.00" height="${h.toFixed(2)}" fill="#${["4477aa", "ee6677", "228833"][Math.floor(i / 40) % 3]}" opacity="0.85"/>`);
    points.push(`${(x + 3).toFixed(1)},${(500 - h).toFixed(1)}`);
  }
  parts.push(`<polyline fill="none" stroke="#aa3377" stroke-width="2" points="${points.slice(0, 40).join(" ")}"/>`);
  parts.push("</svg>");
  return `${parts.join("\n")}\n`;
}

/**
 * Builds a document. rowsOf(i) gives the number of rendered table rows (header + body) of table i.
 */
function build({ name, sections, tableRows, images, totalLines, threads, tables = true, inlineSvg = false, flat = false, seed = 547 }) {
  const random = rng(seed);
  const word = () => WORDS[Math.floor(random() * WORDS.length)];
  const words = (count) => Array.from({ length: count }, word).join(" ");
  const sentence = (count) => { const s = words(count); return `${s[0].toUpperCase()}${s.slice(1)}.`; };
  const dir = path.join(out, name);
  fs.mkdirSync(path.join(dir, "svg"), { recursive: true });
  const lines = ["---", "type: Reference", "title: Lorem ipsum performance report", "description: Generated equivalent of a large review document.",
    "tags: [lorem, ipsum, performance]", "---", "", "# Lorem ipsum performance report", ""];
  const marks = { cells: [], paragraphs: [] };
  const rowCounts = [];
  const base = Math.floor(tableRows / sections), extra = tableRows - base * sections;
  for (let i = 0; i < sections; i += 1) rowCounts.push(base + (i < extra ? 1 : 0));
  const imageEvery = images > 0 ? sections / images : 0;
  let imageCount = 0;
  const svgs = [];
  // Padding paragraphs: spread so that the total line count matches totalLines.
  const perSection = [];
  for (let i = 0; i < sections; i += 1) {
    const block = [`## Section ${i + 1} ${words(2)}`, ""];
    const marker = `marker${i + 1}alpha beta ${words(2)}`;
    block.push(`${sentence(30)} The ${marker} closes this part, with **${words(2)}** and \`${word()}\` inline. ${sentence(24)}`, "");
    marks.paragraphs.push({ section: i, offset: 2, quote: marker });
    const rows = [];
    rows.push("| Item | Owner | Status | Notes | Value |");
    rows.push("|------|-------|--------|-------|-------|");
    for (let r = 1; r < rowCounts[i]; r += 1) {
      const cellMark = `cell${i + 1}x${r} ${word()} ${word()}`;
      rows.push(`| ${words(2)} ${i + 1}.${r} | ${words(2)} | **${word()}** | ${cellMark} ${words(18)} | ${Math.floor(random() * 100000)} |`);
      marks.cells.push({ section: i, row: r, offset: block.length + rows.length - 1, quote: cellMark });
    }
    if (flat) block.push(...rows.filter((_, k) => k !== 1).map((row) => `- ${row.split("|").map((c) => c.trim()).filter(Boolean).join(" ")}`), "", "");
    else if (tables) block.push(...rows, "");
    if (images > 0 && imageCount < images && Math.floor(i / imageEvery) === imageCount) {
      imageCount += 1;
      const svg = chartSvg(imageCount, rng(seed + imageCount));
      svgs.push(svg);
      if (inlineSvg) block.push("```svg", ...svg.trimEnd().split("\n"), "```", "");
      else {
        const file = `svg/chart-${String(imageCount).padStart(2, "0")}.svg`;
        fs.writeFileSync(path.join(dir, file), svg);
        block.push(`![Chart ${imageCount} ${words(2)}](${file})`, "");
      }
    }
    perSection.push(block);
  }
  const fixed = lines.length + perSection.reduce((n, b) => n + b.length, 0);
  // Reference line count: the image variant. Variants without tables or images keep the same padding.
  const referenceExtra = (tables ? 0 : rowCounts.reduce((n, r) => n + r + 2, 0)) + (images === 0 ? 0 : 0);
  let missing = totalLines === undefined ? 0 : Math.max(0, totalLines - fixed - referenceExtra);
  for (let i = 0; missing > 0; i = (i + 1) % sections) {
    if (missing >= 4) {
      perSection[i].push(`- ${sentence(9)}`, `- ${sentence(11)}`, `- ${sentence(8)}`, "");
      missing -= 4;
    } else if (missing >= 2) {
      perSection[i].push(sentence(24), "");
      missing -= 2;
    } else {
      perSection[i].push("");
      missing -= 1;
    }
  }
  const absolute = [];
  let cursor = lines.length;
  for (const block of perSection) { absolute.push(cursor); cursor += block.length; }
  let text = `${[...lines, ...perSection.flat()].join("\n")}\n`;
  fs.writeFileSync(path.join(dir, "report.md"), text);
  // Comment threads: sidecar format of src/core/comments/commentModel.ts (version 1).
  const list = [];
  for (let t = 0; t < threads; t += 1) {
    const section = Math.floor((t * sections) / Math.max(1, threads));
    const inCell = tables && t % 2 === 0;
    const target = inCell
      ? marks.cells.find((c) => c.section === section && c.row === 1 + (t % 4)) ?? marks.cells.find((c) => c.section === section)
      : marks.paragraphs[section];
    const line = absolute[section] + target.offset + 1 - (flat && inCell ? 1 : 0);
    const createdAt = `2026-11-${String(10 + (t % 15)).padStart(2, "0")}T10:00:00.000Z`;
    const comments = Array.from({ length: 1 + (t % 3) }, (_, k) => ({
      id: `c_${(t * 10 + k + 1).toString(16).padStart(8, "0")}`, author: k % 2 ? "Grace" : "Ada", createdAt, body: sentence(18),
    }));
    list.push({ id: `t_${(t + 1).toString(16).padStart(8, "0")}`, anchor: { line, endLine: line, quote: target.quote, prefix: "", suffix: "" }, resolved: t === 4, createdAt, comments });
  }
  fs.writeFileSync(path.join(dir, "report.comments.json"), `${JSON.stringify({ version: 1, document: "report.md", threads: list }, null, 2)}\n`);
  const stats = {
    name, lines: text.split("\n").length - 1, bytes: Buffer.byteLength(text),
    tables: tables ? sections : 0, tableRows: tables ? tableRows : 0,
    tableSourceLines: text.split("\n").filter((l) => l.startsWith("|")).length,
    images: inlineSvg ? 0 : imageCount, inlineSvgs: inlineSvg ? imageCount : 0,
    svgBytes: svgs.map((s) => Buffer.byteLength(s)), threads: list.length, cellThreads: list.filter((_, t) => tables && !flat && t % 2 === 0).length,
  };
  return stats;
}

const full = { sections: 22, tableRows: 197, images: 11, totalLines: 464, threads: 9 };
const stats = [
  build({ name: "full", ...full }),
  build({ name: "nothreads", ...full, threads: 0 }),
  build({ name: "nosvg", ...full, images: 0 }),
  build({ name: "notables", ...full, tables: false }),
  build({ name: "flat", ...full, flat: true }),
  build({ name: "small", sections: 2, tableRows: 10, images: 1, totalLines: 45, threads: 1 }),
  build({ name: "xl4", sections: 88, tableRows: 788, images: 44, totalLines: 1840, threads: 36 }),
  build({ name: "inlinesvg", ...full, totalLines: undefined, inlineSvg: true }),
];
fs.writeFileSync(path.join(out, "stats.json"), JSON.stringify(stats, null, 2));
for (const s of stats) console.log(JSON.stringify({ ...s, svgBytes: s.svgBytes.length ? `${Math.min(...s.svgBytes)}-${Math.max(...s.svgBytes)}` : "-" }));
