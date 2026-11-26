"""The 50 rows: id, name, roles, Claude means, Claude mark, Copilot means."""

FOREMAN = ["foreman", "chief-of-staff"]
DRIVERS = ["cr-driver", "stack-driver", "qa-driver", "release-driver"]
STEER = ["foreman", "chief-of-staff", *DRIVERS]
SESSION = ["chief-of-staff", "foreman", "griller"]
WRITERS = [
    "cr-driver",
    "coder",
    "conflict-resolver",
    "debugger",
    "inspector",
    "investigator",
    "verifier",
]

P, U = "proved", "untested"

ROWS = [
    dict(
        id="start-foreman",
        name="Start the Foreman's session",
        roles=["chief-of-staff"],
        mark=U,
        claude=[
            "`mcp__ccd_session__start_session` with `initiation: \"user_asked\"`, `title: \"<title>\"`, `context: \"fresh\"`, no `cwd`, no `preset`, `use_worktree: false`.",
            "`model: \"claude-sonnet-5-5\"`, `effort: \"medium\"`, the user's permission mode; leave the session linked.",
        ],
        copilot=[
            "`create_session` with `model: \"claude-opus-5.5\"`, `workspace` = the repository, `worktree: false`, `title: \"<title>\"`.",
            "A refused start is reported with its exact text.",
        ],
    ),
    dict(
        id="own-session-id",
        name="Own session id and title",
        roles=SESSION,
        mark=P,
        claude=[
            "`get_session(\"self\")` gives the session's id and title.",
            "The transcript's id is `$CLAUDE_CODE_SESSION_ID`.",
        ],
        copilot=[
            "`$COPILOT_AGENT_SESSION_ID`, which is also the transcript's id.",
            "Reading the session's own title is not recorded on this host.",
        ],
    ),
    dict(
        id="set-own-title",
        name="Set a session's own title",
        roles=SESSION,
        mark=U,
        claude=[
            "`set_session_title` renames the session itself (the Chief of Staff, a Griller, the Foreman).",
            "`get_session(\"self\")` shows the new title.",
        ],
        copilot=[
            "When the host offers a way, the session sets its own title (the Foreman first); else the title stays.",
            "The tool that does it is not recorded on this host.",
        ],
    ),
    dict(
        id="skills",
        name="The skills",
        roles=SESSION,
        mark=U,
        claude=[
            "`/chantier:chantier` (the router), `/chantier:chief-of-staff [foreman|direct]`, `/chantier:griller`, `/chantier:status`.",
            "A plugin's `skills/<name>/` is `/<plugin>:<name>`; the argument `reload` of the router and of both role skills reloads the rules.",
        ],
        copilot=[
            "The same four skills, same names: `skills/chantier` (the router), `skills/chief-of-staff`, `skills/griller`, `skills/status`.",
            "Declared in `.github/plugin/plugin.json`; how Copilot passes the arguments `foreman`, `direct` or `reload` is not known.",
        ],
    ),
    dict(
        id="load-skill",
        name="Load another skill (the router)",
        roles=SESSION,
        mark=U,
        claude=[
            "The host's Skill tool loads another skill.",
            "The router (`/chantier:chantier`) asks which role, then loads that role's skill.",
        ],
        copilot=[
            "Not recorded on this host: which tool loads another skill.",
            "The four skills are declared in `.github/plugin/plugin.json`.",
        ],
    ),
    dict(
        id="list-sessions",
        name="List the sessions and their state",
        roles=["chief-of-staff"],
        mark=U,
        claude=[
            "The session tools of the `mcp__ccd_session__` set list the sessions and tell whether the seat's session is alive.",
            "The exact tool and its states are not recorded on this host; the \"looks stopped\" line of `session-start.md` is asked.",
        ],
        copilot=[
            "Not known on this host: how a session lists the sessions or tells the seat's session alive.",
            "The seat's session always looks stopped to a new session; the \"looks stopped\" line of `session-start.md` is asked.",
        ],
    ),
    dict(
        id="message-session",
        name="Message another session of the user",
        roles=SESSION,
        mark=U,
        claude=[
            "`SendMessage` to the other session's id (a hand-over, a Griller's line).",
            "Claude Desktop limits messages between sessions; a refused send is reported, never sent another way.",
        ],
        copilot=[
            "`send_message` to the other session's link (a hand-over, a Griller's line).",
            "Whether a limit applies is not recorded on this host.",
        ],
    ),
    dict(
        id="session-link",
        name="A session's link (for the seat)",
        roles=["chief-of-staff", "griller"],
        mark=U,
        claude=[
            "`get_session` gives the session's link; the seat records it.",
            "The name of the link field is not recorded on this host.",
        ],
        copilot=[
            "Not recorded on this host: where a session reads its own link.",
            "`send_message` takes a session link (see `message-chief`).",
        ],
    ),
    dict(
        id="start-driver",
        name="Start a Driver or a worker",
        roles=STEER,
        mark=P,
        claude=[
            "`Agent` with `subagent_type: chantier:<role>`; `run_in_background: true` for a Driver.",
            "The `model` parameter only when `$CHANTIER` printed a start value (an alias), as printed; no effort.",
        ],
        copilot=[
            "`task`, `mode: background`, `agent_type: <agent>`; the plugin's agent is `chantier-<role>`; no model, no effort.",
            "The CLI prints the plugin's agent or yours; when it prints `agent=(generic)`, use `start-generic-agent` instead.",
        ],
    ),
    dict(
        id="model-at-start",
        name="Models at an agent's start",
        roles=STEER,
        mark=U,
        claude=[
            "A named agent starts with a model through the `model` parameter of `Agent`, set to an alias: `opus`, `sonnet` or `haiku`.",
            "The CLI maps the identifier to the alias: `claude-opus-5-5` is `opus`, `claude-sonnet-5-5` is `sonnet`, `claude-haiku-5-5` is `haiku`.",
            "The full identifier is not recorded as accepted; the agent's tools stay unchanged.",
        ],
        copilot=[
            "A named plugin agent runs on its file's model: given another model, the host replaces it with the file's.",
            "A generic agent takes the model passed; the start value is the identifier (the display name in lower case, spaces as `-`, dots kept).",
            "A model changed in the configuration starts a generic agent; the user's own agent with a model is refused.",
        ],
    ),
    dict(
        id="start-generic-agent",
        name="Start a generic agent",
        roles=STEER,
        mark=U,
        claude=[
            "Not on this host as a separate start: a configured model goes through the `model` parameter of `Agent` (see `model-at-start`).",
            "The role runs as its named agent `chantier:<role>` with that model, its tools unchanged.",
        ],
        copilot=[
            "`task`, `mode: background`, the generic agent (`agent_type: general-purpose`), `model:` the printed start value.",
            "The prompt carries the printed contract lines; its tools are the caller's, not restricted.",
        ],
    ),
    dict(
        id="model-ran-on",
        name="The model a role ran on",
        roles=FOREMAN,
        mark=U,
        claude=[
            "Not recorded on this host: no step reads the model back after a start.",
            "The model a role ran on is the one its transcript shows.",
        ],
        copilot=[
            "The steering session's `events.jsonl`: `subagent.started` and `subagent.completed` carry `model`, `firstDispatchedModel`, `modelSelectionSource`.",
            "After a start with a model, read that `model`; when it differs from the printed identifier, stop the agent's work and report both.",
        ],
    ),
    dict(
        id="start-spec-writer",
        name="Start the Spec-writer",
        roles=["chief-of-staff"],
        mark=U,
        claude=[
            "`Agent` with `run_in_background: true` and `subagent_type: chantier:spec-writer`; no effort.",
            "The `model` parameter as in `start-driver`, only when `$CHANTIER playbook` printed one.",
        ],
        copilot=[
            "`task`, `mode: background`, `agent_type: chantier-spec-writer`; no model, no effort.",
            "The CLI prints the plugin's agent or yours; when it prints `agent=(generic)`, use `start-generic-agent` instead.",
        ],
    ),
    dict(
        id="start-spec-critic",
        name="Start the Spec critic",
        roles=["chief-of-staff", "griller"],
        mark=U,
        claude=[
            "`Agent` with `run_in_background: true` and `subagent_type: chantier:spec-critic`; no effort.",
            "The `model` parameter only when `$CHANTIER playbook` printed one or the user asked for Fable.",
        ],
        copilot=[
            "`task`, `mode: background`, `agent_type: chantier-spec-critic`; no model, no effort; Fable is not recorded on Copilot.",
            "The CLI prints the plugin's agent or yours; when it prints `agent=(generic)`, use `start-generic-agent` instead.",
        ],
    ),
    dict(
        id="start-retro-critic",
        name="Start the Retro critic",
        roles=FOREMAN,
        mark=U,
        claude=[
            "`Agent` with `subagent_type: chantier:retro-critic`; no effort.",
            "The `model` parameter only when `$CHANTIER playbook` printed one or the user asked for Fable.",
        ],
        copilot=[
            "`task` with `agent_type: chantier-retro-critic`; no model, no effort; Fable is not recorded on Copilot.",
            "The CLI prints the plugin's agent or yours; when it prints `agent=(generic)`, use `start-generic-agent` instead.",
        ],
    ),
    dict(
        id="message-driver",
        name="Message a Driver",
        roles=FOREMAN,
        mark=P,
        claude=[
            "`SendMessage` to the Driver's agent id.",
            "A Driver that stopped resumes, with its context, when it gets the message (see `resume-subagent`).",
        ],
        copilot=[
            "`write_agent` to the Driver's agent id.",
            "A stop is the same tool with `[foreman→driver <cr>] stop` (see `stop-driver`).",
        ],
    ),
    dict(
        id="message-chief",
        name="Message the Chief of Staff",
        roles=["foreman", "griller"],
        mark=P,
        claude=[
            "`SendMessage` to the Chief of Staff's session id.",
            "The Foreman's lines and a Griller's `ready` line travel the same way.",
        ],
        copilot=[
            "`send_message` to the Chief of Staff's session link.",
            "The Foreman's lines and a Griller's `ready` line travel the same way.",
        ],
    ),
    dict(
        id="driver-hand-back",
        name="A Driver's final report to a Foreman's Desktop session",
        roles=DRIVERS,
        mark=P,
        claude=[
            "For a steering session of Claude Desktop (id `local_…`), a Driver sends one message: its final report, by `SubagentHandback`, at its end.",
            "Before its end a background subagent has no means to reach that session, and `SendMessage` to `main` does not reach it.",
            "The report's first line is the hand-back line, then every other line due (`anomaly`, `push`), one per line, as the cards word them.",
            "An `anomaly` is recorded when it happens: `$CHANTIER note <cr> \"anomaly: <text>\"`.",
        ],
        copilot=[
            "The Driver's final answer is its hand-back to its steering session (the Foreman).",
            "In direct mode the final answer returns to the Chief of Staff that started the Driver.",
        ],
    ),
    dict(
        id="driver-messages-steering-direct",
        name="A Driver messages its steering session in direct mode",
        roles=DRIVERS,
        mark=U,
        claude=[
            "Direct mode run from Claude Desktop: the final report only, as `driver-hand-back` says, once, at the Driver's end.",
            "Direct mode run from a terminal or VS Code: `SendMessage` to `main`, and the `Steering:` line names it.",
        ],
        copilot=[
            "In direct mode the Driver's final answer returns to the Chief of Staff that started the Driver.",
            "No earlier message from the Driver to that session is recorded on this host.",
        ],
    ),
    dict(
        id="stop-driver",
        name="Stop a Driver",
        roles=FOREMAN,
        mark=P,
        claude=[
            "`TaskStop` with the Driver's agent id.",
            "After a Driver's own `TaskStop` with no restart at once, the steering session clears the recorded id.",
        ],
        copilot=[
            "`write_agent` to the Driver's agent id with `[foreman→driver <cr>] stop`.",
            "The steering session sends it; no other route is used.",
        ],
    ),
    dict(
        id="stop-woken-driver",
        name="Stop an ended Driver that wakes again",
        roles=FOREMAN,
        mark=U,
        claude=[
            "`TaskStop` with the Driver's agent id, as in `stop-driver`.",
            "Whether it also ends the background tasks that Driver left running is not known: say so, never tell it as a fact.",
        ],
        copilot=[
            "Not recorded on this host: the stop of an ended Driver that wakes again.",
            "A Driver stopped from outside is read when the host says it was stopped (`foreman-lost-driver.md`).",
        ],
    ),
    dict(
        id="driver-start-folder",
        name="A CR Driver's start folder",
        roles=["cr-driver"],
        mark=U,
        claude=[
            "A CR Driver starts in the folder the plugin's mod gives it, as `write-guard` says.",
            "That is its worktree, or the project's root while the worktree does not exist yet.",
        ],
        copilot=[
            "A Driver starts in the folder the host gives it; no mod moves it.",
            "The write guard's start folder does not apply here (see `write-guard`).",
        ],
    ),
    dict(
        id="stop-own-background-task",
        name="Stop a background task of one's own",
        roles=DRIVERS,
        mark=U,
        claude=[
            "`TaskStop` with the id the start returned (`Bash` or `PowerShell` with `run_in_background: true`, or `Monitor`).",
            "The Driver agents list `TaskStop` in their tools for it.",
        ],
        copilot=[
            "The host's stop of a background shell, within the agent's `execute` tool set.",
            "A Driver stops its CI watch before its hand-back.",
        ],
    ),
    dict(
        id="name-env-holders",
        name="Name the holders of the checkout's environment",
        roles=FOREMAN,
        mark=U,
        claude=[
            "Windows, the `PowerShell` tool: `Get-CimInstance Win32_Process` filtered on an `ExecutablePath` under `<plugin root>\\.venv\\`, showing PIDs and `CommandLine`.",
            "macOS and Linux, the `Bash` tool: `ps -eo pid,ppid,args | grep -F \"<plugin root>/.venv/\"`, the grep line itself excluded.",
            "A `chantier.exe` and its child `python.exe` are one holder, named by the top process's PID, subcommand and `--project` value.",
            "Read-only: never `Stop-Process`, `taskkill` or `kill` on a holder.",
        ],
        copilot=[
            "The same commands through the host's shell tool: on Windows `Get-CimInstance Win32_Process` under `<plugin root>\\.venv\\`.",
            "On macOS and Linux `ps -eo pid,ppid,args | grep -F \"<plugin root>/.venv/\"`, the grep line itself excluded.",
            "Read as on Claude Code, \"own\" by its evidence (`--seat <this session's id>`).",
            "Read-only: never a stop or a kill of a holder.",
        ],
    ),
    dict(
        id="stop-session",
        name="Stop another session",
        roles=["chief-of-staff"],
        mark=U,
        claude=[
            "`mcp__ccd_session_mgmt__stop_session` with the session's id (a Foreman not answering, on the user's yes).",
            "Whether it works from Remote Control is not recorded on this host.",
        ],
        copilot=[
            "Not recorded on this host: how a session stops another session.",
            "A missing tool is reported with its text; no other route is used.",
        ],
    ),
    dict(
        id="agent-ids",
        name="Agent ids of the project",
        roles=["chief-of-staff"],
        mark=P,
        claude=[
            "The `name:` of a file in `.claude/agents/` or `~/.claude/agents/`.",
            "The plugin's own agents are `chantier:<role>`.",
        ],
        copilot=[
            "A file in `.github/agents/` or `~/.copilot/agents/`.",
            "The plugin's own agents are `chantier-<role>`.",
        ],
    ),
    dict(
        id="models",
        name="Models",
        roles=["chief-of-staff", "foreman"],
        mark=U,
        claude=[
            "The Spec-writer, the Spec critic and the Retro critic run Opus 5.5; the Foreman, every Driver and the workers run Sonnet 5.5.",
            "Unless the configuration (`hosts.<host>.roles`) sets one; the defaults are `config/chantier.defaults.yml`'s.",
            "A task under escalation runs the role's `escalation` model, printed by `$CHANTIER playbook` (`coder`, `debugger`, `conflict-resolver`).",
        ],
        copilot=[
            "Each plugin agent's file names its model (Luna, Sol, Terra, Sonnet 5.5 or Opus 5.5); it runs when no model is passed.",
            "Each file sets `model-policy: required` except `chantier-coder`'s; defaults are `config/chantier.defaults.yml`'s unless `hosts.<host>.roles` sets one.",
            "An identifier is the display name in lower case, spaces as `-`, dots kept; the list comes from `just copilot-models`.",
            "An escalated role (`coder`, `debugger`, `conflict-resolver`) starts as a generic agent on its model, printed `(generic)`.",
        ],
    ),
    dict(
        id="session-skills-tools",
        name="Skills and tools of a session",
        roles=["chief-of-staff"],
        mark=U,
        claude=[
            "Not recorded on this host: how a session lists its skills and tools, and whether a subagent sees what the session sees.",
            "The Chief of Staff compares a role's needs with what it can tell.",
        ],
        copilot=[
            "Not known on this host: how a session lists its skills and tools.",
            "The Chief of Staff compares a role's needs with what it can tell.",
        ],
    ),
    dict(
        id="preflight-p2",
        name="Preflight P2",
        roles=["chief-of-staff", "foreman"],
        mark=P,
        claude=[
            "`mcp__ccd_session__start_session` loads.",
            "Preflight P2 passes when that tool is available to the session.",
        ],
        copilot=[
            "`create_session` and `send_message` load.",
            "Preflight P2 passes when both tools are available to the session.",
        ],
    ),
    dict(
        id="ask-questions",
        name="Ask the user a series of questions",
        roles=["chief-of-staff", "griller"],
        mark=U,
        claude=[
            "The host's question tool (`AskUserQuestion`): at most 4 questions per call, at most 4 options per question, plus its own free answer (\"Other\").",
            "The reference opens each question's text; the tool's short header field, if used, need not hold it.",
            "Remote Control relays the same tool: the same 4-question form shows on the phone, above the conversation.",
            "The text is written before every call all the same.",
        ],
        copilot=[
            "The host's question tool, at most 5 questions per call, at most 4 options per question.",
            "The reference opens each question's text; the tool's exact name and its free answer are not recorded here.",
        ],
    ),
    dict(
        id="run-board",
        name="Run the board",
        roles=["chief-of-staff"],
        mark=U,
        claude=[
            "`Bash` with `run_in_background: true` and the command `$CHANTIER serve --seat <id>`; `$CHANTIER serve --restart --seat <id>` runs the same way.",
            "Add `--forge-always` on a host that cannot run the watcher.",
            "Read its first lines from the background task's output; stop it with the host's stop of a background shell.",
        ],
        copilot=[
            "The host's background shell with the command `$CHANTIER serve --seat <id>`; `serve --restart --seat <id>` runs the same way.",
            "Add `--forge-always` on a host that cannot run the watcher; read the first lines from the output; stop it with the host's stop of a background shell.",
            "If the host has no background command, give the one line of `session-start.md` and go on: no workaround.",
        ],
    ),
    dict(
        id="board-griller",
        name="The board's Griller",
        roles=["board-griller", "griller"],
        mark=U,
        claude=[
            "The surface server starts `claude -p` with the JSON output, as the agent `chantier:board-griller` with `--model <effective model>`.",
            "The conversation is fixed by an id and resumed by it; the prompt goes on standard input; no user, project or local settings load; the plugin loads explicitly.",
            "The run works from an allow list alone (the Griller card's \"Started from the board\"); the exact flags are not recorded on this host.",
        ],
        copilot=[
            "`copilot -p` is the intended run.",
            "The Grill action refuses on Copilot with one line: grill in a session with the Griller skill.",
        ],
    ),
    dict(
        id="workspace-trust",
        name="Trust of a workspace inside a trusted folder",
        roles=["chief-of-staff"],
        mark=U,
        claude=[
            "A folder the user trusted once in Claude Desktop at the desk covers every new folder created inside it later.",
            "A session started on such a folder from Remote Control does not ask for trust.",
        ],
        copilot=[
            "Not recorded on this host: how Copilot trusts a workspace.",
            "A refused start is reported with its exact text.",
        ],
    ),
    dict(
        id="move-session",
        name="Move a started session to another folder",
        roles=["chief-of-staff"],
        mark=P,
        claude=[
            "A session started with no `cwd` may move with `mcp__ccd_directory__change_directory` into a folder inside a trusted folder.",
            "No question is asked in auto mode and the next turn runs there; project instructions do not reload (the session keeps its own `AGENTS.md`).",
            "`clear_session` on another id is denied by the auto mode classifier; no chantier route uses it.",
        ],
        copilot=[
            "Not recorded on this host: moving a started session to another folder.",
            "A refused start or move is reported with its exact text; no other route is used.",
        ],
    ),
    dict(
        id="prompt-cache-ttl",
        name="Prompt cache TTL",
        roles=FOREMAN,
        mark=U,
        claude=[
            "A session's cache writes are 1-hour (`cache_creation.ephemeral_1h_input_tokens` in its transcript's usage).",
            "A subagent's cache writes are 5-minute (`ephemeral_5m_input_tokens`).",
        ],
        copilot=[
            "Not known on this host: how long a session's prompt cache keeps a prefix.",
            "The `cache_ttl` default is `5m`.",
        ],
    ),
    dict(
        id="steering-wake-bound",
        name="Steering wake bound (60 minutes)",
        roles=FOREMAN,
        mark=U,
        claude=[
            "The CLI refuses a `steering_wake` over 60 minutes.",
            "The shipped default is 55 minutes (3300 seconds), scheduled with `ScheduleWakeup`.",
        ],
        copilot=[
            "`/every` takes whole minutes: the CLI refuses a Copilot duration that is not whole minutes.",
            "The heartbeat uses `/every 4m` today.",
        ],
    ),
    dict(
        id="heartbeat",
        name="Heartbeat",
        roles=FOREMAN,
        mark=P,
        claude=[
            "The steering session runs the `/loop` skill in dynamic mode; its prompt is `chantier status --refresh --batch <batch> --epoch <n>` alone, with no interval.",
            "Each wake is scheduled with `ScheduleWakeup`, the steering wake of the `timing: Claude Code session:` line `chantier playbook` prints, in seconds.",
            "It ends with `ScheduleWakeup` `stop: true`, after `chantier status --stop-heartbeat --batch <batch> --epoch <n>`; it never ends the session.",
            "An order's line or a `ping` starts a turn; if a Driver is left running, the heartbeat is armed again.",
        ],
        copilot=[
            "The Chief of Staff sends the Foreman chat `/every <steering wake> chantier status --refresh --batch <batch> --epoch <n>` on its `ready <batch>`.",
            "The wake comes from the batch's `timing: Copilot <family> models:` line, else `timing: Copilot other models:`, in `/every`'s form (`4m` by default).",
            "The Foreman cannot end `/every`: at every pause the Chief of Staff tells the user to delete it; in direct mode it runs `/every` in its own session.",
            "Whoever ends the heartbeat first records it with `chantier status --stop-heartbeat --batch <batch> --epoch <n>`.",
        ],
    ),
    dict(
        id="run-watcher",
        name="Run the watcher",
        roles=FOREMAN,
        mark=U,
        claude=[
            "`Monitor`, with no timeout, running the command the `watch: not running` or `still running` line prints, as is (it ends with `--stream`).",
            "Each notification (event lines closed by `... still watching`) and the monitor's end start a turn of the idle session.",
            "On the `no event for <name> in 2 h` line, start again at once as printed, nothing told.",
            "Auto mode drops every `Monitor` allow rule, so the start is the classifier's call.",
        ],
        copilot=[
            "The host's background shell with the command the `watch: not running` or `still running` line prints, as is (no `--stream`: it ends after each block).",
            "Its end must start a turn of the idle Chief of Staff session; its output is read from the task.",
            "Until then the Chief of Staff also runs the printed `watch --once` command at each user message.",
            "With no background command, or an end that starts no turn, no watcher starts and one line says so: no workaround.",
        ],
    ),
    dict(
        id="watcher-session-end",
        name="The watcher when the session ends",
        roles=FOREMAN,
        mark=U,
        claude=[
            "Not recorded on this host: whether the host ends a background command when the session ends.",
            "An orphaned watcher ends by the CLI's own rules: when the project's seat is another session's, or after 2 h with no event and no batch in flight.",
        ],
        copilot=[
            "Not recorded on this host: whether the host ends a background command when the session ends.",
            "An orphaned watcher ends by the CLI's own rules, once the project's seat is another session's.",
        ],
    ),
    dict(
        id="board-session-end",
        name="The board when the session ends",
        roles=["chief-of-staff"],
        mark=U,
        claude=[
            "Not recorded on this host: whether the host ends a background command when the session ends.",
            "The board stops when the seat moves (the CLI); a board a watcher started stops 30 minutes after its last client.",
        ],
        copilot=[
            "Not recorded on this host: whether the host ends a background command when the session ends.",
            "The board stops when the seat moves (the CLI); a board a watcher started stops 30 minutes after its last client.",
        ],
    ),
    dict(
        id="message-limit",
        name="Limit on messages",
        roles=SESSION,
        mark=U,
        claude=[
            "Claude Desktop limits messages between sessions: 10 since someone last typed.",
            "A refused send is reported, never sent another way; the limit applies to the lines between a Griller and the Chief of Staff, and to a hand-over's.",
        ],
        copilot=[
            "Not recorded on this host.",
            "A refused send is reported, never sent another way.",
        ],
    ),
    dict(
        id="end-turn-background",
        name="End a subagent's turn with nothing running in the background",
        roles=DRIVERS,
        mark=P,
        claude=[
            "The host asks a subagent for its hand-back at once (`[handback-send-enforce] Your report has not been delivered. Call SubagentHandback…`).",
            "It asks before a resumed worker's reply arrives; a background shell's end wakes the subagent (the CI wait of `driver.md`).",
        ],
        copilot=[
            "Not recorded on this host: how a subagent's turn ends with nothing running in the background.",
            "A Driver's final answer is its hand-back (see `driver-hand-back`).",
        ],
    ),
    dict(
        id="subagent-stops",
        name="A background subagent stops",
        roles=FOREMAN,
        mark=P,
        claude=[
            "`<task-notification>` summary `Agent \"<name>\" is waiting on its own background work`: it stopped with its own work running and resumes when that reports.",
            "`Agent \"<name>\" finished`: it stopped with no live background child, and its `SubagentHandback` report arrives as a message.",
        ],
        copilot=[
            "Not recorded on this host: the notices that tell a background subagent stopped or finished.",
            "A Driver's final answer is its hand-back (see `driver-hand-back`).",
        ],
    ),
    dict(
        id="subagent-stopped-outside",
        name="A background subagent is stopped from outside",
        roles=FOREMAN,
        mark=U,
        claude=[
            "The steering transcript's `attachment` record `task_status` with `status: \"killed\"` and the agent's id as `taskId`, seen as `Task \"<name>\" (<id>) was stopped.`",
            "A message to the stopped agent is refused. What a stop by the user in the app leaves in the transcript is not recorded.",
        ],
        copilot=[
            "A Driver stopped from outside is read when the host says the Driver was stopped (`foreman-lost-driver.md`).",
            "What a user's stop leaves in the session's record is not recorded on this host.",
        ],
    ),
    dict(
        id="resume-subagent",
        name="Resume a stopped subagent",
        roles=FOREMAN,
        mark=P,
        claude=[
            "`SendMessage` to a stopped subagent's agent id resumes it with its context.",
            "Not for a subagent the host stopped (`task_status` `killed`): the message gets `Agent <id> was stopped and won't be resumed. Treat its work as cancelled; ...`.",
            "A refused agent answers a `taken back:` or `record your hand-back` note with its refusal.",
        ],
        copilot=[
            "Not recorded on this host: resuming a stopped subagent.",
            "`write_agent` to the agent id is the message to a Driver; whether it resumes a stopped one is not known.",
        ],
    ),
    dict(
        id="compact",
        name="Compacting",
        roles=FOREMAN,
        mark=U,
        claude=[
            "`/compact` continues the same conversation; connected devices follow it, `$CHANTIER cost` keeps the transcript, and `/clear` may replace it.",
            "No role runs it: the person types it. The window is `autoCompactWindow` (100000 to 1000000), capped at the model's context window.",
            "`idleCompaction` (default true) compacts after about an hour idle; `/autocompact` and the setting set the window.",
        ],
        copilot=[
            "Name no compacting command or setting to the user.",
            "The manual reload (\"chantier reload\") is the only reload after a compaction.",
        ],
    ),
    dict(
        id="reload-after-compact",
        name="Reload after a compaction",
        roles=["chief-of-staff", "griller"],
        mark=U,
        claude=[
            "The plugin's mod hooks `session.compact`: after each compaction of a session that loaded a chantier role skill, it adds one reload message.",
            "The message tells the role to call its chantier skill again with the argument `reload`; the answer opens with one line saying the rules were reloaded.",
            "It leaves a subagent's own compaction alone and never vetoes one; the manual reload (`/chantier:chantier reload`) works everywhere.",
        ],
        copilot=[
            "Not done on this host: Copilot has no mod (its manifest names no hooks).",
            "The manual reload (\"chantier reload\", `session-start.md`, \"Reload\") is the only one.",
        ],
    ),
    dict(
        id="write-guard",
        name="The write guard",
        roles=WRITERS,
        mark=U,
        claude=[
            "The plugin's mod reads the `writes: <folder>; <folder>` line of a spawn's prompt and starts the agent in the first folder (a `worktree:` line wins).",
            "That agent's Write, Edit or NotebookEdit outside every folder is refused: `refused: <path> is outside the folders this agent may write in (...); write there`.",
            "Its shell writes (`>`, `tee`, `sed -i`, `cp`, `mv`, `rm`, `Set-Content`, `Out-File`) follow the same rule; `git`, `gh`, `glab` and the chantier CLI pass.",
            "Not guarded: the main session, the Release, stack and QA drivers, the Spec agents, the Griller, the Demo explorer, any agent with no `writes:` line.",
        ],
        copilot=[
            "Copilot has no hook (its manifest names none): no guard refuses a write outside the `writes:` folders.",
            "The `writes:` line is inert there; the card's rule alone covers a worker's writes.",
        ],
    ),
    dict(
        id="griller-in-worktree",
        name="A Griller in a worktree",
        roles=["griller", "chief-of-staff"],
        mark=U,
        claude=[
            "A Griller in a worktree sends its files by `SendMessage` to the seat's session, naming the absolute paths.",
            "The Chief of Staff on the main checkout reads them under `.claude/worktrees/<name>/`.",
        ],
        copilot=[
            "A Griller in a worktree sends its files as on Claude Code: by message to the seat's session, naming the absolute paths.",
            "The message is `send_message` to the session's link (see `message-session`).",
        ],
    ),
    dict(
        id="surface-session-writes",
        name="A session in a planning surface writing in the project's clone",
        roles=["chief-of-staff", "foreman", "griller", "cr-driver"],
        mark=U,
        claude=[
            "A session in a planning surface writes the planning folder by absolute paths, and the project's clone and worktrees outside its own folder.",
            "The host must allow those folders: add the clone and its worktrees folder as working directories (`/add-dir <path>`, or `additionalDirectories`).",
        ],
        copilot=[
            "A session in a planning surface writes the project's clone and worktrees outside its own folder; that folder may be the surface's checkout or the clone.",
            "The host must allow those folders; the remote finding is Claude Code's and was not run on Copilot.",
        ],
    ),
]

assert len(ROWS) == 50
assert sum(r["mark"] == P for r in ROWS) == 13, sum(r["mark"] == P for r in ROWS)
