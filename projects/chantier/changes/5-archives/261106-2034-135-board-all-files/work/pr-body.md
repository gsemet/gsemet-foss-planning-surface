## Why

On the CR board, an inbox or backlog item opened as the list of its top-level Markdown files. An
item that holds only `intake/request.md`, such as `drivers-sonnet`, showed an empty list.

## What changes

- `loadPage` in `hooks/register.tsx` drops the filter of the `items` page: it lists every entry of
  the folder, files of any type and sub-folders, as the `dir` page does. A sub-folder opens as a
  `dir` page and a file as a `doc` page, with the checks they already have (200 KB, UTF-8).
- The comment of `showCr` says so.
- `hooks/register.test.tsx`: the test of the item's list now expects `notes.txt`; a new test takes
  an item holding only `intake/request.md` from its page to `intake/`, to `request.md`, which
  opens. The test's fake `fs.list` now reports a registered sub-folder as a `dir`.

The README says nothing about Markdown files only, so it does not change.

## Out of scope

The sheet of a CR with a `STATUS.json`, and the board's other pages.

## Evidence

`claude plugin test .` with the same `hooks/register.test.tsx` on both sides: before is 0f93c2a,
the commit under this one, with only the test file put in; after is e862777.

| Case | Before (`0f93c2a`) | After (`e862777`) |
| --- | --- | --- |
| Item holding only `intake/request.md` | fails: the list has no link, `Received: undefined` | passes: lists `intake/`, then `request.md`, which opens |
| Item holding `01-intent.md`, `02-more.md`, `notes.txt` | fails: `notes.txt` is not listed | passes: all three are listed |
| Whole run | exit 1, 19 pass, 2 fail | exit 0, 21 pass, 0 fail |

Checks at `e862777`:

- `claude plugin validate .`: exit 0, with the two known warnings (marketplace description, icon);
- `just check`: exit 0, 28 tests passed;
- long gate `just scenario`, local on Windows: passed;
- CI: `just check` passes on Linux, macOS and Windows, `just scenario` on Linux, none skipped. CI
  does not run the mod's tests: `claude plugin test .` above is what covers this change.

Not shown: the board in a real pane. The tests stand in for the file system and draw no pane, and
the plugin loads only from the main checkout, so open the board in a session once after the merge.
