# CR 221, round 3: Inspector review

Worktree: `markdown-okf-schema-studio-wt-221` (uncommitted, base origin/main 0b4ede78). Reviewed
the whole diff (rounds 1 to 3), including the untracked `test/page/runtimeCardOptionEnter.test.ts`.

## Verdict: APPROVE

Round 3 changes only comments and requirement wording, as planned. It resolves round-2
non-blocking findings 1, 2, 3 and 5, and partly resolves 4: the title is now broader.

## Checks

- **No behaviour change.** The only `src/` edits in round 3 are comments. The single-line
  branches in `src/page/features/blockSourceEditor.ts` sit on the same lines that round 2
  reviewed: the Shift/Alt+Enter branch at `:352-358`, plain Enter at `:379-383` and the Tab early
  return at `:407`. The conditions are unchanged: Shift or Alt, no Meta or Ctrl, no composition.
- **Comments are accurate now.**
  - `blockSourceEditor.ts:350-351` now says "plain Enter and Cmd/Ctrl+Enter are done below". That
    is true: plain Enter is handled at `:379` and Cmd/Ctrl+Enter at `:425`.
  - The `BlockEdit.singleLine` doc in `src/page/features/pageRuntime.ts` now lists every key: plain
    Enter saves like Done, Shift+Enter and Alt+Enter do nothing, and Tab and Shift+Tab do
    nothing.
- **BLOCK-258 is consistent.**
  - The frontmatter `description` and the body text under `### Normative behavior` are the same
    text (whitespace-normalised comparison).
  - The title "A click on a card title or option opens a one-line editor on its own line, where
    Enter saves" matches the `##` heading exactly. It also matches the generated link titles in
    `requirements/tiers/swrs/block-editing/index.md` and `StRS-MDOKFSTUDIO-BLOCK-001.md`.
  - No stale copy of the old title remains in `requirements/`, `src/` or `test/`.
  - The SHALL now says Shift+Enter and Alt+Enter "insert nothing, save nothing and leave the
    editor open", in line with the table.
- **Lifecycles.** Every changed requirement file is `req_lifecycle: proposed` on origin/main and
  in the worktree:
  - `requirements/tiers/strs/block-editing/StRS-MDOKFSTUDIO-BLOCK-001.md`: proposed (generated
    link title only)
  - `requirements/tiers/swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-033.md`: proposed
  - `requirements/tiers/swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-258.md`: proposed
  - `requirements/tiers/swrs/block-editing/index.md`: generated index, no lifecycle
  - `requirements/tiers/log.md`: update log, no lifecycle

  None of the locked approved StRS appears in the diff: CORE-001, GFM-002, MYST-001, DIAG-001,
  DIAG-006, REVIEW-001, REVIEW-003, REVIEW-012, REVIEW-015, BLOCK-003, BLOCK-025, PALETTE-015,
  TABLE-001, TABLE-012, LAYOUT-001 and LAYOUT-003 are all unchanged.
- **`just check`**: exit 0. Unit 3334/3334, the 72-test suite 72/72, pytest 153 passed. Index,
  projection and coverage checks report 0 changes.
- **`UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`**:
  1072 requirements, 0 errors, 21 W2 warnings. These are the same warnings that were there before
  this change. None is in BLOCK-001, BLOCK-033 or BLOCK-258.
- **Diff is coherent.** The CHANGELOG, the log entry, BLOCK-033 (hint), BLOCK-258 (SHALL, table,
  scenarios, verification notes and file lists), the renderer marker, the sanitizer allowlist, the
  `singleLine` gate in `blockEditor.ts`, the key handling and the tests all describe the same
  behaviour.

## Findings

### Blocking

None.

### Non-blocking

1. **One log line is over 100 columns** (`requirements/tiers/log.md:15`, 107 characters). The
   "Verification:" line runs past the limit because two long paths share it. A wrap after
   `runtimeCardOptionEnter.test.ts,` would fix it. Round 3 fixed the wrap at lines 9-12. Several
   older entries in the same log are also over 100 columns, so this is cosmetic.
2. **Round-2 finding 4, carried over.** BLOCK-258 still holds two behaviours: the click mapping
   and the one-line key handling. The broader title now names both, which is enough while the
   requirement is `proposed`. A split could be considered before approval.
3. **Round-2 finding 6, carried over.** These are coverage notes, not regressions:
   - The E2E covers only the `:header:` line.
   - Removing the marker in tab items has no test.
   - Alt+Enter and Tab are checked at runtime-harness level only.
