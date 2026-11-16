# Answers

The Chief of Staff with the user, 2026-11-13 (asked in French, recorded in English).

1. **One method, aligned versions** (the user: "ça donnerait 2 méthodes de déploiement… je pense qu'il
   faut qu'une seule méthode, en s'assurant que les versions soient bien alignées"): no second way to
   launch the CLI beside the first.
2. **Order** (the user: "B, laisse le rework se faire et insère une CR juste après"): CR-221 finishes as
   specified, PEP 723 included; this CR comes right after it, in batch-17, and the Python CRs still
   queued wait for it.
3. **A root `pyproject.toml`** (the user: "on passe à un pyproject.toml à la racine"): the package is
   declared once, at the repository's root, so `uvx --from git+https://github.com/gsemet/chantier@<ref>
   chantier` works with no `#subdirectory`.
4. **The ref is pinned in the skill** (the user: "le skill hardcode la version du ref à utiliser (script
   `just version` je crois) qui sera utilisé lors de l'uvx git+http"): `just version X.Y.Z` (and
   `just bump-version`) writes the ref the skill launches, so the skill and the package are always the
   same version.
5. **Dev mode** (the user: "en mode dev de chantier lui-même il faut pas que ça checkout quoi que ce
   soit, le skill doit avoir une détection 'je suis dans le checkout de chantier lui-même, le code est
   là je l'utilise directement' vs 'je suis installé en skill par un plugin par exemple'"): in
   chantier's own checkout the skill runs the local code, live, with no fetch; installed as a plugin
   it runs `uvx` at the pinned ref.
6. Whatever the answers leave open takes the specification's defaults, listed as open points.
## Decisions after the specification (they replace the open points they name)

Asked by the Chief of Staff, 2026-11-13 (in French, recorded in English).

- **Plugin mode runs `uvx --from "<plugin root>" chantier`** (the user: "je veux bien ce fonctionnement
  avec --from"), not `uvx --from git+https://…@v<version>`. One method, `uvx --from <source> chantier`;
  only the source differs: the installed plugin's own folder (cards and CLI from the same commit, no
  fetch, offline, about 0.5 s per call), chantier's checkout in dev mode (live, no fetch), and
  `git+https://github.com/gsemet/chantier@v<version>` for a launch with no agent (a planning surface's
  `just board`), the version pinned where that launch lives. This replaces open points 1, 2 and 3: no
  release is needed for plugin mode to work after this CR, and no version mismatch between the cards
  and the CLI. The skill keeps no hard-coded ref for plugin mode; `just version` still writes the
  version into the root `pyproject.toml` and the documented `git+https` example. Measure that uvx from
  the plugin folder picks up a new plugin version after an update (cache keys), and say so in the PR.