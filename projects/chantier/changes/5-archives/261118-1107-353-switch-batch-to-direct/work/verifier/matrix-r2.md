# Matrix probe r2

Head: 9433f8377cf3ca62d1eb5b3c17347243751e42ab (committed, not pushed)

Command (worktree, in-process, shipped code):
`uv run --no-sync --project . pytest skills/chantier/scripts/cli/tests/test_rail_refusals.py -k makes_it_direct -v`
Output: 3 passed in 1.32s (host_cell0, host_cell1, host_cell2), at 9433f837.
The test opens a Foreman batch (env set before `open`, so chief_transcript is recorded), Foreman claims n1, Chief claims n2.

| Cell | Param | Result |
| --- | --- | --- |
| Claude Code, CoS transcript recorded | host_cell0 (claude, CLAUDE_CODE_SESSION_ID=uuid-chief) | PASS: batch.json steering direct; one `steering` event direct/uuid-chief; output line `steering direct: ...` without "epoch"; status line " steering direct (the Chief of Staff) "; `status --refresh --epoch 1` exit 3; `take` skeleton "Steering: the Chief of Staff" |
| Copilot, CoS transcript recorded | host_cell1 (CHANTIER_HOST=copilot, COPILOT_AGENT_SESSION_ID=uuid-chief) | PASS: same assertions |
| Either host, none recorded | host_cell2 (claude, no env) | PASS: steering stays foreman, output == ["transcript uuid-chief"], no steering event |

Card-text-only cells (checked at 9433f837, files read in the worktree):
- Claude Desktop, silent Foreman stopped by CoS: chief-of-staff.md:1589-1594 (bullet 5, "Switching to direct mode") names `mcp__ccd_session_mgmt__stop_session` on the user's yes; hosts/claude-code.md:38 has the row, marked unproved with the trial. OK.
- Claude Code under Remote Control, silent Foreman: chief-of-staff.md:1592-1594 "say the stop needs the machine (stopping a session from the phone is unproved), name the session and wait"; bullet 4 (l.1586-1589) keeps the live-Foreman path under Remote Control; claude-code.md:38 "From Remote Control: unproved". OK.
- Copilot, silent Foreman: chief-of-staff.md:1592 "Copilot: none recorded, so the user stops it"; hosts/copilot.md has no stop-session means (rg for stop_session finds nothing). OK.

Verdict: all cells hold.
