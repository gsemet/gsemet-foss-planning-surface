# Session titles: the batch number last, in parentheses

## Behaviour

- A title that names a batch ends with ` (Batch <n>)`, `<n>` the batch's number on two digits
  as today (`(Batch 07)`, `(Batch 23)`), and the project name stands alone before the role:
  - Chief of Staff steering a direct batch: `[<code>] 💬 Project · CoS (Batch <nn>)`;
  - Foreman: `[<code>] ⚙️ Project · Foreman (Batch <nn>)`.
- Titles with no batch keep their form: `[<code>] 💬 Project · CoS`, `[<code>] 💬 Project ·
  Griller`, `[<code>] 💬 Project · Griller · <subject>`.
- When to rename does not change: the Foreman gets its title in its prompt; a later Foreman of
  the same batch has the same title; the Chief of Staff renames itself at `open --direct` and
  back at `close --yes`.

## Where

- `skills/chantier/references/session-start.md`, "Titles": the table and its examples.
- `skills/chantier/references/concepts.md`, "Session title".
- `skills/chantier/references/chief-of-staff.md`: the Foreman prompt's `<title>` with its example,
  and "Your title" of direct mode.
- Any other card, doc, scenario, test or CLI text that builds or quotes a title with
  `Project <nn>`: grep for it, and change each one the same way.

## Acceptance

- No card, doc, test or CLI text still shows a batch number between the project and the `·`.
- The examples in `session-start.md` include `[Battle] 💬 Chantier · CoS (Batch 17)` and
  `[Battle] ⚙️ Chantier · Foreman (Batch 17)`.
- `just check` passes.

## Open questions

None. The user gave the format, 2026-11-17.
