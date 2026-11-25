# Verify CR-498

Head: cb1ccf693f2ad61203981586bd4e4f198ca3c6b0

Worktree clean at the head (`git status --short` empty). PR 519 draft, base `chantier/batch-09/cr-495-feature-clip-edit-a-figure-in-one-form`, head on the forge = cb1ccf693f2ad61203981586bd4e4f198ca3c6b0.

## Claims (all judged at cb1ccf6)

1. Kit tests pass: `just clip-kit-test` -> `tests 39, pass 39, fail 0` (includes "the shipped wide-table-auto-width clip.md reads as the clip the owner reviews" and "the stage of the wide-table-auto-width scenario is the shipped stage file, byte for byte").
2. The clip's committed media pass the kit's check: `CLIP_PORT=9498 CLIP_SCRATCH=C:/okfclip498 just clip wide-table-auto-width check` -> every line `ok`: mp4 10.600 s = Length, 1280x720, 15 fps, h264 yuv420p, no audio, 0.56 MB; webm vp9 0.35 MB; gif 960 px 12 fps 1.99 MB loop 0; seam SSIM 0.99137; scenario verify passed: true; reading mode off at start; playback rate 1.011.
3. The site page plays the clip: `node --import ./scripts/register-myst-patches.mjs --test out/test/site/siteClips.test.js` (after `just compile`) -> `tests 16, pass 16, fail 0`, incl. "the shipped wide tables page plays the wide table clip as video". (Run without the import, all shipped-page tests fail on a module path: my invocation, not the CR.)
4. Frames are the CR's own and show what is claimed, no user name or home folder: opened `contact-sheet.png`, `frames/margin.png`, `frames/04-mark-1.png`. Margin: table cut after April with shaded edge and scrollbar, tooltip "Width: Margin", Text 1, title bar `deploys.md - workspace`. Auto: Jan to Dec and Total whole, centred, wider than the paragraph, paragraph unmoved, orange marks (table, then paragraph), Text 2. No `gaeta` and no `C:\Users` anywhere. Workspace is `C:\okfclip498` (own scratch).
5. Scope: `git diff --stat origin/chantier/batch-09/cr-495-...HEAD` = 19 files, only the clip folder, the two kit test files, `test/site/siteClips.test.ts`, `docs/user/wide-tables.md` (no `src/`, no skill). Matches the body's Changes.
6. PR description as posted equals `work/pr-body.md` (diff: one trailing blank line). Sections render; MP4, WebM and GIF raw URLs at cb1ccf6 return HTTP 200 (`curl -sIL`: gif image/gif, mp4, webm). Body Summary, Deliverables, Changes match the diff; Known gaps lists the unchecked motion/rhythm and the logo/toolbar overlap; deviation from the recipe order is reported; Internal references hold only the CR line. No image shows a user path (claim 4).
7. Review box: `chantier log 498` -> "r1 approved at d930238c, committed as cb1ccf69" and "r1 inspector approved at d930238c": supports `Review: approved at cb1ccf6`.
8. Gates: `ship` records no long gate pass at cb1ccf6 (off list); the project gate `just check` and `just preflight` (static) were run by the Coder on the identical tree (Driver note). CI at cb1ccf6: static pass, static-windows pass, viewer-graph pass, visual pending at the time of this check (`gh pr checks 519`). Not my claim to wait on; the body's "CI green" box is rightly unticked.

Not checked by the Verifier: motion, rhythm, the loop as watched (owner's review, disclosed in Known gaps). No before/after pair: a new clip has no before; the Margin and Auto frames are the pair.

VERIFIED
