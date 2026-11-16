
## A. batch made by `open --release` (first, second, release v1.5.0)

### A1 open with --release 3, status
    $ chantier file First change  → exit 0
      filed .agents/changes/1-inbox/first-change; write the intent and grill the CR here
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\1-inbox\first-change --priority P1  → exit 0
      triaged .agents/changes/2-backlog/P1/first-change (P1)
    $ chantier file Second change  → exit 0
      filed .agents/changes/1-inbox/second-change; write the intent and grill the CR here
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\1-inbox\second-change --priority P1  → exit 0
      triaged .agents/changes/2-backlog/P1/second-change (P1)
    $ chantier file Release v1.5.0  → exit 0
      filed .agents/changes/1-inbox/release-v1-5-0; write the intent and grill the CR here
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\1-inbox\release-v1-5-0 --priority P1  → exit 0
      triaged .agents/changes/2-backlog/P1/release-v1-5-0 (P1)
    $ chantier open C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\2-backlog\P1\first-change C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\2-backlog\P1\second-change C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\2-backlog\P1\release-v1-5-0 --release 3 --slots 1 --default-branch main  → exit 0
      opened batch-01 on claude: 3 CRs, 1 slots, stack
      next: complete the brief .agents/changes/3-requests/batch-01/brief.md, then start the Foreman
      CR-101 First change: 2-backlog/P1/first-change -> 3-requests/batch-01/101-first-change
      CR-102 Second change: 2-backlog/P1/second-change -> 3-requests/batch-01/102-second-change
      CR-103 Release v1.5.0: 2-backlog/P1/release-v1-5-0 -> 3-requests/batch-01/103-release-v1-5-0
    $ chantier foreman set local_foreman6 --epoch 1  → exit 0
      foreman local_foreman6 epoch 1
    $ chantier status  → exit 0
      batch-01 open stack live 0/1 queued 3 foreman local_foreman6 e1 heartbeat never spent $0.00
      CR-101 queued r0/3 - | -
      CR-102 queued r0/3 - | -
      CR-103 queued r0/3 - release | -

### A2 first starts, goes ready; status; take release
    $ chantier take CR-101 --epoch 1  → exit 0
      took CR-101 (1 of 1 slots held)
      CR-101 "First change" (change) working in batch batch-01 (stack)
      cli: uv run --script "C:/Users/gaeta/AppData/Local/Temp/chantier-before-c4aac8e/skills/chantier/scripts/cli/chantier.py" <command> --batch batch-01
      cards: C:/Users/gaeta/AppData/Local/Temp/chantier-before-c4aac8e/skills/chantier/references/ (driver.md, worker.md, concepts.md); the project's rules rank above them: `rules`
      project instructions: C:/Users/gaeta/AppData/Local/Temp/verif137-oy_x26zb/proj/AGENTS.md
      specification: C:/Users/gaeta/AppData/Local/Temp/verif137-oy_x26zb/proj/.agents/changes/3-requests/batch-01/101-first-change/03-change-spec.md
      folder: C:/Users/gaeta/AppData/Local/Temp/verif137-oy_x26zb/proj/.agents/changes/3-requests/batch-01/101-first-change (work/, evidence/)
      worktree: C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj.worktrees\batch-01-CR-101 branch chantier/batch-01/cr-101-first-change base origin/main; not created yet: a Driver creates it first
      PR: none; head -
      rounds: 0 of 3
      notes: none
    $ chantier agents set CR-101 agent-1 --epoch 1  → exit 0
      CR-101 → agent-1
    (foreman take CR-101 -> exit 0)
    $ chantier round CR-101 --note edit first.py  → exit 0
      round 1 of 3 for CR-101
      CR-101 "First change" (change) working in batch batch-01 (stack)
      cli: uv run --script "C:/Users/gaeta/AppData/Local/Temp/chantier-before-c4aac8e/skills/chantier/scripts/cli/chantier.py" <command> --batch batch-01
      cards: C:/Users/gaeta/AppData/Local/Temp/chantier-before-c4aac8e/skills/chantier/references/ (driver.md, worker.md, concepts.md); the project's rules rank above them: `rules`
      project instructions: C:/Users/gaeta/AppData/Local/Temp/verif137-oy_x26zb/proj/AGENTS.md
      specification: C:/Users/gaeta/AppData/Local/Temp/verif137-oy_x26zb/proj/.agents/changes/3-requests/batch-01/101-first-change/03-change-spec.md
      folder: C:/Users/gaeta/AppData/Local/Temp/verif137-oy_x26zb/proj/.agents/changes/3-requests/batch-01/101-first-change (work/, evidence/)
      worktree: C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj.worktrees\batch-01-CR-101 branch chantier/batch-01/cr-101-first-change base origin/main
      PR: none; head -
      rounds: 1 of 3
      notes: none
    $ chantier gate CR-101 uv run --no-project python -m compileall -q .  → exit 0
      pass uv run --no-project python -m compileall -q . at a95b381; log C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\3-requests\batch-01\101-first-change\work\gates\20261106-212512.log
    $ gh pr create --base main…  → exit 0
    $ chantier ship CR-101 https://github.com/acme/demo/pull/40  → exit 0
      recorded https://github.com/acme/demo/pull/40 (base main, head a95b381)
    $ chantier handback CR-101 ready https://github.com/acme/demo/pull/40  → exit 0
      [driver CR-101→foreman] hand-back ready https://github.com/acme/demo/pull/40
      CR-101 ready
    $ chantier status  → exit 0
      batch-01 open stack live 0/1 queued 2 foreman local_foreman6 e1 heartbeat never spent $0.00
      CR-101 ready r1/3 https://github.com/acme/demo/pull/40 | -
      CR-102 queued r0/3 - | -
      CR-103 queued r0/3 - release | -
    $ chantier take CR-103 --epoch 1  → exit 2
      stderr: error: CR-103 releases what is merged: it starts once every other CR is merged or cancelled

### A3 first merged, second dropped: take release with the others ended
    $ chantier order merged CR-101  → exit 0
      [chief-of-staff→foreman] order O-1: merged CR-101
      merged CR-101: archived to .agents/changes/4-archives/261106-2025-101-first-change
    $ chantier order drop CR-102  → exit 0
      [chief-of-staff→foreman] order O-2: drop CR-102
      dropped CR-102: .agents/changes/5-trash/261106-2025-102-second-change
    $ chantier status  → exit 0
      batch-01 open stack live 0/1 queued 1 foreman local_foreman6 e1 heartbeat never spent $0.00
      CR-101 merged r1/3 https://github.com/acme/demo/pull/40 | -
      CR-102 cancelled r0/3 - | -
      CR-103 queued r0/3 - release | -
      orders the CLI applied, the Foreman marks each `order done <O-k>`: O-1 merged CR-101; O-2 drop CR-102
    $ chantier take CR-103 --epoch 1  → exit 0
      took CR-103 (1 of 1 slots held)
      CR-103 "Release v1.5.0" (release) working in batch batch-01 (stack)
      cli: uv run --script "C:/Users/gaeta/AppData/Local/Temp/chantier-before-c4aac8e/skills/chantier/scripts/cli/chantier.py" <command> --batch batch-01
      cards: C:/Users/gaeta/AppData/Local/Temp/chantier-before-c4aac8e/skills/chantier/references/ (driver.md, worker.md, concepts.md); the project's rules rank above them: `rules`
      project instructions: C:/Users/gaeta/AppData/Local/Temp/verif137-oy_x26zb/proj/AGENTS.md
      specification: C:/Users/gaeta/AppData/Local/Temp/verif137-oy_x26zb/proj/.agents/changes/3-requests/batch-01/103-release-v1-5-0/03-change-spec.md
      folder: C:/Users/gaeta/AppData/Local/Temp/verif137-oy_x26zb/proj/.agents/changes/3-requests/batch-01/103-release-v1-5-0 (work/, evidence/)
      worktree: C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj.worktrees\batch-01-CR-103 branch chantier/batch-01/cr-103-release-v1-5-0 base origin/main; not created yet: a Driver creates it first
      PR: none; head -
      rounds: 0 of 3
      grant: every irreversible action waits for the user's approval; the user starts and merges the fixes; attempts 0; approvals unused: none
      notes: none
    $ chantier agents set CR-103 agent-2 --epoch 1  → exit 0
      CR-103 → agent-2
    (foreman take CR-103 -> exit 0)

### A4 order add once the release has started
    $ chantier file Late change  → exit 0
      filed .agents/changes/1-inbox/late-change; write the intent and grill the CR here
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\1-inbox\late-change --priority P1  → exit 0
      triaged .agents/changes/2-backlog/P1/late-change (P1)
    $ chantier file Fix one  → exit 0
      filed .agents/changes/1-inbox/fix-one; write the intent and grill the CR here
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\1-inbox\fix-one --priority P1  → exit 0
      triaged .agents/changes/2-backlog/P1/fix-one (P1)
    $ chantier file Fix two  → exit 0
      filed .agents/changes/1-inbox/fix-two; write the intent and grill the CR here
    $ chantier triage C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\1-inbox\fix-two --priority P1  → exit 0
      triaged .agents/changes/2-backlog/P1/fix-two (P1)
    $ chantier order add --note C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\2-backlog\P1\late-change  → exit 0
      [chief-of-staff→foreman] order O-3: add C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\2-backlog\P1\late-change
      added CR-104, queued
    $ chantier order add --note C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\2-backlog\P1\fix-one --fix-for CR-103  → exit 0
      [chief-of-staff→foreman] order O-4: add C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\2-backlog\P1\fix-one
      added CR-105 (fix for CR-103), queued

### A5 release PR merged, back to queued: order add
    $ chantier release start CR-103  → exit 0
      attempt 1: the procedure starts from its first step
    $ chantier order merged CR-103  → exit 0
      [chief-of-staff→foreman] order O-5: merged CR-103
      merged CR-103: the procedure goes on with a new Release driver
    release now: status=queued attempts=1
    $ chantier order add --note C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\2-backlog\P1\late-change  → exit 1
      stderr: error: prepared CR not found: C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\2-backlog\P1\late-change
    $ chantier order add --note C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\2-backlog\P1\fix-two --fix-for CR-103  → exit 0
      [chief-of-staff→foreman] order O-6: add C:\Users\gaeta\AppData\Local\Temp\verif137-oy_x26zb\proj\.agents\changes\2-backlog\P1\fix-two
      added CR-106 (fix for CR-103), queued

### A6 (a) release taken again after its merged PR put it back to queued, no new confirm
    release confirmed=None status=queued
    $ chantier take CR-103 --epoch 1  → exit 2
      stderr: error: CR-103 releases what is merged: it starts once every other CR is merged or cancelled
    (foreman take CR-103 -> exit 2)
