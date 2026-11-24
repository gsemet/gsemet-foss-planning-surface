# Conflicts: CR-481 rebase onto origin/main (2026-11-24)

Commit 1 ("feat(pane): ...") applied cleanly. Commit 2 ("refactor(board): move the link helpers
to board/links.py ...") conflicted in one hunk of `skills/chantier/scripts/cli/src/chantier/board/address.py`.

## Hunk: the link helpers and `_call`

- HEAD (main): the link helpers (`is_loopback`, `_default_route_address`, `reachable`, `_bracket`,
  `url`, `_loopback_of`, `local_url`, `_base`, `loopback_base`) still in address.py, unchanged
  from the CR's base, and `_call` given a `timeout: float = 2` parameter (CR-478/479/482/483).
- CR: the helpers removed (moved to `board/links.py`), `_call` without the timeout.
- Choice: helpers dropped from address.py (main changed none of them, so `links.py` stays as the
  CR wrote it); main's `_call` signature with `timeout` kept.

## Outside the hunk

- main's new `call_op` called `_base(host, port)`, which no longer exists in address.py:
  changed to `links.base(host, port)`, as the CR did for `probe` and `register_seat`.
- main's other uses (`commands/live.py` importing `loopback_base` from address, `hub/feed.py`
  calling `address.loopback_base`) go through the names address.py re-exports: unchanged.
- No test monkeypatches the old private names. File's line endings (CRLF) kept, no BOM added.

## Fast gate

`just check` in the worktree at bf5fdbd4: pass (2599 passed, 20 skipped; release-notes ok).
