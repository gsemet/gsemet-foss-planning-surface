# Verify CR-194

Head: 76b0c8732447e9a7cdba26520b2290749f974a7e

All claims judged at 76b0c8732447e9a7cdba26520b2290749f974a7e (76b0c87).

1. The three edits are in the diff and nothing else changes (76b0c87). `git diff --name-only origin/main...HEAD` lists only skills/chantier/references/{chief-of-staff.md,foreman.md,hosts/claude-code.md}; the diff text matches sections 1-3 of the specification (new "Windows PowerShell 5.1" subsection between Prerequisites and Allow rules; the exact 11-form list and "exit 2" in both cards). PASS.
2. The list matches the CLI (76b0c87). From the worktree, `uv run --script skills/chantier/scripts/cli/chantier.py <cmd> --help` shows `--epoch` for order, foreman, status, agents, take, cancel, pause, and for none of round, handback, note, ship, gate, verdict, release, stack, asks, open, close, cost, seat, board, log, handoff, rules, playbook. The 11 forms equal the spec's table. PASS.
3. `git grep -n -e "--epoch" -- skills/chantier/references/` (76b0c87): every hit is on a listed command (foreman set/transcript, status --refresh/--stop-heartbeat, take, agents set, order done/merged/add --fix-for, pause). No card puts `--epoch` outside the list. PASS.
4. UTF-8 without BOM (76b0c87): first bytes of the three files are `# ` (35,32,...), no EF BB BF. PASS.
5. Gate pass (76b0c87): work/gates/20261112-134408.log first line `gate CR-194 branch ... head 76b0c8732447e9a7cdba26520b2290749f974a7e`, last line `result: pass at 76b0c8732447e9a7cdba26520b2290749f974a7e` (gitlab 586/586; just check and just scenario, per the Driver). Not re-run. Worktree clean. CI scenario job still running at my time: not waited for, not judged here.
6. PR description as posted (head on the forge is 76b0c87): renders (sections, table, details fold, no images); Summary, Deliverables, Changes match the diff; each proof names 76b0c87. The two unchecked boxes (`Verified at <sha7>`, `CI green at <sha7>`) are the pending process steps, not claims of fact. PASS.

Before/after evidence: card text only, no runtime behaviour; the before is the base text visible in `git diff origin/main...HEAD`, the after is the pushed head. No separate captures: nothing to capture beyond command outputs recorded above.

## Re-verify after a rebase onto origin/main

Head: c7adf7e56eea4ff32f74e8975751b8ebca6eee9b (old 76b0c87, base d6271d4 to dfc6740, which changed only skills/chantier/references/driver.md).

Judged again at c7adf7e (only what the move touched); the other claims stand from 76b0c87 since range-diff shows the patch unchanged (=).
- Diff scope (c7adf7e): `git diff --name-only origin/main...HEAD` still lists only chief-of-staff.md, foreman.md, hosts/claude-code.md; driver.md is not in the CR. PASS.
- --help list (c7adf7e): `--epoch` appears in `--help` of order, foreman, status, agents, take, cancel, pause; not in round, handback, note, ship, gate, verdict, release, stack, handoff. Same as before. PASS.
- `git grep -e "--epoch"` in the cards (c7adf7e): hits in foreman.md, chief-of-staff.md, claude-code.md remain on listed commands; copilot.md and status-layout.md hits are outside the CR diff. PASS.
- PR head on the forge is c7adf7e (matches the worktree HEAD). CI green at c7adf7e per the caller. The local long gate is running; not judged here.

VERIFIED
