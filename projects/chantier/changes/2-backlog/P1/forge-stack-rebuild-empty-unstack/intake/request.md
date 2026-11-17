# `forge-stack rebuild` fails on the forge's empty unstack reply

Found 2026-11-17 in batch-22 by the stack driver, joining the release CR-307 (PR #259) on top of
stack #258: `$CHANTIER forge-stack rebuild` exited 4 with
`error: gh api -X POST repos/gsemet/chantier/stacks/258/unstack -F pull_requests[]=251 … : not JSON: `.
GitHub had already dissolved the stack: the unstack call answers with an empty body, which the CLI
tries to parse as JSON. The rebuild stopped half done (the PRs unstacked, no stack on the forge);
the stack driver recreated it with `forge-stack create` (stack #260).

Expected: an empty body on a 2xx unstack is a success; `rebuild` goes on to retarget and create,
then reads the stack back. Evidence: a test of the CLI's reply parsing on an empty body, and the
scenario. Also study whether a `rebuild` that fails after the unstack should say so plainly
("the stack is dissolved; run `forge-stack create`") rather than only the parse error.
