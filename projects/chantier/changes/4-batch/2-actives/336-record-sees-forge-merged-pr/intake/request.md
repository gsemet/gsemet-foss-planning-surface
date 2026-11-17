# The CLI sees a PR merged on the forge as landed

From the retro of batch-24 (2026-11-17), kept by the retro critic; the user (2026-11-17): put the five retro points in the batch.

The record held CR-330 as ready while its content was on main (the partial stack merged by the user at 18:58, PR 288 merged on the forge), so the board said "not landed" and `forge-stack create` was refused (HTTP 422 on the merged PR): the CLI recognises a PR merged on the forge, or whose patch-id is on main, as landed and tells the Foreman to record it.

