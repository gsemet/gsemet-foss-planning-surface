# CR-102 before and after

- Before: base `2f09cef3e786d1696e42b5cb305d4a55111e7725`. **Not captured**, for every pair.
- After: head `8537709c5c10c77140a62542d794421537448d59`, worktree CLI on Windows, run in a
  throwaway project folder. `<project>` in the captures stands for that folder.

`<W>` is the CR's worktree and `<CR>` the CR folder.

## Why the before was not captured

The detached worktree of the base could not be checked out: a tracked path is too long for
Windows under the scratch folder.

```text
$ git -C <W> worktree add --detach <CR>/work/scratch/v/b 2f09cef3e786d1696e42b5cb305d4a55111e7725
error: unable to create file skills-evals/results/iteration-30.06.26-20.12/bootstrap-knowledge-base/with_skill/workspace/_schema/Sensor.schema.json: Filename too long
(many more lines of the same kind)
fatal: Could not reset index file to revision 'HEAD'.
(exit 128)
```

No other folder and no other way to run the base was tried. The base behaviour is supported only
by reading the base source and by the output quoted in issue 57, neither of which is a capture:

- issue 57, "Actual": `- [api](./api/) — [Health Check](health-check.md)  [API Endpoint]`, with
  `validate` reporting no W2;
- at the base, `_get_subdir_description` returns the first non-heading line of the subdirectory
  `index.md`, `validate_index` and `validate_log` run no link check, and `find_broken_links`
  checks the resolved target as written (no anchor strip, no percent decoding).

## Pairs

| Pair | Before | After | What the after shows |
| --- | --- | --- | --- |
| Subdirectory summary | not captured | [after-1-summary.txt](after-1-summary.txt) | A list-only subdirectory index gives the generic sentence; the damaged line of issue 57 is repaired; an introduction is written with its link rewritten for the parent; an authored summary is kept; a second run changes nothing |
| W2 in `index.md` and `log.md` | not captured | [after-2-w2.txt](after-2-w2.txt) | A broken link in each file draws W2 and `validate --strict` exits 1; `index` keeps the authored line; `validate --strict` passes once the `log.md` link is removed |
| Anchors, encoded paths, `stats` | not captured | [after-3-anchors-stats.txt](after-3-anchors-stats.txt) | A percent-encoded link to an existing file and an anchor-only link are not broken; `stats` and `validate` count and name the same broken target |

## How to reproduce

In an empty folder, with the worktree's `okf-schema` at the head:

1. `okf-schema new --path kb/bundle --name api/health-check --type "API Endpoint" --title "Health Check"`
2. `okf-schema index --path kb/bundle`, twice.
3. Make the edit each `(edit)` line of a capture describes, then run the command that follows it.

The captures follow the steps of the specification's scenario, in the order summary (steps 1, 2,
4, 6), W2 (steps 3, 7) and anchors and stats (steps 5, 7b); each file keeps the step headings.
The state is shared: run the steps in numeric order.
