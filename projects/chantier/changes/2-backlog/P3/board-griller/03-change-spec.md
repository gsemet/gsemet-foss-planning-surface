# A Griller started from the web board

Spec v3 (2026-11-21). Short name: `board-griller`. Destination: batch-30 (ui-night, running),
joined on top of the batch-30 CRs it overlaps (see Overlaps). Built on the user's directions of
2026-11-17 and of the UI night (2026-11-21, "Tout"), on board-griller-Q4 and Q20 (the user's: B,
any holder of the board's key, with a plain-HTTP warning), and on Q1 to Q3, Q5 to Q19 and Q21 to
Q27, answered by a Fable advisor in the user's place. Every question is decided. v2 applied the
spec critic's findings on v1, judged against Q4 B; v3 carries Q25 to Q27 and applies the second
critic's findings on v2.

## Goal

From the web board, on an inbox, backlog or ready item, the user opens a discussion with a Griller
and grills that CR without a desktop session: the user types, a Griller answers, and the Griller
records the grill in the CR's folder as its card says. The surface server runs the headless CLI of
the host it runs under, on the machine it runs on, one run per message, under limits that hold
against the user's own settings; any client holding the board's key may start it (this machine,
or the local network when `board.host: network`). A turn that wrote in the CR's folder wakes the
Chief of Staff's watcher with one line, and nothing else talks to any session.

## Decisions carried

| Answer | Carried as | Where |
| --- | --- | --- |
| ui-night | in batch-30; the goal is a working UI | header |
| ui-night scope | this CR is one of the eight UI items | header, Overlaps |
| ui-night act | the board edits no batch and messages no session; reconciled in the AGENTS.md text | 1 |
| Q1 | a Grill action opens a discussion panel; the Griller records as the card says; nothing more | 5, 6 |
| Q2 | the surface server starts the run, headless, with the user's CLI, one run per message, resumed; a new named exception in AGENTS.md; not the Chief of Staff | 1, 3 |
| Q3 (as narrowed by Q27) | the host of the machine the server runs on, the project's model for the role on that host (the agent: the plugin's only, Q27); Claude Code proven by a real trial; Copilot only if a trial proves the same contract, else one refusal line and Known gaps | 2, 3, Evidence |
| Q4 (the user's: B) | any holder of the board's key may start it, the network included; it writes only in that CR's folder and runs only the card's `chantier` commands; no other shell, no network, no subagent; no loopback check: the key is the boundary | 1, 3, 4 |
| Q5 | inbox, `P1`...`P4`, `3-ready` only; never `4-batch/`, an archive or the trash | 4 |
| Q6 | grills as the card says; no spec-writer, spec-critic, `triage`, `abandon`, `restore`, label or group; says who specifies and places | 2 |
| Q7 | one conversation per CR, one turn at a time, answer shown at the turn's end, a working mark, Stop; kept while the server runs and across a reload; after a restart, a new conversation from the files; no streaming | 4, 5 |
| Q8 (as replaced by Q22) | at most one running turn per planning surface (per project's planning folder in-project); a second refused with one line naming the project and the CR | 3, 4 |
| Q9 | no process between turns; a turn ends by Stop, 10 minutes, or the server's stop; End forgets the conversation, the files stay | 3, 4, 5 |
| Q10 | a turn that wrote appends one waking `board@1` line through the one append function; "grilled enough" and the destination named in it; griller-Q7's questions and requests out | 4 |
| Q11 | the remote worktree Griller and a file-carrying hand-over: out, to a follow-up item | Out of scope |
| Q12 | writes in the planning folder directly; refuses with `writer: not running` or `stopped`; in-project, `.agents/changes/` of the main checkout; no commit, push or pull | 2, 4 |
| Q13 (worded by Q21) | the panel names the CLI, the machine and the model before the first message; the first message is the yes; cost in no batch; a turn's cost not owed | 5 |
| Q14 | one line with the CLI's own words; nothing retried; what was written stays and the panel says a turn was cut | 3, 4, 5 |
| Q15 | no seat, watcher, server or hub; never opens, pauses, orders or steers | 2 |
| Q16 | through the published API; `live` gets nothing | 4, Out of scope |
| Q17 | AGENTS.md, the Griller card, the host references, `DESIGN.md`; the evidence of one real discussion on Claude Code that records an answer and wakes a watcher | 1, 2, 5, Evidence |
| Q18 (as narrowed by Q27) | a `board-griller` agent file on both hosts, bodies identical, its model in the shipped defaults; AGENTS.md's role rule names the server's knowledge of the role | 1a, 2 |
| Q19 | no line in `board-journal.jsonl`; only the waking `board@1` line (action `grill`) in `forge-journal.jsonl` | 4, Overlaps |
| Q20 (the user's) | no opt-in key, no daily cap; the panel and `docs/web-board.md` say the board speaks plain HTTP (the key, link and 30-day cookie, and every turn's text travel in clear on the network) and that `chantier board --new-key` revokes the key | 4 (docs), 5 |
| Q21 | the notice's exact wording; the machine's name comes from the server (`machine` in `griller.get`) | 4, 5 |
| Q22 | one shared conversation per CR; every holder reads it, any holder may Stop or End; the panel marks a turn sent from another client; the notice says the conversation is shared; one running turn per surface | 3, 4, 5 |
| Q23 | the run loads none of the user's, project's or local settings, loads chantier explicitly, works from an allow list alone; the trial's list of refusals on the user's real machine; sign-in and the agent still resolve; the proved version recorded in `hosts/claude-code.md` (recorded only); no flag set giving all of it is a stop | 2, 3, Evidence |
| Q24 | the card keeps its four commands and adds "and no other `chantier` command"; the allow rules are those four shapes only, `summary lint` and `summary set` pinned to the CR's folder | 2, 3 |
| Q25 | the run may also read the plugin's skill folder, read-only, and nothing else outside the project and the planning folder; the trial shows a read there allowed and a read outside the three refused; `hosts/claude-code.md` records it; AGENTS.md's exception and section 3's read rule gain it | 1e, 2, 3, Evidence |
| Q26 | while a turn runs on an item, the board's own move, trash and running-batch ops on it answer 409 naming the running turn; a turn whose CR's folder another session moved ends `failed` naming where it went; a test shows no stray folder at the old path | 3, 4, Evidence |
| Q27 | only the plugin's `board-griller` agent; any other agent set for that role refuses the Grill action with one line naming the setting; the model stays configurable; the role's skills and tools never widen the allow list | 1e, 2, 3, Evidence |

## What changes

### 1. AGENTS.md: the new named exception (Q2, Q4 B, Q17, Q18, Q22, Q23, Q25 to Q27, ui-night act)

Six edits, found by their text.

**a. The role rule (Q18).** In the bullet that starts "A role's contract lives in", replace the
sentence "The CLI knows no role; one named exception: the cost code knows the two specification
agents by their agent type (`spec-writer`, `spec-critic`), to put them on the grill line." with:

> The CLI knows no role; two named exceptions: the cost code knows the two specification agents by
> their agent type (`spec-writer`, `spec-critic`), to put them on the grill line, and the surface
> server knows the board's Griller (`board-griller`), to start it with its brief and read its
> `[griller→board]` line (below).

**b. The surface server's first "never messages an agent".** In the surface server's paragraph,
replace "it never edits a batch and never messages an agent;" with "it never edits a batch and never
messages an agent (the board's Griller, below, is not one);".

**c. The "only through" clause.** In the same paragraph, replace "only through the CLI's role-free
commands and its own reading, checking and writing of that file;" with "only through the CLI's
role-free commands and its own reading, checking and writing of that file, and the board's Griller's
writes in one CR's folder;".

**d. The board's sentence on agents.** In the same paragraph, replace "the board itself records
nothing and messages no agent, but its writer's commits of the planning surface's published paths
(below) and its journal lines (`sync-*@1`);" with:

> the board itself records nothing and messages no agent, but its writer's commits of the planning
> surface's published paths (below) and its journal lines (`sync-*@1`), and the board's Griller (the
> fourth exception, which passes the words a holder of the key typed to a run the server started for
> the key's holder, and is not a message of the board to an agent);

**e. The fourth exception.** In the same paragraph, replace "it takes its dependencies like the rest
of the CLI and knows no role." with the text below, written out exactly:

> a fourth, the board's Griller: on the request of any client holding the board's key (this machine,
> or the local network when `board.host: network`), and on an item of the inbox, the backlog
> (`2-backlog/P1`...`P4`) or `3-ready` only (never a CR of `4-batch/`, an archive or the trash), the
> server starts the headless CLI of the host it runs under (`claude -p`; `copilot -p` only once a
> trial has proved the same limits; on a host not proved or not told, the Grill action refuses with
> one line), as the plugin's own `board-griller` agent only (any other agent set for that role
> refuses the Grill action with one line naming the setting) with the project's model for that role
> on that host, one run per message typed in the board, each run resuming the conversation of the run
> before, one shared conversation per CR that every holder of the key reads and any holder may stop
> or end, at most one run per planning surface (per project's planning folder in-project) at a time
> and at most 10 minutes per run, and no process between two runs; the first run's prompt is a fixed
> brief that names the Griller card, the CR's folder and the CLI, followed by the typed text, and each
> later run's prompt is the typed text alone, passed unchanged; the run loads none of the user's,
> project's or local host settings (allow rules, hooks, MCP servers), loads chantier explicitly, and
> works from an allow list alone, which the role's skills and tools never widen: it may read the
> project, the planning folder and the plugin's skill folder (read-only), write only in that CR's
> folder, and run only the four `chantier` commands that the Griller card's "Started from the board"
> names, `summary lint` and `summary set` on that CR's folder only: no other shell command, no
> network tool (no web fetch or search, no shell beyond those four commands; the host CLI's own
> calls to its model aside), no MCP tool, no subagent; a host whose flags cannot give all of these
> limits gets no run; it grills as that card says, messages no session and runs no git command of
> its own; while a run works on an item, the board's own moves of that item (the trash and the
> running batch included) are refused; this is not the board messaging an agent: the server sends a run nothing of its own
> but that fixed brief, only the words a holder of the key typed, to a run it started for the key's
> holder, and it sends nothing to any session (no Chief of Staff, Foreman, Driver or Griller
> session) and records nothing in a batch; when a run has written in that CR's folder, the server
> appends one `board@1` line (action `grill`) to the project's `forge-journal.jsonl` through the one
> append function, which the Chief of Staff's watcher carries; the server keeps the conversation in
> its memory only (the host CLI keeps its own session files, as for any session of the user),
> refuses with one line while the surface's writer is not running or stopped, and no agent starts
> it; the board speaks plain HTTP, so on the network the key and every turn's text travel in clear,
> and `chantier board --new-key` revokes the key; built on the user's direction of 2026-11-17 and
> answers "Tout" (2026-11-21) and board-griller-Q4 B and Q20, with no measured cost; it takes its
> dependencies like the rest of the CLI and knows no role but the board's Griller.

**f. The no-setup bullet.** In the bullet that starts "The plugin must work with no setup", replace
"except the server's read of a batch's PRs, the forge hub and the surface server's writer, whose
fetch and push need it (below))" with "except the server's read of a batch's PRs, the forge hub, the
surface server's writer, whose fetch and push need it, and the board's Griller run (the host CLI's
calls to its model) (below))"; and, in the same bullet, replace "the surface server keeps its key,"
with "the surface server keeps its key, the host CLI that the board's Griller runs keeps its own
session files, as for any session of the user,".

### 2. The cards and the agent files (Q3, Q6, Q12, Q15, Q17, Q18, Q24, Q25, Q27)

**`skills/chantier/references/griller.md`**: a new level-2 section `## Started from the board`,
placed after "In a planning surface", short, saying:

- You are started by the surface server, headless, one run per message typed in the web board,
  resumed from the run before; the conversation is shared by every holder of the board's key, so
  the words may come from more than one person. You take no seat (skip `session-start.md`'s seat
  reading and title), start no watcher, server or hub, and never open, pause, order or steer
  anything ("Never" holds).
- Your brief names the CR's folder: you grill that CR only. "From the files" holds: re-read the
  folder at each run. In a planning surface, "In a planning surface" holds but its `seat` reading:
  skip it (the server has checked the writer before your run). You may read the project, the
  planning folder and the plugin's skill folder (your card, the startup core, your host's
  reference), nothing else.
- You grill as "What you do" says, for that CR: questions in the user's language, each answer
  recorded in `02-answers.md` at once, the restatement before "grilled enough?", and at "grilled
  enough?" the destination asked and recorded as the Chief of Staff's "Where the CR goes" says.
- You do not start a spec-writer or a spec-critic, run `file`, `triage`, `abandon` or `restore`, or
  set a label or a group; you tell the user that the Chief of Staff (or a desktop Griller) specifies
  and places the CR. For a CR with an `issue:` line, you write no issue drafts: the Chief of Staff
  drafts them when it starts the spec-writer. You send no `[griller→chief-of-staff]` line: a question or request for the
  Chief of Staff, you tell the user to put to it.
- You write only in the CR's folder (prototypes included, as "A CR's folder holds its work" says),
  and you run only these commands: `$CHANTIER rules`, `$CHANTIER access`, `$CHANTIER summary lint
  <the CR's folder>` and `$CHANTIER summary set <the CR's folder> ...` (the summary rule of this card
  holds), and no other `chantier` command. A tool refused by your limits: say it in one line; never
  another way.
- When the user has said "grilled enough" and the destination is recorded, end your reply with the
  line `[griller→board] grilled enough: <next batch|running batch>`.
- Your cost is in no batch.

**`skills/chantier/references/startup-manifest.json`**: `roles` gains `"board-griller":
"griller.md"`; `startup_sections` gains `"board-griller": ["griller.md#Started from the board"]`;
`actions` gains `"board-griller": ["griller.md"]`. The manifest's size `limit` holds.
**`skills/chantier/scripts/cli/tests/test_startup_manifest.py`**: `WITH_SECTIONS` gains
`"board-griller"` (the test compares the manifest's `startup_sections` keys with it, and its
`_roles()` finds the role by `agents/board-griller.md`).

**Agent files** (one per host, bodies identical, as AGENTS.md asks): `agents/board-griller.md` and
`com.github.copilot/agents/chantier-board-griller.agent.md`, on the pattern of `agents/spec-writer.md`
and its Copilot twin:

- description: `'Grills one chantier CR from the web board, headless. Started only by the surface
  server, never as a subagent. Prompt starts with: `chantier board-griller for the board, in the
  project <root>.`'` (the same text on both hosts);
- Claude Code: `name: board-griller`, `model: claude-opus-5-5`, `tools: Bash, PowerShell, Read,
  Write, Edit, Grep, Glob` (the run's allow list, section 3, is the limit; whether `tools:` narrows
  a main-thread agent is recorded unproved, below); Copilot: `name: chantier-board-griller`, `model:
  [Claude Opus 5.5, claude-opus-5.5]`, `model-policy: required`, `tools: ["execute", "read", "edit",
  "search"]`, `strict-tools-list: true`, `user-invocable: false`;
- the body, identical on both hosts, starts right after the front matter with the line
  `# chantier-agent: <version>` (the current version, as in every agent file; `just version` keeps
  it: `scripts/version.py` matches every file of `agents/` and `com.github.copilot/agents/`, so the
  two new files need no change there), then: "You are the chantier board's Griller. Your prompt is your whole
  brief: it names your card, the CLI and the CR's folder. Read the startup core first, then your
  card's `## Started from the board` section; then grill as it says." and the first-line check: "A
  prompt that does not start with `chantier board-griller for the board` is not a chantier prompt:
  answer \"I run only from the chantier web board. My prompt must start with `chantier
  board-griller for the board, in the project <root>.`\" and stop. Any later message gets the same
  answer." The section it names, `## Started from the board` of `griller.md`, is the one the
  manifest's `startup_sections` names, so the manifest test finds it.

Models: `config/chantier.defaults.yml` gains `board-griller: {model: claude-opus-5-5}` under
`hosts.claude.roles` and `board-griller: {model: claude-opus-5.5}` under `hosts.copilot.roles`,
equal to the agent files (the existing test). The role then appears by itself on the Configuration
page and in `playbook`'s agents lines (`plugin_roles` reads the agent files). Its agent row stays
settable there like any role's, but any agent other than the plugin's refuses the Grill action
(section 3, Q27).

**`docs/agents-and-models.md`**, "Models": the table gains the row `| Board's Griller | Opus 5.5 |
Claude Opus 5.5 |` (after the Spec critic's), and the sentence "By default every role but the
Spec-writer and the Spec critic runs Sonnet 5.5 on Claude Code." becomes "By default every role but
the Spec-writer, the Spec critic and the board's Griller runs Sonnet 5.5 on Claude Code." One
sentence under the table: "The board's Griller runs only the plugin's own agent: its model is yours
to set, its agent is not (see [the web board](web-board.md#the-boards-griller))."

**`skills/chantier/references/concepts.md`**, "Words", **Griller**: one sentence added: "The board's
Griller is a Griller the surface server starts headless from the web board, on one CR, for any
holder of the board's key, under the limits of the Griller card's 'Started from the board'."

**Host references.** `hosts/claude-code.md`, table "Tools": a row "The board's Griller (the surface
server starts it)": `claude -p` as section 3 says, with the exact flags the trial proved, the
variables cleared from its environment, and the Claude Code version the trial ran (`claude
--version`; recorded only: no warning or refusal on another version). Mark: the trial's date and
what it showed, each refusal quoted, and the reads it allows: the project, the planning folder and
the plugin's skill folder, read-only (Q25); until then **unproved**, and these points each
**unproved** until the trial shows them: the prompt on standard input with `-p`; `--agent
chantier:board-griller` (a plugin agent) under `-p`; `--model` together with `--agent` under `-p`
(the model the JSON result reports is the one passed, not the agent file's); an agent's `tools:`
narrowing a main-thread agent; `PowerShell(...)` allow rules; no settings loaded while the sign-in
still resolves; how the server tells that the host saved a conversation for an id (section 3, "The
brief"). `hosts/copilot.md`, table
"Tools": a row "The board's Griller": `copilot -p`, **unproved**: the Grill action refuses on Copilot
(section 3) until a trial proves the same contract; the trial named (the same list as Claude Code's).

**`skills/chantier/references/chief-of-staff.md`**: unchanged. Its watcher rule already handles a
`board wrote (...)` line: one line to the user, no tool call, no action; the spec-writer starts only
on the user's word, as for any grill. Its destination rule (a `board wrote (...)` line that sets a
CR's destination is written into `02-answers.md`) does not fire: the `grill` line's text says the
Griller already recorded the destination and nothing is to be written (section 4).

### 3. The run (Q2, Q3, Q4 B, Q9, Q12, Q22 to Q27)

A new module `skills/chantier/scripts/cli/src/chantier/board/griller.py` holds the conversations and
the runs; `board/context.py`'s `Context` gains one field, `griller`, the registry, made at start.

- **Host and model.** The host is `plugin_files.detect_host()` in the server's process (a session
  that started the board passes its environment). A host it cannot tell refuses the action: a board
  started by hand from a terminal has no host variable, and `griller.get`'s `reason` says so: "the
  board was started outside a Claude Code or Copilot session, so it cannot tell which CLI to run:
  start it from a session, or set CHANTIER_HOST before `chantier board`" (`CHANTIER_HOST` is
  `detect_host`'s own setting, not a fallback). The model is the effective one for role
  `board-griller` on that host, read by the same code as the Configuration page (`playbook/edit.py`'s
  `config_view` rows); a refused start (`playbook/config.py`'s `start_refusal`) refuses the action
  with its line. The agent is the plugin's only (Q27): when the effective `agent` of that row is not
  `config.default_agent(host, "board-griller")` (`chantier:board-griller` on Claude Code), the
  action refuses with one line naming the setting: `role "board-griller": the board's Griller runs
  only the plugin's agent <default>: remove "agent" for board-griller under hosts.<host>.roles
  (<layer>)` (the layer `config_view` reports). The role's skills and tools (the agent file's
  `tools:`, any setting) never widen the allow list below: it is built from its fixed shapes only.
- **Hosts supported.** A table `HEADLESS` in `griller.py` holds one entry per proved host: Claude
  Code only in this CR. Copilot gets an entry only if the PR's trial proves the same contract
  (headless, resumed, the same limits, each refusal shown); else `griller.get` says `available:
  false` with the reason "the board's Griller is not proved on Copilot yet: grill in a session with
  the Griller skill", and the PR's Known gaps names it. No look-alike, no fallback.
- **The command (Claude Code).** `claude -p` with the JSON output, started as the agent
  `chantier:board-griller` with `--model <effective model>`, the conversation fixed by an id the
  server makes at the first run and resumed by it at each later run, the prompt on standard input
  (no quoting or length limit of a Windows command line). The Driver finds and proves the flags in
  the trial; candidates: `--output-format json`, `--agent`, `--session-id` then `--resume`,
  `--setting-sources` with no source (no user, project or local settings: no allow rule, hook or
  MCP server of theirs), `--plugin-dir <plugin root>` (chantier loaded explicitly, since the
  user's settings that enable it are not read), `--strict-mcp-config` with no MCP configuration,
  `--permission-mode` (one that refuses what is not allowed, with no prompt), `--allowedTools`
  (the list below), `--add-dir`. `hosts/claude-code.md` records the set that held.
- **The allow list (Q23, Q24).** The run's only permissions, built at each run from the absolute
  paths (`$CHANTIER` is `plugin_files.cli_command(repo)` as the brief names it; `<cr>` the CR's
  folder):
  - read: `Read`, `Grep`, `Glob` on the session root, the project's clone when it is added
    (below) and the plugin's skill folder (the folder that holds `references/`), read-only (Q25);
    nothing else outside them;
  - write: `Write` and `Edit` on `<cr>/**` only;
  - shell, in Bash and in PowerShell: `<$CHANTIER> rules`, `<$CHANTIER> access` with its arguments,
    `<$CHANTIER> summary lint <cr>`, `<$CHANTIER> summary set <cr>` with its arguments; nothing else.
  No deny list: what the list does not name is refused (Q24). A tool the run does not name (a web
  fetch or search, an MCP tool, `Agent`, `Task`, any other command) is refused by the host. The two
  `summary` shapes are written so that no other folder matches: not `<cr>-x`, not
  `<cr>/../<sibling>`, and not `<cr>` followed by `--project <other>`; if the host's rule grammar
  cannot express that, it is the stop below.
- **The stop (Q23).** If no flag set gives all of it (no settings loaded, chantier and the agent
  resolved, the sign-in resolved, the allow list alone, each refusal of the trial shown), `HEADLESS`
  gets no Claude Code entry, the Grill action refuses on Claude Code with the reason "the board's
  Griller's limits are not proved on this host", and the PR says so: never a weaker run.
- **The run's environment.** The run inherits the server's environment minus the variables that
  would make it look like the steering session or a nested session: `CLAUDECODE`,
  `CLAUDE_CODE_ENTRYPOINT`, `CLAUDE_CODE_SESSION_ID`, `CLAUDE_CODE_SSE_PORT`, `CLAUDE_PROJECT_DIR`
  and `CHANTIER_BATCH` cleared (a constant `CLEARED_ENV` in `griller.py`), and `CHANTIER_HOST` set
  to the host. The list is the trial's to prove (a nested `claude -p` that starts, and whose
  `chantier` calls do not take the steering session's identity); `hosts/claude-code.md` records
  the list that held.
- **Where it runs.** The working directory is the planning folder's session root: the surface's
  checkout in a planning surface (`Repo.session_root`), with the project's clone added as a readable
  folder; the project's main checkout in-project. The same directory at every run (a resume needs
  it).
- **The brief.** The first run's prompt is the fixed text below, then a blank line and the typed
  text; each later run's prompt is the typed text alone, unchanged:

  ```text
  chantier board-griller for the board, in the project <project root>.
  Your card: <skill folder>/references/griller.md, its section "Started from the board" first; your host's reference: <skill folder>/references/hosts/<claude-code|copilot>.md.
  The CLI: <cli_command(repo)>.
  The CR's folder: <absolute folder>. You write only there.
  The user speaks to you from the web board; their words follow.
  ```

  A first run that was cut (no result read) leaves the next run a first run again (the brief sent
  again, under the same id) only if the host saved no conversation for that id; when the host saved
  one, the next run resumes it with the typed text alone. The server asks the host's own state for
  that id, as the trial proves it (recorded in `hosts/claude-code.md`); the trial stops a first turn
  and then sends a second message, and shows which of the two happened.
- **One turn at a time per surface (Q22).** The registry holds at most one running turn for the
  whole server (one server serves one planning surface, or one in-project planning folder), across
  its projects. A thread starts the process; the turn ends at the process's exit, at a holder's
  Stop (the process and its children stopped with `psutil`, as `procs.py` does), at 10 minutes
  (`TURN_LIMIT_S = 600`, under the test seam), when the CR's folder moves (below), or at the
  server's stop (`app.py`'s `Server.shutdown` stops a running turn first), whatever stops the
  server: a stop by hand, or the idle stop of a board a watcher started (`--stop-idle`, CR-429: 30
  minutes with no client; the turn then ends `stopped`, "the board stopped"). Nothing runs between
  two turns.
- **Reading the result.** The answer is the run's result text (Claude Code's JSON `result`); an
  error result, an error exit, a missing CLI (`claude: not found on this machine`) or the time limit
  is the turn's `error`, in the CLI's own words (its result text, else the last lines of its error
  output, cut to 2,000 characters). Nothing is retried; no other tool is tried.
- **What it wrote.** Before and after the run the server lists the CR's folder (each file's
  relative path, size and modification time): the files added, changed or removed are the turn's
  `wrote`.
- **A folder that moves during a turn (Q26).** The board's own moves of the item are refused while
  its turn runs (section 4). Another session may still move it (a Chief of Staff's `triage`, `order
  add`, `abandon`): while the turn runs, the server checks the CR's path at each file notification
  of the project and at least once a second; when the folder is no longer at the turn's path, it
  stops the turn at once (as Stop does) and ends it `failed` with one line naming where the folder
  went, found by its slug (`lifecycle/backlog.py`'s `backlog_folder`, or the batch, archive or
  trash folder that holds it): "the CR's folder moved during the turn: <slug> is now in <stage>"
  ("... is gone" when none holds it). At the turn's end, if the old path exists again holding only
  files the turn wrote after the move, the server removes them and the empty folder, so the writer
  publishes no stray folder; a file there it did not see the turn write, it leaves and names in the
  line. `wrote` is listed at the new path.
- **The push.** The conversation lives in memory, so no file notification reports its changes:
  the `griller` topic is pushed by the push loop's regular pass (every `push_every_s()`, 2 s, which
  CR-429 keeps), and at each change (a turn started, ended, stopped, timed out or failed; a
  conversation ended) the registry also calls the wake entry CR-429 gives `board/api/push.py`
  (`PushLoop.wake()`), so the change is pushed at once. The wake is a latency gain only; nothing
  depends on it for correctness. This CR's `depends.json` is `{"after": ["board-fingerprint-cache"]}`,
  so the entry exists when it is coded.
- **The seam.** `griller.py` builds the run's command through one function, `command(run) ->
  list[str]` (and its environment), which a test replaces by another command; the rest (the child
  process, standard input, the JSON parsing, the exit code, the tree kill) runs for real.

### 4. The server's API and its documentation (Q5, Q7, Q9, Q10, Q12, Q14, Q16, Q19 to Q22, Q26, Q27)

**Who may call.** Any client holding the board's key, as for every op (`board/api/auth.py`
unchanged); no address or proxy-header check.

**Ops and topic** (`board/api/protocol.py`'s `OP_ARGS`, `TOPIC_ARGS`; `board/api/ops.py`'s `HANDLERS`;
`board/api/topics.py`; `board/api/protocol.json` rewritten by `just protocol-schema`):

| Name | Arguments | Answer |
| --- | --- | --- |
| `griller.get` (op) and `griller` (topic) | `project`, `item` | `available`, `reason` (when not), `host`, `machine` (`socket.gethostname()`), `model`, `cli` (`claude` or `copilot`), `running` (the project and item whose turn runs on the server and since when, or null), `conversation` (null, or its `started` and `turns`: each `n`, `from`, `user`, `answer`, `state` `running`/`done`/`stopped`/`timed-out`/`failed`, `error`, `wrote`, `started`, `ended`, `grilled`), `now`; the topic's `rev` is a hash of that value without `now` |
| `griller.send` | `project`, `item`, `text` (1 to 8,000 characters), `from` (an opaque client id, 64 characters at most) | 202 `{turn}`; the answer comes through the topic or the next `griller.get` |
| `griller.stop` | `project`, `item` | 200 `{stopped}` (false when no turn ran) |
| `griller.end` | `project`, `item` | 200 `{ended}`; 409 while a turn runs ("stop the turn first") |

`from` only marks a turn sent from another client (Q22); the server does not tell holders apart
and checks nothing on it.

**`griller.send` refusals**, each one line, in this order: no such project or item (404); the item
not in the inbox, `P1`...`P4` or `3-ready` (409, "the board's Griller grills inbox, backlog and
ready items only: <slug> is in <stage>"; `write_api.COLUMNS` and `backlog.column_of`); the host not
proved or not told, the role's start refused, or an agent other than the plugin's set for the role
(409, the reason; Q27); in a planning surface, the writer
`not running` or `stopped` (409, the `writer:` line of `writer/lines.py`, as `seat` prints it); a
turn already running on the server (409, "a Griller turn runs on <project>/<slug>: wait for it or
stop it"); a text empty or too long, or a `from` too long (400).

**The board's own moves during a turn (Q26).** While a turn runs on an item, the board's ops that
move its folder refuse that item: the check sits in `board/write_api.py`'s `_move_one`, which
`backlog.move` (to any destination, `6-trash` and `running-batch` included) and `backlog.group`'s
moves go through, and asks the registry (through the `Context`) which item's turn runs; the item's
result is refused with "a Griller turn runs on <project>/<slug>: stop it before moving the item",
and a call on that item alone answers 409. The other items of the same call move as today. The
other backlog writes (labels, a new file) are unchanged.

**The conversation.** One per (project, item), shared by every holder, in the server's memory only:
kept across a page reload and between turns, gone at the server's stop (the next conversation starts
from the CR's files, as the card's "From the files" says), gone at `griller.end` (the CR's files
stay). Any holder may Stop or End it. The registry writes no file.

**The journal line (Q10, Q19).** When a turn's `wrote` is not empty, whatever its end (a cut turn
included), the server appends one `board@1` line through `hub/journal.py`'s `append(repo, lines,
"board")` (the one append function), built by `board_event("grill", [slug], text)`; `WAKING_ACTIONS`
gains `"grill"`, so it wakes. The text: `the board's Griller wrote <slug> (<files, comma-separated>)`,
`; cut` added for a turn that did not end `done`, and when the answer's last line is
`[griller→board] grilled enough: <destination>`, `; grilled enough, destination <destination>,
already recorded in 02-answers.md by the Griller: nothing to write` added (the turn's `grilled`
set). The watcher prints it as `board wrote (grill): ...; for the Chief of Staff: tell the user, act
on nothing` (`hub/board_text.py`'s `board_text`, unchanged). `board@1` stays
as published (its `action` is an open set): `hub/schemas.json` is unchanged. No line for a turn that
wrote nothing. The board's own `board-journal.jsonl` gets no line (Q19).

**`live`.** `clients/tui/` is unchanged: it reads, writes nothing, and calls no `griller.*` op.

**`docs/server-api.md`**: the ops table gains the four `griller.*` rows (arguments and answers as
above, the refusals' statuses in one sentence below the table); the topics table gains the `griller`
row ("what `griller.get` gives; pushed at each change of the conversation"); the "Limits" table
gains the row "A Griller message (`griller.send`'s `text`) | 8,000 characters | 400". A sentence
under the ops table says the Griller ops start a run of the host CLI on the board's machine and
spend the tokens of the account signed in there.

**`docs/web-board.md`**: a new section `## The board's Griller` (after "A CR's files"): the Grill
button and what it runs (the board's machine's `claude`, its model, its account's tokens; the
plugin's agent only, the model yours to set), the shared conversation and the one turn at a time
per surface, that the item cannot be moved from the board while its turn runs, what it writes and
the Chief of Staff's line, and the warning of Q20, word for word as the panel's (section 5): "The board speaks plain
HTTP: on the network, the key (the link and its 30-day cookie) and every turn's text travel in
clear. `chantier board --new-key` revokes the key."

### 5. The web client (Q1, Q7, Q9, Q13, Q14, Q20, Q21, Q22)

Read `clients/web/DESIGN.md` first and keep it true.

- **The action.** `js/panel/head.js` fills its empty `data-place="panel-actions"` place, for an item
  target whose bucket is in `model/grill.js`'s `BUCKETS` only (never a batch CR or a merged one), with
  one button, "Grill" (`data-grill`), built with the existing button classes. A host not proved or
  not told gets it disabled with `griller.get`'s `reason` in its `title`.
- **The discussion.** A new `js/panel/griller.js`: with Grill on, the panel's document region shows
  the discussion instead of the file view (the tree stays, so the files the Griller writes appear);
  a second click on Grill, or a click on a file, goes back to the files. It subscribes to the
  `griller` topic through `js/core/transport.js` only (no other socket, the transport rule) and calls
  the ops through a new `js/api/griller.js`, as `js/api/backlog.js` does.
- **The client id.** The page makes one random id at its first load and keeps it in
  `sessionStorage` (so a reload keeps it), and sends it as `from` with each `griller.send`.
- **Before the first message** (no conversation yet): one notice, word for word (Q21), with the
  server's `cli`, `machine` and `model`: "This runs `{cli}` on {machine}, the machine the board runs
  on, with `{model}`, and spends the tokens of the account signed in there. Your first message is
  your yes."; then "This conversation is shared: anyone holding the board's key sees it and may stop
  or end it." (Q22); then the warning of Q20: "The board speaks plain HTTP: on the network, the key
  (the link and its 30-day cookie) and every turn's text travel in clear. `chantier board --new-key`
  revokes the key." The two last sentences stay shown under the conversation once it has started.
- **The turns.** The typed text shown as plain text; the answer rendered by the panel's Markdown
  renderer (`js/panel/markdown.js`), as a file is. A turn whose `from` is not this page's id is
  marked "sent from another client". While a turn runs: a working mark, the text box and Send
  disabled, and Stop (for every holder, whoever sent the turn). A turn that ended `stopped`,
  `timed-out` or `failed` shows its one line (the CLI's words, or "cut at 10 minutes"), and when it
  wrote: "This turn was cut; what it wrote stays: {files}". A turn that wrote shows its files. End
  (enabled with no turn running) forgets the conversation after one confirmation through
  `js/ui/dialog.js`.
- **Another CR's turn running** on the server: Send disabled with "A Griller turn runs on
  {project}/{slug}".
- **Words.** Every string through `t()`/`tn()` under new `griller.*` keys, in every language file
  (`js/i18n/en*.js`, `fr*.js`).
- **Styles.** A new sheet `css/griller.css` (linked from `index.html` with the panel's sheets): layout
  only, tokens only, no side accent border on a turn (a turn is told apart by its fill, `--band` for
  the typed text, `--panel` for the answer, with the hairline all around), no new component. If a
  token is needed, it is added to `css/tokens.css` and to `DESIGN.md`'s table together (the test).
- **`DESIGN.md`** gains a section `## The board's Griller`: the Grill button lives in the panel's
  actions place, for inbox, backlog and ready items only; the discussion replaces the file view, the
  tree stays; the notice, the shared sentence and the plain-HTTP warning before the first message,
  the last two kept under the conversation; one turn at a time, a working mark, Stop, no streaming;
  plain text for the typed text, the Markdown renderer for the answer; the "sent from another
  client" mark in words; no side accent; words only for the states.

## Out of scope

- The remote Griller in a worktree and a hand-over that carries files (Q11): the Chief of Staff
  files a follow-up item from this CR's Q11 when the PR lands.
- griller-Q7's questions and requests from the Griller to the Chief of Staff (Q10).
- Starting a spec-writer or spec-critic, `triage`, `abandon`, `restore`, labels and groups from the
  board's Griller (Q6).
- Streaming partial text, showing a turn's cost (Q7, Q13); a conversation kept across a server
  restart (Q7).
- An opt-in key, a daily cap, HTTPS, or telling holders of the key apart (Q20, Q22).
- `live` and any client but the web board's UI (Q16; the API is open to any client with the key).
- A server-side check that no file outside the CR's folder changed: the host's limits and the trial
  prove the boundary.
- The cost code: unchanged; the board's Griller runs are host sessions no batch reads, so their cost
  is in no batch.
- The Chief of Staff's card (its generic `board wrote` rule holds).

## Overlaps (batch-30, running, and the UI night)

batch-30 runs in stack mode. This CR joins it on top of every batch-30 CR it overlaps, so each of
them lands (merged, or handed back ready below it) before this one: CR-428, 429, 433 to 446 and 448,
which all edit AGENTS.md at least (CR-437, 438 and 442 that file alone, or with `concepts.md`,
`hosts/claude-code.md` or `startup-manifest.json`; entries side by side). CR-425 to 427 and 430 to
432 are in `3-done`; CR-426 (board-exposure) gives `board.host: network`, which this CR names.
`depends.json` holds only the real need, `{"after": ["board-fingerprint-cache"]}` (the push wake);
the rest is the stack's order, not a dependency. Only CR-447 goes above this CR (below).

- **CR-429 (board-fingerprint-cache, `4-batch/2-actives`)**: its push loop keeps a regular 2 s
  pass and gains `PushLoop.wake()`; this CR calls it for the `griller` topic (section 3, "The
  push"), a latency gain only. It adds `board --stop-idle` (30 minutes with no client), one of the
  ways a turn ends. Both touch `board/context.py`, `board/api/topics.py`, `board/api/push.py`,
  `docs/server-api.md`, `docs/web-board.md`, `DESIGN.md`, `config/chantier.defaults.yml`,
  `hosts/claude-code.md`: entries side by side.
- **CR-445 (board-history, `4-batch/1-pending`)**: shares `board/api/protocol.py`,
  `protocol.json`, `board/api/ops.py`, `board/api/topics.py`, `board/context.py`,
  `docs/server-api.md`, `docs/web-board.md`, `DESIGN.md`, the i18n files and `index.html` (its own
  "no shared file expected" with this CR does not hold). It lands first; this CR rewrites
  `protocol.json` with `just protocol-schema` and keeps the tables' rows side by side.
- **CR-448 (dashboard-pages)**: shares `protocol.py`, `protocol.json`, `board/api/ops.py`,
  `docs/server-api.md`, `docs/web-board.md`, `DESIGN.md`, the i18n files and `index.html` (v2 said
  "no overlap": wrong); handled as CR-445.
- **CR-444 (board-user-inbox)**: shares `board/api/topics.py`, `docs/server-api.md`,
  `docs/web-board.md`, `DESIGN.md`, the i18n files and `index.html`. Its `question` kind comes from a
  batch's answer waits only: a board Griller's question is not an Inbox entry.
- **CR-446 (live-several-boards-and-keys)**: `clients/tui/`, which this CR leaves untouched, and
  one sentence of `docs/server-api.md`'s "A terminal client"; rows side by side.
- **CR-443 (gate-hold-narrowing)**: shares `docs/agents-and-models.md`,
  `config/chantier.defaults.yml`, `concepts.md`, `docs/server-api.md`, `hosts/claude-code.md`. The
  allow rules preflight's P10 names are the steering session's; the board's Griller's allow list is
  its run's own flags, is not added to `~/.claude/settings.json`, and is not widened by it (no
  settings loaded).
- **CR-440 (board-triage-polish)**: its "writes since rescan" explanation counts the board's own
  writes (`board-journal.jsonl`); a Griller turn adds none there (Q19), so its text stays true.
  Shares `docs/web-board.md`, `DESIGN.md`, the i18n files.
- **CR-439 (board-help-page)**: shares `docs/agents-and-models.md`, `docs/web-board.md`,
  `DESIGN.md`, the i18n files and `index.html`; this CR adds the board's Griller to its Griller
  entry in one sentence.
- **CR-433, 434, 435, 441** (batch chip, kanban, batch page): `docs/web-board.md`, `DESIGN.md`, the
  i18n files and `index.html`'s sheet list; entries side by side.
- **CR-436 (sync-blocked-by-others), CR-428 (drop-to-next-batch)**: AGENTS.md, `concepts.md`,
  `docs/web-board.md`, `hosts/claude-code.md`; entries side by side.
- **CR-447 (docs-gardening, `4-batch/1-pending`)**: its `depends.json` `after` list and its table of
  areas gain `board-griller` (its spec asks the Foreman to add a CR that joins later), with this
  CR's areas: `docs/web-board.md`, `docs/server-api.md`, `docs/agents-and-models.md`. It lands
  after this CR and checks those areas.

## Evidence

Checks, in `just check` (in-process, few and parametrized, in a new
`skills/chantier/scripts/cli/tests/test_board_griller.py`). Budget: every refusal is tested
in-process with no child process (the refusals come before any start); at most about six tests
start a child (the stand-in); the time limit is about 0.3 s in tests, and no test sleeps longer.
The PR quotes `just test`'s time before and after the change on the user's Windows machine
(AGENTS.md's budget: at most 30 s above its 18.5 s).

- **The stand-in.** A small Python script, `skills/chantier/scripts/cli/tests/griller_standin.py`,
  replaces the host CLI through the seam (`command()` returns `[sys.executable, <stand-in>, ...]`)
  and runs as a real child: it reads its prompt from standard input, writes a file in the CR's
  folder (named in its arguments), prints a JSON result like Claude Code's (`result`, `is_error`,
  `session_id`), and on request (a word in the prompt) sleeps, starts a child of its own that
  sleeps, exits non-zero with an error text and no JSON, or writes after a pause (for the move).
- In-process, no child: `griller.send` refused, each with its status and line: an item of
  `4-batch/`, of `5-archives/`, of `6-trash/`; the writer stopped in a surface; a second turn on the
  server while one runs (a registry holding a running turn), in the same project and in another
  project of the surface (naming the project and the CR); an empty and a too-long text; Copilot as
  the host (not proved); no host told (the hand-started board's reason); a project's
  `chantier.yaml` that sets `agent` for `board-griller` (the line names the setting and its layer;
  Q27). `backlog.move` of the item to a column, to `6-trash` and to `running-batch`, and
  `backlog.group` with it, while its turn runs: 409 (alone) with the line, another item of the same
  call moved (Q26). The parsing of a result with no JSON: `failed` with the output's last lines.
- Child runs (about six): (1, 2) a first and a second turn: the prompt read on standard input is
  the brief then the text, then the text alone (the same conversation id, resumed); the JSON result
  read as the answer; the file written in `wrote`; the second answer ends with `[griller→board]
  grilled enough: next batch`. (3) A non-zero exit with no JSON: `failed` with the stand-in's own
  words. (4) Stop on a turn that wrote and then sleeps: `stopped`, the stand-in and its own child
  gone (`psutil.pid_exists` false). (5) The time limit: `timed-out`, the tree gone. (6) The folder
  moved as another session would (the CLI's backlog functions, not the board's op) while the
  stand-in pauses, then the stand-in writes at the old path: the turn ends `failed` naming the new
  stage, and no folder is left at the old path (Q26).
- The journal, read back by `hub/journal.py`'s `read` from those runs: turns 1 and 2 each append
  one `board@1` line, action `grill`, waking, the second's text naming "grilled enough, destination
  next batch, already recorded ... nothing to write"; run 3 (wrote nothing) appends none; run 4
  (cut, wrote) appends one that says cut; `board-journal.jsonl` gets nothing. `griller.end` forgets
  and refuses while a turn runs; a turn sent with another `from` keeps it in `griller.get`.
- The command line built for Claude Code (the real `command()`, not run) from the shipped
  `config/chantier.defaults.yml` and agent file (the effective model `claude-opus-5-5`, the agent
  name) and from a project's `chantier.yaml` that sets another model, read from the files as they
  ship at the head under test: the allow list holds exactly the four command shapes with the CR's
  folder in the two `summary` ones, `Write`/`Edit` on the CR's folder only, and the reads on the
  session root, the added clone and the skill folder; checked against the prefix-and-`*` matching
  that `hosts/claude-code.md` records, no rule matches `summary set` on `<cr>-x`, on
  `<cr>/../<sibling>`, or on `<cr> --project <other>`; the environment has none of `CLEARED_ENV`.
- The existing shipped-file tests, reading the files as they ship: the agent files' bodies identical
  on both hosts (the `# chantier-agent:` line included, among `scripts/version.py`'s targets) and
  equal to the defaults' models; `test_startup_manifest.py` with `board-griller` in `WITH_SECTIONS`
  (the section `griller.md#Started from the board` exists, the startup stays under the limit);
  `tests/test_board_design.py` (tokens table, no side accent, components); `test_board_ui.py`'s
  transport rule (no socket outside `transport.js`).
- `just eval-dry-run` (a change under the CLI's `src/`), and `just scenario` green (cards and CLI
  change); no new scenario step (no model in the scenario).

The real trial (Q17, Q23, Q25), on Claude Code, on the user's machine with the real
`~/.claude/settings.json` in place, in the PR's Deliverables:

- One discussion from the web board on a backlog item: the notice shown with the machine and the
  model, a question asked, the user's answer recorded in `02-answers.md` by the Griller, the summary
  refreshed, and a running Chief of Staff's watcher waking with the `board wrote (grill)` line (its
  output quoted).
- The sign-in and the `chantier:board-griller` agent resolved with no settings loaded.
- The model: a project's `chantier.yaml` sets another model for `board-griller`; the model the JSON
  result reports (its per-model usage) is that one, not the agent file's (`--model` with `--agent`
  under `-p`).
- Each refusal quoted, the host's own words: `chantier gate <cr> "git status"`, `chantier lease
  hold`, `chantier triage`, a bare `git status`, a bare `git commit`, `curl` and `Invoke-WebRequest`,
  `cat` of a file outside the three readable folders, `chantier summary set` on a sibling CR's
  folder, on `<cr>-x`, on `<cr>/../<sibling>`, and on the CR's folder followed by `--project
  <other>`, a write in a sibling CR's folder, a read outside the project, the planning folder and
  the plugin's skill folder, a web fetch, an MCP tool, an `Agent` call; and one read allowed in the
  skill folder (Q25).
- The run's environment: the cleared list, the nested run starting, and its `chantier` calls not
  taking the steering session's identity.
- A first turn stopped, then a second message: which happened (resumed, or the brief sent again
  because the host saved no conversation for that id), and how the server told.
- A second turn resumed (the Griller knows the first), Stop on a running turn, a page reload that
  keeps the conversation, and a turn sent from a second browser marked "sent from another client"
  in the first.
- `claude --version`, recorded in `hosts/claude-code.md`, with the flags, the reads allowed and the
  unproved points that the trial proved.
- A screenshot of the panel with a conversation, captioned with the head's SHA.

Host and default matrix:

| Cell | Expected | Proof |
| --- | --- | --- |
| Claude Code, shipped default model | runs `claude-opus-5-5` | the trial |
| Claude Code, model set in `chantier.yaml` | runs that model; the notice names it | test (command line) and the trial, required: the model the JSON result reports |
| Claude Code, another agent set in `chantier.yaml` | the action refuses with one line naming the setting | test |
| Claude Code, limits not proved by the trial | the action refuses with one line; the PR says so | test (no `HEADLESS` entry) |
| Copilot, not proved | the action refuses with one line; Known gaps names it | test |
| Copilot, proved by a trial in the PR | the same contract as Claude Code | that trial, else the row above |
| No host told (board started by hand) | the action refuses with the hand-started reason | test |
| A planning surface, writer running | runs in the surface's checkout | the trial |
| A planning surface, writer stopped | refused with the `writer:` line | test |
| In-project planning folder | runs in the main checkout, writes `.agents/changes/<stage>/<slug>/` | test (stand-in) |

## Open questions

None: every question of the grill is decided (Q4 and Q20 by the user, the rest by the Fable
advisor).
