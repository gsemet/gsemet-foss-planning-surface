# Before / after

No UI change. Pair: default host, before at base origin/main `DEFAULT_HOST = "0.0.0.0"` (board/address.py:21), after at 7c1d8905be1a1ca0a0f85e15710d2bc4670661ee `"127.0.0.1"`; reproduce with `git show <sha>:skills/chantier/scripts/cli/src/chantier/board/address.py | grep DEFAULT_HOST`, and the after run in verify.md claim 1. A before run on a detached base worktree was not captured: the source line proves it.
