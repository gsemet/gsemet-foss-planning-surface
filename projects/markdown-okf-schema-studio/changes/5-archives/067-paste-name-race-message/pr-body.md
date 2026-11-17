## Summary

Pasting an image never overwrites an existing file. When another program created a file with the
chosen name between the name choice and the final rename, the paste was refused and the user saw
VS Code's raw "file exists" error. The paste now saves the image under the next free name.

## Deliverable showcase

```text
Folder at choice time:   (empty)            -> chosen name image.png
Another program writes:  image.png          (kept untouched)
Before:  paste refused, "file exists"
After:   image-1.png written, answer ok with fileName "image-1.png"
```

## Changes

- `src/session/features/hostRequests.ts`: the paste chooses the name again from a fresh folder
  listing when the rename fails because the name is now taken (up to 5 attempts); other errors are
  still reported as before and the hidden partial file is always removed.
- The image-write requirement states the retry; the requirements log has a dated entry.

## Impacts

No visual change. A clash with a concurrent writer is invisible to the user.

## Blast radius

Grade: 1. Local to the pasted-image write; a plain `git revert` restores the refusal.

## Test plan

- [x] New or changed tests (the race test now expects `image-1.png` and fails on the previous code)
- [x] Requirements: SwRS updated, markers in sync, `okfreq validate/lint/update-coverage --check` clean (1010 requirements)
- [x] Local gates: `just check` (2595 + 44 + 2 unit/contract tests, 31 Python tests, 0 failures)
- [ ] Review
- [ ] CI green

## Internal references

CR 067 (paste-name-race-message), follow-up of PR #53.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
