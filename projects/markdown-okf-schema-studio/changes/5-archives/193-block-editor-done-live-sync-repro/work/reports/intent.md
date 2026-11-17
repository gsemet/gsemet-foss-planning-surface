# Done while the block editor is still syncing duplicates the source

Source: demo video track B, 2026-10-28 (observed while scripting).

Selecting text inside a block editor while live sync is in flight, then clicking Done, left the
source duplicated and the editor stuck on "Saving Markdown...". Data-integrity risk: reproduce,
then guard Done against an in-flight sync.

## Decision (user, 2026-10-28)

Not a 1.0.0 blocker. Stays in the backlog; act only once reproduced, after the release.
