# Task T1 — alert paragraph opens the editor on the wrong lines

Implement `00-request.md` in `../markdown-okf-schema-studio-wt-171` on branch
`change-requests/171-alert-paragraph-opens-wrong-lines` (from `origin/main`, own `npm ci`).
Use the README snapshot as a fixture copy (under test fixtures), never the main checkout README.
Gates: `just check`; `uv run --group requirements okfreq validate --check-links --project-root .`;
normal CI, then heavy CI.
