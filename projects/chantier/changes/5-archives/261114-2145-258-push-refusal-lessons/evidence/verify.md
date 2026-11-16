# Verify CR-258

Head: 4254a298ca4da124db476cdaa200b6a0ffcb75df

Verdict: VERIFIED

All claims judged at 4254a29, in the worktree C:\Users\gaeta\Projets\chantier.worktrees\batch-18-CR-258
(`git rev-parse HEAD` printed 4254a298ca4da124db476cdaa200b6a0ffcb75df). Not rerun: just check, just scenario, CI (passed at this head per the brief).

## Claim 1: driver.md records the refusal exactly (Area 1)

Command: `git grep -n -e "the exact command" -e "host's exact text" -e "next after push" -e "waits: push" -- skills/chantier/references/driver.md`
Output:
- driver.md:333: `1. Record the refusal first, in one note: $CHANTIER note <cr> "refused: <the exact command> ->`
- driver.md:334: `<the host's exact text>"`: the command as it ran (its git -C <path> form included, flags`
- driver.md:336: `such as "Git Destructive", when the host gives one). Never a summary such as "refused by`
Met.

## Claim 2: driver.md hands back instead of waiting (Area 2)

Same grep, output:
- driver.md:338: `2. Then one note with what is next: $CHANTIER note <cr> "next after push: <the steps left, in`
- driver.md:342: `3. $CHANTIER handback <cr> blocked waits: push <branch> <expected remote sha> <local sha>`
- driver.md:344-346: `4. Send [driver <cr>->foreman] push <branch> <expected remote sha> <local sha>, and end: no other push, no other way, and no wait in your turn. The CR waits, not you; the steering session restarts a fresh Driver on it when the Chief of Staff's answer comes back.`
- driver.md:348-355: the four answers read from the `take` note: `pushed <branch>` ship; `push failed` look at why, never the same push; `push refused <branch>: no long gate passed at <sha>` run the long gate, send the push line again, hand back `waits:` again; any other `push refused` -> `handback blocked refused <exact text>`.
Met.

## Claim 3: no Driver waits for a push, stack driver excepted

Command: `git grep -n -e "keep waiting" -e "then wait" -e "keeps waiting" -e "hears the" -e "note push" -e "push result" -- skills/chantier/references/`
Relevant output:
- driver.md:356-357: `The stack driver, which restacks several branches in one take, sends the push line and waits for the result as a note, no other push, no other way.` (named exception)
- foreman.md:385-386: `The stack driver, which waits for the push result, still gets [foreman->driver stack] note push <branch>: <the answer>.` (named exception)
- chief-of-staff.md:1046: `The CR keeps waiting (its Driver has handed back).`
- no "keep waiting"/"then wait" hit on a CR Driver; no "hears the" hit about a push.
Met.

## Claim 4: foreman.md restarts the CR on each answer (Area 3)

Command: `git grep -n -e "take <cr> --note" -e "waits: push" -- skills/chantier/references/foreman.md` and read of foreman.md lines 367-390.
Output:
- foreman.md:375-380: `The answer does not go to a live Driver as a note: the Driver handed back blocked waits: push <branch> ... and ended. When the CR is blocked with that waits:, take it back at once with the restart path's steps (the id cleared first: agents set <cr> - --epoch <n>) and take <cr> --note "push: <the Chief of Staff's answer, as it came>", then a new CR Driver (or Release driver), before any queued CR ... No round is counted.`
- foreman.md:381-383: `An answer that comes before the hand-back has landed (the CR still working): wait for the hand-back, then take it back as above. A Driver that ended without its hand-back takes the lost-Driver path, with the answer in its resume: note.`
- foreman.md:384-385: `A Driver of a CR handed back waits: push is never pinged, and the CR is not a lost Driver (it is blocked, not working).`
- foreman.md:387-390: each refusal recorded once, whoever sees it.
Met.

## Claim 5: routing.md, chief-of-staff.md, status-layout.md, hosts/claude-code.md (Areas 1 to 4)

Command: `git grep -n -e "fresh Driver" -e "keeps waiting" -e "refused <exact" -e "note <text>" -e "no refusal recorded" -e "before it sends the push line" -- skills/chantier/references/routing.md chief-of-staff.md status-layout.md hosts/claude-code.md`
Output:
- routing.md:12: `... push refused <branch>: <reason or git's exact text> (the CR's fresh Driver then hands back blocked refused <exact text>) ...`
- routing.md:15: `| Foreman -> Driver | note <text>, fix <fix-cr>, ping, stop |` (no "(the push result too)")
- chief-of-staff.md:1046: `The CR keeps waiting (its Driver has handed back).`
- chief-of-staff.md:1281: `the CR goes back to a fresh Driver with the result as its take note (push: <the result>, as foreman.md says)`
- status-layout.md:91: `"pushed for the Driver (host refused: <the exact command> -> <the host's exact text>)", quoting the Driver's recorded refused: note as handoff <cr> prints it, or "pushed for the Driver (no refusal recorded)" when the Driver left none.`
- hosts/claude-code.md:332-334: `the Driver records the refused command and text before it sends the push line (driver.md), so a refusal on a command an allow rule matches is told apart from one with no rule.`
No card says the Driver hears the push result as a live note (Claim 3 grep). Met.

## Claim 6: CLI proof in a scratch project (not batch-18)

Scratch project: C:\Users\gaeta\AppData\Local\Temp\v258 (`chantier init`, one filed CR with a stub spec, `open` -> batch-01, CR-101; `take CR-101` exit 0).
Commands and output:
- `chantier handback CR-101 blocked waits: push chantier/b/cr-1-x aaaaaaa bbbbbbb --batch batch-01`
  printed `[driver CR-101->foreman] hand-back blocked waits: push chantier/b/cr-1-x aaaaaaa bbbbbbb` and `CR-101 waits; the Foreman takes it back when that lands`; exit 0.
- `chantier status --batch batch-01` printed `CR-101 blocked r0/3 - | blocked: waits: push chantier/b/cr-1-x aaaaaaa bbbbbbb | -`.
- `chantier take CR-101 --note "push: pushed chantier/b/cr-1-x" --batch batch-01`: exit 0; status `CR-101 working r0/3 - | no Driver recorded | -`; `handoff CR-101` printed `rounds: 0 of 3` and the note `back to a Driver: push: pushed chantier/b/cr-1-x`. No round counted.
Met.

## Observation

evals/SCORECARD.md and evals/real-direct/RUNBOOK.md each changed one line, not named in the spec (not a failed claim).

## Description pass at 4254a29 (PR 204)

Commands: `gh pr view 204 --json body,headRefOid` (head 4254a298ca4da124db476cdaa200b6a0ffcb75df); `git diff origin/main...HEAD --stat` (8 files: driver, foreman, routing, chief-of-staff, status-layout, hosts/claude-code, evals/SCORECARD.md, evals/real-direct/RUNBOOK.md); `git diff ... -- driver.md | Select-String "elease|stack"`; same for foreman.md and evals.
- Template order and fold: Summary, Deliverables, Blast radius (Grade 1), Autonomous decisions, Known gaps outside; Details with Changes, Human decisions, Impacts, Test plan, Internal references; nothing after details. Met (no issue: line, no Issues References).
- Deliverables: sequence diagram, real names (handback, take --note, waits: push) match diff and Claim 6 CLI proof. Met.
- Changes vs diff: all six card files named are in the diff; Release driver and stack-driver exclusion appear in driver.md diff; "before any queued CR", "never pinged" appear in foreman.md diff. Autonomous decision (SCORECARD J11, RUNBOOK) matches the evals diff. Met.
- Internal references only in last section; roles appear as product terms of cards changed. Met.
- Test plan SHAs all 4254a29; claims match earlier VERIFIED at this head. Met.
Result: description passes; earlier VERIFIED stands, no new verdict.
