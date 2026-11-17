# A hidden `.partial` image can be left behind after a crash

Since the pasted-image fix ([PR #53](https://github.com/gsemet/markdown-okf-schema-studio/pull/53)),
a pasted image is first written to a hidden `.partial` file, then renamed into place. If the
extension host dies between the write and the rename (crash, window closed, machine sleep), the
hidden file stays in the user's image folder forever.

## Expected

- Decide and implement a cleanup: for example, remove `.partial` files older than a short age
  from the target folder at the next paste into it, or at activation for known image folders.
- Never delete a file that is not ours (exact naming pattern only).
- Unit tests for the cleanup rule; note the behaviour in the README image-paste section.

Needs PR #53 merged first.
