# Verifier run at 4959358 (worktree CLI, scratch repo outside this batch)

Scratch repo: scratchpad/proj, remote git@gitlab.example.com, `open --parallel` two CRs, fake Foreman transcript
(1M in + 100k out, sonnet-5-5 = $3.00).

- No link: `STATUS.md` table header `| PR/MR |`.
- `status --refresh` (no epoch), GitLab link `.../-/merge_requests/7` on CR-101: `spent $3.00`, exit 0;
  batch.json `spent_usd` 3.0, `heartbeat` null (unchanged); table header `MR`, cell `[MR](...)`;
  CR-101 STATUS.md head `[MR](...)`.
- GitHub links `/pull/7`, `/pull/8` (both CRs): header `PR`, cells `[PR](...)`, batch and CR STATUS.md say PR.
- Not run: mixed table (code: any `/merge_requests/` gives MR); `status --refresh --epoch`.
- README line 247-248 reads "priced apart ... never in the batch's spend nor in its budget": true to
  chief-of-staff.md line 169-177. The only "not counted" left is about compaction calls, correct.

## Second pass

1. Card (chief-of-staff.md lines 125-141, 169-177) and SKILL.md "status?" row, item by item: Progress header
   (number and name, mode, slots, CRs done, spend, budget) yes; columns CR, subject, state, PR link, cost yes;
   cost table (Cost item, `--by role`) yes; "For you:" with "nothing" yes. Completion header (merged of total,
   spend, budget) yes; columns CR, subject, result, PR, rounds, cost yes; cost table per Driver type
   (`--by driver`) yes; what the batch did not prove yes; "For you:" with what `close` lists yes. Five icons each
   with its word yes, "belong to the report" yes. MR on a GitLab remote, in column and text, yes. Refresh with no
   epoch, leaving the heartbeat alone, stated in the Status item where `status` is given yes; SKILL.md row says
   `status --refresh` (no epoch) then `status`.
2. Heartbeat: `status --refresh --epoch 1` gave batch.json `"heartbeat": "2026-11-06T09:23:43Z"`; two seconds
   later `status --refresh` (no epoch) printed `spent $3.00` and batch.json still had
   `"heartbeat": "2026-11-06T09:23:43Z"`.
3. Own links: the CLI cannot hold two batches with links in one project (`open` refuses while any batch,
   landed included, stays until `close`). So I called status.py's real table writer `_rows_markdown` with each
   link set: GitLab `/merge_requests/9` gives header `MR`, cell `[MR](...)`; GitHub `/pull/7` gives `PR` and
   `[PR](...)`; no link gives `PR/MR`. Each table takes the word of its own rows.
