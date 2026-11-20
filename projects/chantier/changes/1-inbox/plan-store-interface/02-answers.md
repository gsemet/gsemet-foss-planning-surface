# Answers: plan-store-interface (Part B)

The grill is planning-server's (`2-backlog/P3/planning-server/02-answers.md`, Q1-Q30). The
answers below settle the open questions of this CR's first specification.

## 2026-11-20, settled by the Chief of Staff (the user asks no questions)

1. **Writes the reference's methods cannot carry.** The interface adds `write_bytes(rel, data)`
   and `make_folder(rel, exist_ok)`; a copy and an append are a read then a write. Every
   published write goes through the store, so Part C can refuse it; no write stays outside.
2. **The board's Configuration save.** A named method, `write_config(data)`, published and
   checked by `check_publish`; the store's root stays the planning folder, and no path argument
   can leave it.

## 2026-11-20, the spec critic's first pass (9 points), settled by the Chief of Staff

Eight text fixes (2 to 9) go to the writer without a question; for 5, `<command>` is an optional
keyword of `check_publish` that the CLI's dispatch and each board route pass; for 6, the append
keeps the file's own bytes and line endings, and `restored.json` keeps its bytes; for 7,
`changes_lock(repo)` stays the callers' name and delegates to `repo.store.lock()`, no call site
moves. The one that touches behaviour:

- **Critic 1, the planning folder's `.gitignore`:** written through the store and never refused,
  like a local file; the writer commits it with the next change. Refusing every command after an
  upgrade would be a larger change, and a stale `.gitignore` could let the writer publish a local
  file.
