var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// ../../gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/517-perf-547-comment-update-and-author/work/verifier/base-tree/test/probe/perf547Document.ts
var perf547Document_exports = {};
__export(perf547Document_exports, {
  PERF547_FILE: () => PERF547_FILE,
  PERF547_SHAPE: () => PERF547_SHAPE,
  perf547Document: () => perf547Document
});
module.exports = __toCommonJS(perf547Document_exports);
var PERF547_FILE = "report.md";
var PERF547_SHAPE = {
  lines: 464,
  tables: 22,
  rows: 197,
  images: 11,
  threads: 9
};
var SEED = 547;
var BLOCKQUOTES = 21;
var SVG_WIDTH = 1100;
var SVG_HEIGHT = 560;
var SVG_BYTES = 16100;
var WORDS = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum".split(" ");
function seeded(seed) {
  let state = seed >>> 0;
  return () => {
    state = state + 1831565813 >>> 0;
    let mixed = state;
    mixed = Math.imul(mixed ^ mixed >>> 15, mixed | 1);
    mixed ^= mixed + Math.imul(mixed ^ mixed >>> 7, mixed | 61);
    return ((mixed ^ mixed >>> 14) >>> 0) / 4294967296;
  };
}
function chartSvg(number) {
  const random = seeded(SEED + number);
  const parts = [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${SVG_WIDTH}" height="${SVG_HEIGHT}" viewBox="0 0 ${SVG_WIDTH} ${SVG_HEIGHT}">`,
    `<rect x="0" y="0" width="${SVG_WIDTH}" height="${SVG_HEIGHT}" fill="#ffffff"/>`,
    `<text x="40" y="36" font-family="sans-serif" font-size="22" fill="#222222">Chart ${number} lorem ipsum dolor</text>`
  ];
  for (let grid = 0; grid <= 10; grid += 1) {
    const y = 60 + grid * 45;
    parts.push(`<line x1="70" y1="${y}" x2="1070" y2="${y}" stroke="#dddddd" stroke-width="1"/>`);
    parts.push(`<text x="30" y="${y + 4}" font-family="sans-serif" font-size="12" fill="#555555">${(10 - grid) * 10}</text>`);
  }
  const points = [];
  for (let bar = 0; parts.join("\n").length + points.length * 14 < SVG_BYTES; bar += 1) {
    const x = 80 + bar % 40 * 24.5;
    const series = Math.floor(bar / 40);
    const height = Math.round(random() * 400 * 100) / 100;
    const color = ["4477aa", "ee6677", "228833"][series % 3];
    parts.push(`<rect x="${(x + series * 6).toFixed(2)}" y="${(510 - height).toFixed(2)}" width="6.00" height="${height.toFixed(2)}" fill="#${color}" opacity="0.85"/>`);
    points.push(`${(x + 3).toFixed(1)},${(500 - height).toFixed(1)}`);
  }
  parts.push(`<polyline fill="none" stroke="#aa3377" stroke-width="2" points="${points.slice(0, 40).join(" ")}"/>`);
  parts.push("</svg>");
  return `${parts.join("\n")}
`;
}
function perf547Document() {
  const random = seeded(SEED);
  const word = () => WORDS[Math.floor(random() * WORDS.length)];
  const words = (count) => Array.from({ length: count }, word).join(" ");
  const sentence = (count) => {
    const text = words(count);
    return `${text[0].toUpperCase()}${text.slice(1)}.`;
  };
  const files = {};
  const head = [
    "---",
    "type: Reference",
    "title: Lorem ipsum performance report",
    "description: Generated equivalent of a large review document.",
    "tags: [lorem, ipsum, performance]",
    "---",
    "",
    "# Lorem ipsum performance report",
    ""
  ];
  const { tables, rows, images, threads, lines: totalLines } = PERF547_SHAPE;
  const sections = [];
  let imageCount = 0;
  for (let index = 0; index < tables; index += 1) {
    const rowCount = Math.floor(rows / tables) + (index < rows % tables ? 1 : 0);
    const block = [`## Section ${index + 1} ${words(2)}`, ""];
    const marker = `marker${index + 1}alpha beta ${words(2)}`;
    const paragraph = { offset: block.length, quote: marker };
    block.push(`${sentence(30)} The ${marker} closes this part, with **${words(2)}** and \`${word()}\` inline. ${sentence(24)}`, "");
    if (index < BLOCKQUOTES) block.push(`> ${sentence(12)} Then **${word()}** and \`${word()}\` follow.`, "");
    block.push("| Item | Owner | Status | Notes | Value |", "|------|-------|--------|-------|-------|");
    const cells = [];
    for (let row = 1; row < rowCount; row += 1) {
      const quote = `cell${index + 1}x${row} ${word()} ${word()}`;
      cells.push({ offset: block.length, quote });
      const notes = `${quote} ${words(4)} \`${word()}\` ${words(4)} **${word()}** ${words(5)} \`${word()}\` ${words(4)} **${word()}** ${words(2)} \`${word()}\``;
      block.push(`| ${words(2)} ${index + 1}.${row} \`${word()}\` | **${word()}** ${word()} | **${word()}** | ${notes} | ${Math.floor(random() * 1e5)} |`);
    }
    block.push("");
    if (imageCount < images && Math.floor(index / (tables / images)) === imageCount) {
      imageCount += 1;
      const file = `svg/chart-${String(imageCount).padStart(2, "0")}.svg`;
      files[file] = chartSvg(imageCount);
      block.push(`![Chart ${imageCount} ${words(2)}](${file})`, "");
    }
    sections.push({ block, paragraph, cells });
  }
  let missing = totalLines - head.length - sections.reduce((count, section) => count + section.block.length, 0);
  for (let index = 0; missing > 0; index = (index + 1) % tables) {
    const { block } = sections[index];
    if (missing >= 4) {
      block.push(`- ${sentence(9)}`, `- ${sentence(11)}`, `- ${sentence(8)}`, "");
      missing -= 4;
    } else if (missing >= 2) {
      block.push(sentence(24), "");
      missing -= 2;
    } else {
      block.push("");
      missing -= 1;
    }
  }
  const starts = [];
  let cursor = head.length;
  for (const section of sections) {
    starts.push(cursor);
    cursor += section.block.length;
  }
  files[PERF547_FILE] = `${[...head, ...sections.flatMap((section) => section.block)].join("\n")}
`;
  const list = Array.from({ length: threads }, (_, thread) => {
    const index = Math.floor(thread * tables / threads);
    const section = sections[index];
    const target = thread % 2 === 0 ? section.cells[thread % 4] : section.paragraph;
    const line = starts[index] + target.offset + 1;
    const createdAt = `2026-11-${String(10 + thread % 15).padStart(2, "0")}T10:00:00.000Z`;
    const comments = Array.from({ length: 1 + thread % 3 }, (_unused, reply) => ({
      id: `c_${(thread * 10 + reply + 1).toString(16).padStart(8, "0")}`,
      author: reply % 2 ? "Grace" : "Ada",
      createdAt,
      body: sentence(18)
    }));
    return {
      id: `t_${(thread + 1).toString(16).padStart(8, "0")}`,
      anchor: { line, endLine: line, quote: target.quote, prefix: "", suffix: "" },
      resolved: thread === 4,
      createdAt,
      comments
    };
  });
  files[PERF547_FILE.replace(/\.md$/u, ".comments.json")] = `${JSON.stringify({ version: 1, document: PERF547_FILE, threads: list }, null, 2)}
`;
  return files;
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  PERF547_FILE,
  PERF547_SHAPE,
  perf547Document
});
