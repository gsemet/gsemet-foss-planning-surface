# 057 — contributing-security-overrides

From backlog `P3/contributing-security-overrides` (`01-intent.md` moved here). Started by the
overnight chain the user asked for on 2026-10-23 ("the 2 other CRs on top of the refactor").

## Decisions

1. For each `package.json` `overrides` entry (`csv-parse`, `linkify-it`, `markdown-it`):
   - find the advisory or the reason for it (git log / blame of `package.json`, `npm ls <pkg>`);
   - check whether it is still needed with the current lock;
   - remove it only if this needs no network. If removing it needs a relock that uses the
     network, keep it and say so in the PR.
2. Rewrite the CONTRIBUTING.md note: where the overrides are, one line per override with its
   reason, and when to revisit them.
3. No `src/` change. Gates: `just check`, `just visual`.
4. Branch `changes-requests/057-contributing-security-overrides`, created from
   `changes-requests/056-refactor-host-neutral-core`. The PR targets that branch: it stacks on the
   refactor PR #51, which is not merged yet. No assets branch.
5. Opus, 3 rounds. PR for an external reader. Commits end with `Assisted-by: Claude:Opus-5.5`.
   Never merge.
