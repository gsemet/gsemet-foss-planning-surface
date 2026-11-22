# A blocked uv sync names chantier's holders, waits, never kills

Short name: `sync-wait`. Split from `sync-blocked-by-others` (CR-436, sync-lock-Q4): CR-436 is the
launch part (dev mode only for chantier itself), this CR is the wait part. It lands in batch-30
right after CR-436 (`depends.json`: `{"after": ["sync-blocked-by-others"]}`), on CR-436's merged
head, which sits on CR-432's (`permissions-bypass`).

Spec v3 (2026-11-21): v2 (sync-wait-Q6 to Q9, the spec critic's run-1 findings 3 to 7) with the spec
critic's run-2 findings 2 to 7 and sync-wait-Q11.

## Goal

In the user's terms: a dev-mode `uv sync` of chantier's checkout never stops or kills a process
of chantier's, whoever runs it (a gate, a watcher, the board or hub, of any project or surface),
with one exception the user approves each time: the session's own board and watcher. The session
first checks, writing nothing, whether a sync is needed; when it is and processes hold the
checkout's `.venv`, the session names them, goes on unsynced with `sync pending`, tries again at
its next turn, and after 3 minutes tells the user, offering, then or as soon as it holds, to stop
its own board and watcher when they are the only holders.

The evidence (`intake/request.md`): on 2026-11-21 at about 03:33Z the chantier Chief of Staff's
dev-mode sync of the shared checkout stopped Studio's live CR-444 `just preflight` gate (PID 29808)
and its watcher; the gate was re-run (about 4 minutes). The sync rule checked only the Chief of
Staff's own `$CHANTIER status`, which cannot see another surface's processes. Batch-29 had the user
approve killing a Studio gate mid-run for the same reason.

What CR-436 already changes: other projects run the plugin mode (`uvx --from`, uv's cache), so they
no longer hold `<plugin root>/.venv`. Holders remain: chantier's own sessions' commands, gates,
watchers, and a board or hub started from a chantier session (it serves every project of the
surface), plus processes started before CR-436 lands. This CR covers them all the same way.

Every release meets this path: `scripts/version.py` bumps the version in `uv.lock` and prints
`uv.lock changed: sync pending`, so after a release merges the environment is out of date while
the session's own board and watcher hold `.venv`.

## Decisions carried (02-answers.md)

- **sync-wait-Q1 (A).** A sync blocked at a session's start: the session goes on unsynced, with a
  `sync pending` line naming the holders, and syncs later when nothing runs; it never kills another's
  gate. This is a named exception to `startup-core.md`'s "report the exact error and stop".
- **sync-wait-Q2 (A, refined by Q8).** The board and hub, which serve other projects too, are
  waited on like any holder: never stopped to sync without the user's yes; the session offers only
  its own board and watcher. (Today's "stop the board, sync, start the board again", done with no
  question, goes away.)
- **sync-wait-Q3 (A).** The session itself names the holders, with its shell, by its host's text in
  `hosts/`. No new CLI tool (AGENTS.md's measured-cost rule).
- **sync-wait-Q4 (A).** 3 minutes: after that, the user is told, naming the holders; the session
  goes on unsynced and tries again at its next turn.
- **Restatement.** A dev-mode `uv sync` blocked by chantier's own processes (a gate, a watcher, the
  board or hub, any surface's) kills nothing: the session names the holders with its shell, goes on
  unsynced with `sync pending`, tells the user after 3 minutes, tries again at its next turn; the
  startup rule gets this named exception; the shipped-text check covers the SKILL.md sync sentences
  and `startup-core.md`'s exception.
- **Destination (the user's words).** Batch-30, after `sync-blocked-by-others` (CR-436).
- **sync-wait-Q6 (A).** Check first with `uv sync --locked --check`; P10 names its real-path rule
  in the dev mode, in the same P10 question as any other missing rule; the check line in the four
  SKILL.md files is byte-identical to the command inside the rule P10 prints. Exit read in three
  cases: 0 in sync; 1 with "The environment is outdated" the holder steps; any other exit an
  ordinary sync failure, never `sync pending`. A stale `uv.lock` also gives 1 with that text; the
  real sync then fails with its lock error, today's handling.
- **sync-wait-Q7 (A).** Holders looked for before syncing, on every system; the os-error-32 clause
  stays as the net. The listing gets no allow rule: the host row's Mark and the PR's Known gaps say
  it may prompt outside auto or bypass mode, rarely (after a `uv.lock` change).
- **sync-wait-Q8 (A, bounded).** After 3 minutes, when every holder is this session's own board or
  watcher, the session offers once to stop them, sync, and start them again; never while a gate
  runs, never another session's process, never without the user's yes.
- **sync-wait-Q9 (A, refined by Q11).** In a batch, after 3 minutes, one **For you** item `sync
  pending: held by <holders>` in each report while pending (Notes before that), carrying the offer
  until the user answers, and after a no the holders only, plus "a later yes still counts"; outside
  a batch the 3-minute chat line, and at most one more, the offer line when the offer could not be
  in it (Q11); `status-layout.md` keeps "nothing waits on the user" and adds this exception.
- **sync-wait-Q10 (A, a fact).** On a planning surface the board is also the surface's writer; the
  offer's cost reads: "the board and the surface's writer are off for all projects meanwhile; the
  hub too, unless another session's watcher takes it" (spec critic run 2, finding 5: with no
  server running, a watcher of the surface takes the hub's lock).
- **sync-wait-Q11 (A, refines Q9).** When the own-holders condition first holds after the 3-minute
  message, the offer is the For you item's new state in a batch, and outside a batch one more chat
  line, the only one after step 5's; no third line; once per pending sync; it goes out at the
  session's next turn, not on a timer.

## What changes

Paths: `CLI/` is `skills/chantier/scripts/cli/src/chantier/`, `REF/` is
`skills/chantier/references/`, `TESTS/` is `skills/chantier/scripts/cli/tests/`.

**Finding the places.** The Driver works on CR-436's merged head and finds each place by its text
(the function's name, the quoted sentence, the table row), never by a line number: CR-432 and
CR-436 move and rewrite the lines (the line numbers given below are today's main, `3b3eba06`, a
hint only). Where a sentence quoted here is today's text and CR-432 or CR-436 rewrote it, the
Driver edits their text with this CR's intent and keeps their additions word for word ("Overlaps
with CR-432 and CR-436" lists them).

### 1. The sync rule (one text, four SKILL.md files)

The paragraph that begins "`$CHANTIER` is the CLI, one launch in two modes", in
`skills/chantier/SKILL.md`, `skills/chief-of-staff/SKILL.md`, `skills/griller/SKILL.md` and
`skills/status/SKILL.md`, the same text in all four (CR-436's test asserts it).

Its opening words "one launch in two modes, checked once at the session's start" become "one
launch in two modes, its mode checked once at the session's start": "once" is the mode check, not
the sync.

In the dev mode as CR-436 defines it, today's "run `uv sync --locked --project "<plugin root>"`
once, before the first `$CHANTIER` command" becomes the steps below, written once in the paragraph
(compact; the words may be tightened, the steps and the quoted words may not change). They run
before the first `$CHANTIER` command and at each place the cards name a sync (a batch's start,
after a merge that changes `uv.lock`).

1. **Check, writing nothing.** Run `uv sync --locked --check --project "<plugin root>"`. This line,
   with `<plugin root>` filled in, is byte for byte the command inside the rule P10 prints for it
   (section 6). Read its exit:
   - 0 (in sync): nothing to sync, no holder matters, stop here.
   - 1 with uv's text "The environment is outdated": go to step 2.
   - any other exit: an ordinary sync failure, today's handling at that place (at the session's
     start `startup-core.md`; at a batch's start or after a merge, one line to the user with uv's
     text, and you go on); never `sync pending`.
   A stale `uv.lock` also gives 1 with the same text; the real `uv sync --locked` of step 3 then
   fails with its lock error, which keeps today's handling (one sentence in the paragraph says so).
2. **Name the holders, before syncing, on every system.** List the processes that hold
   `<plugin root>/.venv`, by the host's means (the host's reference, row "Name the holders of the
   checkout's environment", section 3).
3. **None: sync.** With no holder, run `uv sync --locked --project "<plugin root>"`.
4. **Any: wait, never kill.** With any holder (a gate, a watcher, the board or hub, of any project
   or surface, the session's own included), or when the sync itself fails with os error 32 (a
   holder the listing missed, or one that started in between; the net kept on Windows): never stop
   or kill a process, ask no one to; go on unsynced, saying `sync pending: held by <holders>` (each
   holder as `PID <n> <subcommand> <project>`, or `an unlisted process` when the listing found
   none), and try again from step 1 at each next turn but a reload (`session-start.md`, "5. Reload":
   a reload runs no `uv sync`).
5. **3 minutes.** When the sync is still pending 3 minutes after its first try, tell the user once,
   naming the holders, that the sync waits for them (in a batch, as the **For you** item of
   `status-layout.md`; outside a batch, one chat line, and at most one more, step 6's offer); then
   go on as in step 4.
6. **Your own board and watcher, on your yes.** At the first try, at or after those 3 minutes,
   where every listed holder is this session's own board or watcher, offer, once per pending sync,
   to stop them, stating the cost: the board and the surface's writer are off for all projects
   meanwhile; the hub too, unless another session's watcher takes it (off a planning surface there
   is no writer, and the cost names the board and the hub only, with the same "unless"). When that
   holds at the 3-minute message, the offer is in that message. When it first holds later (a gate
   held `.venv` at 3 minutes and has ended since), the offer is, in a batch, the For you item's new
   state, and outside a batch, one more chat line, the only one after step 5's. No third line: if a
   gate or another holder appears after the offer, say nothing more; the offer stands for a later
   yes while the conditions hold. "First try" is a turn (step 4's next turn), not a timer: no
   sleep, no monitor, no wake for it.
   "Own" is the host row's evidence (section 3): own board, its command line holds `--seat <this
   session's id>` and this session's `board --seat` did not print `board already running`; own
   watcher, a `watch` process with this project's `--project` while this session holds a running
   watcher task and the project's seat; anything else is not own (another session's board
   included, even on this surface). An own process is stopped by the host's stop of the background
   shell that holds it, never by `Stop-Process`, `taskkill`, `kill` or a PID.
   On the user's yes: stop the watcher and the board, list the holders again, sync only if none,
   then start the board and the watcher again whatever the result (`session-start.md`'s board
   start, and the watcher's printed command, as is). A holder still listed after the stop is no
   longer own (its shell is gone): it is waited on as in step 4, never killed; the board's restart
   then meets `board already running`, passed on as is. The user's yes covers the restart: no
   second question; the board's start lines are handled as `session-start.md` says. A failed sync
   is one line with uv's text.
   No offer while another holder is listed or a gate runs (listed, or shown by `$CHANTIER
   status`). No answer: the offer stands (in a batch, the For you item keeps carrying it). A no:
   keep waiting as in step 4, do not ask again; in a batch the For you item then names the holders
   only, plus "a later yes still counts". A later yes from the user counts, if the conditions
   still hold.
   The paragraph holds the words "on your yes", "own board and watcher" and "No third line".

Only the steering session syncs, never a Foreman, a Driver or a worker (unchanged). The sentence
"Any failure of the sync or of `$CHANTIER`, in either mode, at any call, follows `startup-core.md`"
stays word for word (`TESTS/test_cli_stop.py` asserts it), followed by: ", except a sync held as
above (`sync pending`)". A CLI that then cannot start on the unsynced environment is
`startup-core.md`'s stop, and the report names the holders.

### 2. `startup-core.md`: the named exception

`REF/startup-core.md`, at the end of its first paragraph (the one holding "report the exact error and
stop"; `TESTS/test_startup_manifest.py`'s `test_the_rules_that_must_not_be_missed_come_first` wants
"No fallback" to stay the second paragraph), one sentence:

> One named exception: in the dev mode, a `uv sync` that chantier's own processes block (they hold
> the checkout's `.venv`; os error 32 on Windows) is not a launch failure: the session goes on
> unsynced with `sync pending`, as the `$CHANTIER` paragraph of its skill says, and stops nothing
> that paragraph does not name.

The startup bytes stay under `STARTUP_LIMIT` (12 544; today's highest, the Chief of Staff on
Copilot, is 9 126 before CR-432 and CR-436 add theirs). The SKILL.md paragraph is not in the
startup bytes.

### 3. The host text: naming the holders (Q3, Q7)

One row in each host's Tools table, "Name the holders of the checkout's environment":

- `REF/hosts/claude-code.md`, `## Tools` (columns Generic, Claude Code, Mark): on Windows, the
  PowerShell tool: `Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -like '<plugin
  root with backslashes>\.venv\*' } | Select-Object ProcessId, ParentProcessId, CommandLine`; on
  macOS and Linux, the Bash tool: `ps -eo pid,ppid,args | grep -F "<plugin root>/.venv/"` (the grep
  line itself excluded). Reading: a `chantier.exe` and its child `python.exe` are one holder, named
  by the top process's PID, its subcommand (`board`, `watch`, `gate`, `status`...) and its
  `--project` value, from its command line. "Own", by its evidence: own board = its command line
  holds `--seat <this session's id>` and this session's `board --seat` did not print `board already
  running`; own watcher = a `watch` process with this project's `--project` while this session
  holds a running watcher task and the project's seat; anything else is not own. Read-only; never `Stop-Process`, `taskkill` or `kill` on a
  holder. Mark: the Windows listing exercised on 2026-11-21 by this CR's v1 spec-writer on the
  user's Windows machine (it listed a Studio board, a Studio watcher, chantier's watcher and a Studio
  command, each a `chantier.exe` with its `python.exe` child, both under `.venv\Scripts`); the macOS
  and Linux listing untested; no allow rule (a path-bearing pipeline rule is unproved), so it may
  prompt outside auto or bypass mode, rarely (only after a `uv.lock` change, since the check comes
  first); a process holding a `.venv` file without running from `.venv` is not listed (then step
  4's `an unlisted process`); on macOS and Linux a gate started between the listing and the sync is
  not caught (no os error 32 there).
- `REF/hosts/copilot.md`, `## Tools` (columns Generic, Copilot; no Mark column): the same commands
  through the host's shell tool, the Copilot cell ending "untested".
- The "synced once" places, all on CR-432's and CR-436's text, take the `uv` row's new words, "after
  the steering session's checked sync, which waits for holders (the skill's `$CHANTIER`
  paragraph)", in place of "after one `uv sync --locked --project`... by the steering session" or
  "synced once":
  - `REF/hosts/claude-code.md`, the `uv` row of the tools table (today line 218).
  - `REF/hosts/claude-code.md`, "Capabilities and their commands", the "Every batch" row's commands
    cell (today line 381), "after one `uv sync --locked --project <checkout>` by the steering
    session".
  - `REF/hosts/claude-code.md`, "Allow rules", the sync rule's row (today line 268, CR-432's
    real-path form): "the steering session's one sync of chantier's own checkout" becomes "the
    steering session's checked sync of chantier's own checkout, which waits for holders".
  - `REF/concepts.md`, the `$CHANTIER` word (today line 416): "the environment synced once by the
    steering session with `uv sync --locked --project "<…>"`".
  - `CONTRIBUTING.md`, "A CLI" (today line 76): "after one `uv sync --locked --project "<root>"` by
    the steering session".
  - `CONTRIBUTING.md`, the paragraph "In this checkout, `$CHANTIER` runs the local code, live"
    (today line 225, "synced once by the steering session"), with section 5's sentence.

### 4. The Chief of Staff's sync places

`REF/chief-of-staff.md`:

- **Starting a batch, step 1** ("In chantier's own checkout (the dev mode), first sync: stop the
  board (the host's stop of its background shell), run `uv sync ...`, then start the board again
  ... A sync that fails is one line to the user with uv's text, and you go on."): becomes "In the
  dev mode, first the sync as your skill's `$CHANTIER` paragraph says (check, name the holders, sync
  only with none; your own board and watcher are stopped only on the user's yes, after 3 minutes);
  a pending sync never blocks the go, and the plan says `sync pending: held by ...`. A sync that
  fails otherwise is one line to the user with uv's text, and you go on." "Only you sync, never a
  Foreman, a Driver or a worker" stays.
- **The fast-forward paragraph** ("On that note (yours or the Foreman's), in chantier's own
  checkout, sync once `$CHANTIER status` shows no gate running: stop the board, `uv sync ...`, start
  the board again; until then say `sync pending` in your report's Notes."): becomes "On that note
  (yours or the Foreman's), in the dev mode, sync as your skill's `$CHANTIER` paragraph says, at
  this turn and each next one until it is done; `$CHANTIER status` is not enough, it sees only this
  surface's batch; until then say `sync pending: held by ...` in your report's Notes; after 3
  minutes, it is a For you item (`status-layout.md`)."
- One sentence in the same paragraph: "Never stop or kill a holder to sync, nor ask a Foreman or a
  Driver to; the one exception is your own board and watcher, on the user's yes, as the skill's
  paragraph says."

`REF/foreman.md`: unchanged (the Foreman never syncs; its `uv.lock changed: sync pending` note
stays).

`REF/status-layout.md`, the `main checkout:` paragraph:

- The **Notes** line ("with `; uv.lock changed: sync pending` while the sync waits"): "while the
  sync waits, then `sync pending: held by <holders>` when holders were named".
- "It is not a **For you** item: nothing waits on the user" stays word for word, followed by: "but
  a sync pending more than 3 minutes: then one **For you** item, `sync pending: held by <holders>`,
  with the offer to stop your own board and watcher when they are the only holders (from the
  3-minute report, or from the first report where that holds), until the user answers; after a no,
  the holders only, plus "a later yes still counts"; or what the user may stop otherwise." Then:
  one item, its latest state, in each Progress and Completion report while the sync is pending,
  gone once synced, never a second chat question; outside a batch, the skill's chat line, and its
  one offer line when the offer could not be in it. The rest of the paragraph (the `tracked changes` and `on <branch>` sentence)
  stays.

### 5. Docs

- `AGENTS.md`, the bullet "The CLI is one Python package..." (CR-436 rewrote it): after "`uv sync
  --locked --project` once at the moments the cards name (...)", add "; it checks first, and a sync
  that chantier's own processes block names them and waits, never stopping or killing one but the
  session's own board and watcher on the user's yes (the cards)". If CR-436 kept "once" there, it
  becomes "at the moments the cards name".
- `CONTRIBUTING.md`, the paragraph "In this checkout, `$CHANTIER` runs the local code, live" (CR-436
  rewrote it): after "so a running board or gate never holds a file a command needs to rewrite (os
  error 32 on Windows)", add one sentence: "the sync itself runs only when the environment is out of
  date and no chantier process holds it; otherwise the session goes on unsynced with `sync pending`
  and stops nothing, but its own board and watcher on the user's yes".

### 6. The CLI and P10: the check's allow rule (Q6)

The check line is a new command form; CR-432's exact real-path sync rule
(`uv sync --locked --project "<checkout>"`, no wildcard) does not match it. So:

- `CLI/plugin_files.py`: beside CR-432's sync-line function, one for the check line,
  `uv sync --locked --check --project "<plugin root>"`, and its rule, built the same way (CR-432's
  quoting, per its trial). A `sync_check_command(repo: Repo | None)` returns it under the same
  condition as CR-436's `sync_command(repo)` (`is_dev_checkout()` and `is_chantier_project(repo)`),
  else None. Its text is the SKILL.md line with `<plugin root>` filled in, byte for byte.
- `CLI/commands/permissions.py`: in the dev mode (CR-436's mode helper), the check line is one more
  dev sample and its rule one more dev rule: P10 names it missing in the same question as any other
  missing rule (no question of its own), it counts in CR-432's replacing-rule logic like any dev
  sample (a broad `uv sync *` lets it through, so its replacing rules include it; `uv sync --locked
  --project *` does not), and it is stale only when its folder is gone, as CR-432 says of dev-form
  rules. Plugin mode: unchanged, never named.
- `REF/hosts/claude-code.md`, "Allow rules": one row for the check rule (Bash and PowerShell), beside
  CR-432's sync rule, what it allows ("the steering session's read-only check before a sync, the dev
  mode"), its risk ("none: writes nothing"), Mark documented (rule form) plus the Driver's trial
  result (Evidence); the pasteable block, the "Every batch" row of "Capabilities and their
  commands", and "Allow rules to add" carry it too, in CR-432's real-path form. No row for the
  holder listing (Q7).
- `REF/chief-of-staff.md`, "The allow rules (P10, Claude Code)": unchanged; the check rule is one of
  the rules P10 names, joined to the same P10 question.

### Overlaps with CR-432 and CR-436 (on their merged heads)

- The `$CHANTIER` paragraph of the four SKILL.md files: CR-432 adds the `<plugin root>` path
  sentence, CR-436 the second dev-mode condition; both kept word for word; this CR edits only the
  opening "checked once" words, the sync sentences and appends the exception clause, the four
  paragraphs staying identical (CR-436's test).
- `CLI/plugin_files.py`: CR-432's per-form and rule functions, CR-436's `is_chantier_project`; this
  CR adds the check line's form and rule and `sync_check_command`, touching neither.
- `CLI/commands/permissions.py`: CR-432's samples, probes, replacing and stale rules, CR-436's mode
  helper; this CR adds one dev sample and rule.
- `REF/hosts/claude-code.md`: CR-432's allow-rule rows, block and "Allow rules to add", CR-436's
  mode words in the `uv` and "Every batch" rows; this CR adds a row and the Tools row, and edits the
  sync words of the `uv`, "Every batch" and sync-rule rows only.
- `REF/concepts.md` and `CONTRIBUTING.md`'s "A CLI": CR-436's mode words kept; this CR edits the
  sync words only.
- `REF/chief-of-staff.md`: CR-436's "(the dev mode)" words in step 1 and the fast-forward
  paragraph; this CR rewrites the sync behaviour around them. CR-432's P10 bullets untouched.
- `AGENTS.md` and `CONTRIBUTING.md`: CR-436's rewritten sentences and its Q12 sentence kept; this CR
  appends.
- `TESTS/test_cli_runs.py`: CR-432's mode-parametrized P10 tests, CR-436's "dev" case with a chantier
  `Repo`: the dev case also expects the check rule.

## Out of scope

- A CLI command that lists the holders (sync-wait-Q3: the session's shell does it).
- An allow rule for the holder listing (sync-wait-Q7).
- Any stop, kill or restart of a chantier process to sync, by the session, a Foreman or a Driver,
  but the session's own board and watcher, by the host's stop of their shells, on the user's yes
  (sync-wait-Q8).
- Who syncs (the steering session only) and the plugin mode, which never syncs.
- The P5 Windows tail's wording in `commands/preflight.py`.
- The launch rule and the foreign-build notice (CR-436; `surface-server-foreign-build`).
- A waiting loop inside one turn: the session tries again at its next turn, it does not sleep.

## Host and default matrix

The rule applies only in the dev mode (CR-436's); the plugin mode is untouched on every host.

| Cell | Naming the holders | Blocked sync | P10 check rule |
| --- | --- | --- | --- |
| Claude Code, Windows | PowerShell `Get-CimInstance` listing: exercised 2026-11-21 (spec-writer); may prompt outside auto or bypass mode | listed before syncing; os error 32 the net: step 4; the host's stop ending an own shell's `chantier.exe` and its `python.exe` child: unproved | named in the dev mode, in the one P10 question |
| Claude Code, macOS or Linux | `ps ... grep -F`: untested; may prompt outside auto or bypass mode | listed before syncing; no os error 32, so a gate started between the listing and the sync is not caught (Known gaps) | named in the dev mode, in the one P10 question |
| Copilot, Windows | shell tool, the same listing: untested | as for Claude Code, Windows | no P10 |
| Copilot, macOS or Linux | shell tool, `ps`: untested | as for Claude Code, macOS or Linux | no P10 |
| Any host, plugin mode (any project but chantier, or no `.git`) | not run | no sync | not named |

## Evidence

Checks read the shipped files from the repository as they ship, at the head under test.

- A shipped-text test (in `TESTS/test_cli_stop.py` beside CR-363's, or `TESTS/test_plugin_files.py`
  beside CR-436's paragraph test), reading the four shipped SKILL.md files: the `$CHANTIER`
  paragraph holds "its mode checked once", `uv sync --locked --check --project "<plugin root>"`,
  "The environment is outdated", "never stop or kill", `sync pending: held by`, "3 minutes", "but a
  reload", "on your yes", "own board and watcher", "No third line", "no second question", "is no
  longer own", "unless another session's watcher takes it" and the host row's name, and keeps "Any failure of
  the sync or of `$CHANTIER`, in either mode, at any call, follows `startup-core.md`" followed by the
  exception clause.
- The same test reads `REF/startup-core.md` (the exception sentence is in its first paragraph,
  which still holds "report the exact error and stop"); `REF/hosts/claude-code.md` and
  `REF/hosts/copilot.md` (the row "Name the holders of the checkout's environment" with the listing
  commands, and its "Own" evidence holding `--seat <this session's id>` and `board already
  running`); `REF/chief-of-staff.md` (the sentence "the one exception is your own board and watcher,
  on the user's yes"); and `REF/status-layout.md` (the exception sentence "but a sync pending more
  than 3 minutes", with "until the user answers" and "a later yes still counts", in the paragraph
  that still holds "It is not a **For you** item: nothing waits on the user").
- Byte identity (Q6): a test in `TESTS/test_plugin_files.py` takes the check line from the shipped
  `skills/chief-of-staff/SKILL.md`, fills in `<plugin root>` with the dev cell's root, and asserts it
  equals `sync_check_command(repo)` and the command inside the rule P10 prints for it (Bash and
  PowerShell forms).
- `TESTS/test_startup_manifest.py`'s moved-rule test (`test_moved_rule_is_gone_from_where_it_was`):
  "stop the board (the host's stop of its background shell), run `uv sync" and "sync once
  `$CHANTIER status` shows no gate running" are gone from `REF/chief-of-staff.md`; "synced once by
  the steering session" is gone from `REF/concepts.md`. Its startup-bytes test stays green.
- `TESTS/test_plugin_files.py`, CR-436's `command_for` cells: `sync_check_command(repo)` gives the
  check line in the dev cells and None in the plugin cells, `repo` None included.
- `TESTS/test_cli_runs.py`, the P10 tests: the dev case names the check rule (missing, then present)
  in the same P10 output as the other missing rules; a broad `uv sync *` names it among its
  replacing rules; the plugin case and the "another project from a `.git` root" case never name it.
- The check's trial, by hand, once, on a throwaway project outside the repository (in the
  scratchpad): `uv sync --locked`, then `uv sync --locked --check` (expect 0); then a version bump
  as `scripts/version.py` makes it (the version in `pyproject.toml` and in `uv.lock`'s own
  package), then `uv sync --locked --check` again (expect 1 with "The environment is outdated");
  then a stale `uv.lock` (a dependency added to `pyproject.toml` only: expect 1, and the real
  `uv sync --locked` failing with its lock error). The uv version and the three results go in the
  check rule's Allow rules row's Mark (section 6) and in the PR. The advisor's measure (uv 0.13.6,
  Windows: 0 in sync, 1 out of date, 1 with a stale `uv.lock`) is the expectation, not the proof.
- The scenario: its sandbox project is not chantier (plugin mode since CR-436), so it never syncs;
  no scenario step.
- The PR's **Known gaps** names: the session's behaviour (checking, naming, waiting, the 3-minute
  For you item or line, or the later offer line) and the stop, sync and restart of its own board
  and watcher are card behaviour with no automated proof, and every release bump (`scripts/version.py` prints
  `uv.lock changed: sync pending`) meets this path, so the first release after the merge is its
  first live proof; the holder listing has no allow rule and may prompt outside auto or bypass
  mode, rarely (after a `uv.lock` change); on macOS and Linux a gate started between the listing
  and the sync is not caught; the macOS, Linux and Copilot listings are untested; whether the
  host's stop of a background shell ends its process tree (on Windows the `chantier.exe` and its
  `python.exe` child) is unproved (`REF/hosts/claude-code.md`, rows "Stop a background task of
  one's own" and "Run the board", today lines 38 and 48), so a holder may stay listed after the
  stop (step 6: waited on, never killed).
- Gates owed (`AGENTS.md`): `just check`, `just test` within its budget, `just eval-dry-run` (the
  CLI's `src/` changes), the pipeline's `just scenario (ubuntu-latest)` job at the PR's head; as the
  top CR of batch-30 while it is, `chantier gate` locally. No `hooks/` or `types/` change.
