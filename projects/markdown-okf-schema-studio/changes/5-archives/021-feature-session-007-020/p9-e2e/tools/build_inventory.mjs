// Read-only P9 inventory generator.
// Usage (repo root): node .agents/changes/requests/feature-session/p9-e2e/tools/build_inventory.mjs
// Reads out/test/visual/scenarios.js (compiled), out/reports/e2e/screenshots/** and the LATEST
// pointers; writes p9-e2e/inventory.md and p9-e2e/migration.md. Touches nothing else.
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { GROUPS, VISUAL, FIRST_GAP_KEEP, REAL, NO_CAPTURE } from "./decisions.mjs";
import { TO_ASSERTION_ONLY } from "./overrides.mjs";

// plan-review R1: former D/M rows that are not exact aliases become assertion-only.
for (const [id, slug] of Object.entries(TO_ASSERTION_ONLY)) {
  if (!VISUAL[id]) throw new Error(`override for unknown scenario ${id}`);
  const { note } = VISUAL[id];
  VISUAL[id] = { g: VISUAL[id].g, a: "A", s: slug, note: `was ${VISUAL[id].a}: its checks have no equal elsewhere, kept assertion-only. ${note ?? ""}`.trim() };
}

const root = process.cwd();
const here = path.join(root, ".agents/changes/requests/feature-session/p9-e2e");
const shots = path.join(root, "out/reports/e2e/screenshots");
const reports = path.join(root, "out/reports/e2e");
const require = createRequire(import.meta.url);
const { SCENARIOS } = require(path.join(root, "out/test/visual/scenarios.js"));

const GAP_CASE = {
  "23-first-paragraph": "paragraph", "17-wrapped-editing": "h1", "24-first-h2": "h2", "25-first-h3": "h3",
  "26-first-table": "table", "27-first-image": "image", "28-first-admonition": "admonition",
  "07-frontmatter": "properties", "08-okf-schema": "properties-docs",
  "09-okf-schema-missing-required": "properties-issues", "20-empty-document": "empty",
};
const groupIndex = Object.fromEntries(GROUPS.map(([id], i) => [id, i]));
const groupCode = (g) => String(groupIndex[g] + 1).padStart(2, "0");

function decision(s) {
  if (s.id.startsWith("first-element-gap-")) {
    const state = s.firstElementGapState ?? "edit";
    const slug = ["first-gap", GAP_CASE[s.fixture], state, s.firstElementGapWidth, s.toolbarState]
      .filter(Boolean).join("-");
    return { g: "layout-width", a: FIRST_GAP_KEEP.has(s.id) ? "K" : "A", s: slug, po: s.id === "first-element-gap-table-360-collapsed" };
  }
  const d = VISUAL[s.id];
  if (!d) throw new Error(`no decision for ${s.id}`);
  return d;
}

const files = fs.readdirSync(shots).filter((f) => f.endsWith(".png")).map((f) => f.slice(0, -4));
const ids = new Set(SCENARIOS.map((s) => s.id));
const secondary = {};
for (const f of files) {
  if (ids.has(f)) continue;
  const owner = [...ids].filter((id) => f.startsWith(`${id}-`)).sort((a, b) => b.length - a.length)[0];
  if (owner) (secondary[owner] ??= []).push(f.slice(owner.length + 1));
}

const editLike = (s) => Boolean(s.editMode || (s.firstElementGap && s.firstElementGapState !== "read")
  || s.editAffordances || s.editPalette || s.editPaletteTall || s.paletteModeShot || s.slashMenuShot
  || s.insertAfterFigureChecks || s.topSpacingChecks || s.listTypingChecks || s.editorKeyboardChecks || s.editActivationScroll);
const themeTok = (s) => s.previewThemeMode ?? s.theme;
const widthMode = (s) => s.widthModeBreak ?? s.tocShot ?? s.firstElementGapWidth ?? s.widthModeShot ?? (s.widthModeChecks ? "cycle" : "margin");
const palette = (s) => s.paletteModeShot ?? s.slashMenuShot?.mode ?? (editLike(s) ? "myst*" : "-");
const scroll = (s) => s.scroll.kind + (s.scroll.value !== undefined ? `:${String(s.scroll.value).slice(0, 24)}` : "") + (s.fullPage ? " full" : "");
const SKIP = new Set(["id", "fixture", "theme", "width", "height", "scroll", "description", "previewThemeMode", "fullPage", "screenshotOf", "expectedStickyHeadings", "insertAfterBlock"]);
const checks = (s) => Object.entries(s).filter(([k, v]) => !SKIP.has(k) && v !== undefined && v !== false)
  .map(([k, v]) => (k === "machineChecks" ? `mc:${v.join("+")}` : typeof v === "boolean" ? k : `${k}=${typeof v === "object" ? JSON.stringify(v) : v}`)).join(", ");
const locks = (s) => {
  const first = s.description.split(/(?<=\.)\s/)[0];
  return (first.length > 150 ? `${first.slice(0, 147)}...` : first).replaceAll("|", "/");
};

// Assign new ids per group in campaign order.
const counters = {};
const rows = SCENARIOS.map((s, index) => {
  const d = decision(s);
  let newId = "";
  if (d.a === "K" || d.a === "A") {
    counters[d.g] = (counters[d.g] ?? 0) + 1;
    newId = `${d.g}/v${String(counters[d.g]).padStart(2, "0")}-${d.s}-${themeTok(s)}-${s.width}`;
  }
  const sec = (secondary[s.id] ?? []).sort();
  const drop = new Set(d.drop ?? []);
  return { index: index + 1, s, d, newId, sec, keptSec: d.a === "K" ? sec.filter((x) => !drop.has(x)) : [], droppedSec: d.a === "K" ? sec.filter((x) => drop.has(x)) : sec };
});
for (const row of rows) if (row.d.a === "M" && !ids.has(row.d.into)) throw new Error(`bad merge target ${row.d.into}`);
const byOld = Object.fromEntries(rows.map((row) => [row.s.id, row]));

// Real-window captures.
function latestDir(pointer, pattern) {
  const p = path.join(pointer.startsWith("screenshots") ? reports : reports, pointer);
  if (!fs.existsSync(p)) return null;
  const m = fs.readFileSync(p, "utf8").match(pattern);
  return m ? path.join(pointer.includes("/") ? shots : reports, m[1]) : null;
}
const suites = {
  "real-input": latestDir("screenshots/REAL-INPUT-LATEST.md", /\]\(([^)]+)\/INDEX\.md\)/),
  checkbox: latestDir("CHECKBOX-LATEST.md", /\]\((screenshots\/[^)]+)\/INDEX\.md\)/),
  frontmatter: latestDir("FRONTMATTER-LATEST.md", /\]\((screenshots\/[^)]+)\/INDEX\.md\)/),
  scroll: latestDir("screenshots/LATEST.md", /\]\(([^)]+)\/INDEX\.md\)/),
  reload: latestDir("RELOAD-LATEST.md", /\]\((screenshots\/[^)]+)\/INDEX\.md\)/),
};
function note(dir, name) {
  const md = path.join(dir, `${name}.md`);
  const json = path.join(dir, `${name}.json`);
  if (fs.existsSync(md)) {
    const lines = fs.readFileSync(md, "utf8").split("\n").map((l) => l.trim())
      .filter((l) => l && !l.startsWith("#") && !l.startsWith("!["));
    return (lines.find((l) => l.startsWith("Expected:")) ?? lines[0] ?? "").replaceAll("|", "/");
  }
  if (fs.existsSync(json)) return (JSON.parse(fs.readFileSync(json, "utf8")).summary ?? "").replaceAll("|", "/");
  return "";
}
const realRows = [];
const realCounters = {};
for (const [suite, dir] of Object.entries(suites)) {
  if (!dir || !fs.existsSync(dir)) continue;
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".png")).sort()) {
    const name = f.slice(0, -4);
    const key = `${suite}/${name}`;
    const d = REAL[key];
    if (!d) throw new Error(`no decision for ${key}`);
    realRows.push({ key, suite, name, d, dir, note: note(dir, name) });
  }
}
for (const key of Object.keys(REAL)) if (!realRows.some((row) => row.key === key)) console.warn(`decision without capture: ${key}`);
realRows.sort((a, b) => groupIndex[a.d.g] - groupIndex[b.d.g]);
for (const row of realRows) {
  realCounters[row.d.g] = (realCounters[row.d.g] ?? 0) + 1;
  row.newId = `${row.d.g}/r${String(realCounters[row.d.g]).padStart(2, "0")}-${row.d.s}`;
}

const cut = (t, n = 160) => (t.length > n ? `${t.slice(0, n - 3)}...` : t);
const count = (pred) => rows.filter(pred).length;
const out = [];
out.push("# P9 e2e inventory (generated)", "",
  "Generated by `tools/build_inventory.mjs` from `out/test/visual/scenarios.js` (HEAD 355bf50),",
  "the last visual run in `out/reports/e2e/screenshots/` and the LATEST real-window runs.",
  "Decisions come from `tools/decisions.mjs`; reasons are in `findings.md`, targets in `plan.md`.", "",
  "Legend: action K keep, A assertion-only (no PNG), D delete, M merge into another scenario.",
  "`myst*` = default palette mode (MyST). Trust is always \"trusted, mock host\" for visual scenarios.", "",
  "## Counts", "",
  "| Item | Count |", "| --- | --- |",
  `| Visual scenarios | ${rows.length} |`,
  `| Visual aliases (\`screenshotOf\`) | ${count((r) => r.s.screenshotOf)} |`,
  `| Visual primary PNGs | ${count((r) => !r.s.screenshotOf)} |`,
  `| Visual secondary PNGs (step captures, not in the manifest) | ${rows.reduce((n, r) => n + r.sec.length, 0)} |`,
  `| Visual decisions K / A / D / M | ${count((r) => r.d.a === "K")} / ${count((r) => r.d.a === "A")} / ${count((r) => r.d.a === "D")} / ${count((r) => r.d.a === "M")} |`,
  `| Secondary PNGs kept / dropped | ${rows.reduce((n, r) => n + r.keptSec.length, 0)} / ${rows.reduce((n, r) => n + r.droppedSec.length, 0)} |`,
  `| Real-window captures (latest runs) | ${realRows.length} |`,
  `| Real-window decisions K / A | ${realRows.filter((r) => r.d.a === "K").length} / ${realRows.filter((r) => r.d.a === "A").length} |`,
  `| Integration test files without captures | ${NO_CAPTURE.length} |`, "");

out.push("## Per group after the audit (before gap filling)", "", "| Group | Visual K | Visual A | Real K | Real A |", "| --- | --- | --- | --- | --- |");
for (const [g] of GROUPS) {
  out.push(`| ${groupCode(g)} ${g} | ${count((r) => r.d.g === g && r.d.a === "K")} | ${count((r) => r.d.g === g && r.d.a === "A")} | ${realRows.filter((r) => r.d.g === g && r.d.a === "K").length} | ${realRows.filter((r) => r.d.g === g && r.d.a === "A").length} |`);
}
out.push("");

out.push("## Visual scenarios (test/visual/scenarios.ts + capture.py, mock host)", "",
  "| # | Old id | Group | Fixture | Theme/mode | Width | Edit | Width mode | Palette | Toolbar | Scroll | Checks (flags) | Locks (one line) | Secondary PNGs | README | Act |",
  "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |");
for (const r of rows) {
  const s = r.s;
  out.push(`| ${r.index} | ${s.id}${s.screenshotOf ? ` (alias of ${s.screenshotOf})` : ""} | ${r.d.g} | ${s.fixture} | ${s.theme}${s.previewThemeMode ? `/${s.previewThemeMode}` : ""} | ${s.width} | ${editLike(s) ? "edit" : "read"} | ${widthMode(s)} | ${palette(s)} | ${s.toolbarState ?? "expanded"} | ${scroll(s)} | ${checks(s) || "page checks"} | ${locks(s)} | ${r.sec.join(", ")} | ${r.d.readme ?? ""} | ${r.d.a} |`);
}
out.push("");
out.push("Every visual scenario also runs the page checks (`PAGE_CHECKS`, theme checks, toolbar, contracts,",
  "tooltip contrast, final-frame checks). Theme ids: dark = Dark Modern, light = Light Modern,",
  "fallback = no host variables; white/cream are forced preview modes.", "");

out.push("## Real-window captures (integration suites, real VS Code)", "",
  "| Suite | Capture | Group | State / behaviour (from the capture note) | README / gallery | Act |",
  "| --- | --- | --- | --- | --- | --- |");
for (const r of realRows) {
  out.push(`| ${r.suite} | ${r.name} | ${r.d.g} | ${cut(r.note)} | ${r.d.readme ?? r.d.gallery ?? ""} | ${r.d.a} |`);
}
out.push("", "Run folders: " + Object.entries(suites).map(([k, v]) => `${k} = \`${v ? path.relative(root, v) : "missing"}\``).join(", ") + ".", "");

out.push("## Integration tests without screenshots", "", "| File | Group | Locks |", "| --- | --- | --- |");
for (const [file, g, text] of NO_CAPTURE) out.push(`| test/integration/${file} | ${GROUPS[["RC", "CB", "GF", "MY", "DG", "FM", "LW", "TZ", "TN", "BE", "PS", "TE", "RA", "LS", "TS"].indexOf(g)][0]} | ${text} |`);
out.push("");

out.push("## README and docs images", "",
  "| README image | Produced from (current) | Scenario after P9 |", "| --- | --- | --- |");
const readme = [
  ...rows.filter((r) => r.d.readme).map((r) => [r.d.readme, `visual \`${r.s.id}\``, r.newId]),
  ...realRows.filter((r) => r.d.readme || r.d.gallery).map((r) => [r.d.readme ?? r.d.gallery, `real-input \`${r.name}\``, r.newId]),
];
for (const [img, from, to] of readme) out.push(`| ${img} | ${from} | \`${to}\` |`);
out.push("");
fs.writeFileSync(path.join(here, "inventory.md"), out.join("\n"));

// Migration table.
const mig = ["# P9 migration table (generated)", "",
  "Old id → new id. New visual ids are `<group>/vNN-<slug>-<theme>-<width>`, real-window ids",
  "`<group>/rNN-<slug>`. PNG paths: `out/reports/e2e/screenshots/visual/<group>/<file>.png`, step PNGs",
  "`<file>--<step>.png`. Numbers are assigned in campaign order and become permanent at the end of",
  "B2a (new scenarios take the next free number of their group). PNG location: `screenshots/visual/<group>/`.",
  "After plan-review R1 the only D/M rows are the 4 exact aliases (action M); every former D/M row",
  "with other checks is A (assertion-only), see `tools/overrides.mjs`.", "",
  "## Visual", "", "| Old id | Action | New id | Step PNGs kept | Step PNGs dropped | Note |", "| --- | --- | --- | --- | --- | --- |"];
for (const r of rows) {
  const target = r.d.a === "M" ? `→ ${byOld[r.d.into].newId}` : r.newId;
  mig.push(`| ${r.s.id} | ${r.d.a} | ${target} | ${r.keptSec.join(", ")} | ${r.droppedSec.join(", ")} | ${(r.d.note ?? r.d.fix ?? "").replaceAll("|", "/")} |`);
}
mig.push("", "## Real window", "", "| Suite / capture | Action | New id | Note |", "| --- | --- | --- | --- |");
for (const r of realRows) mig.push(`| ${r.key} | ${r.d.a} | ${r.newId} | ${(r.d.note ?? r.d.fix ?? "").replaceAll("|", "/")} |`);
mig.push("");
fs.writeFileSync(path.join(here, "migration.md"), mig.join("\n"));

console.log(JSON.stringify({
  visual: rows.length, K: count((r) => r.d.a === "K"), A: count((r) => r.d.a === "A"), D: count((r) => r.d.a === "D"), M: count((r) => r.d.a === "M"),
  primaryPng: count((r) => !r.s.screenshotOf), secondary: rows.reduce((n, r) => n + r.sec.length, 0),
  keptSec: rows.reduce((n, r) => n + r.keptSec.length, 0), real: realRows.length, realK: realRows.filter((r) => r.d.a === "K").length,
  perGroup: Object.fromEntries(GROUPS.map(([g]) => [g, [count((r) => r.d.g === g && r.d.a === "K"), count((r) => r.d.g === g && r.d.a === "A"), realRows.filter((r) => r.d.g === g && r.d.a === "K").length]])),
}));
