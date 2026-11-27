// Usage: node probe-prime.js <worktree>   (needs `just compile` output in <worktree>/out)
const wt = process.argv[2];
const fs = require("fs"), os = require("os"), path = require("path");
const { createPreviewResourcePolicy } = require(path.join(wt, "out/src/core/security/resource-policy.js"));
const { createNodeFileSystem } = require(path.join(wt, "out/src/node-services/nodeFileSystem.js"));
(async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "probe-"));
  fs.writeFileSync(path.join(dir, "a.png"), "x");
  const policy = createPreviewResourcePolicy(createNodeFileSystem(), dir, dir, false);
  // visual harness: no prime before the first sanitizer pass
  console.log("pass 1 (no prior prime):", policy.resolvePrimed("a.png", dir, { image: true }));
  console.log("takeUnprimed after pass 1:", JSON.stringify(policy.takeUnprimed()));
  await policy.prime([{ request: "a.png", baseDirectory: dir, options: { image: true } }]);
  console.log("after explicit prime:", policy.resolvePrimed("a.png", dir, { image: true }));
  fs.rmSync(dir, { recursive: true, force: true });
})();
