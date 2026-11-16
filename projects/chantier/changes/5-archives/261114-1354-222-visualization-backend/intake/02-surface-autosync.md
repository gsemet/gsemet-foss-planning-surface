# A planning surface stays in sync through its own autosync

Received 2026-11-13 from the Chief of Staff's session ([Battlestation] Chantier [Chief of Staff]):
the user asked to merge this request into visualization-backend, the backend being a server
with an "autosync" mode in its UI. The separate CR (surface-autosync) was deleted. The design
below was discussed with the user (their pick, "option A") before they decided the backend's UI
carries it; how the server mode fits it is to be re-checked with the user.

## What is wrong

With an external planning surface, the Chief of Staff commits and pushes the surface by hand
after each step that changes it and at each hand-back (chief-of-staff.md, "With a planning
surface"). That costs turns, is easy to forget, and leaves the surface behind while a batch runs:
the Foreman, a Griller and the Chief of Staff all write in it.

A surface may already ship its own autosync. The user's surface gsemet-foss-planning-surface
does: `scripts/ai-autosync-git.py` with `.agents/guidelines/autosync.guidelines.md`, named first in
its AGENTS.md (`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/`).

How that autosync works:
- every agent session in the checkout joins one group (`join . --owner-pid <host pid>`, detached);
- a file lock in `.git/ai-autosync/` elects one leader. The leader commits after 10 s of quiet
  (30 s at most), fetches, scans for secrets with Gitleaks, pushes LFS objects and pushes;
- when upstream moved, it never rebases on its own: it disables the group with a `blocked:`
  reason, and an agent integrates and runs `start . --enable-only`;
- staged changes or a found secret need the user's approval (`approve . <incident>`), never an
  agent's;
- start, stop and sync apply to the whole group; status prints the control state, the leader and
  the participants as JSON.

## The solution discussed (option A)

chantier does not own an autosync: the surface does, and chantier uses it.
1. Cards: when the surface's rules name an autosync, every chantier session that runs in the
   surface joins its group at session start: the Chief of Staff, the Foreman and a Griller.
   Drivers work in the code's worktrees and do not join, and a Griller in a surface worktree
   joins nothing. While the group is enabled, no session commits or pushes the surface by hand.
2. A `blocked:` group: the Chief of Staff handles it.
   - Upstream moved: integrate (no discarded change, never a force push), then
     `start . --enable-only`.
   - An approval needed: show the user the incident and wait for their word.
   The Foreman that meets it tells the Chief of Staff.
3. Read-only checks in the CLI (no git write, no dependency):
   - preflight warns when the surface names an autosync but its group has no live participant or
     is `blocked:`;
   - status shows one line with the autosync state, read from `.git/ai-autosync/status.json` and
     `control.json`.
4. "start autosync" / "stop autosync": the Chief of Staff runs the surface's own commands.

## Out of scope (as discussed)

- An autosync for the project's code repository.
- Porting the autosync into chantier's CLI, or a CLI command that wraps it: AGENTS.md wants a CLI
  with no dependency and no git write. The board/backend server is the named exception to weigh
  against this.
- A surface with no autosync keeps today's rule.
