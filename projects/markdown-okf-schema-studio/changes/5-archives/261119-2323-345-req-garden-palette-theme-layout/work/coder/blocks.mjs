import { markerBlocks } from "file:///C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-06-CR-345/scripts/check-marker-companions.mjs";
import { readFileSync } from "node:fs";
const min = Number(process.env.MIN ?? 0);
for (const f of process.argv.slice(2)) {
  const t = readFileSync(f, "utf8");
  for (const b of markerBlocks(t)) { if (b.ids.size > min) console.log(`${f}:${b.first}-${b.last} (${b.ids.size}) ` + [...b.ids].map(i=>i.replace("MDOKFSTUDIO-","").replace("SwRS-","")).join(" ")); }
}
