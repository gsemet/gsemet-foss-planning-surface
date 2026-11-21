## Summary

Any project whose session loaded chantier from chantier's own checkout ran chantier's dev mode, so its `chantier` processes held the checkout's `.venv` open and a `uv sync --locked` of that checkout failed on Windows (os error 32). The dev mode now applies only when the session's project is chantier itself; every other project runs the plugin mode (`uvx --from "<plugin root>"`), even from chantier's checkout.

## Deliverables

The launch decision, before and after:

| Plugin root has `.git` | Session's project | Before | After |
| --- | --- | --- | --- |
| yes | chantier | dev form, sync line | dev form, sync line |
| yes | another project | dev form, sync line | plugin form, no sync line |
| no | any | plugin form | plugin form |

New helper, used by the launch text and by the permission check (`plugin_files.py` / `launch.py`):

```python
def is_chantier_project(repo: Repo | None) -> bool:
    # planning surface: project folder named "chantier"
    # in-project: repo root holds a plugin manifest named "chantier"
    # None: False
```

## Blast radius

Grade: 2. The launch text of every session, the allow-rule check and the cards change; revert restores the old rule. Another project may run a build uv caches by version (accepted, named in the docs).

## Autonomous decisions

- The helper moved into `launch.py` and the launch tests into `test_launch_modes.py`, to keep file and function sizes within the project's limits.

## Known gaps

- A session's reading of its own context ("is the project chantier") is card behaviour: no automated check proves it; the shipped-text checks prove the cards say it.
- The board server, its writer and the forge hub started from another project's session run that project's cached build: accepted in words only, no check proves it.
- The scenario's sandbox project is not chantier, so it runs the plugin mode; the chantier cells (dev form, the Windows tail, the dev rules) are carried by unit tests only.

<details>
<summary>Details</summary>

## Changes

- `is_chantier_project`; `cli_command` and `sync_command` take the repo and return the dev form and the sync line only for chantier's own project.
- Preflight passes its repo, so the Windows dev-mode tail prints in the dev mode only; the allow-rule check uses one `_dev_mode(repo)` helper.
- The four `$CHANTIER` launch paragraphs, the concepts, host and session-start cards, `AGENTS.md`, `CONTRIBUTING.md` and `docs/web-board.md` state the rule in the same words, with the stale-build sentence.
- Tests and the scenario follow the new mode.

## Human decisions

- Dev mode only for chantier itself; other projects in plugin mode.
- In a planning surface, the project is chantier by its folder name `projects/chantier` alone.
- The stale build for other projects is accepted.

## Impacts

No visual change. Other projects' sessions get the plugin-mode allow rule, asked once at their next batch start.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at c5af034: `just check` pass (1625 passed), `just eval-dry-run` pass (18 of 18), `just scenario` pass
- [x] Evidence: no before/after capture (CLI and cards); checks in the verifier's report at c5af034
- [x] Review: approved at c5af034 (carried from 14160a6)
- [x] Verified at c5af034
- [x] No CI: no check listed at c5af034 (PR is on a stacked base)

## Internal references

- CR-436 sync-lock (batch-30), after CR-432; the wait part is the inbox item sync-lock-wait.

</details>
