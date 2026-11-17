# CR 228 — round 3 Inspector review

Worktree `markdown-okf-schema-studio-wt-228`, HEAD `6cb3bd2e` (stack top, contains `edce238a` and
`6cb3bd2e`). Under review: the uncommitted diff against HEAD. Rounds 1–2 are staged. Round 3 is
unstaged: `qa210Replays.ts` (+118/-10) and `SwRS-MDOKFSTUDIO-LAYOUT-043.md` (+1).

## 1. c7-1: the decision to add a scenario

**The "not covered by v88" reasoning is true.**

- v88 (`test/visual/toolbarFloatScenarios.ts`, `layout-width/v88-…-393`) is not a `freshWorkspace`
  page. Every such page gets `PINNED_WORKSPACE_CHOICES.toolbarCollapsed: false`
  (`test/visual/renderOptions.ts:80-84`). So v88 only checks a page that loads with the rows
  already shown.
- In the real extension the default is collapsed: `DEFAULT_VIEW_PREFERENCES.toolbarCollapsed: true`
  (`src/core/state/previewViewPreferences.ts:34`), and
  `toolbarCollapsed !== false` → collapsed (`src/page/modules/toolbarCollapse.ts:47-49`).
- The replay expands the toolbar by clicking `Show view controls` after the render
  (`c7-1-toolbar-covers-first-lines-narrow.json`, step 5).
- After that click, the float only appears through the re-measure path:
  - the click handler calls `onChange()` (`toolbarCollapse.ts:136-158`);
  - `transitionend` on height also calls it (`:63-65`);
  - the ResizeObserver and MutationObserver on the toolbar fire too (`firstClearance.ts:310-321`).

  No visual scenario covers this path. Adding a real-input scenario was the right call.

**Faithful to the replay, real input only.**

| Replay step | Scenario |
| --- | --- |
| Open Preview to Side | `openSidePreview` |
| Wait for the h1 | `waitForRender` |
| `innerWidth <= 460` | Asserted (`qa210Replays.ts`, `width <= 460`) |
| Click Show view controls (optional) | Real `locator.click()`. If the toolbar is already expanded, it first collapses it with a real click, so the expand always goes through a click |
| Wheel to the top | Asserted `scrollY === 0` instead (a fresh document opens at its top) |
| Paragraph line boxes ∩ toolbar = ∅ | Same range/`getClientRects` test, on the h1 too. The anchor icon is excluded the same way v88 does it |

- It uses no `evaluate`-driven state change, no `force`, no retry.

**It fails before `edce238a`.**

- Without the float, the paragraph's line boxes run across the whole column, under a toolbar more
  than 120 px tall.
- So the wait "no h1/p line box under the toolbar" times out.
- A paragraph that slid below the toolbar is no escape either: the follow-up `besideToolbar`
  assertion fails, as the v88 assertion does.

**It plausibly passes after the fix.**

- The toolbar is a column of 30 px buttons (`pageChromeStyles.ts:205-213`, `:378-382`), so the float
  is narrow.
- The heading wraps beside it, and the paragraph still starts above the toolbar's bottom.
- v88 asserts the same thing at 393 px, with the same chapter-opening text. The scenario runs at
  about 426 px, which gives more room.

**Flake review.**

- **Viewport math.**
  - The window is 900 px wide, and `run.ts:156-158` closes the sidebar and the auxiliary bar.
  - The side preview is then about (900 − activity bar) / 2.
  - Precedent: `frontmatterFields.ts:304-311` uses a 1100 px window and asserts a 480–620 px frame,
    consistent with this.
  - The `<= 460` assertion fails loudly rather than by chance. The toolbar height does not depend
    on the width (flex column).
- **Animation.**
  - The wait checks two things: `data-sphinx-preview-toolbar-animating` is absent (it is removed
    after 200 ms, `toolbarCollapse.ts:76-88`), and the toolbar is taller than 120 px.
  - With reduced motion, no mark is ever set, so the wait still ends.
- **The load hint.** A collapsed toolbar unrolls on load for 700 ms. Both cases are handled:
  - A click during the hint keeps the rows open and flips the state to expanded
    (`endHint(false, collapsed)`, `:138-141`). The hint never changes
    `data-sphinx-preview-toolbar-state`.
  - After the click, `startHint` returns early because the toolbar is no longer `collapsed`.
- **Edit mode.** `withDocument` calls `leaveEditModeOff()` after every scenario
  (`common.ts:103-116`, `:140-142`). So c7-1 starts in view mode, whatever the alert scenario before
  it left behind.
- **Restore.**
  - The inner `finally` puts the stored toolbar choice back by real click, before `withDocument`
    closes the editors.
  - The outer `finally` restores 1400×900, the default from `run.ts:156`.
  - Later scenarios that care about the toolbar, such as `blockKeys.ts:173`, handle both states
    anyway.

## 2. c6-2: the precondition is deterministic

**(a) It does not depend on `/tmp`, and untracked files can only make it stronger.**

- It now indexes `[repository]` only, with `REPOSITORY_ROOT = ../../../..` from `out/test/integration/realInput`.
  That is the repository root, the same expression as `harness.ts:20` and `previewWindow.ts:43`.
- Untracked repository files only add stems.
- I counted the tracked Markdown stems under directories the index does not exclude (dot folders,
  `out`, `node_modules` and so on, per `stemIndex.ts:4-12,46-48`): **1213 unique stems**, none
  `>= "zz"`. That matches the Coder's figure and is well above the cap of 500.

**(b) The sort and dedup claims are true.**

- `stems()` is `[...candidatesByStem.keys()].sort()`, the default UTF-16 code-unit order, which is a
  total order (`stemIndex.ts:67-70`).
- `candidatesByStem` is a `Map` keyed by stem, so each stem appears once (`:146-148`).
- The extension uses `filenameRoots` = workspace roots plus `bundleRoot` (`fileLinks.ts:153`), a
  superset of `[repo]`. The root `roots.includes(repository)` check (both sides realpath'd) proves it.
- In a superset, every stem that sorts before the target is still present. So the target's position
  can only grow.

**(c) A `/tmp` file sorting after the target, or holding the same stem, cannot affect the result.**

- The warning tests membership in `known = index.stems()`, the full list, not the cut
  (`fileLinks.ts:167-172`). A stem that sorts after the target changes neither membership nor
  position.
- The suggestions use `nearestStems`, so stems in `/tmp` sit far from the fixture folder.
- Only an identical stem could matter: two paths could make the table's link resolve to more than
  one file.
- The token makes that practically impossible:
  - The stem is `zz-qa210-c6-2-link-hint-target-<pid36>-<ms36>`.
  - `index.get(target).length === 1` checks it inside the repository.
  - The fixture folder is disposed (`common.ts:144`), so no stale copy is left behind.

**(d) The token.**

- It is a module-level `const`, evaluated once per extension-host process, so it is stable for the
  whole run.
- The same value goes into the frontmatter, the file name and the precondition.
- The journey still works:
  - `End` → `X` gives `<target>X`, which no file holds, so the warning shows.
  - `Backspace` brings the value back to `<target>`, so the warning clears.
  - The length of the stem plays no part.

**(e) The repository is a link root on CI.**

- `run-tests.ts:14` sets `workspaceRoot = extensionRoot`.
- `run-tests.ts:101-106` defines the folders as `[workspaceRoot, "/tmp"]`.
- So the repository is the first workspace folder, and the `roots.includes(repository)` assertion
  holds.

## 3. Rebase sanity

`run.ts` has CR 227's `scenarioWideTableTab` import (`:40`), its `wide-table-tab` single entry (`:71`)
and its sequence call (`:217`). It also has this CR's import (`:43`), the `qa210-replays` single entry
(`:171-173`) and the sequence loop (`:230`). The diff against HEAD contains only additions (+6), so
nothing was lost.

## 4. Integrity

- No `force: true`, `.skip`, retry or raised timeout appears in any added line.
- The `linkEditMode.ts` and `textEditing.ts` changes only add assertions.
- The SwRS changes are one `tested_in_files` line each, nine files in total.
- LAYOUT-043 is `req_lifecycle: proposed` (line 14). None of the nine is approved.
- `@tests_req SwRS-MDOKFSTUDIO-LAYOUT-043` is on the new scenario, and `update-coverage --check`
  reports 0 changes.

## 5. Gates (run by the Inspector)

| Gate | Result |
| --- | --- |
| `npm run check-types` | clean |
| `just check` | exit 0 |
| Unit tests | 3465/3465 |
| Contract tests | 0/0 |
| Security tests | 73/73 |
| pytest | 153 passed |
| `check-boundaries` | 315 modules |
| `check-limits` | 921 files, 0 on the size baseline |
| `check-exports` | no unused export |
| `check-markers` | 3 ok |
| `check-settings` | 19 |
| okfreq | 0 indexes, 0 projections, 0 files would change |

- I ran `just --fmt --check` first: the justfile was already formatted, so `just check`'s format
  step did not write anything.
- The worktree status was identical before and after the run.

## Nits (not blocking)

1. In `scenarioToolbarExpandKeepsFirstLinesClear`, a `null` initial toolbar state skips the restore
   but still clicks to expand. The cast `initial as "expanded" | "collapsed"` hides this.
   `waitFor` would have already failed in that case (the state stays `null`), so this is harmless.
2. Carried over from round 2: the extension's cached stem index is keyed on the root's mtime. A
   target written in a nested fixture folder relies on the watcher invalidation. The `waitFor` on
   the table link covers this.

VERDICT: APPROVE
Must-fix: none.
