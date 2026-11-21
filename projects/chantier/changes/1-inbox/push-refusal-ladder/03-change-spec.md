# A refused push climbs: Foreman, then Chief of Staff, then the user

Spec v3 (2026-11-21), over v2: carries push-ladder-Q11 (narrows Q10) and Q12, which close v2's two
open questions. v2 carried push-ladder-Q3 to Q10 (Q8 revises Q5, Q10 revises Q4) and the spec
critic's findings 4 to 8. Short name: `push-ladder`. Destination: batch-30, running
(push-ladder-Q2), after CR-438, CR-442 and CR-443 where they overlap textually ("Overlaps in
batch-30").

## Goal

The user's words (2026-11-21): "Tu dois d'abord essayer dans ces cas au lieu de me demander."
When the host refuses a Driver's legitimate force push (on Claude Code, the auto-mode classifier
refusing a subagent's `git push --force-with-lease` on its own `chantier/` branch), the push climbs
a ladder and reaches the user only last:

1. the Foreman judges the push and, when it is legitimate, tries the same push itself;
2. if the host refuses the Foreman (or the Foreman could not try: its route rule is missing), the
   Chief of Staff judges the push again and, when it is legitimate, tries it, without asking the
   user;
3. only if the host refuses the Chief of Staff too, it asks the user one question, and on the
   user's yes pushes once. On Claude Code that yes, given in the conversation, is what tells the
   classifier the push is really wanted.

Each session that pushes judges the push first (the Foreman, then the Chief of Staff again). Each
refusal is recorded with its exact command and the host's exact text, at the step that met it.

In direct mode the steering session is the Chief of Staff: the ladder is Driver, Chief of Staff,
the user, with one judgement (the Chief of Staff's).

## Decisions carried (02-answers.md, the latest winning)

- **push-ladder-Q1, the ladder:** Foreman tries, then the Chief of Staff without asking, then the
  user's yes and one push. Every section below.
- **push-ladder-Q2, the destination:** batch-30.
- **push-ladder-Q3, one place for the check and the judgement:** they move, wording kept, from
  `chief-of-staff.md` into `foreman.md`, in a level-2 section of its own, `## A Driver's refused
  force push` (critic finding 5); `chief-of-staff.md`, `driver.md` and `routing.md` link to it
  and hold no copy (sections 1 to 4).
- **push-ladder-Q4, revised by Q10:** its "no second judgement", its same-sha clause and its
  missing-note fallback are dropped.
- **push-ladder-Q5, revised by Q8:** its "no new rule" is dropped.
- **push-ladder-Q6, a push the Foreman judges not legitimate:** the Foreman pushes nothing and asks
  through `asks`; the Chief of Staff relays it to the user and pushes on the user's go (section 2,
  "Not legitimate"; section 3).
- **push-ladder-Q7, the J22 exemption:** both modes, the route form only, the preflight trial's
  `--dry-run` not counted; narrowed further by critic finding 7 (section 11).
- **push-ladder-Q8, the `git -C` route rule:** one new P10 rule, `git -C * push
  --force-with-lease=chantier/* origin *chantier/*`, its sample, its test and its rows in
  `hosts/claude-code.md` (sections 6 and 8). Why: for a steering session an allow rule resolves a
  matching command before the classifier (documented), and with a planning surface the steering
  push is always `git -C <clone>`.
- **push-ladder-Q9, the Foreman's stopped push:** a refusal of the Foreman's own push goes to the
  Chief of Staff as the `push` line, a named exception to the `refused <cr> <text>` ask and to the
  allow line in the Foreman's chat; the Foreman tries only when `$CHANTIER preflight`'s P10 shows
  the route rule present, and with it missing records `push not tried: route rule missing` and
  sends the `push` line at once (section 2).
- **push-ladder-Q10, who judges:** whoever pushes judges first; on the Foreman's `push` line the
  Chief of Staff runs the full check and judgement again, records its own `push judged legitimate`
  note, then pushes; one it judges not legitimate is not pushed and goes to the user naming both
  judgements (section 3). `01-intent.md`'s done line now says it. Narrowed by Q11.
- **push-ladder-Q11, the Chief of Staff's failed hard check:** the two checks (the branch is this
  batch's; a long gate passed at the local head, outside the skips) are facts, not judgements: when
  either fails at the Chief of Staff, it pushes nothing, records a note, and answers `push refused
  <branch>: <reason>` to the Foreman as today, with no user question; only a push it judges not
  legitimate goes to the user, naming both judgements (section 3).
- **push-ladder-Q12, the Foreman on Copilot:** P10 does not run there and no allow rule is recorded
  for Copilot, so the Foreman skips the route-rule read and tries, as a Driver already does there;
  whether Copilot stops the Foreman's unwatched session on a prompt instead of refusing is unproved,
  and the first Copilot batch that meets a refused push records it (sections 2 and 7).

The route command (from Q8 and the cards as they stand): every steering-side push of a Driver's
refused force push (the Foreman's, the Chief of Staff's, both modes) is

```
git push --force-with-lease=<branch>:<expected> <remote> <local sha>:refs/heads/<branch>
```

run from the main checkout, without changing its branch or touching its files, or as
`git -C <checkout> push --force-with-lease=<branch>:<expected> <remote> <local sha>:refs/heads/<branch>`
when the session's own directory is not that checkout (always with a planning surface: the
project's clone that `take` names). One command per branch, never a loop or a script, even for a
whole restack. Below, "the route form" means these two.

## What changes

### 1. `skills/chantier/references/driver.md`

- **"Means: a force push the host refuses" (~line 389), the opening sentence:** "the Chief of Staff
  judges it and runs it for you" becomes: the push climbs the ladder of [foreman](foreman.md#a-drivers-refused-force-push),
  "A Driver's refused force push" (the steering session judges it and runs it; if the host refuses
  it there, the Chief of Staff judges it again and runs it; if the host refuses the Chief of Staff,
  the user is asked once); "without the user's word in the normal case" kept. In direct mode the
  steering session is the Chief of Staff, so the ladder is Driver, Chief of Staff, the user.
- Steps 1 to 3 unchanged (the `refused:` note with the exact command and the host's whole text,
  the `next after push` note, `handback <cr> blocked waits: push <branch> <expected remote sha>
  <local sha>`).
- Step 4: the push line and the end unchanged; "when the Chief of Staff's answer comes back"
  becomes "when the push's answer comes back (the Foreman's, or the Chief of Staff's)".
- The fresh Driver's reading of its `push:` note (~line 411): `pushed <branch>`, `push failed`,
  `push refused <branch>: no long gate passed at <sha>` unchanged. In that last case's parenthesis
  (~line 416), "the Chief of Staff does not send it" becomes "the steering session does not send
  it" (critic finding 8). "Any other `push refused` (the branch is not this batch's, or the Chief
  of Staff's own push was refused)" becomes "(the branch is not this batch's, the push was judged
  not legitimate and the user said no, or the host refused it at every step, the user's yes
  included)": `handback blocked refused <exact text>` at once, as today.
- The stack driver's sentence: it sends one push line per refused branch and waits for each result
  as a note, as today; the result may now come from the Foreman's own push. No other push, no
  other way.
- The Release driver: covered by the same section, no own text.

### 2. `skills/chantier/references/foreman.md`

**A new level-2 section, `## A Driver's refused force push`**, placed at the end of the card,
after "## Your means" and its closing paragraph ("How you start, message and stop a Driver, …").
It holds, in this order:

1. **Who reads it.** You (the Foreman) on a Driver's `push` line; the Chief of Staff on yours
   (`chief-of-staff.md`, "A refused force push") and, in direct mode, as the steering session. It
   is the one place of the check and the judgement (push-ladder-Q3).
2. **The check and the judgement**, moved verbatim from `chief-of-staff.md`, "A refused force
   push", steps 1 and 2 (links adjusted; "you" for the judge), the gate check and its three skips
   included (the `ci: beside the long gate` line, a branch whose PR the record holds, a pipeline
   job as the long gate). Its refusals: a branch that is not this batch's, or no long gate passed
   at the local head (outside the skips): push nothing; you take the CR back with `take <cr>
   --note "push: push refused <branch>: <the reason>"` by the restart path's steps, as for any
   answer, with no hop to the Chief of Staff (in direct mode the Chief of Staff does the same).
3. **Legitimate: the route rule first** (Claude Code; push-ladder-Q9; on Copilot, where P10 does
   not run, skip this step and go to step 4: push-ladder-Q12). Run `$CHANTIER preflight`
   and read its P10 line for "every batch". The route rule of the form you will run (`git -C *
   push --force-with-lease=chantier/* origin *chantier/*` for the `git -C` form, `git push
   --force-with-lease=chantier/* origin *chantier/*` for the plain form) is present when that line
   is `P10 ok`, or a `P10 warn` that names that rule in no `(add …)` part, the route command in no
   `denied:` part, and no `unreadable:` file. Otherwise it is missing: push nothing, record
   `$CHANTIER note <cr> "push not tried: route rule missing"` and send the `push` line of step 6 at
   once. (P10 names a missing rule readably today, as `<command> (add Bash(<rule>))`, with
   `PowerShell(<rule>)` on Windows: no new CLI output.)
4. **Legitimate, the rule present:** first `$CHANTIER note <cr> "push judged legitimate at <local
   sha7> for <branch>: <one line: what the judgement checked>"`, then the route form, one command
   per branch. Accepted: take the CR back with `push: pushed <branch>` (the stack driver:
   `[foreman→driver stack] note push <branch>: pushed <branch>`) and send
   `[foreman→chief-of-staff] pushed <branch>` (information for the Chief of Staff's report; it
   answers nothing).
5. **Not legitimate** (push-ladder-Q6): push nothing; `$CHANTIER asks "<the CR, number and slug>:
   push <branch> <expected> <local> not legitimate: <what the judgement found>"` (the existing ask
   channel, relayed by the Chief of Staff to the user). The CR keeps waiting; the Chief of Staff
   answers `pushed <branch>` or `push refused <branch>: <the user's reason>` by the existing answer
   lines.
6. **The host refuses your push** (push-ladder-Q9): `$CHANTIER note <cr> "refused: <the exact
   command> -> <the host's exact text>"` first, then send `[foreman→chief-of-staff] push <branch>
   <expected remote sha> <local sha>`, not through `asks`. This is a named exception to the
   `refused <cr> <text>` ask (the asks bullet of "Your means", ~line 582) and to the user's allow
   line in your own chat ("The user's boundaries", ~line 203): you wait for no allow line and ask
   the user nothing; the Chief of Staff takes it "sans demander". That line from you now means:
   judged legitimate, then refused to you or not tried (your notes say which). Retry nothing, try
   no other form, change no permission setting. Wait for the Chief of Staff's answer (`pushed
   <branch>`, `push failed <branch> <text>`, `push refused <branch>: <text>`) and take the CR back
   with it.
7. **A failed lease** (git rejects the lease: the remote moved): never retried, at any step. Take
   the CR back with `push: push failed <branch> <git's text>` (the Driver looks at why) and send
   `[foreman→chief-of-staff] push failed <branch> <git's text>`; the Chief of Staff tells the user
   at once, and nobody waits for a word.
8. **The answer's way back**, moved from today's bullet unchanged: the three sub-bullets (the
   answer never goes to a live Driver as a note, the take-back with `take <cr> --note "push: <the
   answer, as it came>"` before any queued CR; an answer before the hand-back; a Driver of a CR
   handed back `waits: push` never pinged, the stack driver's note).
9. **Record each refusal once, whoever sees it:** the Driver's (before its push line), yours
   (step 6, or the `push not tried` note of step 3), the Chief of Staff's; each before the next
   step's line.

**Today's bullet (~line 738)**, "A Driver's `[driver <cr>→foreman] push …`", is replaced by one
line: "A Driver's `[driver <cr>→foreman] push <branch> <expected remote sha> <local sha>`: [A
Driver's refused force push](#a-drivers-refused-force-push)." Its sentences "you push nothing
yourself", "The Chief of Staff judges the push and may ask the user first" and "A push the host
refuses the Chief of Staff too is the user's, shown by it" go.

**"The user's boundaries", the never-push bullet (~line 205):** "Never code, review, commit,
rebase, push or edit a PR" gains a second named exception beside the PR close: the push of a
Driver's refused force push, by "A Driver's refused force push".

**Your own chat (~line 203):** "the user's line allowing a refused action" adds "(not for your
push of a Driver's refused force push: that goes to the Chief of Staff, 'A Driver's refused force
push')".

**The asks bullet (~line 582):** after `refused <cr> <text>` (record it at once …), one clause:
"but a refusal of your push of a Driver's refused force push, which is the `push` line ('A
Driver's refused force push')".

CR-438 moves the Foreman's stack rules into `foreman-stack.md`; this section is not a stack rule
and stays in `foreman.md`. If CR-438 has landed and moved the stack driver's note sub-bullet, the
matching sentence goes where it now lives, and the new section links there.

### 3. `skills/chantier/references/chief-of-staff.md`

- **"A refused force push" (~line 1364)** becomes the ladder's top, still "not a question for the
  user" in the normal case. Steps 1 and 2 (the check, the judgement) leave for `foreman.md`; the
  section names them as "the check and the judgement of [foreman](foreman.md#a-drivers-refused-force-push),
  'A Driver's refused force push'".
  - **Who checks what (critic finding 8):** in Foreman mode the gate check and its three skips are
    the Foreman's, run inside its judgement; your own judgement on its `push` line runs them again
    (push-ladder-Q10). In direct mode they are yours, once.
  - **On `[foreman→chief-of-staff] push <branch> <expected> <local>`** (the Foreman judged it
    legitimate, then the host refused the Foreman or the Foreman did not try): read in `handoff
    <cr>` the Foreman's `push judged legitimate` note and its `refused:` or `push not tried: route
    rule missing` note; then run the full check and judgement of `foreman.md` yourself, whatever
    the Foreman's note says, at the shas of the line.
    - Legitimate: `$CHANTIER note <cr> "push judged legitimate at <local sha7> for <branch>: <one
      line>"` (your own note), then the route form, at once, no ask.
    - A hard check that fails (not this batch's branch, or no long gate passed at the local head
      outside the skips; push-ladder-Q11): push nothing; record `$CHANTIER note <cr> "push refused
      <branch>: <the reason>"`; answer `push refused <branch>: <the reason>` to the Foreman, as
      today; no user question (the user's yes must not push such a branch, and the Driver already
      knows what to do with each answer).
    - Not legitimate (the checks pass, your judgement disagrees with the Foreman's): push nothing;
      tell the user at once, in the report's shape (the **For you:** line, no tip), naming both
      judgements: the Foreman's (its note) and yours (what you found); the CR (number and slug),
      the branch, the expected and local shas. On the user's go, push in the route form; on their
      no, answer `push refused <branch>: <the user's reason>`.
  - **In direct mode** (the Driver's `push` line): you are the steering session; run the check and
    judgement, record `push judged legitimate at <sha7> for <branch>: …`, then push, no ask (the
    route rule's P10 read of `foreman.md` is not a step for you: you push and, refused, ask).
  - Accepted: answer `pushed <branch>` (in direct mode, the CR's `take` note); the report's line
    (section 5).
  - A failed lease: today's step 5 unchanged (`push failed <branch> <git's text>`, the user told at
    once, never retried).
  - **The host refuses your push:** record it at once with `$CHANTIER note <cr> "refused: <the
    exact command> -> <the host's exact text>"`, then ask the user **one question**, in the
    report's shape (the **For you:** line, no tip), naming: the CR (number and slug), the branch,
    the expected and local shas; both judges, with each one's `push judged legitimate` line (in
    Foreman mode the Foreman and you; in direct mode you); each step's outcome quoted from the
    notes as `handoff <cr>` prints them: the Driver's refusal (exact command, exact text), the
    Foreman's refusal (exact command, exact text) or its `push not tried: route rule missing`
    (refused and not tried told apart), your refusal (exact command, exact text); and the exact
    command you will run on a yes. In direct mode record it with `$CHANTIER asks "<the question>"`
    too, as any ask.
  - **On the user's yes:** run that command once, unchanged. Accepted: `pushed <branch>`. Refused
    again: record it (`refused:` note), show the user the exact text and the command so they can
    run it themselves or allow it, answer `push refused <branch>: <exact text>`; never a second
    try, never another form, never a change to the permission settings. A failed lease: as above.
  - **On the user's no:** answer `push refused <branch>: <the user's reason>`.
  - **The Foreman's ask that a push is not legitimate** (push-ladder-Q6): today's step 4 in
    substance: relay it to the user at once; on the user's go, push in the route form (a host
    refusal then: record it, show the exact text and the command, answer `push refused <branch>:
    <exact text>`, no second try); on a no, `push refused <branch>: <the user's reason>`.
  - "All answers go to the Foreman, never to the Driver": kept.
- **The manifest reading (critic finding 5):** in Foreman mode the Chief of Staff's reading list
  (`startup-manifest.json`, action `chief-of-staff`) does not reach `foreman.md` today (only the
  `batch` action reads it). Section 9 adds the new section to that action, so the link above is a
  reading the manifest lists.
- **Preflight "On the yes" (~line 120):** "a refused one comes to you, and you run it when it is
  legitimate" becomes "a refused one climbs: the Foreman judges and runs it, then you judge and run
  it; the user is asked only when the host refuses you too".
- **Preflight "On a no" (~line 132):** "goes Driver -> Foreman -> Chief of Staff, and an unattended
  batch waits at the first one" becomes: the Foreman does not try with the route rule missing
  (`push not tried: route rule missing`), so the push comes to you, and an unattended batch still
  waits at the first push that climbs to the user.
- **Direct mode, "Nothing is sent to yourself" (~line 1827):** "judged and run by you, as above,
  without asking the user" adds "and asked to the user only when the host refuses you too".
- **"A refusal is said before it is met" (~line 57):** one clause: the push ladder is not "trying
  the refused action to see": each step is the same push, by the session the cards name, judged
  first, with the lease; rule 7 holds (each refusal goes up with its exact text).
- **"Never" (~line 2164):** "(but the refused force push above)" kept.

### 4. `skills/chantier/references/routing.md`

- Foreman → Chief of Staff: `push <branch> <expected remote sha> <local sha>` becomes "(a Driver's
  refused force push the Foreman judged legitimate and the host refused it, or the Foreman did not
  try: its route rule missing; [foreman](foreman.md#a-drivers-refused-force-push), 'A Driver's
  refused force push')"; add `pushed <branch>` (the Foreman ran a Driver's refused force push; for
  the report) and `push failed <branch> <text>` (a failed lease at the Foreman's push; told to the
  user at once).
- Chief of Staff → Foreman: unchanged (`pushed`, `push failed`, `push refused`).

### 5. `skills/chantier/references/status-layout.md`, the Notes line (~line 98)

"When you ran a Driver's refused force push" becomes "When a Driver's refused force push was run
since the last report (by the Foreman, by you, or by you on the user's yes)": one line per push in
**Notes**: the CR (number and slug), the branch and `pushed for the Driver by <the Foreman | the
Chief of Staff | the Chief of Staff on your yes> (<each step: refused: <exact command> -> <exact
text>, or not tried: route rule missing>)`, quoting the notes as `handoff <cr>` prints them, or
"(no refusal recorded)" when the Driver left none. In Foreman mode the Chief of Staff learns of the
Foreman's push from its `pushed <branch>` line. The sentence on a push held for the user's word, or
failed, stays.

### 6. `skills/chantier/references/hosts/claude-code.md` (the host's specifics, only here)

- **"Allow rules", the table (~line 266):** one row after the route's row:
  `Bash(git -C * push --force-with-lease=chantier/* origin *chantier/*)` and `PowerShell(…)` |
  the steering session's route when its directory is not the main checkout, always with a planning
  surface (the project's clone that `take` names): `git -C <checkout> push
  --force-with-lease=<branch>:<expected> <remote> <sha>:refs/heads/<branch>` | a lease-protected
  force push of any `chantier/` branch, in any repository the `-C` path names; the steering session
  pushes only a branch the check ties to this batch (`foreman.md`, "A Driver's refused force
  push"); the rule's `*` does not enforce that, the card does | documented (rule form).
  The route row's use names the Foreman and the Chief of Staff.
- **The pasteable JSON block (~line 328):** the two lines
  `"Bash(git -C * push --force-with-lease=chantier/* origin *chantier/*)"` and
  `"PowerShell(git -C * push --force-with-lease=chantier/* origin *chantier/*)"` after the route's
  two lines (the test compares the block with `RECOMMENDED_ALLOW`).
- **"Capabilities and their commands", the "Every batch" row (~line 400):** the commands column
  names the route as `git [-C <checkout>] push --force-with-lease=<branch>:<sha> <remote>
  <sha>:refs/heads/<branch>`; the rules column gains `git -C * push --force-with-lease=chantier/*
  origin *chantier/*` right after `git push --force-with-lease=chantier/* origin *chantier/*` (the
  test compares the column with `SAMPLES`); the mark column's "a refusal goes the route of
  `driver.md`" becomes "a refusal climbs the ladder of `foreman.md`, 'A Driver's refused force
  push'".
- **"Auto mode", the refused-force-push bullet (~lines 449-457):** the route becomes the ladder
  (Driver, Foreman, Chief of Staff, the user's yes). The fact, form and date stay as written: "the
  steering session's own `git -C <worktree> push --force-with-lease=...` went through (**proved by
  use**, 2026-11-11, batch-09; not always: refused on 2026-11-13 as a loop)", with one addition:
  batch-09 was a direct batch, the Chief of Staff steering (its archive: `5-archives/261111-1247-171-batch-09-retro-fixes/work/retro.md`,
  "direct mode, the Chief of Staff steering"; `261111-0840-170-force-push-judgement/02-answers.md`),
  so that use proves the Chief of Staff's case, not the Foreman's (critic finding 6). Then the
  Foreman's push, per case: the Foreman is not a subagent but a session of its own, started with
  the user's permission mode (row "Start the Foreman's session");
  - **with the route rule set:** an allow rule resolves a matching command before the classifier
    for a steering session (**documented**, <https://code.claude.com/docs/en/permission-modes>; not
    yet seen for the Foreman);
  - **without it** (P10 names it missing): the Foreman does not try (`push not tried: route rule
    missing`); whether the classifier would pass it is **unproved**;
  - trial: the next Driver refusal in a Foreman batch, the Foreman's push accepted or refused, its
    exact text recorded here with the date.
- **The user's yes:** the classifier judges a command with the conversation as context; a user's
  own yes in the Chief of Staff's conversation, to a question that names the exact command, is what
  lets it see that the push is wanted. Mark: **unproved** unless the auto-mode docs say it (the
  Driver checks <https://code.claude.com/docs/en/auto-mode-config> and marks it documented with the
  link, or unproved with "checked <date>"); trial: the first push asked to the user this way,
  accepted or refused, recorded here.
- **The alert of the first turn (~line 478):** "It then goes to the Chief of Staff, who runs a
  legitimate one without asking you" becomes "It then goes to the Foreman, then to the Chief of
  Staff, who each judge and run a legitimate one without asking you; you are asked only if both are
  refused".
- CR-443 adds a sentence to the chantier rows' "Risk accepted" of the same table: a textual overlap
  only.

### 7. `skills/chantier/references/hosts/copilot.md`, Configuration (~line 80)

One sentence after "A refusal of a force push on Copilot is reported like any refusal (rule 7)":
the ladder of `foreman.md`, "A Driver's refused force push", holds. P10 does not run on Copilot and
no allow rule is recorded for it, so the Foreman skips the route-rule read (step 3) and tries the
push, as a Driver already does there (push-ladder-Q12). The risk, **unproved**: Copilot may stop the
Foreman's unwatched session on a prompt instead of refusing the push, which would halt the batch;
the first Copilot batch that meets a refused push records what Copilot did, with the date, here.

### 8. The CLI: `skills/chantier/scripts/cli/src/chantier/commands/allow_samples.py` and its test

- **`SAMPLES`:** one entry, right after the route's entry (`git push --force-with-lease={_BRANCH}:{_SHA}
  origin {_SHA}:refs/heads/{_BRANCH}`), keeping the table's order:

  ```python
  (
      "batch",
      "any",
      f"git -C {_TREE} push --force-with-lease={_BRANCH}:{_SHA} origin {_SHA}:refs/heads/{_BRANCH}",
      "git -C * push --force-with-lease=chantier/* origin *chantier/*",
  ),
  ```

  `RECOMMENDED_ALLOW` and P10's "every batch" count follow from it (P10 counts commands); nothing
  else in the CLI changes. P10's existing text names a missing rule as `<command> (add
  Bash(<rule>))` (and `PowerShell(<rule>)` on Windows), which the Foreman reads (section 2, step 3):
  no new output.
- **Its test**, `skills/chantier/scripts/cli/tests/test_cli_runs.py`:
  - `test_the_allow_rules_json_block_lists_exactly_what_preflight_checks` passes unchanged once the
    block and the table carry the rule (section 6): it already compares them with `SAMPLES` and
    checks that each sample is covered by its rule, in Bash and PowerShell, from the shipped
    `hosts/claude-code.md`.
  - `test_preflight_warns_on_missing_allow_rules_and_never_fails_on_them`: with the user's rules
    the two of today (`git push --force-with-lease -u origin chantier/*`, `git push
    --force-with-lease=chantier/* origin *chantier/*`), the P10 line also holds `add Bash(git -C *
    push --force-with-lease=chantier/* origin *chantier/*)`; with `filled_allow()` it does not.
- The scenario (`scenario/run_scenario.py`, the P10 section ~line 973): its checks hold as written
  (they name other rules); no new step.

### 9. `skills/chantier/references/startup-manifest.json`

The action `chief-of-staff` gains the reading `"foreman.md#A Driver's refused force push"`, after
`"chief-of-staff.md"`, so a Chief of Staff in Foreman mode reads the section its card links to
(critic finding 5). `test_startup_manifest.py` already asserts that every action's section resolves
to a non-empty level-2 section of the shipped file; the startup limit is not concerned (an action
reading, not a startup one). CR-438 adds the action `batch:stack` to the same file: textual overlap.

### 10. The docs (critic finding 4)

- **`docs/tutorial-claude-code.md`, "The classifier refused a chantier command" (~line 257):** one
  line added: "A Driver's force push the host refuses climbs on its own: the Foreman pushes it, then
  the Chief of Staff; you are asked only when both are refused."
- **The same page, "The Foreman was refused an action by a classifier" (~line 261):** one clause:
  "except a Driver's force push, which goes to the Chief of Staff, not to you".
- **`docs/hosts.md` (~line 39), the same sentence on a Foreman refused an action:** the same clause,
  so the two pages agree.

### 11. The eval kit (an eval-kit change: `just eval-dry-run` owed)

- **`evals/kit/audit.py` (~line 618), J22:** the exemption holds in both modes (not only `if
  direct:`) and only for a steering command that is the route form (`git [-C <path>] push
  --force-with-lease=<branch>:<sha> <remote> <sha>:refs/heads/<branch>`) **and** whose `<branch>`
  appears in an earlier `push judged legitimate` note command (`… note <cr> "push judged legitimate
  at <sha7> for <branch>: …"`) in the same steering transcript (critic finding 7). Any other push by
  a steering session still fails J22: a route push with no such note, and any `--force-with-lease
  -u` push, in either mode (today's direct-mode breadth narrowed on purpose, push-ladder-Q7). The
  preflight trial's `git -C <main checkout> push --force-with-lease -u <remote>
  chantier/preflight-trial --dry-run` is not the route form and is not exempted; the Driver checks
  that no `dry_run.py` case relies on today's breadth (the trial runs before the claim's window in
  a normal run). The printed line names the steering session, not "the Chief of Staff".
- **`evals/kit/dry_run.py`:** one new case, `foreman-route-push`, built like `plain-merge` and,
  for direct mode, like `audit-claim-call` (`data["steering"] = "direct"` and a claim):
  - Foreman mode: the Foreman's transcript holds the note command, then the route push: no `FAIL
    [J22]`;
  - Foreman mode: a route push with no note before it: `FAIL [J22]`;
  - direct mode: the Chief of Staff's note, then the route push: no `FAIL [J22]`;
  - direct mode: `git push --force-with-lease -u origin chantier/...`: `FAIL [J22]`.
  Added to `CASES`, the dispatch table and the docstring's case table.
- **`evals/SCORECARD.md`, rows J11 and J22:** J11 says the ladder (the Driver records and sends the
  `push` line; the Foreman judges and, the route rule present, pushes; refused or not tried, the
  Chief of Staff judges again and pushes with no ask; refused, one question to the user and one push
  on the yes; each refusal recorded with its exact text); its cards column gains `routing.md` and
  `hosts/claude-code.md`. J22's exception reads "a force push it runs on a Driver's `push` line, in
  the route form, after its `push judged legitimate` note, J11".

### 12. Not touched

- `agents/` and `com.github.copilot/agents/`: they hold no text of this route (no "force push" or
  "push refused" there). If the Driver finds one to change, both hosts' files change together and
  stay identical.
- The rest of the CLI: no command, no refusal, no output changes (section 8 is the only CLI edit).

## Out of scope

- Any change to the check or the judgement's content (moved, not changed).
- Any retry: a refusal is never retried at the same step, a failed lease never at any step.
- Changing the permission settings on a refusal (forbidden, as today); the new rule is added to the
  user's settings only through P10 and the Chief of Staff's existing ask, on the user's yes.
- Pushes that are not a Driver's refused force push (the release tag, `gh release create`, a plain
  push): their routes stay.
- The GitLab or Copilot behaviour beyond the sentence of section 7.

## Overlaps in batch-30

- CR-438 `stack-shape-guard`: moves the Foreman's stack rules from `foreman.md` into
  `foreman-stack.md` and adds `batch:stack` to `startup-manifest.json`; this CR's section is not a
  stack rule (section 2). Textual only.
- CR-442 `stack-git-chain`: edits `driver.md`'s stack sections and `test_came_back.py`; this CR
  edits "Means: a force push the host refuses" and adds one test there. Textual only.
- CR-443 `gate-hold-narrowing`: edits `foreman.md`'s lease sentences, `hosts/claude-code.md`'s
  allow-rules table, `test_cli_runs.py` and `docs/tutorial-claude-code.md` (another paragraph);
  textual only.
- CR-447 `docs-gardening`: runs last; its inventory row for this CR names `docs/tutorial-claude-code.md`
  and `docs/hosts.md` (section 10), not "none in docs/".
- No `depends.json`: no real dependency; whichever lands later rebases.

## Evidence

- `just check` passes (lint, tests, card structure) at the pushed head.
- `just eval-dry-run` passes, with the new `foreman-route-push` case (the CLI's `src/` and the eval
  kit change: AGENTS.md owes it before the first push), its output noted with the head's sha.
- `just scenario (ubuntu-latest)` green at the PR's head (a CLI and card change, AGENTS.md's long
  gate).
- The tests of section 8 (they read the shipped `hosts/claude-code.md` from the repository at the
  head under test) and `test_startup_manifest.py` (section 9, the shipped manifest and card).
- One test, reading the shipped cards from the repository at the head under test (no prepared
  text): `test_the_cards_name_the_push_ladder` in
  `skills/chantier/scripts/cli/tests/test_came_back.py`, beside the park test and with its `CARDS`
  (whitespace-normalised reads), asserting:
  - `foreman.md` holds the heading line `## A Driver's refused force push`, and in that section the
    route form `git push --force-with-lease=<branch>:<expected> <remote> <local sha>:refs/heads/<branch>`,
    `push judged legitimate at`, `push not tried: route rule missing` and
    `[foreman→chief-of-staff] pushed <branch>`;
  - `chief-of-staff.md`, `driver.md` and `routing.md` each hold `foreman.md#a-drivers-refused-force-push`;
  - `chief-of-staff.md` no longer holds the moved judgement's sentence "the local head holds the
    remote head's work rebased onto the CR's base" (one place: push-ladder-Q3), and holds "push
    judged legitimate", "both judgements" and "on the user's yes";
  - `driver.md` holds "the steering session does not send it" and not "the Chief of Staff does not
    send it";
  - `routing.md`'s Foreman → Chief of Staff row holds `pushed <branch>` and `push failed`.
- Host and default matrix (the route depends on the host and on the user's settings, not on a
  shipped default):
  - Claude Code, Foreman mode, route rule set: Driver → Foreman (documented to resolve before the
    classifier for a steering session; not yet seen for the Foreman) → Chief of Staff → user.
  - Claude Code, Foreman mode, route rule missing: Driver → Foreman (not tried, recorded) → Chief
    of Staff → user; the Chief of Staff's push without the rule: as batch-09, proved by use once.
  - Claude Code, direct mode: Driver → Chief of Staff (proved by use, batch-09) → user; the yes's
    effect unproved (section 6 trial).
  - Copilot, Foreman mode: Driver → Foreman (no P10 read, it tries; a prompt instead of a refusal
    unproved, section 7) → Chief of Staff → user.
  - Copilot, direct mode: Driver → Chief of Staff → user; unproved (section 7).

## Open questions

None: push-ladder-Q11 and Q12 closed v2's two.

## Note for the Chief of Staff

CR-447's inventory row for this CR must name `docs/tutorial-claude-code.md` (and `docs/hosts.md`),
not "none in docs/" (critic finding 4).
