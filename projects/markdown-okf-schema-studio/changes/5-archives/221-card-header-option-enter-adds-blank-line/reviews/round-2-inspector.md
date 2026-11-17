# CR 221, round 2: Inspector review

Worktree: `markdown-okf-schema-studio-wt-221` (uncommitted, base origin/main 0b4ede78). Reviewed
the whole diff (round 1 + round 2), including the untracked
`test/page/runtimeCardOptionEnter.test.ts`.

## Verdict: APPROVE

Round 2 resolves round-1 findings 1, 2 and 4 as the Driver decided:

- In a one-line editor, Enter with Shift or Alt (no Meta or Ctrl, no composition in progress) is
  prevented and does nothing (`src/page/features/blockSourceEditor.ts:352-358`). Cmd/Ctrl+Enter
  is excluded from that branch, so it still reaches the done branch (`:425`). Plain Enter is
  unchanged from round 1: image alt-text exit first, then save and close (`:378-383`).
- Tab and Shift+Tab are prevented and return before `indentSelection` (`:407`). The existing
  `preventDefault` keeps the focus in the text box. This matches the approved hint, which drops
  "Tab: indent".
- The slash-menu precedence is now pinned by a runtime test.

Other editors are unchanged. Every new branch is gated on `edit.singleLine`. That flag is set only
when the clicked element has `data-single-line`, there is no table cell and no `sourceRange`
(`src/page/features/blockEditor.ts:300-304`). The approved behaviours are all in place: the hint
text, no `line == endLine` detection, and an unmarked linked card.

## Checks run

- **New tests fail on round-1 behaviour.** I saved a copy of `blockSourceEditor.ts` and `git diff`.
  Then I reverted only the round-2 hunks: the Alt condition went back to Shift only, and I removed
  the Tab early return. After recompiling, 4 tests failed: Alt+Enter, Alt+Shift+Enter, Tab and
  Shift+Tab. The other 8 passed, as expected. The slash-menu test is a guard: the precedence
  already existed in round 1. I restored the file. `git diff` is byte-identical to the saved copy
  (`cmp`).
- **`just check`**: exit 0. Unit 3334/3334, the 72-test suite 72/72, pytest 153 passed. Index,
  projection and coverage checks report 0 changes.
- **`okfreq validate --check-links`**: 1072 requirements, 0 errors, 21 W2 warnings. All 21 were
  there before this change. None is in BLOCK-033 or BLOCK-258.
- **Approved requirements**: none edited. The only SwRS files changed are BLOCK-033 and BLOCK-258.
  Both are `req_lifecycle: proposed` on origin/main and in the worktree. `index.md` and `log.md`
  are generated or log files.
- **No weakened assertions.** The only existing assertion that changed is the e2eGroups count,
  from 410 to 411, with a reason.
- **Test quality.** Each new test checks that the key was taken over (`preventDefault` count), the
  text is unchanged, there was no final save, and the editor is still open (the status line). The
  Shift+Tab test starts from an indented line, so an outdent would show up. The paragraph and
  heading guard tests also check that Tab still indents and that Enter and Shift+Enter are not
  prevented.

## Findings

### Blocking

None.

### Non-blocking

1. **Inaccurate code comment** (`src/page/features/blockSourceEditor.ts:351`). It says
   "Cmd/Ctrl+Enter is done earlier", but Cmd/Ctrl+Enter is handled later in the same listener
   (`:425`). The branch's `!event.metaKey && !event.ctrlKey` is what lets it through. Suggest
   "handled below".
2. **Stale doc comment** (`src/page/features/pageRuntime.ts:127-131`). The `BlockEdit.singleLine`
   comment still says only "Enter is done, Shift+Enter does nothing". Round 2 also ignores
   Alt+Enter and Tab/Shift+Tab.
3. **Odd line wrap in the requirements log** (`requirements/tiers/log.md:9-12`). The phrase
   "new scenarios for Enter and for one-line paragraphs…" breaks after "one-line" and leaves a
   short line. The 100-column clause-boundary wrap rule is not followed.
4. **Round-1 finding 3 still stands, and BLOCK-258 has grown**
   (`requirements/tiers/swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-258.md:5, 9-17, 46`). The title
   still names only the click and the inline title. The SHALL now adds a second behaviour: key
   handling in the one-line card editors (Enter, Shift/Alt+Enter, Tab/Shift+Tab). This is
   acceptable while the requirement is `proposed`. Consider a separate proposed SwRS, or a broader
   title, before approval.
5. **Wording gap between the normative text and the table**
   (`SwRS-MDOKFSTUDIO-BLOCK-258.md:46` vs the table). The SHALL says Shift+Enter and Alt+Enter
   "insert nothing". The table also says they save nothing and the editor stays open. The tests
   check both. Adding "and leave the editor open" to the SHALL would make the table and the
   normative text agree.
6. **Coverage carried over from round 1.** These are not regressions:
   - The E2E covers only the `:header:` line.
   - Removing the marker in tab items has no test (`src/core/render/mystGridToctree.ts:380`).
   - Alt+Enter and Tab are covered at runtime-harness level only. I did not confirm Chromium's
     native Alt+Enter behaviour in a real browser.
