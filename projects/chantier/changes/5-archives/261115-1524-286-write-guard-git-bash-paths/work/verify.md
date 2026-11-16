# Verify CR-286

Head: 8c6964d573b5537d62dfb3106fb88903bb1cd359

Claims, all judged at 8c6964d:
1. `just mod` passes: validate ok, `claude plugin test .` 62 pass 0 fail (3 new tests listed pass).
2. New tests cover the spec's list and fail on the base: base 842b800 + new test file via `just mod`: 60 pass, 2 fail (Git Bash drive path test; Git Bash folder form test). The POSIX no-mapping test passes on both, as it should (unchanged behaviour).
3. Pane unchanged: `git diff origin/main --stat` touches only hooks/register.tsx, register.test.tsx, hosts/claude-code.md; the register.tsx hunks are fromGitBash/guardInside, judgeShell and the tool.call handler; isInside, onOpen, showPath untouched.
4. Refusal messages unchanged: diff shows only the compare call changed in the two refusal branches; message strings untouched.
5. claude-code.md sentence present in "The write guard" (diff).
6. CI at head: all 5 checks pass, per Driver note (gh pr checks 234 at 8c6964d), incl. scenario; not re-run by me.
7. PR body (work/pr-body.md) vs diff: Summary, Deliverables, Changes match; Known gaps names the missing release-notes entry; Review box "approved at 842b800" matches the log note "r1 approved at 842b800, committed as 8c6964d". `just check` claim relies on CI check x3 green.

VERIFIED

Description pass (posted body, `gh pr view 234 --json body`, judged at 8c6964d): test-plan boxes checked with SHA 8c6964d; Summary, Deliverables, Changes match the diff (3 files); Review box 8c6964d proved by log note "r1 approved at 842b800, committed as 8c6964d"; CI 5 of 5 pass (`gh pr checks 234`); Known gaps present; internal reference only in the last section; no STALE mark.

VERIFIED
