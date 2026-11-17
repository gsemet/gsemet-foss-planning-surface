// STAB-01 probe: frontmatter values ending with "..." must not truncate the block or corrupt edits.
// Run from src/markdown-okf-schema-studio after `npm run compile`.
const path = require("node:path");
const out = path.resolve(process.env.OUT ?? "out/src");
const { extractFrontmatter, createFrontmatterFieldPatch } = require(`${out}/frontmatter/okfFrontmatter.js`);
const source = "---\ntitle: To be continued...\nauthor: Ada\nstatus: draft\n---\n# Body\n";
const keys = Object.keys(extractFrontmatter(source).frontmatter ?? {});
const patch = createFrontmatterFieldPatch(source, "status", "done");
const edited = patch ? source.slice(0, patch.start) + patch.text + source.slice(patch.end) : undefined;
const expected = "---\ntitle: To be continued...\nauthor: Ada\nstatus: done\n---\n# Body\n";
console.log(JSON.stringify({
  probe: "frontmatter-fence",
  extractedKeys: keys,
  allKeysExtracted: ["title", "author", "status"].every((key) => keys.includes(key)),
  editIsSingleLineChange: edited === expected,
  edited,
}));
