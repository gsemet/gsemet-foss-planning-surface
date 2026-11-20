# Verify CR-431

Head: b2bdd7217bd127ebdeb1165416aee227d505b8b9

Gate pass cited: work/gates/20261120-130618.log, first line `gate CR-431 branch chantier/batch-06/cr-431-code-requirement-mismatches-found-by-bat head b2bdd7217bd127ebdeb1165416aee227d505b8b9` (`just preflight`).

## Claims (all judged at b2bdd72)

1. CORE-025, the code now follows the SwRS. Command at the head: `npx tsc -p tsconfig.json` then
   `node scripts/node-test.mjs unit out/test/host/coreReq.requirements.test.js`. Output: 7 tests,
   7 pass, 0 fail, including the throws-undefined, throws-null, empty-message Error and later-render
   (stale, "The latest render failed.") tests. PASS.
2. CORE-025, the four new tests fail on the base. I could not capture my own before: the detached
   worktree of the base failed at checkout (`git worktree add --detach <CR>/work/scratch/base e05f0b51`:
   `error: unable to create file .agents/skills/markdown-studio-exploratory-qa-claude/scenarios/...json:
   Filename too long`, `fatal: Could not reset index file to revision 'HEAD'`), a stop per the card; I
   removed the leftovers. What stands instead is the Coder's log work/coder/before-src-change.log (new
   test file on the old code): `✖` on the four tests (`ℹ fail 4`), `✔` on "a failure with a text but
   no Error keeps that text", matching the PR body "4 failed, 3 passed". Not proved by me; does not
   alone change the verdict.
3. The five SwRS no longer carry the CR-347 known issue and match the code. Command:
   `git diff main...HEAD -- requirements/tiers/swrs` read in full. CORE-010: known issue removed, new
   table row for text between inline tags (the new test asserts it converts). CORE-025: known issue
   removed, verification note names the new tests, `previewManager.ts` added to implemented_in_files.
   DIAG-005: table split into "Checked in the drawn picture" (node fill, background) and "as the value
   given to Mermaid" (the rest); first known issue removed, the other three stay (lines 85-87).
   DIAG-009: Mermaid passes serialised, replaced-key rule stated for PlantUML and charts, replaced-key
   known issue removed, the other three stay; method note matches the renamed test. TRUST-042: known
   issue removed, SVG xlink:href rows say it is treated like an HTML link, matches the test's
   assertions (data-sphinx-preview-navigation on both, one blocked-navigation). PASS.
4. No StRS changed: `git diff main...HEAD --name-only | grep -ci strs` printed `0`. PASS.
5. `just requirements-lint` exit 0 (`main paths: 92 StRS checked, 578 SwRS citations, all valid`;
   `use case diagrams: 93 StRS checked, all parse`). PASS.
6. `just requirements-update` leaves the tree clean: see the last section.
7. PR description (`gh pr view 439`, head oid b2bdd72): renders (sections, table, one code fence);
   Summary, Deliverables and Changes match the diff (src: renderPipeline, rendering, previewManager,
   comment-only changes in mermaidPreview and html-sanitizer; five SwRS; log.md; CHANGELOG; tests);
   the "4 failed, 3 passed" count matches item 2; no image attached; Known gaps lists the GFM-003
   note and no unproved claim. Impacts says why there is no screenshot. PASS.

## requirements-update

See the end of this file.

Command `just requirements-update` at the head: output `0 indexes updated`, `0 requirement OKF
projections updated`, exit 0 (two W2 broken-link warnings on SwRS PALETTE-264, a file this CR does not
touch). Then `git status --short | wc -l` printed `0`: nothing generated or hand-edited differs. PASS.

VERIFIED
