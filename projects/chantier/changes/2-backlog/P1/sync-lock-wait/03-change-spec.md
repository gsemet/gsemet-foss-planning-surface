# A blocked uv sync names chantier's holders, waits, never kills

Short name: `sync-wait`. Split from `sync-blocked-by-others` (CR-436, sync-lock-Q4): CR-436 is the
launch part (dev mode only for chantier itself), this CR is the wait part. It lands in batch-30
right after CR-436 (`depends.json`: `{"after": ["sync-blocked-by-others"]}`), on CR-436's merged
head, which sits on CR-432's (`permissions-bypass`).

Spec v1 (2026-11-21).

## Goal

In the user's terms: a dev-mode `uv sync` of chantier's checkout never stops or kills a process
of chantier's, whoever runs it (a gate, a watcher, the board or hub, of any project or surface).
When such processes hold the checkout's `.venv`, the session names them, goes on unsynced with
`sync pending`, tries again at its next turn, and tells the user after 3 minutes.

The evidence (`intake/request.md`): on 2026-11-21 at about 03:33Z the chantier Chief of Staff's
dev-mode sync of the shared checkout stopped Studio's live CR-444 `just preflight` gate (PID 29808)
and its watcher; the gate was re-run (about 4 minutes). The sync rule checked only the Chief of
Staff's own `$CHANTIER status`, which cannot see another surface's processes. Batch-29 had the user
approve killing a Studio gate mid-run for the same reason.

What CR-436 already changes: other projects run the plugin mode (`uvx --from`, uv's cache), so they
no longer hold `<plugin root>/.venv`. Holders remain: chantier's own sessions' commands, gates,
watchers, and a board or hub started from a chantier session (it serves every project of the
surface), plus processes started before CR-436 lands. This CR covers them all the same way.

## Decisions carried (02-answers.md)

- **sync-wait-Q1 (A).** A sync blocked at a session's start: the session goes on unsynced, with a
  `sync pending` line naming the holders, and syncs later when nothing runs; it never kills another's
  gate. This is a named exception to `startup-core.md`'s "report the exact error and stop".
- **sync-wait-Q2 (A).** The board and hub, which serve other projects too, are waited on like any
  holder: never stopped to sync. The session's own watcher is never stopped either. (Today's "stop
  the board, sync, start the board again" goes away.)
- **sync-wait-Q3 (A).** The session itself names the holders, with its shell, by its host's text in
  `hosts/`. No new CLI tool (AGENTS.md's measured-cost rule).
- **sync-wait-Q4 (A).** 3 minutes: after that, one line to the user naming the holders; the session
  goes on unsynced and tries again at its next turn.
- **Restatement.** A dev-mode `uv sync` blocked by chantier's own processes (a gate, a watcher, the
  board or hub, any surface's) kills nothing: the session names the holders with its shell, goes on
  unsynced with `sync pending`, tells the user after 3 minutes, tries again at its next turn; the
  startup rule gets this named exception; the shipped-text check covers the SKILL.md sync sentences
  and `startup-core.md`'s exception.
- **Destination (the user's words).** Batch-30, after `sync-blocked-by-others` (CR-436).
- Open questions 1 and 2 below are built as their option A (the user asked no questions tonight:
  "plus de question. demande a un agent fable").

## What changes

Paths: `CLI/` is `skills/chantier/scripts/cli/src/chantier/`, `REF/` is
`skills/chantier/references/`, `TESTS/` is `skills/chantier/scripts/cli/tests/`.

**Finding the places.** The Driver works on CR-436's merged head and finds each place by its text
(the function's name, the quoted sentence, the table row), never by a line number: CR-432 and
CR-436 move and rewrite the lines. Where a sentence quoted here is today's text and CR-432 or
CR-436 rewrote it, the Driver edits their text with this CR's intent and keeps their additions
word for word ("Overlaps with CR-432 and CR-436" lists them).

### 1. The sync rule (one text, four SKILL.md files)

The paragraph that begins "`$CHANTIER` is the CLI, one launch in two modes", in
`skills/chantier/SKILL.md`, `skills/chief-of-staff/SKILL.md`, `skills/griller/SKILL.md` and
`skills/status/SKILL.md`, the same text in all four (CR-436's test asserts it). In the dev mode as
CR-436 defines it, today's "run `uv sync --locked --project "<plugin root>"` once, before the first
`$CHANTIER` command" becomes the steps below, written once in the paragraph (compact; the words may
be tightened, the steps may not change):

1. **Check, writing nothing.** Run `uv sync --locked --check --project "<plugin root>"` (open
   question 1). When it says the environment is in sync (exit 0, "Would make no changes"), there is
   nothing to sync: no holder matters, nothing more is done.
2. **Name the holders.** When it says the environment is out of date, list the processes that hold
   `<plugin root>/.venv`, by the host's means (the host's reference, row "Name the holders of the
   checkout's environment", section 3).
3. **None: sync.** With no holder, run `uv sync --locked --project "<plugin root>"`.
4. **Any: wait, never kill.** With any holder (a gate, a watcher, the board or hub, of any project
   or surface, the session's own included), or when the sync itself fails with os error 32 (a holder
   the listing missed, or one that started in between): never stop or kill a process, ask no one to
   kill it; go on unsynced, saying `sync pending: held by <holders>` (each holder as
   `PID <n> <subcommand> <project>`, or `an unlisted process` when the listing found none), and try
   again from step 1 at each next turn.
5. **3 minutes.** When the sync is still pending 3 minutes after its first try, tell the user once,
   in one line naming the holders, that the sync waits for them (only the user stops one); then go on
   as in step 4.

Only the steering session syncs, never a Foreman, a Driver or a worker (unchanged). The sentence
"Any failure of the sync or of `$CHANTIER`, in either mode, at any call, follows `startup-core.md`"
stays word for word (`TESTS/test_cli_stop.py` asserts it), followed by: ", except a sync held as
above (`sync pending`)". A CLI that then cannot start on the unsynced environment is
`startup-core.md`'s stop, and the report names the holders. Another sync failure (not os error 32)
keeps today's handling.

### 2. `startup-core.md`: the named exception

`REF/startup-core.md`, at the end of its first paragraph (the one holding "report the exact error and
stop"; `TESTS/test_startup_manifest.py`'s `test_the_rules_that_must_not_be_missed_come_first` wants
"No fallback" to stay the second paragraph), one sentence:

> One named exception: in the dev mode, a `uv sync` that chantier's own processes block (they hold
> the checkout's `.venv`; os error 32 on Windows) is not a launch failure: the session goes on
> unsynced with `sync pending`, as the `$CHANTIER` paragraph of its skill says, and kills nothing.

The startup bytes stay under `STARTUP_LIMIT` (12 544; today's highest, the Chief of Staff on
Copilot, is 9 126 before CR-432 and CR-436 add theirs).

### 3. The host text: naming the holders (Q3)

One row in each host's Tools table, "Name the holders of the checkout's environment":

- `REF/hosts/claude-code.md`, `## Tools`: on Windows, the PowerShell tool:
  `Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -like '<plugin root with
  backslashes>\.venv\*' } | Select-Object ProcessId, ParentProcessId, CommandLine`; on macOS and
  Linux, the Bash tool: `ps -eo pid,ppid,args | grep -F "<plugin root>/.venv/"` (the grep line
  itself excluded). Reading: a `chantier.exe` and its child `python.exe` are one holder, named by the
  top process's PID, its subcommand (`board`, `watch`, `gate`, `status`...) and its `--project`
  value, from its command line. Read-only; never `Stop-Process`, `taskkill` or `kill` on a holder.
  Mark: the Windows listing exercised on 2026-11-21 by this CR's spec-writer on the user's Windows
  machine (it listed a Studio board, a Studio watcher, chantier's watcher and a Studio command, each a
  `chantier.exe` with its `python.exe` child, both under `.venv\Scripts`); the macOS and Linux
  listing untested; a process holding a `.venv` file without running from `.venv` is not listed
  (then step 4's `an unlisted process`).
- `REF/hosts/copilot.md`, `## Tools`: the same commands through the host's shell tool; Mark
  untested.
- `REF/hosts/claude-code.md`, the `uv` row of the tools table (CR-436's text): "after one
  `uv sync --locked --project` by the steering session" becomes "after the steering session's
  sync, which waits for holders and never kills one".

### 4. The Chief of Staff's sync places

`REF/chief-of-staff.md`:

- **Starting a batch, step 1** ("In chantier's own checkout (the dev mode), first sync: stop the
  board (the host's stop of its background shell), run `uv sync ...`, then start the board again
  ... A sync that fails is one line to the user with uv's text, and you go on."): becomes "In the
  dev mode, first the sync as your skill's `$CHANTIER` paragraph says (check, name the holders, sync
  only with none, never stop the board, a watcher or a gate); a pending sync never blocks the go, and
  the plan says `sync pending: held by ...`. A sync that fails otherwise is one line to the user
  with uv's text, and you go on." "Only you sync, never a Foreman, a Driver or a worker" stays.
- **The fast-forward paragraph** ("On that note (yours or the Foreman's), in chantier's own
  checkout, sync once `$CHANTIER status` shows no gate running: stop the board, `uv sync ...`, start
  the board again; until then say `sync pending` in your report's Notes."): becomes "On that note
  (yours or the Foreman's), in the dev mode, sync as your skill's `$CHANTIER` paragraph says, at
  this turn and each next one until it is done; `$CHANTIER status` is not enough, it sees only this
  surface's batch; until then say `sync pending: held by ...` in your report's Notes." The 3-minute
  line of step 5 applies here too.
- One sentence in the same paragraph: never stop or kill a holder to sync, nor ask a Foreman or a
  Driver to; only the user stops one.

`REF/foreman.md`: unchanged (the Foreman never syncs; its `uv.lock changed: sync pending` note
stays).

`REF/status-layout.md`, the **Notes** line on `main checkout:` ("with `; uv.lock changed: sync
pending` while the sync waits"): "while the sync waits, then `sync pending: held by <holders>`
when holders were named".

### 5. Docs

- `AGENTS.md`, the bullet "The CLI is one Python package..." (CR-436 rewrote it): after "`uv sync
  --locked --project` once at the moments the cards name (...)", add "; a sync that chantier's own
  processes block names them and waits, never stopping or killing one (the cards)".
- `CONTRIBUTING.md`, the paragraph "In this checkout, `$CHANTIER` runs the local code, live" (CR-436
  rewrote it): after "so a running board or gate never holds a file a command needs to rewrite (os
  error 32 on Windows)", add one sentence: "the sync itself runs only when the environment is out of
  date and no chantier process holds it; otherwise the session goes on unsynced with `sync pending`
  and kills nothing".

### 6. The CLI and P10: the check's allow rule (open question 1, A)

The check line is a new command form; CR-432's exact real-path sync rule
(`uv sync --locked --project "<checkout>"`, no wildcard) does not match it. So:

- `CLI/plugin_files.py`: beside CR-432's sync-line function, one for the check line,
  `uv sync --locked --check --project "<plugin root>"`, and its rule, built the same way (CR-432's
  quoting, per its trial). A `sync_check_command(repo: Repo | None)` returns it under the same
  condition as CR-436's `sync_command(repo)` (`is_dev_checkout()` and `is_chantier_project(repo)`),
  else None.
- `CLI/commands/permissions.py`: in the dev mode (CR-436's mode helper), the check line is one more
  dev sample and its rule one more dev rule: P10 names it missing like the sync rule, it counts in
  CR-432's replacing-rule logic like any dev sample (a broad `uv sync *` lets it through, so its
  replacing rules include it; `uv sync --locked --project *` does not), and it is stale only when its
  folder is gone, as CR-432 says of dev-form rules. Plugin mode: unchanged, never named.
- `REF/hosts/claude-code.md`, "Allow rules": one row for the check rule (Bash and PowerShell), beside
  CR-432's sync rule, what it allows ("the steering session's read-only check before a sync, the dev
  mode"), its risk ("none: writes nothing"), Mark documented (rule form); the pasteable block, the
  "Every batch" row of "Capabilities and their commands", and "Allow rules to add" carry it too, in
  CR-432's real-path form.
- `REF/chief-of-staff.md`, "The allow rules (P10, Claude Code)": unchanged; the check rule is one of
  the rules P10 names. A chantier session already set up gets one P10 question for it, once.

### Overlaps with CR-432 and CR-436 (on their merged heads)

- The `$CHANTIER` paragraph of the four SKILL.md files: CR-432 adds the `<plugin root>` path
  sentence, CR-436 the second dev-mode condition; both kept word for word; this CR edits only the
  sync sentences and appends the exception clause, the four paragraphs staying identical (CR-436's
  test).
- `CLI/plugin_files.py`: CR-432's per-form and rule functions, CR-436's `is_chantier_project`; this
  CR adds the check line's form and rule and `sync_check_command`, touching neither.
- `CLI/commands/permissions.py`: CR-432's samples, probes, replacing and stale rules, CR-436's mode
  helper; this CR adds one dev sample and rule.
- `REF/hosts/claude-code.md`: CR-432's allow-rule rows, block and "Allow rules to add", CR-436's
  mode words in the `uv` and "Every batch" rows; this CR adds a row and the Tools row, and edits the
  `uv` row's sync words only.
- `REF/chief-of-staff.md`: CR-436's "(the dev mode)" words in step 1 and the fast-forward
  paragraph; this CR rewrites the sync behaviour around them. CR-432's P10 bullets untouched.
- `AGENTS.md` and `CONTRIBUTING.md`: CR-436's rewritten sentences and its Q12 sentence kept; this CR
  appends.
- `TESTS/test_cli_runs.py`: CR-432's mode-parametrized P10 tests, CR-436's "dev" case with a chantier
  `Repo`: the dev case also expects the check rule.

## Out of scope

- A CLI command that lists the holders (sync-wait-Q3: the session's shell does it).
- Any stop, kill or restart of a chantier process to sync, by the session, a Foreman or a Driver.
- Who syncs (the steering session only) and the plugin mode, which never syncs.
- The P5 Windows tail's wording in `commands/preflight.py`.
- The launch rule and the foreign-build notice (CR-436; `surface-server-foreign-build`).
- A waiting loop inside one turn: the session tries again at its next turn, it does not sleep.

## Host and default matrix

The rule applies only in the dev mode (CR-436's); the plugin mode is untouched on every host.

| Cell | Naming the holders | Blocked sync | P10 check rule |
| --- | --- | --- | --- |
| Claude Code, Windows | PowerShell `Get-CimInstance` listing: exercised 2026-11-21 (spec-writer) | os error 32: step 4 | named in the dev mode |
| Claude Code, macOS or Linux | `ps ... grep -F`: untested | no os error 32; the check and the listing still keep a sync off a running gate | named in the dev mode |
| Copilot, Windows | shell tool, the same listing: untested | step 4 | no P10 |
| Copilot, macOS or Linux | shell tool, `ps`: untested | as for Claude Code | no P10 |
| Any host, plugin mode (any project but chantier, or no `.git`) | not run | no sync | not named |

## Evidence

Checks read the shipped files from the repository as they ship, at the head under test.

- A shipped-text test (in `TESTS/test_cli_stop.py` beside CR-363's, or `TESTS/test_plugin_files.py`
  beside CR-436's paragraph test), reading the four shipped SKILL.md files: the `$CHANTIER`
  paragraph names `uv sync --locked --check --project`, "never stop or kill", `sync pending: held
  by`, "3 minutes" and the host row's name, and keeps "Any failure of the sync or of `$CHANTIER`, in
  either mode, at any call, follows `startup-core.md`" followed by the exception clause.
- The same test reads `REF/startup-core.md`: the exception sentence is in its first paragraph, which
  still holds "report the exact error and stop"; and `REF/hosts/claude-code.md` and
  `REF/hosts/copilot.md` hold the row "Name the holders of the checkout's environment" with the
  listing commands.
- `TESTS/test_startup_manifest.py`'s moved-rule test (`test_moved_rule_is_gone_from_where_it_was`):
  "stop the board (the host's stop of its background shell), run `uv sync" and "sync once
  `$CHANTIER status` shows no gate running" are gone from `REF/chief-of-staff.md`. Its startup-bytes
  test stays green.
- `TESTS/test_plugin_files.py`, CR-436's `command_for` cells: `sync_check_command(repo)` gives the
  check line in the dev cells and None in the plugin cells, `repo` None included.
- `TESTS/test_cli_runs.py`, the P10 tests: the dev case names the check rule (missing, then present);
  a broad `uv sync *` names it among its replacing rules; the plugin case and the "another project
  from a `.git` root" case never name it.
- `uv sync --locked --check`'s exit when the environment is out of date (expected non-zero, read
  from its text): the Driver tries it once by hand on a throwaway project and writes the result in
  the host row's Mark and the PR; exit 0 with holders running is exercised (this spec, 2026-11-21).
- The scenario: its sandbox project is not chantier (plugin mode since CR-436), so it never syncs;
  no scenario step. The session's behaviour (naming, waiting, the 3-minute line) is card behaviour,
  proved by no automated check; the PR's Known gaps says so, and that a real dev-mode session with a
  holder running is the first live proof.
- Gates owed (`AGENTS.md`): `just check`, `just test` within its budget, `just eval-dry-run` (the
  CLI's `src/` changes), the pipeline's `just scenario (ubuntu-latest)` job at the PR's head; as the
  top CR of batch-30 while it is, `chantier gate` locally. No `hooks/` or `types/` change.

## Open questions for the user

Built as A unless the user says otherwise.

1. **How the session knows a sync is needed, with its own board running.** A sync with the session's
   own board up is always held (Q2), so a blind sync at each batch start would always be pending.
   - **A (built).** Check first with `uv sync --locked --check`, which writes nothing; only an
     out-of-date environment leads to the holders and the sync; P10 names the check's real-path rule
     in the dev mode (one more question once).
   - B. The same check, with no P10 rule: the host's prompt or auto mode decides (unproved).
   - C. No check: name the holders and sync only with none; every batch start with a board up says
     `sync pending`.
2. **Look before syncing, or only after a failed sync.**
   - **A (built).** Look before (Studio's proposal): a sync with holders is not started, so a running
     gate is never touched mid-run, on every system; a failed sync with os error 32 is handled the
     same way.
   - B. Sync first, name the holders only when it fails with os error 32 (Windows only; a POSIX sync
     may replace files under a running gate).
