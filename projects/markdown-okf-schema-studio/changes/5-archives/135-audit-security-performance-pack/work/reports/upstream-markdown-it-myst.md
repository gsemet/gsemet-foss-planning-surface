# Upstream pull request text: markdown-it-myst (not opened)

Repository: https://github.com/executablebooks/mystmd (package `packages/markdown-it-myst`).
Tested against markdown-it-myst 1.0.18.

## Title

perf(markdown-it-myst): split the source into lines once per parse in `computeBlockTightness`

## Body

`computeBlockTightness` in `src/directives.ts` runs `src.split('\n')` on the whole document every
time a directive fence is converted (`{note}`, `{figure}`, `{code-block}`, `{mermaid}`, ...), only
to read two lines around the fence. A parse therefore costs O(directives x document size).

On a synthetic 55,000-line document with thousands of directive fences, a CPU profile attributes
48.6% of the parse time (5.0 s of 10.4 s sampled) to this function.

### Change

Split the source once per parse state and reuse the array for every fence of that state:

```ts
const blockLinesByState = new WeakMap<StateCore, { src: string; lines: string[] }>();

function computeBlockTightness(state: StateCore, map: [number, number] | null) {
  let cached = blockLinesByState.get(state);
  if (!cached || cached.src !== state.src) {
    cached = { src: state.src, lines: state.src.split('\n') };
    blockLinesByState.set(state, cached);
  }
  const lines = cached.lines;
  // ... unchanged
}
```

The call site passes `state` instead of `state.src`. Nested parses (`nestedPartToTokens`) create
their own state, so they get their own cache entry; the `WeakMap` releases it with the state.
The returned value is unchanged for every input.

### Measurements

Parse of a 60,960-line (1.7 MB) document, median of 3 runs after 1 warm-up, Node 25, Apple
Silicon: 2,498 ms before, 460 ms after (5.4x faster). Output tokens are identical.

### Test

A test that parses a document with several directive fences and spies on
`String.prototype.split` fails before the change (one split of the source per fence) and passes
after (one split); the `tight` values (`false`, `'before'`, `'after'`, `true`) are asserted equal.
