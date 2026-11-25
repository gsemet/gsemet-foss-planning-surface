An update to the comment above, before any code:

- A leading `/` will read from the bundle root, as in OKF links: `/api/health-check` and `api/health-check` will name the same concept, from any terminal folder.
- On Windows, a name starting with `\` keeps its Windows meaning (a path from the root of the drive). Git Bash rewrites `/api/...` into a Windows path: write the name without `/`, or set `MSYS_NO_PATHCONV=1`.

No date yet; the pull request will be linked here.
