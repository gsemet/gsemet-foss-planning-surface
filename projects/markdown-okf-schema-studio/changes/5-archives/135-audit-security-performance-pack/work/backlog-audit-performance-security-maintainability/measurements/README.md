# Measurements of the 2026-10-27 audit

All scripts ran against a copy of the repository compiled with
`npx tsc -p . --outDir <scratch>/out` (Node 25.4, macOS, Apple Silicon) with `node_modules`
symlinked next to it. Nothing in the repository was modified. Timings are medians of 5 runs after
3 warm-ups (50k lines: 3 runs after 1 warm-up; 100k lines: 1 run).

## Folders

- `render/`: `gen-doc.mjs` (synthetic MyST documents), `common.cjs` (setup), `bench-render.mjs`
  (parse, render, sanitize, mapping, anchoring), `bench-typing.mjs` (50 single-character edits),
  `one-shot.mjs` (50k and 100k single runs), `cpuprof-summary.mjs` (top self-time functions of a
  `.cpuprofile`), `bundle-meta.mjs` (esbuild metafile by package), `vscode-stub.cjs` +
  `bench-activation.cjs` + `act2.cjs` (require time of the bundle with a Proxy `vscode` stub),
  `bench-sanitizer.mjs` + `bench-sanitizer2.mjs` (sanitizer stress), `results.md` (raw tables).
- `leaks/`: `churn.js` (opens and closes N previews with the memory host, counts subscriptions,
  watchers and timers, reports heap; `node --expose-gc churn.js 50 6 10`), `whosubs.js` (stack
  trace of the leaking subscriptions).
- `security-probes/`: `probe1.js` to `probe3.js` (payloads against `renderMyst`,
  `buildPreviewWebviewHtml` and `classifyPreviewReference`).
- `modularity/`: `graph.mjs` and `graph-value.mjs` (import graph, fan-in/out, strongly connected
  components, with and without `import type` edges), `dead.mjs` (exports referenced nowhere else).

## Raw numbers not in `render/results.md`

### CPU profile, 50k-line document (2 renders + 1 parse, 10.4 s of samples)

| self ms | share | function | file |
|---|---|---|---|
| 5058 | 48.6% | `computeBlockTightness` | `node_modules/markdown-it-myst/dist/directives.js:6` |
| 1307 | 12.6% | `visit` | `unist-util-visit-parents/lib/index.js:178` |
| 528 | 5.1% | `detachNode` | `parse5/dist/tree-adapters/default.js:81` |
| 500 | 4.8% | garbage collector | |
| 304 | 2.9% | `count` | `unist-util-select/lib/walk.js:283` |
| 168 | 1.6% | `all` | `unist-util-select/lib/walk.js:108` |
| 96 | 0.9% | `one` | `unist-util-select/lib/walk.js:73` |
| 87 | 0.8% | `factory` | `unist-util-visit-parents/lib/index.js:155` |
| 64 | 0.6% | `getNodeOrLiftedChildren` | `myst-common/dist/utils.js:106` |

`computeBlockTightness` does `src.split('\n')` of the whole source once per directive fence
(`{note}`, `{figure}`, `{code-block}`, `{mermaid}`...), so parsing is O(directives x size).

### Sanitizer stress (`rewriteSphinxHtml`)

| case | result |
|---|---|
| 2.8 MB, 48k flat elements | 145 ms |
| same + nested lists depth 500 | 125 ms (depth 500 alone: 1 ms) |
| 100 columns of divs nested 500 deep | 104 ms |
| `<ul>` nested 5,000 deep | `RangeError: Maximum call stack size exceeded` |
| 50k unknown tags + blocked images | 39.2 s |
| unknown tags 5k / 10k / 20k | 109 ms / 382 ms / 1,260 ms (quadratic) |
| `<script>` 5k / 20k | 46 ms / 687 ms |

Cause of the quadratic case: `removeNode` (`src/core/security/html-sanitizer.ts:262-266`)
filters `parent.childNodes` for every removed sibling.

### Bundles (esbuild metafile, minified, KB)

- `extension.js` 1,798: own source 453, katex 263, parse5 125, highlight.js 118, ajv 117,
  yaml 112, entities 101, he 85, csv-parse 51, markdown-it 51, js-yaml 44, json5 29,
  myst-directives 28, myst-parser 26. Shipped with a 6.5 MB source map that embeds
  `sourcesContent` (700 sources).
- `preview.js` 301 (all own source); `preview.css` 145.
- `mermaidPreview.js` 5,141 (shipped 5,265): mermaid 1,671, elkjs 1,446, @mermaid-js/parser 645,
  cytoscape 440, katex 267 (second copy).
- `plantumlPreview.js` 3,441: @plantuml/core 3,350.

### Activation

`require()` of the shipped bundle with a Proxy `vscode` stub: 47-54 ms, heap +8.5 MB,
rss +33-37 MB. `activate()` itself was not measured (the stub throws on
`workspace.workspaceFolders`).

### Preview churn with the memory host (`leaks/churn.js 50 6 10`)

| point | heapUsed | live subscriptions | watchers | timers |
|---|---|---|---|---|
| baseline (engine warm) | 25.9 MB | 3 | 0 | 0 |
| round 1, 50 previews open | 58.7 MB (about 0.66 MB per session) | 503 | 100 | 0 |
| round 1 closed | 26.5 MB | 153 | 0 | 0 |
| round 6 closed | 27.7 MB | 903 | 0 | 0 |

Sessions are collected (a `WeakRef` to the first session clears after each round); no timer or
watcher survives a close; the +150 subscriptions per round come from
`CommentsController.watchSidecar` (`src/session/features/comments.ts:356-358`), whose three
`onDid*` disposables are discarded. Heap growth with edits (about 235 KB per round) is the memory
host's own `applied` log; without edits the heap is flat over 8 rounds (+0.39 MB).

### npm audit

`npm audit --offline --json` returns zero findings, which is meaningless offline (no advisory
database). An online audit was not run (audit constraint). 502 lock entries, 245 non-dev, all
resolved on registry.npmjs.org with integrity hashes.
