# Intent

When the Chief of Staff starts, it checks that the batch's forge operations will go through:
on GitHub, or on GitLab when the project's remote is there. It says what is missing at the
first turn, before any go, and not when a Driver is refused in the middle of the night.

## Origin

Batch-15, night of 2026-11-12 to 13. The stack driver's 14 `--force-with-lease` pushes, on
`chantier/batch-15/*` branches, were refused to the Foreman. The Chief of Staff's own run of
them, a PowerShell loop, was refused too by the auto mode classifier, which gave no reason. The
stack waited until the user's word in the morning ("Push oui"), after which the same pushes,
run as a script, went through. The user says this is not the first time (see the force-push
route of 2026-11-06).

## What exists today

- `preflight` P10 compares the recommended allow rules (`hosts/claude-code.md`, "Allow rules")
  with the settings *as written* and only warns. On this machine it warns "19 of 19 not found".
  Yet `~/.claude/settings.json` holds equivalent force-with-lease rules in another form
  (`PowerShell(git push --force-with-lease=chantier/* origin *chantier/*)`, …). So a warning
  that is always on goes unheard.
- P9 checks only that `gh` or `glab` is logged in. It checks neither the right to push to the
  repository, nor the branch rules, nor the token's scopes.
- An allow rule does not cover a command of another shape. A loop, a script or a `-C` path does
  not match a prefix rule, and the auto mode classifier then judges it alone.
- `chief-of-staff.md` "A refused force push", step 6, sends the user the exact command. That is
  right, but it comes too late in an unattended night.

## What the check should cover (to grill)

- Host side: would the commands a batch runs be allowed as the agents will write them?
  - push `-u` and push `--force-with-lease` on `chantier/` branches, from the worktree and with
    `-C`;
  - `gh pr create/edit/ready/checks`, or `glab mr …` and `glab ci status`;
  - the CLI itself;
  - `SendMessage`.
  The check should judge equivalence rather than the exact string, or name the precise rules
  to add.
- Forge side: can the logged-in account do what the batch needs?
  - push rights on the repository (e.g. `gh repo view --json viewerPermission`, or the GitLab
    project's access level);
  - branch rules that would refuse a force push on `chantier/*`;
  - the token's scopes, for example `workflow` when a CR touches `.github/workflows/`.
- When: the Chief of Staff's first turn, as P9 and P10 run now, and again at step 1 of
  "Starting a batch".
- What failing means: a warning with the exact block to add and the forge right that is
  missing. Whether a missing force-push right blocks a stack batch is a question for the user.

## Related

- [[force-push-route]]: the route of 2026-11-06, under which the Chief of Staff runs a refused
  push.
- Retro point 3 of the batch-15 morning report.

## Joined 2026-11-13: release publication (from the batch-15 retro, to grill)

Batch-15: 'gh release create v0.9.0' was refused to the Foreman by the permission check after 'just tag' passed (ask A-24); the Chief of Staff ran it on the user's word. The release's publication step is run by the user or allowed by a named permission rule, and the cards say which.

The start check names the release's publication (`gh release create`) among the rights the batch needs, next to the force push.
