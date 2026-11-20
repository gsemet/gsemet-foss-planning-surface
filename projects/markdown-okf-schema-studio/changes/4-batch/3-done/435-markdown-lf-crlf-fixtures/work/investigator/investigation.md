# Investigation CR-435

## 1. Fixtures
- Tracked CRLF files: none (git ls-files --eol: 0 i/crlf, 0 i/mixed). Only candidate:
  .agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/crlf-source.md (i/lf). Its line 7 and
  scripts/setup-workspace.sh:44-46 say it is converted to CRLF at setup (perl, as synth/crlf.md) and the
  source removed: so ux-35 (file synth/crlf.md) already runs on CRLF IF setup ran. The request's premise
  "ux-35 edits an LF file" is only true if the workspace was not built by setup-workspace.sh. Verify by
  running setup and `file`/od on crlf.md.
- Other CRLF content is built in memory (replaceAll/\r\n) in tests: crlfAlerts, sourceEdits, blockReq (l.526),
  blockRangeGuard, listItemMove, markdownTable*, tableInContainer, integration/inlineThread, qa210Replays.
- .gitattributes: `* text=auto eol=lf` then LFS rules. Keep-CRLF rule must come AFTER, e.g.
  `**/*.crlf.md -text` (bytes untouched, no conversion either way; best, works with any autocrlf) or
  `eol=crlf` (checkout CRLF, stored LF: NOT byte-stable in repo, a Linux test reading would still see CRLF
  only via attribute; -text is stronger). Naming convention needed: e.g. test/fixtures/line-endings/*.crlf.md,
  *.mixed.md, *.lf.md. Then `git add --renormalize .` (expected to change nothing; run to prove).
  Note: the skill's crlf-source.md could become a real CRLF `crlf.md` fixture, dropping the perl step.

## 2. Tests, smallest layer
- The stuck-Saving bug is in the PAGE (blockEditor.ts postBlockEditSave: textarea turns \r\n to \n, compares to
  originalText) plus host no-reply path. Smallest layer for "ends, no stuck": page runtime tests,
  test/page/runtimeBlockEditor.test.ts (1446 lines, limit 1500: add a NEW file, e.g.
  test/page/runtimeBlockEditorLineEndings.test.ts, using runtimeHarness/runtimeTestSupport openBlockEditorWithSource,
  sourceReply). Assert: no "Saving Markdown..." left / finishing reset after Done on an unchanged CRLF block.
- Byte level: test/session/blockReq.requirements.test.ts (581 lines; fixture({text}) + run.send previewEditSave,
  run.document.getText()) already covers CRLF for list (l.~498-523) and last-block (l.526). Add: open two blocks
  of a CRLF / LF / mixed text, edit block A with LF editedText, leave B, assert getText() == expected exact bytes.
  Core: test/core/edits/sourceEdits.test.ts (withLineEndingOf, planBlockTextEdit) cheap CRLF/LF/mixed matrix.
- Would FAIL on current main: page-level CRLF "unchanged block then Done" (originalText CRLF vs textarea LF ->
  finishing stuck, posts final save) -- this is CR-436's bug; host test "unchanged final save gets an answer"
  (no reply today). Probably GREEN guards on main: core/session byte-preservation for CRLF, LF, mixed (withLineEndingOf
  already normalises). Real-file variant: read fixture bytes from disk (fs.readFileSync) so an LF-planted
  fixture makes it fail. Integration (test/integration, real VS Code) only for CRLF fixture on disk: optional,
  qa210Replays/inlineThread already use \r\n.
- CR-435 owns fixtures + guard + CRLF tests; the "ends" tests that fail on main belong with CR-436's fix (mark
  them, or land them expected-red in order: CR-436 first or same stack).

## 3. Requirements
- Line-ending preservation lives in block-editing SwRS: BLOCK-042 (autosave smallest replacement), 014, 058, 094,
  117, 124, 127, 129, 169, 174, 216, 227, 232-239 (234 = CRLF last block). Smallest change: extend BLOCK-042 or
  add a new SwRS BLOCK-NNN "a block save keeps each line's ending, final save always ends" derived from
  StRS-MDOKFSTUDIO-BLOCK-006/025 (StRS approved => owner-reapproval rule, avoid editing StRS). Frontmatter:
  implemented_in_files/tested_in_files lists + `@tests_req <ID>` comment directly above EACH test (max 3 IDs per
  block, not in file headers), `@implements_req` at code. Then `just requirements-update`, dated entry in
  requirements/tiers/log.md. Read requirements/guidelines/project.guidelines.md "During a change".

## 4. Guard test
- New test/build/lineEndingFixtures.test.ts (test/build holds repo-meta tests): (a) for every tracked file matching
  *.crlf.md / listed fixture, bytes contain \r\n and no bare \n (or for *.mixed.md both kinds); (b) run
  `git check-attr text eol -- <fixtures>`: expect `text: unset` (or eol crlf) -- fails if the rule is removed;
  (c) tracked *.md elsewhere hold no \r (git ls-files --eol i/lf). Must be added to the unit glob (test/build/unitGlobs.test.ts
  checks it). Limits: src 800 lines, tests 1500 (scripts/check-file-sizes.mjs, baseline file-size-baseline.json); keep new
  files small. Windows: tests must not rely on autocrlf; read with fs buffers.

## Risks / questions
- Premise question for owner: ux-35 may be already CRLF via setup-workspace.sh; is the scenario rerun just to prove it?
- Fixture-in-a-file vs in-memory: owner asked "kept CRLF" so create real files.

## Evidence plan
Kind: tests + repo config. Before/after: (1) `git ls-files --eol <fixtures>` shows i/crlf w/crlf (before: no file);
`git check-attr` output; `git add --renormalize .` diff empty/committed. (2) Run new tests with `node scripts/node-test.mjs`
(or the project's unit command) green on fixed code; red proof: run them on main (git stash-free: checkout the base in
a temp worktree or revert the fix hunk) and with a planted LF-converted fixture, logs in evidence/*.log. (3) ux-35
rerun with the exploratory-QA skill on a real CRLF crlf.md (od -c head showing \r\n before/after save, diff of bytes).
`just check` + `just requirements-update`; preflight static on Windows. Cannot show: real VS Code stuck-Saving UI
without CR-436's fix (screenshot belongs to CR-436).
