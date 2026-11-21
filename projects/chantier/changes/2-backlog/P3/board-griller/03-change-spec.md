# A Griller started from the web board

Spec v1 (2026-11-21). Short name: `board-griller`. Destination: batch-30 (ui-night). Built on the
user's directions of 2026-11-17 and of the UI night (2026-11-21, "Tout"), then on board-griller-Q1
to Q17, answered by a Fable advisor in the user's place. **board-griller-Q4 (the security boundary)
is the user's and still open**: this specification is built on its option A and lists it first
under "Open questions".

## Goal

From the web board, on an inbox, backlog or ready item, the user opens a discussion with a Griller
and grills that CR without a desktop session: the user types, a Griller answers, and the Griller
records the grill in the CR's folder as its card says. The surface server runs the user's own
headless CLI of this machine's host, one run per message, under tight limits; a turn that wrote in
the CR's folder wakes the Chief of Staff's watcher with one line, and nothing else talks to any
session.

## Decisions carried

| Answer | Carried as | Where |
| --- | --- | --- |
| ui-night | in batch-30; the goal is a working UI | header |
| ui-night scope | this CR is one of the eight UI items | header, Overlaps |
| ui-night act | the board edits no batch and messages no session; reconciled in the AGENTS.md text | 1 |
| Q1 | a Grill action opens a discussion panel; the Griller records as the card says; nothing more | 5, 6 |
| Q2 | the surface server starts the run, headless, with the user's CLI, one run per message, resumed; a new named exception in AGENTS.md; not the Chief of Staff | 1, 3 |
| Q3 | this machine's host, the project's agent and model for the role on that host; Claude Code proven by a real trial; Copilot only if a trial proves the same contract, else one refusal line and Known gaps | 2, 3, Evidence |
| Q4 | **open, the user's**: built on A (this machine only; reads the project and the planning folder, writes only in that CR's folder, only the card's role-free `chantier` commands; no other shell, no network, no subagent) | 1, 3, 4, Open questions |
| Q5 | inbox, `P1`...`P4`, `3-ready` only; never `4-batch/`, an archive or the trash | 4 |
| Q6 | grills as the card says; no spec-writer, spec-critic, `triage`, `abandon`, `restore`, label or group; says who specifies and places | 2 |
| Q7 | one conversation per CR, one turn at a time, answer shown at the turn's end, a working mark, Stop; kept while the server runs and across a reload; after a restart, a new conversation from the files; no streaming | 4, 5 |
| Q8 | one running turn per project; a second refused with one line naming the CR | 4 |
| Q9 | no process between turns; a turn ends by Stop, 10 minutes, or the server's stop; End forgets the conversation, the files stay | 4, 5 |
| Q10 | a turn that wrote appends one waking `board@1` line through the one append function; "grilled enough" and the destination named in it; griller-Q7's questions and requests out | 4 |
| Q11 | the remote worktree Griller and a file-carrying hand-over: out, to a follow-up item | Out of scope |
| Q12 | writes in the planning folder directly; refuses with `writer: not running` or `stopped`; in-project, `.agents/changes/` of the main checkout; no commit, push or pull | 2, 4 |
| Q13 | the panel names the CLI, the machine and the model before the first message; the first message is the yes; cost in no batch; a turn's cost not owed | 5 |
| Q14 | one line with the CLI's own words; nothing retried; what was written stays and the panel says a turn was cut | 4, 5 |
| Q15 | no seat, watcher, server or hub; never opens, pauses, orders or steers | 2 |
| Q16 | through the published API; `live` gets nothing | 4, Out of scope |
| Q17 | AGENTS.md, the Griller card, the host references, `DESIGN.md`; the evidence of one real discussion on Claude Code that records an answer and wakes a watcher | 1, 2, 5, Evidence |

## What changes

### 1. AGENTS.md: the new named exception (Q2, Q4 A, Q17, ui-night act)

Three edits, found by their text.

**a. The role rule.** In the bullet that starts "A role's contract lives in", replace the sentence
"The CLI knows no role; one named exception: the cost code knows the two specification agents by
their agent type (`spec-writer`, `spec-critic`), to put them on the grill line." with:

> The CLI knows no role; two named exceptions: the cost code knows the two specification agents by
> their agent type (`spec-writer`, `spec-critic`), to put them on the grill line, and the surface
> server knows the board's Griller (`board-griller`), to start it (below).

**b. The board's sentence on agents.** In the surface server's paragraph, replace "the board itself
records nothing and messages no agent, but its writer's commits of the planning surface's published
paths (below) and its journal lines (`sync-*@1`);" with:

> the board itself records nothing and messages no agent, but its writer's commits of the planning
> surface's published paths (below) and its journal lines (`sync-*@1`), and the board's Griller (the
> fourth exception, which passes the user's own words to a run the server started for that user, and
> is not a message of the board to an agent);

**c. The fourth exception.** In the same paragraph, replace "it takes its dependencies like the rest
of the CLI and knows no role." with the text below, written out exactly:

> a fourth, the board's Griller: on the request of a client on this machine only (the connection's
> peer is a loopback address and the request carries no proxy header, `Forwarded`,
> `X-Forwarded-For`, `X-Forwarded-Host` or `X-Real-IP`; never a client over the network, even with
> the key), and on an item of the inbox, the backlog (`2-backlog/P1`...`P4`) or `3-ready` only (never
> a CR of `4-batch/`, an archive or the trash), the server starts the user's own headless CLI of this
> machine's host (`claude -p`; `copilot -p` only once a trial has proved the same limits; on a host
> not proved, the Grill action refuses with one line), as the `board-griller` agent with the
> project's agent and model for that role on that host, one run per message the user types in the
> board, each run resuming the conversation of the run before, at most one run per project at a time
> and at most 10 minutes per run, and no process between two runs; the first run's prompt is a fixed
> brief that names the Griller card, the CR's folder and the CLI, followed by the user's text, and
> each later run's prompt is the user's text alone, passed unchanged; the run may read the project
> and the planning folder, write only in that CR's folder, and run only the role-free `chantier`
> commands that the Griller card's "Started from the board" names: no other shell command, no
> network but the host CLI's own calls to its model, no subagent; it grills as that card says,
> messages no session and runs no git; this is not the board messaging an agent: the server sends a
> run nothing of its own but that fixed brief, only the words the user typed, to a run it started for
> that user, and it sends nothing to any session (no Chief of Staff, Foreman, Driver or Griller
> session) and records nothing in a batch; when a run has written in that CR's folder, the server
> appends one `board@1` line (action `grill`) to the project's `forge-journal.jsonl` through the one
> append function, which the Chief of Staff's watcher carries; the server keeps the conversation in
> its memory only (the host CLI keeps its own session files, as for any session of the user), refuses
> with one line while the surface's writer is not running or stopped, and no agent starts it; built
> on the user's direction of 2026-11-17 and answer "Tout" of 2026-11-21, with no measured cost; it
> takes its dependencies like the rest of the CLI and knows no role but the board's Griller.

Should the user choose B or C of board-griller-Q4, only this text and the checks of section 4 change
(B: drop "on the request of a client on this machine only ... even with the key"; C: replace the run's
limits by "the full Griller of a desktop session", this machine only).

### 2. The cards and the agent files (Q3, Q6, Q12, Q15, Q17)

**`skills/chantier/references/griller.md`**: a new level-2 section `## Started from the board`, placed
after "In a planning surface", short, saying:

- You are started by the surface server, headless, one run per message the user types in the web
  board, resumed from the run before; you take no seat (skip `session-start.md`'s seat reading and
  title), start no watcher, server or hub, and never open, pause, order or steer anything ("Never"
  holds).
- Your brief names the CR's folder: you grill that CR only. "From the files" holds: re-read the
  folder at each run. In a planning surface, "In a planning surface" holds (the server has checked
  the writer before your run).
- You grill as "What you do" says, for that CR: questions in the user's language, each answer
  recorded in `02-answers.md` at once, the restatement before "grilled enough?", and at "grilled
  enough?" the destination asked and recorded as the Chief of Staff's "Where the CR goes" says.
- You do not start a spec-writer or a spec-critic, run `file`, `triage`, `abandon` or `restore`, or
  set a label or a group; you tell the user that the Chief of Staff (or a desktop Griller) specifies
  and places the CR. You send no `[griller→chief-of-staff]` line: a question or request for the
  Chief of Staff, you tell the user to put to it.
- You write only in the CR's folder (prototypes included, as "A CR's folder holds its work" says),
  and you run only these commands: `$CHANTIER rules`, `$CHANTIER access`, `$CHANTIER summary lint
  <the CR's folder>` and `$CHANTIER summary set <the CR's folder> ...` (the summary rule of this card
  holds). A tool refused by your limits: say it in one line; never another way.
- When the user has said "grilled enough" and the destination is recorded, end your reply with the
  line `[griller→board] grilled enough: <next batch|running batch>`.
- Your cost is in no batch.

**`skills/chantier/references/startup-manifest.json`**: `roles` gains `"board-griller":
"griller.md"`; `startup_sections` gains `"board-griller": ["griller.md#Started from the board"]`;
`actions` gains `"board-griller": ["griller.md"]`. The manifest's size `limit` and its test hold.

**Agent files** (one per host, bodies identical, as AGENTS.md asks):
`agents/board-griller.md` and `com.github.copilot/agents/chantier-board-griller.agent.md`, written on
the pattern of `agents/spec-writer.md` and its Copilot twin: the description ends "Started by the
surface server. Prompt starts with: `chantier board-griller for the board, in the project
<root>.`"; the body names the role "the chantier board's Griller" and the first-line check with
`chantier board-griller`; `tools: Read, Write, Edit, Grep, Glob, Bash, PowerShell` (the run's own
limits, section 3, narrow them further). Models: `config/chantier.defaults.yml` gains
`board-griller: {model: claude-opus-5-5}` under `hosts.claude.roles` and `board-griller: {model:
claude-opus-5.5}` under `hosts.copilot.roles`, equal to the agent files (the existing test). The role
then appears by itself on the Configuration page and in `playbook`'s agents lines (`plugin_roles`
reads the agent files).

**`skills/chantier/references/concepts.md`**, "Words", **Griller**: one sentence added: "The board's
Griller is a Griller the surface server starts headless from the web board, on one CR, under the
limits of the Griller card's 'Started from the board'."

**Host references.** `hosts/claude-code.md`, table "Tools": a row "The board's Griller (the surface
server starts it)": `claude -p` as section 3 says, with the exact flags the trial proved; Mark: the
trial's date and what it showed, each limit's refusal included; until then **unproved**.
`hosts/copilot.md`, table "Tools": a row "The board's Griller": `copilot -p`, **unproved**: the Grill
action refuses on Copilot (section 3) until a trial proves the same contract; the trial named.

**`skills/chantier/references/chief-of-staff.md`**: unchanged. Its watcher rule already handles a
`board wrote (...)` line: one line to the user, no tool call, no action; the spec-writer starts only
on the user's word, as for any grill.

### 3. The run (Q2, Q3, Q4 A, Q9, Q12)

A new module `skills/chantier/scripts/cli/src/chantier/board/griller.py` holds the conversations and
the runs; `board/context.py`'s `Context` gains one field, `griller`, the registry, made at start.

- **Host and model.** The host is `plugin_files.detect_host()` in the server's process (the session
  that started the board passes its environment); a host it cannot tell refuses the action with its
  own line. The agent and model are the effective ones for role `board-griller` on that host, read by
  the same code as the Configuration page (`playbook/edit.py`'s `config_view` rows); a refused start
  (`playbook/config.py`'s `start_refusal`) refuses the action with its line.
- **Hosts supported.** A table `HEADLESS` in `griller.py` holds one entry per proved host: Claude
  Code only in this CR. Copilot gets an entry only if the PR's trial proves the same contract
  (headless, resumed, the same limits, each refusal shown); else `griller.get` says `available:
  false` with the reason "the board's Griller is not proved on Copilot yet: grill in a session with
  the Griller skill", and the PR's Known gaps names it. No look-alike, no fallback.
- **The command (Claude Code).** `claude -p` with the JSON output, started as the agent
  `chantier:board-griller` with `--model <effective model>`, the conversation fixed by an id the
  server makes at the first run and resumed by it at each later run, the prompt on standard input
  (no quoting or length limit of a Windows command line), and the permission flags that make the
  limits below hold whatever the user's own allow rules say (a user allow rule must not widen them).
  The flags are the Driver's to find and prove in the trial (candidates: `--output-format json`,
  `--agent`, `--session-id` then `--resume`, `--permission-mode`, `--allowedTools`,
  `--disallowedTools`, `--strict-mcp-config`, `--add-dir`); `hosts/claude-code.md` records the set
  that held. A limit the host cannot enforce is a stop: the action refuses on that host and the PR
  says so, never a weaker run.
- **Where it runs.** The working directory is the planning folder's session root: the surface's
  checkout in a planning surface (`Repo.session_root`), with the project's clone added as a readable
  folder; the project's main checkout in-project. The same directory at every run (a resume needs
  it).
- **The limits (Q4, option A).** Read: the project (its clone, in a surface) and the planning folder.
  Write: only the CR's folder (its absolute path at the run's start). Shell: only the four commands
  of the card's section, each as `<$CHANTIER> <command> ...` with `$CHANTIER` from
  `plugin_files.cli_command(repo)`, in Bash or PowerShell. Refused: any other shell command, any
  web fetch or search, any MCP tool, any subagent (`Agent`, `Task`).
- **The brief.** The first run's prompt is the fixed text below, then a blank line and the user's
  text; each later run's prompt is the user's text alone, unchanged:

  ```text
  chantier board-griller for the board, in the project <project root>.
  Your card: <skill folder>/references/griller.md, its section "Started from the board" first; your host's reference: <skill folder>/references/hosts/<claude-code|copilot>.md.
  The CLI: <cli_command(repo)>.
  The CR's folder: <absolute folder>. You write only there.
  The user speaks to you from the web board; their words follow.
  ```

  A first run cut before the host saved its conversation (no result read) leaves the next run a
  first run again: the brief is sent again.
- **One turn.** A thread starts the process; the turn ends at the process's exit, at the user's Stop
  (the process and its children stopped with `psutil`, as `procs.py` does), at 10 minutes
  (`TURN_LIMIT_S = 600`), or at the server's stop (`app.py`'s `Server.shutdown` stops a running
  turn first). Nothing runs between two turns.
- **Reading the result.** The answer is the run's result text (Claude Code's JSON `result`); an
  error result, an error exit, a missing CLI (`claude: not found on this machine`) or the time limit
  is the turn's `error`, in the CLI's own words (its result text, else the last lines of its error
  output, cut to 2,000 characters). Nothing is retried; no other tool is tried.
- **What it wrote.** Before and after the run the server lists the CR's folder (each file's
  relative path, size and modification time; the folder found again by its slug,
  `lifecycle/backlog.py`'s `backlog_folder`, should it have moved meanwhile): the files added,
  changed or removed are the turn's `wrote`.

### 4. The server's API (Q5, Q7, Q8, Q9, Q10, Q12, Q14, Q16)

**Who may call.** `board/context.py`'s `Request` gains `peer: str | None` (Starlette's
`request.client.host` in `app.py`; the WebSocket's `client.host` at its upgrade in `api/ws.py`, kept
with the connection). `board/api/auth.py` gains `is_local(peer, headers)`: `address.is_loopback(peer)`
and none of `forwarded`, `x-forwarded-for`, `x-forwarded-host`, `x-real-ip` among the headers.
`ops.call(ctx, name, args)` gains a third argument, the caller (`local: bool`), passed by `api/http.py`
and `api/ws.py`; the key is still required as for every op. `griller.send`, `griller.stop` and
`griller.end` refuse a caller that is not local, 403, "the board's Griller starts only from a browser
on this machine". `griller.get` and the topic answer anyone with the key, with `local` in their value.

**Ops and topic** (`board/api/protocol.py`'s `OP_ARGS`, `TOPIC_ARGS`; `board/api/ops.py`'s `HANDLERS`;
`board/api/topics.py`; `board/api/protocol.json` rewritten by `just protocol-schema`):

| Name | Arguments | Answer |
| --- | --- | --- |
| `griller.get` (op) and `griller` (topic) | `project`, `item` | `available`, `reason` (when not), `local`, `host`, `model`, `cli` (`claude` or `copilot`), `running` (the item whose turn runs in the project and since when, or null), `conversation` (null, or its `started` and `turns`: each `n`, `user`, `answer`, `state` `running`/`done`/`stopped`/`timed-out`/`failed`, `error`, `wrote`, `started`, `ended`, `grilled`), `now`; the topic's `rev` is a hash of that value without `now` |
| `griller.send` | `project`, `item`, `text` (1 to 8,000 characters) | 202 `{turn}`; the answer comes through the topic or the next `griller.get` |
| `griller.stop` | `project`, `item` | 200 `{stopped}` (false when no turn ran) |
| `griller.end` | `project`, `item` | 200 `{ended}`; 409 while a turn runs ("stop the turn first") |

**`griller.send` refusals**, each one line, checked in this order: not local (403); no such project
or item (404); the item not in the inbox, `P1`...`P4` or `3-ready` (409, "the board's Griller grills
inbox, backlog and ready items only: <slug> is in <stage>"; `write_api.COLUMNS` and
`backlog.column_of`); the host not proved or not told, or the role's start refused (409, the reason);
in a planning surface, the writer `not running` or `stopped` (409, the `writer:` line of
`writer/lines.py`, as `seat` prints it); a turn already running in the project (409, "a Griller turn
runs on <slug>: wait for it or stop it"); a text empty or too long (400).

**The conversation.** One per (project, item), in the server's memory only: kept across a page
reload and between turns, gone at the server's stop (the next conversation starts from the CR's
files, as the card's "From the files" says), gone at `griller.end` (the CR's files stay). The
registry writes no file.

**The journal line (Q10).** When a turn's `wrote` is not empty, whatever its end (a cut turn
included), the server appends one `board@1` line through `hub/journal.py`'s `append(repo, lines,
"board")` (the one append function), built by `board_event("grill", [slug], text)`; `WAKING_ACTIONS`
gains `"grill"`, so it wakes. The text: `the board's Griller wrote <slug> (<files, comma-separated>)`,
and when the answer's last line is `[griller→board] grilled enough: <destination>`, `; grilled enough,
destination <destination>` added (the turn's `grilled` set). The watcher prints it as `board wrote
(grill): ...; for the Chief of Staff: tell the user, act on nothing` (`hub/schemas.py`'s `board_text`,
unchanged). `board@1` stays as published (its `action` is an open set): `hub/schemas.json` is
unchanged. No line for a turn that wrote nothing. The board's own `board-journal.jsonl` gets no line
(open question 3).

**`live`.** `clients/tui/` is unchanged: it reads, writes nothing, and calls no `griller.*` op.

### 5. The web client (Q1, Q7, Q9, Q13, Q14)

Read `clients/web/DESIGN.md` first and keep it true.

- **The action.** `js/panel/head.js` fills its empty `data-place="panel-actions"` place, for an item
  target whose bucket is in `model/grill.js`'s `BUCKETS` only (never a batch CR or a merged one), with
  one button, "Grill" (`data-grill`), built with the existing button classes. A client that is not
  local, or a host not proved, gets it disabled with the reason in its `title`.
- **The discussion.** A new `js/panel/griller.js`: with Grill on, the panel's document region shows
  the discussion instead of the file view (the tree stays, so the files the Griller writes appear);
  a second click on Grill, or a click on a file, goes back to the files. It subscribes to the
  `griller` topic through `js/core/transport.js` only (no other socket, the transport rule) and calls
  the ops through a new `js/api/griller.js`, as `js/api/backlog.js` does.
- **Before the first message** (no conversation yet): one notice, "This runs your own `{cli}` on this
  machine, with `{model}`, and spends your tokens. Your first message is your yes."
- **The turns.** The user's text shown as plain text; the answer rendered by the panel's Markdown
  renderer (`js/panel/markdown.js`), as a file is. While a turn runs: a working mark, the text box
  and Send disabled, and Stop. A turn that ended `stopped`, `timed-out` or `failed` shows its one line
  (the CLI's words, or "cut at 10 minutes"), and when it wrote: "This turn was cut; what it wrote
  stays: {files}". A turn that wrote shows its files. End (enabled with no turn running) forgets the
  conversation after one confirmation through `js/ui/dialog.js`.
- **Another CR's turn running** in the project: Send disabled with "A Griller turn runs on {slug}".
- **Words.** Every string through `t()`/`tn()` under new `griller.*` keys, in every language file
  (`js/i18n/en*.js`, `fr*.js`).
- **Styles.** A new sheet `css/griller.css` (linked from `index.html` with the panel's sheets): layout
  only, tokens only, no side accent border on a turn (a turn is told apart by its fill, `--band` for
  the user's, `--panel` for the answer, with the hairline all around), no new component. If a token
  is needed, it is added to `css/tokens.css` and to `DESIGN.md`'s table together (the test).
- **`DESIGN.md`** gains a section `## The board's Griller`: the Grill button lives in the panel's
  actions place, for inbox, backlog and ready items only; the discussion replaces the file view, the
  tree stays; the notice before the first message; one turn at a time, a working mark, Stop, no
  streaming; plain text for the user, the Markdown renderer for the answer; no side accent; words
  only for the states; the button disabled, with its reason, for a client not on this machine.

## Out of scope

- The remote Griller in a worktree and a hand-over that carries files (Q11): the Chief of Staff
  files a follow-up item from this CR's Q11 when the PR lands.
- griller-Q7's questions and requests from the Griller to the Chief of Staff (Q10).
- Starting a spec-writer or spec-critic, `triage`, `abandon`, `restore`, labels and groups from the
  board's Griller (Q6).
- Streaming partial text, showing a turn's cost (Q7, Q13); a conversation kept across a server
  restart (Q7).
- `live` and any client but the web board's UI (Q16; the API is open to any local client with the
  key).
- A server-side check that no file outside the CR's folder changed: the host's limits and the trial
  prove the boundary.
- The cost code: unchanged; the board's Griller runs are host sessions no batch reads, so their cost
  is in no batch.
- The Chief of Staff's card (its generic `board wrote` rule holds).

## Overlaps (batch-30 and the UI night)

- **CR-429 (board-fingerprint-cache)**: the server watches the planning files; the panel's tree then
  shows the Griller's files as they land. Both touch `board/context.py`, `board/api/topics.py`,
  `board/api/protocol.py`: entries side by side; this CR goes on top of it.
- **board-history** and **board-user-inbox** (specs v1): both add to `OP_ARGS`/`TOPIC_ARGS` and
  `protocol.json`; the second to land rewrites `protocol.json` with `just protocol-schema`.
  board-user-inbox's `question` kind comes from a batch's answer waits only: a board Griller's
  question is not an Inbox entry.
- **CR-440 (board-triage-polish)**: its "writes since rescan" explanation counts the board's own
  writes (`board-journal.jsonl`); a Griller turn adds none there (open question 3), so its text
  stays true.
- **CR-439 (board-help-page)**: its Griller entry gains the board's Griller in one sentence,
  whichever lands second.
- **CR-427, 433, 434, 435, 441** (Triage lane, batch page): no shared file but the i18n files and
  `index.html`'s sheet list; entries side by side.
- **CR-426 (board-exposure, merged)**: the board listens on this machine by default; the local check
  here still holds when `board.host: network` opens it, and refuses a proxied request.
- **CR-432, CR-443 (permissions)**: the allow rules preflight's P10 names are the steering session's;
  the board's Griller's limits are its run's own flags and are not added to `~/.claude/settings.json`.
- **dashboard-pages**: no overlap.

## Evidence

Checks, in `just check` (in-process, few and parametrized, in a new
`skills/chantier/scripts/cli/tests/test_board_griller.py`, with the run's launcher replaced through a
seam of `board/griller.py`, no host CLI started):

- `griller.send` refused, each with its status and line: a peer not loopback; a loopback peer with
  each proxy header; an item of `4-batch/`, of `5-archives/`, of `6-trash/`; the writer stopped in a
  surface; a second turn in the project while one runs (naming the CR); an empty and a too-long text;
  Copilot as the host (not proved).
- A turn that writes `02-answers.md` appends one `board@1` line, action `grill`, waking, read back by
  `hub/journal.py`'s `read`; with the `[griller→board] grilled enough: next batch` last line, the text
  names it; a turn that writes nothing appends none; a cut turn that wrote appends one and says cut.
- `griller.stop` ends a running turn (`stopped`); the time limit ends one (`timed-out`, the limit
  lowered for the test); `griller.end` forgets and refuses while a turn runs; a second turn of a
  conversation resumes it (the launcher sees the same conversation id and no brief).
- The command line built for Claude Code from the shipped `config/chantier.defaults.yml` and agent
  file (the effective model `claude-opus-5-5`, the agent name) and from a project's `chantier.yaml`
  that sets another model: read from the files as they ship at the head under test.
- The existing shipped-file tests, reading the files as they ship: the agent files' bodies identical
  on both hosts and equal to the defaults' models; the startup manifest's sections exist and stay
  under its limit; `tests/test_board_design.py` (tokens table, no side accent, components);
  `test_board_ui.py`'s transport rule (no socket outside `transport.js`).
- `just eval-dry-run` (a change under the CLI's `src/`), and `just scenario` green (cards and CLI
  change); no new scenario step (no model in the scenario).

The real trial (Q17), on Claude Code, the user's machine, in the PR's Deliverables:

- One discussion from the web board on a backlog item: the notice shown with the model, a question
  asked, the user's answer recorded in `02-answers.md` by the Griller, the summary refreshed, and a
  running Chief of Staff's watcher waking with the `board wrote (grill)` line (its output quoted).
- Each limit refused in a turn, the host's refusal quoted: a shell command other than the four
  (`git status`), a write outside the CR's folder, a web fetch, a subagent.
- A second turn resumed (the Griller knows the first), Stop on a running turn, and a page reload
  that keeps the conversation.
- A screenshot of the panel with a conversation, captioned with the head's SHA.

Host and default matrix:

| Cell | Expected | Proof |
| --- | --- | --- |
| Claude Code, shipped default model | runs `claude-opus-5-5` | the trial |
| Claude Code, model set in `chantier.yaml` | runs that model; the notice names it | test (command line); trial optional |
| Copilot, not proved | the action refuses with one line; Known gaps names it | test |
| Copilot, proved by a trial in the PR | the same contract as Claude Code | that trial, else the row above |
| A planning surface, writer running | runs in the surface's checkout | the trial |
| A planning surface, writer stopped | refused with the `writer:` line | test |
| In-project planning folder | runs in the main checkout, writes `.agents/changes/<stage>/<slug>/` | test (launcher seam) |

## Open questions

1. **board-griller-Q4, the user's (the security boundary)**: what the headless Griller may do with no
   one to answer a permission prompt, and which clients may start it.
   - A (recommended, built): only a client on this machine (never over the network, even with the
     key); it reads the project and the planning folder, writes only in that CR's folder, and runs
     only the role-free `chantier` commands the card names; no other shell, no network, no subagent.
   - B: the same limits, and any client holding the key may start it, the network included.
   - C: the full Griller of a desktop session (shell, subagents), on this machine only.
2. **How the run gets its model and agent** (Q3 asks for "the project's configured agent and model
   for the Griller role", and no such role is configured today).
   - A (recommended, built): a `board-griller` agent file on both hosts and its model in the shipped
     defaults, so the role has a Configuration row like any other, and AGENTS.md's role rule names
     the server's knowledge of it.
   - B: no agent file; a new key `board.griller.model` per host in `chantier.yaml`, not on the
     Configuration page.
   - C: the host CLI's own default model, named in the panel only after the first turn (against
     Q13's notice before the first message).
3. **The board's own journal**: does a Griller turn also add a line to `board-journal.jsonl` (the
   Triage "writes since rescan" count)?
   - A (recommended, built): no; the forge journal line alone, as Q10 says; the count stays the
     board's own backlog writes.
   - B: yes, one line per turn that wrote, counted until the next rescan.
