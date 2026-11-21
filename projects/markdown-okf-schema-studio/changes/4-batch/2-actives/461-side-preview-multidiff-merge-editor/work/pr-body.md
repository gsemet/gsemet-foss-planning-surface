## Summary

The side preview does not follow the multi-file diff editor nor the merge editor, because the VS Code API gives these two editors no tab input class. This PR writes that limit down for users and in the requirements, instead of leaving it implicit. Documentation and requirements only: no code change.

## Deliverables

What a reader gets, in one table:

| Where | What it now says |
| --- | --- |
| `docs/known-limitations.md` | the side preview does not follow the multi-file diff editor nor the merge editor (3-way merge), with the reason, and the workaround |
| `docs/user/open-studio.md` | the button, the command and the following do not apply to these two editors: open the file in a text editor or the single-file diff |
| SwRS-MDOKFSTUDIO-LIFE-026 | a boundary scenario "Editors the side preview does not follow" and a known-limit line |

Choice made: document the limit, build no detection (the API offers none to build on).

## Blast radius

Grade: 1 (local and isolated: documentation and requirements text only). A plain git revert restores the previous state.

## Autonomous decisions

- The limit is recorded in the requirement that already covers following text diffs (LIFE-026), not in a new one: it is the same behaviour boundary, and the known-limit row is marked "by reading the API, not run" since no code detects these editors.

## Known gaps

- The new known-limit row has no test: no code exists to test, and the VS Code API gives no way to tell these editors from another editor change.

<details><summary>Details</summary>

### Changes

- `docs/known-limitations.md`: the "does not claim" bullet on diffs names the two editors, the reason and the workaround.
- `docs/user/open-studio.md`: one sentence after the text diff paragraph.
- `requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-026.md`: boundary scenario and known limit.
- `requirements/tiers/log.md`: dated entry.

### Human decisions

- Document the limit rather than support these editors some other way: no code, a known limitation and a requirement naming both editors as not followed, with the reason.

### Impacts

No visual change; users learn from the docs that these two editors are not followed.

### Test plan

- [x] Tests: none needed (documentation and requirements only, no behaviour change).
- [x] SwRS: LIFE-026 updated; `just requirements-update` and `just requirements-lint` pass, as part of the preflight run at afc0013.
- [x] Changelog: No user-facing change in behaviour (documentation of an existing limit).
- [x] Local gates: `just preflight` (static stage on Windows) passes at afc0013.
- [x] Review: Inspector approved at 7aa1e9b4 (rebased as afc00137); Verifier VERIFIED at afc00137.
- [x] CI green at afc00137 (static, static-windows, viewer-graph, visual).

### Internal references

- CR-461 (batch-07), follow-up of CR-455 decision 10.

</details>
