# Update okf-schema to the latest release

Update the project to the okf-schema release the owner just made. For the next batch. Filed on
2026-11-26 from the Chief of Staff session of batch-09, on the owner's word.

The owner, verbatim: "Il faudra aussi faire une CR sur le prochain batch sur la mise à jour de
okf-schema que je viens de release en 0.18, pas d'impact particulier."

Facts at filing:

- `pyproject.toml`, group `requirements`, already asks `okf-schema>=0.18.1`, and `uv.lock` pins
  0.18.1 (commit e9699d2a, 2026-11-25, "build: move the requirements bundle to okf-schema 0.18.1").
- PyPI lists 0.18.0 (2026-11-25 11:51Z), 0.18.1 (2026-11-25 12:09Z) and 0.19.0 (2026-11-26 06:58Z).
- So the version the project should move to is to be confirmed with the owner (see `02-answers.md`).

Expected by the owner: no particular impact. Not examined: the 0.19.0 changes and their effect on the
requirements bundle or on the schema validation the extension carries.
