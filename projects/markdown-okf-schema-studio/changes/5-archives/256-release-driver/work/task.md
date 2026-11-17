# Task: Release driver role and "green heavy run on main before the version commit"

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-256
Branch: change-requests/256-release-driver

## Files (start here)

- `.agents/guidelines/change-requests-lifecycle.guidelines.md`: add the **release driver** role
  (Roles and models table: count 1 per release, Sonnet, never codes or reviews itself; started by
  the main session; owns the release CR folder `03-requests/NNN-release-x-y-z/` and its `STATE.md`
  header; may merge the PRs the release needs and the version PR, on the owner's standing
  permission for release work; uses coder/reviewer per round for any fix PR like a CR driver).
  Add a short section "Release driver" with its prompt (like "Driver prompt") and point to
  `release-process.guidelines.md` for the steps. Keep the rest of the guideline as is.
- `.agents/guidelines/release-process.guidelines.md`: rewrite "The order" as the release driver's
  steps, in the order decided in `00-request.md` (decision 2): owner says "release X" → agree on
  the version → notes and thread drafted, owner review → monitor and merge the release PRs and
  `main` → heavy run on `main` HEAD green (integration and stress, exact commit; red → fix PR,
  merge, run again; flake → re-run once, then red) → **then** version commit and version PR →
  monitor tag, Marketplace, Pages → replace notes → archive. State that the driver asks the owner
  nothing between the notes review and publication except a real blocker. Fix the change count
  rule: count commits of `vPREVIOUS..vX.Y.Z^` without merges and without `chore: version` commits
  of unpublished versions (1.3.2 case). Note that images may come from a CR `-assets` branch at a
  raw URL.
- `CONTRIBUTING.md` "How to Release": same step order (heavy run on `main` before the version
  commit), linking the guideline; keep commands accurate (`gh workflow run ci.yml --ref main -f
  heavy=true`, `gh run watch`, `gh run rerun <id> --failed`).
- `AGENTS.md`: the "When preparing a release" line also names the release driver.
- `.agents/guidelines/ci.guidelines.md` rule 14: one sentence that the version commit is made only
  after a green heavy run of `main` HEAD (release-process guideline), the version push's heavy run
  staying the final gate.

## Change

What `00-request.md` decides, and nothing more. Documentation only; no CI or script change
(decision 5). Write plainly, short sentences, consistent with the existing guideline style.

## Tests first

None (docs only). The gates below must stay green.

## Requirements

None (process docs, no product behaviour).

## Changelog

No user-facing line; if the changelog has a contributor section convention, follow it, else skip.

## Gates (foreground)

- `just check` (needs `node_modules`: run `fnm exec -- npm ci` first if missing; that install is
  allowed for this CR)
