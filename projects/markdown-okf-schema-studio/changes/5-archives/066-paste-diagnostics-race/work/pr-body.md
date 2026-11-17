## Summary

The diagnostics of the image-paste real-window test can no longer throw. A file that vanishes between
the folder listing and its stat (the hidden `.partial` file) is reported as "gone during listing"
instead of replacing the real assertion message with `ENOENT`. Test code only.

## Deliverable showcase

```text
before: Error: ENOENT: no such file or directory, stat '.../.image.png.partial'
after:  folder: .image.png.partial (gone during listing), image.png (68 B); editor text: "..."
```

## Test plan

- New unit test `test/node-services/folderListing.test.ts` (1 test: vanishing file, undefined stat, missing folder).
- `just check`: 2595 unit tests pass, requirements validate/lint/coverage clean.

## Internal references

- CR 066 (paste-diagnostics-race); follows PR #53.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
