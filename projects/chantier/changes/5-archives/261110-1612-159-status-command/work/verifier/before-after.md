# Before / after, CR-159 status-command (head cd4b7cd)

Before (origin/main): no `skills/status/`, no `report.md`; the report format lives in a ~35-line "Reports" bullet plus "Cost" bullet inside `chief-of-staff.md` (530 lines); "status" is answered only by the Chief of Staff.

After: `skills/chantier/references/report.md` (99 lines) holds the format; `chief-of-staff.md` has one-line pointers; `skills/status/SKILL.md` runs `status --refresh`, `status`, `cost` and writes the report (sample: evidence/progress-report.md, from evidence/status-cost-raw.txt and evidence/batch-STATUS.md). No-active path: evidence/no-active.txt.
