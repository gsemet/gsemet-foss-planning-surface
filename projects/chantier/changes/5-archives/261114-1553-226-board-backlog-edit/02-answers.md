
## Decisions after the specification

Asked by the Chief of Staff, 2026-11-13 (in French, recorded in English).

- **The page's language: both.** English by default and French, from one word file per language, built so that more translations can be added later. The prototype's French labels are the French file. Where an open point above says English only or French only, this answer replaces it.
- **JS and CSS lint: ESLint (and Stylelint, Prettier) through uvx**, on a Node.js taken from PyPI and pinned in the `justfile`, run by `just check`; Biome instead if it covers the targets more simply. `uv`, `just` and `git` stay the only tools installed by hand. The first CR that ships JavaScript (visualization-backend) adds it.
- The other open points stay at the specification's defaults.
