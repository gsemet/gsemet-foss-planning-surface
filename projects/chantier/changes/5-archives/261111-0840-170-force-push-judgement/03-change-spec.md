# Change Specification: the Chief of Staff judges a refused force push and runs it

## Goal

When the host refuses a Driver's `git push --force-with-lease`, the steering session (the Chief
of Staff, in Foreman mode and in direct mode) judges whether the push is legitimate and, when it
is, runs it **without asking the user**. It asks the user only when it judges the push not
right, or when it cannot push (the host refuses its own push too, or the lease fails). The rule
lives in the cards, so every user gets it: no per-session agreement, no memory.

In the user's words (2026-11-11): "Je veux que tu sois capables de juger si c'est légitime ou
pas et que tu pousses automatiquement si tu le peux et tu me demandes uniquement quand tu penses
que c'est pas bon ou que tu n'y arrives pas", and "Encode cette règle dans Chantier pour que ça
n'arrive pas".

Why it happens: Claude Code's auto-mode classifier blocks destructive git in subagents ("Git
Destructive"); the steering session's own push is not refused the same way (proved 2026-11-11 in
batch-09: the Chief of Staff's `git -C <worktree> push --force-with-lease=...` went through). In
batch-09 the Chief of Staff asked the user although its card already made the push its own:
the card must say plainly that the push is not a question for the user.

## Decisions carried (from `02-answers.md`)

| # | Decision | Where |
| --- | --- | --- |
| D1 | The steering session (direct mode: the Chief of Staff; Foreman mode: the Chief of Staff, who receives the push line from the Foreman) judges a Driver's refused force push and runs it without asking the user | Area 1, Area 2 |
| D2 | It asks the user only when it judges the push not legitimate, or when it cannot push (the host refuses it too, or the lease fails) | Area 1 |
| D3 | The refusal's cause: the classifier blocks destructive git in subagents; the steering session's own push went through (2026-11-11, batch-09) | Area 4 |
| D4 | The rule goes in the cards; no per-session agreement, no memory | all areas |
| D5 | The Chief of Staff's card says plainly that the push is not a question for the user | Area 1 |
| D6 (default) | Legitimacy is judged, not a fixed list. The card names what the judgement looks at: the branch is the CR's own and never the default branch (today's check), the local head contains the remote head's work rebased onto the default branch (the CR's base), the gate passed at the local head | Area 1 |
| D7 (default) | What the user hears: a pushed branch is reported in the next report, not asked | Area 1, Area 5 |

## What changes

Cards only. No CLI change, no agent file change (the agent files carry no part of this
contract), no new message in `routing.md` (the existing `pushed`, `push failed` and
`push refused` answers cover every outcome).

### Area 1: `skills/chantier/references/chief-of-staff.md`, "A refused force push" (line ~319)

Rewrite the bullet so it holds, in this order:

1. **Not a question.** On `[foreman→chief-of-staff] push <branch> <expected remote sha> <local
   sha>` (in direct mode: the Driver's `push` line, which reaches you), the push is yours, the one
   exception to "do no Driver's work". It is **not a question for the user**: you judge it and run
   it, with no ask and no wait for a word.
2. **The branch check (unchanged, a hard refusal).** The branch is `chantier/<batch>/<cr>-<slug>`:
   read the CR from its name (`cr-115` is `CR-115`), run `$CHANTIER handoff <cr>`; its `worktree:
   … branch <branch>` line must give exactly the branch on the line, and never the default branch.
   Else push nothing and answer `push refused <branch>: not a branch of this batch` (the Driver
   hands it back blocked; the user hears it through that hand-back, as today).
3. **The judgement.** Then judge whether the push is legitimate, on what you can read (read-only,
   from the main checkout or with `git -C <worktree>`; `git fetch <remote>` first). What it looks
   at, not a fixed list:
   - the local sha is the worktree's committed head (`git -C <worktree> rev-parse HEAD`, a clean
     `git status`);
   - the local head holds the remote head's work, rebased onto the CR's base (the `base` that
     `handoff` prints: the default branch, or another CR's branch in a series or a stack): the base
     is an ancestor of the local head, and the remote head's commits are in it (`git range-diff
     <base>...<expected>` against `<base>..<local>`, or `git cherry`); a patch changed by a
     resolved conflict is not by itself a doubt (the Driver's card has it inspected);
   - the long gate passed at the local head: a `gate` event with `result` `pass` and `head` the
     local short sha in the batch's `events.jsonl`, or the Driver's notes and last gate log in
     `handoff`; the stack driver's restack is judged by its own card (heavy CI once at the top).
   A push that would drop work the remote has and the local head does not, or that you cannot tie
   to the CR, is not legitimate.
4. **Legitimate: push.** From the main checkout, without changing its branch or touching its files:
   `git push --force-with-lease=<branch>:<expected> <remote> <local sha>:refs/heads/<branch>`
   (unchanged command). Done: answer `pushed <branch>`. **What the user hears:** nothing at the
   time; your next report has one line saying the branch you pushed for which CR and why it was
   yours (the host refused the Driver's push), as `status-layout.md` says (Area 5).
5. **Not legitimate: ask the user.** Push nothing; tell the user at once, in the report's shape
   (the question is the **For you:** line, and the report carries no tip): the CR (number and
   slug), the branch, the expected remote sha and the local sha, and what your judgement found
   (for instance: "the remote has 2 commits the local head does not hold"). The Driver keeps
   waiting. On the user's go, push as in 4; on their no, answer `push refused <branch>: <the
   user's reason>` (the Driver hands back blocked).
6. **The lease fails: tell the user.** It is not retried (the remote moved; the Driver looks at
   why): answer `push failed <branch> <git's text>` as today, and tell the user at once, with git's
   text and what it means (the remote branch moved since the Driver read it).
7. **The host refuses your own push: ask the user.** Unchanged: show the user the exact text, as
   for any `refused`, and answer `push refused <branch>: <exact text>`; retry nothing, try no other
   way, never change the permission settings. Add: the message names the CR, the branch and the
   exact push command, so the user can run it themselves or allow it.

All answers go to the Foreman (`[chief-of-staff→foreman]`), never to the Driver (Foreman mode);
in direct mode the Driver hears them as a note (Area 2).

### Area 2: `chief-of-staff.md`, direct mode (line ~457)

The sentence "A Driver's refused force push is run by you, as above; the Driver hears the result
as a note." becomes: a Driver's refused force push is judged and run by you, as above, without
asking the user; the Driver hears the result as a note (`order note` or the host's message, as
your other notes to it), `pushed <branch>`, `push failed <branch> <text>` or `push refused
<branch>: <text>`.

The "never" list (line ~604, "but the refused force push above") stays as it is.

### Area 3: `skills/chantier/references/driver.md` (line ~93) and `foreman.md` (line ~116)

- `driver.md`: "the Chief of Staff runs it for you" becomes "the Chief of Staff judges it and runs
  it for you, without the user's word in the normal case". Add: while the steering session asks
  the user (a push it judges not right), you keep waiting, as for any push. The rest is unchanged
  (the line to send, a failed lease, `push refused` ends with `handback blocked refused <exact
  text>`). The Push lines at ~138 and ~174 ("a refused one goes up as written above") need no
  change.
- `foreman.md`: the sentence "A push the host refuses the Chief of Staff too is the user's, shown
  by it" gets: the Chief of Staff judges the push and may ask the user first; you wait for its
  answer and pass nothing else meanwhile. No new message.

### Area 4: `skills/chantier/references/hosts/claude-code.md`, Auto mode (line ~200)

The line "A refused force push takes the route already written (`driver.md`, `foreman.md`:
Driver → Foreman → Chief of Staff)" gets the cause and the proof: the classifier blocks
destructive git in subagents ("Git Destructive"); the steering session's own `git -C <worktree>
push --force-with-lease=...` went through (**proved by use**, 2026-11-11, batch-09); so the route
ends in the steering session, which judges and runs the push without asking the user
(`chief-of-staff.md`). The permission rules table (lines ~109-110) and the JSON block are
unchanged: they stay the user's choice to spare the route, and the CLI's list they mirror does not
change.

`hosts/copilot.md` says nothing of a force push today; it gets nothing (the rule is
host-neutral, in `chief-of-staff.md`).

### Area 5: `skills/chantier/references/status-layout.md`, Progress (line ~51)

Next to the chain line, add: when you ran a Driver's refused force push since the last report,
your next report has one line with the CR (number and slug), the branch and "pushed for the
Driver (host refused its push)". A push held for the user's word or failed was already told at
once (Area 1); the report's **For you:** line still names a push question while it is open.

## Out of scope

- Any CLI change: no new command or `handoff` line for the gate's head (the gate event is in
  `events.jsonl`; a CLI tool comes only from measured token cost).
- The permission rules recommended in `hosts/claude-code.md` and the CLI's list
  (`commands.py`, `git push --force-with-lease*` entries): unchanged.
- Who pushes in the normal case: a Driver still pushes its own branch; only a refused force push
  goes up.
- The branch check's strictness: a branch that is not this batch's stays refused, never pushed on
  any word.
- Plain pushes, the release's push, and deleting branches ("What stays refused").

## Evidence

- `just check` passes (Linux, macOS, Windows; `tests/test_structure.py` holds no push text).
- Read-through proofs, by the Verifier, at the PR's head with `git grep -n` on the cards:
  - `chief-of-staff.md` "A refused force push" holds: "not a question for the user", the
    unchanged branch check and command, the judgement's three points (committed head; remote
    work rebased onto the base `handoff` prints; gate passed at the local head), and the three
    cases where the user is asked or told (judged not legitimate, failed lease, own push refused),
    each with what the user hears.
  - The direct-mode line says "without asking the user".
  - `driver.md`, `foreman.md`, `hosts/claude-code.md` and `status-layout.md` carry Area 3, 4 and 5,
    and no other card contradicts them (`git grep -n -i "force push"` over
    `skills/chantier/references/`).
- Scenario: no impact. `just scenario` does not run the refused-push route (the scenario's
  Driver pushes itself, `scenario/run_scenario.py` line ~412) and the change is agent behaviour in
  the cards; the PR runs `just scenario` anyway, as AGENTS.md asks of a change to the cards.

## Open questions

1. **A missing gate pass: ask the user, or send it back to the Driver?** The Driver's card makes
   the long gate pass before any push, so a head with no gate pass is the Driver's slip, not a
   doubt about the push. Recommended: answer `push refused <branch>: no long gate passed at <local
   sha>` to the Driver (it runs the gate and sends the line again), and ask the user only for the
   other doubts (lost work, a head not tied to the CR).
2. **A failed lease: tell the user, or wait for their word?** The user said "ask me when you
   cannot"; today the Driver looks at why on its own. Recommended: tell the user at once and let
   the Driver go on as today (no wait); the user's word is needed only if the Driver then hands
   back blocked.
3. **The host refuses your own push: offer the user the command to run themselves?**
   Recommended: yes, the exact push command in the message, so the user can run it in their own
   terminal or allow it; the Driver still hands back blocked, and the CR goes back to a Driver
   once the user says it is pushed.
