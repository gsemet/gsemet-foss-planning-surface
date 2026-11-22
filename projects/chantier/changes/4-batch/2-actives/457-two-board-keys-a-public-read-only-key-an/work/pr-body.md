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

None.

## Known gaps

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

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates: `just check`, `just eval-dry-run`
- [ ] Evidence: after at the head
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-457 two-board-keys-a-public-read-only-key-an

</details>
