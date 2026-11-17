# Release driver: green heavy run on main before the version commit

Type: docs (process) · Priority: P1 · Filed 2026-11-03 by the main session from the owner's
request. Starts **after 1.3.2 is published** (owner: "Met a jour la procédure après la 1.3.2").

## Owner request (verbatim, French)

> Ok il faut donc que la procédure de release note de faire les tests longs sur main s'assurer que
> tout passe PUiS faire le commit de release. Met a jour la procédure après la 1.3.2. Le but c est
> que cette procédure soit plus fiable pour moi ou je veux juste te dire de faire une release X, on
> se met d'accord sur la version, puis relecture de la release notes, puis tu monitors les PR et
> main en mergeant tout ce qu'il faut PUIS quand la release est presque garantie tu fait le commit
> de releases.
>
> Pour moi c'est un driver spécial qui doit le faire. Encode ca dans le workflow guideline, qui
> don't devra être compléter pour release driver avec les instructions du release guidelines.

## Why

1.3.0 and 1.3.1 were never tagged: the version push was the first real VS Code (heavy) run of
their code, and it went red both times (see the P1 backlog item
`release-stability-heavy-runs-before-version`). The owner wants to say "release X" and get a
release that is almost guaranteed before the version commit is made.

## Decisions (owner, 2026-11-03)

1. A **release driver** role, a special driver started by the main session, runs a release end to
   end. It is described in `.agents/guidelines/change-requests-lifecycle.guidelines.md` (role,
   model, lock, `STATE.md` header, what it may merge) and completed by
   `.agents/guidelines/release-process.guidelines.md` (the steps, notes, thread, publishing).
2. The release flow, in this order:
   1. Owner: "release X". Main session and owner agree on the version number.
   2. The release driver opens the release CR folder and drafts the notes and the thread; the
      owner reviews them (the only owner step after the version).
   3. The release driver monitors the open PRs that belong to the release and `main`, and merges
      what the release needs (owner's standing permission for release work), keeping the order
      of stacks.
   4. When everything is in `main`: dispatch the heavy run on `main` HEAD
      (`gh workflow run ci.yml --ref main -f heavy=true`) and wait for integration and stress to
      be green on that exact commit. A red job: fix PR, merge, heavy run again. A flake: re-run
      once, then treat as red.
   5. **Only then** the version commit (`just bump-version`, changelog heading, version PR,
      squash, merge). The version push's own heavy run (CI rule 14) stays the final gate.
   6. Monitor the version push through tag, Marketplace publish and Pages; replace the generated
      notes; archive the release CR.
3. The driver asks the owner nothing between the notes review and the publication, except a real
   blocker (round limit reached, a product decision).
4. Updating `CONTRIBUTING.md` "How to Release" so its step order matches (heavy run on main before
   step 2).
5. No CI change in this CR: automatic heavy jobs on PRs, the nightly run and a bump gate in
   `scripts/version.py` stay in the backlog item `release-stability-heavy-runs-before-version`.
