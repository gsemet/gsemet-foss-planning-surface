# Verify CR-499 (clip okf-schema-bundle-frontmatter)

Head: b7518fb3c16b8ac5da27f87c1165837530e5127f

Move judged: 635f1ba09e6511333ac80ebe30e97678ec1fce24 -> b7518fb3c16b8ac5da27f87c1165837530e5127f
(restack onto CR-498 head 37ef61b338b3ca56d1cb428983c78ebdb54684f0). Claims are judged at b7518fb
unless marked "carried from 635f1ba". Commands run in the CR's worktree; tree clean before and after.

## The move and the scope (b7518fb)

1. Head, base and push. `git ls-remote origin refs/heads/chantier/batch-09/cr-499-...` ->
   `b7518fb3c16b8ac5da27f87c1165837530e5127f`; `git merge-base --is-ancestor 37ef61b3 HEAD` ->
   `base is ancestor`; `gh pr view 521` -> head b7518fb, base `chantier/batch-09/cr-498-...`,
   `isDraft: true`. PASS.
2. Clip folder unchanged. `git diff --stat 635f1ba HEAD -- docs/demo-video/clips/okf-schema-bundle-frontmatter`
   -> empty. PASS (no new take).
3. Patch of the move. `git range-diff 4a47151e..635f1ba0 37ef61b3..b7518fb3`: differences are in the
   context and merge of `check.test.mjs` (title lists the stack's siblings plus "bundle frontmatter"),
   `storyboard.test.mjs`, `docs/user/okf.md` (standard GIF first, then the bundle GIF) and
   `siteClips.test.ts`. PASS.
4. Scope. `git diff --stat 37ef61b3..HEAD` -> 23 files, 745 insertions, 1 deletion: the clip folder
   (19), `docs/user/okf.md`, two clip kit test files, `test/site/siteClips.test.ts`.
   `git diff --stat 37ef61b3..HEAD -- src` -> empty. PASS.

## Gates (b7518fb)

5. `just check` -> `exit=0`. Log `work/verifier/just-check-b7518fb.log`: clip kit `tests 53 pass 53
   fail 0`; unit `tests 5305 pass 5297 fail 0 skipped 8`; security `tests 107 pass 107`; `205 passed`;
   `1227 requirements, 0 errors, 26 warnings`; `0 files would change`. PASS.
6. `just clip-kit-test` -> `tests 53 pass 53 fail 0`, with "the shipped okf-schema-bundle-frontmatter
   clip.md reads as the clip the owner reviews", "the stage of the ... clip differs from the expected
   page by the status line only" and the checks test naming "bundle frontmatter". PASS.
7. `node scripts/node-test.mjs unit "out/test/site/siteClips.test.js"` -> `tests 22 pass 22 fail 0`,
   with "the shipped OKF page plays the schema bundle frontmatter clip as video". PASS.
8. Rest of the Windows static stage: `just check-no-merge-commits` -> `passed (17 commits since
   origin/main, no merge commit)`; `just audit` -> `found 0 vulnerabilities`; `just sphinx-check` ->
   `4 passed`; `just requirements-report` -> `"errors": 0`; each exit 0 (logs
   `work/verifier/just-*-b7518fb.log`). PASS. No long gate is configured.

## The take and the clip

9. `check.json` (carried from 635f1ba: file unchanged, read again): `passed: true`, length 12,
   MP4/WebM 1280x720 15 fps, GIF 960 px 12 fps, `loopSeamSsim 0.995998`, `rawFps 2.1`,
   `playbackRate 1.007`, `verifyPassed true`, `platform win32`, `extensionSource vsix`, check line
   "scenario verify passed" ok. PASS.
10. `ffprobe` at b7518fb: MP4 h264 1280x720 15/1 12.000 s; WebM vp9 1280x720 15/1 12.000 s; GIF
    960x540 12/1 12.000 s; one video stream each, no audio. `git lfs ls-files` lists 14 files of the
    clip. PASS.
11. Take history. `work/gates/clip-all-1.log`: `FAILED: the table headers are ["Name","Value◀▶",...]`;
    `clip-all-2.log`: `FAILED: the save did not clear the error: {... "statusValue":"\"published\""
    ... "errorRows":[] ...}`; `clip-all-3.log`: all checks ok. The two scenario fixes are at
    `scenario.mjs` lines 98 (header text stripped) and 227 (`JSON.stringify("published")`). PASS.
12. What the scenario proves (`scenario.mjs`): select options after the click (lines 187-196), two
    ArrowDown `draft` then `published` (203-211), save clears rows, badge, body `published`
    (220-229), file equals EXPECTED and schema unchanged (258-268). No Escape press in the file.
    PASS.
13. Own scratch and port: `grep clip-all-3.log` -> `Using value 'C:\okfclip499\...'`;
    `C:/okfclip499/okf-schema-bundle-frontmatter/user/DevToolsActivePort` holds `9499`;
    `git diff --name-only 37ef61b3..HEAD -- docs/demo-video/clip-kit` -> the two test files only. PASS.
14. Pictures (media unchanged since 635f1ba; opened again): contact sheet, `invalid.png`,
    `select-open.png`, `picked.png`, `01-selected.png`, `02-pasted.png`, `03-zoomed.png`,
    `04-mark-1.png`, `05-mark-2.png`, and 8 frames of the GIF. Frame 0: schema table with Name,
    Value, Description and type icons, `publshed`, badge "x 1", status row not coloured; select on
    "Choose a value..." then `draft`, `published`; save badge; badge gone and body "Status:
    published"; Text 1 then Text 2; mark 1 on the status row, mark 2 on the Status line; no native
    popup; window title "release-note.md - workspace"; no username or home path. PASS.
15. Stage (carried from 635f1ba, files unchanged): schema enum draft/published/retired; `grep -c $'\r'`
    -> 0 on both files; `diff okf-frontmatter/stage/release-note.md .../notes/release-note.md` ->
    only `type: note` added and `status: draft` -> `publshed`. PASS.

## PR description (judged again, body at b7518fb, last edit 2026-11-26T01:55:08Z)

16. Renders: `gh api graphql ... bodyHTML` -> headings, lists, task boxes and the GIF `<img>` render.
    The project template's sections are in its order, then the extra sections; Internal references
    last; no internal id or agent role outside it. PASS.
17. Links: `curl -sIL` GIF, MP4, WebM raw URLs at b7518fb -> 302 then 200 (`image/gif` 1415941;
    393654; 256798 bytes); `clip.md` blob -> 200. sha256 of each download equals the LFS oid at
    HEAD. PASS.
18. Summary: 12 s silent (claim 10); the typed table, badge, select, save (14); sibling "same page,
    status field, click, save chord and marks" (`okf-frontmatter/clip.md` badge and mark rows, claim
    15); stage differences (15, and the sibling's stage sits at `stage/release-note.md`, no
    `notes/`). On the base `docs/user/okf.md` holds one image, the standard frontmatter GIF
    (`git show 37ef61b3:docs/user/okf.md`). PASS.
19. Deliverables, Changes, Impacts, Blast radius match claims 4 and 10. PASS.
20. Test plan: tests (6, 7); requirements: `0 files would change` (5) and the added
    `@tests_req SwRS-MDOKFSTUDIO-CORE-095` marker in the siteClips diff; changelog:
    `git log 37ef61b3..HEAD` -> one commit, `docs:`; local gates 53 tests and `just check` (5, 6);
    evidence (9, 11), carried from 635f1ba as the body says. PASS.
21. Review box: `chantier log CR-499` -> `2026-11-26T01:34:04Z driver note ... move 635f1ba..b7518fb
    (restack) inspector approved at b7518fb3c16b...`. PASS.
22. CI: `gh run view 45728474453` -> headSha b7518fb, `success`; `gh pr checks 521` -> static,
    static-windows, visual, viewer-graph, report, checks pass. The known stack failure of
    check-no-merge-commits on a new run is not this change's; nothing re-run or pushed. PASS.
23. "What the clip proves" (9, 12). Owner approval of storyboard and clip: `02-answers.md`, "Owner
    approval (2026-11-25, evening ...)", given after the take of 11:35Z; media unchanged since (2).
    The body claims no motion or rhythm proof. PASS.
24. Deviation and Autonomous decisions: review moved after the take (bundle-fm-Q3); `okf-error` is
    styled only at `propertiesStyles.ts:183` `.okf-info-row.okf-error th` (`grep -rn okf-error src`);
    `grep -niw red scenario.mjs docs/user/okf.md` -> empty, `clip.md` keeps "red" only in the note
    that records the change; the missing style is filed
    (`changes/1-inbox/field-row-with-a-validation-error-has-no/intake/request.md`). PASS.
25. Known gaps: row colour (24); `01-selected.png` captioned frame 0 shows `published` picked before
    the save (14; `03-zoomed.png` in section 1 shows mark 2); opening paragraph of `clip.md` omits
    the typo its Stage row names; raw 2.1 fps (9); Windows only (9). The earlier gap "Mark rows write
    status without code quotes" is rightly gone: both Mark rows of the unchanged `clip.md` have the
    backticks (the second half of the 635f1ba claim 10 was wrong). Motion/rhythm is closed by the
    owner's approval (23). PASS.

## Observations (do not decide the verdict)

- Not in the spec's evidence list and no statement of the body is false: spec section 7 also asked
  the body to name the twin clip's PR (open: #517, below in this stack) and to list under Autonomous
  decisions the parked pointer, key frame names, measured times and editor association pattern. The
  body names the twin by what it is, not by number, and omits those four; the pointer and times are
  in `clip.md`'s review notes.
- The spec asked for two commits (`docs:`, `test:`); the branch has one `docs:` commit (as at
  635f1ba).
- `just preflight` itself was not run (it cleans `out/`); its Windows stage's recipes are claims 5
  and 8.

VERIFIED
