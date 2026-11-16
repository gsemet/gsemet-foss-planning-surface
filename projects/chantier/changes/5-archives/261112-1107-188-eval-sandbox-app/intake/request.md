Build the eval sandbox project (user, 2026-11-12; first of two CRs, before `reproducible-evals`).

The eval campaigns get a frozen project to run on: https://github.com/gsemet/chantier-eval-sandbox (public, created by the user). This CR builds that project in a clear, clean, working state, so every eval starts from one known SHA-1.

What the user asked:
- Python with uv, with CI (GitHub Actions), and the CI is fast.
- A web application served by a Python backend; the HTML is written directly. No Node: only uv and hand-written HTML.
- The app exists and works before any eval; the CRs the evals run on it are real coding, not too long.
- The project carries what a chantier user's project carries: an `AGENTS.md` (how it builds, tests, ships and releases), a release procedure (version, notes, tag, GitHub release), so a batch can end with a release.

The project's source and the way its initial commit is produced belong to chantier's eval kit, so the base SHA-1 stays known and reproducible.