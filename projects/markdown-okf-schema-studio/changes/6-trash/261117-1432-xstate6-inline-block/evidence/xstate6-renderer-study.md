# Study: rendering an `xstate-json` block (XState v6 machine JSON) in Studio

Date: 2026-11-17. Scope: read-only feasibility study, no change in the product repository.
Fixed decisions (02-answers.md): the block holds machine JSON only (`machineToJSON` output), no code
runs; fence `xstate-json`; the rendering engine and every runtime dependency it ships in the VSIX are
MIT.

## Conclusion and recommendation

The block is feasible without changing the webview CSP, but **no existing statechart renderer meets
the strict-MIT rule**, and **the existing Mermaid path does not meet it either**: Mermaid itself is
MIT, but what it ships for a state diagram includes d3 (ISC), DOMPurify (MPL-2.0 OR Apache-2.0) and,
in Mermaid 12, the ELK layout (elkjs, EPL-2.0) that state diagrams use by default. Every ready-made
viewer found is either non-MIT (Graphviz-based: Apache-2.0 / EPL; ELK-based: EPL-2.0; ISC), tied to a
UI framework (React, Vue), archived, or not a library. **Recommendation: write Studio's own renderer
(Studio's own MIT code) with one MIT runtime dependency, `@dagrejs/dagre` 3.1.3 (with its bundled
`@dagrejs/graphlib` 4.0.6, both MIT, LICENSE files checked, 49 KB minified / 17 KB gzip, no eval, no
wasm, no worker).** A pure-TS model in `src/core` reads the JSON tolerantly (not the strict
`machineFromJSON` loader, which rejects keys that `machineToJSON` itself emits), resolves targets,
and a page bundle `xstatePreview.js` lays out each composite state bottom-up with dagre and draws a
themed SVG picture, wired exactly like the Vega chart block (lazy bundle, cache, error in place,
export). Effort: large (about the size of the Vega integration plus a layout/drawing module). If the
owner accepts Mermaid's already-shipped dependencies as outside the rule, a **JSON to Mermaid
`stateDiagram-v2` converter** is the cheapest first step (small to medium, no new dependency) but it
cannot draw history states nor transitions between states of different composite states, and shows
guards, delays and actions only as label text. Either way: XState v6 is beta (beta.3, 2026-11-15) and
the JSON API was renamed one month ago, so the parser must be tolerant and the fixtures pinned to a
version; a v6 machine written in the idiomatic style (transitions as functions) loses its targets in
JSON, which caps what any renderer can draw.

## Comparison of candidates

License = license of the package and of every runtime dependency it would ship. "Strict MIT" is the
owner's rule. Size = minified browser JS unless noted. CSP fit = works under Studio's current CSP
(no `unsafe-eval`, no `wasm-unsafe-eval`, `worker-src 'none'`, `connect-src 'none'`).

| Candidate | License (runtime closure) | Strict MIT | Size | Statechart coverage | CSP fit | Maintenance | Effort |
|---|---|---|---|---|---|---|---|
| **Own renderer + `@dagrejs/dagre` 3.1.3** (recommended) | Studio MIT + dagre MIT + graphlib MIT (bundled) | Yes | dagre.min.js 49 KB (17 KB gz) incl. graphlib; own code est. 30-60 KB | Full: what we draw (nested, parallel, history, final, guards, after, always, invoke, tags, `@code`) | Yes (pure JS, SVG data image) | dagre 3.1.3, 2026-10-24, active (5.9k stars) | Large |
| Own renderer, zero dependency (nested boxes, transitions as rows, Stately Sketch style) | Studio MIT | Yes | est. 15-30 KB | Full as text; no arrows | Yes | Ours | Medium |
| JSON to Mermaid `stateDiagram-v2` (existing Mermaid 12.2.0 path) | mermaid MIT, but d3 ISC, dompurify MPL-2.0/Apache-2.0, elkjs EPL-2.0 (default state layout), dagre-d3-es MIT | **No** | 0 new; already lazy-loaded chunks (state ~80 KB + shared ~280 KB + ELK 1.5 MB in Studio's bundle) | Partial: no history, no cross-composite transitions, guards/after/actions as text | Yes (already used) | mermaid 12.3.0, 2026-11-11 | Small-Medium |
| state-machine-cat 15.0.12 | MIT, but `@hpcc-js/wasm-graphviz` Apache-2.0 for SVG | **No** | 199 KB unpacked + Graphviz wasm (~2 MB unpacked) | Good (composite, parallel, history, choice, fork) but its own smcat/SCXML input | **No** (WebAssembly needs `wasm-unsafe-eval`) | Active, 2026-11-15 | Medium + CSP change |
| Graphviz: `@hpcc-js/wasm(-graphviz)`, `d3-graphviz`, `@viz-js/viz` | Apache-2.0; BSD-3-Clause; viz-js says MIT but embeds Graphviz (EPL, UNVERIFIED) and has no LICENSE file in the package | **No** | 2-37 MB unpacked | Clusters, no statechart semantics | **No** (wasm) | Active | Medium + CSP change |
| elkjs 0.12.1 (alone or via cytoscape-elk, xstate-viz, xstate-diagram) | EPL-2.0 OR GPL-3.0-or-later | **No** | ~1.5 MB | Best compound layout | Yes (bundled build, no worker) - UNVERIFIED for 0.12 | Active | Medium |
| cytoscape 3.35.0 (+ cytoscape-dagre) | MIT (cytoscape-dagre bundles old dagre, MIT) | Yes | ~400 KB min (5.8 MB unpacked) | Compound nodes; canvas rendering, no SVG export | Yes | Active | Large, poor fit (canvas, force layouts) |
| React Flow / xyflow (`@xyflow/react` 13, `@xyflow/system` 1.0) | MIT, but needs React and d3-* (ISC) | **No** | 1.3 MB + React | None by itself (no layout engine) | Yes | Active | Large, wrong fit |
| xstate-viz (statelyai) | MIT; React 17, Next, Chakra, elkjs EPL | **No** | app | XState v4 | n/a | **Archived** 2023 | n/a |
| Stately Sketch (statelyai/sketch) | MIT app; React, TanStack, Tailwind; evaluates code with `new Function` | Not a library (not on npm) | app | v5 code/JSON/YAML/Mermaid; nested boxes | No (eval) | Active (2026-07) | Design reference only |
| `@statelyai/graph` 2.6.0 | MIT; layouts are optional peers (elkjs, dagre, graphviz, cytoscape) | Yes alone | 1.3 MB unpacked | Graph data + algorithms, no drawing | Yes | Active | Not needed |
| `@xstate/graph` 3.0.4 / `xstate/graph` (in v6 core) | MIT, zero deps | Yes | xstate 149 KB + graph 38 KB (UMD min) | Resolved node/edge graph, no drawing | Yes (no eval in dist) | v6 beta | Optional helper; see 2.6 |
| xstate-diagram 0.2.1 | ISC; elkjs EPL; xstate v5; no LICENSE file in package | **No** | 770 KB unpacked | v5 machines | UNVERIFIED | 3 stars, created 2026-11-11 | n/a |
| `@statewalker/fsm-charts` 0.2.9 | MIT (vendored dagre; lodash injected, MIT) | Yes | 475 KB dist | Own HFSM format, no parallel/history (UNVERIFIED) | UNVERIFIED | 0 stars, one maintainer | Adapter + risk |
| statechart-kit 0.15.1 | MIT; Vue 3 peer; `@tinyactors/scxmljs` dev build | No (Vue, prerelease dep) | 1.6 MB | SCXML editor | UNVERIFIED | New (2026-11-11) | n/a |
| libavoid-js (edge routing) | LGPL-2.1-or-later | **No** | 1 MB | Routing only | wasm | Active | n/a |

## 1. The XState v6 JSON format

Evidence: `xstate@6.0.0-beta.3` (npm dist-tag `beta`, published 2026-11-15; `latest` is still
5.33.4), packed with `--ignore-scripts`; LICENSE: "The MIT License (MIT) Copyright (c) 2015 David
Khourshid"; `package.json` has no `dependencies`. Files read: `dist/declarations/src/serialize.d.ts`,
`dist/declarations/src/machineFromJSON.d.ts`, `docs/serialization.md`, `docs/api-stability.json`,
`dist/xstate.esm.js`; JSON Schema `packages/core/src/machine.schema.json` on GitHub.

### 1.1 Structure

`machineToJSON(machine): MachineJSON` returns the machine's config copied as data
(`machine._json` if the machine came from JSON, else `machineConfigToJSON(machine.config)`). The
shape (`StateNodeJSON`, recursive through `states`) has these keys:

- **Identity and kind**: `id`, `key`, `type` (`atomic | compound | parallel | final | history |
  choice`), `initial` (child key), `states` (map of child state nodes; a literal dot in a key is
  escaped `\.`). `type` is present only if the author wrote it: a renderer infers compound (has
  `states`) and atomic.
- **Transitions**: `on` (event to transition or array), `after` (delay key, e.g. `"1000"` or a named
  delay, to transition), `always` (eventless), `onError`, `timeout` + `onTimeout` (new in v6),
  `choice` (v6 choice states: branches `{ when, target, ... }`), `route`. A transition
  (`TransitionJSON`) is `{ target?: string | string[], guard?, actions?, context?, description?,
  reenter?, meta?, matches?, input? }`. Targets use XState's syntax: sibling key, `.child`, `#id`,
  `#id.path`.
- **History**: `type: "history"`, `history: "shallow" | "deep"`, `target` (required by the schema
  and the loader).
- **Final**: `type: "final"`, `output`.
- **Actions**: `entry`, `exit`, transition `actions`: built-ins `@xstate.raise`, `@xstate.emit`,
  `@xstate.assign`, `@xstate.cancel`, `@xstate.log`, or custom `{ type, params }`.
- **Guards**: `{ type, params? }` references; built-ins `@xstate.not` and `@xstate.stateIn`.
- **Invoke**: `{ id?, src: string, input?, onDone?, onError?, onSnapshot?, timeout?, onTimeout? }`.
  Inline actor logic cannot be named, so "the whole `invoke` is dropped when its `src` cannot be
  named" (docs/serialization.md).
- **Spawn**: `enq.spawn(...)` happens inside transition functions; it has no JSON representation of
  its own (only inside `@code` text). "Some v6 features have no JSON representation yet: state
  `input`, `enq.listen`/`enq.subscribeTo`, and `choice` functions." (docs/serialization.md)
- **Documentation fields**: `description`, `meta`, `tags`.
- **Machine-only keys**: `version` (requires `id`), `context`, `@exprLang`, `actions`, `guards`,
  `actors`, `delays`, `schemas`, `internalEvents`.

### 1.2 What is lost for function transitions

In v6 a transition may be a plain function returning `{ target, context }` and enqueuing effects
(blog post). `machineConfigToJSON` turns every function into a code expression,
`{ "@code": fn.toString(), "@lang": "ts" }` (`codeExpression` in `dist/xstate.esm.js`). So for a
function transition **the target, the guard logic and the effects are only in a source string**: a
diagram can show "event E leaves state S" but not where it goes. `xstate/graph`'s
`toDirectedGraph` reports this as a `dynamic-target` diagnostic (`DirectedGraphDiagnostic` in
`graph/types.d.ts`). Root `actions`/`guards`/`actors`/`delays` whose values are functions are
omitted ("Named source keys are not preserved when their values are functions"). Class instances,
`Date`, `bigint`, `symbol`, runtime (Zod) schemas are omitted.

Consequence: a machine written in idiomatic v6 style (function transitions) yields a diagram of
states with dangling event stubs. Object transitions (`{ target, guard: { type } }`) render fully.
Reading `target: '...'` literals out of the `@code` text would be a heuristic static parse, never an
execution (open question).

### 1.3 Stability, versioning, schema

- `docs/api-stability.json` (beta.3) marks `machineToJSON`, `machineFromJSON`, `MachineJSON`,
  `StateNodeJSON`, `TransitionJSON`, `ActionJSON`, `GuardJSON`, `InvokeJSON` as `"public"`;
  `getMachineSerializationDiagnostics` and `MachineSerializationDiagnostic` as `"experimental"`.
- Blog: "We consider the core API stable, and we only plan to make breaking changes before the stable
  release if overwhelming feedback shows that we need to."
- Churn evidence: commit "Make v6 names consistent before beta (#5800)", 2026-10-17: "serializeMachine/
  createMachineFromConfig are machineToJSON/machineFromJSON". Built-in guard keys moved to the
  `@xstate.` prefix in the same commit.
- **The JSON has no format version field.** `version` is the author's machine version (for snapshot
  migration), not the format's. Only the persisted *snapshot* envelope is declared stable across 6.x
  (docs/persistence.md).
- **JSON Schema**: `packages/core/src/machine.schema.json` (draft-07, title "XState v6 machine
  definition (MachineJSON)", 11.5 KB) exists in the repository at tag `xstate@6.0.0-beta.3` and on
  `next` (default branch), but is **not shipped in the npm package**. The state node object allows
  additional properties.
- **Inconsistency found** (static reading, beta.3): the strict loader
  (`stateNodeJSONKeys` in `dist/xstate.esm.js`, "Unknown key ... at ...") does not list `onDone`, and
  `StateNodeJSON` has no `onDone`, but state-level `onDone` is a v6 feature (docs/final-states.md;
  `TRANSITION_KEYS = ['onDone', ...]` in the runtime) and `machineConfigToJSON` copies config keys
  verbatim. So `machineToJSON` of a code machine with a state `onDone` would produce JSON that
  `machineFromJSON` rejects. Running it to confirm was not possible in this study (executing the
  downloaded package was refused): UNVERIFIED at runtime. It argues for a tolerant reader.

### 1.4 Minimal example

````markdown
```xstate-json
{
  "id": "toggle",
  "initial": "off",
  "states": {
    "off": { "on": { "TOGGLE": { "target": "on" } } },
    "on":  { "on": { "TOGGLE": { "target": "off" } } }
  }
}
```
````

### 1.5 Rich example (hand-written to the beta.3 types; not produced by running `machineToJSON`)

```json
{
  "id": "checkout",
  "version": "1.0.0",
  "initial": "cart",
  "context": { "items": 0 },
  "states": {
    "cart": {
      "description": "The shopper edits the cart.",
      "tags": ["editable"],
      "on": {
        "ADD": { "actions": [{ "type": "@xstate.assign", "context": { "items": 1 } }] },
        "CHECKOUT": [
          { "target": "payment", "guard": { "type": "hasItems" } },
          { "target": "cart", "description": "An empty cart stays." }
        ]
      }
    },
    "payment": {
      "type": "parallel",
      "states": {
        "card": {
          "initial": "entering",
          "states": {
            "entering": { "on": { "SUBMIT": { "target": "validating" } } },
            "validating": {
              "invoke": { "src": "validateCard", "onDone": { "target": "valid" }, "onError": { "target": "entering" } }
            },
            "valid": { "type": "final" },
            "hist": { "type": "history", "history": "deep", "target": "entering" }
          }
        },
        "address": {
          "initial": "editing",
          "states": {
            "editing": { "on": { "CONFIRM": { "target": "confirmed" } } },
            "confirmed": { "type": "final" }
          }
        }
      },
      "after": { "600000": { "target": "#checkout.timedOut" } },
      "on": { "BACK": { "target": "cart" } }
    },
    "review": {
      "always": [{ "target": "placed", "guard": { "type": "@xstate.stateIn", "params": { "stateId": "#checkout.payment" } } }],
      "on": { "EDIT": { "@code": "({ event }) => ({ target: event.where })", "@lang": "ts" } }
    },
    "placed": { "type": "final", "output": { "ok": true } },
    "timedOut": { "type": "final", "meta": { "reason": "inactivity" } }
  }
}
```

It exercises: initial, nested and parallel states, deep history, final states with output, guarded
transitions with a fallback, an assign action, invoke with onDone/onError, a delayed transition to a
`#id` target across the hierarchy, an eventless guarded transition, a function transition
(`@code`, target unknown), tags, description and meta. (`payment` has no `onDone` here on purpose, see
1.3.)

## 2. Candidate renderers

Studio's webview CSP (`src/core/security/csp.ts`, `createContentSecurityPolicy`, SwRS TRUST-012):
`default-src 'none'; img-src <cspSource> data:; style-src <cspSource> 'nonce-…'; font-src …;
media-src …; script-src <cspSource> 'nonce-…'; connect-src 'none'; frame-src 'none'; object-src
'none'; worker-src 'none'; base-uri 'none'; form-action 'none'`. No `unsafe-eval`, no
`wasm-unsafe-eval`, no workers, no network. `esbuild.mjs` already records that PlantUML's
`viz-global.js` (Graphviz as WebAssembly) was rejected because it "would need 'wasm-unsafe-eval' in
the CSP", and `test/security/package-contract.test.ts` asserts the Vega chart code has no `eval(` or
`new Function`.

### 2.1 Conversion to Mermaid `stateDiagram-v2` (existing path)

How Mermaid is wired: `package.json` `"mermaid": "^12.2.0"` (lock: 12.2.0, MIT). The page module
`src/page/modules/mermaidPreview.ts` dynamically imports Mermaid (ES module with code splitting,
`scripts/page-bundle.mjs` `mermaidBundleOptions`, chunks in `out/bundle/mermaid-chunks/`), waits for
fonts, builds `themeVariables` from `--studio-*` CSS variables (DIAG-005), initializes
`securityLevel: "strict"`, `theme: "base"`, renders each `.myst-mermaid-diagram` to SVG and shows it
as an `<img>` with a `data:image/svg+xml` URL (DIAG-001), caches drawings by theme+source
(`mermaidCache.ts`, DIAG-009, PERF-07), and on failure calls `showMermaidError` (DIAG-015). The host
injects `mermaidPreview.js` only when the page has a `myst-mermaid-figure`
(`src/session/webview.ts`).

A converter would be a pure function in `src/core/render/` (JSON to Mermaid text), run at
normalization, emitting a Mermaid figure whose "source" panel shows the JSON. Mapping:

| XState | Mermaid stateDiagram-v2 |
|---|---|
| atomic state, description | `state "label" as s1` + `note right of s1` |
| compound state, `initial` | `state s { [*] --> child ... }` |
| parallel state | composite with regions separated by `--` |
| final | `s --> [*]` |
| transition `on` with target | `a --> b : EVENT [guard] / action` (label text only) |
| `after`, `always` | label text `after 1000`, `always` |
| multiple targets (array) | `<<fork>>` pseudo-state (approximation) |
| choice state / guarded branches | `<<choice>>` (approximation) |
| history | **none** (no syntax; no "history" token in Mermaid 12.2.0's state chunks); fake atomic state "H"/"H*" |
| transition between states of different composite states | **not supported**: "You cannot define transitions between internal states belonging to different composite states" (mermaid.js.org/syntax/stateDiagram.html) |
| invoke, tags, meta, entry/exit | notes or label text only |
| `@code` transition | a dangling edge to a placeholder "?" state |

Other limits: ids must be sanitized (dots, spaces, `#`); `classDef` "Cannot be applied to or within
composite states"; the layout cannot be steered. Mermaid's docs say state diagrams default to the ELK
layout in Mermaid 12; Studio does not set `layout`, and `out/bundle/mermaid-chunks/elk-*.js` (1.5 MB)
is already in the build, so the converter would draw with elkjs (EPL-2.0) unless it emits a
`layout: dagre` config (then dagre-d3-es, MIT, plus d3, ISC). License closure of what Mermaid loads
for a state diagram (read from `node_modules/*/package.json`): mermaid MIT, dagre-d3-es MIT,
lodash-es MIT, khroma MIT (license file), stylis MIT, **d3 ISC**, **dompurify (MPL-2.0 OR
Apache-2.0)**, **elkjs EPL-2.0** (default layout), chevrotain Apache-2.0 (used by
`@mermaid-js/parser`; whether the state parser uses it: UNVERIFIED). Verdict: cheapest, lowest risk
in code, but not strict MIT and the weakest statechart fidelity.

### 2.2 Stately's open-source pieces

- **xstate-viz** (github.com/statelyai/xstate-viz): MIT, **archived** (last push 2023-11-03); React 17,
  Next 11, Chakra UI, Monaco, **elkjs ^0.7.1**, xstate ^4.26. Not usable.
- **Stately Sketch** (github.com/statelyai/sketch): MIT, active (last push 2026-07-29), not
  published on npm (`@statelyai/sketch` is 404). A full app (React 19, TanStack Start, Tailwind,
  CodeMirror, better-sqlite3, Cloudflare wrangler). It draws nested boxes with transitions as rows
  (`src/components/MachineViz.tsx`, `TransitionViz.tsx`), no graph layout engine, and evaluates
  machine code with `new Function()` (`src/lib/machine.ts`). Useful only as a design reference for
  the zero-dependency option.
- **Stately visual editor / Editor Sync / Stately Editor VS Code extension**: product features named
  in the blog; license not open source (UNVERIFIED).
- **`@statelyai/graph` 2.6.0**: MIT, graph data structures and algorithms; layouts are optional
  peers (elkjs, dagre, graphviz, cytoscape...). Adds nothing a direct dagre use does not.
- **`@statelyai/inspect` 0.7.2**: MIT; runtime inspection over WebSocket (`ws`, `partysocket`): out
  of scope (network, live actors).
- **`@xstate/graph` 3.0.4**: MIT, zero deps, peer `xstate ^5.19.4` (v5). In v6 the graph utilities
  ship inside `xstate` as the `xstate/graph` entry (`toDirectedGraph`, `getAdjacencyMap`, paths).
- **`xstate` CLI** (`bin/xstate.js`, `bin/agent.js`): `inspect` returns `toDirectedGraph` +
  serialization diagnostics as JSON; it refuses definitions with code expressions
  (`EVALUATOR_REQUIRED`). Node only; no drawing.

### 2.3 state-machine-cat

MIT (LICENSE: "Copyright (c) 2016-2026 Sander Verweij"), 15.0.12 (2026-11-15), 875 stars. Rich
statechart semantics (composite, parallel, history, choice, fork/join), inputs smcat, SCXML, scjson.
Its SVG output goes through `@hpcc-js/wasm-graphviz` 1.30.0 (**Apache-2.0**, WebAssembly;
`dist/render/index.mjs` imports `./vector/vector-with-wasm.mjs`); other deps `he` (MIT),
`fast-xml-parser`, `neotraverse` (licenses not checked). Needs an XState JSON to smcat/scjson
adapter and `wasm-unsafe-eval` in the CSP. Rejected (license and CSP).

### 2.4 Layout libraries

- **`@dagrejs/dagre` 3.1.3** (2026-10-24): MIT (LICENSE "Copyright (c) 2012-2014 Chris Pettitt", plus
  `dist/*.LEGAL.txt` with the same MIT text). Only dependency `@dagrejs/graphlib` 4.0.6 (MIT, same
  LICENSE), bundled into `dist/dagre.min.js` (49 326 bytes, 17 271 gzip). No `eval`/`new Function`
  in the minified file. Layered (Sugiyama) layout fits state machines. Compound graphs (clusters) are
  supported by graphlib (`compound: true`); edges attached to a cluster node itself are, as far as
  known, not supported by dagre (Mermaid works around it): UNVERIFIED (the dagre wiki does not say).
  Hence the recommended bottom-up layout (2.6).
- **`dagre` 0.8.5** (old name): MIT, last release 2022, depends on lodash; use `@dagrejs/dagre`.
- **elkjs 0.12.1**: "EPL-2.0 OR GPL-3.0-or-later". Best compound layout, but not MIT. Note: elkjs
  0.9.3 (EPL-2.0) is already in Studio's VSIX through Mermaid.
- **Graphviz** (`@hpcc-js/wasm` 2.36.0 Apache-2.0, 37 MB unpacked; `@hpcc-js/wasm-graphviz` 1.30.0
  Apache-2.0; `d3-graphviz` 5.6.0 BSD-3-Clause, last release 2024-08; `@viz-js/viz` 3.31.0 package
  field MIT but no LICENSE file in the tarball and it embeds Graphviz, whose license is EPL:
  UNVERIFIED). All need WebAssembly, so `wasm-unsafe-eval`. Rejected.
- **cytoscape** 3.35.0: MIT, canvas renderer, compound nodes; hierarchical layout only through
  extensions (cytoscape-dagre MIT, cytoscape-elk MIT wrapper over EPL elkjs). Canvas output does not
  fit Studio's SVG-picture model (export, theme redraw). Not recommended.
- **React Flow / xyflow** (`@xyflow/react` 13.0.1, `@xyflow/system` 1.0.0): MIT, but needs React (or
  Svelte) and `d3-drag`/`d3-zoom`/`d3-selection`/`d3-interpolate` (ISC), and has no layout engine.
  Interactive editor canvas: wrong fit for a read-only preview picture.
- **libavoid-js** 0.5.0-beta.6: LGPL-2.1-or-later, wasm. Rejected.

### 2.5 Other statechart / SCXML viewers found (npm search "statechart", GitHub)

- **xstate-diagram** 0.2.1 (created 2026-11-11, 3 stars): **ISC**, no LICENSE file in the tarball,
  depends on elkjs (EPL-2.0) and xstate v5. Rejected.
- **`@statewalker/fsm-charts`** 0.2.9 / `@statewalker/fsm-viewer` 0.6.2: MIT (LICENSE checked), no
  runtime deps but needs lodash injected; vendored dagre; renders its own HFSM format
  (`{ key, transitions, states }`) as nested `<details>` panels with one SVG per composite state.
  No parallel/history concept (UNVERIFIED). 0 stars, one maintainer. Reference design, not a
  dependency.
- **statechart-kit** 0.15.1: MIT, Vue 3 peer, SCXML editor, depends on a `-dev` prerelease.
  Rejected.
- `@statebacked/react-statechart` (2023, React), `statechart-viz` (2021, React), `xstate-plantuml`
  (2020, emits PlantUML text for XState v4): stale or framework-bound. An XState-to-PlantUML route
  would reuse Studio's PlantUML block (`@plantuml/core`, MIT, Smetana layout), but PlantUML's state
  diagrams with Smetana instead of Graphviz have limited composite-state layout: UNVERIFIED, not
  studied further.
- `@xstate/scxml` 1.0.0-alpha.4: MIT, SCXML to XState converter (input side only).

### 2.6 Recommended design: own renderer with dagre

- **Model (`src/core/render/xstateModel.ts`, pure TS, Node-testable)**: parse the fence text as JSON;
  accept `MachineJSON` tolerantly (unknown keys kept as notes, `onDone` accepted); infer state kinds;
  resolve targets (sibling, `.child`, `#id`, `#id.path`, escaped dots, arrays); collect transitions
  per source with kind (`on`, `after`, `always`, `onDone`, `onError`, `onTimeout`, invoke's
  `onDone`/`onError`, choice branches); mark `@code`/`@expr` as "dynamic" (text shown escaped, never
  evaluated). Errors: invalid JSON (with line/column), not an object, no `states`/`initial` (unknown
  format), unresolved target (drawn but flagged). Optional: depend on `xstate` (MIT, zero deps, no
  eval in dist) only as a **dev dependency** to generate test fixtures with the real
  `machineToJSON`, not at runtime (its strict loader rejects some `machineToJSON` output, 1.3, and it
  would add ~190 KB).
- **Layout (page bundle)**: bottom-up: lay out the children of each compound state with dagre
  (`rankdir` TB or LR), size the compound box from the result, then lay it out as a single node in
  its parent; parallel regions side by side with dashed separators; transitions whose source and
  target sit in different composites are routed at their lowest common ancestor between box borders.
  Label sizes measured in the page with the pinned Mermaid font (as `mermaidPreview.ts` does).
- **Drawing**: an SVG string (initial dot, rounded state boxes, double-border final states, `H`/`H*`
  circles, guards as `[guard]`, actions as `/ action`, `after 1s`, `always`, invoke as a badge, tags
  as chips, dashed stub for dynamic transitions), colours from `--studio-*` variables (like
  `chartTheme.ts`), shown as a `data:image/svg+xml` `<img>`, cached by theme+source via
  `mermaidCache.ts` `diagramKey`.

Alternative zero-dependency option: the same model drawn as nested HTML/SVG boxes with transitions
listed as rows ("EVENT [guard] -> target"), Stately Sketch style: full fidelity, accessible text, no
arrows. Medium effort; could also be the fallback when a machine is too large to lay out.

## 3. How the block fits Studio

Files that the Vega chart block touched (grep for `myst-vega`/`vega-lite`) and their equivalents:

- `src/core/render/mystNormalize.ts`: `NODE_RULES` gets a rule for `code` nodes with
  `lang === "xstate-json"`; `normalizeDiagram` (kind union `"mermaid" | "plantuml" | "vega"`) gets an
  `"xstate"` kind, producing `figure.myst-xstate-figure > div.myst-xstate-diagram` (aria-label) and
  the `details` source panel (DIAG-001/023 markers).
- `src/session/webview.ts`: inject `xstatePreview.js` only when the HTML contains
  `class="myst-xstate-figure"` (like DIAG-124 for the chart runtime).
- `esbuild.mjs`: a new IIFE bundle `src/page/modules/xstatePreview.ts` to `out/bundle/xstatePreview.js`
  (browser, es2020, minified), next to the Vega one; ship dagre's LICENSE if the packaging copies
  third-party licenses as it does for KaTeX and PlantUML.
- `src/page/modules/xstatePreview.ts` (queue, theme observer, `studio:content-replaced`, cache),
  `xstateDiagram.ts` (layout + SVG), and an error module: generalize `mermaidError.ts`/`chartError.ts`
  ("Unable to render the state machine. Its source remains available below." + `details` with the
  reason; one error, replaced on redraw; `data-render-state="error"`).
- `src/page/features/rendererBridge.ts`: no change; the renderer listens to
  `studio:content-replaced` like Mermaid and Vega.
- `src/page/modules/exportSnapshot.ts`: add `.myst-xstate-diagram` to `DIAGRAM_SELECTOR` so the
  export waits for it (DIAG "Exported diagrams are drawn images in the theme of the file").
- `src/page/modules/codeCopy.ts`, `commentCompose.ts`, `commentThreads.ts`, `blockEditActions.ts`:
  figure-class lists (`.myst-mermaid-figure, .myst-plantuml-figure, .myst-vega-figure`) get
  `.myst-xstate-figure` (copy button, comments, click-to-edit source).
- `src/core/preview/styles/contentBlockStyles.ts`: figure, image and error styles.
- `src/core/palette/paletteActions.ts`: an `xstate` action (slash aliases such as `xstate`,
  `statechart`, `state machine`; group `full`, scope `block`) with the minimal example as template;
  a PALETTE SwRS like PALETTE-265 for Vega.
- **Writing skill** `skills/writing-for-markdown-okf-schema-studio/SKILL.md`: a row in the capability
  table ("State machines: `xstate-json` fence, XState v6 machine JSON"), a taste rule (Mermaid
  `stateDiagram` for small sketches, `xstate-json` for a real XState machine), a limit (functions
  show as dynamic transitions), and a real example rendered by `test/core/render/writingSkill.test.ts`
  (constitution section 6; skill must stay under 160 lines).
- **Requirements**: new SwRS in `requirements/tiers/swrs/diagrams/` via `okfreq new` (do not
  hand-allocate), modelled on DIAG-121..124: fence becomes a state-machine figure; drawn as a themed
  SVG picture with errors in place (invalid JSON, unknown format, unresolved target); runtime loads
  only with a figure and needs no eval/wasm/network; function transitions shown as dynamic; plus
  export and palette SwRS updates; StRS DIAG-001/007 links; a `requirements/tiers/log.md` entry.
- **Tests**: unit tests of the model (fixtures generated from real `machineToJSON` output, pinned
  version), normalization (`mystPaletteRendering`, `chartRendering`-like), page tests like
  `chartError.test.ts`/`vegaChart.test.ts`, a CSP test like `test/page/chartCsp.test.ts`, the
  package contract in `test/security/package-contract.test.ts` (bundle present, no `eval(` /
  `new Function`, dependency pinned), visual fixtures in `test/visual/renderFixtures.ts` (light and
  dark), slash-menu coverage (`slashSyntaxCoverage.test.ts`), and the e2e/requirements test file of
  the diagrams group.
- **Sphinx build**: Studio also builds with Sphinx (`sphinx/`); an `xstate-json` fence there falls
  back to a code block unless the Sphinx extension learns it (UNVERIFIED; open question).

## 4. Risks

- **Beta format**: v6 is 6.0.0-beta.3 (11 days after beta.0); `latest` on npm is still 5.33.4. The JSON
  API was renamed on 2026-10-17; the format has no version field; the schema is not in the npm
  package; type, schema and loader disagree on `onDone` (1.3). Mitigation: tolerant reader, fixtures
  pinned to a stated xstate version, unknown keys never fatal, an SwRS that names the version
  studied.
- **Fidelity**: idiomatic v6 (function transitions) loses targets; inline invokes are dropped;
  spawn, `enq.*` have no JSON. The diagram can mislead by omission: show dynamic transitions
  visibly and say so in the skill.
- **Security**: the block is JSON only; `@code`/`@expr` strings are displayed as escaped text, never
  evaluated; no `machineFromJSON` evaluators; no network; CSP unchanged. Label text goes into SVG:
  escape it (Mermaid relies on `securityLevel: "strict"` + DOMPurify; an own renderer must escape
  XML itself). Large or deeply nested JSON: cap size/depth and fail with a message.
- **Size and performance**: dagre adds 17 KB gzip in a bundle loaded only on pages with the block.
  Layout cost grows with states x transitions; cache by theme+source as Mermaid/Vega do.
- **Licensing drift**: pin `@dagrejs/dagre` and recheck the LICENSE on each upgrade (its graphlib
  is pinned exactly at 4.0.6 in its `package.json`).
- **Maintenance**: an own renderer is Studio's code to maintain (layout edge cases: cross-hierarchy
  edges, self-loops, many parallel regions).

## Open questions for the owner

1. Does "every runtime dependency MIT" apply to dependencies Studio **already ships** (Mermaid with
   d3 ISC, DOMPurify MPL-2.0/Apache-2.0, elkjs EPL-2.0)? If not, the Mermaid conversion becomes the
   cheap first step; if yes, only an own renderer (with dagre, or without dependency) qualifies.
2. ISC and BSD-0/BSD are permissive but not MIT: may they be accepted case by case (for example d3
   modules), or is the rule MIT only?
3. Arrows (own renderer + dagre, large effort) or nested boxes with transitions as rows (no
   dependency, medium effort), or Mermaid conversion (small effort, lower fidelity)?
4. Function transitions (`@code`): show a dynamic stub only, or also extract literal
   `target: '...'` strings from the code text by a static (non-executing) heuristic, marked as
   inferred?
5. Ship while XState v6 is beta (pinning the studied version) or wait for 6.0.0 stable?
6. Should the block also accept v5 JSON (no `@code`, different guard prefixes), or v6 only?
7. Should an `xstate-json` fence render in the Sphinx build output too, or only in the preview?
8. Validation strictness: draw what can be drawn and flag problems in place, or refuse a machine
   that the v6 JSON Schema / `machineFromJSON` would reject?
9. Palette: add an "XState machine" insert action and slash aliases now, or later?

## Sources

- Blog: https://stately.ai/blog/2026-11-05-xstate-v6-beta (read 2026-11-17).
- npm `xstate@6.0.0-beta.3` tarball (`npm pack --ignore-scripts`): `LICENSE`, `package.json`,
  `dist/declarations/src/serialize.d.ts`, `dist/declarations/src/machineFromJSON.d.ts`,
  `dist/declarations/src/graph/*.d.ts`, `dist/xstate.esm.js` (`machineToJSON`, `codeExpression`,
  `stateNodeJSONKeys`), `dist/createActor-*.esm.js` (`TRANSITION_KEYS`), `docs/serialization.md`,
  `docs/final-states.md`, `docs/persistence.md`, `docs/api-stability.json`, `bin/xstate.js`,
  `bin/agent.js`. `npm view xstate dist-tags time`.
- https://github.com/statelyai/xstate (default branch `next`, MIT, pushed 2026-11-17);
  https://raw.githubusercontent.com/statelyai/xstate/next/packages/core/src/machine.schema.json (also
  at tag `xstate@6.0.0-beta.3`); commits via GitHub API for that path (#5810 2026-10-18, #5800
  2026-10-17, #5679 2026-08-03); branches `v6`, `next`.
- Mermaid docs: https://mermaid.js.org/syntax/stateDiagram.html; Studio's `node_modules/mermaid`
  12.2.0 (`dist/chunks/mermaid.core/stateDiagram-v2-*.mjs`, `elk-*.mjs`), `package-lock.json`,
  `node_modules/{d3,dompurify,elkjs,chevrotain,dagre-d3-es,khroma,vega,d3-sankey}/package.json`.
- Studio sources (repo `markdown-okf-schema-studio`, `main` at dedbdb2a): `src/core/security/csp.ts`,
  `src/session/webview.ts`, `src/page/modules/mermaidPreview.ts`, `mermaidError.ts`, `vegaPreview.ts`,
  `exportSnapshot.ts`, `src/page/features/rendererBridge.ts`, `src/core/render/mystNormalize.ts`,
  `src/core/palette/paletteActions.ts`, `esbuild.mjs`, `scripts/page-bundle.mjs`,
  `test/security/package-contract.test.ts`, `requirements/tiers/swrs/diagrams/`,
  `skills/writing-for-markdown-okf-schema-studio/SKILL.md`,
  `.agents/guidelines/writing-skill-maintenance.guideline.md`, `out/bundle/mermaid-chunks/`.
- npm registry (`npm view`, 2026-11-17): elkjs, @dagrejs/dagre, @dagrejs/graphlib, dagre,
  state-machine-cat, @xstate/graph, @statelyai/inspect, @statelyai/graph, @statelyai/sketch (404),
  @xstate/inspect, cytoscape, cytoscape-elk, cytoscape-dagre, @xyflow/react, @xyflow/system,
  @xyflow/svelte, @hpcc-js/wasm, @hpcc-js/wasm-graphviz, d3-graphviz, @viz-js/viz, viz.js,
  @xstate/scxml, libavoid-js, xstate-diagram, @statewalker/fsm-charts, @statewalker/fsm-viewer,
  statechart-kit, mermaid; `npm search statechart`.
- Tarballs inspected (`--ignore-scripts`): @dagrejs/dagre 3.1.3, @dagrejs/graphlib 4.0.6,
  state-machine-cat 15.0.12, @statewalker/fsm-charts 0.2.9, xstate-diagram 0.2.1, @viz-js/viz 3.31.0.
- GitHub API / raw files: statelyai/xstate-viz (archived, `package.json` on `dev`), statelyai/sketch
  (`package.json`, `README.md`, `src/components/MachineViz.tsx`, `TransitionViz.tsx`,
  `src/lib/machine.ts`), statelyai/graph, statelyai/inspect, sverweij/state-machine-cat, kieler/elkjs,
  dagrejs/dagre (and its wiki), emmby/xstate-diagram, statewalker/statewalker-fsm.
- Not verified by execution: running `machineFromJSON`/`toDirectedGraph`/`machineToJSON` on the
  examples was refused in this session, so every runtime behaviour above comes from reading the
  published code and docs.

## Follow-up 2026-11-17: Stately look and editing

New owner decisions: (a) the MIT rule covers only what this change **adds**; dependencies Studio
already ships (Mermaid's d3, DOMPurify, elkjs 0.9.3) may be reused. (b) The owner wants the **same
rendering as Stately's own diagrams** (the blog's read-only viz, editor.stately.ai, the Stately Editor
VS Code extension) **and editing** like the vendor's extension, writing changes back to the block's
JSON.

### Recommendation

The exact Stately rendering cannot be reused. The blog diagram is an **iframe of the hosted,
proprietary editor** (`https://editor.stately.ai/viz#machine=…&format=…&theme=…`). The VS Code
extension is **proprietary** ("Stately Editor Proprietary License Agreement", which forbids copying,
derivative works and reverse engineering); it embeds that same hosted editor, needs network and an
account, and opens only "read-only root-level views" on free accounts. **Recommendation: build the
Stately look in Studio by porting the MIT-licensed rendering approach of Stately's archived
`xstate-viz` (LICENSE "Copyright (c) 2021 Stately": ELK `layered` with `INCLUDE_CHILDREN`, state
boxes, transitions passing through event "pills") to framework-free TypeScript/SVG, laid out with the
elkjs 0.9.3 Studio already ships; then add a structured diagram editor on Studio's existing
block-edit path** (like the table cell editor: open on click, edit a model, serialise the JSON, save
through `previewEditSave`). Phase 1 read-only (large); phase 2 structural edits: rename, add, delete
states; add, retarget, delete transitions; edit event, guard and description labels (large); phase 3
optional dragging with stored positions (medium, needs a decision on where positions live). Today's
editor.stately.ai also lays out with ELK `layered` (its public bundle carries
`elk.algorithm":"layered` and many `org.eclipse.elk.*` options), so this approach matches the
vendor's layout family; fidelity to the **current** proprietary visuals stays approximate and will
drift. ELK replaces the dagre recommendation of the main study: it handles transitions across
composite states natively. Cheap extras, opt-in: **"Open in Stately viz"** (external browser link to
the public `/viz` URL with `format=xstate-json`, small effort; sends the machine to Stately's page)
and, when the vendor extension is installed, **"Open in Stately Editor"** (medium, fragile, command
contract UNVERIFIED). Neither can be the in-preview renderer under Studio's CSP and offline posture.

### Comparison of the options

| Option | What ships / license | Look vs Stately | Editing | Offline, CSP | Maintenance risk | Effort |
|---|---|---|---|---|---|---|
| **A. Port xstate-viz rendering (MIT) + elkjs 0.9.3 (already shipped)** (recommended, phase 1) | Studio code (MIT, keep "Copyright (c) 2021 Stately" notice); elkjs EPL-2.0 already in VSIX | Close to Stately Studio 2021-2023 (same author, same ELK approach); not pixel-identical to today's editor | None by itself | Yes: ELK already runs in the webview through Mermaid; no eval, wasm or worker | Ours; v6 model adaptation | Large (about 2 000 lines of React/SCSS to port) |
| **B. Structured diagram editor on A** (phases 2-3) | Studio code | Same as A | Rename/add/delete states, add/retarget transitions, edit event/guard/description; drag with positions (phase 3) | Yes | Ours; the JSON writer must keep unknown keys and `@code` verbatim | Large (+ medium for drag) |
| C. Reimplement today's Stately look from screenshots, ELK layout | Studio code + elkjs | Approximate; chases a moving proprietary design | Same as B | Yes | High (design drift; trade-dress imitation to avoid) | Large+ |
| D. Embed the editor.stately.ai iframe in the preview (as the blog does) | Nothing shipped; hosted proprietary service | Identical | Yes, with account/API key; free plan read-only | **No**: needs `frame-src https://editor.stately.ai` and network; sends the machine to a third party | Vendor-controlled | Medium |
| E. "Open in Stately Editor" command when `statelyai.stately-editor` is installed | Nothing shipped; vendor extension proprietary | Identical (in the vendor's panel, not in the preview) | Yes in the vendor panel; write-back through a temp or sidecar file | Needs network and sign-in | Fragile: command arguments undocumented (UNVERIFIED); the extension works on files, not on a fence in Markdown | Medium |
| F. "Open in Stately viz" external link (`/viz#machine=<base64url>&format=xstate-json&theme=…`) | Nothing shipped | Identical, read-only, in the browser | No | User-initiated, outside the webview; machine sent to Stately's page | URL contract undocumented (read from the blog's bundle) | Small |
| G. Extract Stately Sketch components | React 19, TanStack, Tailwind, shadcn; deps include Apache-2.0 (class-variance-authority, ts-blank-space), ISC (lucide-react, yaml), OFL-1.1 (Figtree font), "Remix Icon License 1.0" | Different: nested boxes, transitions as rows, no arrows | No diagram editing (code panel + simulation) | JSON path fine; XState-code path uses `new Function` | Not a library; app-shaped | Large, wrong look |
| H. `@statelyai/sdk` 0.49.3 (MIT) | MIT postMessage client for the hosted editor; graph converters | Only through D | Only through D | Same as D | Alpha ("APIs may change between minor releases") | Medium (with D) |

### F1. What renders Stately's diagrams

- **Blog post** (https://stately.ai/blog/2026-11-05-xstate-v6-beta, fetched 2026-11-17): the text
  says the checkout machine is "rendered with the editor's read-only viz". In the page's RSC payload
  the diagram is a client component (module 525928, chunk `06vejnktxb~_f.js`) with props
  `{"machine":{"format":"xstate","definition":"<TS source>"},"name":"checkout"}`. That component
  builds `https://editor.stately.ai/viz#` + `URLSearchParams({ machine: base64url(definition),
  format, theme })` (accepted formats: `digraph`, `xgraph`, `xstate`, `xstate-json`; optional
  `mode`), mounts it in an **iframe** when scrolled into view, listens for `@statelyai.loaded` /
  `@statelyai.error` messages from origin `https://editor.stately.ai`, and keeps a screenshot as a
  fallback ("The screenshot stays available if the editor cannot load"). The blog diagram is the
  hosted editor, not a library.
- **editor.stately.ai**: a Next.js app with no public repository in the `statelyai` GitHub
  organization (repos listed through the GitHub API on 2026-11-17: xstate, sketch, graph, inspect,
  agent, skills, docs, schema, specification, xstate-tools, xstate-viz (archived), and others). Its
  public JS for `/viz` (70 chunks, 8.8 MB) contains ELK layered options, so it bundles elkjs; no
  React Flow/xyflow identifiers were found. Only third-party library identifiers were searched; the
  vendor's own code was not analysed. Proprietary: consistent with the extension's license and with
  "For enterprise self-hosting options, see pricing" in `@statelyai/sdk`'s README; no license is
  published for the hosted app, so the formal terms are UNVERIFIED.
- **Stately Sketch** (github.com/statelyai/sketch): LICENSE "MIT License, Copyright (c) 2026
  Stately". Not on npm (`@statelyai/sketch` 404); `package.json` is a TanStack Start app (React 19,
  `@base-ui/react`, Tailwind 4, shadcn, CodeMirror, better-sqlite3, Cloudflare wrangler,
  `@statelyai/graph` ^0.5.0, `xstate` ^5.31.1). Rendering is about 470 lines of React
  (`MachineViz.tsx` 71, `StateNodeViz.tsx` 217, `TransitionViz.tsx` 185) with Tailwind classes:
  **nested boxes with transitions listed as rows** (event, target name, timer/always icons), no edges
  and no layout engine, unlike the blog's arrow diagram. `new Function` is used only by
  `parseXStateMachineCode` (XState code input); the JSON path is `JSON.parse` +
  `xstate.createMachine` (v5), so for JSON input it is removable. Sketch edits code (CodeMirror), not
  the diagram. Runtime licenses (npm, 2026-11-17): React, base-ui, TanStack, Tailwind, shadcn, vaul,
  zod, clsx, tailwind-merge, CodeMirror, `@xstate/store`, `@statelyai/graph` MIT;
  `class-variance-authority` and `ts-blank-space` Apache-2.0; `lucide-react` and `yaml` ISC;
  `@fontsource-variable/figtree` OFL-1.1; `@remixicon/react` "Remix Icon License 1.0"; `remixicon`
  Apache-2.0. It can only be "extracted" by rewriting (React + Tailwind tokens), and its look is not
  the requested one.
- **xstate-viz** (github.com/statelyai/xstate-viz, archived 2023-11-03): LICENSE "MIT License,
  Copyright (c) 2021 Stately"; the predecessor of Stately Studio's diagram. Rendering files (branch
  `dev`): `graphUtils.ts` 455 lines (ELK graph: `elk.hierarchyHandling: INCLUDE_CHILDREN`,
  `elk.algorithm: layered`, `considerModelOrder: NODES_AND_EDGES`, `wrapping.strategy: MULTI_EDGE`,
  `aspectRatio: 2`, `direction: RIGHT`; transitions as ELK label nodes; up to three layout attempts
  on ELK errors), `directedGraph.ts` 174, `StateNodeViz.tsx` 199 + `.scss` 184, `TransitionViz.tsx`
  175 + `.scss` 87, `EdgeViz.tsx` 82, `Edges.tsx` 47, `Graph.tsx` 91, `EventTypeViz.tsx` 111,
  `ActionViz.tsx` 230, `DelayViz.tsx` 44, `elkMachine.ts` 52 (about 2 000 lines). It renders HTML
  state and label nodes, measures their DOM rectangles, lays them out with ELK, then draws SVG
  edges. Dependencies: React 17, Chakra UI, `@xstate/react`, react-markdown, xstate v4, elkjs
  ^0.7.1. Porting means: replace React/Chakra with DOM building, replace the v4 `StateNode` model
  with the v6 JSON model of the main study (2.6), keep the ELK graph construction and the CSS look
  (themed with `--studio-*` variables), and keep the MIT notice of the ported files.
- **Other Stately packages**: `@statelyai/sdk` 0.49.3 (MIT, "Copyright (c) 2026 Stately Software,
  Inc."), "The public alpha SDK for embedding the Stately visual editor": `createStatelyEmbed({
  baseUrl: "https://editor.stately.ai", apiKey })` mounts an iframe and talks `postMessage`;
  `planSourceUpdate` needs "the editor-sync endpoint on the editor at `baseUrl` ... and editor-sync
  write access"; `readOnlyReason: 'free-plan'` shows "Upgrade to edit"; self-hosting the editor is an
  enterprise offer. It ships graph converters (`fromStudioMachine`, `toStudioMachine`; graph types
  with `position?: Point`) but **no renderer**. It also ships `schemas/xstate-v6.schema.json` (draft
  2020-12) for the v6 `machineFromJSON` loader format and states that this format does not support
  state `onDone` (consistent with 1.3). `statelyai` 0.21.14 (MIT CLI, `statelyai open`) depends on
  the SDK, `@statelyai/mcp`, tsx and TypeScript. `@statelyai/graph` 2.6.0 and `@xstate/graph`: no
  drawing. `@xstate/viz` 0.3.4 (MIT, React 16 era, styled-components): obsolete. The private
  `@statelyai/editor-sync` package named in the SDK README is not published (npm 404).

### F2. The Stately Editor VS Code extension

Evidence: VS Code Marketplace gallery API, `statelyai.stately-editor` 0.2.46 (released
2026-07-24, updated 2026-11-16, verified publisher "Stately"); its manifest, LICENSE and README
fetched as Marketplace assets (the VSIX itself was neither downloaded nor opened).

- **License**: `"license": "SEE LICENSE IN LICENSE"`; LICENSE: "Stately Editor Proprietary License
  Agreement ... Copyright (c) 2025-2026 Stately Software, Inc. All rights reserved." It forbids to
  "copy, modify, translate, adapt, or create derivative works of the Software" and to "reverse
  engineer, decompile, disassemble". README: "Stately Editor is proprietary software. It is free to
  install, with available features determined by your Stately account and plan." and "Free accounts
  open read-only root-level views."
- **How it embeds the editor**: a webview panel with an **iframe** of the configured editor host
  (`statelyai.editorUrl`, "Defaults to `https://editor.stately.ai`"; README: "The iframe stays hidden
  until initialization completes"). Sign-in by Stately OAuth or API key (`statelyai.signIn`,
  `statelyai.useApiKey`). Sync conversion runs `local` by default (`statelyai.syncBackend`), but the
  editor UI is remote. **Offline: no**, except with a self-hosted editor URL (enterprise offer).
- **Supported sources**: XState JS/TS, "JSON and JSONC", YAML, Amazon States Language, Redux Toolkit,
  Zustand, Mermaid. It works on **files** (a CodeLens per machine, `Stately: Open Visual Editor`), not
  on a fenced block inside Markdown. Layout and colours of unlinked machines live in a sidecar
  `.statelyai/local.json`; `statelyai.roundTripStatelyMetadata` can write `@statelyai.*` metadata into
  source. It projects v6 **function transitions** onto their literal return targets ("The chart shows
  their targets"), which a JSON-only block cannot do (main study 1.2).
- **Commands** (manifest): `statelyai.openVisualEditor`, `statelyai.openVisualEditorWorktree`,
  `statelyai.signIn`, `statelyai.useApiKey`, `statelyai.signOut`, `statelyai.exportLogs`.
- **Integration from Studio**: Studio could detect the extension
  (`vscode.extensions.getExtension("statelyai.stately-editor")`) and offer "Open in Stately Editor"
  on an `xstate-json` figure: write the fence's JSON to a temporary or sidecar `.json` file, open it,
  run `statelyai.openVisualEditor`, watch that file and write its content back into the fence through
  Studio's edit path. Whether the command accepts a URI argument is undocumented (UNVERIFIED, and
  finding out by decompiling is prohibited by its license). Studio would ship no Stately code, so the
  MIT rule is not involved, but the feature depends on a proprietary, online, account-gated tool, and
  the temp-file round trip is fragile (two writers, conflicts). It is an optional bridge, not a
  renderer.

### F3. Reaching "same look + editing" in Studio

**Layout and look.** ELK is now allowed: Studio ships elkjs 0.9.3 through Mermaid 12.2.0
(`package-lock.json`), and Mermaid already runs it inside the webview under the current CSP, so the
CSP fit is demonstrated. ELK `layered` with `INCLUDE_CHILDREN` routes transitions across composite
states natively, which dagre does not (main study 2.4). Bundling: ELK must not ship twice. Either add
`elkjs` as a direct dependency pinned to the same 0.9.3 and build the renderer as an ES module with
code splitting that shares the ELK chunk with Mermaid (`scripts/page-bundle.mjs`
`mermaidBundleOptions` already splits `mermaid-chunks/`), or reach Mermaid's ELK chunk indirectly
(fragile). The VSIX then gains only Studio's own code. The look ported from xstate-viz: rounded state
boxes with the state name and entry/exit/invoke/tags sections, a dot and arrow for the initial state,
transitions drawn as edges through an event "pill" (event, `[guard]`, actions, `after` delay),
dashed parallel regions, double-bordered final states, history `H`/`H*`; colours from VS Code theme
variables in light and dark.

**Editing model** (Studio's block-edit path). Today a click on a block posts `previewEditOpen`; the
host (`src/session/features/blockEdits.ts`) answers `previewEditSource` with the block's source; the
page opens the raw text box (`src/page/features/blockSourceEditor.ts`) or a structured editor (the
table cell editor, `tableCellEditor.ts`, which parses the source into a model and writes it back,
TABLE-121); `blockEditor.saveBlockEdit()` posts `previewEditSave` with the new text. Mermaid, Vega and
PlantUML figures are edited as raw source (DIAG "A click on a picture opens its source editor";
insert templates in `blockEditActions.ts`). A diagram editor fits as a new structured editor:

1. A click on an `xstate-json` figure opens the diagram in edit mode over the renderer's JSON model
   (main study 2.6), with a "Source" button that falls back to the raw JSON text box.
2. Structural actions (toolbar, context menu, keys): rename a state (inline input; the key in
   `states` and every target naming it are updated; `#id` targets kept); add a child or sibling
   state; delete a state (and the transitions targeting it, after confirmation); set initial; mark
   final, parallel or history; add a transition by dragging from a state to a target; retarget or
   delete it; edit the event name, guard type and params, description and `after` delay. `@code`
   transitions stay read-only (shown, never evaluated).
3. Serialise: rewrite the fence's JSON with the same indentation, keep key order and **every unknown
   key and `@code` value verbatim**; save through `previewEditSave` (undo then works as for any
   block edit).
4. Dragging states: positions are not part of `MachineJSON`. Options: no persistence (automatic
   layout only, recommended first), positions in each state's `meta` (accepted by the schema and the
   loader, but it pollutes the machine), or a Studio sidecar file. Stately's own position format
   (`.statelyai/local.json`, `@statelyai.*` metadata) is not publicly documented: UNVERIFIED.

**Efforts** (with the Vega block integration as "medium"): read-only port of the xstate-viz look with
ELK: large; structural editor (items 1-3): large; dragging with persistence: medium; "Open in Stately
viz" link: small; "Open in Stately Editor" bridge: medium.

**Risks**: fidelity to a moving, proprietary design (today's editor differs from the 2023 xstate-viz
look; matching it from screenshots risks trade-dress imitation: keep Studio's theme and no Stately
logos, fonts or icons); the beta format (main study, section 4); a diagram editor that rewrites JSON
can lose authoring details (key order, spacing, unknown keys must survive); ELK layout cost on large
machines (cache by theme and source, size cap); elkjs is EPL-2.0 (accepted under the new rule because
it is already shipped, but it becomes a direct dependency of this feature); the external "Open in
Stately" options send the machine to Stately.

### Open questions for the owner (follow-up)

1. "Same rendering": is the xstate-viz look (Stately's MIT predecessor of the Studio diagram, same ELK
   approach) acceptable, given that the current editor's look is proprietary and cannot be reused?
2. Editing scope of a first release: structural edits only (states, transitions, labels), or also
   dragging with stored positions? If positions are stored: in `meta` inside the JSON, in a Studio
   sidecar file, or not at all?
3. Add elkjs as a direct dependency pinned to the version Mermaid ships (0.9.3), with a shared bundle
   chunk, accepting that this feature depends directly on EPL-2.0 code?
4. Offer "Open in Stately viz" (external link that sends the machine to Stately's page) and/or "Open in
   Stately Editor" (vendor extension, account and network required)? Both would be opt-in and
   user-initiated; do they fit Studio's privacy and offline posture?
5. When the diagram editor rewrites the JSON, is normalised formatting (2-space indent, stable key
   order) acceptable, or must the author's formatting be preserved?
6. Keep `@code` transitions read-only in the diagram editor (recommended), with a note to edit them in
   the machine's source code?

### Additional sources (follow-up)

- Blog page HTML and chunk `https://stately.ai/_next/static/chunks/06vejnktxb~_f.js` (module 525928,
  the `Embed` component that builds `https://editor.stately.ai/viz#...`), fetched 2026-11-17.
- `https://editor.stately.ai/viz` HTML and its 70 `/_next/static/chunks/*.js` files, searched for
  third-party library identifiers only.
- GitHub API `orgs/statelyai/repos` (2026-11-17); statelyai/sketch `LICENSE`, `package.json`,
  `src/lib/machine.ts`, `src/components/{MachineViz,StateNodeViz,TransitionViz}.tsx`;
  statelyai/xstate-viz `LICENSE`, `package.json`, `src/{graphUtils,directedGraph,elkMachine}.ts`,
  `src/{Graph,StateNodeViz,TransitionViz,EdgeViz,Edges,EventTypeViz,ActionViz,DelayViz,MachineViz}.tsx`,
  `src/{StateNodeViz,TransitionViz,InvokeViz}.scss` (branch `dev`).
- npm: `@statelyai/sdk` 0.49.3 tarball (`LICENSE`, `README.md`, `dist/*.d.mts`, `schemas/`),
  `statelyai` 0.21.14 tarball; `npm view` for `@statelyai/{cli,editor,viz,embed,editor-sync,schema}`
  (404), `@xstate/viz`, and the Sketch dependencies listed in F1.
- VS Code Marketplace gallery API for `statelyai.stately-editor` 0.2.46 and its assets
  `Microsoft.VisualStudio.Code.Manifest`, `Microsoft.VisualStudio.Services.Content.License`,
  `Microsoft.VisualStudio.Services.Content.Details`.
- Studio: `src/page/features/blockSourceEditor.ts`, `src/page/features/blockEditor.ts`,
  `src/session/features/blockEdits.ts`, `src/page/modules/blockEditActions.ts`,
  `scripts/page-bundle.mjs`, `package-lock.json` (elkjs 0.9.3 under mermaid 12.2.0).
