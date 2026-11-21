## Summary

`chantier board` listened on every network address by default, in plain HTTP, behind a key that never expired and sat in a one-year cookie. Anyone on the local network who read the key could rewrite a specification and queue it for the Drivers. The board now stays on this machine unless the user opens it, its key can be replaced with one command, and the phone on the local network stays reachable as a conscious choice that follows the machine's address.

## Deliverables

Start lines, by setting:

| Setting | Listens on | Start lines |
| --- | --- | --- |
| none (new default) | `127.0.0.1` | `board on http://127.0.0.1:<port>/?k=<key> over <folder>` |
| `board.host: network` (an address is found at this start) | `0.0.0.0` | link on the found address, `on this machine: http://127.0.0.1:...`, `board: listens on the local network (0.0.0.0); ...` |
| `board.host: network`, no network | `127.0.0.1` | one `board on http://127.0.0.1:...` line, then `board: no local network address found; on this machine only` |
| `--host <address>` | that address | the option wins, for one start |

- `chantier.yaml` accepts only the word `network` for `board.host`; a fixed address there is refused with a message pointing to `--host`, so a shared file never breaks another machine.
- The local network address is found at each start and never stored, so a new address from DHCP is followed at the next start.
- A second `chantier board` while a network-open board runs now also prints the `board: listens on the local network` line.
- The cookie lasts 30 days (was one year). `chantier board --new-key` (already present) replaces the key while the board runs: old link, cookies and open pages stop at once.

## Blast radius

Grade: 2

The default address changes for every user of `chantier board`: a phone that reached the board before needs `board.host: network` (or `--host`) and a restart. A fixed `board.host` in an existing `chantier.yaml` is now refused. Revert restores the old default.

## Autonomous decisions

- The `board` configuration check moved from `playbook/config.py` into a new `playbook/board_check.py`, because `config.py` reached the project's file-size cap.

## Known gaps

- The cookie's `Secure` flag and TLS are out of scope: the board stays plain HTTP, since a `Secure` cookie would not reach a phone on a local network address.
- The board does not follow an address change or the network's return while it runs; a restart does.
- **UNVERIFIED:** the pipeline's scenario run (board steps 10 and 11, new checks) has not run at this head yet.

<details>
<summary>Details</summary>

## Changes

- `board/address.py`: default host `127.0.0.1`; `settings()` resolves `board.host: network` through the default-route address at each start and reports the no-network case.
- `playbook/board_check.py` (new) and `playbook/config.py`: `board.host` accepts only `network`; `port` check unchanged.
- `board/key.py`: cookie `Max-Age` 30 days.
- `board/command.py`: `NO_NETWORK` line; the already-running path appends the network line when the board found listens beyond this machine.
- `declare/board.py`: help texts.
- Cards and docs (`chief-of-staff.md`, `session-start.md`, `hosts/claude-code.md`, `README.md`, `docs/web-board.md`, `docs/boards.md`): the default is this machine only, how to open it, how to rotate the key.
- Tests: `test_board_exposure.py` (new), `test_playbook_layers.py`; the scenario's board steps and its README.

## Human decisions

- The board listens on `127.0.0.1` by default and on the network only on request (`chantier.yaml` or `--host`).
- The key stays stable across restarts; `--new-key` replaces it; the full link keeps being printed.
- The network setting holds no fixed address: `board.host: network`, found at each start, listening on every address and keeping the `on this machine:` link.
- With no network at start the board stays on this machine and says so.
- The cookie's `Secure` flag is left out.

## Impacts

Users who read the board from the phone must open it to the network. No visual change in the web client.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`: `just check`, `just eval-dry-run`
- [ ] Evidence: before at `<sha7>`, after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-426 board-exposure.

</details>
