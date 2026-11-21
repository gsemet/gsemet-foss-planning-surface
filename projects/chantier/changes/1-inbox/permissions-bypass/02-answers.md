Short name: `perm-bypass`

# Answers

1. perm-bypass-Q1 (2026-11-21): **What `gate` may run.** A. Only a command the project names in its rules (`chantier.yaml`), called by its name (e.g. `gate CR-430 scenario`); a free command is refused.
2. perm-bypass-Q2 (2026-11-21): **What `lease hold` may run.** A. Nothing: it keeps the lease live while a given process lives (`--pid`); the Driver starts its wait itself.
3. perm-bypass-Q3 (2026-11-21): **`uvx --from *`.** A. P10 writes the plugin's real path instead of `*`.
4. perm-bypass-Q4 (2026-11-21): **The push rule's second refspec** (audit, medium: `git push -u origin chantier/*` lets `git push -u origin chantier/x +HEAD:main` through). A. In this CR: P10 also recommends `deny` rules on `git push * +*` and `git push * *:main`, and `main`'s protection becomes a named prerequisite of P9.
5. perm-bypass-Q5 (2026-11-21): **Grilled enough.** A. Yes, specify now.
Spec critic: yes, it changes the CLI's refusals, what Drivers may do and the rules offered to the user.
6. perm-bypass-Q6 (2026-11-21, spec critic finding 1): **The old broad rules already in the user's settings.** A. P10 names each broad chantier rule it finds (`uvx --from * chantier *`, `uv run --no-sync --project * chantier *`...) as letting any command through, for the user to remove; nothing removes them for the user.
7. perm-bypass-Q7 (2026-11-21, critic finding 2, the spec's open question 5): **The dev-mode rules' `*`.** A. In this CR, P10 writes the checkout's real path into both dev-mode rules (`uv run --no-sync --project <checkout> chantier *`, `uv sync --locked --project <checkout>`).
8. perm-bypass-Q8 (2026-11-21, critic finding 7, the spec's open question 7): **The deny rules' scope and who writes them.** A. Accepted: in the user's settings they refuse any `+` push and any push to `main` in every project, with no prompt; P10 says so in one line; the Chief of Staff adds the two deny rules on the user's yes, and AGENTS.md and chief-of-staff.md ("adds ... and nothing else") change to say so.
9. perm-bypass-Q9 (2026-11-21, critic finding 9): **Existing projects with no gate command.** A. At its first turn the Chief of Staff sees a declared long gate with no command configured and offers the `long_gate.commands` entry, written on the user's yes; AGENTS.md's no-setup bullet says a runnable long gate needs it.
