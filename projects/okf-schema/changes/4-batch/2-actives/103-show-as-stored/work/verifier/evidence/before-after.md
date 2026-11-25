# Before and after

- Before: base `1a742d714439595753a3b0b416f9cc04183015a3`, wheel built from a detached worktree.
- After: head `6572527608200cb688c0ae0224427e8b8bb44539`, wheel built from the CR worktree.
- Windows, Python 3.12.10. `<probe>` is a disposable folder.

| Pair | What it shows |
|------|---------------|
| `before-show.txt`, `after-show.txt` | Before: frontmatter rewritten (block style, quoted dates, comment lost), `trust:` and `stale: true` lines added, invented `{}` block, traceback on a Latin-1 file. After: the stored bytes. Missing, directory and outside-bundle messages are the same. |
| `before-trust.txt`, `after-trust.txt` | Before: no such command. After: tier and staleness, one error line with exit 2 on a Latin-1 file, no file changed. |

Reproduce: build a wheel at each SHA (`uv build --wheel`), install them in two virtual
environments named `vb` (base) and `vh` (head) beside a copy of `work/verifier/probe.py`, then
run `python probe.py <base sha> <head sha> <output folder>`.

No screenshot or video: the project has no user interface. No pair is missing.
