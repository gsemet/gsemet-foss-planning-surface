# CR-427 before and after

Before: base `82c11a472250b6b808476ec797c2106481ddbd15` (origin/main). After: pushed head
`ebfb7f28603a2688c246349bfc4706b281210993`. Windows 11, local. No visual change, so no images:
the pairs are command outputs.

Runner: `node <work>/investigator/timed-run.mjs <limit s> <node args>` from the worktree; it ends a
run still alive at the limit by its own PID (`taskkill /PID <pid> /T /F`), never by name.

## Pair 1: pinned font folder missing (FONTS temporarily set to `C:/does-not-exist/fonts`)

Command (after `just compile`):
`node <work>/investigator/timed-run.mjs 120 --import ./scripts/register-myst-patches.mjs --test out/test/page/tableBreakout.test.js`

- Before (82c11a47): carried from the Coder's round-1 run at the base
  (`work/evidence-r1/2a-base-82c11a47-missing-folder.log`): `[timed-run] HUNG: ended by timed-run after 120.7 s`.
  Not taken again by the Verifier: `git worktree add --detach <work>/scratch/base 82c11a47` failed with
  `error: unable to create file .agents/skills/markdown-studio-exploratory-qa-claude/scenarios/ux-38-invalid-field-does-not-block-others.json: Filename too long`
  and `fatal: Could not reset index file to revision 'HEAD'.`; the card makes that a stop with no workaround.
  The worktree's base tree is the one the Coder ran on (head = base, nothing changed yet; driver log
  `round=1 wt_head=82c11a47`).
- After (ebfb7f2, Verifier): `work/verifier/logs/2b-after-missing.log`: 7 breakout tests fail on
  `ENOENT ... C:\does-not-exist\fonts\KaTeX_SansSerif-Regular.woff2`, the new regression test passes,
  `[timed-run] exited by itself after 3.2 s, code 1`.

## Pair 2: pinned font files that are not fonts (FONTS temporarily set to a folder of three `not a font` files)

Same command.

- Before (82c11a47): carried from `work/evidence-r1/2a-base-82c11a47-bad-bytes.log`:
  `[timed-run] HUNG: ended by timed-run after 120.1 s` (same reason as pair 1).
- After (ebfb7f2, Verifier): `work/verifier/logs/2b-after-badbytes.log`: 7 breakout tests fail on
  `the pinned test font did not load: KaTeX_SansSerif-Regular.woff2 (error), KaTeX_SansSerif-Bold.woff2 (error), KaTeX_Typewriter-Regular.woff2 (error) from <folder>`,
  the new regression test passes, `[timed-run] exited by itself after 3.5 s, code 1`.

Every temporary edit of `test/page/pinnedFont.ts` was reverted (`git checkout -- test/page/pinnedFont.ts`;
`git status --short` empty afterwards).
