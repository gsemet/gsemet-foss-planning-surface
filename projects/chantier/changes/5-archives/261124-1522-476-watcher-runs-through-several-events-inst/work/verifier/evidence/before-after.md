# Before and after (CR-476)

Before: base a94085d3498d3c41febd77fdc18fa74ff4d8d507 (detached worktree, removed). After: 8f0f54d8e14f98861cbb1ebe8c6c8dfb2fb05a72.

- Pair 1: `grep -c stream skills/chantier/scripts/cli/src/chantier/declare/watch.py` and `grep -n "def running_batch\|def followed_batch" .../hub/batch_prs.py`.
  Before: `0`, and `27:def running_batch(...)`. After: `watch --stream --once --after 0` refused with `error: watch: --stream and --once do not go together` (exit 1 = EXIT_USAGE), and `followed_batch` in place of `running_batch`.
  Reproduce: run the commands in each checkout (text only, no image).
- No screenshot or video: the change has no UI.
