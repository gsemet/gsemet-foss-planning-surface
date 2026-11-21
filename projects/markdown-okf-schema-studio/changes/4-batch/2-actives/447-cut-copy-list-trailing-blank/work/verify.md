# Verify CR-447

Head: 15a0ef09e3763f7ed52ce60130da8ccfaba1ed5b

Verdict: NOT VERIFIED (one claim fails: the posted PR description cites a stale SHA; everything else holds).

## Claims, all judged at 15a0ef09

1. Copy and cut trim for LF, CRLF, lone CR; refused cases unchanged (nbsp line, blank-only, blank-first,
   past the end). Command: `npm run compile`, then
   `node --test out/test/core/edits/sourceEdits.test.js out/test/core/mapping/blockRange.test.js out/test/core/edits/blocksDelete.test.js out/test/session/dropFiles.requirements.test.js`
   Output: `tests 88, pass 88, fail 0`. sourceEdits file alone: `tests 37, pass 37, fail 0`, with the
   6 new tests listed for each of `LF:`, `CRLF:`, `lone CR:` (list in the middle, list last,
   selection ending on a list, same result as Delete block, still refused, no-break-space refused).
   The no-break-space test document holds a real U+00A0 (`grep -nP "\x{00a0}"` matches line 291).
2. Paste on the blank anchor and refusals (blank with nothing above, right under frontmatter, nbsp
   line): same run, blockRange tests `paste after the blank line that ends a list inserts after the
   list`, `both blank lines of a run ... same pasted text`, `paste still refuses a blank line with no
   body above it and a no-break-space line`: all pass.
3. The new tests fail on the base. Command: detached worktree at 5a84db8b with the two test files
   from 15a0ef09, `npx tsc -p .`, same `node --test` on sourceEdits and blockRange. Output:
   `tests 64, pass 49, fail 15`; failing: the 12 trim tests (4 per EOL), `paste refuses an empty
   clipboard, the frontmatter and stale lines` (the changed assertion), `paste after the blank line
   that ends a list...`, `both blank lines of a run...`. The guard tests (still refused) pass on the
   base, as the spec says. The detached worktree is removed.
4. Requirements: `just requirements-lint` ran (diagram check: 94 StRS parse); `just requirements-update`
   ended `0 indexes updated, 0 requirement OKF projections updated`, `git status --short` empty.
   (One W2 warning, broken cross-link in PALETTE-264, is not touched by this CR.) The diff
   `git diff 5a84db8b HEAD` edits BLOCK-124, 166, 169, 174, the block-editing index and a dated
   entry in `requirements/tiers/log.md`; CHANGELOG has the one line under Unreleased.
5. Code against spec: `git diff 5a84db8b HEAD -- src` shows `withoutTrailingCommonMarkBlankLines`
   (CommonMark test, same guards) used in `planBlocksCopyCut`, and `planPaste` moving a
   CommonMark-blank anchor to `above + 1`, refusing no-body-above, frontmatter and nbsp, with the
   markers BLOCK-166/169 and BLOCK-174/124.
6. Gate: `work/gates/20261121-121839.log`, first line `gate CR-447 branch ... head
   15a0ef09e3763f7ed52ce60130da8ccfaba1ed5b`, last line `result: pass at 15a0ef09...` (static stage;
   visual, integration and gallery run in CI on Windows-skipped).
7. Real VS Code steps (copy, cut, paste in `scenarioBlockSelection`): NOT run locally (Windows).
   CI evidence only: `gh run view 44898480884 --json jobs,headSha`: headSha 15a0ef09..., jobs
   integration, stress, visual, static, static-windows, report, checks = success. The new blocks
   are in `test/integration/realInput/blockKeys.ts` (captures r25 and r26, markers BLOCK-169 and
   BLOCK-174). The PR is a draft, base main, head 15a0ef09 (`gh pr view 458`).

## Description (as posted on PR 458)

- Summary, Deliverables, Changes match the diff (src, requirements, changelog, the two capture
  registries, the dropFiles test change under Autonomous decisions). No image. Known gaps lists the
  heavy-only real scenario.
- FAILS: the posted body says "all passing at 150ee65" in the Test plan; the head is 15a0ef09 and
  150ee65 is neither the head nor carried with a reason. `diff` of `gh pr view 458 --json body`
  against `work/pr-body.md` shows exactly this line (the work copy already says 15a0ef0). Update
  the posted body (`gh pr edit`) to 15a0ef0.
