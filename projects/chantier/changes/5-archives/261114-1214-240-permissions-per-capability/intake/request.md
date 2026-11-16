Every capability chantier offers (a native stack made and rebuilt at night, a release run on the user's grant, a fix merged on a grant, force pushes after a rebase) works end to end under the host's permission check: chantier knows the commands each capability runs, checks them before the go, and offers the missing rules for the capabilities this batch will use.

The user (2026-11-14): "chantier doit être capable et flexible pour livrer une stack dans une variété de cas, et donc il faut donner au skill et au CLI les outils et instructions pour qu'il le fasse. Le classifier doit empêcher des cas non prévus, mais si chantier prévoit des stacks dynamiques, des releases autonomes, … il faut que tout fonctionne bien."

What happened: batch-17's Drivers had their force pushes refused (the `git -C <worktree> push …` form was not in the user's rules; preflight's P10 warned and nobody acted). CR-238 (allow-rules-ask, in batch-17) makes the Chief of Staff ask and add the missing rules, but keeps `gh release create` and `glab release create` out of the recommended set: a release granted to run on its own (`order grant releases=N`) would then stop at the host's prompt at night, with nobody to answer.

Wanted:
- one table, in the host reference and in P10's samples, of each capability and the exact commands its agents run (the forms with `git -C <worktree>`, `gh stack …`, `forge-stack rebuild`, `gh pr ready`, the tag push and `gh release create` for a release, …);
- preflight checks the rules for the capabilities this batch will use (its mode, a release CR, a grant), and the Chief of Staff offers to add exactly those before the go: release rules only when the user grants a release to run on its own, so an unplanned release still meets the prompt;
- a missing rule for a used capability is a preflight failure (all or nothing), not a warn: the night does not start with a capability that cannot work;
- where the host offers no way to try a rule ahead (auto mode's classifier judges at run time), say so in the host reference, and record any refusal's exact command and text, so the next table fixes it.
After CR-238; it extends CR-238's rules and its P10 check from one fixed set to sets per capability.
## After the critic's review (Fable, 2026-11-14)

- A table proves nothing: three rules are still "unproved" in `hosts/claude-code.md` (lines ~180, 186, 193), including the one that covers every `$CHANTIER` command, `forge-stack` included. Preflight runs a real, harmless trial per capability in the session's permission mode before the go (e.g. `gh stack view`, a `--dry-run` push form), and records the result.
- Extend to the forge's capabilities, probed before the go, not first called at 3 am: the stacks API (`forge_stack.py` calls it only at create, lines ~119, 133), the default branch's rules (required reviews, required checks, a merge queue, the allowed merge method; P9 reads only the `chantier/` branches' rules and only warns, `chief-of-staff.md:318-334`).
- This is a reversal of CR-238's choices (P10 warn-only, spec line 54; release rules removed "by design", lines 78-82) and of `chief-of-staff.md:366` ("warns and never fails"): say so in the specification.
- Copilot: the item says nothing for it; the specification names what applies there.