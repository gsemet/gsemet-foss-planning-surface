## Summary

A pasted image is first written to a hidden `.partial` file and then renamed. If the window is
closed or the extension host dies in between, that hidden file used to stay in the image folder
forever. The next image paste into the folder now removes such leftovers.

## What changes for the user

- Hidden files named like `.image-2.png.k3j9x0ab.partial` (the extension's own naming) that are
  older than 10 minutes are deleted at the next paste into that folder.
- Recent ones (another paste may still be writing), files of any other name and all regular files
  are never touched. A file that cannot be removed does not stop the paste.

## Deliverable showcase

```text
before: images/  image.png  .image-1.png.k3j9x0ab.partial   (stays forever)
paste ->
after:  images/  image.png  image-1.png
```

## Test plan

- New unit test in `test/session/pasteImageWrite.test.ts`: two old matching files are removed; a
  recent match, a non-image name, a non-hidden name, a wrong-alphabet name and an old regular file
  are kept.
- `just check`: 2596 unit tests pass, requirements validate and lint clean, coverage regenerated.
- The file system port now reports an optional modification time (Node, VS Code, memory hosts).

## Internal references

- CR 068 (paste-partial-leftover); follow-up of PR #53.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
