# CR-426 before and after

Before: technique of the evidence plan (spec, "Evidence"), the busy-wait alone with only
`setTimeout` mocked. It is not taken at the bare base 82c11a472250b6b808476ec797c2106481ddbd15:
that base has no busy-wait, so its tests fail only under a rare load and give no reproducible
before. The before is the pushed head cc3a627e2b09ebb998854b46f735d122c3f97cc0 with `"Date"`
removed from the two changed mocks in the compiled, git-ignored file
`out/test/node-services/build/buildQueue.test.js` (lines 94 and 126), then restored by
recompiling. No detached worktree was needed.

After: the pushed head cc3a627e2b09ebb998854b46f735d122c3f97cc0, unchanged.

| Pair | Shows | Reproduce |
| --- | --- | --- |
| `../before-busywait-setTimeout-only.log` | 10 pass, 2 fail: "retains a successful result as stale after a failed newer build" at `assert.ok(pending.has(2))`; "still renders a build whose buffer already moved on, and cleans up on dispose" with `false !== true` | `fnm exec -- npm run compile`; in the compiled file, replace `["setTimeout", "Date"]` by `["setTimeout"]` on lines 94 and 126; `fnm exec -- node --test out/test/node-services/build/buildQueue.test.js` |
| `../after-20-runs.log` | 20 passes in a row of the whole file (12 tests each) | `fnm exec -- npm run compile`; `for i in $(seq 20); do fnm exec -- node --test out/test/node-services/build/buildQueue.test.js > /dev/null 2>&1 \|\| break; echo "run $i pass"; done` |

The raw logs stay in `work/verifier/` (they hold local paths). No screenshot or video: the
change is a unit test.
