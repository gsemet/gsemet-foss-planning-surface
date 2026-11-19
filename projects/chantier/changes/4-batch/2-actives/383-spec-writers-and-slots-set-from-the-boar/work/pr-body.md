## Summary

Two numbers now live in the project's configuration and can be changed from the web board's Configuration page: how many change requests are specified at once (`specifying.parallel`, default 4) and how many slots a new batch gets (`batch.slots`, default 4, what `open` used to hard-code). When the board saves a change to either number, it appends a `config` line to the project's forge journal, which the watcher reads like a merge, so the Chief of Staff learns of it at once and acts on it: it gives an `order slots` for a running or paused batch, and starts or holds back spec-writers against the new limit.

## Deliverables

A new "Limits" tab on the board's Configuration page, next to Models and Timing, with two number inputs, the effective value and the layer it comes from, and a "use the inherited value" control. Shape of the new journal line:

```json
{"seq": 12, "t": "...", "by": "board", "kind": "config", "key": "batch.slots", "old": 4, "new": 6, "batch": "batch-29"}
```

`playbook` gets a role-free `limits:` line:

```
limits: specifying 4, markers 2 (cr-a, cr-b); batch slots 6 [surface project]
```

Choices: the keys are role-free (the CLI names no role); `--slots` still wins over `batch.slots`; a running batch keeps its recorded slots until an `order slots`; a configured `batch.slots: 0` makes `open` with no `--slots` refuse; the board never edits a batch or messages an agent.

## Blast radius

Grade: 2. Touches configuration checks, `open`, the board's config page, the forge journal and the cards. Revert is possible; no data format outside the journal changes.

## Autonomous decisions

- The two keys are checked in a checked-only list, not frozen into the batch record with the other playbook keys, so a running batch never reads a live change.
- `status` hides the slots line only for an order strictly after the save.
- The journal's dedup key gets its own branch for `config` lines so two saves with the same values stay two lines.

## Known gaps

- That the watcher's end wakes an idle Claude Code session on a board save is unproved; `status` is the fallback for the slots and `playbook`'s `limits:` line for the specifying limit.
- A paused batch has no watcher (`chantier watch` refuses one), so the slots event for a paused batch reaches the Chief of Staff through `status` only.
- No screenshot of the Limits tab from a real session.
- The journal and `status` text says a batch `keeps <old effective value>`; when the batch's recorded slots differ from that value the text is off (the board's own response line uses the recorded slots).

<details>
<summary>Details</summary>

## Changes

- Shipped defaults and `config.py` checks for `specifying.parallel` and `batch.slots`; a per-layer reader (`playbook/limits.py`, `plugin_files.read_limits`).
- `open`: no default for `--slots`, uses `batch.slots`, labels a user-layer value, refuses a configured 0.
- `playbook`: the `limits:` line.
- Board: config view, `edit_surface_file` and the comment-keeping YAML edit accept the two keys and `null`; a real PUT appends one `config` journal line per changed key; the Limits tab and its texts.
- Journal: the `config` kind, its text, and `status` printing the un-acted `batch.slots` line.
- Cards, `AGENTS.md`, `CONTRIBUTING.md`, `docs/web-board.md`, `scenario/README.md` follow.

## Human decisions

- The two keys have role-free names (`specifying.parallel`, `batch.slots`); the limit counts specifying markers only and is shared by everyone who starts one on the project.
- A board save of either key is the user's word: the Chief of Staff acts on it without asking.
- A configured `batch.slots: 0` makes `open` with no `--slots` refuse.
- Both keys ship in one change; the board writes one `config` journal line per changed key.

## Impacts

A new tab on the board; `open` takes its default slots from configuration. No other visual change.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `bb2eb0f`: just check, just eval-dry-run, scenario surface-board
- [ ] Evidence: none, see Known gaps
- [x] Review: approved at `bb2eb0f`
- [ ] Verified at `bb2eb0f`
- [ ] CI green at `bb2eb0f`

## Internal references

- CR-383 config-spec-writers-slots

</details>
