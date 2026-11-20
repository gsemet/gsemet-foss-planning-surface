Head: 47ac69759897d83bde917de9209bcf0a1b1b4bf0

Claims, each judged at 47ac697 from `git diff origin/main` in the worktree:
1. claude-code.md has one row starting "A Driver messages its steering session" (`grep -c` = 1); no "proved, same" left on it; names the final report/SubagentHandback; cites Studio batch-06, 2026-11-20; Steering text holds the five elements (nothing before end; final report; hand-back line first; anomaly as `$CHANTIER note`; ping needs no answer); terminal/VS Code keeps SendMessage to main; trial text present. OK.
2. "A Driver's silence" section present with six points, ping point marked Unproved with trial. OK.
3. foreman.md proof-of-death pointer and driver.md ping bullet present; no host tool named in them. OK.
4. Prompt/structure tests: `pytest skills/chantier/scripts/cli/tests -k "each_host_has_its_reference or driver_prompt or allow"` -> 32 passed.
5. CI at head: 5 checks SUCCESS (gh pr view 388).
6. PR description: renders, Summary/Deliverables/Changes match the 3-file diff, Known gaps names the two unproved items. Test-plan `<sha7>` placeholders are the Driver's to fill at ship; not a failure of the content.

VERIFIED

Description pass at 47ac69759897d83bde917de9209bcf0a1b1b4bf0 (posted body, `gh pr view 388 --json body`, against `git diff origin/main..HEAD`):
- Renders, Summary/Deliverables/Changes match the 3-file diff, Known gaps present, no images. OK.
- Review box: "Review: approved at `47ac697`". `$CHANTIER log 423 --batch batch-29` holds only `r1 inspector approved at 4ed0d56cc1a0ad51d1a4aa5f277cebc9ccaa8296` (the base; round 1 `wt_head=4ed0d56`, no `committed as` note). No approved-pass note names 47ac697. FAILS per the card.

NOT VERIFIED
