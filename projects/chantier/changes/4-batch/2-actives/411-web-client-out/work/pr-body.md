## Summary

The web board's files leave the server's package: they now live in `chantier/clients/web/`, still shipped in the one wheel. `chantier board` serves that folder by default, another UI's static files with `--ui <folder>`, or only the API with `--ui none`. A test keeps the server's code from naming the client's folder.

## Deliverables

- The web client moved with `git mv` (every file a 100 % rename except `DESIGN.md`, whose path sentence changed): `board/web/` -> `clients/web/`.
- `chantier board --ui <folder>|none`: a folder needs an `index.html`, refused at the start otherwise with nothing written; on a board already running, `--ui` is not applied and one line says so (exit 0).
- Hand checks at `dd1f1c1` (spec 8.3): `git diff --find-renames=100%` lists 154 files `R100` to `clients/web/`, `DESIGN.md` deleted and added (its path sentence), 5 `chantier/` files modified; `git ls-files --eol`: 153 text files `lf`, the 2 `.woff2` `-text`; the wheel holds 155 files under `chantier/clients/web/` (`index.html`, `js/main.js`, `fonts/Inter-Regular.woff2` among them) and none under `chantier/board/web/`; Biome checks 151 files at the base and at the head; `just test` 69 s at the base, 72 s at the head; `just docs-screenshots` gives the same bytes at the base and at the head (`batch-pc.png` alone varies between two runs of the same code, so it is not a diff of this CR).
- `--ui none`: outside `/api/`, every GET answers 404 with `this server serves no UI: see docs/server-api.md`.

```mermaid
flowchart LR
  cmd[declare/board.py: --ui, SHIPPED_UI] --> command[board/command.py]
  command --> ctx[Context.ui]
  ctx --> routes[board/routes.py]
  routes --> static[board/static.py: serve ui]
  static -.-> web[clients/web/ or --ui folder]
```

## Blast radius

The board's static serving and the `chantier board` command line; paths in `.gitattributes`, `biome.json`, `justfile`, docs and tests. The API, protocol, key rules and the client's own files are unchanged. A board running from a checkout across the merge answers 404 on its page until restarted.

## Autonomous decisions

- The exit code of a refused `--ui` is `EXIT_USAGE` (1 in this code base).

## Known gaps

- The browser check of the spec's 8.3 was not run in a real browser: the Verifier has no browser tool and proved the same by HTTP requests at `dd1f1c1` (default client, `--ui none` 404 line, a drive-letter folder under the CSP, a bad folder, a running board).
- The symlink case of the new test skips on a Windows account that cannot make symlinks.
- Passing the shipped folder explicitly to a running board also prints the "--ui not applied" line (the code compares a string with a path); harmless, exit 0.
- No release-notes line: no file for the next release exists yet.

<details><summary>Details</summary>

## Changes

See the diff: static serving takes a folder; `Context.ui`; `--ui` parsing in `board/command.py`; `docs/server-api.md` "Serving another UI"; `docs/web-board.md`; `AGENTS.md` and `CONTRIBUTING.md` paths; tests incl. `test_board_ui.py`; scenario `remote_board` additions.

## Human decisions

`--ui` on a running board is not refused; no `board.ui` key; today's file types stay; a folder needs an `index.html`.

## Impacts

None on data, configuration or records.

## Test plan

- [x] Local gates at `dd1f1c1`: `just check` pass, `just eval-dry-run` pass (18 of 18), `just scenario` pass (local Windows)
- [x] Review: approved at `dd1f1c1` (carried from `daed507`, the reviewed state, rebased onto main)
- [x] Verified at `dd1f1c1`
- [x] CI green at `dd1f1c1` (5 jobs, incl. `just scenario (ubuntu-latest)`)

## Internal references

CR-411, batch-29; after CR-406.

</details>
