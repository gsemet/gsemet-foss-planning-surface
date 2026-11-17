# CR 228 — round 2 Inspector review

Worktree `markdown-okf-schema-studio-wt-228`, branch `change-requests/228-promote-qa-210-replays-to-e2e`,
base `e1005766`, uncommitted diff (11 files modified, 1 new `test/integration/realInput/qa210Replays.ts`).
Read-only review. No real-window test was run. Round 2 touched only `qa210Replays.ts`; the other
files are as reviewed in round 1.

## Round-1 nits

| Nit | Status |
| --- | --- |
| 1. c6-2 fillers | Fixed. The 520 fillers are gone. A precondition computed from the workspace replaces them (`qa210Replays.ts:239-259, 270`). See section 7. |
| 2. ux-35 stale check | Fixed. "No stale" is now checked while the editor is still open after autosave, before the commit click (`:432-437`), as in the replay. |
| 3. Mapping not in repo | Fixed. The header table (`:31-54`) lists all 18 replays, c5-1 and c7-1 included. It matches the round-1 mapping table. |
| 4. c6-2 without `withDocument` | Fixed. It uses `withDocument(..., LINK_HINT_SCHEMA)` (`:268, 293`), so it gets the focus dump. `writeSchema` puts the schema in `<fixture>/_schema` (`common.ts:133`). |
| 5. Step budget | Fillers removed, so the extra time drops (coder estimate ~40 s). Still worth a look on CI. |

## 1. Mapping honesty

Unchanged since round 1, and the new header table agrees with it. No coverage is claimed wrongly.

## 2. New and extended scenarios

Round-1 findings still hold for c1-1, c1-2, c3-1, c4-1, c6-3, ux-16 and ux-17. Round-2 deltas:

- **c6-2** (`:267-294`). The journey is unchanged: table link click, list editor, `X` warns, Backspace
  clears it, Escape, buffer unchanged. Before a123bf4e the editor checked values against `stems(500)`,
  the first 500 stems in sorted order. The precondition proves the target falls outside that cut, so
  `:288` fails on the old code. On HEAD, `nearestStems` puts the same-folder target first. The `known`
  list is sent once the dropdown is capped (`okfFrontmatter.ts:454-458`).
- **ux-35** (`:420-447`). The flow is: wait for the autosave to bring both lines into the buffer
  (`:432`), assert the editor is still open (`:434`), assert no "stale" (`:436`), commit click, wait
  for the rendered alert to show the new line (`:439`), then the CRLF checks.
  - This is race-free. A stale refusal would keep the buffer from updating, so a buffer that holds
    both lines means the last autosave was accepted. Renders are deferred while editing
    (`hostEvents.ts:199`, `deferWhileEditing`), so the open-editor assert is stable on HEAD. The
    final buffer read happens after the committed render, which reflects the buffer.
  - The replay used `aside.admonition` and fixed waits. The test uses `aside[data-okf-github-alert]`
    and condition waits. Same journey, and stricter.

No injected messages and no direct state writes. The c6-2 target file is written next to the fixture,
the same pattern as `scenarioListEditorClickAndKeys` (`frontmatterFields.ts:141-145`). No fixed sleep.

## 3. Weakening

- No existing assertion is weakened.
- No timeout is raised.
- No retry loop, no `force: true`, no skip.

## 4. Conventions

- Inline fixtures through `withDocument`/`createFixture` under `test/integration/fixtures/` follow
  the repo convention (round 1).
- `@tests_req` markers are present on all 7 new scenarios.
- `run.ts` wiring is unchanged since round 1.
- `check:limits` passed.

## 5. SwRS

- The 8 SwRS files each gain one `tested_in_files` line, and nothing else changed.
- Lifecycles: 7 are `proposed`, TOOLBAR-012 is `draft`. None is approved.

## 6. Gates (run by the Inspector)

| Gate | Result |
| --- | --- |
| `npm run check-types` | clean |
| `just check` | exit 0 |
| Unit tests | 3455/3455 |
| Untrusted manifest tests | 73/73 |
| pytest | 153 passed |
| `check:limits` | passed (917 files, 0 on baseline) |
| `check:exports` | no unused export in 315 modules |
| `check:markers` | 3 companion files ok |
| Format | 0 files would change |

## 7. Round-2 specifics

**c6-2 precondition: honest.**

- Same roots as the extension:
  - The precondition calls `resolveFrontmatterLinkRoots(...).filenameRoots`, the function
    `filenameStemSuggestions` uses (`fileLinks.ts:167-168`).
  - Its workspace roots are `vscode.workspace.workspaceFolders`, the same source as `sessionRoots`
    (`sessionFactory.ts:82`).
  - It passes `schemaDirectory = <fixture>/_schema`, where `withDocument` writes the schema.
  - It leaves out a configured `bundleRoot`/`projectRoot`. Extra roots only add stems, and added stems
    can only push the target further down, so the precondition errs on the safe side.
- Same sort: `stems()` is the plain `.sort()` that the old `stems(500)` cut used (a123bf4e diff of
  `stemIndex.ts`). The cap of 500 matches the old `limit = 500`.
- It fails when the target is missing or when fewer than 500 stems sort before it. It never skips.
- On CI the workspace is the repo plus `/tmp` (`run-tests.ts:99-106`). The fixture lives under the
  repo (`test/integration/fixtures`, not an excluded folder name), so it is indexed.
- It builds a fresh `MarkdownStemIndex`, not the cached one, so it does not touch the extension's
  cache.

**Importing `src/core` from an integration test** follows precedent: `radioChoice.test.ts:14` and
`stockCoexistence.test.ts:15` import values from `src/`. `tsc` compiles it (check-types clean, and
tsconfig includes `test/**`).

## Nits (not blocking)

1. **Synchronous index walk** (`:253`). The precondition walks the repo and `/tmp` once, synchronously,
   on the extension host. The extension does the same walk anyway, and this costs a second or less on
   CI. Acceptable, but if CI `/tmp` grows large this is where time goes.
2. **Watcher lag on the new target file** (`:269`). The target is written right before the preview
   opens. If the cached index is not invalidated in time, the first render may not resolve the link.
   `waitFor` at `:275` covers a later resolve, and t21 uses the same pattern successfully. This is a
   low risk, noted only for CI triage.

VERDICT: APPROVE
Must-fix: none.
