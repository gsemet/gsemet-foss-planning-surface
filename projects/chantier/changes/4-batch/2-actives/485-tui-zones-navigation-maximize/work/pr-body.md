## Summary

`chantier live` (the terminal board) only scrolled its central box, the Flow, which showed the oldest line first, and its time column was as wide as a full clock. This PR gives the terminal board an active panel moved with Tab, per-panel scrolling, a newest-first Flow, a narrow right-aligned `Ago` column, and a key that maximizes the active panel.

## Deliverables

The active box is marked in plain text (`▸ Flow`), so no colour carries the meaning alone. The Flow starts active.

| Key | Effect |
| --- | --- |
| Tab / Shift-Tab | next / previous drawn panel (Projects, Agents, Flow, Ready, Tasks; under 100 columns only Flow, Ready, Tasks) |
| Up, Down, PgUp, PgDn, Home, End | scroll the active panel; in the Flow Up is newer, Home is the newest and follows live, End is the oldest kept |
| `m` | maximize the active panel to the whole body; the same key restores |
| `t` | switch the Flow's time column between the clock (14 columns) and `Ago` (3 to 8 columns, right-aligned, widest text drawn) |

Choices: the active marker is a `▸ ` title prefix; the Flow keeps its pause semantics (`Flow  paused, <n> new`); other boxes keep their own offset; the screen stays maximized when Tab moves the active panel; Projects and Tasks moved to a new `clients/tui/boxes.py` to respect the repository's file-size limit.

## Blast radius

Grade: **1**. Confined to the terminal client, its tests and one docs section; no server or API change. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- Maximize key `m`: a printable letter not bound before, mnemonic, and one key both ways.
- `Ago` width computed per drawing: the widest relative-time text of the lines drawn, at least 3 and at most 8, so every form up to `100 days` fits and the freed columns go to `Event`.
- Shift-Tab goes back, Home/End are top (newest) and bottom (oldest), and the screen stays maximized on Tab (defaults the specification proposed).

## Known gaps

- **UNVERIFIED:** Tab, scrolling, maximize and `t` were not checked in a real terminal on a running board; they are proven by in-process tests only.

<details>
<summary>Details</summary>

## Changes

- `clients/tui/view.py`: active panel, Tab cycle, per-panel offsets, newest-first window, maximize state.
- `clients/tui/screen.py`, `ready.py`, `parts.py`, new `boxes.py`: marker, maximized layout, computed `Ago` width, help, footer, `Tab`/`Shift-Tab` key names.
- Tests: `test_live_model.py`, `test_live_ready.py`, new `test_live_panels.py`, helpers in `live_world.py`.
- `docs/boards.md`: the `chantier live` section.

## Impacts

Terminal board only: the Flow now reads newest first, so Up and Down and Home and End swap their old directions there.

## Test plan

- [x] New or changed tests (they fail on the previous code), in `test_live_model.py`, `test_live_ready.py`, `test_live_panels.py`
- [x] Local gates at `4564806`: `just check` pass, `just eval-dry-run` pass (19 of 19), long gate `scenario` pass
- [x] Evidence at `4564806`: in-process screens through `screen.plain()`; no real-terminal capture (see Known gaps)
- [x] Review: approved at `4564806`
- [x] Verified at `4564806`
- [x] CI green at `4564806`

## Internal references

CR-485 tui-zones-navigation-maximize (batch-31).

</details>
