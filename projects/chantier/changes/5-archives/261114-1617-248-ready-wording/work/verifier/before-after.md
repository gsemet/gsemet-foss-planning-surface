# before-after

Before: base be5563c (`origin/main`), not rebuilt as a worktree: the before is shown by `git grep -c "🔵" be5563c -- skills hooks scenario`, which finds 7 hits (a ready CR drew 🔵 `ready` in the pane test, the scenario, status-layout.md and `status/words.py`). After: head 2202425.

| Pair | Before (be5563c) | After (2202425) | Reproduce |
| --- | --- | --- | --- |
| Label of a ready CR | `🔵 ready Notify 1/3` for every ready CR (per spec) | `🟢 ready to merge Notify 1/3`, `🟤 PR in draft, waits for CR-101`, `🟣 ready locally Notify 1/3` | `evidence/STATUS.md`, `status-output.txt`, `STATUS.json` |
| Web board | not captured (before) | `evidence/board.png`, three states on Home | `scenario` driver at head, `chantier board --port 0`, Chrome headless |
| Pane in a real session | not captured | not captured: a Verifier cannot run a real Claude Code session; no screenshot was faked | n/a |

Scenario transcripts at the head: `rw-github.txt`, `rw-gitlab.txt` (`ready_words`, 35 checks each), `fs-github.txt`, `fs-gitlab.txt` (`stack_batch` plus `forge_stack_cli`, 65 and 45 checks).
