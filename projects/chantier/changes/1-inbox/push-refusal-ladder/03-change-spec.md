# A refused push climbs: Foreman, then Chief of Staff, then the user

Spec v1 (2026-11-21). Short name: `push-ladder`. Destination: batch-30 (push-ladder-Q2).

## Goal

The user's words (2026-11-21): "Tu dois d'abord essayer dans ces cas au lieu de me demander."
When the host refuses a Driver's legitimate force push (in Claude Code, the auto-mode classifier
refusing a subagent's `git push --force-with-lease` on its own `chantier/` branch), the push climbs
a ladder and reaches the user only last:

1. the Foreman, which judges the push, tries the same legitimate push itself;
2. if the host refuses the Foreman, the Chief of Staff tries it, without asking the user;
3. only if the host refuses the Chief of Staff too, it asks the user one question, and on the
   user's yes pushes once. On Claude Code that yes, given in the conversation, is what tells the
   classifier the push is really wanted.

Each refusal is recorded with its exact command and the host's exact text, at the step that met it.

## Decisions carried (02-answers.md)

- **push-ladder-Q1, the ladder:** Foreman tries, then the Chief of Staff without asking, then the
  user's yes and one push. Carried in every section below.
- **push-ladder-Q2, the destination:** batch-30.

Decisions this specification takes where the answers say nothing on behaviour (each also listed as
an open question, option A, for the user to confirm or change):

- **D1. One judgement, one place.** The check and the judgement (today `chief-of-staff.md`, "A
  refused force push", steps 1 and 2) move, wording kept, into `foreman.md`, the steering session's
  card: the Foreman reads it there, and in direct mode the Chief of Staff reads `foreman.md` already
  ("Steering a batch yourself"). `chief-of-staff.md` keeps the ladder's last steps and refers to
  `foreman.md` for the check and the judgement; no card holds a second copy (open question 1).
- **D2. The same judgement, run once.** The Foreman runs the full check and judgement, not a
  lighter one. On the Foreman's escalation the Chief of Staff does not judge again: it runs the
  hard check only (the branch is this batch's, the `handoff` line) and reads the Foreman's
  `push judged legitimate` note; the lease (`--force-with-lease=<branch>:<expected>`) refuses the
  push if the remote moved since the judgement (open question 2).
- **D3. The push command.** Every steering-side push (Foreman or Chief of Staff, both modes) uses
  the form the Chief of Staff uses today, with its existing allow rule: `git push
  --force-with-lease=<branch>:<expected> <remote> <local sha>:refs/heads/<branch>`, one command per
  branch, from the main checkout (with a planning surface, the project's clone that `take` names)
  without changing its branch or touching its files; `git -C <that checkout>` only when the
  session's own directory is not it. No new allow rule in this CR (open question 3).

## What changes

### 1. `skills/chantier/references/driver.md`, "Means: a force push the host refuses"

- The opening sentence: "the Chief of Staff judges it and runs it for you" becomes: the push climbs
  the ladder (the steering session judges it and runs it; if the host refuses it there, the Chief
  of Staff runs it; if the host refuses the Chief of Staff, the user is asked once), "without the
  user's word in the normal case" kept. In direct mode the steering session is the Chief of Staff,
  so the ladder is Driver, Chief of Staff, the user.
- Steps 1 to 3 unchanged (the `refused:` note with the exact command and the host's whole text,
  the `next after push` note, `handback <cr> blocked waits: push <branch> <expected remote sha>
  <local sha>`).
- Step 4: the push line and the end unchanged; "when the Chief of Staff's answer comes back"
  becomes "when the push's answer comes back (the Foreman's, or the Chief of Staff's)".
- The fresh Driver's reading of its `push:` note: `pushed <branch>`, `push failed`, `push refused
  <branch>: no long gate passed at <sha>` unchanged. "Any other `push refused` (the branch is not
  this batch's, or the Chief of Staff's own push was refused)" becomes "(the branch is not this
  batch's, the push was judged not legitimate and the user said no, or the host refused it at every
  step, the user's yes included)": `handback blocked refused <exact text>` at once, as today.
- The stack driver's sentence: it sends one push line per refused branch and waits for each result
  as a note, as today; the result may now come from the Foreman's own push. No other push, no
  other way.
- The Release driver: covered by the same section, no own text.

### 2. `skills/chantier/references/foreman.md`, the push bullet (today ~line 738)

The bullet "A Driver's `[driver <cr>→foreman] push …`" is rewritten; its sub-bullets on the
answer's way back to a fresh Driver, the never-pinged Driver and the stack driver's note stay. The
new text:

- **The check and the judgement**, moved verbatim from `chief-of-staff.md` steps 1 and 2 (links
  adjusted: "the Chief of Staff" read as "you" where it names the judge). Its own refusals now go
  straight back, with no hop: a branch that is not this batch's, or no long gate passed at the
  local head (with the same three skips: the `ci: beside the long gate` line, a branch whose PR the
  record holds, a pipeline job as the long gate): take the CR back yourself with `take <cr> --note
  "push: push refused <branch>: <the reason>"` by the restart path's steps, as for any answer.
- **Legitimate:** first `$CHANTIER note <cr> "push judged legitimate at <local sha7>: <one line:
  what the judgement checked>"`, then the push in D3's form, one command per branch, never a loop
  or a script, even for a whole restack. Accepted: take the CR back with `push: pushed <branch>`
  (the stack driver: `[foreman→driver stack] note push <branch>: pushed <branch>`) and send
  `[foreman→chief-of-staff] pushed <branch>` (information for the Chief of Staff's report; it
  answers nothing).
- **Not legitimate:** push nothing; `$CHANTIER asks "<the CR, number and slug>: push <branch>
  <expected> <local> not legitimate: <what the judgement found>"` (the existing ask channel, which
  the Chief of Staff relays to the user). The CR keeps waiting; the Chief of Staff answers
  `pushed`, or `push refused <branch>: <the user's reason>`, by the existing answer lines.
- **A failed lease** (git rejects the lease: the remote moved): never retried, at any step. Take
  the CR back with `push: push failed <branch> <git's text>` (the Driver looks at why) and send
  `[foreman→chief-of-staff] push failed <branch> <git's text>`; the Chief of Staff tells the user
  at once, and nobody waits for a word.
- **The host refuses your push:** `$CHANTIER note <cr> "refused: <the exact command> -> <the
  host's exact text>"` first, then send `[foreman→chief-of-staff] push <branch> <expected remote
  sha> <local sha>`, not through `asks`. That line from the Foreman now means: judged legitimate,
  refused to the Foreman, both recorded. Retry nothing, try no other form, change no permission
  setting. Wait for the Chief of Staff's answer (`pushed <branch>`, `push failed <branch> <text>`,
  `push refused <branch>: <text>`) and take the CR back with it, as the existing sub-bullets say.
- "The Chief of Staff judges the push and may ask the user first" and "A push the host refuses the
  Chief of Staff too is the user's, shown by it" are replaced by the ladder above.
- "Record each refusal once, whoever sees it": kept, its list now the Driver's, yours and the
  Chief of Staff's, each before the next step's line.
- **"The user's boundaries", the never-push bullet (~line 205):** "Never code, review, commit,
  rebase, push or edit a PR" gains a second named exception beside the PR close: the push of a
  Driver's refused force push, as this bullet says.
- CR-438 moves the Foreman's stack rules into `foreman-stack.md`; this bullet is not a stack rule
  and stays in `foreman.md`. If CR-438 has landed and moved the stack driver's note sub-bullet, the
  matching sentence goes where it now lives.

### 3. `skills/chantier/references/chief-of-staff.md`

- **"A refused force push" (~line 1364)** becomes the ladder's top, still "not a question for the
  user" in the normal case:
  - On `[foreman→chief-of-staff] push <branch> <expected> <local>` (the Foreman judged it and the
    host refused the Foreman): the check of `foreman.md` (the branch is this batch's, the
    `handoff` line), no second judgement; read the Foreman's `push judged legitimate` note and its
    `refused:` note in `handoff <cr>`. Then the push in D3's form, at once, no ask. Missing
    `push judged legitimate` note: run the judgement of `foreman.md` yourself before the push.
  - In direct mode (the Driver's `push` line): you are the steering session; run `foreman.md`'s
    check and judgement, record `push judged legitimate`, then push, no ask.
  - Accepted: answer `pushed <branch>` (in direct mode, the CR's `take` note); the report's line
    (section 5).
  - A failed lease: today's step 5 unchanged (`push failed <branch> <git's text>`, the user told at
    once, never retried).
  - **The host refuses your push:** record it at once with `$CHANTIER note <cr> "refused: <the
    exact command> -> <the host's exact text>"`, then ask the user **one question**, in the
    report's shape (the **For you:** line, no tip), naming: the CR (number and slug), the branch,
    the expected and local shas, that the push was judged legitimate (by whom: the Foreman, or
    you in direct mode, with the note's one line), the refusal at each step with its exact command
    and the host's exact text (the Driver's, the Foreman's when there is one, yours, quoted from
    the `refused:` notes as `handoff <cr>` prints them), and the exact command you will run on a
    yes. In direct mode record it with `$CHANTIER asks "<the question>"` too, as any ask.
  - **On the user's yes:** run that command once, unchanged. Accepted: `pushed <branch>`. Refused
    again: record it (`refused:` note), show the user the exact text and the command so they can
    run it themselves or allow it, answer `push refused <branch>: <exact text>`; never a second
    try, never another form, never a change to the permission settings. A failed lease: as above.
  - **On the user's no:** answer `push refused <branch>: <the user's reason>`.
  - **A push the Foreman judged not legitimate** (its ask): today's step 4, unchanged in substance:
    the user hears it at once; on the user's go, push in D3's form (a host refusal then: show the
    exact text and the command, answer `push refused <branch>: <exact text>`, no second try);
    on a no, `push refused <branch>: <the user's reason>`.
  - Steps 1 and 2 (the check, the judgement) leave this section for `foreman.md` (D1); this
    section names it ("the check and the judgement of `foreman.md`, 'A Driver's refused force
    push'").
  - "All answers go to the Foreman, never to the Driver": kept.
- **Preflight "On the yes" (~line 120):** "a refused one comes to you, and you run it when it is
  legitimate" becomes "a refused one climbs: the Foreman runs it, then you; the user is asked only
  when the host refuses you too".
- **Preflight "On a no" (~line 132):** "goes Driver -> Foreman -> Chief of Staff, and an unattended
  batch waits at the first one" becomes the ladder (Driver, Foreman, Chief of Staff, then the user
  only when the host refuses all), and an unattended batch still waits at the first push that
  climbs to the user.
- **Direct mode "Nothing is sent to yourself" (~line 1827):** "judged and run by you, as above,
  without asking the user" adds "and asked to the user only when the host refuses you too".
- **"A refusal is said before it is met" (~line 57):** one clause: the push ladder is not "trying
  the refused action to see": each step is the same push, by the session the cards name, with the
  lease; rule 7 holds (each refusal goes up with its exact text).
- **"Never" (~line 2164):** "(but the refused force push above)" kept.

### 4. `skills/chantier/references/routing.md`

- Foreman → Chief of Staff: `push <branch> <expected remote sha> <local sha>` described as "a
  Driver's refused force push the Foreman judged legitimate and the host refused it too"; add
  `pushed <branch>` (the Foreman ran a Driver's refused force push; for the report) and `push failed
  <branch> <text>` (a failed lease at the Foreman's push; told to the user at once).
- Chief of Staff → Foreman: unchanged (`pushed`, `push failed`, `push refused`).

### 5. `skills/chantier/references/status-layout.md`, the Notes line (~line 98)

"When you ran a Driver's refused force push" becomes "When a Driver's refused force push was run
since the last report (by the Foreman, by you, or by you on the user's yes)": one line per push in
**Notes**: the CR (number and slug), the branch and `pushed for the Driver by <the Foreman | the
Chief of Staff | the Chief of Staff on your yes> (refused: <each step's exact command -> exact
text>)`, quoting the `refused:` notes as `handoff <cr>` prints them, or "(no refusal recorded)"
when the Driver left none. In Foreman mode the Chief of Staff learns of the Foreman's push from its
`pushed <branch>` line. The sentence on a push held for the user's word, or failed, stays.

### 6. `skills/chantier/references/hosts/claude-code.md` (the host's specifics, only here)

- "Auto mode", the refused-force-push bullet (~lines 449-457): the route becomes the ladder
  (Driver, Foreman, Chief of Staff, the user's yes). Why on this host: the classifier blocks
  destructive git in subagents ("Git Destructive"); the Foreman is not a subagent but a session of
  its own, started with the user's permission mode (row "Start the Foreman's session"), so it may
  pass where a Driver is refused: **unproved**; trial: the next Driver refusal in a Foreman batch,
  the Foreman's push accepted or refused, its exact text recorded here with the date.
- The user's yes: the classifier judges a command with the conversation as context; a user's own
  yes in the Chief of Staff's conversation, to a question that names the exact command, is what
  lets it see that the push is wanted. Mark: **unproved** unless the auto-mode docs say it (the
  Driver checks <https://code.claude.com/docs/en/auto-mode-config> and marks it documented with the
  link, or unproved with "checked <date>"); trial: the first push asked to the user this way,
  accepted or refused, recorded here.
- The alert of the first turn (~line 478): "It then goes to the Chief of Staff, who runs a
  legitimate one without asking you" becomes "It then goes to the Foreman, then to the Chief of
  Staff, who run a legitimate one without asking you; you are asked only if both are refused".
- The allow-rules row of the steering route (~line 266): "the steering session's route" names the
  Foreman and the Chief of Staff. The capability row (~line 400): "a refusal goes the route of
  `driver.md`" kept.
- CR-443 adds a sentence to the chantier rows' "Risk accepted" of the same table: a textual
  overlap only.

### 7. `skills/chantier/references/hosts/copilot.md`, Configuration (~line 80)

One sentence after "A refusal of a force push on Copilot is reported like any refusal (rule 7)":
the ladder of `driver.md` holds as written; whether Copilot refuses such a push at all, and to
which session, is **unproved** until a Copilot batch meets one.

### 8. The eval kit (this makes the CR more than cards-only)

- `evals/kit/audit.py` (~line 618): J22 exempts a steering session's force push on a Driver's
  `push` line only in direct mode (`if direct:`). With the ladder the Foreman runs it too: the
  exemption holds in both modes, and only for D3's route form (a `git [-C <path>] push
  --force-with-lease=<branch>:<sha> <remote> <sha>:refs/heads/chantier/...`), so any other push by
  a steering session still fails J22. Its printed line names the steering session, not "the Chief
  of Staff".
- `evals/kit/dry_run.py`: one new case, `foreman-route-push`, built like `plain-merge`: the
  Foreman's transcript holds the route push; the audit has no `FAIL [J22]`; the same transcript
  with `git push --force-with-lease -u origin chantier/...` (not the route form) fails `[J22]`.
  Added to `CASES` and the case table.
- `evals/SCORECARD.md`, rows J11 and J22: J11 says the ladder (the Driver records and sends the
  `push` line; the Foreman judges and pushes; refused, the Chief of Staff pushes with no ask;
  refused, one question to the user and one push on the yes; each refusal recorded with its exact
  text); its cards column gains `routing.md` and `hosts/claude-code.md`. J22's exception reads "a
  force push it runs on a Driver's `push` line, in the route form, J11".

### 9. Not touched

- `agents/` and `com.github.copilot/agents/`: they hold no text of this route (checked: no
  "force push" or "push refused" there). If the Driver finds one to change, both hosts' files
  change together and stay identical.
- The CLI (`src/`): no change. `allow_samples.py` already carries the route form's rule
  (`git push --force-with-lease=chantier/* origin *chantier/*`).
- `docs/`: no page describes the route today (only the v0.9.0 release notes, history, untouched).
  CR-447 (docs gardening, last in batch-30) records this CR as "none in docs/" in its inventory.

## Out of scope

- A new allow rule (the `git -C *` form of the route), or any P10 change (open question 3).
- Any change to the check or the judgement's content (moved, not changed).
- Any retry: a refusal is never retried at the same step, a failed lease never at any step.
- Changing the permission settings on a refusal (forbidden, as today).
- Pushes that are not a Driver's refused force push (the release tag, `gh release create`, a
  plain push): their routes stay.
- The GitLab or Copilot behaviour beyond the sentence of section 7.

## Overlaps in batch-30

- CR-438 `stack-shape-guard`: moves the Foreman's stack rules from `foreman.md` into
  `foreman-stack.md`; this CR's bullet is not a stack rule (section 2). Textual only.
- CR-442 `stack-git-chain`: edits `driver.md`'s stack sections ("push with `--force-with-lease`");
  this CR edits "Means: a force push the host refuses" only. Textual only.
- CR-443 `gate-hold-narrowing`: edits `foreman.md`'s lease sentences and `hosts/claude-code.md`'s
  allow-rules table; textual only.
- CR-447 `docs-gardening`: runs last; one inventory row (section 9).
- No `depends.json`: no real dependency; whichever lands later rebases.

## Evidence

- `just check` passes (lint, tests, card structure) at the pushed head.
- `just eval-dry-run` passes, with the new `foreman-route-push` case (the eval kit changed:
  AGENTS.md owes it before the first push), its output noted with the head's sha.
- `just scenario (ubuntu-latest)` green at the PR's head (a card change, AGENTS.md's long gate).
- One test, reading the shipped cards from the repository at the head under test (no prepared
  text): `test_the_cards_name_the_push_ladder` in
  `skills/chantier/scripts/cli/tests/test_came_back.py`, beside the park test and with its
  `CARDS` (whitespace-normalised reads), asserting:
  - `foreman.md` holds the route form `git push --force-with-lease=<branch>:<expected> <remote>
    <local sha>:refs/heads/<branch>`, `push judged legitimate`, and `[foreman→chief-of-staff]
    pushed <branch>`;
  - `chief-of-staff.md` refers to `foreman.md` for the judgement and no longer holds the moved
    judgement's sentence "the local head holds the remote head's work rebased onto the CR's base"
    (one place: D1), and holds the ask's "judged legitimate" and "on the user's yes";
  - `routing.md`'s Foreman → Chief of Staff row holds `pushed <branch>` and `push failed`.
- Host matrix (the route depends on the host):
  - Claude Code, Foreman mode: Driver → Foreman → Chief of Staff → user; Foreman's push unproved
    (section 6 trial).
  - Claude Code, direct mode: Driver → Chief of Staff → user; the yes's effect unproved (section 6
    trial).
  - Copilot, both modes: the ladder as written, unproved (section 7).

## Open questions (for the Chief of Staff)

1. **Where the check and the judgement live.** A: in `foreman.md` (moved from
   `chief-of-staff.md`, wording kept), the Chief of Staff referring to it (D1). B: they stay in
   `chief-of-staff.md` and `foreman.md` refers there. C: a shared section in `concepts.md`.
2. **Does the Chief of Staff judge again after the Foreman's refusal?** A: no; the hard check
   only, the Foreman's `push judged legitimate` note and the lease (D2). B: it runs the full
   judgement again before its push.
3. **The Foreman's command and its allow rule.** A: D3's route form, from the main checkout (or the
   project's clone), with the existing rule; `git -C` only when the session's directory is not
   that checkout, with no new rule (cards and eval kit only, no CLI change). B: also add `git -C *
   push --force-with-lease=chantier/* origin *chantier/*` to P10's rules (`allow_samples.py`, its
   test, `hosts/claude-code.md`): a CLI change, so `just eval-dry-run` and the scenario owe it
   anyway.
4. **A push the Foreman judges not legitimate.** A: the Foreman asks the user through `asks`; on
   the user's go the Chief of Staff pushes (the yes is in its conversation). B: the Foreman sends
   it to the Chief of Staff as today's `push` line and the Chief of Staff judges and asks.
5. **The eval audit's J22 exemption.** A: both modes, the route form only (section 8). B: both
   modes, any `--force-with-lease` push by a steering session (today's direct-mode breadth).
