// Transpiles the sources of <commit> that differ from the worktree into <target>/out (a copy of the build).
const fs = require("node:fs"), path = require("node:path"), { execFileSync } = require("node:child_process");
const [root, commit, target] = process.argv.slice(2);
const esbuild = require(path.join(root, "node_modules/esbuild"));
const git = (...a) => execFileSync("git", ["-C", root, ...a], { encoding: "utf8" });
for (const file of git("diff", "--name-only", commit, "--", "src").split("\n").filter(Boolean)) {
  const { code } = esbuild.transformSync(git("show", `${commit}:${file}`), { loader: "ts", format: "cjs", platform: "node", target: "es2022" });
  fs.writeFileSync(path.join(root, target, "out", file.replace(/\.ts$/u, ".js")), code);
  console.log(`${commit} ${file}`);
}
