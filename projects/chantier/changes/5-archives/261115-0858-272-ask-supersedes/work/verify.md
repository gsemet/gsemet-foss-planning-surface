# verify.md CR-272
Head: 43e37194d54f6e9996c59c41e3ac766d13e368e8
- Cases 1-7 by hand in scratch batch (worktree CLI, `chantier asks -- <text>`): same-CR supersede (cr-101 vs CR-101), pr-in-draft supersedes ready-to-merge, question/blocked untouched and never superseding, two CRs independent, read ask untouched, two stack asks supersede; second line "A-k superseded by A-n (marked read)"; events: ask carries cr, asks-read has superseded_by. All as spec.
- `just check`: passed (172 tests).
