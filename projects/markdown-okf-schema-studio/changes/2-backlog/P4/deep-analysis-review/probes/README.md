# Probes

Diagnostic scripts used by the [deep analysis review](../00-index.md) and by [plan.md](../plan.md)
to measure findings before and after each fix. They only read the compiled modules; they never
modify the extension.

Run every probe from `src/markdown-okf-schema-studio` after `fnm exec -- npm run compile`.
Set `OUT=/path/to/out/src` to target another compilation.

| Probe | Finding | Command | Baseline at `e1b4ad0` | Target |
| --- | --- | --- | --- | --- |
| `frontmatter-fence.cjs` | STAB-01 | `node $P/frontmatter-fence.cjs` | `allKeysExtracted: false`, `editIsSingleLineChange: false` | both `true` |
| `ajv-cache.cjs` | PERF-12 | `node --expose-gc $P/ajv-cache.cjs` | 1,523 cache entries, +13.4 MB per 500 | 1–5 entries, under 1 MB |
| `include-fanout.mjs` | SEC-05 | `node $P/include-fanout.mjs 5` | 111,110 reads, about 16 s | reads within budget, under 1 s |
| `crlf-alerts.mjs` | STAB-07 | `node $P/crlf-alerts.mjs` | `crlfAdmonition: false` | `true` |
| `plantuml-epipe.cjs` | STAB-04 | `node $P/plantuml-epipe.cjs` | `uncaughtExceptions: 1` | `0` |
| `render-cost.mjs` | PERF-01, PERF-02 | `node $P/render-cost.mjs` | about 85 ms per render (Node 25.4, arm64) | lower; 0 ms on the host after PERF-01 |

`P` stands for `../../.agents/changes/requests/deep-analysis-review/probes`.
After the HAST refactor (plan task T17) some stages of `render-cost.mjs` are reported as `missing`;
adapt the probe to the new module names rather than the code.
