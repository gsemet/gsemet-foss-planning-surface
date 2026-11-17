Verdict: APPROVE

# S8b, round 2: internals and tests (REVIEWER)

I reviewed the whole uncommitted worktree against HEAD `2516aa1` on
`changes-requests/056-refactor-host-neutral-core`. The review was read-only. I wrote only this file
and scratch scripts in my scratchpad. For the parts that did not change since round 1, I rely on
`reviews/S8b-r1.md`. In round 2, only `CONTRIBUTING.md`, `sameData.ts`, the doc comment in
`pageToHost.ts` and the two frontmatter tests changed.

## Gates (worktree, Node 24.22.0 via `fnm exec --`, foreground)

| Gate | Result |
| --- | --- |
| `npx tsc -p .` | exit 0 |
| `npm run test:unit` | 2 306 / 2 306 pass |
| `UV_NO_CONFIG=1 UV_OFFLINE=1 just check` | exit 0, pytest 31 passed (the `rm_rf` warnings are temp-dir noise from before) |
| `npm run bundle` | exit 0, `preview.js` is 287.1 kB |

I did not run integration. The driver handles it.

## F1: resolved

`src/core/frontmatter/sameData.ts` now keeps one path memo per side (`Map<object, depth>`). The
memo is threaded through arrays, keys, symbols, `Set` and `Map`, and entries are removed in
`finally`. The public signature is unchanged.

- **Crash fixed:** recursive aliases no longer overflow the stack.
- **Tests:**
  - `sameData.test.ts` adds 8 cyclic YAML sources. They cover self and two-level cycles,
    unrolled-equal and near-miss pairs, shared aliases and nested anchors. The all-pairs comparison
    against `util.isDeepStrictEqual` passes on both the parsed values and their `structuredClone`s.
  - The new `okfFrontmatter.test.ts` test asserts the exact minimal patches for set, insert, remove
    and rename.
    - The coder showed that the test fails on the round-1 code: set reformats the whole block, and
      remove and rename throw `RangeError`.
    - The coder checked the expected values against a HEAD build. They match the HEAD rows in my
      round-1 table.
- **My fuzz** (independent, in the scratchpad): I compared the function with Node 24
  `isDeepStrictEqual`.
  - **Hand cases, both argument orders:** 1-cycle vs 2-cycle (objects, arrays, maps), mutual vs
    self, mutual vs mutual, self vs shifted self, and a self-containing `Set`. All 16 comparisons
    agree.
  - **Random cyclic graphs:** 1.5 M random pairs. They agree except for 32 pairs, and every one
    goes the same way: Node returns `true` and `isSameData` returns `false`. The minimal case is
    `a = {k0: s}` with `s = {k0: s}`, against `b = {k0: {k0: b}}`. Here the root is part of the
    cycle on one side only. Node 24 accepts a pair when both objects are anywhere on the path.
    `isSameData` also requires both to be at the same depth.
  - **The other direction:** I found no pair where `isSameData` says equal and Node says different.

## F2: resolved

The "Add a message" recipe in `CONTRIBUTING.md` matches the code:

| Recipe item | Where it is in the code |
| --- | --- |
| Page-to-host validator table, typed by the union | `PAGE_TO_HOST_VALIDATORS` at `pageToHost.ts:540`, `{ [T in PageToHostType] }` |
| Host-to-page rules (`render`, `document`, `own-id`), typed by the union | `rules` in `createHostMessageFilter` at `hostToPage.ts:325` |
| Gates, typed by the union | `PAGE_MESSAGE_GATES` at `src/session/pageMessages.ts:43` |
| Host handlers registered with `router.on` | `src/session/features/*` (history, comments, ...) |
| Page handlers registered with `hostMessages.on` | `src/page/features/hostHandlers.ts` |
| Host sends with `preview.postToPage` | session features |
| Page posts through `PageHost` | `src/page/pageHost.ts` |
| Handler count pinned at 41 | `test/session/previewManager.test.ts:20` |
| Protocol tests | `test/core/protocol/pageToHost.test.ts`, `hostToPage.test.ts` |

The stale `src/extension.ts` reference in the `pageToHost.ts` doc comment is fixed, and the palette
recipe now names the subject modules.

## Findings

### N1: low, not blocking: the "same answer as `isDeepStrictEqual`" claim is slightly too strong for cyclic graphs

`src/core/frontmatter/sameData.ts:2-8` and line 106. On cyclic input whose cycle starts at a
different depth on each side, `isSameData` is stricter than Node 24 (see the fuzz above). It is
never laxer.

- **In practice:** in `verified()` (`frontmatterSerialize.ts:302`), a stricter answer can only
  turn a minimal patch into the whole-block fallback, which is still correct. To reach it, the
  candidate text would have to change the alias topology while keeping the unrolled data, and a
  minimal text edit keeps the anchors. The recursive-alias test shows the real case matches HEAD.
- **Optional fix:** reword the doc as "the same answer for acyclic data and for cycles of the same
  shape; stricter, never laxer, when the cycles are shifted".
- **The coder's report:** it says the 640 000-pair fuzz found 0 differences. That generator
  probably never placed the root inside a cycle on one side only.

### Carried over (info)

- The PR text must list "CSS stays as TypeScript modules" under "Autonomous decisions" (round 1,
  I1).
- Real VS Code integration is still to run, by the driver, before the PR is marked ready.
- Do not stage `.venv`. The 76-path staging list in `reports/S8b-r2.md` matches `git status`
  (minus `.venv`).
