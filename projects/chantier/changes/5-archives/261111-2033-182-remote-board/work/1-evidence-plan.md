# Evidence plan, CR-182 remote-board

Claims: the 10 points of the specification's "Evidence / just scenario" list, proved by the scenario step
`remote_board` (both forges) and the `external_surface` step; `just check` passes.

Technique (a CLI with a web page, no screen UI): command output and HTTP transcripts, no screenshot.
Before (base, detached worktree of origin/main): `chantier board` is an unknown command (the CLI refuses it).
After (head): start `chantier board --host 127.0.0.1 --port <free> --seat s-1` over a small throw-away planning
folder (run `uv run --script <cli> --help` for the folder setup, or reuse the scenario's helper), then record
`curl` of `/` (200, html, security headers, a CR label), `/api/status` (JSON, planning_folder, seat, board true),
`/file?p=<spec>` (200), `/file?p=../x` (404), `POST /` (405), the second `board` ("already running"), the start line.
The gate (`$CHANTIER gate CR-182 "just scenario"`) already passed at 372aef1; it needs no second run unless the head moves.
Also: the PR description claims match the diff (`git diff origin/main...HEAD --stat`).
Not provable here, by hand: opening the board from a phone over Tailscale (the PR says UNVERIFIED by hand).
