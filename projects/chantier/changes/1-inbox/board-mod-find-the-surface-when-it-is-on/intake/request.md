# Board mod: find the surface when it is only an added working directory

Relayed from markdown-okf-schema-studio's Chief of Staff, on the owner's word (2026-11-25).

## What happens

The `/chantier-board` mod (`hooks/register.tsx`) shows an empty pane in a session whose main checkout is a project (markdown-okf-schema-studio) and whose planning surface is only an added working directory. This is the Studio's layout: the Chief of Staff runs in the Studio's checkout, with the surface added.

Cause, read by chantier's Chief of Staff: `findBases(root)` looks only at the main checkout of the session's cwd. It takes that checkout's own `.agents/changes` first (the Studio has a leftover, git-ignored one with no `STATUS.json`), else `<root>/projects/<name>/changes`. It never reads the session's added working directories. v0.12.0 (commit 63f857ad) added surface support only for a session whose cwd is the surface itself.

Updating the plugin, reloading the mod or removing the leftover folder does not fix it: without the folder the mod falls back to an empty `[own]`.

## Expected

1. The pane finds the project's planning folder in the surface named by the project's `AGENTS.md` `planning:` pointer, or by the session's added working directories, and shows the project's board.
2. A project's own `.agents/changes` without a `STATUS.json` does not hide a surface that has one.
3. The seat and batch records still choose the project in a surface with several projects.
4. Tests cover the Studio layout (project checkout as cwd, surface added).

## Workaround today

A session whose primary folder is the planning surface, the project added as the extra one. The web board works: `serve` on http://127.0.0.1:8765/.
