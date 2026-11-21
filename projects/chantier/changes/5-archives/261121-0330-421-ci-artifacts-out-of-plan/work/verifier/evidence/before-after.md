# Before / after

Pair 1: `is_published` on artifact paths. Before: base 4ed0d56 (detached worktree, removed). After: b4d7117.
Reproduce: `python -I -c` importing `chantier.store.base.is_published` from each tree's `src/`.

| rel | before | after |
|---|---|---|
| 3-ready/x/work/artifacts-1/a.txt | True | False |
| 3-ready/x/work/debugger/artifacts-99/deep/a.bin | True | False |
| 4-batch/x/work/a/b/artifacts-7/x | True | False |
| 3-ready/x/work/artifacts-1 (file) | True | True |
| 3-ready/x/evidence/artifacts-1/a.txt | True | True |

No images captured (no UI change). The blocked line before the change was `git-error` with git's text; not reproduced separately (the new tests fail on the old code by construction: `too_long_path` does not exist there).
