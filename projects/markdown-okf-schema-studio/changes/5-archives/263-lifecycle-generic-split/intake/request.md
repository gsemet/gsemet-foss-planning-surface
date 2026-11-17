# 263: split the change request process from the project rules

Keep working without Chantier, but make `change-requests-lifecycle.guidelines.md` hold only the
generic process, move what is specific to this project to other guidelines, and give them a clear
precedence in `AGENTS.md` and the constitution. Align vocabulary and folder names on Chantier 0.5.0.

- Intent: [01-intent.md](../01-intent.md)
- Audit, approved by the owner: [02-audit.md](../work/02-audit.md)

## Owner's decisions (2026-11-05)

| Topic | Decision |
| --- | --- |
| Vocabulary | Aligned on Chantier, as in the audit's table |
| Stage folders | `1-inbox`, `2-backlog`, `3-requests`, `4-archives`, `5-trash` |
| Content | A pure move, apart from the precedence and the inconsistencies the audit lists |
| Project rules | Several guidelines, by theme |
| Release guideline | Split in this CR |
| D1 | Keep `ORCHESTRATOR.md` and `just orchestrator` |
| D2 | Names only: `00-request.md` becomes `03-change-spec.md`, `02-decisions.md` becomes `02-answers.md`, `reports/` and `reviews/` go under `work/`; `task.md` and `rules.md` stay |
| D3 | The links of the local documents are rewritten by script at the rename |

The audit's differences with Chantier stay out of this CR.
