# Before and after: CR-343

Before: base `main` c698ac97d5b09c1d173ea02d2c0d58ead7be27b9. After: pushed head
d99d2ef94b5ec2dd80f33ded348f031ecefa1aa5.

| Pair | Shows | Reproduce |
|---|---|---|
| `css-base-c698ac9.txt` / `css-head-d99d2ef.txt` | `EDIT_MODE_CSS` + `CONTENT_BLOCK_CSS` as produced: 56557 bytes each, sha256 b205abda...3793 for both, `cmp` equal | `git archive c698ac97 src` into a scratch folder; bundle `work/verifier/css_entry.ts` with `esbuild --bundle --platform=node --packages=external --alias:SRC=<src>` once per tree; run each with `node` and compare |

No screenshot pair: the PR changes no visual output (requirement text, markers, tests, CSS split
with identical produced CSS).
