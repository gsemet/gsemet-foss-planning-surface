# The Foreman finds a conflict between ready PRs at the second one

Filed 2026-11-15 by the Chief of Staff from batch-18's retro (kept by the retro critic, reshaped by a Fable review), on the user's word "lance le tout dans le batch actuel".

Problem: ten CRs of parallel batch-18 edited the same files (driver.md, commands/driver.py, scenario/run_scenario.py, concepts.md); the conflicts surfaced only at a trial merge at 03:35, with ten ready PRs waiting unmerged; rebuilding them into a stack cost about 2.5 h, 11 conflict-resolvers, about 9 extra long gates and 14 extra Driver takes. foreman.md chains only CRs that edit the same lines, known before the start.

Fix (foreman.md, plain git, no CLI tool): at each hand-back `ready` while another ready PR of the batch is unmerged, the Foreman runs `git merge-tree --write-tree` of the new branch against each of them. On a conflict it sends one ask to switch the batch to a stack (`order mode`, CR-267), so the later CR is rebased once onto the earlier. Neutral on host and forge; on GitLab a stack is a chain of MRs merged bottom-up, unproved on a real GitLab (mark it).

Order in the batch: after the `ship` base CR.
