Head: 224d0679dc13f42da41702b249915856fe001321

Verdict: VERIFIED (second pass: PR description; code claims carried from 224d067)

1. Code claims (findings/exit 3/order/read-only, exit 0 with gaps, exit 1 cases, tests 26 passed and
   `just test` 661 passed in 31.4 s, CI green at this head incl. scenario, docs/code placement, file
   sizes, review box `r1 approved at 8a88c556, committed as 224d0679`): carried from 224d067, head and
   code unchanged.
2. Real run, read-only, redone at 224d0679 with the worktree's code (`uv run --no-sync --project
   <worktree> chantier --project <surface>/projects/<name> validate`; the main checkout does not hold the
   command yet): agentic-planning-surface `7 gap(s) in 3 CRs` exit 0; chantier `14 gap(s) in 364 CRs`
   exit 0; markdown-okf-schema-studio `22 gap(s) in 407 CRs` exit 0; okf-schema `1 gap(s) in 1 CRs`
   exit 0; `grep -c '^error'` gives 0 for each. Equals the table in the posted description.
3. PR description (`gh pr view 345 --json body` equals work/pr-body.md apart from a trailing blank line):
   renders (sections, fold, tables), no images. Summary, Deliverables and Changes match the diff (carried
   from 224d067, claim 6). Test plan SHAs are `224d067`, no `<sha7>` placeholder. Known gaps holds only
   the measured Windows test time, no stale scenario bullet (scenario passed at this head). No role name
   outside Internal references. No `STALE` mark.

VERIFIED
