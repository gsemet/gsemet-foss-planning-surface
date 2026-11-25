/**
 * Scratch probe (not committed): shoots the chart-style candidates.
 * `node out/test/probe/vegaCandidates.js <folder> <A|B|C>`.
 */
import * as fs from "node:fs";
import * as path from "node:path";

import { openChartPage } from "../page/chartPage";

const LINE = {
  title: "Monthly active users by plan",
  width: 520,
  height: 220,
  data: { values: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"].flatMap((month, index) => [
    { month, plan: "Free", users: 120 + index * 18 },
    { month, plan: "Team", users: 60 + index * 11 + (index % 2) * 6 },
    { month, plan: "Enterprise", users: 25 + index * 7 },
  ]) },
  mark: { type: "line", point: true },
  encoding: {
    x: { field: "month", type: "ordinal", sort: null, title: "Month" },
    y: { field: "users", type: "quantitative", title: "Active users (thousands)" },
    color: { field: "plan", type: "nominal", title: "Plan", sort: ["Free", "Team", "Enterprise"] },
  },
};

const BAR = {
  title: { text: "Revenue by quarter and product", subtitle: "Grouped bars, in k$" },
  width: 520,
  height: 220,
  data: { values: ["Q1", "Q2", "Q3", "Q4"].flatMap((quarter, index) => [
    { quarter, product: "Editor", revenue: 40 + index * 9 },
    { quarter, product: "Viewer", revenue: 28 + index * 5 },
    { quarter, product: "Cloud sync", revenue: 15 + index * 12 },
  ]) },
  mark: "bar",
  encoding: {
    x: { field: "quarter", type: "nominal", title: "Quarter" },
    xOffset: { field: "product", sort: ["Editor", "Viewer", "Cloud sync"] },
    y: { field: "revenue", type: "quantitative", title: "Revenue (k$)" },
    color: { field: "product", type: "nominal", title: "Product", sort: ["Editor", "Viewer", "Cloud sync"] },
    tooltip: [{ field: "quarter", title: "Quarter" }, { field: "product", title: "Product" }, { field: "revenue", title: "Revenue (k$)" }],
  },
};

const VEGA = {
  width: 480,
  height: 200,
  padding: 5,
  title: { text: "Build time per pipeline stage" },
  data: [{ name: "table", values: [
    { run: 1, stage: "compile", seconds: 42 }, { run: 2, stage: "compile", seconds: 38 }, { run: 3, stage: "compile", seconds: 45 }, { run: 4, stage: "compile", seconds: 36 }, { run: 5, stage: "compile", seconds: 33 },
    { run: 1, stage: "test", seconds: 80 }, { run: 2, stage: "test", seconds: 92 }, { run: 3, stage: "test", seconds: 76 }, { run: 4, stage: "test", seconds: 70 }, { run: 5, stage: "test", seconds: 74 },
    { run: 1, stage: "package", seconds: 20 }, { run: 2, stage: "package", seconds: 22 }, { run: 3, stage: "package", seconds: 19 }, { run: 4, stage: "package", seconds: 25 }, { run: 5, stage: "package", seconds: 21 },
  ] }],
  scales: [
    { name: "x", type: "linear", domain: { data: "table", field: "run" }, range: "width", nice: false, zero: false },
    { name: "y", type: "linear", domain: { data: "table", field: "seconds" }, range: "height", nice: true, zero: true },
    { name: "color", type: "ordinal", domain: { data: "table", field: "stage" }, range: "category" },
  ],
  axes: [
    { orient: "bottom", scale: "x", title: "Pipeline run", tickCount: 5 },
    { orient: "left", scale: "y", title: "Duration (s)", grid: true },
  ],
  legends: [{ stroke: "color", title: "Stage", symbolType: "stroke" }],
  marks: [{
    type: "group",
    from: { facet: { name: "series", data: "table", groupby: "stage" } },
    marks: [{
      type: "line",
      from: { data: "series" },
      encode: { enter: { x: { scale: "x", field: "run" }, y: { scale: "y", field: "seconds" }, stroke: { scale: "color", field: "stage" }, strokeWidth: { value: 2 } } },
    }],
  }],
};

const MARKDOWN = [
  "# Chart style candidates",
  "",
  "A Vega-Lite line chart with three series and a colour legend:",
  "",
  "```vega-lite", JSON.stringify(LINE, null, 2), "```",
  "",
  "A Vega-Lite grouped bar chart with a legend:",
  "",
  "```vega-lite", JSON.stringify(BAR, null, 2), "```",
  "",
  "A full Vega chart with a legend and axis titles:",
  "",
  "```vega", JSON.stringify(VEGA, null, 2), "```",
  "",
].join("\n");

const THEMES: Array<[string, string, string | undefined]> = [["cream", "light", "cream"], ["dark", "dark", undefined], ["light", "light", undefined]];

async function shoot(folder: string, candidate: string, label: string, theme: string, mode: string | undefined, hover: boolean): Promise<Record<string, unknown>> {
  const opened = await openChartPage(MARKDOWN, {}, theme, mode);
  if (!opened) throw new Error("no Chromium can start here");
  try {
    const { page } = opened;
    await page.setViewportSize({ width: 820, height: 1000 });
    await page.waitForFunction(() => document.querySelectorAll(".myst-vega-diagram[data-render-state='rendered']").length === 3, undefined, { timeout: 30_000 });
    // The theme variables are set after load: wait until the drawings settle on the last theme.
    await page.waitForTimeout(1500);
    const measured = await page.evaluate(() => {
      const paragraph = document.querySelector("p");
      return {
        body: getComputedStyle(document.body).fontSize,
        paragraph: paragraph ? getComputedStyle(paragraph).fontSize : "",
        font: getComputedStyle(document.body).getPropertyValue("--sphinx-preview-font").trim(),
        background: getComputedStyle(document.body).backgroundColor,
        errors: document.querySelectorAll(".myst-vega-diagram[data-render-state='error']").length,
        images: [...document.querySelectorAll<HTMLImageElement>(".myst-vega-image")].map((image) => `${image.naturalWidth}x${image.naturalHeight} shown ${image.width}x${image.height}`),
      };
    });
    if (hover) {
      await page.evaluate(() => {
        const image = document.querySelectorAll<HTMLImageElement>(".myst-vega-image")[1]!;
        const svgText = decodeURIComponent(image.src.slice(image.src.indexOf(",") + 1));
        const holder = document.createElement("div");
        const box = image.getBoundingClientRect();
        holder.style.cssText = `position:absolute;left:${box.left + window.scrollX}px;top:${box.top + window.scrollY}px;visibility:hidden;`;
        const svg = new DOMParser().parseFromString(svgText, "image/svg+xml").documentElement;
        holder.appendChild(document.importNode(svg, true));
        document.body.appendChild(holder);
        const bars = [...holder.querySelectorAll<SVGPathElement>("g.mark-rect.role-mark path")];
        // The Q3 "Cloud sync" bar: the 9th bar in data order.
        const bar = bars[8] ?? bars[0]!;
        const barBox = bar.getBoundingClientRect();
        const scale = image.width / image.naturalWidth;
        const aria = bar.getAttribute("aria-label") ?? "";
        holder.remove();
        const style = getComputedStyle(document.body);
        const svgRoot = new DOMParser().parseFromString(svgText, "image/svg+xml");
        const labelNode = svgRoot.querySelector("g.role-axis-label text");
        const labelFontSize = labelNode?.getAttribute("font-size") ?? "10px";
        const gridNode = svgRoot.querySelector("g.role-axis-grid path, g.role-axis-domain path");
        const font = style.getPropertyValue("--sphinx-preview-font").trim() || "sans-serif";
        const grid = style.getPropertyValue("--sphinx-preview-border").trim() || gridNode?.getAttribute("stroke") || "#ccc";
        // The bar's own fields (its aria-label repeats the xOffset field in lower case): the tooltip encoding, in order.
        const rows = ["Quarter: Q3", "Product: Cloud sync", "Revenue (k$): 39"];
        void aria;
        const tip = document.createElement("div");
        tip.style.cssText = [
          "position:absolute",
          `left:${box.left + window.scrollX + (barBox.left - box.left) * scale + (barBox.width * scale) / 2 + 10}px`,
          `top:${box.top + window.scrollY + (barBox.top - box.top) * scale - 8}px`,
          `background:${style.backgroundColor}`,
          `color:${style.color}`,
          `font-family:${font}`,
          `font-size:${labelFontSize}`,
          "line-height:1.45",
          `border:1px solid ${grid}`,
          "border-radius:4px",
          "padding:6px 9px",
          "box-shadow:0 2px 6px rgba(0,0,0,0.18)",
          "white-space:nowrap",
          "z-index:10",
        ].join(";");
        for (const row of rows) {
          const line = document.createElement("div");
          const [key, ...rest] = row.split(":");
          const strong = document.createElement("span");
          strong.style.opacity = "0.75";
          strong.textContent = `${key}: `;
          line.append(strong, document.createTextNode(rest.join(":").trim()));
          tip.appendChild(line);
        }
        document.body.appendChild(tip);
      });
    }
    const height = await page.evaluate(() => Math.ceil([...document.querySelectorAll(".myst-vega-figure")].at(-1)!.getBoundingClientRect().bottom + window.scrollY) + 28);
    const name = `${candidate}-${label}${hover ? "-hover" : ""}.png`;
    await page.screenshot({ path: path.join(folder, name), fullPage: true, clip: { x: 0, y: 0, width: 820, height } });
    const violations = await page.evaluate(() => (window as unknown as { __violations: string[] }).__violations);
    return { name, ...measured, violations, problems: opened.problems };
  } finally {
    await opened.close();
  }
}

async function main(): Promise<void> {
  const folder = path.resolve(process.argv[2] ?? "vega-candidates");
  const candidate = process.argv[3] ?? "A";
  fs.mkdirSync(folder, { recursive: true });
  for (const [label, theme, mode] of THEMES) {
    console.log(JSON.stringify(await shoot(folder, candidate, label, theme, mode, false)));
    if (candidate !== "A" && label !== "light") console.log(JSON.stringify(await shoot(folder, candidate, label, theme, mode, true)));
  }
}

void main().catch((error: unknown) => { console.error(error); process.exitCode = 1; });
