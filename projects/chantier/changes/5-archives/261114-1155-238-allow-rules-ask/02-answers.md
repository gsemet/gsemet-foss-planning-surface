# Answers

The Chief of Staff with the user, 2026-11-13 (asked in French, recorded in English).

1. **The review of the recommended rules** (the user: "fais une revue générale de ces règles et
   dis-moi lesquelles on garde, lesquelles on peut enlever"): keep the five `git push` forms on
   `chantier/*`, `uv run --script *chantier.py *`, `gh pr create|edit|ready|checks|view`,
   `gh stack*` (the user: "gh-stack peut être installé, ça peut arriver"), the four `glab` MR and
   CI rules, and `SendMessage`.
2. **Releases stay asked** (the user, after the reason was given: "ok je comprends"):
   `gh release create*` and `glab release create*` leave the recommended set, its table and its
   block. A release is rare, public and irreversible; the release driver already waits for the
   user's `release go`; without the rule the host's own check is a second guard at publication.
   P10 no longer holds the two release commands, so it checks 15 commands on a GitHub project.
   The "release's publication" line of `chief-of-staff.md` ("Forge permissions") says that the
   publication stays asked by the host, by design, and is not a missing rule.
3. **The Chief of Staff asks, and writes on the yes** (the user: "tu les mets chez moi et tu
   t'arranges pour que quand l'utilisateur ne les a pas, le chief of staff pose la question de
   les rajouter", then "mets le skill à jour et ma config"): when P10 warns, at the first turn of a
   session and at a batch's preflight, the Chief of Staff asks one question: add the rules P10
   named to `~/.claude/settings.json`? It names each rule and its risk (the "Risk accepted" column).
   On the yes it adds exactly those rules to `permissions.allow`, merging with what is there
   (never replacing, never removing), keeps the file valid JSON, runs `preflight` again and says
   what P10 says now. On a no it says once what will be refused (a Driver's force push after a
   rebase goes Driver → Foreman → Chief of Staff), and does not ask again in the session.
4. **The exception is written down.** `AGENTS.md` ("chantier writes only in the planning
   folder") and `hosts/claude-code.md` ("chantier never writes the user's settings: preflight's
   P10 compares, the user adds") gain one named exception: the Chief of Staff adds the allow
   rules P10 named to the user's `~/.claude/settings.json`, on the user's yes, and nothing else
   there. If the host refuses the edit (auto mode's classifier refused it once on 2026-11-13), the
   Chief of Staff says so with the refusal's text and gives the block to paste, as today; no
   workaround.
5. **The user's own config** is already done (2026-11-13): every kept rule is in the user's
   `~/.claude/settings.json`; `preflight` says P10 "1 of 16 not allowed", `gh release create`,
   on purpose.
6. **Order:** after CR-221 (python-inline-deps), in batch-17: the CLI's command list
   (`commands.py`, `_SAMPLES`) changes, and no CR that touches Python runs during that rework.
7. **When the write fails** (the user: "le chief of staff demande, s'il n'y arrive pas il donne
   la ligne à exécuter. Ça peut arriver si en remote, le classifier peut interdire ça, il faudra
   que l'utilisateur se connecte en physique"): answer 3 holds; when the host refuses the edit
   (typically under Remote Control, where auto mode's classifier may forbid it), the Chief of
   Staff gives the user one command line to run at the computer that adds exactly the rules P10
   named (a merge into `permissions.allow`, never a replace), for the user's shell, and says it
   needs the user at that computer, not on the phone. This replaces "the block to paste" of
   answer 4.
8. **`init` checks everything for the user** (the user: "pour moi quand on fait
   `/chief-of-staff init` ça ferait toutes les vérifications nécessaires pour le client"): the
   `init` tour runs every check a user's machine needs (the preflight's P5, P9 and P10, the forge's
   rights and branch rules, the long gate in `AGENTS.md`), and for each missing piece asks and
   fixes it as above (the allow rules by answer 3 and 7); `init.md`'s "the tour writes nothing in
   the user's settings" changes accordingly.
9. **The README says to run `init`** (the user: "en notant dans la section README comment
   installer d'appeler init"): the README's install section ends with the step to run
   `/chief-of-staff init` once after installing, and says what it checks and fixes.
10. Whatever the answers leave open takes the specification's defaults, listed as open points.

## Decisions after the specification (they replace the open points they name)

The Chief of Staff with the user, 2026-11-13 (asked in French, recorded in English).

- **`init` installs the forge tools, on the user's yes** (the user: "init recommande d'installer gh
  si nécessaire, avec l'extension stack, essaye de faire les modifs, et s'il n'y arrive pas donne
  les commandes à l'utilisateur"). This replaces open point 1 for the tools: when the project's
  forge is GitHub and `gh` is missing or not logged in, or the `gh stack` extension
  (github/gh-stack) is not installed, `init` recommends it, says why (the stack driver then makes
  the stack on GitHub with it), asks, and on the yes runs the install itself with the platform's
  usual installer (for instance `winget install --id GitHub.cli` on Windows, `brew install gh` on
  macOS, the distribution's package on Linux; `gh extension install github/gh-stack`); `gh auth
  login` is interactive and stays the user's. The same for `glab` on a GitLab project (no stack
  extension). When an install is refused by the host or fails, it gives the user the exact
  commands to run at the computer, as for the allow rules (answer 7). It checks the result
  (`gh --version`, `gh extension list`) and says what it found. Forge settings (rights, branch
  rules) stay as open point 1 says: the exact change for the user to make.