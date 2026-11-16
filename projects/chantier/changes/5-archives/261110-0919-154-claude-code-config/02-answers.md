# Answers

## 2026-11-10

- **One CR or three?** One CR. User's words: "Oui une seule CR, attention il y a déjà un document
  référence par coding agent, il faut bien le remplir et s'assurer qu'il sera utilisé au bon
  moment".
  - No new reference file: the configuration goes into the existing per-host reference
    (`skills/chantier/references/hosts/claude-code.md`; `hosts/copilot.md` for what applies to
    Copilot), filled in properly.
  - The CR makes sure that reference is read at the right moment by the roles that need it.
    Found: the Chief of Staff, the Foreman and the Drivers read `hosts/<host>.md`; the workers
    read only their card and `concepts.md` (`concepts.md`, "Starting an agent").
- **Push rule:** keep the current rule (`concepts.md` rule 8): a plain push when nothing is
  rewritten, `--force-with-lease` after a rebase; `git -C <worktree>` accepted. The reference
  recommends allow rules for both forms. (User picked the recommended answer.)
- **When the check runs:** at each batch's preflight, and once at the Chief of Staff's first
  turn (and in the `init` tour), with the JSON block to add. (Recommended answer.)
- **Severity:** a missing allow rule warns and never fails preflight (chantier works with no
  setup); a missing tool the batch needs (git, gh or glab, uv) fails it. (Recommended answer.)
- **Where the command-hygiene rules go** (one command per call, read before overwrite, no
  leading assignment): `concepts.md`, read by every agent, workers included; the host reference
  keeps what is proper to Claude Code (allow rules, auto mode, compaction). User's words, 2026-11-10:
  "Ok concepts."
- **Grilled enough** (2026-11-10): after the full restatement, asked "claude-code-config est-il
  assez grillé, et je lance le spec-writer sur les trois ?", the user answered "Parfait".
  Specification by the spec-writer. The points the docs do not confirm are written as
  unverified, not settled.

## The specification's open questions (2026-11-10)

- **Q1 glab:** yes, add `glab mr create*` and `glab ci status*`, Bash and PowerShell, same risk
  text. (Recommended.)
- **Q2 settings files:** P10 also reads `.claude/settings.local.json`; not managed settings.
  (Recommended.)
- **Q5 compaction:** the documented facts plus the values the tutorial already gives
  (`idleCompaction` on, `autoCompactWindow` 400000), marked as a recommendation, not as a proved
  fact. (Recommended.)
- **Q7 plain push rule:** keep `git push -u origin chantier/*`; a remote not named `origin` is not
  covered, and the reference says so. (Recommended.)
- **Q3, Q4, Q6** (which rules and tools P10 checks, PowerShell vs Bash per OS): too detailed
  for the user. User's words: "ce n'est pas un peu trop détaillé ça ?", "Trop détaillé laisse le
  vérifier faire son boulot", "Pareil, trop specific". Left to the Driver's judgment; the spec's
  recommendations stand as the default, and the Verifier proves the result.
- The spec's references to `skill-entry-points` were renamed `multi-session-chief-of-staff` by the
  Chief of Staff after the merge (no content change).
