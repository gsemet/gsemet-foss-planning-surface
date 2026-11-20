// Runs `node <args...>` from the current folder, prints how long it took and how it ended, and,
// when it has not exited after <seconds>, ends it and its whole process tree by its own PID
// (Windows: `taskkill /PID <pid> /T /F`; elsewhere: the process group). Never by name.
// Usage (from the worktree): node <this file> <seconds> <node args...>
// Example: node .../timed-run.mjs 120 --import ./scripts/register-myst-patches.mjs --test out/test/page/tableBreakout.test.js
import { spawn, spawnSync } from "node:child_process";

const [limitText, ...args] = process.argv.slice(2);
const limit = Number(limitText);
if (!Number.isFinite(limit) || limit <= 0 || args.length === 0) {
  console.error("usage: node timed-run.mjs <seconds> <node args...>");
  process.exit(2);
}
const started = Date.now();
const child = spawn(process.execPath, args, { stdio: "inherit", detached: process.platform !== "win32" });
let timedOut = false;
const timer = setTimeout(() => {
  timedOut = true;
  console.log(`\n[timed-run] still running after ${limit} s: ending PID ${child.pid} and its tree`);
  if (process.platform === "win32") spawnSync("taskkill", ["/PID", String(child.pid), "/T", "/F"], { stdio: "inherit" });
  else process.kill(-child.pid, "SIGKILL");
}, limit * 1000);
child.on("exit", (code, signal) => {
  clearTimeout(timer);
  const seconds = ((Date.now() - started) / 1000).toFixed(1);
  console.log(`[timed-run] ${timedOut ? "HUNG: ended by timed-run" : "exited by itself"} after ${seconds} s, code ${code}, signal ${signal}`);
  process.exit(timedOut ? 124 : code ?? 1);
});
