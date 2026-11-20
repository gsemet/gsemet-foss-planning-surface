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

## 2026-11-20, the spec critic's first pass (7 points), settled by the Chief of Staff

Five text fixes (3, 4, 5, 6, 7) go to the writer without a question. The two that touch
behaviour:

- **Critic 1, an event built from forge data that fails its schema:** the models accept what a
  forge can return (null `merged_at` and `landed_at`; `head` of 40 or 64 hex characters, so a
  sha256 repository works). A refused event from a hub or board read is skipped and named in the
  hub entry's error or the page's error, and the other events are still written; the hub, the
  watcher and the PRs page never die on it, and a backlog write keeps its file. A refused event
  from a CLI command stays a code fault (`ValueError`).
- **Critic 2, a line of a type this chantier does not know:** `status` says
  `forge-journal.jsonl: line <n> is of type <t>, unknown to this chantier: update it`; a refused
  payload stays `unreadable`.
