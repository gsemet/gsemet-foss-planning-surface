# CR board pane: pending, ready and merged CRs are not shown

The CR board pane (the mod) does not show the backlog's states: the user sees no CR in pending (4-batch/1-pending), none in ready (3-ready), and none of the CRs merged in the running batch (batch-31, 2026-11-24).

From a quick look at hooks/register.tsx (not a diagnosis): the pane has a "Backlog" section built from index.backlog over PRIORITIES (3-ready, inbox, P1..P4), a "Merged (n of total)" section from index.merged, both created closed (the Section's second argument is false). Whether the pane fails to read these entries, or hides them while collapsed, or reads only part of the planning folder (a surface with an external planning folder, projects/<name>), is unknown. To find out: run the pane on the real surface at batch-31 and compare with `status`.

Wanted: the pane shows, for the running batch, its CRs by state (pending, working, ready to merge, merged), the 3-ready CRs, and the CRs merged in the running batch. The PR's Deliverables carry one screenshot of the pane from a real session at the PR's head (AGENTS.md).
