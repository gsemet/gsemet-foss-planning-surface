// usage: import { genDoc } ; genDoc(lines) -> string
export function genDoc(n) {
  const out = [];
  out.push("---");
  out.push("title: Synthetic benchmark document");
  for (let i = 0; out.length < 150; i++) out.push(`key_${i}: value number ${i}`);
  out.push("---", "");
  const langs = { python: "def f(x):\n    return x * 2\n\nprint(f(3))", ts: "export const f = (x: number): number => x * 2;\nconsole.log(f(3));", bash: "set -e\nfor i in 1 2 3; do echo $i; done", json: '{\n  "a": 1,\n  "b": [1, 2, 3]\n}' };
  const langKeys = Object.keys(langs);
  const mer = Math.max(1, Math.min(20, Math.floor(n / 50))), pu = Math.min(5, mer);
  const merEvery = Math.floor(n / mer), puEvery = Math.floor(n / pu), cmEvery = Math.floor(n / 100);
  let sec = 0, k = 0;
  const rnd = (() => { let s = 42; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 2 ** 32; })();
  while (out.length < n) {
    const L = out.length;
    if (L % 40 < 1) { out.push(`## Section ${sec++}`, ""); }
    if (L > 0 && L % merEvery < 8 && L / merEvery < mer) { out.push("```{mermaid}", "graph TD", "  A[Start] --> B{Choice}", "  B --> C[One]", "  B --> D[Two]", "```", ""); continue; }
    if (L % puEvery < 8 && L / puEvery < pu && L > 0) { out.push("```plantuml", "@startuml", "Alice -> Bob: hi", "Bob --> Alice: ok", "@enduml", "```", ""); continue; }
    if (L % cmEvery < 3 && L > 160) { out.push(k++ % 2 ? "<!-- TODO fix this paragraph -->" : "<!-- THREAD\nAda (2026-10-16 10:47):\n  please check\n-->", ""); continue; }
    const r = rnd();
    if (r < 0.15) { const l = langKeys[k++ % 4]; out.push("```" + l, langs[l], "```", ""); }
    else if (r < 0.17 && n >= 1000 && out.length % 2000 < 40) { out.push("| " + Array.from({ length: 8 }, (_, c) => `H${c}`).join(" | ") + " |", "|" + " --- |".repeat(8)); for (let row = 0; row < 200; row++) out.push("| " + Array.from({ length: 8 }, (_, c) => `r${row}c${c}`).join(" | ") + " |"); out.push(""); }
    else if (r < 0.22) out.push("![](img.png)", "");
    else if (r < 0.27) out.push(":::{note}", `Note body ${k++} with **bold**.`, ":::", "");
    else if (r < 0.30) out.push("```{figure} img.png", ":name: fig-" + k++, "", "Caption text", "```", "");
    else if (r < 0.33) out.push("```{code-block} python", ":linenos:", "print('hi')", "```", "");
    else if (r < 0.37) out.push(`Inline math $a^2+b^2=c^2$ and ${k++}.`, "", "$$", "\\int_0^1 x^2 dx = 1/3", "$$", "");
    else if (r < 0.45) out.push(`### Heading ${k++}`, "");
    else out.push(`Paragraph ${k++} with *emphasis*, **strong**, \`code\` and [a link](https://example.com/${k}) plus more text to fill the line.`, "");
  }
  return out.join("\n") + "\n";
}
if (process.argv[1]?.endsWith("gen-doc.mjs")) { const t = performance.now(); const d = genDoc(+process.argv[2] || 1000); console.log(d.length, "chars", (performance.now() - t).toFixed(0), "ms"); }
