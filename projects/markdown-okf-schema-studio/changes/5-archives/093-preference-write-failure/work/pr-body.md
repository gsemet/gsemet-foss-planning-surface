## Summary

When VS Code could not store the theme or a view choice (zoom, width, table of contents, toolbar),
the preview only wrote to the console. The choice silently disappeared at the next start. The reader
now gets a short warning.

## Deliverables

```
before: storage.update rejects -> console.error                 (reader sees nothing)
after:  storage.update rejects -> console.error + one warning
        "The Markdown preview could not save your display choice;
         it holds until VS Code closes."
```

The warning shows once per run of failures (rapid zoom clicks do not stack notifications); a
successful write re-arms it. The choice still holds for the session.

## Changes

- `src/session/workspaceChoices.ts`: `setPreviewThemeMode` and `setViewPreference` call the host
  warning on a rejected write.
- Requirements: removed the "Known issue" lines about the silent failure (view-choice storage, width
  mode, toolbar-navigation use case) and updated the scenario and verification note; update log entry.
- Test: `test/session/diagReq.viewState.requirements.test.ts` covers theme mode and view preferences
  (failing and absent storage). The existing theme test now also asserts the warning; its intent
  (the value holds for the session, logged, nothing written without storage) is unchanged.

## Impacts

No visual change except the new notification on a storage failure.

## Blast radius

Grade: 1. One extra notification on an already-failing path; a plain `git revert` restores it.

## Test plan

- [x] New or changed tests (they fail on the previous code: the warning list was empty)
- [x] Requirements: SwRS updated, markers in code and tests, `okfreq update-coverage` clean
- [x] Local gates: `just check` (2641 unit tests pass, 46 + 2 contract/other pass), okfreq validate
      (1013 requirements, 0 errors), lint and update-coverage `--check` clean
- [ ] Review
- [ ] CI green

## Internal references

- CR 093 (preference-write-failure); SwRS LIFE-169, LAYOUT-021 (superseded), StRS TOOLBAR-001.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
