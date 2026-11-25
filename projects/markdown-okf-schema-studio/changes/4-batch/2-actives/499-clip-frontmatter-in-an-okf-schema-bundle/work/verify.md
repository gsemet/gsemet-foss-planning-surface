# Verify CR-499 (clip okf-schema-bundle-frontmatter)

Head: 635f1ba09e6511333ac80ebe30e97678ec1fce24

All claims judged at 635f1ba09e6511333ac80ebe30e97678ec1fce24 (origin/main 4a47151e is the merge base; clean tree).

1. Scope: `git diff --stat origin/main...HEAD` lists 23 files: clip folder, `docs/user/okf.md`, two kit test files, `test/site/siteClips.test.ts`; no `src/` change. PASS.
2. Kit tests: `just clip-kit-test` -> `tests 37 pass 37 fail 0`, including the two new bundle-frontmatter cases and the extended checks test. PASS.
3. Site test: `node scripts/node-test.mjs unit "out/test/site/siteClips.test.js"` (after `tsc -p .`) -> `pass 15 fail 0`, incl. "the shipped OKF page plays the schema bundle frontmatter clip as video". PASS.
4. check.json: `passed: true`, 1280x720, 15 fps, 12 s, seam SSIM 0.995998, verifyPassed true, playbackRate 1.007, win32, extensionSource vsix, editMode on, paste false. PASS.
5. Stage: `stage/_schema/note.schema.yaml` and `stage/notes/release-note.md` match the spec (type: note, status: publshed, enum draft/published/retired), LF only (`grep -c $'\r'` -> 0 both). PASS.
6. Frames (opened as images): invalid.png shows the schema table with Description column, type icons, `publshed` and the small badge "x 1"; select-open.png shows the select on "Choose a value..."; picked.png `published`; contact sheet shows Text 1 then Text 2, the save badge, mark 1 on the status row, mark 2 on the Status line; MP4 frames 0/4/10/16 (ffmpeg) show `publshed` and badge at the start. No username or home path visible (window title "workspace"). "Red row" wording gone from clip.md and okf.md (Q11 ruling honoured). PASS.
7. LFS: `git lfs ls-files` lists all 14 clip media files. PASS.
8. PR description vs diff: Summary, Deliverables and Changes match the diff; Known gaps covers the unchecked motion/loop and the uncoloured row; posted body equals work/pr-body.md except one blank line. PASS.
9. PR description, inline GIF resolves: FAIL.
   Command: `curl -sIL "https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/635f1ba0.../okf-schema-bundle-frontmatter.gif"`
   Output: `HTTP/1.1 200 OK`, `Content-Length: 132`, `Content-Type: text/plain`; `curl -s` of it prints `version https://git-lfs.github.com/spec/v1 / oid sha256:31b386fe... / size 1415941`: an LFS pointer, not an image, so the GIF does not render inline.
   The form the spec asks for (`https://github.com/gsemet/markdown-okf-schema-studio/raw/<sha>/...gif`) answers `302` to `media.githubusercontent.com/media/...` and then serves `image/gif`, 1415941 bytes. The body must use that form.
10. Minor, not blocking: clip.md section 1 shows the kit images 01-selected/02-pasted/03-zoomed first with alt texts that do not say what they show ("Frame 0 of the take in the sibling's frames"; 01-selected.png is the frame just before the save, not frame 0); section 2 mark rows dropped the backticks around `status` without a note in Autonomous decisions.

Review box / CI: PR checks at the head are SUCCESS (static, static-windows, visual, viewer-graph, report, checks); review box is unchecked and not claimed.


## Description re-pass (head unchanged, 635f1ba09e6511333ac80ebe30e97678ec1fce24)

- Claim 9 re-judged: the posted body now uses `https://github.com/gsemet/markdown-okf-schema-studio/raw/635f1ba0.../okf-schema-bundle-frontmatter.gif`; `curl -sIL` -> `302`, then `HTTP/1.1 200 OK`, `Content-Type: image/gif`, `Content-Length: 1415941`. PASS.
- Claim 10 re-judged: the two cosmetic points are now bullets in Known gaps (line 32 of the posted body). PASS.
- Rest of the body unchanged in substance; Summary, Deliverables and Changes still match the diff (carried from the first pass, same head).

VERIFIED
