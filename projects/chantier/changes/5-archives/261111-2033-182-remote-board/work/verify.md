# Verify, CR-182 remote-board

Head: 372aef1

Judged at 372aef1 unless noted. Evidence: `verifier/evidence/before.txt`, `after.txt`, `before-after.md`.

| Claim | Proof | Result |
| --- | --- | --- |
| Spec evidence points 1-10 (scenario step `remote_board`, section 16c, and the board checks in section 20 for the external surface) | `$CHANTIER gate` log `work/gates/20261111-191814.log`: github 506/506 and gitlab 506/506 at 372aef1; the transcript lists 18 board checks in 16c and 3 in 20 (project's folder served, other project and clone refused) | ok |
| Before: `board` is unknown on the base | `before.txt` (base 04ed67b): exit 2, `invalid choice: 'board'` | ok |
| Start line, loopback: one line `board on http://127.0.0.1:8791/ over <folder>` | live run, `uv run --script <cli> board --host 127.0.0.1 --port 8791 --seat s-1` | ok |
| `GET /` 200 `text/html; charset=utf-8`, no-store, nosniff, CSP `default-src 'none'; style-src 'unsafe-inline'...`, a `<b>` title escaped | `after.txt` | ok |
| `/api/status` schema 3, `seat` s-1, `board` true, `planning_folder` | `after.txt` | ok |
| `/file` of a folder and of a file 200; `..`, encoded `..`, absolute (Windows and POSIX), missing, `/zzz` 404; POST, PUT, DELETE 405 | `after.txt` | ok |
| Read only | planning-folder file list, sizes and mtimes identical before and after serving; the scenario's own check passes | ok |
| Reuse: second board prints `board already running at http://127.0.0.1:8791/`, exit 0 | `after.txt` | ok |
| Seat move: after `seat take s-2 --over s-1` and one GET, the board process is gone, the port closed | live run | ok |
| `--host 0.0.0.0` prints the second line (`listens beyond this machine (0.0.0.0, on every network of this machine), no password`) | live run | ok |
| `board.port: abc` is reported by `playbook` with line 2 (exit 2) and `board` refuses with the same line (exit 2) | live run | ok |
| Port held by another program: exit 4 | scenario check (not rerun by hand) | ok |
| PR description: clean (sections, fold, mermaid block), Summary, Deliverables and Changes match the diff stat (board.py, cli.py, state.py, playbook.py, cards, both host references, AGENTS/CONTRIBUTING/README, docstrings, scenario); proofs name 372aef1; no claim stated as fact without proof; the by-hand phone trial is not claimed | `git diff origin/main...HEAD --stat` against `work/pr-body.md` | ok |

By hand, not provable here: opening the board from a phone over Tailscale. It is not claimed as fact in the PR.

Failed claims: none.

## Second pass, Head: 372aef1 (description-pass gaps)

| Claim | Proof | Result |
| --- | --- | --- |
| `/file` serves a real file | `after.txt`, 3rd run, at 372aef1: `GET /file?p=1-inbox/probe-b-bold-b-item/intake/request.md` 200, text escaped in `<pre>`; folder 200. The earlier 404 was a wrong path in my probe (`01-intent.md` does not exist), not a defect | ok |
| No file written while serving | `after.txt`, 3rd run: snapshot of every file under the planning folder (SHA-256 prefix, size, mtime) before and after a serving run with requests and a 32 s wait: identical; `git status --porcelain` unchanged | ok |

Failed claims: none.

## Third pass, rebase 372aef1..a94a027, Head: a94a027

Move onto origin/main (merge-base 7010fa6: CR-174 write guard, CR-179 retro in close). `board.py`, `cli.py` (board wiring), `playbook.py` and the board cards are untouched by the move. Touched files that the board or its proofs exercise: `status.py` (`_past` skips retro-only folders; the board reuses status functions), `commands.py` (close), `types/index.d.ts`, cards and host references.

| Claim | Proof | Result |
| --- | --- | --- |
| Board still serves at a94a027 | live run from the worktree CLI, port 8793: start line `board on http://127.0.0.1:8793/ over <planning folder>`; `/` 200 html, `/api/status` 200 json schema 3, `/file?p=` 200, `..%2F..` 404, `/zzz` 404, POST 405; CSP `default-src 'none'`... on responses | ok |
| Long gate at a94a027 | `work/gates/20261111-200548.log` (passed, per the caller) | ok |
| Reuse, seat move, host 0.0.0.0, bad `board.port`, no file written | carried from the 372aef1 passes: board.py, playbook.py and the seat code are unchanged by the move, and the scenario step `remote_board` passed again at a94a027 | carried |
| Close/retro, write guard (CR-174, CR-179) | not this CR's claims; outside its diff | n/a |
| PR description (`gh pr view 119`): proofs name a94a027 (live run, `just check`, `just scenario`, Verified, CI) | live run and gate above; `just check` x3 CI pass at a94a027, `just scenario (ubuntu)` pending at the time of reading (the local gate passed) | ok, CI scenario to confirm |

Failed claims: none.

VERIFIED

## Fourth pass, rebase a94a027..936fb2f, Head: 936fb2f

Old base 7010fa6, new base origin/main d69eb88 (CR-181, CR-176). One conflict resolved in README.md and playbook.py: main's `prices` key and the CR's `board` key coexist.

| Claim | Proof | Result |
| --- | --- | --- |
| Config loading of `board` beside `prices` | live, from the worktree CLI: `chantier.yaml` with `board.port: 8796` and a valid `prices` model block: `playbook` says `valid, host claude`; `board.port: abc` gives `chantier.yaml:2: board: "port" is an integer from 1 to 65535, found "abc"`, exit 2, from both `playbook` and `board` | ok |
| Board still serves at 936fb2f | live run, port 8797: start line `board on http://127.0.0.1:8797/ over <planning folder>`; `/` 200 html, `/api/status` 200 json schema 3, `/file?p=` 200, `..%2F..%2Fx` 404, `/zzz` 404, POST 405; CSP `default-src 'none'`... on `/` | ok |
| Long gate and checks at 936fb2f | `just scenario` and `just check` passed per the caller (gate log `work/gates/20261111-205201.log` present); CI green per the caller | ok |
| Reuse, seat move, host 0.0.0.0, no file written | carried: board.py and the seat code are not touched by the move | carried |
| CR-181 and CR-176 | not this CR's claims | n/a |

Note: the verifier card `skills/chantier/references/verifier.md` is not in the main checkout or the worktree; I judged from the brief and the previous verify.md.

By hand, not provable here (UNVERIFIED): opening the board from a phone over Tailscale. Not claimed in the PR.

Failed claims: none.

VERIFIED
