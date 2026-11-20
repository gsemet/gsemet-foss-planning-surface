# Verify CR-435

Head: cd2f90c22c228ef7f6d256b586b7f4710135eb29

All claims judged at cd2f90c22c228ef7f6d256b586b7f4710135eb29.

1. Fixtures stored byte-exact with attributes. Command: `git ls-files --eol test/fixtures/markdown-line-endings; git check-attr -a <crlf, mixed fixtures>`.
   Output: document.crlf.md i/crlf w/crlf attr/-text; document.lf.md i/lf attr/text=auto eol=lf; document.mixed.md i/mixed attr/-text; no-final-newline.crlf.md i/crlf attr/-text; check-attr: `text: unset`.
2. Every other tracked Markdown stays LF. Command: `git ls-files --eol '*.md' | grep -v 'i/lf'`. Output: only the empty `empty.md` (i/none) and the three fixtures above.
3. New tests pass. Commands: `npx tsc -p .`, then `node --test out/test/build/lineEndingFixtures.test.js out/test/core/edits/lineEndingPreservation.test.js out/test/session/lineEndingSave.test.js out/test/session/blockReq.requirements.test.js`. Output: tests 32, pass 32, fail 0 (the 4 guard tests, the byte-preservation tests, and the moved blockReq tests).
4. Red proof on planted fault: work/evidence-red.log shows 4 fail with LF-planted CRLF fixtures (crlf guard, no bare LF, saved block, last block). Not re-run by me; the log's claim matches the green-to-red shape and the PR body states the two guards not shown red.
5. Long gate: gate log first line `CR-435 branch chantier/batch-07/cr-435-... head cd2f90c22c228ef7f6d256b586b7f4710135eb29`, `just preflight`; `$CHANTIER log` shows `gate result=pass head=cd2f90c2...`. CI at head: static, static-windows, visual pass (log note).
6. PR body (`gh pr view 445 --json title,body,headRefOid`): headRefOid is the head; the body matches work/pr-body.md and the diff (13 files: .gitattributes, 4 fixtures, 3 new tests + guard, shared loader, blockFixture move, SwRS-BLOCK-234, log). Renders as clean sections, no images, no username/home path. Known gaps lists ux-35 not re-run and the stuck-save tests deferred (these narrow the request; declared, not hidden). Review/CI boxes are unchecked, as expected for a draft. Role names: none outside Internal references.

Scope note: the request's ux-35 rerun and the "save ends, no stuck Saving" tests are not delivered; both are declared in Known gaps and Autonomous decisions.

Code claims 1-5 above: VERIFIED at cd2f90c22c228ef7f6d256b586b7f4710135eb29.

## Description-only pass (posted body of PR 445 at cd2f90c22c228ef7f6d256b586b7f4710135eb29)

Command: `gh pr view 445 --json title,body,headRefOid` (headRefOid = cd2f90c22c228ef7f6d256b586b7f4710135eb29), checked against `git diff --stat main...HEAD` (13 files) and the pr-template audit list.

- Consistency with the diff: Summary, Deliverables and Changes match the 13 changed files. OK.
- Images: none. OK.
- FAIL, fold: the posted body has Changes and Impacts outside the `<details>` fold (right after Deliverables). The template's fold holds Changes, Impacts, Test plan and Internal references, after Autonomous decisions.
- FAIL, internal references outside the last section: the Test plan names "approved r1" (a round number) and the planning path `work/evidence-red.log`; the guideline forbids round numbers and planning-folder paths outside Internal references.
- Minor: the mixed-fixture guard and the "other Markdown stored with CR" test not shown red appear only in the Test plan, not in Known gaps.
- Review box SHA cd2f90c matches the Driver's note "r1 approved at dd89211d..., committed as cd2f90c2". OK.

NOT VERIFIED
