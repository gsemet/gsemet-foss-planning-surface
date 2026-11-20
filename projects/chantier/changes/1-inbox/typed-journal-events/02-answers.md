# Answers: typed-journal-events (Part A)

The grill is planning-server's (`2-backlog/P3/planning-server/02-answers.md`, Q1-Q30). The
answers below settle the open questions of this CR's first specification.

## 2026-11-20, settled by the Chief of Staff (the user asks no questions)

1. **Strictness of the four schemas.** Each model fixes each field's JSON type and only the
   formats that cannot change: `cr` matches `CR-<n>`, `head` a 40-character hex SHA. Open sets
   (`board@1.action`, `config@1.key`) stay plain strings: a new board action or configuration
   key must not force a new published version.
2. **Kind words in AGENTS.md and the cards.** Yes: this CR renames "`config` line" and "`board`
   line" to `config@1` / `board@1`, and AGENTS.md's `by: board` to `source: board`, in AGENTS.md,
   `chief-of-staff.md`, `hosts/claude-code.md` and `hosts/copilot.md`, so that no text names the
   old words.
3. **`docs/web-board.md`, "The signal".** Yes: fix the wording there too (`config@1`, `source:`).
4. **A pydantic upgrade.** `test_event_types.py` compares a normalized form of each schema (the
   properties, their JSON types, `required`, the patterns), not pydantic's raw output; a
   generator-only change regenerates nothing and publishes nothing.
5. **A later part's `schemas.json` entry.** This CR adds a `just` recipe that writes the missing
   entries from `model_json_schema()` and never changes an existing one; the test checks the
   file.
