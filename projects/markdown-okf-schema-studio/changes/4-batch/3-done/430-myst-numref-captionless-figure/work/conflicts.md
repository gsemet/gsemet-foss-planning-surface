# Conflicts: CR-430 restacked on CR-428

Rebase of `chantier/batch-06/cr-430-bug-swrs-myst-019-s-numref-scenario-cont` (one commit,
6d76d240 "test: prove a numref to a captionless figure shows its number") onto CR-428's local head
f28463c5 (which sits on CR-425 0b5005d and CR-424). New head: 585983ae, commit message unchanged.

## Hunks

### `requirements/tiers/log.md`, section `## 2026-11-20`, after the CR-429 entry

- Base side (HEAD, CR-425): the entry `### Real-window test flakes (CR-425)`.
- CR-430 side: the entry `### Numref to a captionless figure or table, tested (CR-430)`.
- Choice: both entries kept, word for word, CR-425's first and CR-430's after it, separated by a
  blank line (stack order: CR-430 lands after CR-425). The requirements guidelines order dates
  newest first and set no order inside a date. No byte-order mark before or after (the file starts
  with `# U` on both sides). No conflict markers left.

`requirements/tiers/swrs/myst/SwRS-MDOKFSTUDIO-MYST-019.md` and
`test/core/render/mystFeatures.test.ts` merged automatically.

## Generated blocks

`just requirements-update` run after the resolution: `0 indexes updated`, `0 requirement OKF
projections updated`; nothing to regenerate (the W2 broken cross-link warnings are pre-existing).

## Fast gate

Command, as run in the worktree at 585983ae: `just check`. Result: pass, exit 0 (the last steps:
`okfreq update-coverage --check` 0 files would change; main paths 92 StRS checked, all valid; use
case diagrams 93 StRS checked, all parse). Raw log: `work/gates/conflict-resolver-just-check.log`.

Not pushed.
