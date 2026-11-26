# Study: the host's classifier and permission refusals of chantier agents' commands

Read-only study for `simplify-cards-and-prompts`, 2026-11-24. Transcript text was read as data.

## Summary

- Since 2026-11-13 the auto-mode classifier refused 64 tool calls of chantier roles, in 18
  sessions and 40 subagent runs. Force pushes are the first cause (13), then chantier's own
  subcommands (about 10), process kills (7), `gh pr` (6).
- A force push is refused rarely: 13 refusals for 267 that ran (4.6 %). A rebase almost never: 1
  for 720. But each refusal ends a Driver, costs a fresh Driver, and 4 times reached the user.
- The allow rules do not do what P10 says. 83 % of the force pushes the agents typed were
  compound commands (`W=...; git -C $W push ... | tail -3`, `cd ...; git push ...`), which no allow
  rule can match, so the classifier judged them. 12 of the 13 refusals were compound. The one case
  the host card holds as "refused with the rule set" (batch-23, CR-318) was such a compound
  command: it does not prove that the classifier overrides a matching rule.
- The steering session's own push was never refused in the window except once, for 14 pushes in
  one PowerShell loop (batch-15). So a Chief of Staff can settle a refused own-branch push alone;
  it did so 8 times in 1 to 5 minutes, and asked the user once when it should not have.
- A CLI subcommand that runs the push is technically sound (the classifier sees the tool call, not
  the child process) and would give one stable command and real rails. It is not invisible: the
  classifier reads the chantier command's text and has refused chantier subcommands on their
  meaning (`merge`, `verdict`, `order budget`, `order merged`). It needs a trial, and it changes
  two rules of `AGENTS.md`.

## Method and sample

- Files: every `*.jsonl` under `C:/Users/gaeta/.claude/projects` modified in the last 11 days:
  5033 transcripts, 5.0 GB, main sessions and `subagents/` (role from each `.meta.json`
  `agentType`). Projects: chantier (3755 files), markdown-okf-schema-studio (707), the planning
  surface (322), the evals, hass-brain (20).
- Pass 1: tool results whose text starts with a host refusal (the classifier's, the "no verdict"
  one, don't-ask mode, the built-in safety check, the user's own rejection), joined to the tool
  call by id, with the next six actions. Texts that only quote a refusal (cards, retros) were
  dropped. 225 refusals, 129 since 2026-11-13 once the copies of resumed sessions are removed.
- Pass 2: every Bash or PowerShell call holding a `git push` or a `git rebase`, with its result
  (2363 calls since 2026-11-13), to get the denominators and the command's form.
- Pass 3: the main sessions' texts, wrap-ups and questions that name a refusal (177).
- Limits: a role is known for a subagent, not for a main session (Chief of Staff or Foreman is
  read from the text). "Ran" for a push means git's output shows it. The counts of chantier
  subcommands refused are by hand, from 11 calls. Scripts are in the session's scratchpad.

## Findings

### 1. What is refused, and to whom (since 2026-11-13)

| Kind | Count | Notes |
| --- | ---: | --- |
| Auto-mode classifier | 64 | all in projects run by chantier |
| "No verdict" (a hook changed the call's input) | 13 | session tools, 2 chantier commands |
| Built-in safety check | 12 | 7 `rm`, mostly Coders' scratch cleanups |
| Don't-ask mode | 20 | the permission trials of CR work, not a batch |
| The user's own rejection | 20 | 3 of them questions the user closed |

The 64 classifier refusals, by command and by role:

| Command | Count | | Role | Count |
| --- | ---: | --- | --- | ---: |
| `git push --force-with-lease` | 13 | | main session (Chief of Staff, Foreman) | 20 |
| a chantier subcommand | 11 | | cr-driver | 17 |
| other shell (inline scripts, `git checkout <file>`) | 10 | | coder | 12 |
| `Stop-Process`, `taskkill` | 7 | | stack-driver | 6 |
| `gh pr ready`, `gh pr edit --base` | 6 | | verifier | 5 |
| `git commit` in a chain, `git stash` | 3 | | release-driver | 2 |
| session tools, `SendMessage`, `Edit`, `Agent`, `Monitor` | 9 | | general-purpose | 2 |
| `gh release create`, `rm -rf`, plain push, rebase, settings | 5 | | | |

The label is "Destructive or Unwanted Actions" for 53 of the 103 refusals of the whole sample;
"Git Destructive" appears twice only, both before 2026-11-13.

### 2. Force push and rebase: the rates

| Since 2026-11-13 | Ran | Refused |
| --- | ---: | ---: |
| Force push, cr-driver | 128 | 10 |
| Force push, stack-driver | 103 | 2 |
| Force push, main session | 33 | 1 |
| Rebase, all roles | 720 | 1 |

- Every force push was `--force-with-lease`; no plain `--force` was typed.
- Refusals per day: 0 to 3, on 8 of 12 days. After 2026-11-23 (the `Rewrites:` line, commit
  `55fed1ef`): 24 ran, 0 refused; too few to conclude.
- The classifier is not steady. On 2026-11-21 a stack driver sent five identical pushes in one
  turn: four ran, one was refused, and the same command ran at the retry.

### 3. The form of the command, and what the allow rules can match

| Form of the force push | Ran | Refused |
| --- | ---: | ---: |
| exactly one `git [-C <path>] push --force-with-lease ...` | 13 | 0 |
| the same with `2>&1 \| tail -3` | 33 | 1 |
| starts with an assignment, a `cd` or a shell function | 206 | 11 |
| other chain or loop | 15 | 1 |

- `hosts/claude-code.md` documents that a rule does not match past a leading assignment and that a
  compound passes only when every part is allowed. So 233 of 280 pushes were out of the rules'
  reach, whatever `~/.claude/settings.json` holds. P10 checks the cards' sample commands, not what
  the agents type.
- CR-318 (batch-23), the card's proof of "refused with the rule set", was typed
  `W="..."; git -C $W push --force-with-lease -u origin chantier/batch-23/cr-318-cr 2>&1 | tail -3`.
  The rule could not match it. The card's claim is unproved, not proved.
- The user's settings hold the six force-push rules and none of the eighteen rebase rules that P10
  now names. Rebases ran 720 times without them.
- The same holds for chantier's own commands: agents call them through `C="uv run ..."; $C ...` or
  a shell function, so the `chantier *` rules seldom match either.

### 4. What the agent did next

For the 13 refused force pushes and the one refused rebase:

| Date | Unit | Next | The user |
| --- | --- | --- | --- |
| 11-13 | batch-15 restack, 14 pushes in a loop | refused to the Foreman, then to the Chief of Staff; a script left for the user | ran it in the morning |
| 11-16 | CR-304 | push line; the Chief of Staff pushed in 1 minute | told only |
| 11-17 | CR-338 (Studio) | the Driver ran the rebase again alone; branch already current | none |
| 11-17 | CR-318 | note, hand-back; the Chief of Staff pushed in 5 minutes | none |
| 11-17 | CR-337, stack driver | handed back; the stack left partial | none seen |
| 11-18 | CR-375 | the Chief of Staff pushed in 1 minute | told only |
| 11-20 | CR-393, twice | the Chief of Staff pushed in 2 minutes | none |
| 11-21 | Studio stack driver | same command again, ran | none |
| 11-21 | CR-434 | the Chief of Staff asked the user, then pushed | one question |
| 11-21, 11-22 | CR-439, CR-429, CR-458 | the Chief of Staff pushed | none |
| 11-23 | Studio batch-09, rebase | Driver, Foreman, Chief of Staff, the user | one question |

- No agent worked around a refusal. Drivers recorded it and ended, as `driver.md` says. One
  Driver's report: "I did not retry or look for another route."
- The cost is not the user's time first: each refusal ends a Driver and starts a fresh one that
  reads its record again.
- A false belief spread. On 2026-11-22 a Foreman wrote that a force push is one "which a Driver
  cannot run", and the steering session ran 31 route pushes in the window for 13 refusals:
  pushes went up the ladder without a Driver's try, though 95 % of Drivers' tries pass.

### 5. Questions put to the user because of a refusal

Counted in the steering sessions' texts and questions since 2026-11-13: about 10.

- Force push or rebase of a CR branch: 4 (the batch-15 script, "j'ajoute les règles manquantes et
  je pousse sans te demander ?", CR-434, the batch-09 rebase).
- Other refused commands that went to the user: `gh pr edit --base` (11-13), the `gh stack`
  install (11-13), `gh release create` (11-13), the release branch's push and PR, "Undermining
  Oversight" (11-19), a Verifier's leftover process to stop (11-22), the Foreman session's start
  (11-22).
- The allow rules themselves: the P10 question at each new rule set, and one edit of
  `settings.json` that the classifier refused to the Chief of Staff (11-13).
- Three grills came from it: `forge-permissions-at-start`, `push-refusal-ladder`,
  `own-branch-push`. The cards grew each time: the ladder is about 280 lines in `driver.md`,
  `foreman.md` and `chief-of-staff.md`, and the rules table of the host card about 40 rows.

### 6. What the repository says today

- `AGENTS.md`: "The rest of the CLI keeps no git write"; the named git exceptions are the surface
  writer and the batch's end cleanup. A new CLI tool "comes from measured token-costly
  behaviour". "No fallback: ... no workaround in the skill or the CLI."
- `chantier ship` (`commands/delivery.py`) records the PR at the worktree's head, reads the PR's
  base and draft state once, and prints what is off (`... is not pushed, not this head: push with
  --force-with-lease, then ship again`). It runs no git write.
- P10 (`commands/preflight.py`, `permissions.py`, `allow_samples.py`) warns only, by matching
  sample commands against the settings' allow rules. It cannot see the classifier.
- `hosts/claude-code.md`, "Auto mode": an allow rule resolves before the classifier (documented);
  auto mode drops broad rules such as package-manager run commands; whether it drops the
  `chantier *` rules is marked unproved.

### 7. Does a command inside a chantier subcommand escape the classifier?

- Yes for the child process. The host judges the tool call's text with the conversation; it does
  not see what the process runs. In the sample, `just scenario` and `chantier gate` run git
  commits and pushes in sandboxes with no refusal, and the surface writer pushes the planning
  surface.
- No for the tool call itself. When no allow rule matches (the usual case, finding 3), the
  classifier reads the chantier command and judges its meaning. Refused in the whole sample:
  `merge CR-108` ("Merge Without Review", twice), `verdict CR-312 VERIFIED` ("Undermining
  Oversight"), `order budget --note 400`, `order merged` (twice, 11-24), `serve --restart`,
  `board --host <LAN address>` ("Expose Local Services").
- The host's refusal text sets the limit: "do not use your ability to run tests to execute
  non-test actions". A subcommand used as a detour after a refusal is that. A subcommand that is
  the one designed way to publish a CR branch, checked by the CLI and granted by the user's
  `chantier *` rule, is not; the owner decides which this is.

## Options

### A. A CLI subcommand that pushes (`chantier push <cr>`, or `ship` doing the push)

- What: from the CR's worktree, `git push --force-with-lease=<branch>:<remote head read> <remote>
  HEAD:refs/heads/<branch>`, after rails: the branch is the CR's recorded one, matches
  `chantier/*`, is not the default branch, the caller holds the CR's lease, the worktree is clean.
- For: one short, stable command; the rails are code, where today the rule's `*` enforces nothing
  ("the card does"); the Driver never types `git push --force`; the ladder and most of the rules
  table can leave the cards, which is this CR's aim. Measured cost to justify it: 13 refusals in
  12 days, each a lost Driver, and 4 user questions.
- Against: it changes `AGENTS.md` (a third git exception, a network use, and the "no workaround"
  line needs the owner's word). The classifier still reads `chantier push ...` when no rule
  matches, and its verdict on that text is unproved: a trial in auto mode, from a Driver, in the
  compound form agents type, must come before any card is cut. It must be refused through a
  profile's `cli.run`, like `gate`. A rebase is not covered (1 refusal in 721, so leave it).
- Variant: `ship --push` saves a call but mixes a forge read, a record and a git write.

### B. Allow rules by preflight (today)

- For: documented, the user's own grant, no CLI change.
- Against: they match one exact form and agents type another 83 % of the time; P10 then says
  "allowed" and the refusal comes anyway; one question per machine and per new rule; 36 rules
  for pushes and rebases alone. Telling the Drivers to type the exact form is already in the
  cards and is not followed. A cheaper help inside this option: `take` prints the exact push
  line to paste, alone, with no variable and no pipe.

### C. A hook that allows

- A plugin hook answering "allow" for an own-branch push. Unproved, and the sample speaks
  against it: 13 calls got "a hook changed this call's input after auto mode reviewed it", so the
  classifier reviews before hooks run. A hook is also one more thing in `hooks/` to keep on two
  hosts. Not recommended without a trial. Which hook changed those 13 inputs was not traced.

### D. A host setting

- The auto-mode configuration (`claude auto-mode defaults`, the auto-mode-config page) lets the
  user describe what is routine in their environment; a line on lease-protected pushes of
  `chantier/*` branches may lower the refusals. Its exact keys were not checked here. It is the
  user's own setting: chantier may print the text to paste, never write it. Leaving auto mode for
  a looser mode is the user's choice and nothing chantier should ask for.

### E. Keep the ladder, shorten it

- The steering session pushes; it is not a subagent and was refused once in 34 tries. With A
  refused, the cheapest card is: a Driver refused sends one line; the steering session pushes at
  once in the route form, one command; the user hears of it in the report.

## What a Chief of Staff could settle alone

- A refused `--force-with-lease` push or rebase of a `chantier/*` CR branch that the record ties
  to the batch: run it, tell the user in the report. Done 8 times; never a question.
- A Driver's refused `gh pr ready`, `gh pr edit --base` on the batch's own PRs: run it (the Chief of Staff
  did so for CR-223 on 11-14).
- A chantier subcommand refused in a chain: run it again alone, in the form the rule matches.
- A refused loop or script: one command per branch (batch-15's 14 pushes were one loop).
- Not alone, and rightly asked: editing `settings.json`, stopping a process it did not start,
  publishing a release, starting a session the host refused, deleting branches or folders, and any
  push of a branch that is not the CR's own.
