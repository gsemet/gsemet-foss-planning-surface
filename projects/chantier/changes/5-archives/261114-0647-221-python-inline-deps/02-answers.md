# Answers

Grill with the user, 2026-11-13 (asked in French, recorded in English).

1. **Which dependencies.** Python packages, declared in the script's inline metadata (PEP 723),
   which uv installs. User's words: "les dependances python, tu utilises la PEP723". No vetted
   list in `AGENTS.md`.
2. **Scope of the refactor.** Split `commands.py` (3,198 lines) into modules, and replace
   hand-written code with libraries where one does the job (argument parsing, JSON models…),
   with no change of behaviour.
3. **Offline first run.** Acceptable: the first run needs the network to fetch the dependencies,
   as uv itself does; then uv's cache is enough.
4. **The board server.** May use a web framework (e.g. Starlette) for routes, JSON and live
   updates. The interface stays hand-written HTML, CSS and JavaScript with no compiler (native ES
   modules, one per view); the docs' screenshots use Playwright through a uv script. The user
   confirmed every other proposal: "toutes tes autres propositions me conviennent, javascript,
   playwright, ...".
7. **Code quality.** The code must be very clean, follow good standards and be modular, for easy
   maintenance. User's words: "juste assure toi que le code soit hyper propre avec de beau
   standard et modularité pour facilite la maintenance". It applies to this CR and to every board
   CR after it.
8. **Measured targets** (the user: "donne toi des cibles a atteindre (ligne max par fichiers,
   complexite,...)"; set by the Chief of Staff, 2026-11-13). Every Python file of the plugin,
   the existing ones included (`commands.py` first), meets them at the end of this CR, and
   `just check` enforces them on Linux, macOS and Windows, with tools run through `uvx` (no
   install by the user):
   - **File:** at most 400 lines; one responsibility per module; no import cycle.
   - **Function:** at most 50 lines; cyclomatic complexity at most 10 (ruff `C901`); at most 5
     arguments, 12 branches, 6 returns, 50 statements (ruff `PLR0913`, `PLR0912`, `PLR0911`,
     `PLR0915`); nesting at most 3 levels.
   - **Style:** `ruff format`; `ruff check` with `E`, `W`, `F`, `I`, `B`, `UP`, `SIM`, `C90`,
     `PL`, `RUF`, clean, no blanket `noqa`; line length 100.
   - **Types:** every function annotated; `mypy --strict` clean.
   - **Behaviour unchanged:** `just scenario` passes before and after on both forges; the
     structure tests stay few (`AGENTS.md`).
   - For the board's JavaScript and CSS, in the board CRs: ES modules, one per view, at most 300
     lines a file, at most 50 lines a function, complexity at most 10, checked by a linter run in
     `just check` as a repository tool (never shipped in the plugin).
   The user closed the grill: "sinon, c'est ok".
5. **Order.** This CR runs first, ahead of the board CRs: `visualization-backend` and
   `cr-summaries` wait for it (`depends.json`), and the others follow them.
6. **`AGENTS.md`.** Its rules "The CLI has no dependencies" and the board's "uses the standard
   library only" change to say dependencies come through PEP 723 inline metadata.

9. **The specification's nine defaults** (ruamel.yaml and its error wording, argparse kept, `cancel` on Windows unchanged, no package index declared, `requires-python >=3.11` with `no-build`, start-up time measured with no threshold, targets in CONTRIBUTING.md, tests under `skills/` held to the targets, `chantier.py.lock` committed and checked): accepted by the user, 2026-11-13: "Ok pour les propositions".


## Decisions after the specification

Asked by the Chief of Staff, 2026-11-13 (in French, recorded in English).

- The other open points stay at the specification's defaults.
