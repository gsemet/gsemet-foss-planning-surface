# Clear message when a pasted image loses a file-name race

Since the pasted-image fix ([PR #53](https://github.com/gsemet/markdown-okf-schema-studio/pull/53)),
the final rename never overwrites: if another program creates a file with the same name between
the name choice and the rename, the paste is refused. The user then sees VS Code's raw
"file exists" error.

## Expected

- Either pick the next free name and retry the rename once (the name choice already avoids
  existing files), or show a clear message ("An image with this name was created meanwhile;
  paste again") and remove the hidden file.
- Recommended: retry with the next free name, because the user's intent is unambiguous.
- Unit test for the race path.

Needs PR #53 merged first.
