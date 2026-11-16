# Before / after, CR-182 remote-board

Before: SHA 04ed67b (origin/main, detached worktree, removed). After: SHA 372aef1 (pushed head).

| Pair | Before | After | Reproduce |
| --- | --- | --- | --- |
| `chantier board` | `before.txt`: `invalid choice: 'board'`, exit 2 | `after.txt`: start line, page, API, files, 405s, reuse, seat stop, 0.0.0.0 line, yaml refusal | `uv run --script <cli> board --host 127.0.0.1 --port <p> --seat s-1` in a git repo after `init`, `file`, `seat take s-1` |

Not capturable here: opening the board from a phone over Tailscale (by hand, the PR marks it unverified).

## Second pass (head 372aef1)

`after.txt`, section "3rd run": `/file` of a real file (`1-inbox/<item>/intake/request.md`) answers 200 with its text escaped in a `<pre>`; the earlier 404 came from a wrong path in my probe (`01-intent.md` does not exist in that item), not a defect. The planning folder's SHA-256 prefixes, sizes and mtimes are identical before and after a serving run (about 40 s, with requests and a 32 s wait), and `git status --porcelain` is unchanged. (The 2nd run in `after.txt` is superseded: its board stopped by design, my `seat take s-3` lacked `--over`, so the seat stayed s-2.)
