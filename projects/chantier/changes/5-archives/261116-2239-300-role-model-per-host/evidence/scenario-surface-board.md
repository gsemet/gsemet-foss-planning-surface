# chantier scenario: 1 unit runs, 153.6 s

| unit | forge | checks | commands | seconds | budget | status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| surface-board | github | 162/162 | 259 | 153.6 | 250 | ok |

wall time: 153.6 s
sum of the units' seconds: 153.6 s


# chantier scenario, unit surface-board on github: 162/162 checks passed

- Run: 2026-11-16 23:01:11, 153.2 s
- Workspace: `C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp` (removed)


## 16c. The remote board: the web board's server, behind a key
    $ chantier file Board working  → exit 0
      filed .agents/changes/1-inbox/board-working; write the intent and grill the CR here
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj\.agents\changes\1-inbox\board-working --priority P1  → exit 0
      triaged .agents/changes/2-backlog/P1/board-working (P1)
    $ chantier file Board blocked  → exit 0
      filed .agents/changes/1-inbox/board-blocked; write the intent and grill the CR here
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj\.agents\changes\1-inbox\board-blocked --priority P1  → exit 0
      triaged .agents/changes/2-backlog/P1/board-blocked (P1)
    $ chantier file Board queued <b>bold</b> title  → exit 0
      filed .agents/changes/1-inbox/board-queued-b-bold-b-title; write the intent and grill the CR here
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj\.agents\changes\1-inbox\board-queued-b-bold-b-title --priority P1  → exit 0
      triaged .agents/changes/2-backlog/P1/board-queued-b-bold-b-title (P1)
    $ chantier file Board last  → exit 0
      filed .agents/changes/1-inbox/board-last; write the intent and grill the CR here
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj\.agents\changes\1-inbox\board-last --priority P1  → exit 0
      triaged .agents/changes/2-backlog/P1/board-last (P1)
    $ chantier file Board backlog item  → exit 0
      filed .agents/changes/1-inbox/board-backlog-item; write the intent and grill the CR here
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj\.agents\changes\1-inbox\board-backlog-item --priority P2  → exit 0
      triaged .agents/changes/2-backlog/P2/board-backlog-item (P2)
    $ chantier file Board ready item  → exit 0
      filed .agents/changes/1-inbox/board-ready-item; write the intent and grill the CR here
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj\.agents\changes\1-inbox\board-ready-item --priority P1  → exit 0
      triaged .agents/changes/2-backlog/P1/board-ready-item (P1)
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj\.agents\changes\2-backlog\P1\board-ready-item --ready  → exit 0
      triaged .agents/changes/3-ready/board-ready-item
    $ chantier file Board inbox item  → exit 0
      filed .agents/changes/1-inbox/board-inbox-item; write the intent and grill the CR here
    $ chantier open C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj\.agents\changes\2-backlog\P1\board-working C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj\.agents\changes\2-backlog\P1\board-blocked C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj\.agents\changes\2-backlog\P1\board-queued-b-bold-b-title C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj\.agents\changes\2-backlog\P1\board-last --direct --slots 2 --default-branch main  → exit 0
      opened batch-01 on claude: 4 CRs, 2 slots, parallel, steering direct
      next: complete the brief .agents/changes/4-batch/brief.md, then steer it yourself
      CR-101 Board working: 2-backlog/P1/board-working -> 4-batch/1-pending/101-board-working
      CR-102 Board blocked: 2-backlog/P1/board-blocked -> 4-batch/1-pending/102-board-blocked
      CR-103 Board queued <b>bold</b> title: 2-backlog/P1/board-queued-b-bold-b-title -> 4-batch/1-pending/103-board-queued-b-bold-b-title
      CR-104 Board last: 2-backlog/P1/board-last -> 4-batch/1-pending/104-board-last
    $ chantier seat take s-1 --env remote --title [Remote] 💬 Proj · CoS --link link-s1  → exit 0
      seat s-1
    $ chantier foreman set uuid-chief --epoch 1  → exit 0
      foreman uuid-chief epoch 1
    $ chantier foreman transcript uuid-chief --epoch 1  → exit 0
      transcript uuid-chief
    $ chantier take CR-101 --epoch 1  → exit 0
      took CR-101 (1 of 2 slots held)
      CR-101 "Board working" (change) working in batch batch-01 (parallel)
      cli: uv run --no-sync --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" chantier <command> --batch batch-01
      cards: C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/ (driver.md, concepts.md; each worker's own card, named in its opening lines); the project's rules rank above them: `rules`
      project instructions: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj/AGENTS.md
      specification: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj/.agents/changes/4-batch/2-actives/101-board-working/03-change-spec.md
      folder: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj/.agents/changes/4-batch/2-actives/101-board-working (work/, evidence/)
      worktree: C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj.worktrees\batch-01-CR-101 branch chantier/batch-01/cr-101-board-working base origin/main; not created yet: a Driver creates it first
      PR: none; head -
      rounds: 0 of 3
      notes: none
      gates before handback ready, at the PR's head not shipped yet (the full SHA; the gate log's first line names it):
        [ ] long gate passed (gate CR-101 "<cmd>" ["<cmd>"...]; none in the project's rules: handback CR-101 ready --no-gate "<rule>")
        [ ] verdict VERIFIED (the Verifier: verdict CR-101 VERIFIED|"NOT VERIFIED")
      coder prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier coder for CR-101 "Board working" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/coder.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      conflict-resolver prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier conflict-resolver for CR-101 "Board working" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/conflict-resolver.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      debugger prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier debugger for CR-101 "Board working" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/debugger.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      inspector prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier inspector for CR-101 "Board working" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/inspector.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      investigator prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier investigator for CR-101 "Board working" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/investigator.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      verifier prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier verifier for CR-101 "Board working" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/verifier.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
    $ chantier agents set CR-101 agent-CR-101 --epoch 1  → exit 0
      CR-101 → agent-CR-101
    $ chantier take CR-102 --epoch 1  → exit 0
      took CR-102 (2 of 2 slots held)
      CR-102 "Board blocked" (change) working in batch batch-01 (parallel)
      cli: uv run --no-sync --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" chantier <command> --batch batch-01
      cards: C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/ (driver.md, concepts.md; each worker's own card, named in its opening lines); the project's rules rank above them: `rules`
      project instructions: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj/AGENTS.md
      specification: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj/.agents/changes/4-batch/2-actives/102-board-blocked/03-change-spec.md
      folder: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj/.agents/changes/4-batch/2-actives/102-board-blocked (work/, evidence/)
      worktree: C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj.worktrees\batch-01-CR-102 branch chantier/batch-01/cr-102-board-blocked base origin/main; not created yet: a Driver creates it first
      PR: none; head -
      rounds: 0 of 3
      notes: none
      gates before handback ready, at the PR's head not shipped yet (the full SHA; the gate log's first line names it):
        [ ] long gate passed (gate CR-102 "<cmd>" ["<cmd>"...]; none in the project's rules: handback CR-102 ready --no-gate "<rule>")
        [ ] verdict VERIFIED (the Verifier: verdict CR-102 VERIFIED|"NOT VERIFIED")
      coder prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier coder for CR-102 "Board blocked" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/coder.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      conflict-resolver prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier conflict-resolver for CR-102 "Board blocked" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/conflict-resolver.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      debugger prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier debugger for CR-102 "Board blocked" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/debugger.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      inspector prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier inspector for CR-102 "Board blocked" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/inspector.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      investigator prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier investigator for CR-102 "Board blocked" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/investigator.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      verifier prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier verifier for CR-102 "Board blocked" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/verifier.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
    $ chantier agents set CR-102 agent-CR-102 --epoch 1  → exit 0
      CR-102 → agent-CR-102
    $ chantier round CR-101 --note edit board1.py  → exit 0
      round 1 of 3 for CR-101
      CR-101 "Board working" (change) working in batch batch-01 (parallel)
      cli: uv run --no-sync --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" chantier <command> --batch batch-01
      cards: C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/ (driver.md, concepts.md; each worker's own card, named in its opening lines); the project's rules rank above them: `rules`
      project instructions: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj/AGENTS.md
      specification: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj/.agents/changes/4-batch/2-actives/101-board-working/03-change-spec.md
      folder: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj/.agents/changes/4-batch/2-actives/101-board-working (work/, evidence/)
      worktree: C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj.worktrees\batch-01-CR-101 branch chantier/batch-01/cr-101-board-working base origin/main
      PR: none; head -
      rounds: 1 of 3
      notes: none
      gates before handback ready, at the PR's head not shipped yet (the full SHA; the gate log's first line names it):
        [ ] long gate passed (gate CR-101 "<cmd>" ["<cmd>"...]; none in the project's rules: handback CR-101 ready --no-gate "<rule>")
        [ ] verdict VERIFIED (the Verifier: verdict CR-101 VERIFIED|"NOT VERIFIED")
      coder prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier coder for CR-101 "Board working" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/coder.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      conflict-resolver prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier conflict-resolver for CR-101 "Board working" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/conflict-resolver.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      debugger prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier debugger for CR-101 "Board working" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/debugger.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      inspector prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier inspector for CR-101 "Board working" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/inspector.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      investigator prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier investigator for CR-101 "Board working" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/investigator.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      verifier prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier verifier for CR-101 "Board working" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/proj.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/verifier.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      context: not measured (no transcript found for agent agent-CR-101)
    $ chantier gate CR-101 "C:\Users\gaeta\Projets\chantier.worktrees\batch-22-CR-300\.venv\Scripts\python.exe" -m compileall -q .  → exit 0
      pass "C:\Users\gaeta\Projets\chantier.worktrees\batch-22-CR-300\.venv\Scripts\python.exe" -m compileall -q . at 4f237d6
      log C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\proj\.agents\changes\4-batch\2-actives\101-board-working\work\gates\20261116-225850.log
    $ gh pr create --base main…  → exit 0
    $ chantier ship CR-101 https://github.com/acme/demo/pull/40  → exit 0
      recorded https://github.com/acme/demo/pull/40 (base main, head 4f237d6, out of draft)
    $ chantier handback CR-102 blocked question: which colour?  → exit 0
      [driver CR-102→foreman] hand-back blocked question: which colour?
      CR-102 blocked; the Foreman asks the Chief of Staff
    $ chantier status --refresh --epoch 1  → exit 0
      batch-01 running steering direct (the Chief of Staff) shape parallel live 1/2 queued 2 foreman uuid-chief e1 heartbeat 0 min spent $0.00, 0 min old
      last closed: none
      CR-101 working r1/3 https://github.com/acme/demo/pull/40 | long gate passed 4f237d6 | step: coder r1 | -
      CR-102 blocked r0/3 - | long gate - | step: waits for the user | blocked: question: which colour? | -
      CR-103 queued r0/3 - | long gate - | -
      CR-104 queued r0/3 - | long gate - | -
      activity CR-101 not measured
      spent $0.00
- [x] `board` on a loopback address with `--port 0` prints the picked port and the link with its key, and nothing else
- [x] the key is kept in the git folder's `chantier/board.json`
- [x] with no key `/`, `/api/board`, a static file and a file answer 401
- [x] `/?k=<key>` answers 303 with the cookie (HttpOnly, SameSite=Strict) and no `k` in `Location`
- [x] a wrong key answers 401 and sets no cookie
- [x] the 303 keeps a path with spaces and non-ASCII letters, percent-encoded
- [x] `DELETE` with the good key answers 405 and no cookie
- [x] `PUT` with only `?k` answers 401 (a write needs the cookie or the header) and no cookie
- [x] `PUT` with a bad key answers 401
- [x] the key in the `X-Chantier-Board-Key` header opens the API, with no cookie
- [x] `GET /` with the cookie is HTML in UTF-8, its policy `script-src 'self'` with no `unsafe-inline`, nothing sniffed
- [x] `js/main.js` answers as text/javascript with an ETag
- [x] the policy allows scripts, styles, images and fetches from `'self'` only
- [x] every module and stylesheet the page loads answers 200 with its JavaScript or CSS type
- [x] a static file asked again with its ETag answers 304
- [x] `GET /api/board`: one project, `surface: false`, the seat counted
- [x] E2: a board of an in-project folder has no autosync (present: false) and starts no join
- [x] `state` holds each CR of the batch with its `label` as STATUS.json says it, and the fields the views need
- [x] the read data names `phase` (`coder r1`, `waits for the user`) and `next_to_start` on the queued CR of the lowest order with nothing to wait for, and on none once the budget is spent
- [x] with the budget spent no CR is next to start
- [x] it holds the inbox, `P2` and `3-ready` items with their `grill`, and a title's markup comes back as text
- [x] a title written with a byte-order mark is cleaned of it
- [x] `state` asked again with `If-None-Match` as the ETag, a weak one, a list or `*` answers 304
- [x] a stale `If-None-Match` gets the state again
- [x] `tree` lists a CR folder's files, nested ones included, and no lock
- [x] `file` gives the specification as text
- [x] `file` gives an image with its type
- [x] `file` answers 404 for a path outside the planning folder, an absolute one, a missing one and a lock file
- [x] `POST costs/recompute` answers 202
- [x] `GET costs` then gives a live figure equal to the one `status --refresh` recorded from the same transcripts
- [x] a `POST` with a foreign `Origin` answers 403
- [x] `PUT` answers 405
- [x] nothing was written in the planning folder, its files, sizes and times, nor its git status
- [x] `POST backlog/move` to P2 moves the folder and says so in the journal
- [x] `POST backlog/move` to 3-ready moves the folder and says so in the journal
- [x] `POST backlog/move` to inbox moves the folder and says so in the journal
- [x] a move to the item's own column writes nothing
- [x] a move of '4-batch-item', not in the backlog, is refused
- [x] a move of '../x', not in the backlog, is refused
- [x] a move of 'board-working', not in the backlog, is refused
- [x] `POST backlog/new` files the text byte for byte in 1-inbox
- [x] a second idea with the same slug is refused: already exists
- [x] `GET file` of a text file carries the SHA-256 of its bytes
- [x] `PUT backlog/file` with the right hash writes the text and keeps CRLF
- [x] `PUT backlog/file` with the old hash answers 409 and changes nothing
- [x] an edit of STATUS.md, `..`, a non-Markdown file, a batch CR or an archive slug is refused and writes nothing
- [x] `POST backlog/next-batch` writes next-batch.json with the sorted slugs of 3-ready
- [x] labels and a group show in the state, with the next batch and the journal count
- [x] a post-it moved alone leaves its group
- [x] the journal file is ignored by git
- [x] `POST journal/rescan` empties the journal
- [x] a write with no key answers 401
- [x] a write with a foreign `Origin` answers 403
- [x] a write whose body is not JSON answers 415
- [x] a second `board` on the same address says it is running, with the same link, exit 0
- [x] a port held by another program exits 4 with one `board not started` line naming the port and `--port`
    $ chantier seat take s-2 --over s-1  → exit 0
      seat s-2
- [x] when the seat moves the board stops by itself, exit 0
- [x] a board for the new seat starts on the same port with the same link
- [x] `board --seat s-3` registers the seat on the running board
    $ chantier seat take s-3 --over s-2  → exit 0
      seat s-3
- [x] the seat moving from s-2 to s-3 keeps the board running
    $ chantier seat take s-4 --over s-3  → exit 0
      seat s-4
- [x] the board whose seats are gone stops by itself, with no request of ours
    $ chantier seat take s-5 --over s-4  → exit 0
      seat s-5
- [x] a board that had no seat takes its first over `POST /api/seats`, then stops by itself when that session goes
- [x] an address beyond this machine prints the second line, the link in the first
- [x] `--clock` fixes `now` in the answers and in `X-Chantier-Now`
- [x] `board.port` of chantier.yaml sets the port of a board with no option
    $ chantier playbook  → exit 2
      playbook: the configuration (chantier.yaml) is not valid (1 problems)
      chantier.yaml:3: board: "port" is an integer from 1 to 65535, found "abc"
    $ chantier board --port 0  → exit 2
      stderr: error: chantier.yaml:3: board: "port" is an integer from 1 to 65535, found "abc"
- [x] an invalid `board` (port: abc) is reported by `playbook` with its line, and the board refuses to start with it
    $ chantier playbook  → exit 2
      playbook: the configuration (chantier.yaml) is not valid (1 problems)
      chantier.yaml:3: board: unknown key "color": one of host, port
    $ chantier board --port 0  → exit 2
      stderr: error: chantier.yaml:3: board: unknown key "color": one of host, port
- [x] an invalid `board` (color: red) is reported by `playbook` with its line, and the board refuses to start with it
    $ chantier playbook  → exit 2
      playbook: the configuration (chantier.yml) is not valid (1 problems)
      chantier.yml:3: board: "port" is an integer from 1 to 65535, found "abc"
- [x] `chantier.yml` alone is read like `chantier.yaml`: its problem names it, with its line
    $ chantier playbook  → exit 2
      playbook: the configuration (chantier.yaml, chantier.yml) is not valid (1 problems)
      chantier.yaml and chantier.yml are both present: keep one
- [x] `chantier.yaml` and `chantier.yml` together exit 2, naming both
    $ chantier seat leave s-5  → exit 0
      seat none
    $ chantier seat leave s-2  → exit 0
      seat none
    $ chantier seat leave s-1  → exit 0
      seat none

## 20. A planning surface: the project's plans in a repository of their own
    $ chantier preflight  → exit 0
      P1 ok   host is Claude Desktop
      P6 ok   a planning surface with projects demo, other: pass --project <name>
      P4 ok   the plugin's agents are at 0.10.0 on claude
      P5 ok   chantier 0.10.0, uv and git found; dev mode on Windows: $CHANTIER runs --no-sync; sync with uv sync --locked --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" only when no chantier process runs (the board, a gate): os error 32 otherwise
      P10 ok   every batch: the commands its agents run are allowed by your settings; not checked here: a stack, a release on its own, fixes on a grant (checked at the go when the batch uses them)
      P2, P3, P9 and 'not unattended' are the Chief of Staff's own checks
      preflight passed
- [x] preflight at a surface lists its projects and passes
    $ chantier status  → exit 2
      stderr: error: this is a planning surface with projects demo, other: pass --project <name>
- [x] a command at a surface with two projects exits 2 naming both
    $ chantier --project demo preflight  → exit 2
      P1 ok   host is Claude Desktop
      P4 ok   the plugin's agents are at 0.10.0 on claude
      P5 ok   chantier 0.10.0, uv and git found; dev mode on Windows: $CHANTIER runs --no-sync; sync with uv sync --locked --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" only when no chantier process runs (the board, a gate): os error 32 otherwise
      P6 ok   in the main checkout of surface
      P7 ok   not a linked worktree
      P8 FAIL no clone of the project at C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code (remote C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\origin.git): clone it there
      P12 ok   no chantier.yaml: the plugin's agents and models
      P11 ok   the surface is on its default branch (main)
      P10 ok   every batch: the commands its agents run are allowed by your settings; not checked here: a stack, a release on its own, fixes on a grant (checked at the go when the batch uses them)
      P2, P3, P9 and 'not unattended' are the Chief of Staff's own checks
      preflight FAILED: start nothing
- [x] a missing clone fails preflight and names the path and the remote
    $ chantier --project demo init  → exit 0
      created projects/demo/changes/1-inbox
      created projects/demo/changes/2-backlog
      created projects/demo/changes/3-ready
      created projects/demo/changes/4-batch/1-pending
      created projects/demo/changes/4-batch/2-actives
      created projects/demo/changes/4-batch/3-done
      created projects/demo/changes/5-archives
      created projects/demo/changes/6-trash
- [x] `init` makes the planning folder and its .gitignore of local files
    $ chantier --project demo preflight  → exit 0
      P1 ok   host is Claude Desktop
      P4 ok   the plugin's agents are at 0.10.0 on claude
      P5 ok   chantier 0.10.0, uv and git found; dev mode on Windows: $CHANTIER runs --no-sync; sync with uv sync --locked --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" only when no chantier process runs (the board, a gate): os error 32 otherwise
      P6 ok   in the main checkout of surface
      P7 ok   not a linked worktree
      P8 ok   project instructions: AGENTS.md
      P12 ok   no chantier.yaml: the plugin's agents and models
      P11 ok   the surface is on its default branch (main)
      P10 ok   every batch: the commands its agents run are allowed by your settings; not checked here: a stack, a release on its own, fixes on a grant (checked at the go when the batch uses them)
      P2, P3, P9 and 'not unattended' are the Chief of Staff's own checks
      preflight passed
- [x] preflight passes in the surface's main checkout
    $ chantier --project demo file Surface work  → exit 0
      filed projects/demo/changes/1-inbox/surface-work; write the intent and grill the CR here
    $ chantier --project demo triage C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\surface\projects\demo\changes\1-inbox\surface-work --priority P1  → exit 0
      triaged projects/demo/changes/2-backlog/P1/surface-work (P1)
    $ chantier --project demo file Surface second  → exit 0
      filed projects/demo/changes/1-inbox/surface-second; write the intent and grill the CR here
    $ chantier --project demo triage C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\surface\projects\demo\changes\1-inbox\surface-second --priority P1  → exit 0
      triaged projects/demo/changes/2-backlog/P1/surface-second (P1)
    $ chantier --project demo summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\surface\projects\demo\changes\2-backlog\P1\surface-work --title Surface work --summary A surface CR.  → exit 0
      summary set projects/demo/changes/2-backlog/P1/surface-work (origin verbal; 4 files)
    $ chantier --project demo summary lint  → exit 2
      1 gap(s) in 2 CRs
      projects/demo/changes/2-backlog/P1/surface-second: no summary → summary set projects/demo/changes/2-backlog/P1/surface-second --title "<title>" --summary "<the CR's state now>"
- [x] `summary set` and `lint` with --project write and read the surface's project, and its .gitignore does not ignore summary.json
    $ chantier --project demo open C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\surface\projects\demo\changes\2-backlog\P1\surface-work --direct --slots 1 --default-branch main  → exit 0
      opened batch-01 on claude: 1 CRs, 1 slots, parallel, steering direct
      next: complete the brief projects/demo/changes/4-batch/brief.md, then steer it yourself
      CR-101 Surface work: 2-backlog/P1/surface-work -> 4-batch/1-pending/101-surface-work
- [x] the batch opens in the project's planning folder, the CR path is relative to it
    $ chantier --project demo playbook --batch batch-01  → exit 0
      playbook: chantier.yaml, projects/demo/chantier.yaml, C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/chantier.yaml as batch-01 opened it, host claude
      coder: agent=chantier:coder model=haiku (claude-haiku-5-5, Claude Haiku 5.5) [repository]
      conflict-resolver: agent=chantier:conflict-resolver model=(its file's)
      cr-driver: agent=chantier:cr-driver model=(its file's)
      debugger: agent=chantier:debugger model=(its file's)
      demo-explorer: agent=chantier:demo-explorer model=(its file's)
      inspector: agent=chantier:inspector model=(its file's)
      investigator: agent=chantier:investigator model=(its file's)
      qa-driver: agent=chantier:qa-driver model=(its file's)
      release-driver: agent=chantier:release-driver model=(its file's)
      retro-critic: agent=chantier:retro-critic model=(its file's)
      spec-critic: agent=chantier:spec-critic model=(its file's)
      spec-writer: agent=chantier:spec-writer model=(its file's)
      stack-driver: agent=chantier:stack-driver model=(its file's)
      verifier: agent=chantier:verifier model=(its file's)
      retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      escalate: opus (claude-opus-5-5, Claude Opus 5.5)
    $ chantier --project demo playbook  → exit 0
      playbook: chantier.yaml, projects/demo/chantier.yaml, C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/chantier.yaml, valid, host claude
      coder: agent=chantier:coder model=haiku (claude-haiku-5-5, Claude Haiku 5.5) [repository]
      conflict-resolver: agent=chantier:conflict-resolver model=(its file's)
      cr-driver: agent=chantier:cr-driver model=(its file's)
      debugger: agent=chantier:debugger model=(its file's)
      demo-explorer: agent=chantier:demo-explorer model=(its file's)
      inspector: agent=chantier:inspector model=(its file's)
      investigator: agent=chantier:investigator model=(its file's)
      qa-driver: agent=chantier:qa-driver model=(its file's)
      release-driver: agent=chantier:release-driver model=(its file's)
      retro-critic: agent=chantier:retro-critic model=(its file's)
      spec-critic: agent=chantier:spec-critic model=(its file's)
      spec-writer: agent=chantier:spec-writer model=(its file's)
      stack-driver: agent=chantier:stack-driver model=(its file's)
      verifier: agent=chantier:verifier model=(its file's)
      retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      spec-critic prompt, first line: chantier spec-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      spec-writer prompt, first line: chantier spec-writer for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      escalate: opus (claude-opus-5-5, Claude Opus 5.5)
    $ chantier --project demo playbook  → exit 0
      playbook: chantier.yaml, projects/demo/chantier.yaml, C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/chantier.yaml, valid, host claude
      coder: agent=chantier:coder model=haiku (claude-haiku-5-5, Claude Haiku 5.5) [repository]
      conflict-resolver: agent=chantier:conflict-resolver model=(its file's)
      cr-driver: agent=chantier:cr-driver model=(its file's)
      debugger: agent=chantier:debugger model=(its file's)
      demo-explorer: agent=chantier:demo-explorer model=(its file's)
      inspector: agent=chantier:inspector model=(its file's)
      investigator: agent=chantier:investigator model=(its file's)
      qa-driver: agent=chantier:qa-driver model=(its file's)
      release-driver: agent=chantier:release-driver model=(its file's)
      retro-critic: agent=chantier:retro-critic model=(its file's)
      spec-critic: agent=chantier:spec-critic model=(its file's)
      spec-writer: agent=chantier:spec-writer model=(its file's)
      stack-driver: agent=chantier:stack-driver model=(its file's)
      verifier: agent=chantier:verifier model=(its file's)
      retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      spec-critic prompt, first line: chantier spec-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      spec-writer prompt, first line: chantier spec-writer for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      escalate: opus (claude-opus-5-5, Claude Opus 5.5)
- [x] a surface root, a project folder and a code repository each set the Coder's model: `playbook` prints the repository's with its label, and `open` froze it
    $ chantier --project demo playbook  → exit 0
      playbook: chantier.yaml, projects/demo/chantier.yaml, C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/chantier.yaml, valid, host claude
      coder: agent=chantier:coder model=(its file's) [reset in repository]
      conflict-resolver: agent=chantier:conflict-resolver model=(its file's)
      cr-driver: agent=chantier:cr-driver model=(its file's)
      debugger: agent=chantier:debugger model=(its file's)
      demo-explorer: agent=chantier:demo-explorer model=(its file's)
      inspector: agent=chantier:inspector model=(its file's)
      investigator: agent=chantier:investigator model=(its file's)
      qa-driver: agent=chantier:qa-driver model=(its file's)
      release-driver: agent=chantier:release-driver model=(its file's)
      retro-critic: agent=chantier:retro-critic model=(its file's)
      spec-critic: agent=chantier:spec-critic model=(its file's)
      spec-writer: agent=chantier:spec-writer model=(its file's)
      stack-driver: agent=chantier:stack-driver model=(its file's)
      verifier: agent=chantier:verifier model=(its file's)
      retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      spec-critic prompt, first line: chantier spec-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      spec-writer prompt, first line: chantier spec-writer for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      escalate: opus (claude-opus-5-5, Claude Opus 5.5)
    $ chantier --project demo playbook --batch batch-01  → exit 0
      playbook: chantier.yaml, projects/demo/chantier.yaml, C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/chantier.yaml as batch-01 opened it, host claude
      coder: agent=chantier:coder model=haiku (claude-haiku-5-5, Claude Haiku 5.5) [repository]
      conflict-resolver: agent=chantier:conflict-resolver model=(its file's)
      cr-driver: agent=chantier:cr-driver model=(its file's)
      debugger: agent=chantier:debugger model=(its file's)
      demo-explorer: agent=chantier:demo-explorer model=(its file's)
      inspector: agent=chantier:inspector model=(its file's)
      investigator: agent=chantier:investigator model=(its file's)
      qa-driver: agent=chantier:qa-driver model=(its file's)
      release-driver: agent=chantier:release-driver model=(its file's)
      retro-critic: agent=chantier:retro-critic model=(its file's)
      spec-critic: agent=chantier:spec-critic model=(its file's)
      spec-writer: agent=chantier:spec-writer model=(its file's)
      stack-driver: agent=chantier:stack-driver model=(its file's)
      verifier: agent=chantier:verifier model=(its file's)
      retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      escalate: opus (claude-opus-5-5, Claude Opus 5.5)
    $ chantier --project demo playbook  → exit 0
      playbook: chantier.yaml, projects/demo/chantier.yaml, C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/chantier.yaml, valid, host claude
      coder: agent=chantier:coder model=(its file's) [reset in repository]
      conflict-resolver: agent=chantier:conflict-resolver model=(its file's)
      cr-driver: agent=chantier:cr-driver model=(its file's)
      debugger: agent=chantier:debugger model=(its file's)
      demo-explorer: agent=chantier:demo-explorer model=(its file's)
      inspector: agent=chantier:inspector model=(its file's)
      investigator: agent=chantier:investigator model=(its file's)
      qa-driver: agent=chantier:qa-driver model=(its file's)
      release-driver: agent=chantier:release-driver model=(its file's)
      retro-critic: agent=chantier:retro-critic model=(its file's)
      spec-critic: agent=chantier:spec-critic model=(its file's)
      spec-writer: agent=chantier:spec-writer model=(its file's)
      stack-driver: agent=chantier:stack-driver model=(its file's)
      verifier: agent=chantier:verifier model=(its file's)
      retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      spec-critic prompt, first line: chantier spec-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      spec-writer prompt, first line: chantier spec-writer for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      escalate: opus (claude-opus-5-5, Claude Opus 5.5)
    $ chantier --project demo playbook --batch batch-01  → exit 0
      playbook: chantier.yaml, projects/demo/chantier.yaml, C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/chantier.yaml as batch-01 opened it, host claude
      coder: agent=chantier:coder model=haiku (claude-haiku-5-5, Claude Haiku 5.5) [repository]
      conflict-resolver: agent=chantier:conflict-resolver model=(its file's)
      cr-driver: agent=chantier:cr-driver model=(its file's)
      debugger: agent=chantier:debugger model=(its file's)
      demo-explorer: agent=chantier:demo-explorer model=(its file's)
      inspector: agent=chantier:inspector model=(its file's)
      investigator: agent=chantier:investigator model=(its file's)
      qa-driver: agent=chantier:qa-driver model=(its file's)
      release-driver: agent=chantier:release-driver model=(its file's)
      retro-critic: agent=chantier:retro-critic model=(its file's)
      spec-critic: agent=chantier:spec-critic model=(its file's)
      spec-writer: agent=chantier:spec-writer model=(its file's)
      stack-driver: agent=chantier:stack-driver model=(its file's)
      verifier: agent=chantier:verifier model=(its file's)
      retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      escalate: opus (claude-opus-5-5, Claude Opus 5.5)
- [x] the repository's `model: default` takes the model back to its file's, `[reset in repository]`
    $ chantier --project demo playbook  → exit 0
      playbook: chantier.yaml, projects/demo/chantier.yaml, valid, host claude
      coder: agent=chantier:coder model=opus (claude-opus-5-5, Claude Opus 5.5) [surface project]
      conflict-resolver: agent=chantier:conflict-resolver model=(its file's)
      cr-driver: agent=chantier:cr-driver model=(its file's)
      debugger: agent=chantier:debugger model=(its file's)
      demo-explorer: agent=chantier:demo-explorer model=(its file's)
      inspector: agent=chantier:inspector model=(its file's)
      investigator: agent=chantier:investigator model=(its file's)
      qa-driver: agent=chantier:qa-driver model=(its file's)
      release-driver: agent=chantier:release-driver model=(its file's)
      retro-critic: agent=chantier:retro-critic model=(its file's)
      spec-critic: agent=chantier:spec-critic model=(its file's)
      spec-writer: agent=chantier:spec-writer model=(its file's)
      stack-driver: agent=chantier:stack-driver model=(its file's)
      verifier: agent=chantier:verifier model=(its file's)
      retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      spec-critic prompt, first line: chantier spec-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      spec-writer prompt, first line: chantier spec-writer for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      escalate: opus (claude-opus-5-5, Claude Opus 5.5)
    $ chantier --project demo playbook --batch batch-01  → exit 0
      playbook: chantier.yaml, projects/demo/chantier.yaml, C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/chantier.yaml as batch-01 opened it, host claude
      coder: agent=chantier:coder model=haiku (claude-haiku-5-5, Claude Haiku 5.5) [repository]
      conflict-resolver: agent=chantier:conflict-resolver model=(its file's)
      cr-driver: agent=chantier:cr-driver model=(its file's)
      debugger: agent=chantier:debugger model=(its file's)
      demo-explorer: agent=chantier:demo-explorer model=(its file's)
      inspector: agent=chantier:inspector model=(its file's)
      investigator: agent=chantier:investigator model=(its file's)
      qa-driver: agent=chantier:qa-driver model=(its file's)
      release-driver: agent=chantier:release-driver model=(its file's)
      retro-critic: agent=chantier:retro-critic model=(its file's)
      spec-critic: agent=chantier:spec-critic model=(its file's)
      spec-writer: agent=chantier:spec-writer model=(its file's)
      stack-driver: agent=chantier:stack-driver model=(its file's)
      verifier: agent=chantier:verifier model=(its file's)
      retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      escalate: opus (claude-opus-5-5, Claude Opus 5.5)
    $ chantier --project demo playbook  → exit 0
      playbook: chantier.yaml, projects/demo/chantier.yaml, valid, host claude
      coder: agent=chantier:coder model=opus (claude-opus-5-5, Claude Opus 5.5) [surface project]
      conflict-resolver: agent=chantier:conflict-resolver model=(its file's)
      cr-driver: agent=chantier:cr-driver model=(its file's)
      debugger: agent=chantier:debugger model=(its file's)
      demo-explorer: agent=chantier:demo-explorer model=(its file's)
      inspector: agent=chantier:inspector model=(its file's)
      investigator: agent=chantier:investigator model=(its file's)
      qa-driver: agent=chantier:qa-driver model=(its file's)
      release-driver: agent=chantier:release-driver model=(its file's)
      retro-critic: agent=chantier:retro-critic model=(its file's)
      spec-critic: agent=chantier:spec-critic model=(its file's)
      spec-writer: agent=chantier:spec-writer model=(its file's)
      stack-driver: agent=chantier:stack-driver model=(its file's)
      verifier: agent=chantier:verifier model=(its file's)
      retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      spec-critic prompt, first line: chantier spec-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      spec-writer prompt, first line: chantier spec-writer for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      escalate: opus (claude-opus-5-5, Claude Opus 5.5)
    $ chantier --project demo playbook --batch batch-01  → exit 0
      playbook: chantier.yaml, projects/demo/chantier.yaml, C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/chantier.yaml as batch-01 opened it, host claude
      coder: agent=chantier:coder model=haiku (claude-haiku-5-5, Claude Haiku 5.5) [repository]
      conflict-resolver: agent=chantier:conflict-resolver model=(its file's)
      cr-driver: agent=chantier:cr-driver model=(its file's)
      debugger: agent=chantier:debugger model=(its file's)
      demo-explorer: agent=chantier:demo-explorer model=(its file's)
      inspector: agent=chantier:inspector model=(its file's)
      investigator: agent=chantier:investigator model=(its file's)
      qa-driver: agent=chantier:qa-driver model=(its file's)
      release-driver: agent=chantier:release-driver model=(its file's)
      retro-critic: agent=chantier:retro-critic model=(its file's)
      spec-critic: agent=chantier:spec-critic model=(its file's)
      spec-writer: agent=chantier:spec-writer model=(its file's)
      stack-driver: agent=chantier:stack-driver model=(its file's)
      verifier: agent=chantier:verifier model=(its file's)
      retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
      escalate: opus (claude-opus-5-5, Claude Opus 5.5)
- [x] with the repository's file removed, `playbook` prints the project folder's value `[surface project]`; the batch still prints the frozen one
    $ chantier --project demo open C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\surface\projects\demo\changes\2-backlog\P1\surface-second --direct --default-branch main  → exit 2
      stderr: error: batch-01 is not closed (a paused batch stays until `close`): `order add` joins new work to it
- [x] a second open on the same project is refused
    $ chantier --project other file Other work  → exit 0
      filed projects/other/changes/1-inbox/other-work; write the intent and grill the CR here
    $ chantier --project other triage C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\surface\projects\other\changes\1-inbox\other-work --priority P1  → exit 0
      triaged projects/other/changes/2-backlog/P1/other-work (P1)
    $ chantier --project other init  → exit 0
      exists  projects/other/changes/1-inbox
      exists  projects/other/changes/2-backlog
      created projects/other/changes/3-ready
      created projects/other/changes/4-batch/1-pending
      created projects/other/changes/4-batch/2-actives
      created projects/other/changes/4-batch/3-done
      created projects/other/changes/5-archives
      created projects/other/changes/6-trash
    $ chantier --project other open C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\surface\projects\other\changes\2-backlog\P1\other-work --direct --default-branch main  → exit 2
      stderr: error: projects/other/chantier.yaml:6: role "coder": Copilot cannot start a named agent with a model (hosts/copilot.md, "Models at an agent's start"): remove "model" for coder under hosts.copilot.roles, or name the model in your agent's own file
- [x] on Copilot, the user's own agent with a model is refused by `open` (exit 2, the line named, the cause given) and nothing moved
    $ chantier --project other playbook  → exit 0
      playbook: projects/other/chantier.yaml, valid, host copilot
      coder: agent=(generic) model=gpt-6.1-terra (gpt-6.1-terra, GPT-6.1 Terra) [surface project] tools=(the caller's, not restricted)
      conflict-resolver: agent=chantier-conflict-resolver model=(its file's)
      cr-driver: agent=chantier-cr-driver model=(its file's)
      debugger: agent=chantier-debugger model=(its file's)
      demo-explorer: agent=chantier-demo-explorer model=(its file's)
      inspector: agent=chantier-inspector model=(its file's)
      investigator: agent=chantier-investigator model=(its file's)
      qa-driver: agent=chantier-qa-driver model=(its file's)
      release-driver: agent=chantier-release-driver model=(its file's)
      retro-critic: agent=chantier-retro-critic model=(its file's)
      spec-critic: agent=chantier-spec-critic model=(its file's)
      spec-writer: agent=chantier-spec-writer model=(its file's)
      stack-driver: agent=chantier-stack-driver model=(its file's)
      verifier: agent=chantier-verifier model=(its file's)
      retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code2.
      spec-critic prompt, first line: chantier spec-critic for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code2.
      spec-writer prompt, first line: chantier spec-writer for the Chief of Staff, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code2.
      escalate: (none on this host)
- [x] on Copilot, a model with no agent starts a generic agent: `playbook` prints `agent=(generic)` and the tools line
    $ chantier --project other open C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\surface\projects\other\changes\2-backlog\P1\other-work --direct --slots 1 --default-branch main  → exit 0
      opened batch-01 on copilot: 1 CRs, 1 slots, parallel, steering direct
      next: complete the brief projects/other/changes/4-batch/brief.md, then steer it yourself
      CR-101 Other work: 2-backlog/P1/other-work -> 4-batch/1-pending/101-other-work
    $ chantier --project demo seat take sess-a --env remote --title [remote] surface --link l  → exit 0
      seat sess-a
    $ chantier --project other seat get  → exit 0
      seat none
- [x] two projects of one surface each run a batch, and the seat is one per project
    $ chantier --project demo seat leave sess-a  → exit 0
      seat none
    $ chantier --project other foreman set uuid-chief --epoch 1 --batch batch-01  → exit 0
      foreman uuid-chief epoch 1
    $ chantier --project other take CR-101 --epoch 1 --batch batch-01  → exit 0
      took CR-101 (1 of 1 slots held)
      CR-101 "Other work" (change) working in batch batch-01 (parallel)
      cli: uv run --no-sync --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" chantier --project "C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/surface/projects/other" <command> --batch batch-01
      cards: C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/ (driver.md, concepts.md; each worker's own card, named in its opening lines); the project's rules rank above them: `rules`
      project instructions: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code2/AGENTS.md
      specification: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/surface/projects/other/changes/4-batch/2-actives/101-other-work/03-change-spec.md
      folder: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/surface/projects/other/changes/4-batch/2-actives/101-other-work (work/, evidence/)
      worktree: C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\wt2\batch-01-CR-101 branch chantier/batch-01/cr-101-other-work base origin/main; not created yet: a Driver creates it first
      clone: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code2 (`git -C` it to create the worktree)
      archive: not in the PR
      PR: none; head -
      rounds: 0 of 3
      notes: none
      gates before handback ready, at the PR's head not shipped yet (the full SHA; the gate log's first line names it):
        [ ] long gate passed (gate CR-101 "<cmd>" ["<cmd>"...]; none in the project's rules: handback CR-101 ready --no-gate "<rule>")
        [ ] verdict VERIFIED (the Verifier: verdict CR-101 VERIFIED|"NOT VERIFIED")
      team: coder agent=(generic) model=gpt-6.1-terra (gpt-6.1-terra, GPT-6.1 Terra) [surface project] tools=(the caller's, not restricted)
      coder prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier coder for CR-101 "Other work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code2.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/coder.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      coder contract (a generic agent: copy it unchanged, without the two leading spaces, after the opening lines):
        # chantier-agent: 0.10.0
        
        You are the chantier Coder. Your prompt is your whole brief: it names the files
        to read first, the CLI to use, the worktree to work in and the folder to write to. Read
        the startup core and the short Startup core section of your card first; defer all other card sections until the action names them, then do only your role's part and reply as your card says.
        
        Your card is `coder.md`: read it first, before any other step,
        at the path your prompt's `Read` line gives, and reply in the format it names. The card is
        your contract; this file only points to it.
        
        A prompt that does not start with `chantier coder`, or that names no path to my card
        `coder.md`, is not a chantier prompt: answer
        "I run inside a chantier batch only. My prompt must start with `chantier coder for <cr> "<title>" of batch <batch>, in the project <root>.`, and its `Read` line must name my card, `coder.md`;
        a message to me gets this same answer: start a new agent with that line." and stop. Any later message gets the same answer.
      conflict-resolver prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier conflict-resolver for CR-101 "Other work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code2.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/conflict-resolver.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      debugger prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier debugger for CR-101 "Other work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code2.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/debugger.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      inspector prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier inspector for CR-101 "Other work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code2.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/inspector.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      investigator prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier investigator for CR-101 "Other work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code2.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/investigator.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      verifier prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier verifier for CR-101 "Other work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code2.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/verifier.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
- [x] a project set to keep its archive out of the PR says so in the facts
- [x] `take` prints the generic Coder's contract after its opening lines, and the team line says `agent=(generic)`
    $ chantier --project demo foreman set uuid-chief --epoch 1  → exit 0
      foreman uuid-chief epoch 1
    $ chantier --project demo foreman transcript uuid-chief --epoch 1  → exit 0
      transcript uuid-chief
    $ chantier --project demo take CR-101 --epoch 1  → exit 0
      took CR-101 (1 of 1 slots held)
      CR-101 "Surface work" (change) working in batch batch-01 (parallel)
      cli: uv run --no-sync --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" chantier --project "C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/surface/projects/demo" <command> --batch batch-01
      cards: C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/ (driver.md, concepts.md; each worker's own card, named in its opening lines); the project's rules rank above them: `rules`
      project instructions: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/AGENTS.md
      specification: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/surface/projects/demo/changes/4-batch/2-actives/101-surface-work/03-change-spec.md
      folder: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/surface/projects/demo/changes/4-batch/2-actives/101-surface-work (work/, evidence/)
      worktree: C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\wt\batch-01-CR-101 branch chantier/batch-01/cr-101-surface-work base origin/main; not created yet: a Driver creates it first
      clone: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code (`git -C` it to create the worktree)
      archive: in the PR at .agents/changes/5-archives/261116-2159-101-surface-work/
      PR: none; head -
      rounds: 0 of 3
      notes: none
      gates before handback ready, at the PR's head not shipped yet (the full SHA; the gate log's first line names it):
        [ ] long gate passed (gate CR-101 "<cmd>" ["<cmd>"...]; none in the project's rules: handback CR-101 ready --no-gate "<rule>")
        [ ] verdict VERIFIED (the Verifier: verdict CR-101 VERIFIED|"NOT VERIFIED")
      team: coder model=haiku (claude-haiku-5-5, Claude Haiku 5.5) [repository]
      coder prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier coder for CR-101 "Surface work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/coder.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      conflict-resolver prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier conflict-resolver for CR-101 "Surface work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/conflict-resolver.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      debugger prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier debugger for CR-101 "Surface work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/debugger.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      inspector prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier inspector for CR-101 "Surface work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/inspector.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      investigator prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier investigator for CR-101 "Surface work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/investigator.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      verifier prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier verifier for CR-101 "Surface work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/verifier.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
    $ chantier --project demo agents set CR-101 agent-1 --epoch 1  → exit 0
      CR-101 → agent-1
- [x] the facts carry `cli:` with --project, the clone and the archive path
- [x] the worktree is created under the project's `worktrees` folder, outside the surface
    $ chantier --project demo rules  → exit 0
      project:
      C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/AGENTS.md (5 lines)
      C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/CONTRIBUTING.md (3 lines)
      surface:
      C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/surface/AGENTS.md (3 lines)
- [x] `rules` lists the project's instructions, then the surface's
- [x] after the take: the surface's git lists no local file
- [x] after the take: and still lists the CR's documents
- [x] E7: the files of a second long-gate slot and a move-up marker are not published by the surface
    $ chantier --project demo preflight  → exit 0
      P1 ok   host is Claude Desktop
      P4 ok   the plugin's agents are at 0.10.0 on claude
      P5 ok   chantier 0.10.0, uv and git found; dev mode on Windows: $CHANTIER runs --no-sync; sync with uv sync --locked --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" only when no chantier process runs (the board, a gate): os error 32 otherwise
      P6 ok   in the main checkout of surface
      P7 ok   not a linked worktree
      P8 ok   project instructions: AGENTS.md
      P12 ok   no chantier.yaml: the plugin's agents and models
      P11 ok   the surface is on its default branch (main)
      P10 ok   every batch: the commands its agents run are allowed by your settings; not checked here: a stack, a release on its own, fixes on a grant (checked at the go when the batch uses them)
      P2, P3, P9 and 'not unattended' are the Chief of Staff's own checks
      preflight passed
    $ chantier --project demo status  → exit 0
      batch-01 running steering direct (the Chief of Staff) shape parallel live 1/1 queued 0 foreman uuid-chief e1 heartbeat never spent unknown
      last closed: none
      CR-101 working r0/3 - | long gate - | -
- [x] E2: a surface whose rules do not name the autosync has no P13 and no status line
    $ chantier --project demo preflight  → exit 0
      P1 ok   host is Claude Desktop
      P4 ok   the plugin's agents are at 0.10.0 on claude
      P5 ok   chantier 0.10.0, uv and git found; dev mode on Windows: $CHANTIER runs --no-sync; sync with uv sync --locked --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" only when no chantier process runs (the board, a gate): os error 32 otherwise
      P6 ok   in the main checkout of surface
      P7 ok   not a linked worktree
      P8 ok   project instructions: AGENTS.md
      P12 ok   no chantier.yaml: the plugin's agents and models
      P11 ok   the surface is on its default branch (main)
      P13 warn the surface names an autosync but scripts/ai-autosync-git.py is missing: no autosync until it is there
      P10 ok   every batch: the commands its agents run are allowed by your settings; not checked here: a stack, a release on its own, fixes on a grant (checked at the go when the batch uses them)
      P2, P3, P9 and 'not unattended' are the Chief of Staff's own checks
      preflight passed
    $ chantier --project demo status  → exit 0
      batch-01 running steering direct (the Chief of Staff) shape parallel live 1/1 queued 0 foreman uuid-chief e1 heartbeat never spent unknown
      last closed: none
      CR-101 working r0/3 - | long gate - | -
- [x] E2: the rules name it but the script is missing: P13 warns, and no status line
    $ chantier --project demo preflight  → exit 0
      P1 ok   host is Claude Desktop
      P4 ok   the plugin's agents are at 0.10.0 on claude
      P5 ok   chantier 0.10.0, uv and git found; dev mode on Windows: $CHANTIER runs --no-sync; sync with uv sync --locked --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" only when no chantier process runs (the board, a gate): os error 32 otherwise
      P6 ok   in the main checkout of surface
      P7 ok   not a linked worktree
      P8 ok   project instructions: AGENTS.md
      P12 ok   no chantier.yaml: the plugin's agents and models
      P11 ok   the surface is on its default branch (main)
      P13 warn the surface's autosync has no group yet: join it (.agents/guidelines/autosync.guidelines.md)
      P10 ok   every batch: the commands its agents run are allowed by your settings; not checked here: a stack, a release on its own, fixes on a grant (checked at the go when the batch uses them)
      P2, P3, P9 and 'not unattended' are the Chief of Staff's own checks
      preflight passed
    $ chantier --project demo status  → exit 0
      batch-01 running steering direct (the Chief of Staff) shape parallel live 1/1 queued 0 foreman uuid-chief e1 heartbeat never spent unknown
      autosync: no group yet
      last closed: none
      CR-101 working r0/3 - | long gate - | -
- [x] E2: the script is there and no group ran yet: `no group yet` in both lines
    $ chantier --project demo preflight  → exit 0
      P1 ok   host is Claude Desktop
      P4 ok   the plugin's agents are at 0.10.0 on claude
      P5 ok   chantier 0.10.0, uv and git found; dev mode on Windows: $CHANTIER runs --no-sync; sync with uv sync --locked --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" only when no chantier process runs (the board, a gate): os error 32 otherwise
      P6 ok   in the main checkout of surface
      P7 ok   not a linked worktree
      P8 ok   project instructions: AGENTS.md
      P12 ok   no chantier.yaml: the plugin's agents and models
      P11 ok   the surface is on its default branch (main)
      P13 ok   the surface's autosync is active: leader session scen0001, 1 participant
      P10 ok   every batch: the commands its agents run are allowed by your settings; not checked here: a stack, a release on its own, fixes on a grant (checked at the go when the batch uses them)
      P2, P3, P9 and 'not unattended' are the Chief of Staff's own checks
      preflight passed
    $ chantier --project demo status  → exit 0
      batch-01 running steering direct (the Chief of Staff) shape parallel live 1/1 queued 0 foreman uuid-chief e1 heartbeat never spent unknown
      autosync active, leader session scen0001, 1 participant, synced 23:13
      last closed: none
      CR-101 working r0/3 - | long gate - | -
- [x] E2: active, one live participant (the dead one is not counted): both lines say so
    $ chantier --project demo preflight  → exit 0
      P1 ok   host is Claude Desktop
      P4 ok   the plugin's agents are at 0.10.0 on claude
      P5 ok   chantier 0.10.0, uv and git found; dev mode on Windows: $CHANTIER runs --no-sync; sync with uv sync --locked --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" only when no chantier process runs (the board, a gate): os error 32 otherwise
      P6 ok   in the main checkout of surface
      P7 ok   not a linked worktree
      P8 ok   project instructions: AGENTS.md
      P12 ok   no chantier.yaml: the plugin's agents and models
      P11 ok   the surface is on its default branch (main)
      P13 warn the surface's autosync is active but has no live participant: join it (.agents/guidelines/autosync.guidelines.md)
      P10 ok   every batch: the commands its agents run are allowed by your settings; not checked here: a stack, a release on its own, fixes on a grant (checked at the go when the batch uses them)
      P2, P3, P9 and 'not unattended' are the Chief of Staff's own checks
      preflight passed
    $ chantier --project demo status  → exit 0
      batch-01 running steering direct (the Chief of Staff) shape parallel live 1/1 queued 0 foreman uuid-chief e1 heartbeat never spent unknown
      autosync active, no live participant: join it
      last closed: none
      CR-101 working r0/3 - | long gate - | -
- [x] E2: active with no live participant: both lines ask to join
    $ chantier --project demo preflight  → exit 0
      P1 ok   host is Claude Desktop
      P4 ok   the plugin's agents are at 0.10.0 on claude
      P5 ok   chantier 0.10.0, uv and git found; dev mode on Windows: $CHANTIER runs --no-sync; sync with uv sync --locked --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" only when no chantier process runs (the board, a gate): os error 32 otherwise
      P6 ok   in the main checkout of surface
      P7 ok   not a linked worktree
      P8 ok   project instructions: AGENTS.md
      P12 ok   no chantier.yaml: the plugin's agents and models
      P11 ok   the surface is on its default branch (main)
      P13 ok   the surface's autosync is stopped (stopped by user): commit the surface by hand
      P10 ok   every batch: the commands its agents run are allowed by your settings; not checked here: a stack, a release on its own, fixes on a grant (checked at the go when the batch uses them)
      P2, P3, P9 and 'not unattended' are the Chief of Staff's own checks
      preflight passed
    $ chantier --project demo status  → exit 0
      batch-01 running steering direct (the Chief of Staff) shape parallel live 1/1 queued 0 foreman uuid-chief e1 heartbeat never spent unknown
      autosync stopped (stopped by user): commit the surface by hand
      last closed: none
      CR-101 working r0/3 - | long gate - | -
- [x] E2: stopped: both lines say to commit the surface by hand
    $ chantier --project demo preflight  → exit 0
      P1 ok   host is Claude Desktop
      P4 ok   the plugin's agents are at 0.10.0 on claude
      P5 ok   chantier 0.10.0, uv and git found; dev mode on Windows: $CHANTIER runs --no-sync; sync with uv sync --locked --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" only when no chantier process runs (the board, a gate): os error 32 otherwise
      P6 ok   in the main checkout of surface
      P7 ok   not a linked worktree
      P8 ok   project instructions: AGENTS.md
      P12 ok   no chantier.yaml: the plugin's agents and models
      P11 ok   the surface is on its default branch (main)
      P13 warn the surface's autosync is blocked: upstream moved: the Chief of Staff integrates, then start . --enable-only
      P10 ok   every batch: the commands its agents run are allowed by your settings; not checked here: a stack, a release on its own, fixes on a grant (checked at the go when the batch uses them)
      P2, P3, P9 and 'not unattended' are the Chief of Staff's own checks
      preflight passed
    $ chantier --project demo status  → exit 0
      batch-01 running steering direct (the Chief of Staff) shape parallel live 1/1 queued 0 foreman uuid-chief e1 heartbeat never spent unknown
      autosync blocked: upstream moved: the Chief of Staff integrates, then start . --enable-only
      last closed: none
      CR-101 working r0/3 - | long gate - | -
- [x] E2: blocked: both lines give the reason and who restarts it
    $ chantier --project demo preflight  → exit 0
      P1 ok   host is Claude Desktop
      P4 ok   the plugin's agents are at 0.10.0 on claude
      P5 ok   chantier 0.10.0, uv and git found; dev mode on Windows: $CHANTIER runs --no-sync; sync with uv sync --locked --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" only when no chantier process runs (the board, a gate): os error 32 otherwise
      P6 ok   in the main checkout of surface
      P7 ok   not a linked worktree
      P8 ok   project instructions: AGENTS.md
      P12 ok   no chantier.yaml: the plugin's agents and models
      P11 ok   the surface is on its default branch (main)
      P13 warn the surface's autosync waits for the user's approval of incident staged-0123456789abcdef0123: 3 files staged
      P10 ok   every batch: the commands its agents run are allowed by your settings; not checked here: a stack, a release on its own, fixes on a grant (checked at the go when the batch uses them)
      P2, P3, P9 and 'not unattended' are the Chief of Staff's own checks
      preflight passed
    $ chantier --project demo status  → exit 0
      batch-01 running steering direct (the Chief of Staff) shape parallel live 1/1 queued 0 foreman uuid-chief e1 heartbeat never spent unknown
      autosync waits for the user's approval: incident staged-0123456789abcdef0123: 3 files staged
      last closed: none
      CR-101 working r0/3 - | long gate - | -
- [x] E2: an approval: both lines name the incident
- [x] E2: reading never deletes a participant file, a dead one included
- [x] E2: the board starts without joining the surface's autosync
- [x] E2: the board does not create an autosync participant
- [x] E2: the board reports autosync independently
- [x] E2: stop is refused while the group is stopped
- [x] E2: start in the stopped state runs `start . --enable-only` and the group is active
- [x] E2: start is refused while blocked: the Chief of Staff restarts it
- [x] E2: approving an incident that is not the one waiting is refused (stale)
- [x] E2: approving the current incident runs `approve . <id>` then `start . --enable-only`
- [x] E2: a POST without the JSON content type is refused
- [x] `board` at a surface starts with the link and its key
- [x] the surface's board serves both projects (`surface: true`, two lines)
- [x] the project's state lists its CR
- [x] the other project's folder is reached through its own id
- [x] the surface's board refuses the other project's folder through a `..` path
- [x] the surface's board refuses the code clone through a `..` path
    $ chantier --project demo round CR-101 --note edit surface.py  → exit 0
      round 1 of 3 for CR-101
      CR-101 "Surface work" (change) working in batch batch-01 (parallel)
      cli: uv run --no-sync --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300" chantier --project "C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/surface/projects/demo" <command> --batch batch-01
      cards: C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/ (driver.md, concepts.md; each worker's own card, named in its opening lines); the project's rules rank above them: `rules`
      project instructions: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code/AGENTS.md
      specification: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/surface/projects/demo/changes/4-batch/2-actives/101-surface-work/03-change-spec.md
      folder: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/surface/projects/demo/changes/4-batch/2-actives/101-surface-work (work/, evidence/)
      worktree: C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\wt\batch-01-CR-101 branch chantier/batch-01/cr-101-surface-work base origin/main
      clone: C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code (`git -C` it to create the worktree)
      archive: in the PR at .agents/changes/5-archives/261116-2159-101-surface-work/
      PR: none; head -
      rounds: 1 of 3
      notes: none
      gates before handback ready, at the PR's head not shipped yet (the full SHA; the gate log's first line names it):
        [ ] long gate passed (gate CR-101 "<cmd>" ["<cmd>"...]; none in the project's rules: handback CR-101 ready --no-gate "<rule>")
        [ ] verdict VERIFIED (the Verifier: verdict CR-101 VERIFIED|"NOT VERIFIED")
      team: coder model=haiku (claude-haiku-5-5, Claude Haiku 5.5) [repository]
      coder prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier coder for CR-101 "Surface work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/coder.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      conflict-resolver prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier conflict-resolver for CR-101 "Surface work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/conflict-resolver.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      debugger prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier debugger for CR-101 "Surface work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/debugger.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      inspector prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier inspector for CR-101 "Surface work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/inspector.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      investigator prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier investigator for CR-101 "Surface work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/investigator.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      verifier prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
        chantier verifier for CR-101 "Surface work" of batch batch-01, in the project C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code.
        Read C:/Users/gaeta/Projets/chantier.worktrees/batch-22-CR-300/skills/chantier/references/verifier.md;
        the project's rules rank above it: run `$CHANTIER rules` first and read what touches your work.
      context: not measured (no transcript found for agent agent-1)
    $ chantier --project demo gate CR-101 "C:\Users\gaeta\Projets\chantier.worktrees\batch-22-CR-300\.venv\Scripts\python.exe" -m compileall -q .  → exit 0
      pass "C:\Users\gaeta\Projets\chantier.worktrees\batch-22-CR-300\.venv\Scripts\python.exe" -m compileall -q . at 87d2586
      log C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\surface\projects\demo\changes\4-batch\2-actives\101-surface-work\work\gates\20261116-230037.log
    $ gh pr create --base main…  → exit 0
    $ chantier --project demo ship CR-101 https://github.com/acme/demo/pull/40  → exit 0
      recorded https://github.com/acme/demo/pull/40 (base main, head 87d2586, out of draft)
      off: archive missing from the PR at .agents/changes/5-archives/261116-2159-101-surface-work/
- [x] `ship` says the archive is missing from the PR, at its path
    $ chantier --project demo ship CR-101 https://github.com/acme/demo/pull/40  → exit 0
      recorded https://github.com/acme/demo/pull/40 (base main, head acadfb3, out of draft)
      off: no long gate passed at acadfb3 (`chantier gate`)
- [x] with the archive in the PR, `ship` raises nothing about it
- [x] the PR's archive holds the documents and the evidence, and no work folder
- [x] after the PR: the surface's git lists no local file
- [x] after the PR: and still lists the CR's documents
- [x] the project's clone stays clean: its worktrees hold the Driver's commits
    $ chantier --project demo gate CR-101 "C:\Users\gaeta\Projets\chantier.worktrees\batch-22-CR-300\.venv\Scripts\python.exe" -m compileall -q .  → exit 0
      pass "C:\Users\gaeta\Projets\chantier.worktrees\batch-22-CR-300\.venv\Scripts\python.exe" -m compileall -q . at acadfb3
      log C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\surface\projects\demo\changes\4-batch\2-actives\101-surface-work\work\gates\20261116-230040.log
    $ chantier --project demo verdict CR-101 VERIFIED  → exit 0
      verdict CR-101 VERIFIED at acadfb3
    $ chantier --project demo handback CR-101 ready https://github.com/acme/demo/pull/40  → exit 0
      [driver CR-101→foreman] hand-back ready to merge https://github.com/acme/demo/pull/40
      CR-101 ready to merge
    $ chantier --project demo asks -- ready-to-merge CR-101 https://github.com/acme/demo/pull/40  → exit 0
      [foreman→chief-of-staff] ask A-1: ready-to-merge CR-101 https://github.com/acme/demo/pull/40
    $ gh pr merge https://github.com/acme/demo/pull/40 --rebase…  → exit 0
    $ chantier --project demo order merged CR-101  → exit 0
      [chief-of-staff→foreman] order O-1: merged CR-101
      merged CR-101: moved to 3-done
      every CR is merged or cancelled: `chantier pause --epoch <n>`
- [x] `order merged` writes delivery.md: the PR, the merge time, where the archive is
    $ chantier --project demo note CR-101 main checkout: already at d65b948  → exit 0
      ok
      context: not measured (no transcript found for agent agent-1)
    $ chantier --project demo order done O-1 --epoch 1  → exit 0
      O-1 done
    $ chantier --project demo pause --epoch 1  → exit 0
      paused batch-01: cost to date below
      report: C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\surface\projects\demo\changes\4-batch\STATUS.md
      Spent: unknown (Chief of staff transcript not found: C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\claude-projects\C--Users-gaeta-AppData-Local-Temp-cs-surface-board-vuake9hp-external-surface\uuid-chief.jsonl)
- [x] the batch pauses once its CR is merged
    $ chantier --project demo close --batch batch-01 --yes  → exit 0
      closed batch-01: its files are deleted, 1 CRs archived
      1 CRs move from 3-done to 5-archives: CR-101
      retro: kept in projects/demo/changes/5-archives/batches/batch-01.md
      record: projects/demo/changes/5-archives/batches/batch-01.json closed
      the dropped CRs, to remove on the same word where they still exist (`git -C C:/Users/gaeta/AppData/Local/Temp/cs-surface-board-vuake9hp/external/code worktree remove --force`, `git branch -D`): none
      final cost, up to now (nothing runs):
      Total: $0.00, no budget
      Chief of Staff, steering the batch $0.00 (100%), Drivers $0.00 (0%), workers $0.00 (0%)
      Most: -
      Chief of Staff, grill and specifications with the user (outside the budget): $0.00 since the batch opened (0 calls, 0 spec-writers, 0 spec critics)
      Chief of Staff, whole session: $0.00 ($0.00 of it in the batch's spend), context 10 tokens; not counted: 0 compactions since the batch opened, which leave no record (about $0.12 each)
      Not counted: compaction calls, which leave no record (about $0.12 each)
- [x] `close` puts the merged CR in 5-archives with its delivery.md, the gate log staying off the surface's git
- [x] `close` writes the batch's record and its retro in the surface's planning folder, and the CR's archive in its PR holds no retro.md and no record
- [x] after the close: the surface's git lists no local file
- [x] after the close: and still lists the CR's documents
    $ chantier --project demo summary lint C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\external\surface\projects\demo\changes\5-archives\261116-2200-101-surface-work  → exit 2
      1 gap(s) in 1 CRs
      projects/demo/changes/5-archives/261116-2200-101-surface-work: summary late (delivery.md new) → read them, then summary set projects/demo/changes/5-archives/261116-2200-101-surface-work --summary "<…>" or --unchanged
- [x] the summary travelled through take, order merged and close, and the archive's new delivery.md makes it late

## 21. A CR's summary: the linter and its commands
    $ chantier init  → exit 0
      created .agents/changes/1-inbox
      created .agents/changes/2-backlog
      created .agents/changes/3-ready
      created .agents/changes/4-batch/1-pending
      created .agents/changes/4-batch/2-actives
      created .agents/changes/4-batch/3-done
      created .agents/changes/5-archives
      created .agents/changes/6-trash
    $ chantier file Summary alpha  → exit 0
      filed .agents/changes/1-inbox/summary-alpha; write the intent and grill the CR here
    $ chantier summary lint  → exit 2
      1 gap(s) in 1 CRs
      .agents/changes/1-inbox/summary-alpha: no summary → summary set .agents/changes/1-inbox/summary-alpha --title "<title>" --summary "<the CR's state now>"
- [x] `summary lint` on a filed item exits 2: the count first, then the `no summary` line with its command
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha --title Alpha --summary Alpha is filed.  → exit 0
      summary set .agents/changes/1-inbox/summary-alpha (origin verbal; 1 files)
- [x] `summary set` writes summary.json: schema 1, a verbal origin, one source
    $ chantier summary lint  → exit 0
      no gap (1 CRs)
- [x] `lint` then says no gap
    $ chantier summary lint  → exit 0
      no gap (1 CRs)
- [x] a change in work/, evidence/ or STATUS.md, and a request rewritten with CRLF and a byte-order mark, make no gap
    $ chantier summary lint  → exit 2
      1 gap(s) in 1 CRs
      .agents/changes/1-inbox/summary-alpha: summary late (02-answers.md new, intake/02-more.md new) → read them, then summary set .agents/changes/1-inbox/summary-alpha --summary "<…>" or --unchanged
- [x] a new `02-answers.md` and a new intake file make the summary late, naming both
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha --title Alpha again  → exit 0
      summary set .agents/changes/1-inbox/summary-alpha (origin verbal; 1 files)
    $ chantier summary lint  → exit 2
      1 gap(s) in 1 CRs
      .agents/changes/1-inbox/summary-alpha: summary late (02-answers.md new, intake/02-more.md new) → read them, then summary set .agents/changes/1-inbox/summary-alpha --summary "<…>" or --unchanged
- [x] `--title` alone leaves the summary late
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha --unchanged  → exit 0
      summary set .agents/changes/1-inbox/summary-alpha (origin verbal; 3 files)
    $ chantier summary lint  → exit 0
      no gap (1 CRs)
- [x] `--unchanged` closes the gap and leaves the summary as it was
    $ chantier file Summary beta  → exit 0
      filed .agents/changes/1-inbox/summary-beta; write the intent and grill the CR here
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-beta --title Beta --summary Beta.  → exit 0
      summary set .agents/changes/1-inbox/summary-beta (origin github #41; 2 files)
- [x] an `issue:` line https://github.com/o/r/issues/41 gives the origin github #41
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-beta --title Beta --summary Beta.  → exit 0
      summary set .agents/changes/1-inbox/summary-beta (origin gitlab #12; 2 files)
- [x] an `issue:` line https://gitlab.com/o/r/-/issues/12 gives the origin gitlab #12
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-beta --title Beta --summary Beta.  → exit 0
      summary set .agents/changes/1-inbox/summary-beta (origin jira CHT-118; 2 files)
- [x] an `issue:` line https://example.atlassian.net/browse/CHT-118 gives the origin jira CHT-118
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-beta --title Beta --summary Beta.  → exit 1
      stderr: error: the issue: line's tracker is not known from its URL: add --tracker github|gitlab|jira
- [x] an unplaced URL is refused (exit 1), and summary.json is not touched
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-beta --title Beta --summary Beta. --tracker gitlab  → exit 0
      summary set .agents/changes/1-inbox/summary-beta (origin gitlab #7; 2 files)
- [x] `--tracker gitlab` places it: gitlab #7
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha --unchanged --tracker gitlab  → exit 1
      stderr: error: --tracker needs an `issue:` line: write the line in the CR's intent first
- [x] `--tracker` with no `issue:` line is refused (exit 1), nothing written
    $ chantier summary label C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-beta --add Board,cli  → exit 0
      labels .agents/changes/1-inbox/summary-alpha: board, cli
      labels .agents/changes/1-inbox/summary-beta: board, cli
- [x] `label --add Board,cli` lowercases and stores both labels on both CRs
    $ chantier summary label C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-beta --remove cli  → exit 0
      labels .agents/changes/1-inbox/summary-alpha: board
      labels .agents/changes/1-inbox/summary-beta: board
- [x] `label --remove cli` leaves `board`
    $ chantier summary label C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-beta --add no way  → exit 1
      stderr: error: a label is lowercase letters, digits and hyphens, 24 characters at most, starting with a letter or digit: no way
- [x] a label with a space is refused (exit 1), nothing written
    $ chantier summary group C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-beta --name board v1  → exit 0
      group .agents/changes/1-inbox/summary-alpha: board v1
      group .agents/changes/1-inbox/summary-beta: board v1
- [x] `group --name` puts both CRs in the group
    $ chantier summary group C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-beta --clear  → exit 0
      group .agents/changes/1-inbox/summary-beta: none
- [x] `group --clear` takes one out of its group, and labels and groups leave `sources` alone
    $ chantier file Summary delta  → exit 0
      filed .agents/changes/1-inbox/summary-delta; write the intent and grill the CR here
    $ chantier summary label C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-delta --add board  → exit 0
      labels .agents/changes/1-inbox/summary-delta: board
    $ chantier summary lint C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-delta  → exit 2
      1 gap(s) in 1 CRs
      .agents/changes/1-inbox/summary-delta: no summary → summary set .agents/changes/1-inbox/summary-delta --title "<title>" --summary "<the CR's state now>"
- [x] a label on an item with no summary creates the file, and `lint` still says no summary
    $ chantier file Summary dropped  → exit 0
      filed .agents/changes/1-inbox/summary-dropped; write the intent and grill the CR here
    $ chantier abandon C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-dropped  → exit 0
      abandoned .agents/changes/6-trash/261116-2200-summary-dropped
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha --summary one
two  → exit 1
      stderr: error: summary is one line of plain text: no newline or other control character
- [x] a newline in the summary is refused (exit 1), nothing written
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha --summary xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  → exit 1
      stderr: error: summary is 301 characters: the limit is 300
- [x] a summary of 301 characters is refused (exit 1), nothing written
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\6-trash\261116-2200-summary-dropped --title T --summary S  → exit 1
      stderr: error: a dropped CR keeps its summary as it is: restore it first
- [x] a folder of 6-trash is refused (exit 1), nothing written
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\STATUS.md --title T --summary S  → exit 1
      stderr: error: not a CR folder: .agents/changes/STATUS.md
- [x] a path that is not a CR folder is refused (exit 1), nothing written
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-delta --unchanged  → exit 1
      stderr: error: --title is required: this CR has no title yet
- [x] `--unchanged` on a new item is refused (exit 1), nothing written
    $ chantier summary lint C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha  → exit 2
      1 gap(s) in 1 CRs
      .agents/changes/1-inbox/summary-alpha: summary.json unreadable (Invalid JSON: key must be a string at line 1 column 2) → repair or remove it, then summary set .agents/changes/1-inbox/summary-alpha …
- [x] `lint` names an unreadable summary.json
    $ chantier summary set C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha --title T --summary S  → exit 2
      stderr: error: summary.json unreadable (Invalid JSON: key must be a string at line 1 column 2); repair or remove it
- [x] `set` on it exits 2 and leaves it as it was
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\1-inbox\summary-alpha --priority P2  → exit 0
      triaged .agents/changes/2-backlog/P2/summary-alpha (P2)
- [x] `triage --priority P2` keeps summary.json with the folder
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\2-backlog\P2\summary-alpha --ready  → exit 0
      triaged .agents/changes/3-ready/summary-alpha
- [x] `triage --ready` keeps it too
    $ chantier summary lint  → exit 2
      1 gap(s) in 3 CRs
      .agents/changes/1-inbox/summary-delta: no summary → summary set .agents/changes/1-inbox/summary-delta --title "<title>" --summary "<the CR's state now>"
- [x] an archived CR is not walked by default
    $ chantier summary lint C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\5-archives\261101-1200-901-old-cr  → exit 2
      1 gap(s) in 1 CRs
      .agents/changes/5-archives/261101-1200-901-old-cr: no summary → summary set .agents/changes/5-archives/261101-1200-901-old-cr --title "<title>" --summary "<the CR's state now>"
- [x] but is checked when named
    $ chantier open C:\Users\gaeta\AppData\Local\Temp\cs-surface-board-vuake9hp\summary\proj\.agents\changes\3-ready\summary-alpha --direct --slots 1 --default-branch main  → exit 0
      opened batch-01 on claude: 1 CRs, 1 slots, parallel, steering direct
      next: complete the brief .agents/changes/4-batch/brief.md, then steer it yourself
      CR-101 Summary alpha: 3-ready/summary-alpha -> 4-batch/1-pending/101-summary-alpha
- [x] `open` keeps summary.json with the folder
    $ chantier file Summary spare  → exit 0
      filed .agents/changes/1-inbox/summary-spare; write the intent and grill the CR here
    $ chantier triage 1-inbox/summary-spare --priority P3  → exit 0
      triaged .agents/changes/2-backlog/P3/summary-spare (P3)
    $ chantier triage 1-inbox/summary-spare --priority P3  → exit 0
      triaged .agents/changes/2-backlog/P3/summary-spare (P3)
- [x] the STATUS files (index, batch, CR) are byte-identical with and without summary.json
    $ chantier file Summary many 0  → exit 0
      filed .agents/changes/1-inbox/summary-many-0; write the intent and grill the CR here
    $ chantier file Summary many 1  → exit 0
      filed .agents/changes/1-inbox/summary-many-1; write the intent and grill the CR here
    $ chantier file Summary many 2  → exit 0
      filed .agents/changes/1-inbox/summary-many-2; write the intent and grill the CR here
    $ chantier file Summary many 3  → exit 0
      filed .agents/changes/1-inbox/summary-many-3; write the intent and grill the CR here
    $ chantier file Summary many 4  → exit 0
      filed .agents/changes/1-inbox/summary-many-4; write the intent and grill the CR here
    $ chantier file Summary many 5  → exit 0
      filed .agents/changes/1-inbox/summary-many-5; write the intent and grill the CR here
    $ chantier file Summary many 6  → exit 0
      filed .agents/changes/1-inbox/summary-many-6; write the intent and grill the CR here
    $ chantier file Summary many 7  → exit 0
      filed .agents/changes/1-inbox/summary-many-7; write the intent and grill the CR here
    $ chantier file Summary many 8  → exit 0
      filed .agents/changes/1-inbox/summary-many-8; write the intent and grill the CR here
    $ chantier file Summary many 9  → exit 0
      filed .agents/changes/1-inbox/summary-many-9; write the intent and grill the CR here
    $ chantier file Summary many 10  → exit 0
      filed .agents/changes/1-inbox/summary-many-10; write the intent and grill the CR here
    $ chantier summary lint  → exit 2
      13 gap(s) in 15 CRs
      .agents/changes/1-inbox/summary-delta: no summary → summary set .agents/changes/1-inbox/summary-delta --title "<title>" --summary "<the CR's state now>"
      .agents/changes/1-inbox/summary-many-0: no summary → summary set .agents/changes/1-inbox/summary-many-0 --title "<title>" --summary "<the CR's state now>"
      .agents/changes/1-inbox/summary-many-1: no summary → summary set .agents/changes/1-inbox/summary-many-1 --title "<title>" --summary "<the CR's state now>"
      .agents/changes/1-inbox/summary-many-10: no summary → summary set .agents/changes/1-inbox/summary-many-10 --title "<title>" --summary "<the CR's state now>"
      .agents/changes/1-inbox/summary-many-2: no summary → summary set .agents/changes/1-inbox/summary-many-2 --title "<title>" --summary "<the CR's state now>"
      .agents/changes/1-inbox/summary-many-3: no summary → summary set .agents/changes/1-inbox/summary-many-3 --title "<title>" --summary "<the CR's state now>"
      .agents/changes/1-inbox/summary-many-4: no summary → summary set .agents/changes/1-inbox/summary-many-4 --title "<title>" --summary "<the CR's state now>"
      .agents/changes/1-inbox/summary-many-5: no summary → summary set .agents/changes/1-inbox/summary-many-5 --title "<title>" --summary "<the CR's state now>"
      … 5 more lines
- [x] more than ten gaps: the count is the first line and the output ends with `… N more lines`
- [x] chantier wrote nothing outside the planning folder (`git status` shows only .agents/changes/)

## Timing

| case or section | seconds | commands |
| --- | ---: | ---: |
| build | 0.7 | 8 |
| remote_board | 56.8 | 66 |
| external_surface | 71.7 | 120 |
| cr_summary | 23.8 | 63 |
| total of the rows | 153.0 | 257 |
| whole unit | 153.2 | 259 |

