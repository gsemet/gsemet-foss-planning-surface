# CR-102 before and after

- Before: base `1a742d714439595753a3b0b416f9cc04183015a3`. **Not captured**, for every pair.
- After: head `125952dc04a949cc78810e2340ef57d9ffa6ba5e`, worktree CLI on Windows, run in a
  throwaway project folder. `<project>` in the captures stands for that folder.

`<W>` is the CR's worktree and `<CR>` the CR folder.

## Why the before was not captured

Carried from 8537709, when the base was `2f09cef3e786d1696e42b5cb305d4a55111e7725`: the detached
worktree of the base could not be checked out, because a tracked path is too long for Windows under
the scratch folder.

```text
$ git -C <W> worktree add --detach <CR>/work/scratch/v/b 2f09cef3e786d1696e42b5cb305d4a55111e7725
error: unable to create file skills-evals/results/iteration-30.06.26-20.12/bootstrap-knowledge-base/with_skill/workspace/_schema/Sensor.schema.json: Filename too long
(many more lines of the same kind)
fatal: Could not reset index file to revision 'HEAD'.
(exit 128)
```

The move to the new base changed no file under `skills-evals/` (`git diff --quiet 2f09cef 1a742d7
-- skills-evals` exits 0) and the scratch folder is the same, so the stop stands and the command was
not run again. No other folder and no other way to run the base was tried. The base behaviour is
supported only by reading the base source at `1a742d7` and by the output quoted in issue 57, neither
of which is a capture:

- issue 57, "Actual": `- [api](./api/) — [Health Check](health-check.md)  [API Endpoint]`, with
  `validate` reporting no W2;
- at the base, `_get_subdir_description` returns the first non-heading line of the subdirectory
  `index.md` with its list marker removed, `validate_index` and `validate_log` run no link check,
  and `find_broken_links` checks the resolved target as written (no anchor strip, no percent
  decoding).

## Pairs

| Pair | Before | After | What the after shows |
| --- | --- | --- | --- |
| Subdirectory summary (steps 1, 2, 4, 6) | not captured | [after-1-summary.txt](after-1-summary.txt) | A list-only subdirectory index gives the generic sentence; the damaged line of issue 57 is repaired; an introduction is written with its link rewritten for the parent; an authored summary is kept; a second run changes nothing |
| W2 in `index.md` and `log.md` (steps 3, 7) | not captured | [after-2-w2.txt](after-2-w2.txt) | A broken link in each file draws W2 and `validate --strict` exits 1; `index` keeps the authored line; `validate --strict` passes once the `log.md` link is removed |
| Anchors, encoded paths, `stats` (steps 5, 7b) | not captured | [after-3-anchors-stats.txt](after-3-anchors-stats.txt) | A percent-encoded link to an existing file and an anchor-only link are not broken; `stats` and `validate` count and name the same broken target |

## How to reproduce

In an empty folder, with the worktree's `okf-schema` at the head:

1. `okf-schema new --path kb/bundle --name api/health-check --type "API Endpoint" --title "Health Check"`
2. `okf-schema index --path kb/bundle`, twice.
3. Make the edit each `(edit)` line of a capture describes, then run the command that follows it.

The state is shared across the three files: run the specification's scenario steps in their order
(1, 2, 3, 4, 5, 6, 7, 7b). Each file keeps the step headings.
