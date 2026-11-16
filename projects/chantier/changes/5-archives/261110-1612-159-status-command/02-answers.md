# Answers

## 2026-11-10, during batch-09

- The trigger:
  - After a `/compact`, the Chief of Staff answered "status" in free text, not in the approved
    Progress report shape.
  - The user asked: "pourquoi tu ne me montre pas mon tableau habituel ?"
  - The cause: the format is in `chief-of-staff.md` ("Reports", about 500 lines in all), and
    compaction keeps only a summary of it.
- The user: "alors il me faut une petit CR tres simple "/chantier:status" qui afficher le status.
  je pense qu'il faut recharger tout ou partie du skill pincipal. dis moi ce que tu en penses".
- The Chief of Staff proposed:
  1. a small skill `/chantier:status` (`skills/status/SKILL.md`) that runs `status --refresh`
     and `cost`, then shows the Progress report;
  2. the report format moved into a short card of its own (`references/report.md`), which
     `chief-of-staff.md` points to and which `/chantier:status` reads alone;
  3. not reloading the whole main skill: that would replay the first-turn introduction and
     reread about 500 lines on each status;
  4. optional, not in this CR: a CLI `status --report` that prints the table's skeleton;
  5. this CR goes after `changes-tree-v2` (CR-158), on the new tree.
- The user: "je suis d'accord". The proposal stands as written, without the CLI `--report`.
