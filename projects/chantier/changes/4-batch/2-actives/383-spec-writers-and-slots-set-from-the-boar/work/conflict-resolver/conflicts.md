# Conflicts: CR-383 restacked onto fe2c215e (CR-375)

Command: `git -C <worktree> rebase --onto fe2c215e 020fd864`. One own commit, now cbfa0ddd.

Hunks and choices:

- chief-of-staff.md (watcher section): kept HEAD's "start the watcher again from its last line",
  then appended this CR's `config changed on the board` paragraph, dropping its old "as above".
- hosts/claude-code.md and hosts/copilot.md ("Run the watcher" row): kept HEAD's row (the command
  the `watch:` line prints, as is) and appended this CR's unproved-config-wake sentence.
- commands/opening.py imports: kept both `own_transcript` (HEAD) and `read_limits` (this CR).
- opening.py `_empty_lines`: kept HEAD's factory version (FACTORY_NEXT, `_ready_lines`), with the
  `where` label unpacked from `shape` and shown after the slots.
- opening.py `_freeze` vs `_freeze_rules`: kept HEAD's `_freeze_rules`, dropped this CR's `_freeze`.
- opening.py `open_batch` line: kept HEAD's `, factory` suffix and added `{where}`.

Fixes the gate forced, left uncommitted in the worktree:

- opening.py reached 404 lines (limit 400): shortened `_slots_from`'s docstring and the
  "batch.slots is 0" message (the tests match "batch.slots is 0 in", still true).
- tests/test_forge_hub.py: the config-line test expected the old `watch: cursor 1; next:` last
  line; CR-375 prints the `watch: batch-01 still running: ...` restart line, so it now expects that.

Fast gate: `just check` in the worktree: pass (731 tests passed, release-notes ok), exit 0.
