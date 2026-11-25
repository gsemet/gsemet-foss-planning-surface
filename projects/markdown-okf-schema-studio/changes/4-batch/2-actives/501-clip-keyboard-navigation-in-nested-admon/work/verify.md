# Verify CR-501

Head: 3ea161ce58f3b53cfc4121a4cd0581f3082561e6

Basis: CoS ruling Q12 (clip ends at the admonition editor). Previous pass: VERIFIED at 66b84782 (claims 1-8 there, carried below).

Delta 66b84782..3ea161ce: `git diff --stat 66b84782 HEAD` -> one file, docs/demo-video/clips/keyboard-navigation/clip.md (+7 -4): the "Changing one word" note now says Enter opens the whole admonition editor (Lines 3-11), caret reached by Up x5 + Right, "Friday" replaced. Matches Q12 and the filmed take. No src/ change (`git diff --stat origin/main HEAD -- src` empty).

Claims at 3ea161ce:
1. `just clip-kit-test` -> tests 40, pass 40, fail 0 (incl. "the shipped keyboard-navigation clip.md reads as the clip the owner reviews").
2. `just check` -> exit 0 (ends "use case diagrams: 94 StRS checked, all parse").
3. Take, frames, GIF/MP4/WebM, site test, scenario: carried from 66b8478: the move touched only clip.md prose, not the take or its media.
4. PR description (gh pr view 522, head 3ea161ce, draft): FAILS. Known gaps still says "The storyboard's 'Changing one word' review note still says the editor opens on the item's text", which 3ea161ce fixed. Media links name 66b84782 (files unchanged, still resolve; clip.md link shows the old note). Test plan "all at 66b8478" is accurate for the take but gates were re-run only partly at the new head.

NOT VERIFIED (description only: delete the stale Known gaps bullet, point the clip.md link at 3ea161ce, and say local gates ran at 3ea161ce for check)

## Description pass 2 at 3ea161ce58f3b53cfc4121a4cd0581f3082561e6

Head: 3ea161ce58f3b53cfc4121a4cd0581f3082561e6

Command: `gh pr view 522 --json body,headRefOid` -> headRefOid 3ea161ce.... Checks:
- Known gaps: stale clip.md bullet gone; three bullets remain, all accurate (author unchecked motion; Windows only; Enter-opens-whole-admonition shown, not fixed).
- clip.md link points at 3ea161ce. Media links name 66b84782: `git diff --stat 66b84782 3ea161ce -- <gif mp4 webm>` -> empty (files unchanged, still resolve).
- Gates: take and ci-static stated at 66b8478 with the carry reason (`git diff --stat 66b84782 3ea161ce` -> clip.md only); check and clip-kit-test at 3ea161c, proven in claims 1-2 above. GIF 1.60 MB = check.json gif.bytes 1675368.
- Changes/Deliverables match the diff (clip folder, docs/user/editing.md clip under the list section, kit and site tests; `git diff origin/main 3ea161ce --stat -- src` empty).
- Deviation text matches the storyboard note and Q12. No image attached shows a username (the GIF is a repo file, captured earlier and passed the look at 66b84782).

VERIFIED
