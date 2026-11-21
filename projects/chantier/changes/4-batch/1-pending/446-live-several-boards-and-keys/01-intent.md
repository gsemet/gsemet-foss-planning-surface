# `chantier live`: keys to scroll and filter, and several boards in one screen

Split out of live-activity-tui (2026-11-20, `intake/request.md`). `chantier live` watches one
board per run and reads no key. The user wants a working terminal UI (2026-11-21).

Intent:

- Keys in the live screen: scroll back in the Flow and come back to the live end, filter what is
  shown by a text (a project, a CR), a help of the keys, and quit.
- Several boards in one screen: one link and one key each, one connection each.

It stays read-only: a key changes what this screen shows and nothing else; it reads the server
only, writes nothing and messages no agent. Portable: Linux, macOS and Windows.

Not part of this change: opening a CR's files in the terminal, the mouse. Destination: batch-30
(the user, 2026-11-21).
