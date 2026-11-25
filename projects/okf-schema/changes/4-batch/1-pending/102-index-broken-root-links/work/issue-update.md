An update to the comment above, before any code. The change will also cover:

- `validate` will report W2 for broken links in `log.md` too, so an old entry linking to a deleted file is warned.
- Percent-encoded paths (`my%20file.md`) will be decoded before a link is checked.
- `index` will keep your summary however the subdirectory link is written: `tables/`, `./tables/` or `./tables`.
- `stats` will count broken links with the same check as `validate`.

No date yet; the pull request will be linked here.
