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
