# Evidence 4: `help` after the swap

Worktree `batch-31-CR-510`, uncommitted tree (base `88d9ab40`), 2026-11-26. `$W` is the worktree,
`$S` the CR folder's `work/scratch`.

## The names the CLI source prints

`git grep -h -o "help [a-z][a-z0-9-]*" -- skills/chantier/scripts/cli/src`, counted with
`sort | uniq -c`, exit 0:

```text
      4 help board
      3 help from
      1 help h2
      1 help host-allow-not-add
      6 help lease
      1 help lists
      1 help merge
      1 help of
      1 help refused-push
      1 help stack
      2 help stack-merge
      1 help takes
      2 help topic
      1 help topics
      5 help watcher
```

Eight are topic names: `board` and `watcher` (`hub/watch_lines.py`), `host-allow-not-add` (a
comment, `commands/permissions.py:28`), `lease` (`commands/push.py:32`, `core/leases.py`),
`merge` (`status/ready_line.py:99`), `refused-push` (`commands/push.py:127`), `stack`
(`stack_shape.py:58`) and `stack-merge` (`status/due.py:41` and `:45`). The others are prose or
code, not a topic name: `help from` and `help h2` (the web client's files), `help lists`, `help
takes`, `help topics` (`commands/help.py`), `help of` (`commands/registry.py`), `help topic`
(`retro_draft.py`, `declare/help.py`). A search for a name built at run time (`help {`) finds only
the "did you mean" line of `commands/help.py:134`; `help <topic>` is the closing line of every
brief (`commands/brief.py:53`).

## The runs

`uv run --no-sync --project $W python $S/e4_help.py $W board host-allow-not-add lease merge
refused-push stack stack-merge watcher` (calls `chantier.cli.main` with each argument list),
exit 0, `failed runs: 0`.

The topic list, `chantier help`, exit 0: 240 topic lines under this header (first three shown):

```text
topics: 240; help <topic> prints one, help --for <role> lists a role's
worker-shell: a shell call that chains, assigns or waits; a file write (coder, conflict-resolver, debugger, investigator, verifier, demo-explorer, inspector)
session-shell: a shell call that waits, backgrounds or changes folder; a text for the forge (cr-driver, release-driver, stack-driver, qa-driver, chief-of-staff, foreman, griller, spec-writer, spec-critic, retro-critic)
verifier-scratch: a scratch project to make; a path too long for Windows (verifier)
```

One run per name the source prints, each its readings with exit 0:

```text
help board: exit 0, 14 lines, 2095 bytes, first: topic board: the board, the surface server, `serve`, a `board` line (chief-of-staff)
help host-allow-not-add: exit 0, 11 lines, 701 bytes, first: topic host-allow-not-add: a rule auto mode drops, a rule not to propose (chief-of-staff)
help lease: exit 0, 22 lines, 3052 bytes, first: topic lease: a `--lease` refusal, `claim lost`, a lease `not confirmed`, a wait over 3 minutes (cr-driver, stack-driver, qa-driver, release-driver, foreman, chief-of-staff)
help merge: exit 0, 13 lines, 1627 bytes, first: topic merge: an `order merged`, a CR ready to merge, a merge recorded (foreman, chief-of-staff)
help refused-push: exit 0, 65 lines, 9203 bytes, first: topic refused-push: `push <cr>` exit 4, a force push or rebase the host refuses (cr-driver, stack-driver, release-driver, foreman, chief-of-staff)
help stack: exit 0, 15 lines, 2568 bytes, first: topic stack: a stack batch: `status` shows `shape stack` (foreman, chief-of-staff)
help stack-merge: exit 0, 10 lines, 1577 bytes, first: topic stack-merge: a merge recorded in a stack batch (foreman, chief-of-staff)
help watcher: exit 0, 9 lines, 1618 bytes, first: topic watcher: a `watch: not running` line, the session's first yes (chief-of-staff)
```

The same eight names through the CLI's entry point,
`uv run --no-sync --project $W chantier help <name>`, one run each: all `exit=0`.

## `help --for`, the 18 roles of `roles.yaml`

```text
roles: 18
help --for cr-driver: exit 0, 40 lines
help --for release-driver: exit 0, 31 lines
help --for stack-driver: exit 0, 30 lines
help --for qa-driver: exit 0, 4 lines
help --for coder: exit 0, 1 lines
help --for conflict-resolver: exit 0, 1 lines
help --for debugger: exit 0, 1 lines
help --for inspector: exit 0, 2 lines
help --for investigator: exit 0, 1 lines
help --for verifier: exit 0, 7 lines
help --for spec-writer: exit 0, 2 lines
help --for spec-critic: exit 0, 1 lines
help --for board-griller: exit 0, 1 lines
help --for retro-critic: exit 0, 1 lines
help --for demo-explorer: exit 0, 1 lines
help --for chief-of-staff: exit 0, 183 lines
help --for griller: exit 0, 26 lines
help --for foreman: exit 0, 74 lines
```

`board-griller` has no topic: its one line is `no topic for board-griller; help lists them all`,
exit 0.
