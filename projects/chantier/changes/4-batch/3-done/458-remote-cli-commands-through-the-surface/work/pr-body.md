## Summary

A machine can now log in to a chantier surface server (`chantier login <link>`, like `gh auth login`). After that, every chantier command run there for the projects it logged in for goes to that server, which runs it in its own planning folder and returns the output and the exit code. Projects the profile was not logged in for, a project of the same name served by another surface, and the server's own machine without a login stay local.

## Deliverables

A new `cli.run` operation on the server, and a client that forwards commands to it:

```mermaid
sequenceDiagram
    participant C as chantier (client machine)
    participant P as profiles.json
    participant S as surface server
    C->>P: read the default profile (url, key, projects, origin)
    C->>S: POST api/v1/call/cli.run {argv, project, env, stdin}
    S->>S: check argv with the CLI's parser; start a child, profile local
    S-->>C: {code, stdout, stderr, version, launch}
    C->>C: swap the server's launch form for its own, print, exit with code
```

| Command | Under an active private profile |
| --- | --- |
| `serve`, `watch` | local, profiles never read |
| `login`, `logout`, `live`, `webui` | local; `live` watches the profile's server, `webui` prints its link |
| `gate` | refused (runs on this machine) |
| every other command (`open`, `order`, `take`, `round`, `file`, `status` ...) | forwarded |

A read-only profile serves `live` and `webui`; every forwarded command is refused before any request.

- Profiles live in one file, `chantier/profiles.json` in the user's config folder (`CHANTIER_CONFIG_HOME`, else `%APPDATA%`, else `XDG_CONFIG_HOME` or `~/.config`), mode 0600; a profile tells surfaces apart by the `origin` of the repository behind the server.
- `login` makes the new profile the default (`--no-default` keeps the old one); `logout` removes it; `--profile local` runs one command here.
- The server never trusts the client: it re-checks `argv` with the real parser, refuses `--project`/`--profile`/`--skill` and environment names outside a fixed list, and runs the command as a child of its own build with no profile, so no loop is possible. A running `cli.run` keeps the server from stopping when idle.

## Blast radius

Grade: 2. New client and server paths plus a hook in `cli.main` that every command passes; with no profile every command runs as before. Revert restores the previous behaviour; a profile file left behind is inert.

## Autonomous decisions

- `board.get` also returns the server's home project (`home`) besides `origin`, because `login` needs it to default `--project`.
- `lease <unit> hold` is forwarded, since the lease hold change is already under this branch.
- The eval kit sets `CHANTIER_CONFIG_HOME` in the workspace's session settings, beside the workspace, so a maintainer's profiles never turn an eval remote.

## Known gaps

- No remote watcher: a session working through a profile is not woken by merges, CI or board events; it reads `status` each turn.
- A real eval under a profile is untested; the kit's isolation is checked by the dry run only.

<details>
<summary>Details</summary>

## Changes

- New `clients/profiles.py` (file, folder, active-profile rule), `clients/remote.py` (the forwarding client), `commands/login.py` and `declare/remote.py` (`login`, `logout`), `board/cli_run.py` (the op), `core/origin.py`, `core/remote_wire.py`.
- `cli.py`: the `--profile` root option and the forwarding step; `board/api` registers `cli.run` and `board.get` returns `origin`; `board/idle.py` counts a running `cli.run`; `live` and `webui` read the active profile.
- `docs/server-api.md`, `AGENTS.md`, the Chief of Staff card's routing table, the eval kit's environment, the scenario's `remote_cli` case and the tests.

## Human decisions

- Every command runs remotely once logged in, batch commands included (`order`, `open`, `cancel`).
- The private key is needed to run commands; the read-only key serves `live` and `webui` only.
- A profile applies only to the projects it was logged in for and to the surface it names (its `origin`); a command that cannot pick a project stops and asks, never going to the profile's first.
- No remote watcher in this change: `watch` stays local.
- `webui` under a profile prints the profile's link and starts nothing.

## Impacts

Users get remote commands after one `login`; developers get the `cli.run` op documented in `docs/server-api.md`. No visual change.

## Test plan

- [x] New or changed tests (they fail on the previous code): `tests/test_remote_cli.py`
- [x] Local gates: `just check`, `just eval-dry-run` at 6f91973 (before the first push); scenario case `remote_cli` in CI at bfdf5a2
- [x] Evidence: none, no visual change
- [x] Review: approved, and again after the rebase onto main at bfdf5a2
- [x] Verified: VERIFIED at bfdf5a2
- [x] CI green: `gh pr checks 434` at bfdf5a2: `just check` (ubuntu, macos, windows), `just scenario (ubuntu-latest)` and `just eval-dry-run` pass

## Internal references

CR-458 remote-cli-commands-through-the-surface (batch-30, on top of CR-457).

</details>
