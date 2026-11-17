#!/usr/bin/env node
// P10 helper (read-only on the repo). Checks tools/scope-map.json against the git-tracked files
// of src/, test/ and sphinx/: every src/ file in exactly one scope, every test file in one scope
// or in "tooling", no listed path missing. With --config, prints the `scopes:` block of
// requirements/config.yml. Usage (from the repo root):
//   node .agents/changes/requests/059-requirements-okfreq/tools/scope-map.mjs <repo-root> [--config]
// The repo root defaults to the current directory (CR 059: the refactor worktree wt-059).
import { execFileSync } from "node:child_process";
import { readFileSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2).filter((a) => !a.startsWith("--"));
const repo = path.resolve(args[0] ?? process.cwd());
const map = JSON.parse(readFileSync(path.join(here, "scope-map.json"), "utf8"));

const tracked = execFileSync("git", ["ls-files", "src", "test", "sphinx"], { cwd: repo, encoding: "utf8" })
  .split("\n").filter(Boolean)
  .filter((f) => !/\.(png|jpe?g|gif|webp|pyc)$/i.test(f) && !f.includes("__pycache__"));

const owners = new Map();
const add = (file, owner) => owners.set(file, [...(owners.get(file) ?? []), owner]);
const problems = [];
for (const scope of map.scopes) {
  for (const f of [...scope.src, ...scope.test]) {
    if (!existsSync(path.join(repo, f))) problems.push(`missing path in ${scope.id}: ${f}`);
  }
}
const prefixOwners = [];
for (const scope of map.scopes) for (const f of [...scope.src, ...scope.test]) (f.endsWith("/") ? prefixOwners.push([f, scope.id]) : add(f, scope.id));
for (const f of map.tooling) prefixOwners.push([f, "tooling"]);
for (const file of tracked) {
  const exact = owners.get(file) ?? [];
  const byPrefix = prefixOwners.filter(([p]) => p.endsWith("/") ? file.startsWith(p) : file === p).map(([, o]) => o);
  const all = [...exact, ...byPrefix];
  if (all.length === 0) problems.push(`unmapped: ${file}`);
  else if (all.length > 1) problems.push(`mapped ${all.length} times (${all.join(", ")}): ${file}`);
}

if (process.argv.includes("--config")) {
  const list = (items) => items.length === 0 ? "[]" : `\n${items.map((i) => `      - ${i}`).join("\n")}`;
  console.log("scopes:");
  for (const s of map.scopes) {
    console.log(`  ${s.id}:\n    id_token: ${s.id_token}\n    folder: ${s.id}\n    source_dirs: ${list(s.src)}\n    test_dirs: ${list(s.test)}`);
  }
} else {
  for (const s of map.scopes) console.log(`${s.id.padEnd(20)} ${s.id_token.padEnd(9)} src=${String(s.src.length).padStart(2)} test=${String(s.test.length).padStart(2)}`);
  console.log(`tracked files checked: ${tracked.length}`);
  console.log(problems.length ? problems.join("\n") : "OK: every tracked src/test/sphinx file maps to exactly one scope or tooling");
  process.exitCode = problems.length ? 1 : 0;
}
