# Verify CR-333

Head: 47abe26dc00c97238759e40aea1383cdd9fb2c93

Verdict: VERIFIED

Claims, each judged at 47abe26dc00c97238759e40aea1383cdd9fb2c93:

1. Scenario checks 1-6 and the reworded check. Command: `just scenario --unit stack` in the worktree.
   Output: `ok  stack (github): 172/172 checks, 328.8 s` (log: work/verifier/stack.log). The transcript
   lines show: nearest earlier with a PR (reworded check, line 939); no earlier PR -> default branch, no
   start_on (1360); working earlier CR with PR, no two ready (1489); cancelled/merged skipped (1747);
   fix on default branch, release on top CR's branch (1917); parallel batch still default branch (2281).
   The case "CR right before has no PR, an earlier one has" is in section 13-bis (line 1191 onward) of the same transcript.
2. `start_on_for` is the new rule, `ready_top` removed with no caller left. Command:
   `grep -rn ready_top .` (outside .git) -> no output. `git show HEAD -- stacks.py` shows start_on_for
   returning the max-order candidate (not ended, not fix/release, lower order, with pr), else None;
   `stack_forms` kept; docstring rewritten; records.py comment updated.
3. No old-rule text left. Command: `grep -rnE "starts on the top|until the stack can form|ready part" README.md
   skills/chantier/references docs scenario/README.md` -> only two hits, both about the release's base
   (concepts.md:252, scenario/README.md:295), which is unchanged by the spec.
4. Cards' wording (`git show HEAD -- skills/chantier/references`): concepts.md Stack and Dependencies,
   foreman.md (take bases, "PR in draft", new "final-order take" bullet with queued-CR rule and ask),
   driver.md (CR Driver base paragraph with the cited rule, Ordering sentence, new "final-order take"
   paragraph with the push form) all match the specification.
5. PR description (work/pr-body.md vs `gh pr view 291 --json body`, same but one trailing blank line;
   head 47abe26 confirmed by `gh pr view`). Renders (sections, table, fold), Summary/Deliverables/Changes match the
   diff (stacks.py, records.py, three cards, scenario and its README), no images, no role name outside
   Internal references, Known gaps names the unrun units and Windows run. Test plan names `f86dc23`
   carried over a clean rebase: `git range-diff f86dc23~1...f86dc23 HEAD~1...HEAD` shows one differing
   hunk, a context line of driver.md from the new base; the CR's patch is unchanged. The Review box
   `approved at f86dc23` matches the log note `r1 approved at c103c07, committed as f86dc23`.
6. Scope: no `hooks/` or `types/` change (`git show --stat HEAD` lists none), no test file added.

Not run by me: `just check` on three OSes and the Windows long gate (due at the batch's top, as the
Known gaps say).

VERIFIED
