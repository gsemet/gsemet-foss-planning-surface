Short name: `perm-bypass`

# Answers

1. perm-bypass-Q1 (2026-11-21): **What `gate` may run.** A. Only a command the project names in its rules (`chantier.yaml`), called by its name (e.g. `gate CR-430 scenario`); a free command is refused.
2. perm-bypass-Q2 (2026-11-21): **What `lease hold` may run.** A. Nothing: it keeps the lease live while a given process lives (`--pid`); the Driver starts its wait itself.
3. perm-bypass-Q3 (2026-11-21): **`uvx --from *`.** A. P10 writes the plugin's real path instead of `*`.
4. perm-bypass-Q4 (2026-11-21): **The push rule's second refspec** (audit, medium: `git push -u origin chantier/*` lets `git push -u origin chantier/x +HEAD:main` through). A. In this CR: P10 also recommends `deny` rules on `git push * +*` and `git push * *:main`, and `main`'s protection becomes a named prerequisite of P9.
5. perm-bypass-Q5 (2026-11-21): **Grilled enough.** A. Yes, specify now.
Spec critic: yes, it changes the CLI's refusals, what Drivers may do and the rules offered to the user.
