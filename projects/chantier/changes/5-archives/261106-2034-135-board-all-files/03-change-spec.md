# The board lists every file of an inbox or backlog item

## Problem

On the CR board, an inbox or backlog item opens as the list of its top-level Markdown files. An item
that holds only `intake/request.md`, such as `drivers-sonnet`, shows an empty list.

## Change

In `hooks/register.tsx`, `loadPage` drops the filter of the `items` page: it lists every entry of the
folder, files of any type and sub-folders, as the `dir` page does. A sub-folder opens as a `dir` page
and a file as a `doc` page, with the checks they already have (200 KB, UTF-8).

Update the comment of `showCr`, the test "an inbox or backlog item opens as the list of its Markdown
files" in `hooks/register.test.tsx`, and any text in the README that says Markdown files only.

## Out of scope

The sheet of a CR with a `STATUS.json`, and the board's other pages.

## Done when

- A test shows an item holding only `intake/request.md`: its page lists `intake/`, and pressing it
  lists `request.md`, which opens.
- A file that is not Markdown is listed.
- `claude plugin validate .` and `claude plugin test .` pass, and `just check` passes.
