## Summary

`chantier board` worked only on the machine that ran it. It now serves a JSON API of the record and the planning folder's files on the local network, behind a key in its link, for one project or every project of a planning surface. The board also has a web page frame (sidebar, nav, project views, English and French words) that reads that API, linted by Biome.

## Deliverables

None yet: no browser screenshot of the frame beside the prototype.

```text
chantier board -> board/command.py (options, key, start lines)
                  board/app.py (Starlette: routes, key middleware, headers)
                  board/state.py, crs.py, files.py, fingerprint.py, costs.py, seats.py, projects.py
```

## Blast radius

Grade: 2. The board command changes its default host to `0.0.0.0`, adds a key file in the git folder and two dependencies (`starlette`, `uvicorn`), imported only when `board` runs. A revert restores the old read-only board.

## Autonomous decisions

- The server adds an `X-Chantier-Now` header, because a `304` has no body to carry the server's time.
- The board builds its own rows of CRs rather than changing the pane's `STATUS.json` fields.

## Known gaps

- The scenario ran on Windows only, its GitHub leg (719 of 719); the GitLab leg did not run here. Linux and macOS are proved by CI only.
- No screenshot of the frame beside the prototype yet.
- The phone check on the local network is the user's to confirm.
- The server edits no backlog and runs no autosync yet: `AGENTS.md` words the rule as the specification does, ahead of the code.

<details>
<summary>Details</summary>

## Changes

- `board/` split into `command`, `app`, `key`, `projects`, `state`, `crs`, `files`, `fingerprint`, `costs`, `seats`, `address`.
- `--clock` pins the server's instant; `--new-key` replaces the key.
- `starlette==1.10.0` and `uvicorn==0.54.0` pinned in `pyproject.toml`, `uv.lock` updated.

## Impacts

No visual change yet.

## Test plan

- [ ] New or changed tests: `tests/test_board.py` (3 structure tests), `tests/test_code_targets.py` (web targets)
- [ ] Local gates: `just check`, mypy on linux, darwin, win32
- [ ] Evidence: none yet
- [ ] Review: unchecked
- [ ] Verified: unchecked
- [ ] CI green: unchecked

## Internal references

CR-222 visualization-backend.

</details>



