# Answers

No grill: a retro point of batch-24 (2026-11-17) that the user put straight into the batch.

- The user's word (2026-11-17): "remet les 5 dans le batch et on continue" (put the five retro
  points back in the batch and go on). This CR is one of the five. The user asked no question and
  settled no behaviour; each choice below is settled by the Chief of Staff, within the request.

- A fact the Chief of Staff gave for the specification: the shell that locked the CR-330 folder
  was `bash -c "until grep -qE ... <task>.output; do sleep 5; done; tail -5 ..."`, a monitor or
  background shell started by the Foreman session itself, with its current folder in the CR's
  folder in the planning surface, still running after its purpose had passed. So the rule covers
  two cases: a Driver's own background shells, and the steering session's own (the Foreman, or the
  Chief of Staff in direct mode, which reads the Foreman's card).

- bg-Q1 (who): every Driver kind (CR, stack, QA, release) and the steering session running a batch
  (the Foreman; the Chief of Staff in direct mode). The workers (Coder, Inspector, Verifier,
  Investigator, Debugger, Conflict resolver, Demo explorer) already run no background shell by
  their cards: unchanged. Settled by the Chief of Staff.
- bg-Q2 (what counts): a background shell and a host monitor (a tool that streams a command's
  output to its owner) are the same thing here, "a background task". A task that waits on a file
  or on another task's output (`until grep …; do sleep …; done`) is a polling loop, which the
  shared rule 8 of `concepts.md` already forbids; the change names this form so it is recognised.
  Settled by the Chief of Staff.
- bg-Q3 (the current folder): no shell call, foreground or background, sets its current folder
  inside a CR's folder (any stage of the planning folder) or inside a worktree: no `cd`,
  `Set-Location` or `pushd` there, in a call or chained before a command. Commands name their
  targets instead (`git -C <worktree>`, absolute paths, `gh … --repo <owner>/<name>`,
  `glab … -R <owner>/<name>`). Foreground calls are covered too because a session's folder carries
  over from one call to the next and a later background task inherits it. The CLI's long gate is
  not concerned: `$CHANTIER gate` runs its command in the worktree itself and is stopped by
  `gate <cr> --stop`. Settled by the Chief of Staff.
- bg-Q4 (the Driver's stop): a Driver stops each background task it started as soon as its result
  is read or no longer counts (today's rule for the CI watch when the gate fails first, made
  general), and, before every `$CHANTIER handback` (ready or blocked, whatever the reason,
  `context:` and `waits: push` included), stops every one still running, by the id its start
  returned, with the host's stop of a background task. A long gate still running at that moment
  is stopped first with `$CHANTIER gate <cr> --stop` (recorded `stopped`; the next Driver runs it
  again). Settled by the Chief of Staff.
- bg-Q5 (the steering session's own tasks): the Foreman (and the Chief of Staff in direct mode)
  starts no background task to wait for anything (a file, a task's output, a Driver, CI): what
  wakes it is a Driver's line, the host's notice about a Driver, an order, and the heartbeat. A
  background task of its own that runs anyway is stopped at once by its id, and none is left
  running when it ends the heartbeat or pauses the batch. The board (the Chief of Staff's
  background command, `session-start.md`) keeps its own start and stop rules; only the
  current-folder rule (bg-Q3) applies to it. Settled by the Chief of Staff.
- bg-Q6 (the steering session's backstop for an ended Driver): when a CR or Release Driver whose
  hand-back the record already holds (the CR `ready`, `blocked`, merged or cancelled) wakes again
  with no message from the steering session since that hand-back (its hand-back line sent a
  second time, any other line that answers nothing, or the host's notice that it is waiting on its
  own background work), the steering session does not act on the line again (the record holds the
  hand-back), stops that Driver by the host's means ("Stop a Driver"), records
  `note <cr> "stopped: leftover background work after its hand-back"` and clears its id
  (`agents set <cr> - --epoch <n>`), as "A Driver stopped from outside", "Keeping its own stops
  apart" already asks for its own stops. It is neither a restart nor a silent end, and counts
  toward nothing. A later take-back of that CR finds no id to resume and starts a new CR Driver
  with `take <cr> --note "resume: <the take's note>"`. Settled by the Chief of Staff.
- bg-Q7 (where the host's tool is named): the request says the Foreman's card names `TaskStop`.
  The cards may not name a host tool (`test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`
  refuses `TaskStop` in a card): the cards say "the host's stop of a background task" and "Stop a
  Driver", and `hosts/claude-code.md` names `TaskStop` in its rows; `hosts/copilot.md` names
  Copilot's means, unproved. Settled by the Chief of Staff.
- bg-Q8 (the Driver's tool on Claude Code): the four Claude Code Driver agents (`agents/cr-driver.md`,
  `stack-driver.md`, `qa-driver.md`, `release-driver.md`) list their tools, and `TaskStop` is not
  among them, so a Driver cannot stop its own background task today. The change adds `TaskStop` to
  their `tools:` line, frontmatter only; the bodies stay identical to Copilot's. The Copilot Driver
  agents' `execute` tool set is taken to include the stop of one's own shell, unproved, and their
  files do not change. This goes past "cards only" in the Chief of Staff's brief, because the card
  rule cannot be followed without it. Settled by the Chief of Staff (spec-writer's proposal, for
  the Chief of Staff to confirm).
- bg-Q9 (why, said once): on Windows a process whose current folder is inside a folder keeps that
  folder from being moved or removed (WinError 32): the move of a CR's folder between stages and
  the removal of a merged CR's worktree at the batch's end fail. And a task left running wakes its
  owner each time it reports, so an ended Driver re-sends its hand-back and the steering session
  wakes for nothing (75 times in batch-24). The rule says this reason in one line. Settled by the
  Chief of Staff.
- bg-Q10 (no CLI change): the CLI cannot see an agent's shells; no new command, no rail, no new
  `status` line. Settled by the Chief of Staff.

- Settled by the Chief of Staff (bg-Q8 confirmed): the four Claude Code Driver agents
  (`agents/cr-driver.md`, `stack-driver.md`, `qa-driver.md`, `release-driver.md`) get
  `TaskStop` in their `tools:` line, frontmatter only; without it the rule cannot be followed and
  no workaround is allowed. The Copilot side stays unproved, named in Known gaps.
- retro-Q3 (the user, 2026-11-17, in their words): "the Driver must start in a worktree of its target
  folder and receive its CR's text one way or another, in the current case (an agentic planning
  surface outside the project)". So the plugin's hook starts a CR Driver in its CR's worktree (the
  code project's worktree), never in the CR folder of the planning surface; the Driver reads its CR
  (request, answers, specification) from the CR folder by its absolute path, named in its prompt,
  and keeps its write guard on both. A `hooks/` change: `just mod` and a hook test are owed. Where
  the worktree does not exist yet at the Driver's start, settle the start folder (the main checkout
  or the project's clone) and say so.
- retro-Q4 (the user, 2026-11-17): before a hand-back, a long gate still running is left to finish:
  the Driver stops only its own background shell that waits on it; the CLI's gate finishes and
  records its pass for the next Driver.

- bg-Q3, revised by retro-Q3: a Driver's shells run from the folder it starts in (below); no shell
  call of a Driver or of the steering session changes its folder (`cd`, `Set-Location`, `pushd`)
  into a CR folder, and the steering session's none into a worktree either. Targets are named
  (`git -C`, absolute paths, `--repo`/`-R`). Settled by the Chief of Staff.
- retro-Q3, the start folder (Claude Code, the plugin's mod): an agent whose prompt holds a
  `writes:` line and a `worktree: <path> branch …` line (a CR Driver's, as `take` and `handoff`
  print it) starts in that worktree when the folder exists. While it does not exist yet (a CR's
  first take: the Driver creates it as its first step), it starts in the project's root that the
  prompt's first line names (`…, in the project <root>.`): the main checkout in-project, the
  project's clone with a planning surface. Neither readable or existing: it starts in its parent's
  folder, still guarded, and the board's note says so. A prompt with a `writes:` line and no
  `worktree:` line (a worker's) starts in its first `writes:` folder as today. The `writes:`
  lines and the guard's folders do not change (the CR folder and the archive path for a CR
  Driver), so no CLI change. A relative path is judged against the folder the agent starts in;
  the Driver writes its CR folder's files by the absolute paths its prompt names (`folder:`,
  `specification:`). Copilot has no mod: its Driver's start folder is the host's, unproved, named
  in Known gaps. Settled by the Chief of Staff.
- bg-Q4, revised by retro-Q4: a long gate still running at a hand-back is not stopped (no
  `gate <cr> --stop`). Today the background shell that runs `$CHANTIER gate` is the gate itself: the
  CLI process waits on the suite there and records the result at its end. Stopping that shell
  would end the CLI process before it records anything. So the Driver leaves that one shell running
  and stops every other background task of its own (the CI watch, a monitor, any shell that only
  waits on or reads the gate). When the gate's end wakes it after its hand-back, it sends nothing
  and ends its turn. Settled by the Chief of Staff, reading the user's answer against the CLI as
  it is (no detached gate exists).
- bg-Q6, refined: the host's notice that an ended Driver waits on its own background work is a
  sign of a leftover task only when `status` shows no `gate running` or `gate queued` for that CR.
  With a gate running, the steering session leaves the Driver alone until the gate ends.
  Settled by the Chief of Staff.
