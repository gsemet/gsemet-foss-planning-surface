# Before / after (CR-384)

Before = base 9c3fb6d (detached worktree, since removed). After = head 7a87cfc25b6ac41a99ed50b7872bf7651c77816e.
Paths below are made up (`<scratch>/p` is a scratch project, its own git repo). No UI change: no screenshot.

## 1. watch with no batch
Reproduce: `cd <scratch>/p` (after `git init`, `chantier init`) then `chantier watch --after 0`.
- Before (9c3fb6d): `error: watch: no running batch in p: nothing to watch`
- After (7a87cfc):
  ```
  watch: p from cursor 1, the hub
  board wrote (move): board-idea -> P2; for the Chief of Staff: tell the user, act on nothing
  board wrote (label): label 'x' on board-idea; for the Chief of Staff: tell the user, act on nothing
  watch: p (no batch) still running: for the Chief of Staff, start again in the background now: chantier watch --after 3
  ```
  (run with CHANTIER_HUB_TEST_TIMES=1:4, CLAUDE_CODE_SESSION_ID=sessA)

## 2. Board writes in forge-journal.jsonl (in-process board routes on the scratch project, work/verifier/probe.py)
After: new idea (200), move (200), move of an unknown item (409), label (200) give three lines, none for the refusal:
```
{"seq":1,...,"by":"board","kind":"board","action":"new","items":["board-idea"],"text":"new idea in 1-inbox/board-idea","wakes":true}
{"seq":2,...,"action":"move","items":["board-idea"],"text":"board-idea -> P2","wakes":true}
{"seq":3,...,"action":"label","items":["board-idea"],"text":"label 'x' on board-idea","wakes":false}
```
Before: no `board` kind in the forge journal (the board wrote board-journal.jsonl only; spec "What changes" 1).

## 3. Pull path
`chantier watch --once --after 0` (after): the three `board wrote (...)` lines then
`watch: cursor 3; next, at the user's next message: chantier watch --once --after 3`.
Before: `--once` did not exist.

## 4. seat take
`CLAUDE_CODE_SESSION_ID=sessB chantier seat take sessB` prints the `watch: not running: ... start in the background: ... watch --after 3; after the user's no, at each user message: ... watch --once --after 3` line.

## Not captured
- A Configuration save (PUT /config) needs a planning surface; not run by hand, proved by tests/test_board_config.py (4 save cases, dry run none) in verify.md.
- Seat taken by another session ending a live watcher needs two concurrent processes (no background shell for the Verifier): proved by tests/test_watch_events.py seat cases.
- Real main session wake, orphaned watcher end, Copilot wake: not provable (Known gaps).
