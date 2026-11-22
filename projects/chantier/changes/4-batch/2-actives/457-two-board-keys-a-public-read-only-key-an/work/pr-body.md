## Summary

The surface server had one key: whoever held the link could read the board and change it. This adds a public read-only key that can be shared (it shows the board and acts on nothing) next to the private key, which stays as it was and keeps reading and acting.

## Deliverables

- `chantier/server.json` gains `read_key` (made at a server's start when missing); `key` stays the private key, so every existing link, cookie, watcher and script keeps full rights. `--new-key` replaces both.
- Each request is `read` or `write` by the key it holds (header, cookie or the WebSocket's `hello`); the private key wins when both are present. The read key has its own cookie, `chantier_board_<id>_read`, so the two never overwrite each other.
- Answers carry `X-Chantier-Access`, exposed to CORS; `welcome` carries `access`.
- Under the read key, only an allow-list of read ops (`READ_OPS`) and topics (`READ_TOPICS`) answers; any other op, present or future, answers 403 `refused: the read-only key acts on nothing: use the private link`.
- `serve` and `webui` print a `read-only: <link>` line after the private link; `live --url` takes either link.

```text
read link    -> board.get, project.*, costs.get, prs.get, ... + 6 topics
private link -> everything (backlog.*, config.put, writer.sync, ...)
```

## Blast radius

Grade: 2. Shared auth code of the server and its protocol (`welcome` gains a field). Revert restores the single key; a `read_key` left in `server.json` is ignored by older builds.

## Autonomous decisions

- `board.get` and the board topic's `local_url` carry the read link under the read key (`reads.for_read_key`), so a read-only client never receives the private link.
- The `--ui` and extra serve options moved into `board/options.py`, to keep `command.py` under the file-size limit.

## Known gaps

- The scenario's "board already running" first-server step was skipped on the author's machine (port 8765 held by another program); the full long gate was not run locally.
- The web page does not hide its write controls under the read key: a refused write reaches the page as any refused write does.
- Full `just scenario` on Windows: not run by this PR's author yet.

<details>
<summary>Details</summary>

## Changes

- `board/key.py`, `hub/state.py`: `read_key`, `read_current()`, `set_read_key`.
- `board/api/auth.py`, `ws.py`, `http.py`, `push.py`, `guard.py`, `routes.py`: access by key, cookies, header.
- `board/api/ops.py`, `topics.py`, `protocol.py`, `protocol.json`: allow-lists, `welcome.access`.
- `board/command.py`, `commands/webui.py`, `declare/serve.py`: links and start lines.
- `AGENTS.md`, `docs/server-api.md`, cards, tests and scenario.

## Human decisions

- Two keys: a public read-only one and a private one that acts.
- The read key opens an allow-list of reads only; every other op needs the private key.

## Impacts

A shareable read-only link; the printed start lines gain one line.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_board_read_key.py`, `test_board_exposure.py`, `test_server_api_ws.py`
- [x] Local gates at `53a134e`: `just check` pass (2051 passed), `just eval-dry-run` pass (19 of 19)
- [x] Evidence: after at `53a134e`, a real server on a scratch planning folder; no before (a new capability)
- [x] Review: approved at `53a134e` (reviewed before the commit and the rebase, the patch unchanged)
- [x] Verified at `53a134e`
- [x] CI green at `53a134e`: check on three systems, eval-dry-run and scenario (ubuntu-latest)

## Internal references

CR-457 two-board-keys-a-public-read-only-key-an

</details>
