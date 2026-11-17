# A live view of the batch's PRs that refreshes by itself

The user's word, 2026-11-15, during batch-18 (11 PRs ready at once, merged in several passes): "a 'monitor PR' that refreshes by itself so that I know which PR is merged. Refresh every 10 s for example, from the CLI." P1, for after the release.

Today the user learns a PR's state from the Chief of Staff's lines, which go stale as soon as they merge one (a PR turns conflicting, another is still in draft, a merge did not go through). Wanted: a view, started from the CLI, that refreshes itself (about every 10 s) and shows each PR of the running batch with its CR, its state on the forge (open, draft, merged, conflicting, checks running or green) and whether it is ready to merge now.

To grill: where it shows (terminal, the web board, the CR board pane), the refresh rate against the forge's API limits, and what it shows once every PR is merged.