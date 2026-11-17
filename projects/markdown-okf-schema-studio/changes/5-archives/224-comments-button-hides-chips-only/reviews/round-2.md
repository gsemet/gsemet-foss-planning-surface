# Review round 2 — CR 224 (Comments button hides every review mark)

Inspector, independent review of the uncommitted change in
`markdown-okf-schema-studio-wt-224` (base origin/main 0b4ede78).

Verdict: APPROVE

The round-1 findings 1 to 4 are fixed. The new setting-path test is sound and fails without the
hostHandlers call. Two doc nits remain; they can go in with the PR or be left.

## Round-1 findings

1. **Setting path not tested: fixed.** The new test in `test/page/runtimeCommentsHidden.test.ts`
   opens the popover, sends `previewShowComments` false, and checks three things: the popover is
   removed, a click is plain text (not swallowed, one `previewReveal`), and `true` brings the
   popover back. I checked that it fails on a scratch copy outside the worktree with
   `parts.commentThreads.visibilityChanged()` deleted from `src/page/features/hostHandlers.ts`.
   It fails with "the setting turned off: the open popover is removed", and the other two tests
   pass. It is tagged `@tests_req SwRS-MDOKFSTUDIO-REVIEW-152`. The Tab order on the setting path
   is not covered at runtime level, because the harness has no text nodes. REVIEW-152 says this
   under "Untested", and the module test covers it. Acceptable.
2. **User docs: fixed.** The changes cover `docs/user/toolbar.md`, `docs/user/settings.md`,
   `docs/user/review-comments.md`, the `CHANGELOG.md` Unreleased entry, and the `settingsRegistry.ts`
   description. `package.json` is regenerated from the registry and the two match
   (`check-settings: passed (19 settings)`). The wording matches the behaviour note. The CHANGELOG
   entry follows the file's style: a plain present-tense user sentence, wrapped at 100.
3. **REVIEW-152 verification notes: fixed.** There is a new Method line for the setting test. The
   "Untested" line now names only the runtime Tab order, the layout shift and the compose button.
   The Criteria now name "the previewShowComments message of the setting".
4. **Fixed waits: fixed.** `check_comment_marks_hidden` now uses `wait_for_function`, both on the
   attribute flip (`press_and_wait`) and on "a reveal or a popover" after the click. It has no
   `wait_for_timeout` left. The older checks keep theirs, which is out of scope.
5. **File size (nit): no change, as expected.** Still worth a backlog line for splitting
   `commentThreads.ts`.
6. **PR names the approved requirement (nit): still open, driver's job.** The PR body must list
   StRS-MDOKFSTUDIO-REVIEW-012 (approved; only the generated links block changed).

## New findings

1. **nit — line over 100 characters** (`docs/user/settings.md:26`, 114 characters). The rewrap of
   the old broken line ("chips in open" on its own line) left one long line. Rewrap at a clause
   boundary. `docs/user/review-comments.md:13` is 101 characters; the same applies.
2. **nit — "them" in settings.md** (`docs/user/settings.md:25`). The sentence "The Comments button
   of the toolbar hides and shows them" still points to the gray chips only. The next sentence says
   that the setting hides every review mark, so the button reads as narrower than the setting.
   Suggestion: "hides and shows them and the review marks", or move the list of review marks into
   the button sentence.

## What I checked

- The full diff and the untracked files (`test/page/runtimeCommentsHidden.test.ts`,
  `test/visual/reviewMarksHiddenScenarios.ts`). The code is unchanged since round 1, apart from the
  docs and the description. No regression found.
- Requirements:
  - Only SwRS-REVIEW-152 and SwRS-REVIEW-021 (both `proposed`) are hand-edited.
  - StRS-MDOKFSTUDIO-REVIEW-012 (`approved`) differs by one line, inside the generated
    `okf:links` block (the new SwRS title).
  - The index, projection and coverage checks report 0 would change.
- Gates (run by me):
  - `env -u VIRTUAL_ENV UV_NO_CONFIG=1 just check` exits 0:
    - unit: 3327/3327 pass (+1 since round 1);
    - security: 71/71 pass;
    - contracts: 0 tests, as on main;
    - boundaries, limits, markers, exports and settings pass;
    - requirements lint: 0 changes.
  - `okfreq validate --check-links`: 1072 requirements, 0 errors, 21 warnings. The warnings are
    older and in other files.
- I ran no visual captures. The visual check change replaces sleeps with polling and needs no new
  shots.
