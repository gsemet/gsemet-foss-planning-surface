# Verify CR-484

Head: f42acf7c5f50b7fe580614f13f22f9233c89c82c

All claims judged at f42acf7 (full SHA above) unless marked carried. No long gate pass exists at this head
(the Driver shipped after a local `just preflight`, recorded `--no-gate`); no claim here needs the long suite,
so none was run. Not run by the Verifier: `just check`, `just preflight` (CI `static` and `static-windows`
are green at this head; Round 2 notes report a local pass; not re-run here).

## Claims

1. Parser tests pass at the head, and the test reads the shipped clip.md. VERIFIED (f42acf7)
   `just clip-kit-test` -> `ℹ tests 13  ℹ pass 13  ℹ fail 0` (shipped-file, fenced-block, EXPECTED = Expected
   paste, win32/darwin combined badges, other-platform badge refused, marks, captions, size, fps, cards, no-Size
   default 1920x1080@30). The tests are new and fail on the base: `git show origin/main:.../storyboard.mjs | grep -c
   "parseClipText\|validateStory"` -> 0.
2. `clip-kit-test` runs in `check`, with no direct fnm. VERIFIED (f42acf7)
   `git diff origin/main...HEAD -- justfile package.json`: `check:` lists `clip-kit-test`; the recipe is
   `{{ npm }} run test:clip-kit`; `package.json` gains the script `test:clip-kit`. Deviation from the spec
   (it said no package.json change and `fnm exec`): required by the red CI at ad3c61c, no dependency added.
3. No `src/` change, no SwRS change. VERIFIED: `git diff origin/main...HEAD --name-only | grep -c "^src/"` -> 0.
4. Storyboard clip.md is the approved one with the fields the kit reads. VERIFIED (f42acf7): read
   `docs/demo-video/clips/raw-copy-balance-edges/clip.md`: `status: approved`, Size `1280x720 16:9`, Frame rate
   `15 fps`, Outputs row, `Zoom | result, hold to 8.8 s`, Text 1 and Text 2 as Q36/Q41, badges `Ctrl+C / ⌘C`,
   `Ctrl+V / ⌘V`, Marks 1-3 (5.0-6.2, 6.2-7.4, 7.4-8.6), five-frame pictures link to `frames/`, Expected paste
   block, review notes (setting off, 4.2 fps screencast); no `images/` folder. The test (claim 1) proves the parse.
5. Render passes at the storyboard's size and fps. VERIFIED (f42acf7, media unchanged since ad3c61c: `git
   diff --stat ad3c61c f42acf7` touches only justfile and package.json)
   `ffprobe` mp4: `h264,1280,720,15/1,9.800000`; webm: `vp9,1280,720,15/1`; gif: `960,540,12/1`.
   `check.json`: `passed: true`, 20 checks all ok, `verifyPassed: true`, `pasteWidgets: 0`, `readingMode: off`,
   `loopSeamSsim 0.991153`, `playbackRate 1.006`, platform `win32`, `extensionSource: vsix`, VS Code 1.147.0.
6. Frames, contact sheet show the claimed content. VERIFIED (f42acf7) for stills, opened as images:
   `01-selected` (selection from "migrations" through table and warning to "every worker", Text 1,
   `Comment` button kept as filmed), `02-pasted` (16 lines, table and `---` in paste, Ctrl+V / ⌘V badge, Text 2 in
   cross-fade), `04-mark-1` (outline on `:::{important}`), `05-mark-2` (outline on the opening `**`),
   `06-mark-3` (outline on the closing `:::`), contact sheet (Text 1 then Text 2, badges as two key groups
   split by "/"). No personal name or path, no tooltip, no dirty tab seen. Note: `02-pasted` (named in
   section 1 with Text 1) shows Text 2 mid fade, because it is taken at 4.4 s, the boundary; cosmetic.
7. Recipe updated per spec 6 (storyboard-first section, contract of the storyboard, combined badges, no
   "`-` for none", size and fps, key frames, PR clip rule with the `-assets` fallback, no process role or CR).
   VERIFIED (f42acf7): read `feature-clip-process.guidelines.md`; `grep -in "chantier\|CR-\|Foreman\|driver"` -> none.
8. Glossary, AGENTS.md and settings.md alt text updated as spec. VERIFIED: `git diff origin/main...HEAD` of the
   three files shows exactly the specified wording.
9. PR description as posted. VERIFIED (f42acf7). `gh pr view 502 --json body` equals `pr-body.md` (only a
   trailing newline differs); head `f42acf7c...`, draft. The GIF, MP4 and WebM URLs at the head sha return 200
   (`curl -sIL`), and a ranged GET of the GIF returns `GIF89a` (the `github.com/raw` form resolves LFS).
   Sections match the template; Summary, Deliverables and Changes match the diff (kit, tests, justfile, clip, recipe,
   glossary, AGENTS.md, alt text), nothing delivered is unmentioned. The Mermaid block renders as source here
   only by syntax (not rendered by me). No image attached shows a username or home folder (the attached images
   are the GIF whose frames were opened above). No role name in the body. Review box: `chantier log` has
   `r2 approved at ad3c61c9..., committed as f42acf7c`, which proves the box "committed as f42acf7c".
   Known gaps: the body ends with "Not checked: motion, rhythm and the loop as watched (stills only); macOS Cmd+C
   is not proved in a real window". The text-only no-new-take path (Evidence 4) is not mentioned, see claim 11.
10. CI at the head. VERIFIED: `gh pr view 502` -> static, static-windows, visual, viewer-graph, checks, report
    SUCCESS; integration, stress, gallery, release jobs SKIPPED (as designed for a PR).
11. Text-only change proves the "no new take" path (spec Evidence 4). UNVERIFIED by the Verifier: only the
    Coder's log `work/clip-textonly.log` (a render then `check`, all ok, seam 0.98984) exists; re-rendering here
    would rewrite the committed LFS media, and the log is not a command run by me. Not a failure.
12. Motion, rhythm, the loop as watched, and macOS Cmd+C in a real window: UNVERIFIED (as agreed).

## Verdict

VERIFIED at f42acf7c5f50b7fe580614f13f22f9233c89c82c. Nothing I ran fails. Remark for the Driver, not a
failure: add the text-only path (claim 11) to the PR's Not checked line; the package.json script and the
unchanged-media statement were the Round 2 change.
